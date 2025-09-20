# wait-for-db.ps1
$hostname = $args[0]
$cmd = $args[1..($args.Length-1)] -join " "

$env:PGPASSWORD = $env:APP_PG__PASSWORD

do {
    try {
        $result = psql -h $hostname -U $env:APP_PG__USER -d $env:APP_PG__DATABASE -c "\q" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Postgres is up - executing command"
            Invoke-Expression $cmd
            exit
        }
    } catch {
        # Ignore errors
    }
    Write-Host "Postgres is unavailable - sleeping"
    Start-Sleep -Seconds 2
} while ($true)