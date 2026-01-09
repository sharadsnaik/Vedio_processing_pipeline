import requests

def downlaod_vedio(url: str, out_path:str):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(out_path, 'wb') as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    return out_path