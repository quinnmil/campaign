from django.test import TestCase, Client
from django.urls import reverse
# Create your tests here.
from util.tests import TestSetup
from .models import Job, Campaign
from management.models import ClaimedJob
from accounts.models import User, Worker, Manager
from django.core.exceptions import ValidationError
from django.utils import timezone


# These Views-based tests are deprecated and replaced by tests in ../management/tests
class QuitJobTest(TestCase):
    """tests related to quitting job"""

    def setUp(self):
        self.client = Client()
        setup = TestSetup()
        self.base_job = setup.job
        self.worker = setup.worker

    def test_can_quit_job(self):
        """workers can quit jobs"""
        # Give user Job
        ClaimedJob.objects.create(job=self.base_job, worker=self.worker)
        self.client.login(username='testUser', password='secret')

        response = self.client.post(reverse('gigs:quit'), {
            'job_id': self.base_job.id
        })
        self.assertEqual(response.context['claimedJob'].status, 'Q')
        self.assertQuerysetEqual(
            ClaimedJob.objects.filter(
                job_id=1, worker=response.wsgi_request.user.worker, status='P'), [])
        self.assertQuerysetEqual(ClaimedJob.in_progress_jobs.filter(
            worker=response.wsgi_request.user.worker), [])


class ClaimJobTest(TestCase):
    """tests relating to claiming job"""

    def setUp(self):
        self.client = Client()
        setup = TestSetup()
        self.base_job = setup.job
        self.worker = setup.worker

    def test_can_claim_job(self):
        """workers can claim jobs"""
        self.client.login(username='testUser', password='secret')

        response = self.client.post(reverse('gigs:claim'), {
            'job_id': self.base_job.id})
        self.assertEqual(response.context['claimedJob'].status, 'P')
        self.assertTrue(ClaimedJob.in_progress_jobs.filter(
            worker=response.wsgi_request.user.worker).exists())

    def test_fails_when_job_already_claimed(self):
        """worker can't claim a job they're already working on"""
        self.client.login(username='testUser', password='secret')
        ClaimedJob.objects.create(job=self.base_job, worker=self.worker)

        response = self.client.post(reverse('gigs:claim'), {
            'job_id': self.base_job.id})
        self.assertTrue(response.context['error'])
