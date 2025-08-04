#similar to get kegg but this also groups genes based order in which the appear however the groups have to be renamed manually 


import requests
import xml.etree.ElementTree as ET
import pandas as pd
import re
import math

def cluster_by_order(pathway_id, n_groups=5):
    url = f"http://rest.kegg.jp/get/{pathway_id}/kgml"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch KGML for {pathway_id}")

    root = ET.fromstring(response.content)

    # Collect all genes with their y-coordinates
    gene_data = []
    for entry in root.findall("entry"):
        if entry.attrib.get("type") == "gene":
            name = entry.attrib.get("name", "")
            graphics = entry.find("graphics")
            if graphics is None:
                continue
            gene_symbol = graphics.attrib.get("name", "")
            x = int(graphics.attrib.get("x", 0))
            y = int(graphics.attrib.get("y", 0))
            ids = re.findall(r"hsa:(\d+)", name)
            for gene_id in ids:
                gene_data.append([gene_id, gene_symbol, x, y])

    df = pd.DataFrame(gene_data, columns=["Gene ID", "Gene Symbol", "x", "y"])

    # Sort by y (top to bottom appearance)
    df = df.sort_values(by="y").reset_index(drop=True)

    # Divide into n_groups
    group_size = math.ceil(len(df) / n_groups)
    df["Function"] = df.index // group_size + 1
    df["Function"] = df["Function"].apply(lambda x: f"Group_{x}")

    final_df = df[["Function", "Gene ID", "Gene Symbol"]]
    return final_df

# Example usage:
df = cluster_by_order("hsa03430", n_groups=5)
df.to_excel("hsa03430_ordered_groups.xlsx", index=False)
