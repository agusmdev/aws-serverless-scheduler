from datetime import datetime, timezone, timedelta


class DateTime:
    @property
    def now(self):
        return datetime.now(tz=timezone.utc)

    def get_segment(self, date, extra_minutes):
        return int(
            (date + timedelta(minutes=extra_minutes))
            .replace(second=0, microsecond=0)
            .timestamp()
        )

    def get_current_segment(self, extra_minutes):
        return self.get_segment(self.now, extra_minutes)

    def seconds_until_date(self, date):
        return int((date - self.now).total_seconds())

    def from_isoformat(self, date):
        return datetime.fromisoformat(date)

    def to_isoformat(self, date):
        return date.isoformat()


date_handler = DateTime()