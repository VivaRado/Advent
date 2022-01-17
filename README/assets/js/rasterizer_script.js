mermaid.initialize({
  theme: 'neutral',
  // themeCSS: '.node rect { fill: red; }',
  logLevel: 3,
  flowchart: { curve: 'linear' },
  gantt: { axisFormat: '%m/%d/%Y' },
  sequence: { actorMargin: 50 },
  // sequenceDiagram: { actorMargin: 300 } // deprecated
});

function get_screenshot(c){
	//
	domtoimage.toJpeg(c, { "quality": 1, "bgcolor": "#f6f8fa" }).then(function(dataUrl) { // toPng
		//
		var img = new Image();
		img.src = dataUrl;
		//
		$(c).empty()
		//
		$(c).append(img)
		//
	  })
	  .catch(function(error) {
		console.error('oops, something went wrong!', error);
	  });
	//
}

$(function(){
	//
	setTimeout(function(){
		//
		$(".markdown").addClass("reveal")
		//
		$('.codehilite.mermaid').each(function(e){
			//
			c = $(this).parents('pre')[0]//.find('svg')
			//
			try {
				get_screenshot(c)
			}
			catch(error) {
			  
			}
			//
		});
		//
		$('.codehilite.flowchart').each(function(e){
			//
			c = $(this).parents('pre')[0]//.find('svg')
			//
			try {
				get_screenshot(c)
			}
			catch(error) {
			  
			}
			//
		});
		//
	},500)
	//
});