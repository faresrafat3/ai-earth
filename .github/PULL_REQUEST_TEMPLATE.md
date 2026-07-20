## Objective
<!-- What are you contributing? Are you adding a new LEGO piece (research paper), fixing the Synapse Kernel, or patching the OmniLog Ledger? -->

## Type of Contribution
- [ ] 🧱 **New LEGO Piece:** Adding logic from a new research paper.
- [ ] 🧠 **Synapse Kernel Update:** Modifying how agents talk via the Intelligence Bus.
- [ ] 💾 **Ledger / Storage:** Changes to the OmniLog tracking schemas.
- [ ] 🐛 **Bug Fix:** API cooldowns, fallback logic, or syntax errors.

## New Research Checklist (If adding a LEGO Piece)
- [ ] Link to the original paper included.
- [ ] The logic was implemented verbatim from the paper's methodology.
- [ ] The piece successfully communicates with the `Intelligence Bus`.
- [ ] The new agent operates without breaking the `Resilient Mesh` fallback.

## Testing & Tracing
- [ ] Have you verified that your agent's thoughts are correctly logging to the `OmniLog Ledger`?
- [ ] Did you test API failure states to ensure the fallback mode activates?
