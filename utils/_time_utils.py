#utils/_time_utils.py

from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def convert_relative_time_to_absolute(time_str):
    now = datetime.now()
    try:
        if "hour" in time_str:
            hours = int(time_str.split()[0])
            return now - timedelta(hours=hours)
        elif "minute" in time_str:
            minutes = int(time_str.split()[0])
            return now - timedelta(minutes=minutes)
        elif "day" in time_str:
            days = int(time_str.split()[0])
            return now - timedelta(days=days)
    except Exception as e:
        logger.error(f"Error converting relative time to absolute: {e}")
    return now


