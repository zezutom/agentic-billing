"""Public Commercial-Consistency Auditor for SaaS companies.

The pipeline is deliberately split so that each stage does what it is good at:

    harvest   deterministic crawl of the public pages that make commercial
              promises, rendered into a readable dossier
    analyse   an LLM reads the dossier and reports where the company's own
              pages disagree about what customers receive
    verify    every quote the model produced is checked, character by
              character, against the harvested page it claims to come from
    render    the surviving findings become a report a founder can read

The model is the analyst. The verifier is what makes trusting it reasonable:
a finding whose evidence cannot be located in the source page is dropped
before anyone sees it.
"""

__version__ = "0.2.0"
