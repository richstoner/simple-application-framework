

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