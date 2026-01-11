
@dataclass
class Filter(Enum):
    """Filter criteria for finding specific time periods."""
    NUMBER_OF_ACTIVE_LPS = auto()  # Time with most active liquidity providers
    MAX_LIQUIDITY_USD = auto()     # Time with highest USD liquidity
    MAX_VOLUME_USD = auto()        # Time with highest USD volume
    MAX_TRANSACTIONS = auto()      # Time with most transactions

@dataclass
class Frequency(Enum):
    """Time grouping frequency for data aggregation."""
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

@dataclass
class TimeData:

@dataclass
class Query:
    query = {"query": str},
    variables: Optional[Dict[str, Any]] = None
