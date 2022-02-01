from datetime import datetime, timedelta
from pathlib import Path
from typing import List
from xml.etree import ElementTree as ET

try:
    import dateparser
    _has_dateparser = True
except ImportError:
    dateparser = None
    _has_dateparser = False

import ffmpeg

from stitcher.audio_video_content import AudioVideoContent
from stitcher.content_type import ContentType


def get_content_with_xml_info(content_path: Path, content_type: ContentType) -> AudioVideoContent:
    filename = content_path.stem
    xml_info_file = content_path.parent / f"{filename}.xml"
    start_date = get_content_start_date_from_xml(xml_info_file)
    duration = timedelta(seconds=float(ffmpeg.probe(content_path)["format"]["duration"]))

    return AudioVideoContent(path=content_path, content_type=content_type, start_date=start_date, duration=duration)


def get_content_start_date_from_xml(xml_path: Path) -> datetime:
    xml_info = ET.parse(xml_path)
    time_info_array = [e for e in xml_info.getroot().findall("Message") if e.find("Array")][0].find("Array")

    for elm in time_info_array:
        try:
            return parse_date(elm.text)
        except ValueError:
            pass
    raise Exception(f"Could not determine content start for file '{xml_path}'")


def parse_date(date: str) -> datetime:
    if ":" in date and len(date) >= 5:
        if _has_dateparser:
            parsed = dateparser.parse(date)
            if parsed:
                return parsed
        else:
            return datetime.strptime(date, "%a %b %d %H:%M:%S %Y")

    raise ValueError("The provided string does not look like a date")


def get_all_content(connect_dir: Path) -> List[AudioVideoContent]:
    all_content = []
    for audio in connect_dir.glob("cameraVoip*.flv"):
        all_content.append(get_content_with_xml_info(audio, ContentType.AUDIO))
    for video in connect_dir.glob("screenshare*.flv"):
        all_content.append(get_content_with_xml_info(video, ContentType.VIDEO))
    return all_content
