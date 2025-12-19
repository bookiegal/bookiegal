def apply_snps_to_protein(sequence, snps):
    seq = list(sequence)

    for pos, ref, alt in snps:
        idx = pos - 1

        if idx < 0 or idx >= len(seq):
            raise ValueError(
                f"Position {pos} out of range (sequence length = {len(seq)})"
            )

        if seq[idx] != ref:
            raise ValueError(
                f"Reference mismatch at position {pos}: "
                f"expected {ref}, found {seq[idx]}"
            )

        seq[idx] = alt

    return "".join(seq)


print("=== Protein SNP Substitution Tool ===\n")

# 🔹 Read MULTI-LINE protein sequence
print("Enter canonical protein sequence (paste sequence; press ENTER on empty line to finish):")

sequence_lines = []
while True:
    line = input().strip()
    if line == "":
        break
    sequence_lines.append(line)

protein_seq = "".join(sequence_lines).upper()

print(f"\nSequence length detected: {len(protein_seq)} amino acids")

# 🔹 Read number of SNPs
while True:
    n = input("Enter number of SNPs: ")
    if n.isdigit():
        n = int(n)
        break
    print("❌ Please enter a number.")

# 🔹 Read SNPs
snps = []
print("\nEnter SNPs in format: position reference_AA alternate_AA")
print("Example: 499 N S\n")

for i in range(n):
    while True:
        entry = input(f"SNP {i+1}: ").split()
        if len(entry) == 3 and entry[0].isdigit():
            snps.append((int(entry[0]), entry[1].upper(), entry[2].upper()))
            break
        print("❌ Invalid format. Try again.")

# 🔹 Apply mutations
mutant_seq = apply_snps_to_protein(protein_seq, snps)

print("\nCanonical sequence:")
print(protein_seq)

print("\nMutant sequence:")
print(mutant_seq)
