# Nightly deploy for the Atelier gallery site.
# Rebuilds docs/ from the sealed Atelier directory (read-only), commits if
# anything changed, and pushes to GitHub, which republishes Pages.
# Run nightly by the Claude Code scheduled task "atelier-gallery-nightly-deploy".

$ErrorActionPreference = "Continue"
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$log = Join-Path $repo "deploy.log"
Set-Location $repo

function Log($msg) {
    $line = "{0}  {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg
    Add-Content -Path $log -Value $line -Encoding utf8
}

Log "start"
$build = & python (Join-Path $repo "build.py") 2>&1
Log "build: $build"
if ($LASTEXITCODE -ne 0) { Log "build failed, aborting"; exit 1 }

& git add -A | Out-Null
$changes = & git status --porcelain
if (-not $changes) { Log "no changes, nothing to deploy"; exit 0 }

$epoch = (Get-Content "D:\Users\MyPC\Dev\terrarium-atelier\epoch.txt" -Raw).Trim()
$stamp = Get-Date -Format "yyyy-MM-dd"
& git commit -q -m "Nightly build, Epoch $epoch ($stamp)" | Out-Null
$push = & git push -q 2>&1
if ($LASTEXITCODE -ne 0) { Log "push failed: $push"; exit 1 }
Log "deployed Epoch $epoch"
