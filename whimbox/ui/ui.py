from whimbox.common.cvars import *
from whimbox.interaction.interaction_core import itt
from whimbox.ui.page_assets import *
from whimbox.ui.template.button_manager import Button
from whimbox.common.timer_module import AdvanceTimer
from whimbox.common.logger import logger

from threading import Lock
import time

class UI():

    def __init__(self) -> None:
        self.switch_ui_lock = Lock()

    def ui_additional(self):
        """
        Handle all annoying popups during UI switching.
        """
        while page_loading.is_current_page(itt):
            itt.delay(1, comment='game is loading...')

    def is_valid_page(self):
        for i in ui_pages:
            if i.is_current_page(itt):
                return True
        return False

    def get_page(self, retry_times=0, raise_exception=True, max_retry=5):
        ret_page = None

        # when ui_addition is complete, enable it
        if raise_exception and retry_times >= max_retry:
            logger.info(f"Unknown page, try pressing esc")
            itt.key_press('esc')

        for page in ui_pages:
            if page.is_current_page(itt):
                if ret_page is None:
                    ret_page = page
                else:
                    logger.warning(f"检测到多个Page")
        if ret_page is None:
            logger.warning("未知Page, 重新检测")
            self.ui_additional()
            time.sleep(5)
            ret_page = self.get_page(retry_times=retry_times + 1)
        return ret_page

    def verify_page(self, page: UIPage) -> bool:
        return page.is_current_page(itt)

    def ui_goto(self, destination: UIPage, confirm_wait=0.5):
        """
        Args:
            destination (Page):
            confirm_wait:
        """
        try:
            retry_timer = AdvanceTimer(1)
            self.switch_ui_lock.acquire()
            # Reset connection
            for page in ui_pages:
                page.parent = None

            # Create connection
            visited = [destination]
            visited = set(visited)
            while 1:
                new = visited.copy()
                for page in visited:
                    for link in ui_pages:
                        if link in visited:
                            continue
                        if page in link.links:
                            link.parent = page
                            new.add(link)
                if len(new) == len(visited):
                    break
                visited = new

            logger.info(f"UI goto {destination}")
            while 1:
                # Destination page
                if destination.is_current_page(itt):
                    logger.debug(f'Page arrive: {destination}')
                    break

                # Other pages
                clicked = False
                for page in visited:
                    if page.parent is None or len(page.check_icon_list) == 0:
                        continue
                    if page.is_current_page(itt):
                        logger.debug(f'Page switch: {page} -> {page.parent}')
                        button = page.links[page.parent]
                        if isinstance(button, str):
                            if retry_timer.reached():
                                itt.key_press(button)
                                retry_timer.reset()
                        elif isinstance(button, Button):
                            itt.appear_then_click(button)
                        elif isinstance(button, Text):
                            itt.appear_then_click(button)
                        clicked = True
                        itt.delay(0.5, comment="ui goto is waiting game animation")
                        break
                if clicked:
                    continue

                # Additional
                if self.ui_additional():
                    continue

            # Reset connection
            for page in ui_pages:
                page.parent = None
            self.switch_ui_lock.release()
            itt.delay(0.5, comment="ui goto is waiting game animation")
            # itt.wait_until_stable()
        except Exception as e:
            logger.error(f"UI goto failed: {e}")
            self.switch_ui_lock.release()
            raise e

    def ensure_page(self, page: UIPage):
        if not self.verify_page(page):
            self.ui_goto(page)

    def wait_until_stable(self, threshold=0.9995, timeout=10):
        while 1:
            itt.wait_until_stable(threshold=threshold, timeout=timeout, additional_break_func=self.is_valid_page)
            if not page_loading.is_current_page(itt):
                break


ui_control = UI()

if __name__ == '__main__':
    # ui_control.ui_goto(page_esc)
    ui_control.ui_goto(page_huanjing_jihua)
