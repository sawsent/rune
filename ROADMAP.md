# Rune — Development Roadmap

## Phase 0 — Foundations (v0.5.0)
- [x] Commands: 
    - [x] add
    - [x] get
    - [x] ls
    - [x] update
    - [x] delete
    - [x] config
        - [x] storage
        - [x] encryption
    - [x] login
    - [x] logout
- [x] JSON filesystem storage
- [x] Client-side encryption only
- [x] Per-secret encryption keys supported
- [x] Clear internal domain models (Secret, Field, Namespace)
- [x] Context + Storage + Crypto separation
- [x] Encforce login before secret operations

**Exit criteria**
- [x] Fully functional local-only CLI vault
- [x] No architectural blockers for future expansion

## Phase 1 - Ergonomic improvements (v0.6.0)
- [ ] Introduce command:
    - [ ] move (move a secret from one place to another)
- [x] More easily create secrets with only 1 field
    - [x] No need to specify `--fields` for 1-field secrets
- [ ] Store config profiles for easy switching.
    - [ ] `rune config profile <profile>`
- [ ] Delete requires extra confirmation
- [ ] Introduce soft delete (hide)
- [ ] Introduce undelete for soft deleted secrets
- [ ] Hard delete requires encryption key

**Exit criteria**
- [ ] More usable UX
- [ ] No unwanted deletes
- [ ] Soft and hard deletes

## Phase 2 — Default-Key & Sessions (v0.8.0)
- [ ] Introduce default-key (session key) concept
- [ ] `rune session start --default-key <encryption-key>` / `rune session end`
- [ ] Background session daemon (local-only)
- [ ] Secrets encrypted with:
  - [ ] explicit key OR
  - [ ] default-key if active
- [ ] No keys written to disk

**Exit criteria**
- [ ] Ergonomic UX
- [ ] Secure in-memory key handling
- [ ] Session lifecycle clearly defined
- [ ] Rune is useful daily as a local developer vault


## Phase 3 — Data Model Hardening and unit testing (v1.0.0)
- [ ] Secret IDs as primary identifiers
- [ ] Namespaces fully abstracted from storage
- [ ] Import / export (encrypted)
- [ ] Backward-compatible secret versioning
- [ ] Pluggable encryption algorithms
- [ ] Testing implemented

**Exit criteria**
- [ ] Storage format stable
- [ ] Safe migrations possible
- [ ] Users can back up & move vaults


## Phase 4 — Server-Ready Architecture (v1.1.0)
- [ ] Storage interface supports remote backends
- [ ] Secrets always encrypted client-side
- [ ] Server stores opaque ciphertext only
- [ ] Username becomes first-class concept
- [ ] No server-side decryption possible

**Exit criteria**
- [ ] Same CLI works with local or remote storage
- [ ] Zero trust in server

