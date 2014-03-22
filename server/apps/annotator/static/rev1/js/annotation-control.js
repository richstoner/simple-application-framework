/** Controller for the attribute controls window. */
function AnnotationStateControl(id) {
	this._init(id === undefined ? 'annotationControls' : id);
}
$.extend(AnnotationStateControl.prototype, {
	_init: function(id) {
		this.id = id;

		var annotationState = DERM.getAnnotationState(),
			$annotationState = $(annotationState);

		var self = this;
		$(function() { self.$el = $('#' + self.id); });

		$annotationState.on('allAnnotationsChanged', $.proxy(this, 'refreshAnnotations'));
		$annotationState.on('annotationAdded', function(evt) {
			self.annotationAdded(evt.annotation, evt.index);
		});
	},

	refreshAnnotations: function() {
		var annotationState = DERM.getAnnotationState(),
			annotations = annotationState.annotations;
		$('#' + this.id).find("tr:gt(0)").remove();
		for( var i = 0; i < annotations.length; ++i )
			this.annotationAdded(annotations[i], i);
	},

	annotationAdded: function(annotation, i) {
		if( typeof(i) === 'undefined' )
			i = this.$el.find('tr:gt(0)').length;
		var html='<tr id="' + i + '_annotationControlRow">';
		html+='<td>'+i+'</td>'; //could be changed to annotationState.annotations[i].data.id
		html+='<td>'+annotation.data.type+'</td>';
		html+='<td>'+annotation.data.label+'</td>';
		html+='<td>'+'<div id="'+i+'_alphaSlider" class="alphaSlider"></div>'+'</td>';
		html+='<td>'+'<input type="text" class="input-small" id="'+i+'_colorTextbox" value="'+annotation.data.color+'"></input></td>';
		html+='<td>'+annotation.data.filled+'</td>';
		html+='<td>'+'<input type="checkbox" id="'+i+'_visibilityCheckbox" checked></div>'+'</td>';
		html+='</tr>';
		this.$el.append(html);

		/*need to add code for the toggle visibility here.... */

		$(function() {
			$( '#'+i+'_alphaSlider' ).slider({
				orientation: "horizontal",
				range: "min",
				max: 100,
				value: Math.round(annotation.data.alpha*100),
				change: function( event, ui ) {
					var roi_index=parseInt(this.id.split('_')[0]);
					var value=ui.value;
					var annotationState = DERM.getAnnotationState();

					annotationState.updateAnnotationData(roi_index, {alpha: value/100.0});
		      }
		  });
		  $( '#'+i+'_visibilityCheckbox' ).change(function(){
				//console.log(this.id);
				var roi_index=parseInt(this.id.split('_')[0]);
				var annotationState = DERM.getAnnotationState();
				if($(this).is(":checked")) {
					toggle_roi_properties( roi_index, 'visibility', false, annotationState) ;
				} else {
					toggle_roi_properties( roi_index, 'visibility', true, annotationState) ;
				}
			});
			$( '#'+i+'_colorTextbox' ).on('keyup',function(){
				var roi_index=parseInt(this.id.split('_')[0]);
				var new_color=this.value;
				if (new_color.length == 7 && new_color.charAt(0) == '#'){
					DERM.getAnnotationState().updateAnnotationData(roi_index, {color: new_color});
				}
			});
		});
	},

	annotationRemoved: function(index) {
		this.$el.find('tr:eq(' + (index+1) + ')').remove();
	},
});

/* toggling visibility in the annotation state object..
to get an individual object... it's annotationState.annotations[index]

within that, the $element propery is what actually populates the div that is rendered... making changes to the visibilt of that will toggle things
 on and off.. but I need to make sure I propogate the event properly
 */

function toggle_roi_properties(roi_index, roi_property, prop_value, annotationState) {
	annotation_obj = annotationState.annotations[roi_index];
	elmt_handle = annotation_obj.$element;

	if (roi_property == 'visibility') {
		prop_value ? $(elmt_handle).hide() : $(elmt_handle).show();
	}
}

//function get_url_for_poi_image(pin_color) {
//	if (pin_color == 'FF0000' || pin_color == 'red') {
//		pin_image_src = "drawing_icons/Pin1_Red.png";
//	} else if (pin_color == '00FF00' || pin_color == 'green') {
//		pin_image_src = "drawing_icons/Pin1_Green.png";
//	} else {
//		pin_image_src = "drawing_icons/Pin1_Blue.png";
//	}
//	return (pin_image_src);
//}

//function annotation_setup_code(annotationState) {
	/* bind changing the color to the color buttons */
//	$('#wsi_paint_color button').click(function() {
//		$('#wsi_paint_color button').addClass('active').not(this).removeClass('active');
//		annotationState.lineColor = colourNameToHex(this.id);
//		$("#cur_color").css('background-color',	colourNameToHex(this.id));
//	});
//
//	$('#wsi_active_shape button').click(function() {
//		$('#wsi_active_shape button').addClass('active').not(this).removeClass('active');
//		annotationState.setDrawMode(this.id);
//	});


/*	  $('#wsi_rater_name  button').click(function() {
                $('#wsi_rater_name button').addClass('active').not(this).removeClass('active');
                //SER USER ID Here
        });
*/

//	var $drawingSwitches = $('.drawing_switch');
//		$drawingSwitches.on('switch-change', function(e, data) {
//		console.debug("switch-change caught by drawing switch element");
//		var $el = $(data.el), value = data.value;
//		console.debug("switch change event is %o %O %O", e, $el, value);
//		// value is true/false
//		value ? annotationState.setIsDrawing(true) : annotationState.setIsDrawing(false);
//	});

//	var $annotationState = $(annotationState);

//	$annotationState.on('isDrawingChanged', function(evt) {
//
//			console.debug("annotation state caught isDrawingChanged event. Updating switch elements");
//
//        var isDrawing = evt.isDrawing;
//		$drawingSwitches.each(function() {
//			$drawingSwitch = $(this);
//			if ($drawingSwitch.bootstrapSwitch('status') !== isDrawing) {
//				$drawingSwitch.bootstrapSwitch('setState', isDrawing);
//			}
//		});
//	});


//	Mousetrap.bind( ['ctrl+d'], function(evt) {
//		if (typeof (evt.preventDefault) === 'function')
//			evt.preventDefault();
//		else
//			evt.returnValue = false;
//		annotationState.setIsDrawing(!annotationState.isDrawing);
//	});
//}

//function set_active_color(color, annotationState) {
//	/*
//	 * this function complements the onclick event and allows the active color
//	 * to be changed programatically the buttons are currently named based on
//	 * their color...
//	 */
//	$('#wsi_paint_color button').removeClass('active'); // remove all active
//														// buttons... although
//														// maybe just setting
//														// the button does it
//	selector_string = "#wsi_paint_color #" + color; // selects the button based
//													// on color...
//	$(selector_string).addClass('active');
//	// $('#wsi_paint_color
//	// button').addClass('active').not(this).removeClass('active');
//	annotationState.lineColor = colourNameToHex(color);
//	$("#cur_color").css('background-color', colourNameToHex(color));
//
//	/* TO DO: ADD RETURN CODE AND CHECK FOR INVALID COLORS */
//}

//function set_active_shape(shape, annotationState) {
//	/*
//	 * this function complements the onclick event and allows the active shape
//	 * to be changed programatically
//	 */
//	$('#wsi_active_shape button').removeClass('active'); // remove all active
//															// buttons...
//															// although maybe
//															// just setting the
//															// button does it
//	selector_string = "#wsi_active_shape #" + shape; // selects the button
//														// based on shape...
//	$(selector_string).addClass('active');
//	annotationState.setDrawMode(shape);
//	/* TO DO: ADD RETURN CODE AND CHECK FOR INVALID COLORS */
//}
