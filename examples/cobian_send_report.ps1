param(
    [Parameter(Mandatory = $true)]
    [string]$ApiUrl,

    [Parameter(Mandatory = $true)]
    [string]$ProducerToken,

    [Parameter(Mandatory = $true)]
    [string]$Host,

    [Parameter(Mandatory = $true)]
    [datetime]$FinishedAt,

    [Parameter(Mandatory = $true)]
    [int]$ErrorCount,

    [int]$DurationSeconds = 0,

    [string]$Message,

    [string]$RawText
)

$finalText = if ($RawText) {
    $RawText
} else {
    $formattedDate = $FinishedAt.ToString("yyyy-MM-dd HH:mm:ss")
    $hours = [math]::Floor($DurationSeconds / 3600)
    $minutes = [math]::Floor(($DurationSeconds % 3600) / 60)
    $seconds = $DurationSeconds % 60
    "[{0:dd.MM.yyyy HH:mm}] backup: {1} {2} ** Number of errors: {3}. Time elapsed: {4} hours, {5} minutes, {6} seconds. **" -f (Get-Date), $Host, $formattedDate, $ErrorCount, $hours, $minutes, $seconds
}

$body = @{
    text = $finalText
} | ConvertTo-Json -Depth 4

Invoke-RestMethod `
    -Method Post `
        -Uri "$ApiUrl/api/v1/report/raw" `
        -Headers @{
        Authorization = "Bearer $ProducerToken"
    } `
    -ContentType "application/json" `
    -Body $body
