<h1 align="center">Ytty - Powerful tool for parsing, downloading and uploading videos from youtube based on selenium.</h1>
<h1 align="center"> -WARINING!!!- </h1>

```
You must have Google Chrome installed for google auth bypass!
```

<h1 align="center"> -How to use?- </h1>

<h2 align="center"> -Quickstart- </h2>

```python
from ytty import *

if __name__ == '__main__':
	session = shadow_session()
	options = YTOptions()
	options.parse.search = 'FREE FIRE MOD MENU'
	options.parse.period = 1
	options.parse.max = 10
	videos = parse_videos(session, options)
	video = get_video(videos[0]['link'])
	session.quit()

	session = google_session('login', 'password')
	options.upload.video = video
	options.upload.title = videos[0]['title']
	options.upload.description = '''This you can write description for video
	That text written for example, you can write this what do you want :)'''
	options.upload.tags = ['tags', 'writes', 'in a', 'taglist', 'add', 'some tags', 'this']
	options.upload.preview = get_thumbnail(videos[0]['id'])
	upload_video(session, options)
```


<h2 align="center"> -Parsing videos- </h2>

```python
from ytty import *

if __name__ == '__main__':
	session = shadow_session() #headless chrome session without login
	options = YTOptions()
	options.parse.search = 'FREE FIRE MOD MENU' #Search request
	options.parse.period = 1 #Period from 0 to 2 when -> 0 - Today | 1 - a Week | 2 - a Month (Default is 2)
	options.parse.max = 10 #Limit of parsing video (Default is 20)

	videos = parse_videos(session, options)
	for video in videos:
		title = video['title'] #video title
		link = video['link'] #video link
		id = video['id'] #video id
	session.quit() #For close session
```

<h2 align="center"> -Download thumbnails (previews)- </h2>

```python
for video in videos:
	get_thumbnail(video['id']) #returns filename of preview
```

<h2 align="center"> -Download videos- </h2>

```python
for video in videos:
	get_video(video['link']) #returns filename of video
```

<h2 align="center"> -Download video with uniqualization- </h2>

```python
for video in videos:
	options = YTOptions()
	options.download.unique = True # if use vidspinner (ffmpeg to uniqualize, but it for Windows only)
	get_video(video['link'], options)
```

<h2 align="center"> -Upload videos- </h2>

```python
for video in videos:
	session = google_session('login', 'password') #session with login in google (no headless)
	
	options = YTOptions()
	options.upload.video = 'C:/path-to/video.mp4'
	options.upload.title = videos[0]['title']
	options.upload.description = '''This you can write description for video
	That text written for example, you can write this what do you want :)'''
	options.upload.tags = ['tags', 'writes', 'in a', 'taglist', 'add', 'some tags', 'this']
	options.upload.preview = 'C:/path-to/thumbnails.jpg'

	upload_video(session, options)
```

<h2 align="center"> -Upload video as premiere and access management- </h2>

```python
for video in videos:
	options.upload.acess = 'PUBLIC' #is default | UNLISTED - Acess by link | PRIVATE - Restricted access | SCHEDULE - Planned release (not yet configurable)
	options.upload.premiere = True
```