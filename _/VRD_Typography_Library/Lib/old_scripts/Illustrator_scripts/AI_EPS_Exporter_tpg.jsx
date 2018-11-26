/*!
 * Description: 
 * Exports layers to SVG files
 * http://sixtudio.com/
 * http://github.com/mtreik/export-svg
 */
 
//Global
var _docRef = app.activeDocument;
var _docPath = _docRef.path;
var _ignoreHidden = true;
var _destination;
var desired_scale = 333; // 367
var _auxDoc;
var dlg = new Window('dialog', 'Multi Exporter');
var set_width = 100;


//ArtBoard size
var boardSizeX = get_scale(448); //Modify if you vary the size of the canvas where the layer is exported
var boardSizeY = get_scale(299); //Modify if you vary the size of the canvas where the layer is exported

var artBoardSize = (function setArtBoardSize(){
	var size = [0 - boardSizeX, 0, 0, 0 - boardSizeY];
	return size;
}());

//SVG Export Options
var epsExportOptions = (function epsExportOptions(){
	var options = new EPSSaveOptions();
	options.includeDocumentThumbnails = true;
	options.saveMultipleArtboards = false;
	options.compatibility = Compatibility.ILLUSTRATOR8;
	return options;
}());

//-*-Start export
function initExport(){

	//Get N1 layers
	var layersN1 = _docRef.layers[0].layers;

	//dlg.add('statictext', undefined, layersN1);

	for(i = 0; i < layersN1.length; i++){
		
		//Get N1 layer
		var layerN1 = layersN1[i];
		
		//Export N1 layer
		exportLayer(layerN1);
	}	
	
	//Close the auxiliar document
	_auxDoc.close(SaveOptions.DONOTSAVECHANGES);
}

//-*-Export Layer
function exportLayer(layer, path){
	
	if(!(_ignoreHidden && !layer.visible)){
		
		try { 
			copyLayerTo(layer, _auxDoc);		
			selectAll(_auxDoc);

			//resizeartboard(_auxDoc)

			reNameLayer(_auxDoc, layer.name);		
			var set_width = centerLayer(_auxDoc) + 120;
			//
			//
			ungroup(_auxDoc);
			ungroup(_auxDoc);
			//
			//
			exportAsEPS(validateLayerName(layer.name, '-')+"~"+set_width, _auxDoc, path);
			
			//Delete all the content of auxiliar document
			_auxDoc.activeLayer.pageItems.removeAll();
		}catch(ex){
	    	
	    };
	}
};

function get_scale (_num){

	_calc = (_num / 100) * desired_scale;
	//Finish it up with some simple addition
	return /*_num + */_calc;

}
/*
function resizeartboard(_auxDoc){

	

    var abBounds = _auxDoc.artboards[0].artboardRect;// left, top, right, bottom


    var ableft = abBounds[0]; // 0
    var abtop = abBounds[1]; // 612
    var abwidth = abBounds[2] - ableft; // 792 // width
    var abheight = abtop- abBounds[3]; // 0 // height

    var abctrx = abwidth/2+ableft;
    var abctry = abtop-abheight/2;

    var ableft = abctrx-width/2;
    var abtop = abctry+height/2;
    var abright = abctrx+width/2;
    var abbottom = abctry-height/2;

    _auxDoc.artboards[0].artboardRect = [ableft, abtop, abright, abbottom];

}*/
//-*-Copy layer to auxiliar document
function copyLayerTo(layer, doc){
	var pageItem;
	var numPageItems = layer.pageItems.length;
	for (var i = 0; i < numPageItems; i += 1){
		pageItem = layer.pageItems[i];
		pageItem.duplicate(_auxDoc.activeLayer, ElementPlacement.PLACEATEND);
	}
};

//-*-Selectt all
function selectAll(doc){
	var pageItems = doc.pageItems;
	var numPageItems = doc.pageItems.length;
	for (var i = 0; i < numPageItems; i += 1){
		
		var item = pageItems[i];
		item.selected = true;

	}
};

//-*-Rename layer
function reNameLayer(doc, name){
	doc.activeLayer.name = name;
};
//
function getChildAll(obj)
{
	var childsArr = new Array();
	for(var i=0;i<obj.pageItems.length;i++)childsArr.push(obj.pageItems[i]);
	return childsArr;
}


function ungroup(obj)
{
	var elements = getChildAll(obj);
	if(elements.length<1){
		obj.remove();
		return;
	}else{
		for(var i=0;i<elements.length;i++)
		{
			try{
				if(elements[i].parent.typename!="Layer"){
					elements[i].moveBefore(obj)
				};
				if(elements[i].typename=="GroupItem"){
					ungroup(elements[i])
				};
			}catch(e){
				//alert(e)
			}
		}
	}
	//return obj
}

//-*-Center layer
function centerLayer(doc){
	var layer = doc.layers;
	var group = layer[0].groupItems[0];
	//
	var has_dot = false;
	//
	var dotX = 0;
	var dotY = 0;
	//
	try{
		//

		//
		//var the_dot = layer[0].groupItems[1];
		var the_dot = layer[0].groupItems[0].groupItems[1];
		//
		//if (the_dot.lenght) {

			//alert(the_dot.name);
			//
			has_dot = true;
			//
			
			//
			
			//
			//the_dot.remove();

		//} else {

		//	alert('no_dot')

		//}
		//
		//var myGroup = blablabla....the group you want to ungroup
		//var myDestinationGroup = blablabla....the group where you want the items once ungrouped, this could be a Layer or a Document
		//ungroup(myDestinationGroup, myGroup); // call the function
		//
	}catch(ex){
		
		has_dot = false;

		//alert('no_dot catch')

	};
	//
	group.resize(
	    desired_scale, // x
	    desired_scale, // y
	    undefined, // changePositions
	    undefined, // changeFillPatterns
	    undefined, // changeFillGradients
	    undefined, // changeStrokePattern
	    undefined, // changeLineWidths    <----  NOTE THIS
	    Transformation.CENTER); // scaleAbout
		
	group.top = 0;
	group.left = 0;
	group.translate(0 - boardSizeX, 0);
	
	//var scaleSizeX = get_scale(group.width); //Modify if you vary the size of the canvas where the layer is exported
	//var scaleSizeY = get_scale(group.height);

	//var scale = desired_scale * 10; 

	if (has_dot) {
		//
		var halfWidth = group.width / 2;
		var halfHeight = group.height / 2;
		var halfBoardSizeX = boardSizeX / 2;
		var halfBoardSizeY = boardSizeY / 2;
		//
		dotX = the_dot.position[0] + (the_dot.width / 2);
		dotY = the_dot.position[1] + ((0 - the_dot.height) / 2);
		//
		var posX = 0 - dotX;
		var posY = 0 - dotY;

		group.translate(posX, posY);
		//
		the_dot.remove();
		//
	} else {

		var halfWidth = group.width / 2;
		var halfHeight = group.height / 2;
		var halfBoardSizeX = boardSizeX / 2;
		var halfBoardSizeY = boardSizeY / 2;
		
		var posX = halfBoardSizeX - halfWidth;
		var posY = halfHeight - halfBoardSizeY;

		group.translate(posX, posY);
	}

	var _group = layer[0].groupItems[0];
	
	return Math.floor(_group.width)
			

};

//-*-Export as SVG
function exportAsEPS(name, doc){
	var file = new File(_destination + '/' + name + '.eps');
	//_auxDoc.exportFile(file, ExportType.EPS, epsExportOptions);
	//options.artboardRange = (artboardIndex+1).toString();
	_auxDoc.saveAs( file, epsExportOptions )
};

//-*-Validate name
function validateLayerName(value, separator){
	separator = separator || '_';
	
	return value//.toLowerCase().replace(/\s/, separator);
};
 
 
//Init
(function(){
	
	//Choose destination folder
	_destination = Folder.selectDialog('Select folder for SVG files.', _docPath);	
	if(!_destination){return;}
	
	//Create auxiliar document
	_auxDoc = app.documents.add(DocumentColorSpace.RGB);
	_auxDoc.artboards[0].artboardRect = artBoardSize;
	
	//Star the export
	initExport();

	dlg.add('statictext', undefined, 'Export Done');

	dlg.show();

}());
