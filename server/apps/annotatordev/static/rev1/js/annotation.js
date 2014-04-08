
OpenSeadragon.Utils = OpenSeadragon;

var KEEP_LOGS = true;
var AnnotationTypes = {};
var OverlayTypes = {};


// putting the utilities in the main file
var colorNameToHex = function(colour)
{
    var colours = {"aliceblue":"#f0f8ff","antiquewhite":"#faebd7","aqua":"#00ffff","aquamarine":"#7fffd4","azure":"#f0ffff",
    "beige":"#f5f5dc","bisque":"#ffe4c4","black":"#000000","blanchedalmond":"#ffebcd","blue":"#0000ff","blueviolet":"#8a2be2","brown":"#a52a2a","burlywood":"#deb887",
    "cadetblue":"#5f9ea0","chartreuse":"#7fff00","chocolate":"#d2691e","coral":"#ff7f50","cornflowerblue":"#6495ed","cornsilk":"#fff8dc","crimson":"#dc143c","cyan":"#00ffff",
    "darkblue":"#00008b","darkcyan":"#008b8b","darkgoldenrod":"#b8860b","darkgray":"#a9a9a9","darkgreen":"#006400","darkkhaki":"#bdb76b","darkmagenta":"#8b008b","darkolivegreen":"#556b2f",
    "darkorange":"#ff8c00","darkorchid":"#9932cc","darkred":"#8b0000","darksalmon":"#e9967a","darkseagreen":"#8fbc8f","darkslateblue":"#483d8b","darkslategray":"#2f4f4f","darkturquoise":"#00ced1",
    "darkviolet":"#9400d3","deeppink":"#ff1493","deepskyblue":"#00bfff","dimgray":"#696969","dodgerblue":"#1e90ff",
    "firebrick":"#b22222","floralwhite":"#fffaf0","forestgreen":"#228b22","fuchsia":"#ff00ff",
    "gainsboro":"#dcdcdc","ghostwhite":"#f8f8ff","gold":"#ffd700","goldenrod":"#daa520","gray":"#808080","green":"#008000","greenyellow":"#adff2f",
    "honeydew":"#f0fff0","hotpink":"#ff69b4",
    "indianred ":"#cd5c5c","indigo ":"#4b0082","ivory":"#fffff0","khaki":"#f0e68c",
    "lavender":"#e6e6fa","lavenderblush":"#fff0f5","lawngreen":"#7cfc00","lemonchiffon":"#fffacd","lightblue":"#add8e6","lightcoral":"#f08080","lightcyan":"#e0ffff","lightgoldenrodyellow":"#fafad2",
    "lightgrey":"#d3d3d3","lightgreen":"#90ee90","lightpink":"#ffb6c1","lightsalmon":"#ffa07a","lightseagreen":"#20b2aa","lightskyblue":"#87cefa","lightslategray":"#778899","lightsteelblue":"#b0c4de",
    "lightyellow":"#ffffe0","lime":"#00ff00","limegreen":"#32cd32","linen":"#faf0e6",
    "magenta":"#ff00ff","maroon":"#800000","mediumaquamarine":"#66cdaa","mediumblue":"#0000cd","mediumorchid":"#ba55d3","mediumpurple":"#9370d8","mediumseagreen":"#3cb371","mediumslateblue":"#7b68ee",
    "mediumspringgreen":"#00fa9a","mediumturquoise":"#48d1cc","mediumvioletred":"#c71585","midnightblue":"#191970","mintcream":"#f5fffa","mistyrose":"#ffe4e1","moccasin":"#ffe4b5",
    "navajowhite":"#ffdead","navy":"#000080",
    "oldlace":"#fdf5e6","olive":"#808000","olivedrab":"#6b8e23","orange":"#ffa500","orangered":"#ff4500","orchid":"#da70d6",
    "palegoldenrod":"#eee8aa","palegreen":"#98fb98","paleturquoise":"#afeeee","palevioletred":"#d87093","papayawhip":"#ffefd5","peachpuff":"#ffdab9","peru":"#cd853f","pink":"#ffc0cb","plum":"#dda0dd","powderblue":"#b0e0e6","purple":"#800080",
    "red":"#ff0000","rosybrown":"#bc8f8f","royalblue":"#4169e1",
    "saddlebrown":"#8b4513","salmon":"#fa8072","sandybrown":"#f4a460","seagreen":"#2e8b57","seashell":"#fff5ee","sienna":"#a0522d","silver":"#c0c0c0","skyblue":"#87ceeb","slateblue":"#6a5acd","slategray":"#708090","snow":"#fffafa","springgreen":"#00ff7f","steelblue":"#4682b4",
    "tan":"#d2b48c","teal":"#008080","thistle":"#d8bfd8","tomato":"#ff6347","turquoise":"#40e0d0",
    "violet":"#ee82ee",
    "wheat":"#f5deb3","white":"#ffffff","whitesmoke":"#f5f5f5",
    "yellow":"#ffff00","yellowgreen":"#9acd32"};

    if (typeof colours[colour.toLowerCase()] != 'undefined')
    	return colours[colour.toLowerCase()];

    return false;
}


if( typeof _log !== 'function' ) {
	_log = function() {
		if( !KEEP_LOGS ) return;
		try { console.log(arguments); } catch(err) {}
	}
}

function get_url_for_poi_image(pin_color) {
	if (pin_color == 'FF0000' || pin_color == 'red') {
		pin_image_src = "static/images/drawing_icons/Pin1_Red.png";
	} else if (pin_color == '00FF00' || pin_color == 'green') {
		pin_image_src = "static/images/drawing_icons/Pin1_Green.png";
	} else {
		pin_image_src = "static/images/drawing_icons/Pin1_Blue.png";
	}
	return (pin_image_src);
}






var AnnotationData = function(options) { this._init(options || {}); }

/** Instantiate a copy from storage data. */
AnnotationData.fromValueObject = function(obj) {
	var result;
	if( AnnotationTypes.hasOwnProperty(obj.type) )
		result = new AnnotationTypes[obj.type](obj);
	else
		result = new AnnotationData(obj);
	return result;
};


//TODO: To support setting properties on annotations when they are pushed e.g. zoom_level
// 1. Add the keys for the properties to the OPTIONS so they are white-listed for serialization
// 2. Create a common properties field that is an array of properties to add to each annotation data
// 3. Provide a public getter and setter for the property so users of the annotation state can specify the common properties for the next annotation
$.extend(AnnotationData.prototype, {
	OPTIONS: {
		id: null,
		type: 'unknown',

		label: null,
		points: null,

		color: '#FF00FF',
		alpha: 1,
		filled: false,
		closed: false,
		zoom_level: null,

		markup_for: null,

// 		markup_image_name: null,
// 		markup_image_md5: null,
		server_id: null,
		annotation_timestamp: null,
		annotation_revision_id: null,
		ontology_or_termset_id: null,
		browser_info: null,
		markup_text: null,
		addl_notes: null
	},

	/** If positive, limit the number of points to maxPoints. */
	maxPoints: -1,

	_init: function(options) {
		var opts = $.extend({}, this.OPTIONS, options);
		for( var opt in this.OPTIONS )
			this[opt] = opts[opt];
		if( this.points == null ) this.points = [];

		this.bounds = null;
	},

	/**
	 * Return the bounds, computing if necessary or request by <code>recompute</code>.
	 * @param {boolean} recompute to force bounds to be recomputed
	 * @return {null} the bounds ({x,y,width,height}) or <code>null</code> if no points
	 */
	getBounds: function(recompute) {
		if( this.points.length < 1 ) return null;
		if( this.bounds == null || recompute ) {
			var start = this.points[0], top, bottom, left, right;
			top = bottom = start.y;
			left = right = start.x;
			for( var i = 1; i < this.points.length; ++i ) {
				var p = this.points[i];
				if( p.y < top )    top = p.y;
				if( p.y > bottom ) bottom = p.y;
				if( p.x < left )   left = p.x;
				if( p.x > right )  right = p.x;
			}
			this.bounds = {x: left, y: top, width: right - left, height: bottom - top};
		}
		return this.bounds;
	},

	/** Add a point and invalidate the bounds. */
	addPoint: function(point) {
		if( this.maxPoints > 0 && this.points.length >= this.maxPoints )
			throw new Error('Points already at max: ' + this.maxPoints);
		this.points.push(point);
		this.bounds = null;
	},

	/** Remove a point and invalidate the bounds. */
	removePoint: function(index) {
		if( typeof index !== 'number' ) throw new Error('index is not a number');
		if( index < 0 || index >= this.points.length ) throw new Error('index out of range: ' + index);
		this.points.splice(index, 1);
		this.bounds = null;
	},

	/** Replace an existing point and invalidate the bounds if changed. */
	replacePoint: function(index, point) {
		if( typeof index !== 'number' ) throw new Error('index is not a number');
		if( index < 0 || index > this.points.length ) throw new Error('index out of range: ' + index);
		if( index === this.points.length ) {
			this.addPoint(point);
			return null;
		}
		var old = this.points[index];
		this.points[index] = point;
		if( old.x !== point.x || old.y !== point.y )
			this.bounds = null;
		return old;
	},

	/** Return a copy of this data with only the values for storage. */
	asValueObject: function() {
		var obj = {};
		for( var opt in this.OPTIONS )
			obj[opt] = this[opt];
		return obj;
	}
});

/** Point of Interest data. */
function PointOfInterestData(options) {
	options = options || {};
	options.type = 'poi';
	this._init(options);
}

$.extend(PointOfInterestData.prototype, AnnotationData.prototype, {
	OPTIONS: $.extend({}, AnnotationData.prototype.OPTIONS, {
		imgsrc: null,
		rectsize: 0.025
	}),

	maxPoints: 1,

	/**
	 * Return the bounds, computing if necessary or request by <code>recompute</code>.
	 * @param {boolean} recompute to force bounds to be recomputed
	 * @return {null} the bounds ({x,y,width,height}) or <code>null</code> if no points
	 */
	getBounds: function(recompute) {
		if( this.points.length < 1 ) return null;
		if( this.bounds == null || recompute ) {
			var p = this.points[0], size = this.rectsize;
			this.bounds = {x: p.x - size, y: p.y - size, width: size, height: size};
		}
		return this.bounds;
	}
});


/** A rectangle. */
function RectangleData(options) {
	options = options || {};
	options.type = 'rect';
	this._init(options);
}
$.extend(RectangleData.prototype, AnnotationData.prototype, {
	maxPoints: 2
});


/** A circle / oval. */
var CircleData = function(options) {
	options = options || {};
	options.type = 'circle';
	this._init(options);
}
$.extend(CircleData.prototype, AnnotationData.prototype, {
	maxPoints: 2
});

/** Polygons and freehand drawing data. */
var PolygonData = function(options) {
	options = options || {};
	if( options.type !== 'polygon' && options.type !== 'freehand' )
		options.type = 'polygon';
	this._init(options);
}
$.extend(PolygonData.prototype, AnnotationData.prototype);



AnnotationTypes['poi'] = PointOfInterestData;
AnnotationTypes['polygon'] = PolygonData;
AnnotationTypes['freehand'] = PolygonData;
AnnotationTypes['rect'] = RectangleData;
AnnotationTypes['circle'] = CircleData;


/** Annotation overlay renderer. */
function AnnotationOverlay(options) { this._init(options || {}); }
AnnotationOverlay.fromValueObject = function(obj) {
	var result;
	if( OverlayTypes.hasOwnProperty(obj.type) )
		result = new OverlayTypes[obj.type]({data: obj});
	else
		result = new AnnotationData({data: obj});
	return result;
};
$.extend(AnnotationOverlay.prototype, {
	EMPTY_RECT: new OpenSeadragon.Rect(0,0,0,0),

	_init: function(options) {
		if( options.data )
			this.data = AnnotationData.fromValueObject(options.data);
		else
			this.data = AnnotationData.fromValueObject(options);

		this.viewer = null;
		this.element = null;
		this.labelelement = null;
		if( options.viewer ) this.attachTo(options.viewer);
	},

	/** Implement shape specific drawing. */
	draw: $.noop,

	/** Called by detach() for extra cleanup. */
	cleanup: $.noop,

	/** Creates the drawing element, which is a div by default. */
	createElement: function() {
		return document.createElement('div');
	},

	/** Creates the label display element. */
	createLabelElement: function() {
		var el = document.createElement('div');
		// TODO: use negative 'top' or 'left' values to place outside of element container
		$(el).css({
			'position': 'absolute',
			'overflow': 'visible',
			'top': '0px',
			'left': '0px'
		});
		return el;
	},

	attachTo: function(viewer) {
		this.viewer = viewer;
		this.element = this.createElement();
		this.labelelement = this.createLabelElement();
		$(this.labelelement).text(this.data.label).appendTo(this.element);
		viewer.drawer.addOverlay(this.element, this.EMPTY_RECT);
		this.redraw();
	},

	detach: function() {
		if( !this.viewer ) return;
		this.viewer.drawer.removeOverlay(this.element);
		this.viewer = this.element = this.labelelement = null;
		this.cleanup();
	},

	updateBounds: function() {
		var bounds, rect;
		if( !this.viewer ) return;
		bounds = this.data.getBounds();
		if( bounds == null ) {
			rect = this.EMPTY_RECT;
		} else {
			rect = new OpenSeadragon.Rect(
				bounds.x, bounds.y, bounds.width, bounds.height);
		}
		this.viewer.drawer.updateOverlay(this.element, rect);
	},

	redraw: function() {
		if( this.viewer ) {
			this.updateBounds();
			this.labelelement.innerText = this.data.label || '';
			this.draw();
		}
	}
});

function POIOverlay(options) {
	options = options || {};
	options.type = 'poi';
	if( typeof(options.data) === 'object' )
		options.data.type = 'poi';
	this._init(options);
};


$.extend(POIOverlay.prototype, AnnotationOverlay.prototype, {
	_superinit: AnnotationOverlay.prototype._init,
	_superCreateElement: AnnotationOverlay.prototype.createElement,

	_init: function(options) {
		this._superinit(options);
	},

	createElement: function() {
		var el = this._superCreateElement();

		this.img = document.createElement('img');
		var $img = $(this.img);
		if( this.data.imgsrc )
			$img.attr('src', this.data.imgsrc);
		$img.css({width: '100%', height: '100%'});
		$img.appendTo(el);

		return el;
	},

	cleanup: function() {
		this.img = null;
	}
});

/** Mixin for overlays using a <DIV> and CSS. */
var DivOverlayMixin = {
	/** Implement for initial CSS settings on the DIV. */
	applyStaticCSS: $.noop,

	/** For dynamic attributes, defaults implemented. */
	applyDynamicCSS: function() {
		var d = this.data;
		this.$element.css({
			'border-color': d.color,
			'opacity': d.alpha,
			'filter': 'alpha(opacity=' + (d.alpha*100) + ')',
			'background': (d.filled ? d.color : '')
		});
		this.labelelement.innerText = d.label || '';
	},

	/** Creates the DIV and applies the static CSS to it. */
	createElement: function() {
		var e = document.createElement('div');
		this.$element = $(e);
		this.applyStaticCSS();
		return e;
	},

	cleanup: function() {
		this.$element = null;
	},

	draw: function() {
		if( !this.viewer ) return;
		this.applyDynamicCSS();
	}
};

/** An overlay for a rectangle annotation. */
function RectangleOverlay(options) {
	options = options || {};
	options.type = 'rect';
	if( typeof(options.data) === 'object' )
		options.data.type = 'rect';
	this._init(options || {});
}
$.extend(RectangleOverlay.prototype,
			AnnotationOverlay.prototype,
			DivOverlayMixin, {
	/** Sets the border to show the rectangle. */
	applyStaticCSS: function() {
		this.$element.css({
			'position': 'relative',
			'border-width': '2px',
			'border-style': 'solid'
		});
	}
});

/** An overlay for a circle annotation. */
function CircleOverlay(options) {
	options = options || {};
	options.type = 'circle';
	if( typeof(options.data) === 'object' )
		options.data.type = 'circle';
	this._init(options);
};
OverlayTypes['circle'] = CircleOverlay;
$.extend(CircleOverlay.prototype,
			AnnotationOverlay.prototype,
			DivOverlayMixin, {
	/** Sets the border and makes it circular. */
	applyStaticCSS: function() {
		this.$element.css({
			'position': 'relative',
			'border-width':  '2px',
			'border-style':  'solid',
			'border-radius': '50%'
		});
	}
});


/**
 * Creates a polygon or freehand annotation.
 *
 * @param {object} the options, which may be:<br /><ul>
 *   <li>points - an initial array of points</li>
 *   <li>color - a color string of the form #HHHHHH</li>
 *   <li>alpha - a number [0,1] indicating the alpha level</li>
 *   <li>filled - if the shape should be filled</li>
 *   <li>closed - if the shape should be closed</li>
 *   <li>viewer - the OpenSeadragon viewer to attach to, if not given call attachTo(viewer) later</li>
 * </ul>
 */
function PolygonOverlay(options) {
	options = options || {};
	var type = options.type;
	if( type !== 'polygon' && type !== 'freehand' )
		options.type = 'polygon';
	if( typeof(options.data) === 'object' )
		options.data.type = options.type;
	this._init(options);
};

$.extend(PolygonOverlay.prototype, AnnotationOverlay.prototype, {
	_superinit: AnnotationOverlay.prototype._init,
	_superCreateElement: AnnotationOverlay.prototype.createElement,

	_init: function(options) {
		this._superinit(options);

		this._lastBounds = null;
		this._lastCanvasSize = null;
		this._canvasPoints = null;
	},

	createElement: function() {
      this.canvas = document.createElement('canvas');
      this.$canvas = $(this.canvas).css({'height': '100%', 'width': '100%'});
		var element = this._superCreateElement();
      this.$canvas.appendTo(element);
		return element;
	},

	addPoint: function(point) {
		this.data.addPoint(point);
		this.clearCaches();
		this.redraw();
	},

	clearCaches: function() {
		this._lastBounds = null;
		this._lastCanvasSize = null;
		this._canvasPoints = null;
	},

	/**
	 * Returns whether the bounds are different from the cached version.
	 * If not given, uses the data bounds.
	 */
	areBoundsChanged: function(bounds) {
		var last = this._lastBounds, current = bounds;
		if( current === undefined ) current = this.data.getBounds();

		if( last == null && current != null ) return true;
		if( last != null && current == null ) return true;
		if( last.x !== current.x || last.y !== current.y ||
				last.width !== current.width || last.height !== current.height ) {
			return true;
		}

		return false;
	},

	/** Same as areBoundsChanged but caches the bounds if changed. */
	cacheBounds: function(bounds) {
		if( bounds === undefined ) bounds = this.data.getBounds();
		if( this.areBoundsChanged(bounds) ) {
			this._lastBounds = bounds;
			return true;
		}
		return false;
	},

	/**
	 * Returns whether the canvas size is different from the cached version.
	 * If not given, uses the element dimensions.
	 */
	isCanvasResized: function(width, height) {
		var last = this._lastCanvasSize;
		if( width == null ) {
			width = this.element.width;
			height = this.element.height;
		}
		if( last == null ) return true;
		if( last.width !== width || last.height !== height ) return true;

		return false;
	},

	/** Same as isCanvasResized but caches the size if changed. */
	cacheCanvasSize: function(width, height) {
		if( this.isCanvasResized(width, height) ) {
			this._lastCanvasSize = {width: width, height: height};
			return true;
		}
		return false;
	},

	draw: function() {
		if( !this.viewer ) return;

		var el = this.canvas, cwidth = el.width, cheight = el.height,
			ctx = this.canvas.getContext('2d'), data = this.data;

		if( cwidth === undefined || cheight === undefined ) {
			_log('PolygonAnnotation.draw, canvas width/height undefined:', cwidth, cheight);
			return;
		}

		// always clear
		ctx.clearRect(0, 0, cwidth, cheight);
		if( data.points.length < 2 )
			return;

		var cpoints = this.getCanvasPoints(), first = cpoints[0];

		ctx.beginPath();
		ctx.strokeStyle = data.color;
		ctx.globalAlpha = data.alpha;

		// draw the path
		ctx.moveTo(first.x, first.y);
		for( var i = 1, len = cpoints.length; i < len; ++i ) {
			var p = cpoints[i];
			ctx.lineTo(p.x, p.y);
		}

		if( data.closed ) ctx.closePath();

		ctx.stroke();

		if( data.filled ) {
			ctx.fillStyle = data.color;
			ctx.fill();
		}
	},

	/** Gets the overlay points relative to the canvas. */
	getCanvasPoints: function() {
		var bounds = this.data.getBounds(),
			cwidth = this.canvas.width,
			cheight = this.canvas.height,
			cpoints = this._canvasPoints,
			cached;

		if( cwidth === undefined || cheight === undefined ) {
			_log('PolygonAnnotation.getCanvasPoints, canvas width or height undefined.', cwidth, cheight);
			return null;
		}

		// see if we can reuse the earlier points
		cached = this.cacheBounds(bounds);
		cached = this.cacheCanvasSize(cwidth, cheight) && cached;
		cached = cached && cpoints != null;
		if( cached ) return cpoints;

		// translate based on current bounds and canvas size
		var xorigin = bounds.x,     yorigin = bounds.y,
		      width = bounds.width,  height = bounds.height,
			points = this.data.points,        len = points.length,
			i = 0, x, y, p, Point = OpenSeadragon.Point;

		cpoints = Array(len);
		for(; i < len; ++i) {
			p = points[i];
			x = ((p.x - xorigin) / width)  * cwidth;
			y = ((p.y - yorigin) / height) * cheight;
			cpoints[i] = new Point(x, y);
		}

		// cache and return
		this._canvasPoints = cpoints;
		return cpoints;
	},

	cleanup: function() {
		this.clearCaches();
	}
});


OverlayTypes['poi'] = POIOverlay;
OverlayTypes['rect'] = RectangleOverlay;
OverlayTypes['polygon'] = PolygonOverlay;
OverlayTypes['freehand'] = PolygonOverlay;



// BEGIN Annotation state controller
var AnnotationState = function(viewer) {

    _log("created AnnotationState");

	this.drawMode = 'poi';
	this.lineColor = colorNameToHex('yellow');

	this.viewer = null;
	this.markupFor = null;

    this.isDrawing = false;
	this.annotations = [];

	if( viewer ) this.setSeadragonViewer(viewer);
}

$.extend(AnnotationState.prototype, {

	setDrawMode: function(mode) {
		var oldMode = this.drawMode;

		// cancel the current annotation if switching modes
		if( mode !== oldMode )
			this.cancelAnnotation();
		this.drawMode = mode;
		if( mode !== oldMode ) {
			$(this).trigger({
				type: 'drawModeChanged',
				oldMode: oldMode,
				newMode: mode
			});
		}
        console.log("Draw mode set to " + mode);
	},

	selectForegroundColor: function(color) {
		if( color )
			this.colorPicker.setColor(color);
		else
			this.colorPicker.setColor(this.lineColor);
		this.colorPicker.show();
	},

	setForegroundColor: function(color) {
		this.lineColor = color;
		// FIXME
		$('#line_color').val(color);
		this.$colorInput.css('background-color', color);
	},

	setSeadragonViewer: function(viewer) {
		if( this.viewer ) {

			_log('Warning: setSeadragonViewer already allocated.', this.viewer, viewer, this);

		}

		this.viewer = viewer;

		OpenSeadragon.Utils.addEvent(viewer.element, 'click', $.proxy(this._viewerClicked, this));

		// set up listeners for freehand drawing
		var self = this;
		var $el = this.$el = $(viewer.element);

		$el.on('mousedown', function(evt) {
			var loc, onMouseMove;
			if( 'freehand' === self.drawMode && self.isDrawing ) {
				loc = self._getEventLocation(evt);
				self._startFreehand(loc.point);
				onMouseMove = function(event) {
					var loc = self._getEventLocation(event);
					self._overlay.addPoint(loc.point);
				};

				$el.one('mouseup', function(event) {

					// FIXME this is not preventing the click event for some reason
					event.preventDefault();
					event.stopImmediatePropagation();

					// stop listening to movement and turn off drawing
					$el.off('mousemove', onMouseMove);
					self.annotations.push(self._overlay);
					self._overlay = null;
					self.setIsDrawing(false, true);
				});
				$el.on('mousemove', onMouseMove);
			}
		});
	},

	setIsDrawing: function(drawing, setItemState) {

		var oldVal = this.isDrawing;

        this.isDrawing = drawing;

		this.viewer.setMouseNavEnabled(!this.isDrawing);

		if( !drawing ) {
			// TODO finalize freehand / polygon
			if( this.drawMode !== 'polygon' && this._overlay != null ){
				this.cancelAnnotation();
			}
			if( this._overlay != null ){
				/* adding a sticky option... will be a global variable?? that determines if drawing mode stays on or off i.e. addm ultiple shapes without clicking redraw */
				this.pushAnnotation(this._overlay);
				this._overlay = null;
				console.debug('added annotation from overlay??');
			}
		}
		if( setItemState )
			this.toolbar.setItemState('start_draw', drawing);

		if( oldVal !== this.isDrawing ) {
			$(this).trigger({
				type: 'isDrawingChanged',
				isDrawing: this.isDrawing
			});
		}
	},

	/**
	 * Gets the pixel and point location from a click event.
	 * @return {object} with 'pixel' and 'point' attributes
	 */
	_getEventLocation: function(event) {
		var u = OpenSeadragon.Utils,
			pixel = u.getMousePosition(event).minus(u.getElementPosition(this.viewer.element)),
			point = this.viewer.viewport.pointFromPixel(pixel);
		return {pixel: pixel, point: point};
	},

	_viewerClicked: function(event) {
		var location = this._getEventLocation(event),
			pixel = location.pixel,
			point = location.point;
		_log('_viewerClicked', pixel, point, event, this);
		if( this.isDrawing ) {
			var isNewOverlay = this._overlay == null;

			if( 'poi' === this.drawMode ) {
				this._drawPOI(point);
			} else if( 'polygon' === this.drawMode ) {
				if( isNewOverlay )
					this._startPolygon(point);
				else
					this._overlay.addPoint(point);
			} else if( 'rect' == this.drawMode ) {
				if( isNewOverlay ) {
					this._startRectangle(point);
				} else {
					this._overlay.data.replacePoint(1, point);
					this._overlay.redraw();
					this.pushAnnotation(this._overlay);

					this._overlay = null; // FIXME save these
				}
			} else if( 'circle' === this.drawMode ) {
				if( isNewOverlay ) {
					this._startCircle(point);
				} else {
					this._overlay.data.replacePoint(1, point);
					this._overlay.redraw();
					this.pushAnnotation(this._overlay);

					this._overlay = null; // FIXME save these
				}
			}
		}
	},

	/**
	 * Returns the annotation properties for use in constructing a new overlay.
	 *
	 * @param point the initial point for the overlay
	 * @param props optional non-default properties to merge in
	 */
	_getAnnotationProperties: function(point, props) {
		var defaults = {
			viewer: this.viewer,
			data: {
				label: String(this.annotations.length + 1),
				color: this.lineColor,
				points: [point],
				annotation_timestamp: new Date().getTime(),
				markup_for: this.markupFor,
				// add any other common properties here
			}
		};
		if( typeof props !== 'undefined' )
			defaults = $.extend(true, defaults, props);
		return defaults;
	},

	_startRectangle: function(point) {
		this._overlay = new RectangleOverlay(this._getAnnotationProperties(point));
		var self = this, $el = this.$el = $(this.viewer.element);
		var onMouseMove = function(event) {
			var location = self._getEventLocation(event);
			self._overlay.data.replacePoint(1, location.point);
			self._overlay.redraw();
		};
		$el.one('mouseup', function() { $el.off('mousemove', onMouseMove); });
		$el.on('mousemove', onMouseMove);
	},

	_startCircle: function(point) {
		this._overlay = new CircleOverlay(this._getAnnotationProperties(point));
		var self = this, $el = this.$el = $(this.viewer.element);
		var onMouseMove = function(event) {
			var location = self._getEventLocation(event);
			self._overlay.data.replacePoint(1, location.point);
			self._overlay.redraw();
		};
		$el.one('mouseup', function() { $el.off('mousemove', onMouseMove); });
		$el.on('mousemove', onMouseMove);
	},

	/** Starts a freehand annotation at the given point. */
	_startFreehand: function(point) {
		this._overlay = new PolygonOverlay(this._getAnnotationProperties(point, {
			type: 'freehand'
		}));
	},

	/** Starts a polygon annotation at the given point. */
	_startPolygon: function(point) {
		this._overlay = new PolygonOverlay(this._getAnnotationProperties(point, {
			type: 'polygon',
			data: {
				filled: true,
				closed: true,
				alpha: 0.3
			}
		}));
	},

	/**
	 * Draws a POI (Point of Interest) based on the current
	 * point.
	 */
	_drawPOI: function(point) {
		var lineColor = this.lineColor || '#FFFF00',
			pinImg = get_url_for_poi_image(lineColor.substring(1));

		var overlay = new POIOverlay(this._getAnnotationProperties(point, {
			type: 'poi',
			data: {
				imgsrc: pinImg
			}
		}));
		this.pushAnnotation(overlay);
	},


	/** Cancel and remove the current annotation. */
	cancelAnnotation: function() {
		if( this._overlay != null ) {
			this._overlay.detach();
			this._overlay = null;
		}
	},

	/**
	 * Set and initialize the dhtmlx.Toolbar instance.
	 * Should only be called once.
	 */
	setupToolbar: function(toolbar) {
		var self = this;
		if( this.toolbar ) {
			_log('Warning: setupToolbar already called.', this.toolbar, toolbar, this);
		}
		this.toolbar = toolbar;
		toolbar.attachEvent('onClick', $.proxy(this._toolbarClicked, this));
		toolbar.attachEvent('onStateChange', $.proxy(this._stateChanged, this));

		// this.toolbar.disableItem('foreground_color_input');
		this.$colorInput = $(toolbar.cont).find('input.inp').first();
		this.$colorInput.on('click keypress', function(event){
			event.preventDefault();
			if( event.type === 'click' || (event.type === 'keypress' && event.which == 13) )
				self.selectForegroundColor();
		});

		this.colorPicker = new dhtmlXColorPicker(null, null, true, true);
		this.colorPicker.setSkin('');
		this.colorPicker.setOnSelectHandler($.proxy(this.setForegroundColor, this));
		this.colorPicker.init();

		this.setForegroundColor(this.lineColor);
	},

	_toolbarClicked: function(id) {
		_log('_toolbarClicked', id, this);
		// FIXME handle this ourselves, forward for now
		setup_wsi_toolbar(id);

		var isDrawMode = id.substring(0, "drawmode_".length) === "drawmode_";
		if( isDrawMode ) {
			this.setDrawMode(id.substring("drawmode_".length));
		} else if( id === 'foreground_color' ) {
			this.selectForegroundColor();
		} else if( id === 'add_poi' ) {
			if( this.drawMode === 'poi' ) {
				this.toolbar.setItemState('add_poi', false);
				this.drawMode = null;
			} else {
				this.setDrawMode('poi');
			}
		}
	},

	/**
	 * Adds a new annotation and fires a notification event.
	 */
	pushAnnotation: function(annotation) {
		this.annotations.push(annotation);
		console.log("added annotation %o", annotation);
		$(this).trigger({
			type: 'annotationAdded',
			annotation: annotation,
			index: this.annotations.length - 1
		});
	},

	/**
	 * Update the annotation.data values of the index'th annotation.
	 * If modified, ensures the annotation is redrawn and a notification
	 * event is fired.
	 */
	updateAnnotationData: function(index, values) {
		if( index < 0 || index >= this.annotations.length )
			throw {message: 'Index out of bounds: ' + String(index)};

		var annotation = this.annotations[index];
		var data = annotation.data;
		var modified = {}, isModified = false;
		for( var prop in values ) {
			if( !values.hasOwnProperty(prop) ) continue;
			var newVal = values[prop];
			if( data[prop] !== newVal ) {
				modified[prop] = data[prop] = newVal;
				isModified = true;
			}
		}

		if( isModified ) {
			annotation.redraw();
			$(this).trigger({
				type: 'annotationUpdated',
				annotation: annotation,
				index: index,
				values: modified
			});
		}
	},

	/** Return all the annotation data as value objects. */
	storeAnnotations: function() {
		return $.map(this.annotations, function(el, idx) {
			return el.data.asValueObject();
		});
	},

	/** Remove all the current annotations. */
	clearAnnotations: function() {
		var annotations = this.annotations, annotation;
		while( annotation = annotations.pop() )
			annotation.detach();
		$(this).trigger({
			type: 'allAnnotationsChanged'
		});
	},

	/** Load a set of annotations from value objects. */
	loadAnnotations: function(values) {
		var overlay;
		this.clearAnnotations();
		for( var i=0, ilen=values.length; i < ilen; ++i ) {
			overlay = AnnotationOverlay.fromValueObject(values[i]);
			overlay.attachTo(this.viewer);
			this.annotations.push(overlay);
		}
		$(this).trigger({
			type: 'allAnnotationsChanged'
		});
	},

	_stateChanged: function(id, state) {
		_log('_stateChanged', id, state, this);
		if( 'start_draw' === id ) {
			this.setIsDrawing(state);
		}
	}
});


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


