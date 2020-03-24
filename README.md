# Chrome extension downloader for ungoogled-chromium
This simple python script downloads extensions from the Chrome Web Store and unpacks so you can use them with [ungoogled-chromium](https://github.com/Eloston/ungoogled-chromium).

## Usage:
  * Create your settings file (based on the [example](settings.example.json))
  * Run the script `python crxdownloader.py <extension id/chrome web store url>`
  * Go to chrome://extensions/
  * Turn on 'Developer mode'
  * Click on 'Load unpacked' and select the extension's folder

## License
[MIT License](LICENSE).