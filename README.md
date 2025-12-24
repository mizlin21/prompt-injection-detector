## Profiles (non-toy feature)
PID supports tunable detection profiles to balance false positives vs security:

- **strict**: lower threshold, higher weights (good for high-risk RAG/tooling)
- **balanced**: default
- **permissive**: higher threshold (good for dev/testing)

### Example
```bash
python -m app.cli data/attacks/injection_01.txt --source retrieved_doc --profile strict

## RAG scanning (retrieved documents)
Scan retrieved documents before adding them to the model context:

```bash
python -m app.cli rag data/rag_bundle.json --profile strict

```md
## Evaluation
PID includes a tiny labeled evaluation corpus and metrics runner:

```bash
python -m app.evaluate