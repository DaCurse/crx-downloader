import re
import json
import zipfile
from urllib import parse, request
from os import path, remove
from shutil import copytree, rmtree
from sys import argv, exit

SETTINGS_PATH = './settings.json'


def load_settings():
  try:
    with open(SETTINGS_PATH, 'r') as settings_file:
      return json.load(settings_file)
  except FileNotFoundError:
    print(f'Couldn\'t find settings file: {SETTINGS_PATH}, did you forget to create one?')
    exit()


def download_crx(ext_id):
  payload = settings['payload'].format(id=ext_id)
  url = settings['base_url'] + parse.quote(payload)
  print(f'Downloading {url}')

  res = request.urlopen(url)
  with open(settings['tmp_filename'], 'wb') as crx_file:
    crx_file.write(res.read())
    filename = crx_file.name
  
  return filename


def unpack_crx(filename):
  folder = path.abspath(settings['tmp_folder'])

  with zipfile.ZipFile(filename, mode='r') as archive:
    archive.extractall(folder)

  return folder


def install_ext(path_from):
  with open(path.join(path_from, 'manifest.json'), 'r') as manifest:
    ext_manifest = json.load(manifest)
    ext_name = ext_manifest['name']
    ext_version = ext_manifest['version']

  install_path = path.join(settings['extension_folder'], ext_name)
  cleanup(install_path)

  print(f'Installing {ext_name} v{ext_version} extension to {install_path}')
  copytree(path_from, install_path)


def cleanup(*args):
  for arg in args:
    if path.isdir(arg):
      rmtree(arg)
    elif path.isfile(arg):
      remove(arg)


if __name__ == "__main__":
  settings = load_settings()
  
  inp = input('Enter extension id/chrome web store url: ') if len(argv) < 2 else argv[1]
  url_match = re.search(settings['url_regex'], inp)
  ext_id = inp if url_match is None else url_match.groups()[0]
  
  print(f'Downloading extension with id: "{ext_id}"...')
  crx_file = download_crx(ext_id)
  print(f'Finished downloading extension to {crx_file}')

  print('Unpacking .crx file...')
  ext_folder = unpack_crx(crx_file)
  print(f'Extension archive unpacked to {ext_folder}')

  print(f'Installing extension...')
  install_ext(ext_folder)

  print('Successfully installed extension! Cleaning up...')
  cleanup(crx_file, ext_folder)

  ext_folder = settings['extension_folder']
  print(f'{__file__} is done, please add the unpacked extension in Chromium. Extension folder: {ext_folder}')
