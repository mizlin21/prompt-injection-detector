## Profiles (non-toy feature)
PID supports tunable detection profiles to balance false positives vs security:

- **strict**: lower threshold, higher weights (good for high-risk RAG/tooling)
- **balanced**: default
- **permissive**: higher threshold (good for dev/testing)

### Example
```bash
python -m app.cli data/attacks/injection_01.txt --source retrieved_doc --profile strict
