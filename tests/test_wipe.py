from app.wipe import overwrite_file
import os

def test_overwrite_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("Sensitive Data")
    overwrite_file(str(file))
    assert not file.exists()
