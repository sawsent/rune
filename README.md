# rune

**rune** is a secure, local-first secrets management CLI designed for developers.

It lets you store, retrieve, and manage secrets safely on your machine, with **strong client-side encryption**, a clean namespace model, and an ergonomic workflow optimized for daily use.

Rune is intentionally simple: no servers, no accounts, no background services beyond what you explicitly start.

---

## Features

- 🔐 **Zero-trust by default**  
  Secrets are always encrypted client-side. Decrypted values never leave memory.

- 🗝️ **Per-secret encryption keys**  
  Each secret can use its own encryption key.

- 🗝️ **Multi-field secret storage**  
  Each secret can have multiple fields, allowing you to store complex secrets easily.

- 🧠 **Session-based default key (optional)**  
  Keep an encryption key in memory for repeated use during a session.

- 🗂️ **Namespaced secrets**  
  Organize secrets with paths like `db/prod/my-db`.

- 🧭 **Interactive workflows**  
  Secure prompts, interactive lists, clipboard integration.

- 💻 **Cross-platform**  
  Works on Linux, macOS, and Windows.

---

## Installation

```bash
pip install rune
```

---

## Getting Started

### Login / Logout

Before managing secrets, you must select an active user.

At this stage, **login does not authenticate or unlock anything** — it simply sets the root namespace for secrets.

```bash
# Log in as a user
rune login <username>

# Log out
rune logout
```

> The active user determines which secrets are visible and writable.

---

## Adding Secrets

```bash
rune add db/prod/my-db -f host=localhost,port,user,password -k super-secret-key
```

**Options:**
- Secret names support namespaces using `/`
- `--fields / -f`
  - Comma-separated list of fields
  - Fields without values are prompted securely
  - If omitted entirely, Rune stores a single-field secret
- `--key / -k`
  - Encryption key (securely prompted if omitted)

---

## Retrieving Secrets

```bash
rune get db/prod/my-db
```

Example output:

```text
[1] host
[2] port
[3] user
[4] password
Choose a field to copy (q to cancel):
```

- Selected values are copied to the clipboard by default
- Use `--show` to display values in the terminal
- Use `--interactive` to pick a secret from a list (`rune ls -i` shortcut)

---

## Listing Secrets

```bash
rune ls
```

- Secrets are displayed as a namespace tree
- Supports filtering by namespace
- Interactive mode allows direct retrieval

---

## Updating Secrets

```bash
rune update db/prod/my-db -f user=new-user,password,new_field=new
```

- Updates existing fields
- Adds new fields
- Missing values are prompted securely

---

## Moving Secrets

```bash
rune move db/prod/my-db db/prod/cassandra
```

- Renames or relocates a secret within the namespace tree

---

## Deleting Secrets

```bash
rune delete db/prod/cassandra
```

- By default, secrets are **soft-deleted** (hidden)
- Use `--hard` to permanently delete
- Hard deletes require the encryption key

### Deleting Individual Fields

```bash
rune delete db/prod/cassandra -f password
```

---

## Restoring Secrets

```bash
rune restore db/prod/cassandra
```

- Restores a soft-deleted secret
- All soft-deleted fields are restored

---

## Sessions (Default Encryption Key)

Sessions allow you to keep an encryption key in memory so you don’t have to re-enter it for every operation.

- The key lives **only in memory**
- Stored in a local background daemon
- Never written to disk
- Communicated via a local TCP socket

Sessions are **not accounts or master passwords**.  
They are simply a convenience mechanism for repeated encryption operations.

---

### Starting a Session

```bash
rune session start --session-key <key>
```

- If the key is omitted, you’ll be prompted securely
- A session TTL can be configured (or disabled)

---

### Ending a Session

```bash
rune session end
```

- Clears the session and removes the key from memory

---

### Session Status

```bash
rune session status
```

Displays:
- Whether a session is active
- Associated user
- Remaining TTL (if any)

---

## Other commands
### Show Current Configuration

```bash
rune config show
```

### Locate Important Files

```bash
rune config where
```

Shows where Rune stores:
- Settings
- Profiles
- Secrets (local storage)

---

### Profiles

Profiles allow you to save and switch between different configurations.

```bash
rune config profile save <name>
rune config profile load <name>
rune config profile list
```

---

## Storage & Encryption

- Secrets are stored locally (JSON filesystem by default)
- Encryption is always client-side (decrypted secrets and encryption keys **NEVER** leave memory)
- Encryption mode is configurable (currently `aesgcm`)

---

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for planned features and upcoming milestones.

---

## License

Apache License 2.0

