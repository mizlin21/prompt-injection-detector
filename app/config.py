from dataclasses import dataclass
from typing import Dict, Literal

ProfileName = Literal["strict", "balanced", "permissive"]

@dataclass(frozen=True)
class Profile:
    name: ProfileName
    threshold: float  # risk >= threshold => is_injection True
    severity_weight: Dict[str, float]
    source_multiplier: Dict[str, float]  # user / retrieved_doc / tool_output


PROFILES: Dict[ProfileName, Profile] = {
    "strict": Profile(
        name="strict",
        threshold=40.0,
        severity_weight={"low": 12, "medium": 30, "high": 55},
        source_multiplier={"user": 1.0, "retrieved_doc": 1.25, "tool_output": 1.25},
    ),
    "balanced": Profile(
        name="balanced",
        threshold=50.0,
        severity_weight={"low": 10, "medium": 25, "high": 45},
        source_multiplier={"user": 1.0, "retrieved_doc": 1.15, "tool_output": 1.20},
    ),
    "permissive": Profile(
        name="permissive",
        threshold=65.0,
        severity_weight={"low": 8, "medium": 20, "high": 40},
        source_multiplier={"user": 1.0, "retrieved_doc": 1.10, "tool_output": 1.10},
    ),
}
