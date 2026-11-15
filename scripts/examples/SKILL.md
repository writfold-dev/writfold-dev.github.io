---
name: review
description: Review a change before it is delivered.
allowed-tools: Bash(writfold kb plan use *)
---

## Where the run's plan stands

!`writfold kb plan use review || true`

## Your task

Work the current step shown above, in order. When its gates are met, run
`writfold kb plan advance`; report a gate as passed only when it shows
`[satisfied]` or `[attested]`.
