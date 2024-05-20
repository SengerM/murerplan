import dominate, dominate.tags as tags # https://github.com/Knio/dominate
from pathlib import Path
import json
import os.path

def add_google_analytics(doc):
	with doc.head:
		tags.script(_async=True, src="https://www.googletagmanager.com/gtag/js?id=G-G7QNGJN4FP")
		tags.script(
			'''
			window.dataLayer = window.dataLayer || [];
			function gtag(){dataLayer.push(arguments);}
			gtag('js', new Date());

			gtag('config', 'G-G7QNGJN4FP');
		'''
		)

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
		tags.link(rel="stylesheet", href="../../css/main.css")
		tags.meta(name="viewport", content="width=device-width, initial-scale=1") # This fixes the problem of small font (some texts and also the math) in mobile devices, see https://stackoverflow.com/a/35564095/8849755

	add_google_analytics(doc)

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
			with tags.div(style='display: flex; flex-direction: row; flex-wrap: no-wrap; gap: 10px; margin-top: 10px; overflow: auto;'):
				for path_to_pic in sorted(path_to_pics.iterdir()):
					tags.img(
						src = path_to_thing_folder_relative_from_thing_build_directory/'pics'/path_to_pic.name,
						style = 'max-height: 45vh; height: 333px;' + PICTURES_BORDER,
					)

	path_to_things_pages.mkdir(exist_ok=True)
	with open(path_to_things_pages/f'{thing_id}.html', 'w') as ofile:
		print(doc, file=ofile)

def build_index(path_to_build_directory:Path):
	doc = dominate.document(title='Murerplan')

	with doc.head:
		tags.link(rel="stylesheet", href="../css/main.css")
		tags.meta(name="viewport", content="width=device-width, initial-scale=1") # This fixes the problem of small font (some texts and also the math) in mobile devices, see https://stackoverflow.com/a/35564095/8849755

	add_google_analytics(doc)

	with doc:
		with tags.div(
			id='welcome_msg',
			style = 'margin: auto; width: 88vw; max-width: 444px; padding: 11px; border-radius: 11px; font-size: 155%;',
		):
			tags.h1('Interactive Murerplan')
			tags.p('The Murerplan is a map of Zürich from 1576. Here, you can click on the buildings to compare how they look today. Enjoy!')
			with tags.div(style='width: 100%; display: flex; justify-content: center;'):
				tags.button('Start', onclick = 'start_murerplan()', style='margin: 22px; font-size: 200%;')

		with tags.div(id='murerplan', style='display: none; width: 2122px; height: 1455px;'):
			tags.iframe(
				src = os.path.relpath((Path('.')/'Murerplan.svg').resolve(), start=path_to_build_directory.resolve()),
				style = 'width: 2119.418px; height: 1442.618px; border: 2px; border-color: black; border-style: solid; border-radius: 10px;',
			)
			with tags.div():
				with tags.div():
					tags.span('Arthur Dürst: Die Planvedute der Stadt Zürich von Jos Murer, 1576. In: Cartographica Helvetica. Heft 15 (1997), S. 23–37. ')
					tags.a('doi:10.5169/seals-9067', href='https://doi.org/10.5169/seals-9067', target='_blank')
				with tags.div():
					tags.span('Murerplan in high resolution available in ')
					tags.a('this link', href='https://www.e-gs.ethz.ch/eMP/eMuseumPlus?service=ExternalSearch&module=collection&viewType=detailList&fulltext=Planvedute%20der%20Stadt%20Z%C3%BCrich', target='_blank')

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