from lambda_src.sentry_driver import normalize_error_for_fingerprint, sentry_fingerprint


def test_normalize_error_groups_qrr_executor_ids():
    first_error = (
        "Error in task 395030: Uncaught exception of type 'STATEMENT_ERROR' "
        "on line 2 at position 0 : Job QRR_EXECUTOR_5853B8D4CC044C8E8DD15AF612E49FE9 "
        "failed to complete. Exited with status: FAILED."
    )
    second_error = (
        "Error in task 395030: Uncaught exception of type 'STATEMENT_ERROR' "
        "on line 2 at position 0 : Job QRR_EXECUTOR_5988207CF0EF470199E38645870B10D0 "
        "failed to complete. Exited with status: FAILED."
    )

    assert normalize_error_for_fingerprint(first_error) == normalize_error_for_fingerprint(second_error)


def test_normalize_error_uses_statement_error_shape():
    error = (
        "Error in task 123456: Uncaught exception of type 'STATEMENT_ERROR' "
        "on line 2 at position 0 : Job QRR_EXECUTOR_5853B8D4CC044C8E8DD15AF612E49FE9 "
        "failed to complete. Exited with status: FAILED."
    )

    assert normalize_error_for_fingerprint(error) == (
        "STATEMENT_ERROR|line:2|position:0|"
        "job <qrr-executor-id> failed to complete. Exited with status: FAILED."
    )


def test_normalize_error_preserves_unmatched_ids():
    error = "Failed to process payload 0123456789abcdef0123456789abcdef."

    assert normalize_error_for_fingerprint(error) == error


def test_fingerprint_keeps_task_name_and_history_type():
    error = (
        "Error in task 395030: Uncaught exception of type 'STATEMENT_ERROR' "
        "on line 2 at position 0 : Job QRR_EXECUTOR_5853B8D4CC044C8E8DD15AF612E49FE9 "
        "failed to complete. Exited with status: FAILED."
    )

    assert sentry_fingerprint('TASK_A', 'TASK', error) == [
        'snowflake-error',
        'task',
        'TASK_A',
        'STATEMENT_ERROR|line:2|position:0|job <qrr-executor-id> failed to complete. Exited with status: FAILED.',
    ]
    assert sentry_fingerprint('TASK_B', 'TASK', error) != sentry_fingerprint('TASK_A', 'TASK', error)
