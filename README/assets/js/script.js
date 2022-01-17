mermaid.initialize({
  theme: 'neutral',
  // themeCSS: '.node rect { fill: red; }',
  logLevel: 3,
  flowchart: { curve: 'linear' },
  gantt: { axisFormat: '%m/%d/%Y' },
  sequence: { actorMargin: 50 },
  // sequenceDiagram: { actorMargin: 300 } // deprecated
});
//
var is_multilingual = false;
var lang = ["en"];
var active_lang = 'en'
//
var make_enum = false;
//
var is_enum = '';
if (make_enum) {
	var is_enum = ' enum';
}
//
$(function(){
	//
	if($('[data-render-language]').length){
		active_lang = $('[data-render-language]').attr('data-render-language')
		lang = [active_lang];
		//var active_lang = 'ru'
	}
	//
	function activate_classes(al){
		//
		$(".markdown-body"+' '+'[data-language]').removeClass("active_lang_content")
		$(".markdown-body"+' '+'[data-language]').addClass("hidden")
		$(".markdown-body"+' '+'[data-language="'+al+'"]').addClass("active_lang_content").removeClass("hidden")
		//
		$('body').attr("data-active-lang",al);
		$('[data-language-button]').removeClass("active_lang")
		$('[data-language-button="'+al+'"]').addClass("active_lang")
		//
	}
	//
	function replace_menu_lang(get_active, _lang, _sidebar, target){
		//
		_sidebar.find(target).each(function(){
			//
			is_lang = $(this).attr("data-lang-"+get_active)
			make_lang = $(this).attr("data-lang-"+_lang)
			//
			$(this).find('strong').contents()[0].nodeValue = make_lang//.attr("data-lang-"+lang[x], texts[x][i])
			//
			$('body').attr("data-active-lang",_lang);
			//
		});
		//
	}
	//
	function toggle_lang(_lang, _sidebar){
		//
		get_active = $('[data-active-lang]').attr('data-active-lang');
		make_active = _sidebar.attr("data-lang-"+_lang)
		//
		activate_classes(_lang)
		//
		replace_menu_lang(get_active, _lang,_sidebar,"li")
		replace_menu_lang(get_active, _lang,_sidebar,"h3")
		//
		if (make_enum) {
			//
			add_categ_enum()
			//
		}
		//
	}
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
		get_active = $('[data-active-lang]').attr('data-active-lang');
		//
		chain = '';
		divid = ' / ';
		//
		_parents.each(function(indx){
			//
			t_chain = $(this).attr("data-lang-"+get_active);
			tt_chain = $.trim( $(this).find('strong').eq(0).contents().text() );
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
	function get_candidate(targ, chain, allow_all){
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
		if (lang.length > 0) {
			//select_target = $(".markdown-body"+' '+'[data-language="'+active_lang+'"]')
			select_target = $(".markdown-body"+' '+'.active_lang_content')
		} else {

			select_target = $(".markdown-body")
		}
		//
		//
		select_target.each(function(){
			//
			$(this).find("strong").each(function(){
				//
				if (location_check($(this))) {
					//
					in_t = $.trim($(this).text().toLowerCase());
					//

						if (sanitized_chain == in_t) {
							//
							cand = $(this);
							//
						}
					
					//
				}
				//
			});
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
		$(".codehilite.flowchart").each(function(){
			//
			//
			if ($(this).find('svg').length > 0) {
				//
			}else{
				//
				var diagram = flowchart.parse($(this).text());
				$(this).empty();
				diagram.drawSVG($(this).get(0),{
					'flowstate' : {
						'hide_yesno' : {'yes-text' : ' ', 'no-text' : ' ' }
					}
				});
			}
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
			//
			$(body_elem).each(function(){
				//
				if ( location_check($(this)) ) {
					//
					in_t = $.trim($(this).text());
					//
					is_view = isScrolledIntoView($(this))
					//
					if( is_view ){
						//
						$("#body .selected").removeClass("selected");
						$("#body .current").removeClass("current");
						$(this).addClass("current").addClass("selected");
						//
						window.location.hash = urlize(in_t);
						//
						loc_hash = urlize(in_t)
						get_c = get_candidate(null, urlize(loc_hash,true));
						//
						//
						reveal_sidebar_depth($('.fix_sidebar'), get_c, null, null)
						//
						return false;
						//
					}
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
		//
		return jQuery(a).text().toLowerCase().indexOf(m[3].toLowerCase()) >= 0;
		//
	};
	//
	function reveal_sidebar_depth(fix_sidebar,_c, correlative, is_change){
		//
		var str = _c[1];
		var n = str.split(' / ');
		//
		if (is_change != "change" ) {

			fix_sidebar.find('.selected').removeClass("selected");


		} 
		//
		for (var i = 0; i < n.length; i++) {
			//
			itm = fix_sidebar.find("ol strong:icontains('"+n[i]+"')");
			//
			for (var x = 0; x < itm.length; x++) {
				//
				if (i == n.length - 1) {
					//
					if (n[i-1] != undefined) {

						parent_t = $.trim($($(itm[x]).parent().parents('li').contents().get(0)).text().toLowerCase());
						current = $.trim(n[i-1].toLowerCase());
						//
						if (current == parent_t) {
							//
							if (correlative == null) {
								//
								$(itm[x]).addClass('selected');
								//
							} else {
								//
								return $(itm[x])
								//
							}
							//
							break
							//
						}
						//
					} else {
						//
						if (correlative == null) {
							//
							$(itm[x]).addClass('selected');
							//
						} else {
							//
							return $(itm[x])
							//
						}
						//
					}
					//
				}
			}
			//
			if (correlative == null) {
				//
				if (itm.closest("nav").hasClass('active')) {

				} else {
					//
					itm.closest("nav").click();
					//
				}
			}
			//
		}
		//
	}
	//
	function enum_counter($ol, counters) {
		counters = counters || [];
		$ol.each(function(i) {
			var $this = $(this);
			$this.children("li").each(function(i) {
				var $this = $(this);
				all_c = [];
				all_p = $this.parents('[data-index]');
				//
				if (all_p) {

					for (var x = 0; x < all_p.length; x++) {
						all_c.push( $(all_p[x]).attr('data-index') )
					}
					all_c = all_c.reverse()
					all_c.push([i+1])
				}
				//
				$this.attr('data-index',counters.concat([i+1]));
				$this.attr('data-counter',all_c.join('.'));
				//
				$this.children("ol").each(function(j) {
					enum_counter($(this), counters.concat([i+1]));
				});
			});
		});
	}
	//
	function get_texts_array(text_array, target){
		//
		sidebars[x].find(target).each(function(){
			//
			text_array[x].push($($(this).contents().get(0)).text());
			//
		});
		//
		return text_array
		//
	}
	//
	function set_data_lang(text_array, target){
		//
		i = 0;
		//
		fix_sidebar.find(target).each(function(){
			//
			for (var x = 0; x < lang.length; x++) {
				
				$(this).attr("data-lang-"+lang[x], text_array[x][i]);
			}
			//
			i = i + 1
			//
		});
		//
	}
	//
	function add_categ_enum(){
		//
		fix_sidebar = $('.fix_sidebar');
		//
		enum_counter(fix_sidebar.find("ol"));
		//
		fix_sidebar = $('.fix_sidebar');
		//
		//	
		if (lang.length > 0) {
			//
			active_body = $('.markdown-body .active_lang_content');
			//
		} else {
			//
			active_body = $('.markdown-body');
			//
		}
		//
		this_lang = active_body.attr("data-language");
		//
		is_selected = fix_sidebar.find('.selected').parent();
		//
		if (is_selected) {

			to_activate = active_body.find("h3 strong:icontains('"+is_selected.attr("data-lang-"+this_lang)+"')");
			to_activate.addClass("current selected");
			run_scroll(to_activate);

		}
		//
		active_body.each(function(){
			//
			//
			a_b = $(this)
			//
			$(this).find("h3 strong").each(function(){
				//
				in_t = $.trim($(this).text());
				//
				get_catg = reveal_sidebar_depth(fix_sidebar, [$(this), in_t], this_lang, "change");
				//
				if (get_catg) {
					//
					get_c = get_catg.parent('li').attr('data-counter');
					//
					if ($(this).parent().find(".enum_counter").length == 0) {
						//
						$(this).parent().append('<div class="enum_counter">:'+get_c+'</div>');
						//
					}
					//
				}
				//
			});
			//
		});
		//
	}
	//
	$(".sequence").sequenceDiagram({theme: 'simple'});
	draw_flowcharts();
	check_width();
	//
	$('body').prepend("<aside class='fix_sidebar'><div class='mobile_button'></div></aside>");
	$('body').prepend("<nav class='mobile_menu'></nav>");
	//
	if (make_enum) {
		$('body').addClass('enum')
	}
	//
	var fix_sidebar = $('.fix_sidebar');
	//
	if (is_multilingual) {
		//
		fix_sidebar.append("<div class='lang_controls'></div>")
		//
		for (var i = 0; i < lang.length; i++) {
			
			fix_sidebar.find('.lang_controls').append("<div class='btn lang_btn' data-language-button='"+lang[i]+"'>"+lang[i]+"</div>");
		}
		//
	}
	//
	var scrollTop = $(window).scrollTop();
	//
	fix_sidebar.addClass("show_sidebar");
	//
	sidebars = [];
	//
	for (var i = 0; i < lang.length; i++) {
		//
		sidebars.push($(".markdown-body .sidebar").eq(i))
		//
	}
	//
	if (fix_sidebar.find(".sidebar").length == 0) {
		//
		clone_sidebar = $(".markdown-body .sidebar");
		//
		if (lang.length > 0) {
			//
			clone_sidebar = $(".markdown-body .sidebar").eq(0)
			//
		}
		//
		s_clone = clone_sidebar.clone();
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
		});
		//
		content_texts = [[],[]];
		header_texts = [[],[]];
		//
		for (var x = 0; x < sidebars.length; x++) {
			//
			get_texts_array(content_texts, 'li')
			//
			get_texts_array(header_texts, 'h3')
			//
		}
		//
		set_data_lang(content_texts, 'li')
		set_data_lang(header_texts, 'h3')
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
		if (lang.length > 0) {

			run_scroll($('.markdown-body .active_lang_content .selected'));

		} else {
				
			run_scroll($('.markdown-body .selected'));

		}
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
		get_c = get_candidate($(this),null);
		cand = get_c[0];
		//
		//
		if (cand != null) {
			//
			$(".sidebar .selected").removeClass("selected");
			$(".sidebar .current").removeClass("current");
			$(this).addClass("selected");
			cand.addClass("selected");
			//
			if (cand.length > 0) {
				//
				run_scroll(cand);
				//
			}
			//
			window.location.hash = urlize(get_c[1]);
			//
			$(this).next().addClass('active');
			//
		}
		//
	});
	//
	//
	$('.lang_controls .lang_btn').on('click',function(e){
		//
		toggle_lang($(this).attr("data-language-button"), fix_sidebar);
		//
	});
	//
	setTimeout(function(){
		//
		loc_hash = window.location.hash;
		get_c = get_candidate(null, urlize(loc_hash.substring(1, loc_hash.length),true));
		//
		if (get_c != null) {
			//
			cand = get_c[0];
			//
			run_scroll(cand);
			//
			reveal_sidebar_depth(fix_sidebar, get_c, null, null)
			//
			activate_scroll();
			//
		}
		//
		if ($('[data-render-language]')) {
			//
			active_lang = $('[data-language]').attr('data-language');
			//
		}
		//
		activate_classes(active_lang);
		//
		if (is_multilingual) {
			
		toggle_lang(active_lang, fix_sidebar);
		}
		//
		$(".markdown").addClass("reveal");
		//
	},500);
	//
});