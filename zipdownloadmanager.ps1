param (
    [string]$Url,
    [string]$ZipPath
)

$req = [System.Net.HttpWebRequest]::Create($Url)
$resp = $req.GetResponse()
$stream = $resp.GetResponseStream()
$totalBytes = $resp.ContentLength

$outFile = [System.IO.File]::OpenWrite($ZipPath)
$buffer = New-Object byte[] 8192
$read = 0
$readTotal = 0

function Show-Bar($percent) {
    $barLength = 30
    $filled = [Math]::Floor($percent * $barLength)
    $empty = $barLength - $filled
    $bar = ('#' * $filled) + ('-' * $empty)
    Write-Host -NoNewline "`r[$bar] $([int]($percent * 100))%"
}

while (($read = $stream.Read($buffer, 0, $buffer.Length)) -gt 0) {
    $outFile.Write($buffer, 0, $read)
    $readTotal += $read
    $progress = $readTotal / $totalBytes
    Show-Bar $progress
}

Write-Host "✅ Download complete!"
$outFile.Close()
$stream.Close()
$resp.Close()
