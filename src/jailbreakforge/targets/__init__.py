"""Target connector abstraction layer."""

from jailbreakforge.targets.base import TargetConnector
from jailbreakforge.targets.openai import OpenAITarget
from jailbreakforge.targets.anthropic import AnthropicTarget
from jailbreakforge.targets.generic import GenericTarget
from jailbreakforge.targets.factory import create_target

__all__ = [
    "TargetConnector",
    "OpenAITarget",
    "AnthropicTarget",
    "GenericTarget",
    "create_target",
]
