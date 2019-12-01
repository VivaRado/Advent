function axisSlidersToSamples(sliders, samples) {
	var inputs = document.querySelectorAll(sliders);
	var outputs = document.querySelectorAll(samples);

	function doAxes() {
		var i, l, axes = {}, ffs = [];
		for (i=0, l=inputs.length; i<l; i++) {
			axes[inputs[i].name] = inputs[i].value;
		}
		for (i in axes) {
			if (i.length === 4) {
				ffs.push('"' + i + '" ' + axes[i]);
			}
		}
		ffs = ffs.join(', ') || 'normal';
		
		for (i=0, l=outputs.length; i<l; i++) {
			outputs[i].style.fontVariationSettings = ffs;
			$(".typeface h2")[0].style.fontVariationSettings = ffs;
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