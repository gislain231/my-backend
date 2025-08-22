from datetime import datetime, timedelta
import pytz

def parse_datetime(datetime_str: str, timezone: str = 'UTC') -> datetime:
    """Parse ISO format datetime string with timezone support"""
    dt = datetime.fromisoformat(datetime_str)
    if dt.tzinfo is None:
        tz = pytz.timezone(timezone)
        return tz.localize(dt)
    return dt

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string"""
    periods = [
        ('year', 60*60*24*365),
        ('month', 60*60*24*30),
        ('day', 60*60*24),
        ('hour', 60*60),
        ('minute', 60),
        ('second', 1)
    ]
    
    parts = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            parts.append(f"{int(period_value)} {period_name}{'s' if period_value != 1 else ''}")
    
    return ', '.join(parts) if parts else '0 seconds'

def get_timezone_offset(timezone: str) -> str:
    """Get UTC offset for a timezone"""
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    return now.strftime('%z')