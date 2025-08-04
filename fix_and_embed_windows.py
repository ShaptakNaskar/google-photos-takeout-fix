import os
import subprocess
import magic  # uses python-magic-bin on Windows

# Mapping MIME types to correct extensions
MIME_EXTENSION_MAP = {
    "image/jpeg": ".jpg",
    "image/heic": ".heic",
    "image/png": ".png",
    "video/mp4": ".mp4",
    "video/quicktime": ".mov",
    "image/tiff": ".tif",
    "image/x-canon-cr2": ".cr2",
    "image/x-sony-arw": ".arw",
    "image/x-panasonic-raw": ".rw2",
    "video/x-msvideo": ".avi",
    # Add more if needed
}

def get_mime_type(filepath):
    try:
        mime = magic.from_file(filepath, mime=True)
        return mime
    except Exception as e:
        print(f"Error reading MIME type for {filepath}: {e}")
        return None

def fix_extensions_and_json(root):
    renamed_files = {}
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".supplemental-metadata.json"):
                continue  # skip metadata files for now

            full_path = os.path.join(dirpath, name)
            if not os.path.isfile(full_path):
                continue

            mime_type = get_mime_type(full_path)
            if mime_type in MIME_EXTENSION_MAP:
                correct_ext = MIME_EXTENSION_MAP[mime_type]
                base, current_ext = os.path.splitext(name)
                if current_ext.lower() != correct_ext:
                    new_name = base + correct_ext
                    new_path = os.path.join(dirpath, new_name)
                    if not os.path.exists(new_path):  # avoid overwriting
                        os.rename(full_path, new_path)
                        print(f"🔄 Renamed media: {name} → {new_name}")

                        # Also rename the corresponding JSON if it exists
                        json_old = os.path.join(dirpath, name + ".supplemental-metadata.json")
                        json_new = new_name + ".supplemental-metadata.json"
                        json_new_path = os.path.join(dirpath, json_new)

                        if os.path.exists(json_old):
                            os.rename(json_old, json_new_path)
                            print(f"🔄 Renamed metadata: {os.path.basename(json_old)} → {json_new}")

                        renamed_files[full_path] = new_path
    return renamed_files

def embed_metadata(root):
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".supplemental-metadata.json"):
                json_path = os.path.join(dirpath, name)
                media_path = json_path.replace(".supplemental-metadata.json", "")
                if os.path.exists(media_path):
                    print(f"📎 Embedding metadata into: {media_path}")
                    result = subprocess.run([
                        "exiftool",
                        "-overwrite_original",
                        f"-json={json_path}",
                        media_path
                    ], capture_output=True, text=True)

                    if "Error:" in result.stderr:
                        print(f"❌ ExifTool error: {result.stderr.strip()}")
                else:
                    print(f"⚠️ Media file not found for: {json_path}")

if __name__ == "__main__":
    root_folder = "."  # or change to your target folder
    print("🔍 Fixing misnamed media files and renaming JSONs...")
    fix_extensions_and_json(root_folder)

    print("\n📝 Embedding metadata...")
    embed_metadata(root_folder)

    print("\n✅ All done.")
