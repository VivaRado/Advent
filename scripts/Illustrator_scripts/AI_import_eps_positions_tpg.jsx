// Import SVG Files as Layers - Illustrator CS3 script
// Description: Imports a folder of SVG files as named layers into a new document
// Author: VivaRado
// Version: 0.0.1 on 2014-05-29
var desired_scale = 15;
var boardSizeX = 1000;
var boardSizeY = 1000;
var doc;
var rad = 10;
var columns = 4;
var initial_circle = false;

function getFolder() {
	return Folder.selectDialog('Please select the folder to be imported:', Folder('~'));
}

function get_scale (_num){

	_calc = (_num / 100) * desired_scale;
	//Finish it up with some simple addition
	return /*_num + */_calc;

}

//
function addCircle(new_l, number, left, top, right, bottom){
	//
	g_items = new_l.groupItems;
	//
	elipse = doc.pathItems.ellipse(
		left,top,
		right, bottom/*, 
		false, false*/
	);
	//
	elipse.name = "✕"
	//
	var col = new RGBColor();
	col.red = 255;
	col.green = 0;
	col.blue = 0;
	//
	var swatch = doc.swatches.add();
	swatch.color = col;
	swatch.name = "col";
	//
	elipse.filled = true;
	elipse.fillColor = swatch.color;
	//
	newShapeGroup = doc.groupItems.add();
	//
	newShapeGroup.name = "✕";
	//
	elipse.moveToBeginning( newShapeGroup )
	//
	//
	new_l.groupItems[0].moveToEnd( newGroup )
	//g_items[1].moveToBeginning( newGroup )
	//
	if (number == 0) {
		//
		initial_circle = elipse;
		//
	}
	//
	redraw();
	//
	return elipse
	//
}

function createSpotMark(indx, newLayer){
	//
	//var length = doc.layers.length-1;
	//
	//alert(newLayer.groupItems[0])
	//
	var new_circle;
	//
	var _pa = newLayer.groupItems[0].pageItems;
	//
	//alert(_pa)
	//alert(_pa.length)
	//
	for (var iter=0 ; iter<_pa.length; iter++ ){
		//
		var item = _pa[iter];
		// alert(item.pageItems)
		var typename = item.typename;
		//
		//alert(typename)
		// apply action or get the subitems of object
		//if (typename === "PathItem"){
			//
			//alert(item.pathItems.length)
			//item.clipping = false;

		//} 
		if (typename === "CompoundPathItem" ) {
			
			//alert(item.pathItems.length)
			//
			for (var x = 0; x < item.pathItems.length; x++) {
				//
				p_p = item.pathItems[x].pathPoints;
				p_p_l = p_p.length;
				//
				//alert(p_p_l)
				//
				if (p_p_l <= 2) {
					//
					//alert(p_p_l)
					//
					p_item = item.pathItems[x]

					//
					//alert(p_item)
					//alert(p_item.position)
					//alert(p_item.width)
					//alert(p_item.height)
					//
					pos_x = item.pathItems[x].position[1];
					pos_y = item.pathItems[x].position[0];
					//
					new_circle = addCircle(newLayer, indx, pos_x + 0.5, pos_y, 1, 1);
					//
					p_item.remove();
					//
				}
				//
			}
			//
		}
		//
	}
	//
	return new_circle
	//
}
//
function importFolderAsLayers(selectedFolder) {  
	// if a folder was selected continue with action, otherwise quit
	var document;
	var mm = 2.83464567; // Metric MM converter…  
	// Set the script to work with artboard rulers  
	app.coordinateSystem = CoordinateSystem.ARTBOARDCOORDINATESYSTEM;  

	if (selectedFolder) {
		document = app.documents.add(
			DocumentColorSpace.RGB,  
			width = boardSizeX,
			height = boardSizeY,
		);
		//
		doc = document;
		//
		var firstImageLayer = true;
		var newLayer;
		var thisPlacedItem;
		var marginX=boardSizeX/2;
		var marginY=boardSizeY/2;
		var posX=0+marginX;
		var posY=0+marginY;
		var count=0;
		var movementX = 0;
		var movementY = 0;
		// create document list from files in selected folder
		var imageList = selectedFolder.getFiles().sort();
	
		for (var i = 0; i < imageList.length; i++) {
			try{

				if (imageList[i] instanceof File) {
					var fileName = imageList[i].name;
					if( (fileName.indexOf(".eps") == -1) ) {
						continue;
					} else {
						if( firstImageLayer ) {
							newLayer = document.layers[0];
							firstImageLayer = false;

						} else {
							newLayer = document.layers.add();
						}
						// Give the layer the name of the image file
						newLayer.name = fileName.substring(0, fileName.indexOf(".") );
						//
						//alert(newLayer.name)
						// Place the image on the artboard
						newGroup = newLayer.groupItems.createFromFile( imageList[i] );
						//
						newGroup.resize(
							desired_scale, // x
							desired_scale, // y
							undefined, // changePositions
							undefined, // changeFillPatterns
							undefined, // changeFillGradients
							undefined, // changeStrokePattern
							undefined, // changeLineWidths    <----  NOTE THIS
							Transformation.CENTER); // scaleAbout
						//
						newGroup.position = [ -6000, 6000]
						//
					}
				}
				//
				new_circle_ret = createSpotMark(i, newLayer);
				//
				if (initial_circle == false) {

					diffe = 0;

				} else {
					
					diffe = ( newGroup.position[1] - new_circle_ret.position[1] )
				}
				//
				//alert( (boardSizeX/2 + marginX ) * columns )
				//alert( initial_circle.position[0] + movementX )
				//
				//
				posX = initial_circle.position[0] + movementX;
				posY = (initial_circle.position[1] + diffe) - movementY;
				//	
				newGroup.position = [ posX , posY ];
				//
				if ((initial_circle.position[0] + movementX + boardSizeX ) >= (boardSizeX + marginX) * columns) {

					movementX = 0;
					movementY = movementY + marginY;

				} else {
					
					movementX = movementX + marginX;
				}
				/*if ( ( posX + boardSizeX + marginX ) >= ( boardSizeX + marginX ) * columns ) {

					posX = initial_circle.position[0] + marginX;
					movement = 0;

				} else {*/

					//movement = movement + 5 + 5;

				//}
				//
			}
			catch(err){

			}
		}
		if( firstImageLayer ) {
			// alert("The action has been cancelled.");
			// display error message if no supported documents were found in the designated folder
			alert("Sorry, but the designated folder does not contain any recognized image formats.\n\nPlease choose another folder.");
			document.close();
			importFolderAsLayers(getFolder());
		}
	} else {
		// alert("The action has been cancelled.");
		// display error message if no supported documents were found in the designated folder
		alert("Rerun the script and choose a folder with images.");
		//importFolderAsLayers(getFolder());
	}
}

// Start the script off
importFolderAsLayers( getFolder() );