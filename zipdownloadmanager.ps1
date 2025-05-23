param (
    [string]$Url,
    [string]$Destination
)

$zipPath = "$env:TEMP\temp_download.zip"

try {
    Write-Host "⬇ Downloading from $Url..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $Url -OutFile $zipPath -UseBasicParsing

    Write-Host "Extracting to $Destination..." -ForegroundColor Green
    Expand-Archive -LiteralPath $zipPath -DestinationPath $Destination -Force

    Remove-Item $zipPath -Force
    Write-Host "Done!" -ForegroundColor Green
} catch {
    Write-Host "Download failed: $_" -ForegroundColor Red
    exit 1
}