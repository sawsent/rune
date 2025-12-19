# rune

rune is a secure, local-first secrets management tool designed for developers.
It allows you to store, retrieve, and manage secrets easily while keeping them encrypted client-side.

---

## Features

- zero-trust. Decrypted secrets never leave memory
- Per-secret encryption keys
- Namespaced secrets (`db/prod/my-db`) for easy access
- Interactive secret entry and retrieval
- Cross-platform (Linux, macOS, Windows)

---

## Installation

```bash
pip install rune
```

---

## Getting Started

### Login / Logout

Before performing any secret operations, you must be logged in. At this stage, login simply sets the active username:

```bash
# Log in as a user
rune login <username>

# Log out
rune logout
```

> Note: Currently login only selects the active username which determines access to secret namespaces.

---

### Adding Secrets

```bash
rune add db/prod/my-db -f host=localhost,port,user,password -k super-secret-key
```

- Name of the secret. Supports namespaces using `/`.
- `-f / --fields`
    - Comma-separated list of fields. Fields without a value will be prompted securely.
    - If ommitted, store a single-field secret.
- `-k / --key` → Optional encryption key (prompted secretly if not specified)

---

### Retrieving Secrets

```bash
rune get db/prod/my-db

# result
[1] localhost
[2] port
[3] user
[4] password
Choose a field to copy (q to cancel):
```

- Copies a chosen field to the clipboard by default.
- Use `--show` to display secret values in the terminal.
- `--interactive` triggers an interactive list selection (shortcut for `rune ls -i`).

---

### Listing Secrets

```bash
rune ls
```

- Lists all secrets, organized by namespace.
- Single-child namespaces are collapsed for cleaner display.
- Use `<namespace>` argument to filter results.
- Use `--interactive` to fetch a secret directly from the list.
- Use `--show` to reveal values when in interactive mode.

---

### Updating Secrets

```bash
rune update db/prod/my-db -f user=new-user,password
```

- Updates existing fields or adds new ones.
- Fields without a value will be prompted securely.

---

### Moving Secrets

```bash
rune move db/prod/my-db db/prod/cassandra
```

- Moves a secret from one name to another.

---

### Deleting Secrets

```bash
rune delete db/prod/cassandra
```

- Removes a secret from the vault.
- Use `--hard` to remove the secret from persistence.
- When hard deleting secrets, encryption key is required.

---

### Restoring Secrets

```bash
rune restore db/prod/cassandra
```

- Restores a soft-deleted secret to the vault.

---


### Configuration

Rune CLI supports configuring storage and encryption options:

```bash
rune config show          # Display current config
rune config storage       # Set storage options (local file path)
rune config encryption    # Set encryption mode (currently `aesgcm`)
```

It also allows you to save and load profiles:

```bash
rune config profile save <profile-name>  # Save current settings to profile 
rune config profile load <profile-name>  # Load a saved profile
rune config profile list                 # Show saved profiles
```


---

## Storage & Encryption

- Secrets are stored locally in JSON format (default).
- Fully client-side encrypted. (Decrypted text never leaves memory)
- Per-secret encryption keys are supported.

---

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for the full development roadmap.

---

## License

Apache 2.0

