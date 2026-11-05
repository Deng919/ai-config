#requires -Version 5.1
<#
.SYNOPSIS
Install selected Codex guidance and personal skills; config.toml is never modified.
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [ValidateSet('Rules', 'Skills')]
    [string[]]$Components = @('Rules', 'Skills'),
    [string]$TargetHome = [Environment]::GetFolderPath('UserProfile'),
    [string]$CodexHome,
    [switch]$ReplaceExisting
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Assert-PlainPath([string]$Path) {
    $cursor = [IO.Path]::GetFullPath($Path)
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            $item = Get-Item -LiteralPath $cursor -Force
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Refusing redirected path: $cursor"
            }
        }
        $parent = Split-Path -Path $cursor -Parent
        if ($parent -eq $cursor) { break }
        $cursor = $parent
    }
}

$TargetHome = [IO.Path]::GetFullPath($TargetHome)
if (-not $CodexHome) {
    if (-not $PSBoundParameters.ContainsKey('TargetHome') -and $env:CODEX_HOME) {
        $CodexHome = $env:CODEX_HOME
    } else {
        $CodexHome = Join-Path $TargetHome '.codex'
    }
}
$CodexHome = [IO.Path]::GetFullPath($CodexHome)
$files = @()
if ($Components -contains 'Rules') {
    $files += @{ Source = (Join-Path $PSScriptRoot 'codex/AGENTS.md'); Target = (Join-Path $CodexHome 'AGENTS.md') }
}
if ($Components -contains 'Skills') {
    foreach ($name in @('direct-output', 'report-writing')) {
        foreach ($relative in @('SKILL.md', 'agents/openai.yaml')) {
            $files += @{
                Source = Join-Path $PSScriptRoot "skills/$name/$relative"
                Target = Join-Path $TargetHome ".agents/skills/$name/$relative"
            }
        }
    }
}

# Preflight every selected file before creating any directory or backup.
$pending = @()
$conflicts = @()
foreach ($file in $files) {
    if (-not (Test-Path -LiteralPath $file.Source -PathType Leaf)) { throw "Missing package file: $($file.Source)" }
    Assert-PlainPath $file.Target
    $cursor = Split-Path -Path $file.Target -Parent
    while ($cursor -and -not (Test-Path -LiteralPath $cursor)) { $cursor = Split-Path -Path $cursor -Parent }
    if ($cursor -and -not (Test-Path -LiteralPath $cursor -PathType Container)) { throw "Parent is not a directory: $cursor" }
    $exists = Test-Path -LiteralPath $file.Target
    if ($exists) {
        if (-not (Test-Path -LiteralPath $file.Target -PathType Leaf)) { throw "Target is not a file: $($file.Target)" }
        if ((Get-FileHash -LiteralPath $file.Source).Hash -eq (Get-FileHash -LiteralPath $file.Target).Hash) { continue }
        $conflicts += $file.Target
        Write-Output "Differences for $($file.Target) (< = installed, > = package):"
        Compare-Object -CaseSensitive -SyncWindow 0 -ReferenceObject @(Get-Content -LiteralPath $file.Target -Encoding UTF8) -DifferenceObject @(Get-Content -LiteralPath $file.Source -Encoding UTF8) |
            ForEach-Object { Write-Output "$($_.SideIndicator) $($_.InputObject)" }
    }
    $pending += @{ Source = $file.Source; Target = $file.Target; Exists = $exists }
}
if ($conflicts.Count -gt 0 -and -not $ReplaceExisting -and -not $WhatIfPreference) {
    throw 'Existing files differ. Review the differences, merge manually, or rerun with -ReplaceExisting to back up and replace.'
}
if ($pending.Count -eq 0) { Write-Output 'Already installed; no changes needed.'; return }

$backupRoot = Join-Path $CodexHome ('backups/ai-config/' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [Guid]::NewGuid().ToString('N').Substring(0, 8))
if ($conflicts.Count -gt 0) { Assert-PlainPath $backupRoot }
if (-not $PSCmdlet.ShouldProcess(($pending.Target -join ', '), 'Install selected files (back up existing differing files)')) { return }

$manifest = @()
if ($conflicts.Count -gt 0) {
    New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
    foreach ($file in $pending) {
        if ($file.Exists) {
            $saved = Join-Path $backupRoot (('{0:D2}-' -f $manifest.Count) + [IO.Path]::GetFileName($file.Target))
            Copy-Item -LiteralPath $file.Target -Destination $saved
            if ((Get-FileHash -LiteralPath $file.Target).Hash -ne (Get-FileHash -LiteralPath $saved).Hash) { throw "Backup verification failed: $saved" }
            $manifest += @{ original = $file.Target; backup = $saved }
        }
    }
    ConvertTo-Json -InputObject @($manifest) -Depth 3 | Set-Content -LiteralPath (Join-Path $backupRoot 'manifest.json') -Encoding UTF8
    Write-Output "Backups: $backupRoot"
}
foreach ($file in $pending) {
    New-Item -ItemType Directory -Path (Split-Path -Path $file.Target -Parent) -Force | Out-Null
    Copy-Item -LiteralPath $file.Source -Destination $file.Target -Force
    Write-Output "Installed: $($file.Target)"
}
Write-Output 'Done. Open a new Codex chat to check skill discovery. Merge configuration examples manually if needed.'
