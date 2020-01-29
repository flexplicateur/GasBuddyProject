const puppeteer = require('puppeteer');
const fs = require('fs');
const request = require('request');

const ArgumentParser = require('argparse').ArgumentParser;

const parser = new ArgumentParser({
  addHelp: true,
  version: '0.0.1',
  description: 'Downloads the images for gas stations.',
});

parser.addArgument(['-i', '--input'], {
  help: 'Path to the JSON file containing the annotated links.',
  type: 'string',
  required: true,
});

parser.addArgument(['-o', '--output_directory'], {
  help: 'Path to the directory where the images should be saved.',
  type: 'string',
  required: true,
});

const args = parser.parseArgs();

// Create a directory
if (!fs.existsSync(args.output_directory)) {
  fs.mkdirSync(args.output_directory);
}

var download = function(uri, filename, callback) {
  request.head(uri, function(err, res, body) {
    request(uri)
      .pipe(fs.createWriteStream(filename))
      .on('close', callback);
  });
};

(async () => {
  const data = JSON.parse(fs.readFileSync(args.input));

  const browser = await puppeteer.launch({
    args: ['--no-sandbox'],
    headless: false,
  });

  const input_filename = args.input.split('/')[
    args.input.split('/').length - 1
  ];

  let image_filename = null;
  let image_location = null;

  const page = await browser.newPage();
  let link = null;

  for (let seedIndex = 0; seedIndex < data.length; seedIndex++) {
    const resultsAvailable = data[seedIndex].nearbyStations.results;
    const stationsAvailable = data[seedIndex].nearbyStations.results.length > 0;
    if (!resultsAvailable || !stationsAvailable) {
      continue;
    }
    for (
      let stationIndex = 0;
      stationIndex < data[seedIndex].nearbyStations.results.length;
      stationIndex++
    ) {
      image_filename = `${input_filename.replace(
        '.json',
        '',
      )}_${seedIndex}_${stationIndex}.png`;
      image_location = args.output_directory + '/' + image_filename;

      if (fs.existsSync(image_location)) {
        continue;
      }

      let url = data[seedIndex].nearbyStations.results[stationIndex].isvLink;
      if (!url || url === 'NA') {
        continue;
      }
      while (true) {
        try {
          await page.goto(url.replace(/\,[-+]?[0-9]*\.?[0-9]+z/gi, ',10z'));
          await page.click('button[id="click-to-view"]');
          await page.waitForNavigation();
          await page.click('button[id="share-button"]');
          await page.waitFor(8000);
          link = await page.evaluate(async () => {
            return Promise.resolve(
              document.querySelector('img[id=share-img]').src,
            );
          });
          if (!link.includes('spinner') && link.includes('vimg')) {
            break;
          }
        } catch (e) {
          true; // do nothing and try again
        }
      }

      download(link, image_location, function() {
        console.log(`Downloaded "${image_filename}"! `);
      });
    }
  }
  await browser.close();
})();
