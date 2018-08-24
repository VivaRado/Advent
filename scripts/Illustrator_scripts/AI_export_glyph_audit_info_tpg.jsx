
var doc = app.activeDocument; 
var all_layer_text = "";
//
function getFolder() {
	return Folder.selectDialog('Please select the folder to export the Glyph Audit:', Folder('~'));
}
//
function formattedDate(){
	var date = new Date();  
	var options = {  
	    weekday: "long", year: "numeric", month: "short",  
	    day: "numeric", hour: "2-digit", minute: "2-digit"  
	};
	the_date = date.toLocaleTimeString("en-us", options);
	the_date = the_date.replace(/, /g, '_').replace(/ /g, '_').replace(/:/g, '_');
	return the_date
}
//
//
function save_file(_file){

	var docText = "layer_name,glyph_layer_index,glyph_laer_name,anchor_count_array";
	//
	docText = docText + all_layer_text;
	//
	_file.open('e');  
	_file.write(docText);  
	_file.close(); 
	//
}
//
//
function get_anchor_count(layer_name,layer_index, glyph_index, target_layer){
	//
	anchor_info_text = '';
	//
	var path_item_list = [];
	//
	var _pa = target_layer.groupItems[0].pageItems;
	//
	for (var iter=0 ; iter<_pa.length; iter++ ){
		//
		var item = _pa[iter];
		//
		var typename = item.typename;
		//
		anchor_info = [];
		//
		if (typename === "CompoundPathItem" ) {
			//
			for (var x = 0; x < item.pathItems.length; x++) {
				//
				p_p = item.pathItems[x].pathPoints;
				p_p_l = p_p.length;
				//
				if (p_p_l > 2) {
					//
					anchor_info.push(p_p_l);
					//
					p_item = item.pathItems[x]
					//
				}
				//
			}
			//
		}
		//
		if (anchor_info.length > 0) {

			path_item_list.push([anchor_info])

		}
		//
	}
	//
	for (var y = 0; y < path_item_list.length; y++) {
		//
		path_list = path_item_list[y];
		//
		anchor_info_text = anchor_info_text+'"'+layer_name+'",'+glyph_index+',"'+target_layer.name+'",';
		//
		anchor_info_text = anchor_info_text
						   +'"['+path_list.join(',')+']"'
		//
	}
	//
	return anchor_info_text+'\r'
	//
}
//
var _name = 'glyph_audit'+'_'+formattedDate();
//
var _dir = getFolder();
var _file = File(_dir+'/'+_name+'.csv');
//
var doc_layers = doc.layers;
//
for (var i = 0; i < doc_layers.length; i++) {
	//
	layer_glyph_info_text = '';
	//
	glyph_layers = doc_layers[i].layers;
	//
	for (var x = 0; x < glyph_layers.length; x++) {
		//
		layer_glyph_info_text = layer_glyph_info_text + get_anchor_count(doc_layers[i].name,i,x,glyph_layers[x]);
		//
	}
	//
	all_layer_text = all_layer_text + layer_glyph_info_text;
	//
}
//
save_file(_file)