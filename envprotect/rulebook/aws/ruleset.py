"""Define AWS RuleSet registry.

This ruleset covers AWS dependencies and common community-driven SDKs.
"""
from typing import Dict, Any, Union
from envprotect.constants import RuleSets
from ...core import Detection, DetectionResult
from .. import RuleFactory, RuleSet


@RuleFactory.register(ruleset_name=RuleSets.AWS_RULESET,
                      deps_list=[
                        "aws-sdk",
                        "aws-s3"
                      ])
class AWSRuleSet(RuleSet):
    """AWS Rule Set.

    Describe ruleset with rules for extracting AWS related strings.
    """

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize AWSRuleSet instance."""
        super().__init__()

    # TODO: Update this generic method interface
    def detect_secrets(self,
                       target: Union[str, bytes],
                       apply: bool = False) -> DetectionResult:
        """Detect secrets in the given file.

        Takes target data and detects possible AWS dependency-related secrets.

        Args:
            target: Data string to be used for detection.
            apply: Flag to allow raising detection to apply.

        Returns:
            DetectionResult instance with detections listed.
        """
        # return count(
        #     filter(
        #         detection: detection,
        #         [detector.score_detection(repo) for detector in detectors]
        #     )
        # ) >= (len(detectors) // 2)
        return DetectionResult(ok=[Detection(result="Default result")], exception=None)
