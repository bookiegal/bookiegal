#script to extract all genes involved in a pathway from kegg. 
#works best on relatively short pathways 
#ive used dna mismatch repair as an example here
#adapted from prof saravanan p's dataframes assignment 

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_kegg_genes_from_html(pathway_id):
    url = f"https://www.kegg.jp/entry/{pathway_id}"
    print(f"Fetching: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch KEGG page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the 'Genes' section
    pre_tags = soup.find_all("pre")
    gene_lines = []
    for tag in pre_tags:
        if "Genes" in tag.text:
            gene_lines = tag.text.strip().splitlines()
            break

    gene_data = []

    for line in gene_lines:
        if line.startswith("HSA:"):
            # Multiple genes per line sometimes
            matches = re.findall(r"HSA:(\d+)\(([^)]+)\)", line)
            for gid, symbol in matches:
                gene_data.append(["", gid, symbol])

    df = pd.DataFrame(gene_data, columns=["Function", "Gene ID", "Gene Symbol"])
    return df

# Example usage
if __name__ == "__main__":
    pathway_id = "hsa03430"
    df = get_kegg_genes_from_html(pathway_id)
    df.to_excel(f"{pathway_id}_scraped.xlsx", index=False)
    print(f"Saved {pathway_id}_scraped.xlsx with {len(df)} genes.")
