class Error(Exception):
    """Generic error, taken from practices detailed
    https://hakibenita.com/bullet-proofing-django-models"""


class UserRollError(Error):
    """Thrown when user has the incorrect role for the requested action"""

    def __str__(self):
        return 'You must be a worker to claim or quit a job, \
            please use another account or contract support for assistance'


class OverworkedError(Error):
    """Thrown when worker is already working their maximum amount of simultaneous jobs."""

    def __str__(self):
        return 'You have claimed too many concurrent gigs, \
            please complete a current gig before starting another'


class AlreadyClaimedError(Error):
    """Thrown when user tries to claim job they already have"""

    def __str__(self):
        return 'You have already claimed this job'


class InternalError(Error):
    """Thrown for internal reasons, such an an item not existing in the database"""
