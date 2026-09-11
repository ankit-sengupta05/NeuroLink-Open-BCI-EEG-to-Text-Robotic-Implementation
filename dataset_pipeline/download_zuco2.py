import os
import sys

try:
    import requests
    from tqdm import tqdm
except ImportError:
    print("Please install required packages before running:")
    print("pip install requests tqdm")
    sys.exit(1)

# OSF Node ID for ZuCo 2.0
NODE_ID = "2urht"
BASE_URL = f"https://api.osf.io/v2/nodes/{NODE_ID}/files/osfstorage/"

# Resolve dataset directory (../dataset/zuco2)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset", "zuco2")

import time


def get_osf_data(api_url, max_retries=5):
    """Fetch folder metadata from OSF API with retries, handling pagination."""
    all_data = []
    current_url = api_url

    while current_url:
        for attempt in range(max_retries):
            try:
                response = requests.get(current_url, timeout=30)
                response.raise_for_status()
                json_data = response.json()
                all_data.extend(json_data["data"])

                # Check for next page
                links = json_data.get("links", {})
                current_url = links.get("next")
                break  # Break retry loop if successful
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(
                        f"Network error while fetching metadata: {e}. Retrying in 5s... ({attempt + 1}/{max_retries})"
                    )
                    time.sleep(5)
                else:
                    raise
    return all_data


def download_file_resumable(url, destination, max_retries=5):
    """Downloads a file with resume support and retries."""
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    temp_destination = destination + ".tmp"

    for attempt in range(max_retries):
        file_size = 0
        if os.path.exists(destination):
            print(
                f"File {os.path.basename(destination)} already fully downloaded. Skipping."
            )
            return True

        if os.path.exists(temp_destination):
            file_size = os.path.getsize(temp_destination)

        headers = {"Range": f"bytes={file_size}-"} if file_size > 0 else {}

        try:
            response = requests.get(
                url, headers=headers, stream=True, allow_redirects=True, timeout=30
            )

            # 416 Range Not Satisfiable means we requested a range past the end of the file
            if response.status_code == 416:
                os.rename(temp_destination, destination)
                print(f"File {os.path.basename(destination)} already fully downloaded.")
                return True

            if response.status_code not in [200, 206]:
                print(f"Failed to download {url}. Status code: {response.status_code}")
                return False

            if file_size > 0 and response.status_code == 200:
                print("Server doesn't support resume. Restarting download...")
                file_size = 0
                mode = "wb"
            else:
                mode = "ab"

            total_size = int(response.headers.get("content-length", 0)) + file_size

            with (
                open(temp_destination, mode) as f,
                tqdm(
                    desc=os.path.basename(destination),
                    total=total_size,
                    initial=file_size,
                    unit="iB",
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar,
            ):
                for chunk in response.iter_content(chunk_size=8192 * 4):
                    if chunk:
                        size = f.write(chunk)
                        bar.update(size)

            # Verify the file is complete
            if total_size == 0 or os.path.getsize(temp_destination) >= total_size:
                os.rename(temp_destination, destination)
                return True
            else:
                print(f"Download incomplete for {os.path.basename(destination)}")
                # Will retry in the next loop iteration

        except Exception as e:
            if attempt < max_retries - 1:
                print(
                    f"\nError downloading {os.path.basename(destination)}: {e}. Retrying in 5s... ({attempt + 1}/{max_retries})"
                )
                time.sleep(5)
            else:
                print(
                    f"\nFailed to download {os.path.basename(destination)} after {max_retries} attempts: {e}"
                )
                return False


def traverse_and_download(api_url, current_path):
    """Recursively traverses OSF folders and downloads files sequentially."""
    print(f"Fetching listing for {os.path.relpath(current_path, PROJECT_ROOT)} ...")
    items = get_osf_data(api_url)

    for item in items:
        kind = item["attributes"]["kind"]
        name = item["attributes"]["name"]

        if kind == "folder":
            next_url = item["relationships"]["files"]["links"]["related"]["href"]
            next_path = os.path.join(current_path, name)
            success = traverse_and_download(next_url, next_path)
            if not success:
                return False
        elif kind == "file":
            download_url = item["links"]["download"]
            file_path = os.path.join(current_path, name)

            # Download file sequentially, stopping if one fails
            success = download_file_resumable(download_url, file_path)
            if not success:
                print(f"Stopping download process because {name} failed.")
                return False

    return True


if __name__ == "__main__":
    print(f"Starting download of ZuCo 2.0 to: {DATASET_DIR}")
    print("-" * 50)
    os.makedirs(DATASET_DIR, exist_ok=True)

    success = traverse_and_download(BASE_URL, DATASET_DIR)

    if success:
        print("-" * 50)
        print("Dataset download completed successfully!")
    else:
        print("-" * 50)
        print("Dataset download interrupted. Run the script again to resume.")
