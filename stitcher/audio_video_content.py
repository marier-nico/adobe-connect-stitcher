from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from content_type import ContentType


@dataclass
class AudioVideoContent:
    path: Path
    content_type: ContentType
    start_date: datetime
    duration: timedelta
    offset_from_start: Optional[timedelta] = None

    @property
    def path_str(self):
        return str(self.path.absolute())
