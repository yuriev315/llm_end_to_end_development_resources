# Start llama-server on Windows. Not run in the collection round.
$Here = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Kit = Split-Path -Parent (Split-Path -Parent $Here)
$Gguf = Join-Path $Kit "models\cpu_baseline\qwen2.5-1.5b-instruct-q4_k_m.gguf"
$Urlf = "$Gguf.url.txt"
$Bin = Get-ChildItem -Path (Join-Path $Kit "runtimes\windows_x86_64\llama_cpp") -Recurse -Filter "llama-server.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $Bin) { Write-Error "extract llama.cpp zip first"; exit 1 }
if (-not (Test-Path $Gguf)) {
  Write-Error "missing GGUF (weights are URL-only; see $Urlf)"
  if (Test-Path $Urlf) { Get-Content $Urlf | Write-Error }
  exit 1
}
& $Bin.FullName -m $Gguf --port 8080 --host 127.0.0.1 -c 4096 --alias qwen2.5-1.5b-instruct
