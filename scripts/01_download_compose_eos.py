import os
import zipfile
import urllib.request

# ============================================================
# CompOSE EOS Download Script
# APR / SLY4 / DD2
# ============================================================

EOS_URLS = {
    "APR":  "https://compose.obspm.fr/download//1D/NS/Classical/APR/eos.zip",
    "SLY4": "https://compose.obspm.fr/download//1D/NS/Skyrme/SLY4/eos.zip",
    "DD2":  "https://compose.obspm.fr/download//1D/NS/RMF/DD2/eos.zip",
}

BASE_DIR = "data"

os.makedirs(BASE_DIR, exist_ok=True)

for eos_name, url in EOS_URLS.items():

    out_dir = os.path.join(BASE_DIR, eos_name)
    zip_path = os.path.join(BASE_DIR, f"{eos_name}.zip")

    os.makedirs(out_dir, exist_ok=True)

    print("=" * 60)
    print(f"Downloading {eos_name}")
    print(f"Source: {url}")

    urllib.request.urlretrieve(url, zip_path)

    print(f"Saved ZIP: {zip_path}")

    print(f"Extracting {eos_name} EOS files")

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(out_dir)

    extracted_files = sorted(os.listdir(out_dir))

    print(f"{eos_name} extracted files:")
    for f in extracted_files:
        print("  ", f)

print("=" * 60)
print("All EOS datasets downloaded and extracted successfully.")
