from unittest.mock import MagicMock, patch

from src.pdf_compressor import WorkerThread


@patch('src.pdf_compressor.subprocess.run')
@patch('src.pdf_compressor.time.time', side_effect=[100.0, 102.5])
def test_worker_thread_success(mock_time, mock_run):
    """Tests successful command execution and checks the elapsed time signal."""

    command = ["echo", "test_command_output"]
    worker = WorkerThread(command)

    with patch.object(WorkerThread, 'finished', new=MagicMock()) as mock_finished_signal:

        # 1. Execute the run logic
        worker.run()

        # 2. Assertions
        mock_run.assert_called_once_with(command, check=True)

        # Check if the 'finished' signal (now the mock) was emitted
        # Elapsed time = 102.5 - 100.0 = 2.5 seconds
        mock_finished_signal.emit.assert_called_once_with(2.5)