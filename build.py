import dominate # https://github.com/Knio/dominate
from pathlib import Path
import json

def image_with_link_to_itself(src, **kwargs):
	with dominate.tags.a(href=src):
		dominate.tags.img(src=src, **kwargs),

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
		dominate.tags.meta(name="viewport", content="width=device-width, initial-scale=1") # This fixes the problem of small font (some texts and also the math) in mobile devices, see https://stackoverflow.com/a/35564095/8849755

	with doc:
		dominate.tags.h1(thing_data['name'])

		# Links to maps:
		lat = thing_data['coordinates'][0]
		lon = thing_data['coordinates'][1]
		with dominate.tags.div(style='margin: 22px;'):
			dominate.tags.a(thing_data['address'], href=f'https://www.google.com/maps/place/{lat},{lon}/@{lat},{lon-.0015},111a,35y,90h,50t/data=!3m1!1e3!4m4!3m3!8m2!3d{lat}!4d{lon}?entry=ttu')

		for extension in {'jpg','png','svg'}:
			path_to_thing_in_murerplan = path_to_thing_folder/f'in_murerplan.{extension}'
			if path_to_thing_in_murerplan.is_file():
				image_with_link_to_itself(
					src = path_to_thing_in_murerplan.relative_to(path_to_thing_folder),
					style = 'max-width: 99%; max-height: 45vh; height: 333px; object-fit: cover; border-radius: 5px;',
				)
				break

		path_to_pics = path_to_thing_folder/'pics'
		if path_to_pics.is_dir():
			with dominate.tags.div(style='display: flex; flex-direction: row; flex-wrap: wrap; gap: 10px; margin-top: 22px;'):
				for path_to_pic in path_to_pics.iterdir():
					image_with_link_to_itself(src=path_to_pic.relative_to(path_to_thing_folder), style='max-width: 99%; max-height: 45vh; height: 333px; object-fit: cover; border-radius: 5px;')

	with open(path_to_thing_folder/'index.html', 'w') as ofile:
		print(doc, file=ofile)

if __name__ == '__main__':
	for path_to_thing_folder in Path('things').iterdir():
		create_thing_page(path_to_thing_folder)