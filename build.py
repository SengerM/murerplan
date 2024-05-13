import dominate # https://github.com/Knio/dominate
from pathlib import Path
import json

def create_thing_page(path_to_thing_folder:Path):
	thing_id = path_to_thing_folder.name

	with open(path_to_thing_folder/'data.json', 'r') as ifile:
		thing_data = json.load(ifile)

	doc = dominate.document(title=thing_data['name'])

	with doc.head:
		dominate.tags.link(rel="preconnect", href="https://fonts.googleapis.com")
		dominate.tags.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=True)
		dominate.tags.link(href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap", rel="stylesheet")
		dominate.tags.link(rel="stylesheet", href="../../css/main.css")

	with doc:
		dominate.tags.h1(thing_data['name'])
		with dominate.tags.ul():
			dominate.tags.li(thing_data['address'])

		# Links to maps:
		with dominate.tags.div(style='display: flex; flex-direction: row; flex-wrap: wrap; gap: 10px;'):
			lat = thing_data['coordinates'][0]
			lon = thing_data['coordinates'][1]
			with dominate.tags.a(href=f'https://www.google.com/maps/place/{lat},{lon}/@{lat},{lon-.003},222a,35y,90h,50t/data=!3m1!1e3!4m4!3m3!8m2!3d{lat}!4d{lon}?entry=ttu'):
				dominate.tags.img(
					src = 'https://upload.wikimedia.org/wikipedia/commons/a/aa/Google_Maps_icon_%282020%29.svg',
					style = 'height: 44px',
					title = 'Open in Google Maps',
				)

		with dominate.tags.div(style='display: flex; flex-direction: row; flex-wrap: wrap; gap: 10px; margin-top: 22px;'):
			for path_to_pic in (path_to_thing_folder/'pics').iterdir():
				with dominate.tags.a(href=path_to_pic.relative_to(path_to_thing_folder)):
					dominate.tags.img(src=path_to_pic.relative_to(path_to_thing_folder), style='max-width: 99%; height: 222px; object-fit: cover; border-radius: 5px;')

	with open(path_to_thing_folder/'index.html', 'w') as ofile:
		print(doc, file=ofile)

if __name__ == '__main__':
	for path_to_thing_folder in Path('things').iterdir():
		create_thing_page(path_to_thing_folder)