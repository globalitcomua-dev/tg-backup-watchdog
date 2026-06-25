# Backup Watchdog

Backup Watchdog is a monitoring service for backup jobs.

It collects backup reports from different sources such as REST API, Telegram messages, Restic scripts, Cobian Reflector logs, and custom scripts.

## Current goals

- Receive structured backup reports
- Parse legacy Telegram backup notifications
- Detect failed, warning, and missing backups
- Send daily Telegram summaries
- Provide a web dashboard