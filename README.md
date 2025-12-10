# rune

Are you tired of storing passwords and API keys in plain text files? **rune** is a terminal-based password manager for developers that lets you securely store, retrieve, update, and manage secrets—all encrypted with a key you provide. Each secret can have its own key, and nothing is ever stored on disk except the encrypted data.

---

## Features

- Securely store passwords and API keys with per-secret keys.
- Retrieve secrets by providing the key used for encryption.
- Update or delete stored secrets.
- List all stored entries.
- All data is stored locally in an encrypted file — no master password is ever saved.

---

## Installation

Install Rune via pip:

```bash
pip install rune
```

---

## Usage

### Create a new secret

```bash
rune create -n <name> -p <password> -k <key>
```

- `-n` : Name of the secret (e.g., `github`, `aws`).
- `-p` : Password or API key.
- `-k` : Key used to encrypt this secret. You must provide this key to decrypt later.

---

### Retrieve a secret

```bash
rune get -n <name> -k <key>
```

- Returns the decrypted password associated with `<name>`.
- You must provide the same key that was used to encrypt the secret.

---

### Update a secret

```bash
rune update -n <name> -p <new_password> -k <key>
```

- Update a stored secret. The same key must be provided to authorize the update.

---

### Delete a secret

```bash
rune delete -n <name> -k <key>
```

- Delete a stored secret. The key must match the one used for encryption.

---

### List all secrets

```bash
rune list
```

- Lists all stored secret names. Keys are not required for listing, but are required for retrieving the actual secret.

---

## Security

- Secrets are encrypted on disk with the key you provide.
- Keys are never stored — you must type the key every time you create, retrieve, update, or delete a secret.
- Different secrets can use different keys for added flexibility and security.

---

## Example

```bash
# Store a new secret
rune create -n github -p myGitHubToken123 -k mySecretKey

# Retrieve it later
rune get -n github -k mySecretKey
```

---

## License

Apache 2.0 License

