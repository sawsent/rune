# Rune

Are you tired of storing passwords and API keys in plain text files? **Rune** is a simple, developer-focused terminal vault for securely storing secrets. Each secret is encrypted with a key you provide — nothing is ever stored unencrypted, and no master password is saved.

Rune is built with a workflow developers expect: fast commands, helpful prompts, clipboard integration, and flexible configuration.

---

## Features

- 🔐 Per-secret encryption keys  
- 🏷️ Add, update, delete, and list secrets  
- 📋 Retrieve and auto-copy secrets to your clipboard  
- 🛠️ Configurable encryption mode, storage mode, and file location  
- ❌ Keys are *never stored* — lose the key, lose the secret  
- ✨ Interactive prompts for missing options  

---

## Installation

```bash
pip install rune
```

---

## Usage

All commands prompt for missing values — names, secrets, and keys — making them easy to use interactively.

### Add a Secret

```bash
rune add --name <name> --secret <secret> --key <key>
```

If any option is omitted, Rune will prompt:

- **Name**
- **Secret** (input hidden)
- **Encryption key** (input hidden; must be remembered)

**Example:**

```bash
rune add -n github -s myToken123 -k myKey
```

---

### Retrieve a Secret

```bash
rune get --name <name> --key <key>
```

- Secret is automatically copied to your clipboard.
- Add `--show` to also display it in the terminal.

**Example:**

```bash
rune get -n github -k myKey --show
```

---

### Update a Secret

```bash
rune update --name <name> --secret <new_secret> --key <key>
```

---

### Delete a Secret

```bash
rune delete --name <name>
```

You will be prompted for the name if omitted.

---

### List All Secrets

```bash
rune list
```

Secrets are shown in a numbered list:

```
[1] github
[2] aws
[3] database
```

---

## Configuration

Rune allows you to configure encryption mode, storage mode, and the secrets file location.

```bash
rune config --encryption <mode> --storage-mode <mode> --secrets-file <path>
```

Supported values:

- `--encryption`: `no-encryption`, `aesgcm`
- `--storage-mode`: `local`
- `--secrets-file`: Any file path (e.g., `~/.secrets.json`)

**Example:**

```bash
rune config -e no-encryption -s local -f ~/.rune_secrets.json
```

Run:

```bash
rune config -h
```

for full help.

---

## Security Notes

- Each secret is encrypted with *its own key*.
- Keys are never stored — you must provide the correct key to decrypt or modify a secret.
- Forget the key → the secret is permanently lost.
- Secrets are stored locally in an encrypted file.

---

## Example Workflow

```bash
# Add
rune add -n stripe -s sk_live_abc -k myStrongKey

# Retrieve (copied to clipboard)
rune get -n stripe -k myStrongKey

# Update
rune update -n stripe -s newKey -k myStrongKey

# Delete
rune delete -n stripe

# List
rune list
```

---

## License

Apache 2.0 License

