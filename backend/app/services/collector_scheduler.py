from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler

from app.services.collector_service import CollectorService


class CollectorSchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.service = CollectorService()
        self.running = False

    def start(self):
        if self.running:
            return
        self.scheduler.add_job(self.service.run_all, "interval", minutes=10)
        self.scheduler.start()
        self.running = True

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
        self.running = False


scheduler_service = CollectorSchedulerService()
