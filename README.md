# rune

rune is a secure, local-first secrets management tool designed for developers.
It allows you to store, retrieve, and manage secrets easily while keeping them encrypted client-side.

---

## Features

- Fully local-first, zero-trust CLI
- Per-secret encryption keys
- Namespaced secrets (`db/prod/my-db`)
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
rune add -f host=localhost,port,user,password -n db/prod/my-db
```

- `-f / --fields` → Comma-separated list of fields. Fields without a value will be prompted securely.
- `-n / --name` → Name of the secret. Supports namespaces using `/`.
- `-k / --key` → Optional encryption key.

---

### Retrieving Secrets

```bash
rune get -n db/prod/my-db
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
- Use `--namespace <name>` to filter results.
- Use `--interactive` to fetch a secret directly from the list.
- Use `--show` to reveal values when in interactive mode.

---

### Updating Secrets

```bash
rune update -f password,newpass -n db/prod/my-db
```

- Updates existing fields or adds new ones.
- Fields without a value will be prompted securely.

---

### Deleting Secrets

```bash
rune delete -n db/prod/my-db
```

- Removes a secret from the vault.
- Will prompt for secret name if omitted.

---

### Configuration

Rune CLI supports configuring storage and encryption options:

```bash
rune config show          # Display current config
rune config storage       # Set storage options (local file path)
rune config encryption    # Set encryption mode (currently `aesgcm`)
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

