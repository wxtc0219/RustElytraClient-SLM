$ErrorActionPreference = 'Stop'
$work = 'C:\Users\wxtc\Documents\deepseek-harness\default-workspace\rec-patch'
$javaBin = Join-Path $env:APPDATA 'PrismLauncher\java\java-runtime-delta\bin'
$lib = Join-Path $env:APPDATA 'PrismLauncher\libraries\org\ow2\asm'
$cfr = 'C:\Users\wxtc\Documents\deepseek-harness\default-workspace\cfr.jar'
$py = 'C:\Users\wxtc\AppData\Local\Programs\Python\Python312\python.exe'
$cp = "$lib\asm\9.10.1\asm-9.10.1.jar;$lib\asm-tree\9.10.1\asm-tree-9.10.1.jar;$lib\asm-analysis\9.10.1\asm-analysis-9.10.1.jar;$work\out"

function Strip-Bom([string]$p) {
    $b = [System.IO.File]::ReadAllBytes($p)
    if ($b.Length -gt 3 -and $b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF) {
        $t = [System.Text.Encoding]::UTF8.GetString($b, 3, $b.Length - 3)
        [System.IO.File]::WriteAllText($p, $t, (New-Object System.Text.UTF8Encoding($false)))
    }
}

foreach ($n in 'T.java','Patch4.java','Patch6.java','Patch7b.java','Patch8.java') { Strip-Bom (Join-Path $work "src\$n") }

& (Join-Path $javaBin 'javac.exe') -encoding UTF-8 -d (Join-Path $work 'out') (Join-Path $work 'src\T.java')
& (Join-Path $javaBin 'javac.exe') -encoding UTF-8 -cp $cp -d (Join-Path $work 'out') `
    (Join-Path $work 'src\Patch4.java') (Join-Path $work 'src\Patch6.java') `
    (Join-Path $work 'src\Patch7b.java') (Join-Path $work 'src\Patch8.java')
Write-Host "javac ok"

$orig = Join-Path $env:APPDATA 'PrismLauncher\instances\hjm\minecraft\backup\rec-original\RustElytraClient-1.21.1-beta1.6-260502_1913.jar'
if (-not (Test-Path $orig)) { throw "orig jar missing: $orig" }
$stage = Join-Path $work 'stage-release'
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
New-Item -ItemType Directory -Force -Path (Join-Path $stage 'dev\rstminecraft') | Out-Null

Add-Type -AssemblyName System.IO.Compression.FileSystem
$z = [System.IO.Compression.ZipFile]::OpenRead($orig)
foreach ($n in 'dev/rstminecraft/RustSupplyTask.class','dev/rstminecraft/RustElytraTask.class','dev/rstminecraft/TaskThread$TaskType.class','dev/rstminecraft/RustElytraClient$1.class','dev/rstminecraft/RustSupplyTask$1.class','dev/rstminecraft/RSTScr$ciScr.class') {
    $e = $z.GetEntry($n)
    if (-not $e) { throw "entry missing: $n" }
    [System.IO.Compression.ZipFileExtensions]::ExtractToFile($e, (Join-Path $stage $n), $true)
}
$z.Dispose()
Write-Host "extracted"

function Patch([string]$class, [string[]]$modeArgs) {
    $p = Join-Path $stage "dev\rstminecraft\$class"
    & (Join-Path $javaBin 'java.exe') -cp $cp @modeArgs 2>&1 | ForEach-Object { Write-Host "  $_" }
}

$supply = Join-Path $stage 'dev\rstminecraft\RustSupplyTask.class'
& (Join-Path $javaBin 'java.exe') -cp $cp Patch2 $supply $supply 2>&1 | ForEach-Object { Write-Host "  $_" }
& (Join-Path $javaBin 'java.exe') -cp $cp Patch7b $supply $supply 2>&1 | ForEach-Object { Write-Host "  $_" }

$task = Join-Path $stage 'dev\rstminecraft\RustElytraTask.class'
& (Join-Path $javaBin 'java.exe') -cp $cp Patch8 $task $task 2>&1 | ForEach-Object { Write-Host "  $_" }

$tt = Join-Path $stage 'dev\rstminecraft\TaskThread$TaskType.class'
& (Join-Path $javaBin 'java.exe') -cp $cp Patch4 enum $tt $tt 2>&1 | ForEach-Object { Write-Host "  $_" }
& (Join-Path $javaBin 'java.exe') -cp $cp Patch6 $tt $tt 2>&1 | ForEach-Object { Write-Host "  $_" }

$sw = Join-Path $stage 'dev\rstminecraft\RustElytraClient$1.class'
& (Join-Path $javaBin 'java.exe') -cp $cp Patch4 switchmap $sw $sw 2>&1 | ForEach-Object { Write-Host "  $_" }
$sw2 = Join-Path $stage 'dev\rstminecraft\RustSupplyTask$1.class'
& (Join-Path $javaBin 'java.exe') -cp $cp Patch4 switchmap $sw2 $sw2 2>&1 | ForEach-Object { Write-Host "  $_" }

$gui = Join-Path $stage 'dev\rstminecraft\RSTScr$ciScr.class'
& (Join-Path $javaBin 'java.exe') -cp $cp Patch4 gui $gui $gui 2>&1 | ForEach-Object { Write-Host "  $_" }

Copy-Item (Join-Path $work 'out\dev\rstminecraft\T.class') (Join-Path $stage 'dev\rstminecraft\T.class') -Force

Write-Host "--- verify ---"
& (Join-Path $javaBin 'java.exe') -cp $cp Verify $supply $task $tt $sw $sw2 $gui (Join-Path $stage 'dev\rstminecraft\T.class') 2>&1 | ForEach-Object { Write-Host "  $_" }

$out = Join-Path $work 'RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar'
& $py (Join-Path $work 'repack3.py') $orig $stage $out
Write-Host "BUILD DONE"



