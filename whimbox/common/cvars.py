"""Constants."""

import threading
from whimbox.common.path_lib import IS_DEV_MODE
from whimbox.config.config import global_config

DEBUG_MODE = global_config.get_bool('General', 'debug') and IS_DEV_MODE
CV_DEBUG_MODE = global_config.get_bool('General', 'cv_debug') and IS_DEV_MODE

# 全局的任务停止信号
# 所有和自动化相关的耗时循环都应该检查这个信号
# 比如页面切换、地图移动等等，（task相关已经在TaskTemplate中统一检查）
global_stop_flag = threading.Event()

MCP_TOOL_TIMEOUT = 24*60*60  # mcp工具调用超时时间设为24小时

# Angle modes
ANGLE_NORMAL = 0
ANGLE_NEGATIVE_Y = 1
ANGLE_NEGATIVE_X = 2
ANGLE_NEGATIVE_XY = 3

# Process name
PROCESS_NAME = 'X6Game-Win64-Shipping.exe'

# log
LOG_NONE = 0
LOG_WHEN_TRUE = 1
LOG_WHEN_FALSE = 2
LOG_ALL = 3

IMG_RATE = 0
IMG_POSI = 1
IMG_POINT = 2
IMG_RECT = 3
IMG_BOOL = 4
IMG_BOOLRATE = 5

NORMAL_CHANNELS = 0
FOUR_CHANNELS = 40000

THREAD_PAUSE_SET_FLAG_ONLY = 0
THREAD_PAUSE_FORCE_TERMINATE = 1

# 字符串匹配模式
CONTAIN_MATCHING = 0
ACCURATE_MATCHING = 1