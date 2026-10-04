import random
from django.core.management.base import BaseCommand
from faker import Faker
from tasks.models import Category, Priority, Task, Note, SubTask

class Command(BaseCommand):
    help = "Populate database with sample fake data for Hangarin"

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write("Clearing old data...")
        SubTask.objects.all().delete()
        Note.objects.all().delete()
        Task.objects.all().delete()
        Category.objects.all().delete()
        Priority.objects.all().delete()

        self.stdout.write("Creating Categories...")
        category_names = ['Work', 'School', 'Personal', 'Finance', 'Projects']
        categories = [Category.objects.create(name=cat) for cat in category_names]

        self.stdout.write("Creating Priorities...")
        priority_names = ['High', 'Medium', 'Low', 'Critical', 'Optional']
        priorities = [Priority.objects.create(name=p) for p in priority_names]

        statuses = ['Pending', 'In Progress', 'Completed']

        self.stdout.write("Creating Tasks, Notes, and Subtasks...")
        for _ in range(15):
            task = Task.objects.create(
                title=fake.sentence(nb_words=4).rstrip('.'),
                description=fake.paragraph(nb_sentences=2),
                deadline=fake.future_datetime(),
                status=random.choice(statuses),
                category=random.choice(categories),
                priority=random.choice(priorities)
            )

            for _ in range(random.randint(1, 2)):
                Note.objects.create(
                    task=task,
                    content=fake.sentence(nb_words=8)
                )

            for _ in range(random.randint(1, 3)):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=3).rstrip('.'),
                    status=random.choice(statuses)
                )

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))