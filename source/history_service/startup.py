import schedule
import time
import threading
from history_service.views import BulkCommitSaver


class StartupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        def starter():
            def run_timer():
                def job():
                    BulkCommitSaver().save_or_create_commits()

                # schedule.every(30).seconds.do(job)  # для тестов
                schedule.every().day.at("10:30").do(job)

                while True:
                    schedule.run_pending()
                    # print('111111')
                    time.sleep(1)

            x = threading.Thread(target=run_timer, daemon=True)
            x.start()
        starter()

