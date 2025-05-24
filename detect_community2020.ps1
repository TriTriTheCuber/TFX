# detect_community.ps1

$cfgPath = "$env:AppData\Microsoft Flight Simulator\UserCfg.opt"

if (Test-Path $cfgPath) {
    $line = Select-String 'InstalledPackagesPath' -Path $cfgPath
    if ($line) {
        $match = $line.Line -replace '.*\"(.*)\".*', '$1\Community'
        $match | Set-Content -Path '_community_path.txt' -Encoding ASCII
    } else {
        'NO_INSTALLED_PATH' | Set-Content -Path '_community_path.txt' -Encoding ASCII
    }
} else {
    'NOT_FOUND' | Set-Content -Path '_community_path.txt' -Encoding ASCII
}
