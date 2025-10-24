from PyQt5.QtCore import QThread, pyqtSignal
from fastmcp import Client
import asyncio
from whimbox.config.config import global_config
from whimbox.common.logger import logger


class TaskCallWorker(QThread):
    """异步任务调用Worker"""
    finished = pyqtSignal(bool, object)  # 成功/失败, 结果/错误信息
    progress = pyqtSignal(str)  # 进度消息
    
    def __init__(self, tool_name: str, params: dict):
        super().__init__()
        self.tool_name = tool_name
        self.params = params
        mcp_port = global_config.get_int("General", "mcp_port")
        self.mcp_url = f"http://127.0.0.1:{mcp_port}/mcp"
    
    def run(self):
        """在后台线程中执行异步调用"""
        try:
            logger.info(f"Starting task: {self.tool_name} with params: {self.params}")
            # self.progress.emit(f"正在启动任务: {self.tool_name}...")
            
            # 创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # 执行异步调用
                result = loop.run_until_complete(self._call_tool())
                logger.info(f"Task completed successfully: {result.data}")
                self.finished.emit(True, result.data)
            finally:
                loop.close()
                
        except Exception as e:
            logger.error(f"Task failed: {e}", exc_info=True)
            self.finished.emit(False, str(e))
    
    async def _call_tool(self):
        """异步调用工具"""
        async with Client(self.mcp_url) as client:
            result = await client.call_tool(self.tool_name, self.params)
            return result