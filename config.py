# encoding: utf-8
"""Non-secret configuration for the daily paper workflow.

Credentials are intentionally read from environment variables.  In GitHub
Actions, configure ``OPENAI_API_KEY`` as a repository Actions secret; the
workflow supplies GitHub's short-lived ``GITHUB_TOKEN`` automatically.
"""

import os


# Set new submission url of subject
NEW_SUB_URL = 'https://arxiv.org/list/cs/new'

# Keywords to search
KEYWORD_LIST = [
    # 核心：视觉导航直接相关
    "visual navigation",
    "vision-based navigation",

    # 技术：SLAM与里程计（视觉导航核心底层技术）
    "visual slam",
    "vslam",
    "visual odometry",
    "simultaneous localization and mapping",

    # 前沿与场景：具身智能、机器人与避障
    "embodied ai",
    "robot navigation",
    "autonomous navigation",
    "obstacle avoidance",
    "path planning",
]

# A comma-separated value can be used locally when rotating between keys.
OPENAI_API_KEYS = [
    key.strip()
    for key in os.getenv("OPENAI_API_KEY", "").split(",")
    if key.strip()
]

LANGUAGE = "zh"  # zh | en
