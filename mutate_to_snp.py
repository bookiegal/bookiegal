def apply_snps_to_protein(sequence, snps):
    """
    Applies SNP-based amino acid substitutions to a canonical protein sequence.

    Parameters:
    sequence (str): Canonical protein sequence
    snps (list of tuples): [(position, ref_aa, alt_aa), ...]

    Returns:
    str: Mutated protein sequence
    """

    seq_list = list(sequence)

    for pos, ref, alt in snps:
        index = pos - 1  # Convert to 0-based indexing

        if index < 0 or index >= len(seq_list):
            raise ValueError(f"Position {pos} out of range.")

        if seq_list[index] != ref:
            raise ValueError(
                f"Reference mismatch at position {pos}: "
                f"expected {ref}, found {seq_list[index]}"
            )

        seq_list[index] = alt

    return "".join(seq_list)


def get_user_input():
    """
    Collects protein sequence and SNP information from the user.
    """

    sequence = input("Enter canonical protein sequence:\n").strip().upper()

    n = int(input("Enter number of SNPs: "))

    snps = []
    print("\nEnter SNPs in the format: Position Reference_AA Alternate_AA")
    print("Example: 50 A T\n")

    for i in range(n):
        entry = input(f"SNP {i+1}: ").split()

        if len(entry) != 3:
            raise ValueError("Each SNP must have 3 values: position ref alt")

        pos = int(entry[0])
        ref = entry[1].upper()
        alt = entry[2].upper()

        snps.append((pos, ref, alt))

    return sequence, snps


def main():
    print("=== Protein SNP Substitution Tool ===\n")

    try:
        sequence, snps = get_user_input()
        mutant_sequence = apply_snps_to_protein(sequence, snps)

        print("\nCanonical Sequence:")
        print(sequence)

        print("\nMutant Sequence:")
        print(mutant_sequence)

    except Exception as e:
        print("\nError:", e)


if __name__ == "__main__":
    main()
