from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .middleware import Limiter
from .decorators import limit, exempt, shared_limit
from .errors import RateLimitExceeded

