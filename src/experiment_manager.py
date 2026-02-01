from pathlib import Path
from datetime import datetime
import json

from src.registry_manager import update_registry
from src.team_logger import append_team_log


class ExperimentManager:
    def __init__(self, member, mode):
        self.member = member
        self.mode = mode
        self.exp_id = self._generate_experiment_id()
        self.exp_dir = Path("outputs") / self.exp_id
        self.exp_dir.mkdir(parents=True, exist_ok=False)

    def _generate_experiment_id(self):
        ts = datetime.now().strftime("%Y-%m-%d-%H%M")
        return f"EXP-{ts}-{self.member}-{self.mode}"

    def save_model(self, model):
        path = self.exp_dir / "model.keras"
        model.save(path)
        self.model_path = str(path)

    def save_metrics(self, metrics: dict):
        with open(self.exp_dir / "metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)
        self.metrics = metrics

    def save_summary(self):
        summary = f"""# {self.exp_id}

**Member:** {self.member}  
**Mode:** {self.mode}  
**Accuracy:** {self.metrics.get('accuracy')}

## Notes
Auto-generated experiment summary.
"""
        with open(self.exp_dir / "summary.md", "w") as f:
            f.write(summary)

    def finalize(self):
        update_registry(
            exp_id=self.exp_id,
            model_path=self.model_path,
            metrics=self.metrics,
            member=self.member,
            mode=self.mode
        )
        append_team_log(self.exp_id, self.member)
