# Validation

Source SHA-256: `43465a06f2ccf7c8b5bd2892bc7defb52f97487934fe93b16ae4c3936424676d`

- Raw rows: 541,909
- Exact duplicates removed before text normalisation: 5,268
- Nonzero-quantity, positive-price and required-field filter exclusions: 2,512
- Ledger rows: 534,129
- Independent SQLite row, sales, credit, net and order checks: passed (money tolerance £0.01).
- Monthly, country and product reconciliation: passed.
- Customer segment count and unique LineID checks: passed.
- MySQL scripts, Power Query and DAX require execution in their target desktop applications; their runtime execution is not claimed here.

Duplicate removal is an explicit analytical assumption: identical lines could be legitimate repeated entries. No claim of audited accounts is made.
