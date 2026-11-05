"""Exercise the installer against isolated homes, never the real user profile."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SHELL = os.environ.get('AI_CONFIG_PS_EXE') or shutil.which('pwsh') or shutil.which('powershell')


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT / 'install.ps1').is_file(), 'install.ps1 has not been implemented')
        work = ROOT / '.test-work'
        work.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='install-', dir=work)
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'home'
        self.env = os.environ.copy()
        # Let each PowerShell edition build its own module search path.
        # A Python child otherwise carries PowerShell 7 modules into Windows PowerShell.
        self.env.pop('PSMODULEPATH', None)

    def run_install(self, *args, ok=True, env=None):
        command = [SHELL, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                   str(ROOT / 'install.ps1'), '-TargetHome', str(self.home), *args]
        result = subprocess.run(command, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', env=env or self.env)
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def test_preview_has_no_writes(self):
        self.run_install('-WhatIf')
        self.assertFalse(self.home.exists())

    def test_fresh_install_and_repeat_preserve_existing_config(self):
        codex = self.home / '.codex'
        codex.mkdir(parents=True)
        config = codex / 'config.toml'
        config.write_text('personality = "pragmatic"\n', encoding='utf-8')
        self.run_install()
        self.assertEqual((codex / 'AGENTS.md').read_bytes(), (ROOT / 'codex/AGENTS.md').read_bytes())
        for name in ['direct-output', 'report-writing']:
            self.assertTrue((self.home / '.agents/skills' / name / 'SKILL.md').is_file())
        self.run_install()
        self.assertFalse((codex / 'backups').exists())
        self.assertEqual(config.read_text(), 'personality = "pragmatic"\n')

    def test_conflict_stops_before_any_new_file_is_written(self):
        skill = self.home / '.agents/skills/direct-output/SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text('keep existing skill', encoding='utf-8')
        self.run_install(ok=False)
        self.assertFalse((self.home / '.codex').exists())
        self.assertFalse((self.home / '.agents/skills/report-writing').exists())
        self.assertEqual(skill.read_text(), 'keep existing skill')

    def test_conflict_diff_shows_case_and_order_changes(self):
        agents = self.home / '.codex/AGENTS.md'
        agents.parent.mkdir(parents=True)
        original = (ROOT / 'codex/AGENTS.md').read_text(encoding='utf-8')
        variants = [original.replace('# Git', '# git'), '\n'.join(reversed(original.splitlines()))]
        for text in variants:
            with self.subTest(variant=text[:20]):
                agents.write_text(text, encoding='utf-8')
                result = self.run_install(ok=False)
                self.assertIn('<= ', result.stdout)
                self.assertIn('=> ', result.stdout)

    def test_replace_preserves_original_in_backup(self):
        agents = self.home / '.codex/AGENTS.md'
        agents.parent.mkdir(parents=True)
        agents.write_text('my original rules', encoding='utf-8')
        self.run_install('-ReplaceExisting')
        backups = list((self.home / '.codex/backups/ai-config').glob('*/manifest.json'))
        self.assertEqual(len(backups), 1)
        manifest = json.loads(backups[0].read_text(encoding='utf-8-sig'))
        self.assertEqual(len(manifest), 1)
        self.assertEqual(Path(manifest[0]['original']), agents)
        self.assertEqual(Path(manifest[0]['backup']).read_text(), 'my original rules')
        self.assertEqual(agents.read_bytes(), (ROOT / 'codex/AGENTS.md').read_bytes())

    def test_empty_existing_rule_can_be_backed_up_and_replaced(self):
        agents = self.home / '.codex/AGENTS.md'
        agents.parent.mkdir(parents=True)
        agents.touch()
        self.run_install('-Components', 'Rules', '-ReplaceExisting')
        self.assertEqual(agents.read_bytes(), (ROOT / 'codex/AGENTS.md').read_bytes())
        saved = list((self.home / '.codex/backups/ai-config').glob('*/00-AGENTS.md'))
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0].stat().st_size, 0)

    def test_skills_only_does_not_install_rules(self):
        self.run_install('-Components', 'Skills')
        self.assertFalse((self.home / '.codex').exists())
        self.assertTrue((self.home / '.agents/skills/direct-output/SKILL.md').exists())

    def test_custom_codex_home(self):
        custom = Path(self.temp.name) / 'custom codex'
        self.run_install('-Components', 'Rules', '-CodexHome', str(custom))
        self.assertTrue((custom / 'AGENTS.md').exists())
        self.assertFalse(self.home.exists())

    def test_default_home_respects_codex_home_environment(self):
        custom = Path(self.temp.name) / 'env codex'
        env = self.env.copy()
        env['CODEX_HOME'] = str(custom)
        result = subprocess.run([SHELL, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                                 str(ROOT / 'install.ps1'), '-Components', 'Rules'],
                                capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((custom / 'AGENTS.md').is_file())

    def test_junction_is_rejected(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        self.home.mkdir()
        env = self.env.copy()
        env['AI_CONFIG_JUNCTION'] = str(self.home / '.codex')
        env['AI_CONFIG_OUTSIDE'] = str(outside)
        result = subprocess.run([SHELL, '-NoProfile', '-Command',
                                 'New-Item -ItemType Junction -Path $env:AI_CONFIG_JUNCTION -Target $env:AI_CONFIG_OUTSIDE | Out-Null'],
                                capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.run_install(ok=False)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.home / '.agents').exists())


if __name__ == '__main__':
    unittest.main()
