from app.verifier import generate_certificate
import os

def test_generate_certificate(tmp_path):
    paths = [str(tmp_path / "dummy.txt")]
    (tmp_path / "dummy.txt").write_text("data")
    cert = generate_certificate(paths)
    assert os.path.exists(cert)
