# GasBuddy Project

TBC

## Authors

Kevin Dick - Carleton University - <KevinDick@cmail.carleton.ca>
Francois Charih - Carleton University - <francoischarih@sce.carleton.ca>
Jimmy Woo - Carleton University - N/A
James R. Green - Carleton University - <jrgreen@sce.carleton.ca>

## How to use the data collection app

### Development version

To use the data collection app, you may use the development version by cloning
this repository and running it. This approach requires that you install 
`Node.js`, `yarn`, and all the necessary dependencies. 

After downloading `Node.js` and `yarn` you would do the following:

```
$ cd data-collection-app
$ yarn
$ yarn dev
```

### Production version

You may download the executable for your platform:

* [Windows](http://cu-bic.ca/public/data-collection-app-win.zip)
* [macOS](http://cu-bic.ca/public/data-collection-app-macos.zip)


## Downloading the images in a JSON

Use the package built to download images.

```
$ cd image-collection
$ npm install
$ node index.js -i <JSON file> -o <output directory>
```
