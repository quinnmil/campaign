from django.test import TestCase, Client
from django.urls import reverse
# Create your tests here.
from .models import Job, Campaign
from management.models import ClaimedJob
from accounts.models import User, Worker, Manager


class QuitJobTest(TestCase):
    def setUp(self):
        self.client = Client()
        campaign = Campaign.objects.create(name='testCampaign', candidate='candidate',
                                           description='description', email='email@domain.com')
        base_job = Job.objects.create(description="description", headline="testJob",
                                      instructions="instructions", initial_count=5,
                                      starts_on='2020-09-15 05:27:28+00:00',
                                      ends_on='2020-09-17 05:27:31+00:00',
                                      zipcode='00001', pay='10', campaign=campaign)
        user = User.objects.create(
            is_worker=True, username='testUser')
        user.set_password('secret')
        user.save()
        worker = Worker.objects.create(user=user)
        ClaimedJob.objects.create(job=base_job, worker=worker)

    def test_quit_job(self):
        c = self.client
        """Users can quit jobs"""
        login = c.login(username='testUser', password='secret')
        response = c.post(reverse('gigs:quit'), {
            'job_id': 1
        })
        self.assertEqual(response.context['claimedJob'].status, 'Q')
        self.assertQuerysetEqual(
            ClaimedJob.objects.filter(job_id=1, worker=response.wsgi_request.user.worker, status='P'), [])
        self.assertQuerysetEqual(ClaimedJob.in_progress_jobs.filter(
            worker=response.wsgi_request.user.worker), [])
