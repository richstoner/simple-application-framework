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