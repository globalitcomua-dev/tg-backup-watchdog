param(
    [Parameter(Mandatory = $true)]
    [string]$CompanyName,

    [Parameter(Mandatory = $true)]
    [ValidateSet("ok", "warning", "failed")]
    [string]$Status,

    [Parameter(Mandatory = $true)]
    [datetime]$FinishedAt,

    [Parameter(Mandatory = $true)]
    [int]$ExitCode,

    [string]$FilesLine,
    [string]$DirsLine,
    [string]$AddedLine,
    [string]$ProcessedLine,
    [string]$SnapshotId,
    [int]$WarningsCount = 0,
    [string]$Message,
    [string]$HostName = $(hostname)
)

$statusIcon = switch ($Status) {
    "ok" { "✅" }
    "warning" { "⚠️" }
    default { "❌" }
}

$statusLabel = switch ($Status) {
    "ok" { "OK" }
    "warning" { "WARNING" }
    default { "FAILED" }
}

$watchdogText  = "[$HostName] [$CompanyName] $statusIcon $statusLabel Restic backup`n"
$watchdogText += "Finished at: $($FinishedAt.ToString('yyyy-MM-dd HH:mm:ss'))`n"
$watchdogText += "Exit code: $ExitCode`n"
if ($FilesLine)     { $watchdogText += "$FilesLine`n" }
if ($DirsLine)      { $watchdogText += "$DirsLine`n" }
if ($AddedLine)     { $watchdogText += "$AddedLine`n" }
if ($ProcessedLine) { $watchdogText += "$ProcessedLine`n" }
if ($SnapshotId)    { $watchdogText += "Snapshot: $SnapshotId`n" }
if ($WarningsCount -gt 0) { $watchdogText += "Warnings: $WarningsCount`n" }
if ($Message)       { $watchdogText += "Message: $Message`n" }

$watchdogText
