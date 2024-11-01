from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from tagger.models import LabeledSentence


class Command(BaseCommand):
    help = 'Generates report of what operators have done'

    def handle(self, *args, **options):
        today = timezone.now().date()
        start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        end_of_day = timezone.make_aware(datetime.combine(today, datetime.max.time()))
        daily_activity = LabeledSentence.objects.filter(created_at__range=(start_of_day, end_of_day))

        # Generate a report based on operator activity
        report = {}
        for entry in daily_activity:
            operator_id = entry.operator.id
            if operator_id not in report:
                report[operator_id] = {'name': entry.operator.user, 'count': 0}
            report[operator_id]['count'] += 1
        report_content = f"Daily Activity Report for {today}\n"
        report_content += "=" * 40 + "\n"
        for operator_id, data in report.items():
            report_content += f"Operator {data['name']} performed {data['count']} actions today.\n"

        # Define the path to save the report
        reports_dir = Path('reports')  # Directory for storing reports
        reports_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
        report_filename = reports_dir / f"daily_activity_report_{today}.txt"

        # Write the report to a file
        with report_filename.open('w') as report_file:
            report_file.write(report_content)

        self.stdout.write(self.style.SUCCESS(f'Report saved as {report_filename}'))


