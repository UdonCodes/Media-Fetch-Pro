from script.plugins.bilibili import Bilibili
from script.plugins.bilibili_playlist import BilibiliPlayList
from script.plugins.youtube import Youtube
from script.plugins.endDownloader import EndDownloader

from script.utils.video import renameDir

from script.api import request

from script.model.videoInfo import VideoInfo

import json
import os

def FetchVideoInfo(url: str, storagePath: str):
    websites = Bilibili(BilibiliPlayList(Youtube(EndDownloader())))
    video_info_array = websites.getVideoInfo(url)
    print(json.dumps(list(map(lambda x:x.serialize(),video_info_array)),indent=4, separators=(',', ': ')))
    for video_info in video_info_array:
        request.updateVideoStatus(video_info)


def DownloadVideo(video_info: VideoInfo, storagePath: str):
    try:
        if(video_info.type != "episode"):
            storagePath = storagePath + "/" + video_info.get_id() # video and playlist
        else: # 
            storagePath = storagePath + "/" + video_info.parent
        
        if not(os.path.isdir(storagePath)):
            os.mkdir(storagePath)
    except Exception as e:
        print(e)

    websites = Bilibili(BilibiliPlayList(Youtube(EndDownloader())))

    if video_info.get_type() == "playlist":
        # this is generate a tvshow.nfo🤔 it is very very hard.
        websites.downloadNfo(video_info,args.storage)
        websites.downloadPoster(video_info,args.storage)
        
        # TODO it is a problem how to rename playlist🤔

    elif video_info.type == "video":
        if video_info.get_type() == "video": # episode didn't generate nfo
            websites.downloadNfo(video_info,args.storage)
            print("下载nfo成功")

        websites.downloadPoster(video_info,args.storage)
        websites.downloadVideo(video_info,args.storage)

        video_info.set_status("finished")
        request.updateVideoStatus(video_info)
        
    elif video_info.type == "episode":
        websites.downloadVideo(video_info,args.storage)
        video_info.set_status("finished")
        request.updateVideoStatus(video_info)

def Rename(video_info: VideoInfo, storagePath: str):
    renameDir(f"{storagePath}/{video_info.get_id()}",f"{video_info.get_title()}") 
