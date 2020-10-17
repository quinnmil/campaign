from django.test import TestCase, Client
from django.urls import reverse
# Create your tests here.
from .models import Job, Campaign
from management.models import ClaimedJob
from accounts.models import User, Worker, Manager
from .views import ValidationError
from django.utils import timezone


def create_job():
    """create generic job for use in tests"""
    campaign = Campaign.objects.create(name='testCampaign', candidate='candidate',
                                       description='description', email='email@domain.com')
    return Job.objects.create(description="description", headline="testJob",
                              instructions="instructions", initial_count=5,
                              starts_on='2020-09-15 05:27:28+00:00',
                              ends_on=timezone.now() + timezone.timedelta(days=1),
                              zipcode='00001', pay='10', campaign=campaign)


def create_worker():
    """create worker to use in tests"""
    user = User.objects.create(
        is_worker=True, username='testUser')
    user.set_password('secret')
    user.save()
    return Worker.objects.create(user=user)


class QuitJobTest(TestCase):
    """tests related to quitting job"""

    def setUp(self):
        self.client = Client()
        self.base_job = create_job()
        self.worker = create_worker()

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
        self.base_job = create_job()
        self.worker = create_worker()

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
