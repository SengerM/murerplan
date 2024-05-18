import dominate, dominate.tags as tags # https://github.com/Knio/dominate
from pathlib import Path
import json
import os.path

def image_with_link_to_itself(src, **kwargs):
	with dominate.tags.a(href=src):
		dominate.tags.img(src=src, **kwargs),

def create_thing_page(path_to_thing_folder:Path, path_to_build_directory:Path):
	PICTURES_BORDER = 'border-radius: 5px; border-style: solid; border-color: #4e4f4e;'

	path_to_things_pages = path_to_build_directory/'things'
	path_to_thing_folder_relative_from_thing_build_directory = Path(os.path.relpath(
		(path_to_thing_folder).resolve(),
		start = path_to_things_pages.resolve(),
	))

	thing_id = path_to_thing_folder.name

	with open(path_to_thing_folder/'data.json', 'r') as ifile:
		thing_data = json.load(ifile)

	doc = dominate.document(title=thing_data['name'])

	with doc.head:
		tags.link(rel="preconnect", href="https://fonts.googleapis.com")
		tags.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=True)
		tags.link(href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap", rel="stylesheet")
		tags.link(rel="stylesheet", href="../../css/main.css")
		tags.meta(name="viewport", content="width=device-width, initial-scale=1") # This fixes the problem of small font (some texts and also the math) in mobile devices, see https://stackoverflow.com/a/35564095/8849755

	with doc:
		with tags.div(style='display:flex; gap: 10px; flex-wrap: wrap; flex-direction: row-reverse; justify-content: flex-end;'):
			with tags.div():
				tags.h1(thing_data['name'])

				lat = thing_data['coordinates'][0]
				lon = thing_data['coordinates'][1]
				tags.a(thing_data['address'], href=f'https://www.google.com/maps/place/{lat},{lon}/@{lat},{lon-.0015},111a,35y,90h,50t/data=!3m1!1e3!4m4!3m3!8m2!3d{lat}!4d{lon}?entry=ttu')

			with tags.div():
				for extension in {'jpg','png','svg'}:
					if (path_to_thing_folder/f'in_murerplan.{extension}').is_file():
						tags.img(
							src = path_to_thing_folder_relative_from_thing_build_directory/f'in_murerplan.{extension}',
							style = 'height: 45vh;' + PICTURES_BORDER,
						)
						break

		path_to_pics = path_to_thing_folder/'pics'
		if path_to_pics.is_dir():
<<<<<<< ours
			with dominate.tags.div(style='display: flex; flex-direction: row; flex-wrap: no-wrap; gap: 10px; margin-top: 10px; overflow: auto;'):
				for path_to_pic in sorted(path_to_pics.iterdir()):
					dominate.tags.img(
						src = path_to_pic.relative_to(path_to_thing_folder),
=======
			with tags.div(style='display: flex; flex-direction: row; flex-wrap: no-wrap; gap: 10px; margin-top: 10px; overflow: auto;'):
				for path_to_pic in path_to_pics.iterdir():
					tags.img(
						src = path_to_thing_folder_relative_from_thing_build_directory/'pics'/path_to_pic.name,
>>>>>>> theirs
						style = 'max-height: 45vh; height: 333px;' + PICTURES_BORDER,
					)

	path_to_things_pages.mkdir(exist_ok=True)
	with open(path_to_things_pages/f'{thing_id}.html', 'w') as ofile:
		print(doc, file=ofile)

def build_index(path_to_build_directory:Path):
	doc = dominate.document(title='Murerplan')

	with doc:
		with tags.div(
			id='welcome_msg',
			style = 'position: absolute; top: 50%; left: 50%; margin-top: -50vh; margin-left: -50vw; height: 100vh; width: 100vw; background-color: rgba(0,0,0,.9); color: white; padding: 11px;',
		):
			tags.div('Welcome to the interactive Murerplan')
			tags.button('Start', onclick = 'start_murerplan()', style='margin: 22px;')

		with tags.div(style='width: 98.5vw; height: 97vh;'):
			tags.iframe(
				src = os.path.relpath((Path('.')/'Murerplan.svg').resolve(), start=path_to_build_directory.resolve()),
				style = 'width: 100%; height: 100%; border: 0;',
			)

		tags.script(src=os.path.relpath((Path('.')/'js/start_murerplan.js').resolve(), start=path_to_build_directory.resolve()))

	with open(path_to_build_directory/'index.html', 'w') as ofile:
		print(doc, file=ofile)

def build_site():
	BUILD_DIRECTORY = Path('.')/'build'

	BUILD_DIRECTORY.mkdir(exist_ok=True)

	build_index(BUILD_DIRECTORY)

	for path_to_thing_folder in Path('things').iterdir():
		create_thing_page(path_to_thing_folder, BUILD_DIRECTORY)

if __name__ == '__main__':
	build_site()