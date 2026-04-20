import time
import math

async def progress_bar(current, total, status, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000

        progress = "[{0}{1}] {2}%".format(
            ''.join(["█" for i in range(math.floor(percentage / 10))]),
            ''.join(["░" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2)
        )

        tmp = f"**{status}**\n{progress}\n\n" \
              f"🚀 **Speed:** {humanbytes(speed)}/s\n" \
              f"⏱️ **ETA:** {time_formatting(time_to_completion)}"

        try:
            await message.edit(text=tmp)
        except:
            pass

def humanbytes(size):
    if not size: return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024: return f"{size:.2f} {unit}"
        size /= 1024

def time_formatting(milliseconds):
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s"
  
