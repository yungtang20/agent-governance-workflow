# Security Policy

## Public-content boundary

Never commit credentials, cookies, private keys, connection strings, personal paths, production data, internal project identifiers, or real audit ledgers.

Before publishing:

1. Run `python scripts/validate.py`.
2. Run `python -m unittest discover -s tests -v`.
3. Review every staged file.
4. Scan both the working tree and Git history for secrets.
5. Test from a fresh clone.

Report suspected exposure privately to the repository owner. Rotate exposed credentials immediately; deleting the latest file does not remove a secret from Git history.
