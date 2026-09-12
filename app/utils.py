from fastapi import HTTPException


def parse_month(month: str) -> tuple[int, int]:
    """Turns 'YYYY-MM' into (year, month) ints.
    Raises HTTPException(400) if the format is wrong or the month is out of range."""
    try:
        year_str, month_str = month.split("-")
        year, mon = int(year_str), int(month_str)
    except (ValueError, AttributeError):
        raise HTTPException(status_code=400, detail="month must be in YYYY-MM format")

    if not (1 <= mon <= 12):
        raise HTTPException(status_code=400, detail="month must be between 01 and 12")

    return year, mon