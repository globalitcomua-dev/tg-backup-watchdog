[CmdletBinding()]
param(
    [string]$ApiUrl = "http://127.0.0.1:8088",

    [string]$ProducerToken = $env:WATCHDOG_PRODUCER_TOKEN,

    [ValidatePattern("^[A-Za-z0-9_-]+$")]
    [string]$Host = $env:COMPUTERNAME,

    [datetime]$FinishedAt = (Get-Date),

    [ValidateRange(0, 1000000)]
    [int]$ErrorCount = 0,

    [ValidateRange(0, 315360000)]
    [int]$DurationSeconds = 0,

    [ValidateSet("en", "uk")]
    [string]$Language = "en",

    [string]$Message,

    [string]$RawText,

    [ValidateRange(5, 600)]
    [int]$RequestTimeoutSec = 30,

    [switch]$PassThru
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Format-CobianDuration {
    param(
        [Parameter(Mandatory = $true)]
        [int]$TotalSeconds,

        [Parameter(Mandatory = $true)]
        [ValidateSet("en", "uk")]
        [string]$Language
    )

    $hours = [math]::Floor($TotalSeconds / 3600)
    $minutes = [math]::Floor(($TotalSeconds % 3600) / 60)
    $seconds = $TotalSeconds % 60

    if ($Language -eq "uk") {
        return "Витрачено часу: $hours год, $minutes хв, $seconds сек."
    }

    return "Time elapsed: $hours hours, $minutes minutes, $seconds seconds."
}

function Build-CobianRawText {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Host,

        [Parameter(Mandatory = $true)]
        [datetime]$FinishedAt,

        [Parameter(Mandatory = $true)]
        [int]$ErrorCount,

        [Parameter(Mandatory = $true)]
        [int]$DurationSeconds,

        [Parameter(Mandatory = $true)]
        [ValidateSet("en", "uk")]
        [string]$Language,

        [string]$Message
    )

    $prefixTimestamp = Get-Date -Format "dd.MM.yyyy H:mm"
    $finishedAtText = $FinishedAt.ToString("yyyy-MM-dd HH:mm:ss")
    $durationText = Format-CobianDuration -TotalSeconds $DurationSeconds -Language $Language

    if ($Language -eq "uk") {
        $baseText = "[{0}] backup: {1} {2} ** Кількість помилок: {3}. {4} **" -f $prefixTimestamp, $Host, $finishedAtText, $ErrorCount, $durationText
    } else {
        $baseText = "[{0}] backup: {1} {2} ** Number of errors: {3}. {4} **" -f $prefixTimestamp, $Host, $finishedAtText, $ErrorCount, $durationText
    }

    if ([string]::IsNullOrWhiteSpace($Message)) {
        return $baseText
    }

    return "$baseText`nMessage: $Message"
}

if ([string]::IsNullOrWhiteSpace($ProducerToken)) {
    throw "ProducerToken is required. Pass -ProducerToken or set WATCHDOG_PRODUCER_TOKEN in the environment."
}

if ([string]::IsNullOrWhiteSpace($Host)) {
    throw "Host is required. Use only letters, numbers, underscore, or dash."
}

$ApiUrl = $ApiUrl.TrimEnd("/")
$finalText = if ([string]::IsNullOrWhiteSpace($RawText)) {
    Build-CobianRawText `
        -Host $Host `
        -FinishedAt $FinishedAt `
        -ErrorCount $ErrorCount `
        -DurationSeconds $DurationSeconds `
        -Language $Language `
        -Message $Message
} else {
    $RawText
}

$requestBody = @{
    text = $finalText
} | ConvertTo-Json -Depth 4

try {
    $response = Invoke-RestMethod `
        -Method Post `
        -Uri "$ApiUrl/api/v1/report/raw" `
        -Headers @{
            Authorization = "Bearer $ProducerToken"
        } `
        -ContentType "application/json" `
        -TimeoutSec $RequestTimeoutSec `
        -Body $requestBody

    if ($PassThru) {
        $response
        return
    }

    Write-Host "Report sent successfully."
    if ($null -ne $response.host) {
        Write-Host "Parsed host: $($response.host)"
    }
    if ($null -ne $response.engine) {
        Write-Host "Parsed engine: $($response.engine)"
    }
    if ($null -ne $response.status) {
        Write-Host "Parsed status: $($response.status)"
    }
} catch {
    Write-Error "Failed to send report to $ApiUrl/api/v1/report/raw. $($_.Exception.Message)"
    throw
}
