# Run workspaces

`run-project.sh` creates one directory per execution under this path:

```text
workspaces/<run-id>/
└── .nexus-run.json
```

Run directories are ephemeral and ignored by Git. A run may be cleaned only after
its receipt has been finalized in `.nexus/receipts/<run-id>.json`.

Do not remove a run directory manually while it is active. Do not place source,
credentials or permanent evidence here; finalized receipts belong outside the
run directory.
