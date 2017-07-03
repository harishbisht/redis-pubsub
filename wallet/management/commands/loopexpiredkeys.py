from django.core.management import BaseCommand
from redishelp.config import expiredkeysloop

class Command(BaseCommand):
    # Show this when the user types help
    help = "Run the redis expired key notification"

    # A command must define handle()
    def handle(self, *args, **options):
        self.stdout.write("Waiting for the expired keys")
        expiredkeysloop()
        self.stdout.write("Exiting")
