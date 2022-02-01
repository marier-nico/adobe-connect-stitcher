import subprocess
from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from stitcher.audio_video_content import AudioVideoContent
from stitcher.content_type import ContentType


def find_start_of_all_content(content: List[AudioVideoContent]) -> datetime:
    return min(content, key=lambda e: e.start_date).start_date


def set_offsets_from_start(all_content: List[AudioVideoContent], global_start: datetime):
    for content in all_content:
        content.offset_from_start = content.start_date - global_start


def generate_empty_video(duration: timedelta, connect_dir: Path):
    file_name = Path(str((connect_dir / f"empty_{duration}.mkv").absolute()))
    if not file_name.exists():
        subprocess.run(
            [
                "ffmpeg",
                "-t",
                str(duration.total_seconds()),
                "-s",
                "1920x1080",
                "-f",
                "rawvideo",
                "-r",
                "1",
                "-i",
                "/dev/zero",
                str(file_name.absolute()),
            ],
        )
    return file_name


def convert_to_mkv(flv_video: AudioVideoContent) -> AudioVideoContent:
    out_file = Path(f"{flv_video.path_str}.mkv")
    if not out_file.exists():
        subprocess.run(["ffmpeg", "-y", "-i", flv_video.path_str, "-s", "1920x1080", out_file])
    flv_video.path = out_file
    return flv_video


def concat_videos(videos: List[Path], connect_dir: Path) -> Path:
    temp = NamedTemporaryFile("w")
    temp.writelines([f"file '{str(p)}'\n" for p in videos])
    temp.flush()

    concat_output = connect_dir / "all_videos.mkv"
    if not concat_output.exists():
        subprocess.run(
            ["ffmpeg", "-f", "concat", "-safe", "0", "-i", temp.name, "-c", "copy", str(concat_output.absolute())]
        )

    return concat_output


def stitch(content: List[AudioVideoContent], connect_dir: Path) -> Path:
    global_start = find_start_of_all_content(content)
    set_offsets_from_start(content, global_start)

    audio_content = sorted(
        [elm for elm in content if elm.content_type is ContentType.AUDIO], key=lambda e: e.start_date
    )
    video_content = sorted(
        [convert_to_mkv(elm) for elm in content if elm.content_type is ContentType.VIDEO], key=lambda e: e.start_date
    )

    audio_filter_parts = []
    audio_output_streams = []
    for i, content_elm in enumerate(audio_content):
        delay = round(content_elm.offset_from_start.total_seconds())
        audio_filter_parts.append(f"[{i}]adelay={delay}s|{delay}s[s{i}];")
        audio_output_streams.append(f"[s{i}]")
    audio_filter_parts.append(f"{''.join(audio_output_streams)}amix=inputs={len(audio_filter_parts)}[mixout]")

    videos_paths_with_blanks = []
    if video_content[0].start_date != global_start:
        videos_paths_with_blanks.append(
            str(generate_empty_video(video_content[0].offset_from_start, connect_dir).absolute())
        )
        videos_paths_with_blanks.append(video_content[0].path_str)
    else:
        videos_paths_with_blanks.append(video_content[0].path_str)

    if len(video_content) >= 2:
        for i in range(1, len(video_content)):
            previous_video = video_content[i - 1]
            video_delta = video_content[i].start_date - (previous_video.start_date + previous_video.duration)
            videos_paths_with_blanks.append(str(generate_empty_video(video_delta, connect_dir).absolute()))
            videos_paths_with_blanks.append(video_content[i].path_str)

    all_videos = concat_videos(videos_paths_with_blanks, connect_dir)

    input_command = []
    for elm in audio_content:
        input_command.append("-i")
        input_command.append(elm.path_str)
    input_command.extend(["-i", str(all_videos.absolute())])

    final_output = connect_dir / "final_output.mkv"
    final_command = (
        ["ffmpeg"]
        + input_command
        + ["-filter_complex", "".join(audio_filter_parts)]
        + [
            "-map",
            "[mixout]:a",
            "-map",
            f"{len(audio_output_streams)}:v",
            "-c:v",
            "copy",
            str(final_output.absolute()),
        ]
    )

    subprocess.run(final_command)

    return final_output
