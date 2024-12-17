"""
This scripts downloads DBLP pages for each professor
"""

import argparse
import json
import requests
from pathlib import Path
from tqdm import tqdm


def download_dblp_xml(pid, output_dir="output/pids"):
    path = Path(output_dir) / (pid + ".xml")
    url = f"https://dblp.org/pid/{pid}.xml"
    path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return path

def main():
    parser = argparse.ArgumentParser(
        prog='download_professor_pids',
        description='Download professors pages from DBLP')
    parser.add_argument(
        '-i', '--input', default="output/professor_map.json",
        help="Professor DBLP map. Generated by 2.filter_current_professors")
    parser.add_argument(
        '-o', '--output-dir', default="output/pids",
        help="Output directory for downloads")

    args = parser.parse_args()

    with open(args.input, "r") as f:
        professor_map = json.load(f)

    pbar = tqdm(professor_map.items())
    for name, authors in pbar:
        pbar.set_description(name)
        for author in authors:
            download_dblp_xml(author['pid'], output_dir=args.output_dir)

if __name__ == "__main__":
    main()
    