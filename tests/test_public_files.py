"""Check the public distribution without reading any real user configuration."""
import json
from pathlib import Path
import re
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublicFilesTests(unittest.TestCase):
    def test_configuration_examples_are_parseable_and_services_disabled(self):
        config = tomllib.loads((ROOT / 'codex/config.example.toml').read_text(encoding='utf-8'))
        self.assertEqual(config['personality'], 'pragmatic')
        mcp = tomllib.loads((ROOT / 'codex/mcp.example.toml').read_text(encoding='utf-8'))
        self.assertTrue(mcp['mcp_servers'])
        self.assertTrue(all(s['enabled'] is False for s in mcp['mcp_servers'].values()))

    def test_manifest_matches_distributed_skills(self):
        manifest = json.loads((ROOT / 'manifests/extensions.json').read_text(encoding='utf-8'))
        bundled = {s['name'] for s in manifest['skills'] if s['bundled']}
        self.assertEqual(bundled, {'direct-output', 'report-writing'})
        self.assertEqual(bundled, {p.parent.name for p in (ROOT / 'skills').glob('*/SKILL.md')})
        for name in bundled:
            text = (ROOT / 'skills' / name / 'SKILL.md').read_text(encoding='utf-8')
            self.assertTrue(text.startswith('---\n'))
            self.assertIn('name: ' + name, text.split('---', 2)[1])

    def test_public_text_has_no_common_credentials_or_fixed_windows_profile(self):
        patterns = [r'gh[pousr]_[A-Za-z0-9_]{20,}', r'github_pat_[A-Za-z0-9_]{20,}',
                    r'sk-[A-Za-z0-9_-]{24,}', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                    r'[A-Z]:[\\/]Users[\\/][^\s"<>]+',
                    r'[A-Z]:[\\/](?:CodexTools|Desktop)[\\/]']
        for folder in ['codex', 'skills', 'manifests', 'docs']:
            for p in (ROOT / folder).rglob('*'):
                if not p.is_file():
                    continue
                text = p.read_text(encoding='utf-8')
                for pattern in patterns:
                    self.assertIsNone(re.search(pattern, text, re.I), f'Unexpected private data pattern in {p.relative_to(ROOT)}')
        for p in [ROOT / 'README.md', ROOT / 'install.ps1']:
            text = p.read_text(encoding='utf-8')
            for pattern in patterns:
                self.assertIsNone(re.search(pattern, text, re.I), p.name)


if __name__ == '__main__':
    unittest.main()
