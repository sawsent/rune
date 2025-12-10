# Rune — Encrypted Local Secret Vault (CLI)

Rune is a tiny, dependency-light CLI tool for storing secrets locally on your machine.
Secrets are organized by name and optional namespaces, and can be copied to clipboard securely without printing them to the terminal.

---

## **Features**
- Store secrets with any number of fields (`host`, `user`, `password`, etc.)
- Organize secrets in namespaces (`db/prod/mydb`)
- AES-GCM encryption (or plaintext mode)
- Secure prompts (values are hidden)
- Retrieve secrets interactively
- Copy secrets directly to the clipboard without revealing them
- Minimal configuration
- Simple JSON-based storage

---

## **Installation**

```sh
pip install rune
```

---

## **Basic Usage**

### **Add a secret**
```sh
rune add -n db/prod/mydb -f host,port,user,password
```

You will be prompted *securely* for each field value and for the encryption key (unless provided).

---

## **Names & Namespaces**

You can provide namespaces using slashes:

```
db/prod/mydb
└─ namespace: db/prod
└─ name:      mydb
```

Rune automatically splits these internally.

---

## **Commands**

### `add`
Add a new secret.

```sh
rune add -f field1,field2,... [-n name] [-k key]
```

Example:

```sh
rune add -f username,password -n github/personal
```

---

### `get`
Retrieve a secret (copies to clipboard).

```sh
rune get -n github/personal
```

This **does NOT print the secret** unless you add:

```sh
--show
```

Example:

```sh
$ rune get -n github/personal
[1] - username
[2] - password
Select field to copy (q to cancel):
```

Pick a number, and that field is copied to the clipboard.

---

### `update`
Modify an existing secret.

```sh
rune update -f user,password -n github/personal
```

Only the specified fields are updated.

---

### `delete`
Delete a secret.

```sh
rune delete -n github/personal
```

---

### `ls`
List all secrets.

```sh
rune ls
```

Example output:

```
[1] db/prod/mydb
[2] github/personal
[3] redis/dev/cache
```

#### **Interactive Mode**

```sh
rune ls -i
```

Lets you select an entry and directly open it via `get`.

---

### `config`
Configure Rune’s behavior.

```sh
rune config [--encryption aesgcm|no-encryption] [--storage-mode local] [--secrets-file path]
```

Examples:

Set encryption mode:

```sh
rune config -e aesgcm
```

Change secrets location:

```sh
rune config -f ~/.mysecrets.json
```

---

### `whereis`
Display paths to the settings file and secrets file:

```sh
rune whereis
```

Example output:

```
settings: /home/user/.config/rune/settings.json
secrets:  /home/user/.local/share/rune/secrets.json
```

---

## **Clipboard Behavior**
Rune uses `pyperclip` to copy retrieved secrets directly to your clipboard.

- Nothing is displayed unless `--show` is used.
- You must select the field to copy.
- Copying is interactive to avoid accidental exposure.

---

## **Storage**
Rune stores:

- encrypted (or plaintext) secrets  
- user configuration (settings)

in JSON files in your user directory.  
Use `rune whereis` to locate them.

---

## **License**
Apache 2.0.  
See `LICENSE` file.

