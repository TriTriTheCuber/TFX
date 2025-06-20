# printmulti.ps1
foreach ($line in $args) {
    $parts = $line -split "\|"
    $text = $parts[0]
    $color = if ($parts.Count -gt 1) { $parts[1] } else { "White" }

    try {
        Write-Host $text -ForegroundColor $color
    } catch {
        Write-Host $text -ForegroundColor White
    }
}
