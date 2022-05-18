import logging
from pathlib import Path

from pyroll import solve
from pyroll.ui.reporter import Reporter

THIS_DIR = Path(__file__).parent


def test_solve(tmp_path: Path, caplog):
    import pyroll.ui.cli.res.input_trio as input_py

    caplog.set_level(logging.DEBUG, logger="sims_power_and_labour")

    sequence = input_py.sequence

    solve(sequence, input_py.in_profile)

    report = Reporter()

    rendered = report.render(sequence)
    print()

    report_file = tmp_path / "report.html"
    report_file.write_text(rendered)
    print(report_file)

    print("\nLog:")
    print(caplog.text)
