r"""
               _          __                                                                      
  ___   _ __  | | _   _  / _|  __ _  _ __   ___         ___   ___  _ __   __ _  _ __    ___  _ __ 
 / _ \ | '_ \ | || | | || |_  / _` || '_ \ / __| _____ / __| / __|| '__| / _` || '_ \  / _ \| '__|
| (_) || | | || || |_| ||  _|| (_| || | | |\__ \|_____|\__ \| (__ | |   | (_| || |_) ||  __/| |   
 \___/ |_| |_||_| \__, ||_|   \__,_||_| |_||___/       |___/ \___||_|    \__,_|| .__/  \___||_|   
                  |___/                                                        |_|                
"""

import asyncio
import math
import pathlib
import platform
import sys

import httpx
from tqdm.asyncio import tqdm
try:
    from win32_setctime import setctime  # pylint: disable=import-error
except ModuleNotFoundError:
    pass

from .auth import add_cookies
from .config import read_config
from .dates import convert_date_to_timestamp
from .separate import separate_by_id
from ..db import operations
from .paths import set_directory

config = read_config()['config']
root= pathlib.Path((config.get('save_location') or pathlib.Path.cwd()))

async def process_dicts(headers, username, model_id, medialist,forced):
    if medialist:
        operations.create_database(model_id)
        file_size_limit = config.get('file_size_limit')

        # Added pool limit:
        limits = httpx.Limits(max_connections=8, max_keepalive_connections=5)
        async with httpx.AsyncClient(headers=headers, limits=limits, timeout=None) as c:
            add_cookies(c)
            aws=[]
            photo_count = 0
            video_count = 0
            skipped = 0
            total_bytes_downloaded = 0
            data = 0
            desc = 'Progress: ({p_count} photos, {v_count} videos, {skipped} skipped || {data})'    
            with tqdm(desc=desc.format(p_count=photo_count, v_count=video_count, skipped=skipped, data=data), total=len(aws), colour='cyan', leave=True) as main_bar:   
                for ele in medialist:
                    filename=createfilename(ele[0],username,model_id,ele[1],ele[2],ele[3],ele[4],ele[6])
                    with set_directory(str(pathlib.Path(root,username,ele[5].capitalize(),ele[3].capitalize()))):
                        aws.append(asyncio.create_task(download(c,ele[0],filename,pathlib.Path(".").absolute() ,ele[3],model_id, file_size_limit, ele[1],ele[2],forced=False)))
                for coro in asyncio.as_completed(aws):
                        try:
                            media_type, num_bytes_downloaded = await coro
                        except Exception as e:
                            media_type = None
                            num_bytes_downloaded = 0
                            print(e)

                        total_bytes_downloaded += num_bytes_downloaded
                        data = convert_num_bytes(total_bytes_downloaded)

                        if media_type == 'photo' or media_type == "gif":
                            photo_count += 1
                            main_bar.set_description(
                                desc.format(
                                    p_count=photo_count, v_count=video_count, skipped=skipped, data=data), refresh=False)

                        elif media_type == 'video':
                            video_count += 1
                            main_bar.set_description(
                                desc.format(
                                    p_count=photo_count, v_count=video_count, skipped=skipped, data=data), refresh=False)

                        elif media_type == 'skipped':
                            skipped += 1
                            main_bar.set_description(
                                desc.format(
                                    p_count=photo_count, v_count=video_count, skipped=skipped, data=data), refresh=False)

                        main_bar.update()


def convert_num_bytes(num_bytes: int) -> str:
    if num_bytes == 0:
      return '0 B'
    num_digits = int(math.log10(num_bytes)) + 1

    if num_digits >= 10:
        return f'{round(num_bytes / 10**9, 2)} GB'
    return f'{round(num_bytes / 10 ** 6, 2)} MB'


async def download(client,url,filename,path,media_type,model_id,file_size_limit,date=None,id_=None,forced=False):
    path_to_file = pathlib.Path(path,filename)
    async with client.stream('GET', url) as r:
        if not r.is_error:
            rheaders=r.headers
            total = int(rheaders['Content-Length'])
            if file_size_limit and total > int(file_size_limit): 
                    return 'skipped', 1       
            with tqdm(desc=filename, total=total, unit_scale=True, unit_divisor=1024, unit='B', leave=False) as bar:
                num_bytes_downloaded = r.num_bytes_downloaded
                with open(path_to_file, 'wb') as f:
                    async for chunk in r.aiter_bytes(chunk_size=1024):
                        f.write(chunk)
                        bar.update(
                            r.num_bytes_downloaded - num_bytes_downloaded)
                        num_bytes_downloaded = r.num_bytes_downloaded

        else:
            r.raise_for_status()

    if path_to_file.is_file():
        if date:
            set_time(path_to_file, convert_date_to_timestamp(date))

        if id_:
            data = (id_, filename)
            operations.write_from_data(data, model_id)

    return media_type, total


def set_time(path, timestamp):
    if platform.system() == 'Windows':
        setctime(path, timestamp)
    pathlib.os.utime(path, (timestamp, timestamp))


def get_error_message(content):
    error_content = content.get('error', 'No error message available')
    try:
        return error_content.get('message', 'No error message available')
    except AttributeError:
        return error_content
def createfilename(url,username,model_id=None,date=None,id_=None,media_type=None,text=None,count=None):
    return url.split('.')[-2].split('/')[-1].strip("/,.;!_-@#$%^&*()+\\ ")