"""Dynamic Prompt Adjustment for Token Optimization"""
from typing import Dict, Any, List


class PromptOptimizer:
    """Dynamically adjust agent prompts based on feedback"""

    def __init__(self):
        self.prompt_variations: Dict[str, List[str]] = {
            "decision-making": [
                "Select the most experienced mentor",
                "Select a mentor from the same department",
                "Select a mentor with good availability",
                "Select a mentor who has mentored before",
            ],
            "action-execution": [
                "Schedule all meetings in morning slots",
                "Schedule meetings considering timezone",
                "Prioritize high-priority meetings first",
                "Space meetings out throughout the week",
            ],
        }

        self.current_prompts: Dict[str, str] = {
            agent: variations[0] for agent, variations in self.prompt_variations.items()
        }

        self.performance_history: Dict[str, List[float]] = {}

    def adjust_prompt(self, agent_id: str, feedback_quality: float) -> str:
        """Adjust prompt based on feedback"""
        if agent_id not in self.prompt_variations:
            return self.current_prompts.get(agent_id, "")

        if agent_id not in self.performance_history:
            self.performance_history[agent_id] = []

        self.performance_history[agent_id].append(feedback_quality)

        # If quality is low, try a different prompt
        if feedback_quality < 0.7:
            current_index = self.prompt_variations[agent_id].index(
                self.current_prompts[agent_id]
            )
            next_index = (current_index + 1) % len(self.prompt_variations[agent_id])
            self.current_prompts[agent_id] = self.prompt_variations[agent_id][next_index]

        return self.current_prompts[agent_id]

    def get_prompt(self, agent_id: str) -> str:
        """Get current prompt for agent"""
        return self.current_prompts.get(agent_id, "")

    def get_performance_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get performance summary for agent"""
        if agent_id not in self.performance_history:
            return {"agent_id": agent_id, "attempts": 0, "average_quality": 0}

        scores = self.performance_history[agent_id]
        return {
            "agent_id": agent_id,
            "attempts": len(scores),
            "average_quality": sum(scores) / len(scores),
            "best_quality": max(scores),
            "current_prompt": self.get_prompt(agent_id),
        }


# Global prompt optimizer instance
prompt_optimizer = PromptOptimizer()
