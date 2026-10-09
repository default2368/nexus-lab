# Command Ledger — repeatability test 24
Input: /home/user/nexus-lab/NEXUS-LAB/24-SCANSIONE-PER-CAPACITA.md
SHA: 582d4373807d5ac2485559c5ed79fe3e90046ea2b5bf08728522b612db59aee7
Generated: 2026-10-09T19:08:11.495344+00:00

## Steps
1. sha256sum NEXUS-LAB/24-SCANSIONE-PER-CAPACITA.md → ORIGINAL-SHA.txt
2. parse headings (regex ^#{1,4}) → PARSED-HEADINGS.jsonl
3. parse tables (```text + |...|) → PARSED-TABLES.jsonl
4. extract claims (regex per banda, premio, governance) → CANDIDATE-CLAIMS.jsonl (6 campi minimi)
5. human review → HUMAN-REVIEW.json (CANDIDATE, requires approval)
6. regenerate matrix from claims → REGENERATED-MATRIX.md
7. compare original vs regenerated → COMPARISON-REPORT.md
8. generate PageData → PAGEDATA.json

Headings: 37, Tables: 13, Claims: 12, Repeatable: True