# Reflection

## Which finding deserved attention first?

Bandit rated the shell call High. Cleanup only needs filename matching and deletion. Using filesystem operations directly removes the need to interpret a command.

## What did the tools miss?

All three tools missed the overbooking boundary. Running the starter showed four Yoga members for three seats. Checking the fourth booking and the exported roster verified the correction.

## How did the tools complement each other?

Pylint identified a shared default list and an unmanaged file. Flake8 located spacing violations. Both flagged the bare exception, so one change cleared findings in two reports.

## How were the fixes checked?

All three tools ran again on the final file. Runtime checks covered cancellation, literal-prefix cleanup, JSON export and walk-in inputs including blank, zero, negative, nonnumeric and over-capacity requests.
