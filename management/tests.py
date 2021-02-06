from django.test import TestCase
from util.tests import TestSetup

# Create your tests here.
from .models import ClaimedJob


class ClaimedJobTest(TestCase):
    def setUp(self):
        # ! setup might be called before each test, would use TestCase.setUpTestData()
        # https://docs.djangoproject.com/en/3.1/topics/testing/tools/#django.test.TestCase.setUpTestData
        self.setup = TestSetup()
        self.created_job = ClaimedJob.create(
            user=self.setup.worker.user,
            job_id=self.setup.job.id)

    def test_can_create_job(self):
        self.assertEqual(self.created_job.status, ClaimedJob.IN_PROGRESS)

    def test_can_quit_job(self):
        self.created_job.quit_job()
        self.assertEqual(self.created_job.status, ClaimedJob.QUIT)
        # self.assertEqual(self.worker)

    def test_can_approve_job(self):
        self.created_job.approve()
        self.assertEqual(self.created_job.comment, ClaimedJob.APPROVED)
        self.assertEqual(self.created_job.status, ClaimedJob.COMPLETED)
