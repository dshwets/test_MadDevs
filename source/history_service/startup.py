import schedule
import time

from history_service.views import BulkCommitSaver


class StartupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        def job():
            BulkCommitSaver().save_or_create_commits()

        # schedule.every(2).minutes.do(job)  # для тестов
        schedule.every().day.at("10:30").do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)
