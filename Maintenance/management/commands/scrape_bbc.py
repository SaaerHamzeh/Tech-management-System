from django.core.management.base import BaseCommand
from Maintenance.scrape_news import (
    scrape_bbc_arabic,
)  # ← هون بنستورد السكربت يلي كتبناه


class Command(BaseCommand):
    help = "Scrape BBC Arabic headlines"  # شرح للأمر

    def handle(self, *args, **kwargs):
        self.stdout.write("🔍 Scraping started...")
        scrape_bbc_arabic()  # ← هون منشغل السحب
        self.stdout.write("✅ Scraping completed successfully!")
