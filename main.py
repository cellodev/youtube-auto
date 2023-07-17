import requests

from moviepy.editor import *


def requesting(link):
    headers = {'Authorization': f'{os.getenv("AUTH")}'}
    saida = requests.get(link, headers=headers)
    return saida.json()


def get_video_link(jso):
    try:
        next_page = jso["next_page"]
    except:
        next_page = "unknown"
    videos = jso["videos"]
    for video in videos:
        video_id = video["id"]
        video_files = video["video_files"]
        for quality in video_files:
            if quality["quality"] == "hd":
                video_size = [quality["width"], quality["height"]]
                link = quality["link"]
                break
    return link, next_page, video_id, video_size


def download_video(link, video_id):
    resp = requests.get(link)
    with open(f"default_videos/{video_id}.mp4", "wb") as f: 
        f.write(resp.content)


def add_id(id):
    with open(f"downloaded_videos.txt", "a") as f: 
        f.write(f"{id}\n")


def read_id(video_id):
    lines = open('downloaded_videos.txt', 'r').readlines()
    if f"{video_id}\n" in lines:
        return True
    return False


def pexels_func(search_link):
    jso = requesting(search_link)
    download_link, search_link, video_id, video_size = get_video_link(jso)
    if read_id(video_id):
        edit = False
        return video_id, search_link, video_size, edit
    edit = True
    download_video(download_link, video_id)
    print("downloaded video.")
    add_id(video_id)
    return video_id, search_link, video_size, edit


def edit_video(video_id, video_size):
    video = VideoFileClip(f"default_videos/{video_id}.mp4")
    if video.duration > 30:
        video = video.subclip(0, 30)
    video.without_audio()
    txt_clip = ImageClip("inscreva.png").set_start(0.5).set_duration(4).set_pos("top").resize(width=video_size[0]/4, height=video_size[1]/4).crossfadein(0.5).crossfadeout(1)
    result = CompositeVideoClip([video, txt_clip]) # Overlay text on video
    result.write_videofile(f"modified_videos/{video_id}-edited.mp4", fps=25)


if __name__== "__main__":
    search_link = "https://api.pexels.com/v1/videos/search/?orientation=portrait&page=1&per_page=1&query=cute+cats&size=medium"
    while search_link != "unknown":
        video_id, search_link, video_size, edit = pexels_func(search_link)
        if edit:
            edit_video(video_id, video_size)
        input()