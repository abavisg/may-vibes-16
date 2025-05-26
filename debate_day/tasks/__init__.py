"""
Tasks package for the debate system.

This package contains task definitions for CrewAI agents.
"""

from .pro_task import pro_debate_task, pro_rebuttal_task, pro_task
from .con_task import con_debate_task, con_rebuttal_task, con_task
from .mod_task import mod_task

__all__ = [
    "pro_debate_task",
    "pro_rebuttal_task",
    "pro_task",
    "con_debate_task",
    "con_rebuttal_task",
    "con_task",
    "mod_task"
] 