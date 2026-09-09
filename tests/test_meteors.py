import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.generators import generate_meteor_showers, load_meteor_showers


def test_meteor_calendar_has_valid_dates_and_fallback(tmp_path):
    generated = generate_meteor_showers(year=2026)

    assert len(generated) >= 8
    assert generated["peak_date"].dt.year.eq(2026).all()
    assert (generated["start_date"] <= generated["peak_date"]).all()
    assert (generated["peak_date"] <= generated["end_date"]).all()
    assert load_meteor_showers(data_dir=tmp_path) is None