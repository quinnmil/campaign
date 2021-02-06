from django.utils import timezone
from gigs.models import Job, Campaign
from accounts.models import User, Worker


class TestSetup:
    """Class used to generate placeholder test data"""

    def __init__(self):
        self.job = self.create_job()
        self.worker = self.create_worker()

    def create_job(self):
        """create generic job for use in tests"""
        campaign = Campaign.objects.create(name='testCampaign', candidate='candidate',
                                           description='description', email='email@domain.com')
        return Job.objects.create(description="description", headline="testJob",
                                  instructions="instructions", initial_count=5,
                                  starts_on='2020-09-15 05:27:28+00:00',
                                  ends_on=timezone.now() + timezone.timedelta(days=1),
                                  zipcode='00001', pay='10', campaign=campaign)

    def create_worker(self):
        """create worker to use in tests"""
        user = User.objects.create(
            is_worker=True, username='testUser')
        user.set_password('secret')
        user.save()
        return Worker.objects.create(user=user)
