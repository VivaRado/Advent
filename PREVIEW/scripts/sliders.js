function axisSlidersToSamples(sliders, samples) {
	var inputs = document.querySelectorAll(sliders);
	var outputs = document.querySelectorAll(samples);

	function doAxes(evt) {

		var i, l, axes = {}, ffs = [];

		for (i=0, l=inputs.length; i<l; i++) {

			if (inputs[i].name == "mirror") {
				
				mirror_state = 0

				if(inputs[i].checked){

					mirror_state = 1

				} 

				axes[inputs[i].name] = mirror_state;
				
			} else {

				axes[inputs[i].name] = inputs[i].value;
			}
		}

		for (i in axes) {
			
			if (i == "wght" || i == "ital" || i == "wdth" || i == "opsz" || i == "grad") {
			
				if (evt.target.className == "size") {
					
					if (axes["mirror"] == 1 && i == "opsz") {
						
						$(".opsz").val($(".size").val())
						
					}

				}
				
				ffs.push('"' + i + '" ' + axes[i]);

			}
			
		}

			console.log(ffs)
		ffsj = ffs.join(', ') || 'normal';

		for (i=0, l=outputs.length; i<l; i++) {
			
			outputs[i].style.fontVariationSettings = ffsj;
			outputs[i].style.fontSize = axes["size"]+'pt';

			//no_optical = ffs.splice(0,ffs.length-1).join(', ')

			$(".typeface h2")[0].style.fontVariationSettings = ffsj//no_optical;
			//$(".typeface h2").css({"font-optical-sizing":"none"});

		}
	}
	
	var i, l;

	for (i=0, l=inputs.length; i<l; i++) {

		$(inputs[i]).on('input', doAxes);
		$(inputs[i]).on('change', doAxes);

	}
}

document.querySelectorAll('.typeface:not(.loaded)').forEach(function(li) {
	axisSlidersToSamples('#' + li.id + ' input', '#' + li.id + ' .sample');
	li.className += ' loaded';
});
//
function fluctuate_slider(targ, speed) {
	var max_val = targ.attr('max');
	var min_val = targ.attr('min');
	var step = parseFloat(targ.attr('step'));
	//
	var counter = 0;
	var inc = +step;
	setInterval(function(){
		//
	    if(counter >= max_val) {
	    	inc = inc - step;
	    }else if(counter <= min_val) {
	    	inc = inc + step;
	    }
	    //
	    counter = counter + inc;
		targ.val(counter).trigger('change');
		//

	}, speed);

}
//
$(function(){
	//
	var targ = $('#advent_thnregbld-wght');
	var targ_2 = $('#advent_thnregbld-ital');
	var targ_3= $('#advent_thnregbld-wdth');
	//
	//fluctuate_slider(targ, 50);
	//fluctuate_slider(targ_2, 150);
	//fluctuate_slider(targ_3, 100);
	//
});