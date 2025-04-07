# DEBUG Hunter EXIF Tool (English Version)

This tool provides a sleek hacker-style web interface to:
- Upload or fetch images from a URL
- Display EXIF data including camera info, GPS, date, etc.
- Injects a backdoor EXIF tag `vu` for terminal access
- Allows terminal commands (if backdoor detected) using password: kader11000

## Requirements:
- Python 3
- Flask
- Pillow
- requests

## How to Run:
```bash
pip install flask pillow requests
python app.py
```

Access the interface at: http://localhost:5000
