
# dit-relation-circuits
 
**Circuit Mechanisms for Spatial Relation Generation in Diffusion Transformers**  

Binxu Wang*, Jingxuan Fan*, Xu Pan* · CVPR 2026
 
<!-- [\[Paper\]](#) · [\[Project Page\]](#) · [\[BibTeX\]](#citation) -->
 
---
 
## Overview
 
Why do text-to-image models struggle to place objects in the right spatial relation?
This repo contains the code for our mechanistic interpretability study of how Diffusion Transformers (DiTs) implement spatial relation generation — and under what conditions they fail.
 
We train PixArt-style DiTs from scratch on a controlled two-object relational dataset and dissect the internal circuits responsible for correct spatial composition, comparing models with **random token embeddings (RTE)** vs. a **pretrained T5** text encoder.
 
**Key findings:**
- Both T5-DiT and RTE-DiT achieve high relational accuracy, but via fundamentally different circuits.
- RTE-DiT uses a clean two-stage circuit: a *spatial relation head* tags image positions using QK interactions with positional embeddings; an *object generation head* then reads those tags to render the correct object.
- T5-DiT bypasses explicit relation tokens entirely, decoding spatial layout from contextual embeddings fused into object tokens (especially `shape2`).
- This difference explains why T5-DiT collapses under small prompt perturbations (e.g., inserting "the") while RTE-DiT remains robust.
 
---


## Citation
 
```bibtex
@inproceedings{wang2026circuit,
  title     = {Circuit Mechanisms for Spatial Relation Generation in Diffusion Transformers},
  author    = {Wang, Binxu and Fan, Jingxuan and Pan, Xu},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2026}
}
```

---
 
## Acknowledgements
 
We thank Martin Wattenberg, Yonatan Belinkov, and Thomas Fel for feedback, and participants of the NEMI Workshop and the Mechanistic Interpretability Workshop at NeurIPS 2025 for helpful discussion.
This work was supported by the Kempner Research Fellowship and the Schwartz Fellowship, with compute from the Kempner Institute cluster.