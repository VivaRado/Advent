mermaid.initialize({
  theme: 'neutral',
  // themeCSS: '.node rect { fill: red; }',
  logLevel: 3,
  flowchart: { curve: 'linear' },
  gantt: { axisFormat: '%m/%d/%Y' },
  sequence: { actorMargin: 50 },
  // sequenceDiagram: { actorMargin: 300 } // deprecated
});
$(function(){
	//
	function check_width(){
		//
		if ($(window).width() > 800 ) {
			//
			$('body').removeClass("mobile")
			//
		} else {
			//
			$('body').addClass("mobile")
			//
		}
		//
	}
	function toggle_menu(){
		//
		if ($('body').hasClass("mobile")) {
			//
			if ($('body').hasClass("sidebar_open")) {

				$('body').removeClass("sidebar_open");

			} else {

				$('body').addClass("sidebar_open");
				
			}
			//
		} else {
			return false
		}
	}
	//
	function location_check(_t){
		if ( _t.parents("h6").length > 0 || _t.parents("h5").length > 0 || _t.parents("h4").length > 0 || _t.parents("h3").length > 0 || _t.parents("h2").length > 0) {
			if (_t.parents(".sidebar").length == 0) {
				return true;
			} else {
				return false;
			}
		} else {
			return false;
		}
	}
	//
	function get_chain(targ){
		//
		participant_elements = [];
		//
		_parents = targ.parents("li");
		//
		chain = '';
		divid = ' / ';
		//
		_parents.each(function(indx){
			//
			t_chain = $.trim( $(this).find('strong').eq(0).contents().text() );
			//
			participant_elements.push($(this))
			//
			chain = t_chain + divid  + chain;
			//
		});
		//
		sanitized_chain = chain.slice(0,-divid.length).toLowerCase();
		//
		return [sanitized_chain,participant_elements];
		//
	}
	//
	function get_candidate(targ, chain){
		//
		var cand = null;
		//
		if ( chain ) {
			//
			sanitized_chain = chain.toLowerCase();
			//
		}else{	
			//
			if (targ) {

				sanitized_chain = get_chain(targ)[0];
			} else {
				return null
			}
			//
		}
		//
		$(".markdown-body").find("strong").each(function(){
			//
			if (location_check($(this))) {
				//
				in_t = $.trim($(this).text().toLowerCase());
				//
				if (sanitized_chain == in_t) {
					//
					//
					cand = $(this);
					//
				}
				//
			}
			//
		});
		//
		return [cand, sanitized_chain];
		//
	}
	//
	function run_scroll(_c){
		//
		sc = return_scroll_cont();
		scroll_targ = sc[0];
		add_offset = sc[1];
		//
		if (_c != null) {

			if (_c.length > 0) {			
				//
				scroll_targ.scrollTop(0);
				scroll_targ.scrollTop(_c.offset().top - add_offset);
				//
			}
		}
		//
	}
	//
	function return_scroll_cont() {
		//
		if ($('body').hasClass("mobile")) {
			//
			scroll_targ = $('#body');
			add_offset = 20;
			//
			if ($('body').hasClass("sidebar_open")) {
	
				//toggle_menu();

			}
			//
		} else {
			//
			scroll_targ = $('html,body');
			add_offset = 20;
			//
		}
		//
		return [scroll_targ, add_offset]
		//
	}
	//
	function draw_flowcharts() {
		//
		$(".flowchart").each(function(){
			var diagram = flowchart.parse($(this).text());
			$(this).empty();
			diagram.drawSVG($(this).get(0),{
				'flowstate' : {
					'hide_yesno' : {'yes-text' : ' ', 'no-text' : ' ' }
				}
			});
		});
		//
	}
	//
	function urlize(st, reverse){

		if (reverse) {

			str = st.replace(/\//g, ' / ');
			str_b = str.replace(/-/g, ' ');

		} else {
			str = st.replace(/ \/ /g, '/');
			str_b = str.replace(/ /g, '-');
			
		}
		return str_b.toLowerCase();
	}
	//
	function isScrolledIntoView(elem){
		var docViewTop = $(window).scrollTop();
		var docViewBottom = docViewTop + $(window).height();

		var elemTop = $(elem).offset().top;
		var elemBottom = elemTop + $(elem).height();

		return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
	}
	//
	function scroll_function(){
		//
		if( $(body_elem).offset().top == null){
			return false;
		}else {	
			//var num = 0;
			$(body_elem).each(function(){
				//
				if ( location_check($(this)) ) {
					//
					in_t = $.trim($(this).text());
					//
					is_view = isScrolledIntoView($(this))
					//
					if( is_view){
						//
						$("#body .selected").removeClass("selected");
						$("#body .current").removeClass("current");
						$(this).addClass("current").addClass("selected");
						//
						window.location.hash = urlize(in_t);
						//
						loc_hash = urlize(in_t)
						get_c = get_candidate(null, urlize(loc_hash,true));
						reveal_sidebar_depth($('.fix_sidebar'), get_c)
						//
						return false;
						//
					}
					//
					//
				}
				//
			});
			//
		}
		
	}
	//
	function activate_scroll(){

		$(window).scroll(function(){
			//
			if ($('body').hasClass("mobile")) {
				return false;
			} else {
				//
				scroll_function();
				//
			}
			//
		});
		//
		$('#body').scroll(function(){
			//
			if ($('body').hasClass("mobile")) {
				//
				scroll_function()
				//
			} else {
				return false;
				
			}
			//
		});
	}
	//
	jQuery.expr[':'].icontains = function(a, i, m) {
	  return jQuery(a).text().toLowerCase()
	      .indexOf(m[3].toLowerCase()) >= 0;
	};
	//
	function reveal_sidebar_depth(fix_sidebar,_c){
		//
		var str = _c[1];
		var n = str.split(' / ')
		//
		for (var i = 0; i < n.length; i++) {
			//
			itm = fix_sidebar.find("ol strong:icontains('"+n[i]+"')").eq(0);
			//
			if (i == n.length - 1) {
				//
				fix_sidebar.find('.selected').removeClass("selected")
				itm.addClass('selected')
				//
			}
			//
			if (itm.closest("nav").hasClass('active')) {

			} else {
				//
				itm.closest("nav").click();
				//
			}
			//
		}
		//
	}
	//
	//
	//
	//
	//
	$(".sequence").sequenceDiagram({theme: 'simple'});
	draw_flowcharts();
	check_width();
	
	//
	$('body').prepend("<aside class='fix_sidebar'><div class='mobile_button'></div></aside>");
	$('body').prepend("<nav class='mobile_menu'></nav>");
	//
	var fix_sidebar = $('.fix_sidebar');
	//
	var sidebar = $(".markdown-body .sidebar");
	var scrollTop = $(window).scrollTop();
	var sidebarEdge = parseInt(sidebar.offset().top + sidebar.height());
	//
	sidebar.addClass("hide_sidebar");
	fix_sidebar.addClass("show_sidebar");
	//
	if (fix_sidebar.find(".sidebar").length == 0) {
		//
		s_clone = sidebar.clone();
		s_clone.appendTo('.fix_sidebar');
		//
		fix_sidebar.find("ol").each(function(){
			//
			if ($(this).parents("ol").length >= 1) {
				//
				$(this).wrap("<nav class='toggle'></nav>")
				//
			}
			//
		})
		//
	}
	//
	var _s = 200;
	var elem = '.markdown-body';
	var body_elem = '.markdown-body strong';
	var sidebarLink = '.sidebar strong';
	//
	/* Nested List Toggle */
	$('nav.toggle li').on('click',function(e){
		e.stopPropagation();
	});
	//
	$('nav.toggle').on('click',function(e){
		//
		e.stopPropagation();
		//
		$(this).children().toggle();
		$(this).toggleClass('active');
		//
	});
	//
	$(window).on("resize", function(){
		//
		check_width();
		//
		run_scroll($('.markdown-body .selected'))
		//
	});
	//
	fix_sidebar.find(".mobile_button").on('click',function(e){
		//
		toggle_menu();
		//
	});
	//
	fix_sidebar.find("li strong").on('click',function(e){
		//
		e.stopPropagation();
		get_c = get_candidate($(this));
		cand = get_c[0];
		//
		if (cand != null) {
			
		$(".sidebar .selected").removeClass("selected");
		$(".sidebar .current").removeClass("current");
		$(this).addClass("selected");
		cand.addClass("selected");
		//
		if (cand.length > 0) {
			//
			run_scroll(cand)
			//
		}
		//
		window.location.hash = urlize(get_c[1]);
		//
		$(this).next().addClass('active')//.find('ul').addClass('active');
		}
		//
	});
	//
	
	//
	
	//
	setTimeout(function(){
		loc_hash = window.location.hash 
		get_c = get_candidate(null, urlize(loc_hash.substring(1, loc_hash.length),true));
		if (get_c != null) {
		cand = get_c[0];

		run_scroll(cand);
		//
		reveal_sidebar_depth(fix_sidebar, get_c)
		//
		activate_scroll();
		//
		}
		$(".markdown").addClass("reveal")
		//
	},500)
	//
});