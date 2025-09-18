# Secure Wipe Tool

A cross-platform secure data wiping tool with a simple GUI.
It securely overwrites files/folders and generates a signed wipe certificate.

## Features
- One-click file/folder wiping
- Multi-pass overwrite (NIST SP 800-88 style)
- Tamper-proof PDF + JSON wipe certificate
- Safe checks to avoid wiping system files
- User-friendly UI
- Build to `.exe` with PyInstaller

## Installation
```bash
pip install -r requirements.txt
