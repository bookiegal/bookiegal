#script to extract all genes involved in a pathway from kegg. 
#works best on relatively short pathways 
#ive used dna mismatch repair as an example here
#adapted from prof saravanan p's dataframes assignment 


import requests
import xml.etree.ElementTree as ET
import pandas as pd
import re

def get_genes_from_kegg_kgml(pathway_id):
    url = f"http://rest.kegg.jp/get/{pathway_id}/kgml"
    print(f"Fetching: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch KGML")

    root = ET.fromstring(response.content)

    gene_data = []
    for entry in root.findall("entry"):
        if entry.attrib.get("type") == "gene":
            name = entry.attrib.get("name", "")
            # usually in form hsa:4292 hsa:27030
            graphics = entry.find("graphics")
            gene_symbol = graphics.attrib.get("name", "") if graphics is not None else ""
            ids = re.findall(r"hsa:(\d+)", name)
            for gene_id in ids:
                gene_data.append(["", gene_id, gene_symbol])

    df = pd.DataFrame(gene_data, columns=["Function", "Gene ID", "Gene Symbol"])
    return df

if __name__ == "__main__":
    pathway_id = "hsa03430"
    df = get_genes_from_kegg_kgml(pathway_id)
    df.to_excel(f"{pathway_id}_kgml.xlsx", index=False)
    print(f"Saved {pathway_id}_kgml.xlsx with {len(df)} genes.")
