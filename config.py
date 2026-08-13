# encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# Authentication for user filing issue (must have read/write access to repository to add issue to)
USERNAME = 'Ailing-cao'
TOKEN = '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'

# The repository to add this issue to
REPO_OWNER = 'Ailing-cao'
REPO_NAME = 'ChatDailyPapers'

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
    "path planning"
]


OPENAI_API_KEYS = ['sk-9503aa1443efde055b3d7eefa23e5c63a6026d0be537d055069048cf3dc3000b', ]
LANGUAGE = "zh"  # zh | en
