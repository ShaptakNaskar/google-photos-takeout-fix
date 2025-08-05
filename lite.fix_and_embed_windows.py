import os
import subprocess
import magic  # Requires python-magic-bin on Windows
import difflib

# MIME type to correct extension map
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
}

def get_mime_type(filepath):
    try:
        return magic.from_file(filepath, mime=True)
    except Exception as e:
        print(f"❌ Error reading MIME type for {filepath}: {e}")
        return None

def find_best_json_match(media_file, all_jsons):
    media_name = os.path.basename(media_file)
    media_stem, _ = os.path.splitext(media_name)

    # Strict match
    for json_path in all_jsons:
        json_base = os.path.basename(json_path)
        if json_base == media_name + ".supplemental-metadata.json":
            return json_path
        if json_base.startswith(media_name) or json_base.startswith(media_stem):
            return json_path

    # Fallback (fuzzy)
    candidates = [j for j in all_jsons if j.lower().endswith(".json")]
    if not candidates:
        return None

    matches = difflib.get_close_matches(media_name, [os.path.basename(j) for j in candidates], n=1, cutoff=0.6)
    if matches:
        for json_path in candidates:
            if os.path.basename(json_path) == matches[0]:
                print(f"🧠 Fallback matched '{media_name}' to '{matches[0]}'")
                return json_path

    return None

def fix_extensions_and_json(root):
    renamed_files = {}
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".supplemental-metadata.json"):
                continue

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
                    if not os.path.exists(new_path):
                        os.rename(full_path, new_path)
                        print(f"🔄 Renamed media: {name} → {new_name}")

                        # Rename matching JSON
                        json_old = os.path.join(dirpath, name + ".supplemental-metadata.json")
                        json_new = new_name + ".supplemental-metadata.json"
                        json_new_path = os.path.join(dirpath, json_new)

                        if os.path.exists(json_old):
                            os.rename(json_old, json_new_path)
                            print(f"🔄 Renamed metadata: {os.path.basename(json_old)} → {json_new}")

                        renamed_files[full_path] = new_path
    return renamed_files

def embed_metadata_simple(json_path, media_path):
    print(f"\n📎 Embedding metadata into: {media_path}")
    result = subprocess.run([
        "exiftool", "-m", "-overwrite_original",
        f"-json={json_path}", media_path
    ], capture_output=True, text=True)

    if "files weren't updated" not in result.stdout and "Error:" not in result.stderr:
        print("✅ Metadata embedded successfully")
        return True
    else:
        print("❌ Embedding failed")
        print(result.stderr.strip())
        with open("failed_metadata_log.txt", "a", encoding="utf-8") as log:
            log.write(f"{media_path}\n")
        return False

def embed_metadata(root):
    for dirpath, _, filenames in os.walk(root):
        jsons = [os.path.join(dirpath, f) for f in filenames if f.lower().endswith(".json")]
        medias = [os.path.join(dirpath, f) for f in filenames if not f.lower().endswith(".json")]

        for media_path in medias:
            json_path = find_best_json_match(media_path, jsons)
            if json_path and os.path.exists(json_path):
                embed_metadata_simple(json_path, media_path)
            else:
                print(f"⚠️ No metadata found for: {media_path}")

if __name__ == "__main__":
    root_folder = "."  # Replace with your folder path if needed
    print("🔍 Fixing misnamed media files and renaming JSONs...")
    fix_extensions_and_json(root_folder)

    print("\n📝 Embedding metadata...")
    embed_metadata(root_folder)

    print("\n✅ All done.")
