.. _overview-haplotyping:

===============
Lso Haplotyping
===============

This section explains the haplotyping method implemented in the Haplotype-Lso.
It follows the approach described in [DP21]_:

    *DP21: Candidatus Liberibacter solanacearum.*
    International Standards for Phytosanitary Measures 27.
    Annex 21.
    03 Apr 2017.
    [`URL <https://www.ippc.int/en/publications/84157/>`_].

--------------------
Algorithmic Approach
--------------------

Overall, the algorithmic approach for haplotyping of Candidatus *liberibacter solanacearum* (Lso) is as follows.

User Input
==========

Haplotyping is described for multiple user-provided sequences from multiple genomic regions of a single sample.
Following DP21, the sequences would be generated by capillary sequencing of PCR products from predetermined regions.
DP21 suggests three primer pairs targeting the 16S, 16S-23S, and 50S regions.
However, other regions have been suggested, e.g., in [SwGa2019]_.
At the moment, Haplotype-Lso provides support for 16S, 16S-23S, and 50S regions as these are widely available.
However, extensions to further regions are easily possible.

Reference Dataset
=================

For background information, the haplotyping needs a reference data set (cf. :ref:`overview-reference` on how to rebuild it using the command line intreface of Haplotype-Lso).
The reference dataset consists of a reference sequence for each target region ``R``.
Further, for each known Lso haplotype ``H`` where the sequence is known for ``R`` a variant table ``T`` is given.
``T`` provides a list of variants with respect to ``R`` and whether they are present in ``H`` or whether ``H`` shows the reference sequence.

For example, the table for the 16S locus following DP21 looks as follows.
The reference is given by its GenBank ID, the positions are 1-based and reference and alternative bases are given in VCF syntax (c.f. [DAAA2011]_ while the description is given in HGVS notation [DDMH2016]_.
The columns A to E show the allele for each known haplotype.

===========  ======  =====  =====  ====  ===========     =====   ======  ======  ======  =
reference    region  pos    ref    alt   description     A       B       C       D       E
===========  ======  =====  =====  ====  ===========     =====   ======  ======  ======  =
EU812559.1   16S     108    AT     A     n.109delT       AT      AT      AT      AT      A
EU812559.1   16S     115    A      G     n.115A>G        A       A       A       A       G
EU812559.1   16S     116    C      T     n.116C>T        C       C       C       T       C
EU812559.1   16S     151    A      G     n.151A>G        A       A       A       A       G
EU812559.1   16S     212    T      G     n.212T>G        T       G       T       T       T
EU812559.1   16S     581    T      C     n.581T>C        T       C       T       T       T
EU812559.1   16S     959    C      T     n.959C>T        C       C       C       C       T
EU812559.1   16S     1039   A      G     n.1039A>G       A       A       G       G       A
EU812559.1   16S     1040   CC     C     n.1041delC      CC      CC      CC      CC      C
EU812559.1   16S     1073   G      A     n.1073G>A       G       G       G       A       G
===========  ======  =====  =====  ====  ===========     =====   ======  ======  ======  =

Haplotyping Algorithm
=====================

The haplotyping algorithm for one query sequence is as follows:

1. For each user sequence ``S``, a BLAST search is performed in the reference sequences for the regions defined in the input data sets.
2. The best match is taken for ``S``, and variant descriptions are derived (using the normalization approach described in [TAK2015]_.
3. The call set from the user sequence is compared to all calls that overlap with the BLAST match and a score is computed by summation.
   For each haplotype from the table each position is considered.
   If the user input is equal to the haplotype at the position, the score is increased by 1 and it is decreased otherwise.

If the user provides two sequences for a region (e.g., for forward and reverse primer) then only positions are considered where all sequences show the same variant.
Finally, the scores for all regions for a sample are aggregated for each haplotype.
The haplotype(s) with the highest score are yielded as the final haplotype for the given region.

Final Remarks
=============

Obviously, the described approach is limited to identifying known haploytpes.
However, haplotypes A and C only differ in one base on the 16S region and the algorithm is capable of differentiating between them even in the presence of sequencing errors (it is highly unlikely for sequencing errors to show a known variant on the hundreds of reference positions).
Also, it is is easy to validate the haplotyping result by manual inspection of the BLAST matches.

Future extensions are:

- Also consider phylogenetic approaches that would allow the identification of new haplotypes (e.g., if the user sequence is an outlier to all known haplotype sequences).
- Perform BLAST searches in larger databases to identify other outliers.
