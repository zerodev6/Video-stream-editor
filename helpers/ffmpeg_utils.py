import asyncio
import json
import os

async def get_streams(file_path):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", file_path]
    process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, _ = await process.communicate()
    return json.loads(stdout).get("streams", [])

async def extract_thumbnail(video_path, output_path, timestamp="00:00:05"):
    cmd = ["ffmpeg", "-ss", timestamp, "-i", video_path, "-vframes", "1", "-q:v", "2", output_path, "-y"]
    process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await process.wait()
    return output_path if os.path.exists(output_path) else None

async def map_streams(input_path, output_path, maps):
    # maps is a list of indices e.g., ["0", "1", "3"]
    cmd = ["ffmpeg", "-i", input_path]
    for m in maps:
        cmd.extend(["-map", f"0:{m}"])
    cmd.extend(["-c", "copy", output_path, "-y"])
    
    process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await process.wait()
    return output_path
