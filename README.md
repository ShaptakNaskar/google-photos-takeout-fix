
# Google Photos Takeout Fix

This tool helps clean up and restore metadata for media files exported from **Google Photos Takeout**.

✅ Features:
- Fixes incorrect file extensions (e.g., `.ARW` that is actually a `.JPG`)
- Renames corresponding `.supplemental-metadata.json` files to match
- Embeds metadata (timestamp, GPS, etc.) into media files using [ExifTool](https://exiftool.org/)
- Works recursively across all subfolders
- Supports common photo and video formats
- Smart fallback metadata embedding (in standard version)
- Simplified no-fallback version also available
  
---

## 🛠 Requirements

- **Python 3.7+**
- **[ExifTool](https://exiftool.org/)** installed and available in system `PATH`
- Python package:
  ```bash
  pip install python-magic-bin
  
📦 For Windows users:
This script uses `python-magic-bin`, so there's **no need for Unix tools like `file`**.

---

## 🚀 Usage

1. Extract your **Google Photos Takeout** ZIP/TGZ file.
2. Place `fix_and_embed_windows.py` or `lite.fix_and_embed_windows` inside the extracted folder.
3. Open a terminal or PowerShell in that folder.
4. Run the script:

```bash
python fix_and_embed_windows.py
```
or
```bash
python lite.fix_and_embed_windows
```

The script will:

* Correct mislabeled media file extensions based on MIME type
* Rename the corresponding `.supplemental-metadata.json` file
* Use `exiftool` to embed the metadata into the media file

---

## 📁 Supported File Types

| MIME Type           | Extension |
| ------------------- | --------- |
| `image/jpeg`        | `.jpg`    |
| `image/heic`        | `.heic`   |
| `image/png`         | `.png`    |
| `video/mp4`         | `.mp4`    |
| `video/quicktime`   | `.mov`    |
| `image/tiff`        | `.tif`    |
| `image/x-sony-arw`  | `.arw`    |
| `image/x-canon-cr2` | `.cr2`    |
| `video/x-msvideo`   | `.avi`    |

> You can easily extend the script to support more file types by editing `MIME_EXTENSION_MAP`.

---

## 🧠 Variant Comparison

| Feature                                | `fix_and_embed_windows.py` | `fix_and_embed_windows_lite.py` |
| -------------------------------------- | -------------------------- | ------------------------------- |
| Smart fallback metadata embedding      | ✅ Yes (3-step retry)       | ❌ No (fails fast)               |
| Logs failed files                      | ✅ Yes                      | ✅ Yes                           |
| Strict → fuzzy matching for JSON files | ✅ Yes                      | ✅ Yes                           |
| Recursive folder support               | ✅ Yes                      | ✅ Yes                           |
| Thumbnail/preview tag stripping        | ✅ Conditionally applied    | ❌ Never applied                 |

---

## ⚠️ Notes

* Always **back up your files** before running the script.
* The script will **overwrite** original media files when embedding metadata.
* Only files with both media and matching `.supplemental-metadata.json` will be processed.
* Poorly truncated `.json` files from Google Takeout (e.g., `sup.json`, `supple.json`) will be fuzzily matched to the closest media file when strict matching fails.

---

## 🧑‍💻 Contributions

Pull requests are welcome! Ideas for improvement:

* GUI version
* Metadata validation report
* Custom metadata templates
* Timezone corrections

---

## 📄 License

This project is licensed under the **MIT License**.

---

## ⚠️ Disclaimer

This tool is provided **"AS IS"**, **without warranty or guarantee** of any kind — either express or implied.
Use it **at your own risk**. The authors and contributors are **not responsible** for any damage, data loss, or issues that may arise from its use.

You are strongly advised to **make backups** of your original files before running this script.

---
