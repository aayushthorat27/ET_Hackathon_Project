"""Feedback Loop for Token Optimization"""
from typing import Dict, Any, List
from app.workflows.state import WorkflowState


class FeedbackLoop:
    """Per-step verification and feedback for quality control and token saving"""

    def __init__(self):
        self.feedback_history: Dict[int, List[Dict[str, Any]]] = {}

    def verify_step_result(self, step_id: int, result: Dict[str, Any], step_name: str) -> Dict[str, Any]:
        """Verify a step result and generate feedback"""
        quality_score = self._calculate_quality_score(result, step_name)

        feedback = {
            "step_id": step_id,
            "quality_score": quality_score,
            "passed": quality_score >= 0.8,
            "issues": self._identify_issues(result, step_name),
            "recommendations": self._generate_recommendations(step_id, quality_score),
        }

        if step_id not in self.feedback_history:
            self.feedback_history[step_id] = []
        self.feedback_history[step_id].append(feedback)

        return feedback

    def _calculate_quality_score(self, result: Dict[str, Any], step_name: str) -> float:
        """Calculate quality score (0-1) for a result"""
        if result.get("status") == "error":
            return 0.0

        score = 0.8  # Base score
        if "reasoning" in result:
            score += 0.1
        if result.get("verified"):
            score += 0.1

        return min(score, 1.0)  # Cap at 1.0

    def _identify_issues(self, result: Dict[str, Any], step_name: str) -> List[str]:
        """Identify issues in result"""
        issues = []
        if result.get("status") == "error":
            issues.append(f"Error: {result.get('error', 'Unknown')}")
        if "data" not in result and result.get("status") != "error":
            issues.append("Missing data in result")
        return issues

    def _generate_recommendations(self, step_id: int, quality_score: float) -> List[str]:
        """Generate recommendations for next execution"""
        recommendations = []

        if quality_score < 0.6:
            recommendations.append("Trigger retry with adjusted parameters")
        if quality_score < 0.8:
            recommendations.append("Review and refine agent prompt")

        if step_id in self.feedback_history and len(self.feedback_history[step_id]) > 1:
            prev_score = self.feedback_history[step_id][-2]["quality_score"]
            if quality_score > prev_score:
                recommendations.append("Recent improvements detected")

        return recommendations

    def should_retry(self, step_id: int) -> bool:
        """Determine if step should be retried"""
        if step_id not in self.feedback_history:
            return False
        last_feedback = self.feedback_history[step_id][-1]
        return not last_feedback["passed"]

    def get_feedback_for_step(self, step_id: int) -> Dict[str, Any] | None:
        """Get latest feedback for a step"""
        if step_id not in self.feedback_history:
            return None
        return self.feedback_history[step_id][-1]


# Global feedback loop instance
feedback_loop = FeedbackLoop()
