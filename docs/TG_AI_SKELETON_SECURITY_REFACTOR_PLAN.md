# TG Aiogram Skeleton Security Refactor Plan

## Goal

Use `tg-backup-watchdog` as the first production retrofit, then move the same security boundary patterns into `tg-aiogram-skeleton-module-based`.

## Core decisions

- No shared secret across trust domains.
- Separate principals:
  - admin/operator
  - producer/system integration
  - telegram user/chat
- Separate ingress boundaries:
  - admin API
  - producer HTTP ingest
  - Telegram listener
- Fail closed when a privileged ingress is enabled without a policy.

## What the skeleton must learn from watchdog

### 1. Principal-aware security context

Extend the current actor model so security decisions can use:

- `principal_type`
- `principal_id`
- `channel`
- `trust_level`
- channel-specific authorization attributes

### 2. Per-channel authentication boundaries

The skeleton must support different auth strategies for:

- Telegram updates
- HTTP/webhook ingress
- internal scheduled actions

Each boundary must authenticate and authorize independently.

### 3. Source-bound external producers

For non-Telegram ingress, the skeleton needs a reusable pattern for:

- explicit producer registry
- per-producer credentials
- allowed source bindings such as `host`, `job`, or equivalent external identity
- denial when a producer tries to impersonate another source

### 4. Centralized but boundary-applied policy

Policy can stay centralized, but enforcement must happen at the ingress boundary before business logic mutates state.

### 5. Fail-closed startup validation

If a privileged channel is enabled but its security policy is missing, startup must fail.

## Minimal skeleton changes

- extend `ActorContext` and related contracts
- add abstractions for external principals
- add source-binding policy checks for non-Telegram ingress
- add startup validators for security-critical config
- add tests for fail-closed behavior

## Non-goals

- do not copy watchdog business entities such as `host`, `job`, `run`, `state`
- do not copy the watchdog admin HTML
- do not hardcode backup-specific semantics into the skeleton

## Expected outcome

The skeleton becomes safe to use as a base for:

- admin bots
- bots with webhook/API ingress
- systems with multiple external senders
- future payment / giveaway / privileged flows

without falling back to a single shared token model.
