
'use strict';


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




// Initialization of angular root application
var derm_app = angular.module('DermApp', ['ui.bootstrap', 'ngSanitize', 'toggle-switch', 'colorpicker.module', 'xml']);

derm_app.value( "ol", ol );

var olViewer = derm_app.factory('olViewer', function(ol, $http, xmlParser) {

        var olViewer = function(viewer_options) {

            console.log('Creating OLViewer with opts', viewer_options, this);

            var self = this;

            // Instance variables
            this.image_source = undefined;
            this.image_layer = undefined;

            this.map = undefined;

            this.draw_interaction = undefined;
            this.draw_mode = undefined;


            // annotations added that need to be saved
            this.clearTemporary();

            // annotations previously saved

            this.saved_annotations = [];

            var styleFunction = (function() {
              var styles = {};
              var image = new ol.style.Circle({
                radius: 5,
                fill: null,
                stroke: new ol.style.Stroke({color: 'orange', width: 2})
              });

              styles['Point'] = [new ol.style.Style({image: image})];

              styles['Polygon'] = [new ol.style.Style({
                stroke: new ol.style.Stroke({
                  color: 'blue',
                  width: 3
                }),
                fill: new ol.style.Fill({
                  color: 'rgba(0, 0, 255, 0.1)'
                })
              })];
              styles['MultiLinestring'] = [new ol.style.Style({
                stroke: new ol.style.Stroke({
                  color: 'green',
                  width: 3
                })
              })];
              styles['MultiPolygon'] = [new ol.style.Style({
                stroke: new ol.style.Stroke({
                  color: 'blue',
                  width: 1
                }),
                fill: new ol.style.Fill({
                  color: 'rgba(255, 255, 0, 0.1)'
                })
              })];
              styles['default'] = [new ol.style.Style({
                stroke: new ol.style.Stroke({
                  color: 'yellow',
                  width: 3
                }),
                fill: new ol.style.Fill({
                  color: 'rgba(255, 0, 0, 0.1)'
                }),
                image: image
              })];


              styles['normal'] = [new ol.style.Style({
                stroke: new ol.style.Stroke({
                  color: 'blue',
                  width: 2
                }),
                fill: new ol.style.Fill({
                  color: 'rgba(0, 0, 255, 0.2)'
                })
              })];
              styles['symmetry'] = [new ol.style.Style({
                stroke: new ol.style.Stroke({
                  color: 'black',
                  width: 3
                })
              })];
              styles['lesion'] = [new ol.style.Style({
                stroke: new ol.style.Stroke({
                  color: 'red',
                  width: 2
                }),
                fill: new ol.style.Fill({
                  color: 'rgba(255, 0, 0, 0.2)'
                })
              })];              
              
              return function(feature, resolution) {
                // console.log(feature)
                return styles[feature.get('classification')] || styles['default'];
              };
            })();



            // at some point, convert this into multiple layers
            this.vector_source = new ol.source.Vector();

            this.vector_layer = new ol.layer.Vector({
                source: this.vector_source,
                style: styleFunction
            })

            // initialize map (imageviewer)

            this.map = new ol.Map({
                renderer:'canvas',
                target: 'map',    
            });
            
            
            // set map event handlers

            this.map.on('singleclick', function(evt) {

                // console.log(evt.coordinate)
                var click_coords = [evt.coordinate[0], -evt.coordinate[1]];

                if (self.draw_mode == 'navigate') {

                    console.log("Click at native px:", click_coords);

                } else if (self.draw_mode == 'pointlist') {

                    self.addPoint(evt.coordinate);                	

                } else if (self.draw_mode == 'autofill') {

                    console.log("Click at native px:", click_coords);                    
                   
                   	self.autofill(click_coords)

                } else if (self.draw_mode == 'lines') {

                    self.addPoint(evt.coordinate);
                  
                } 
            });


            // magic wand point style
            var imageStyle = new ol.style.Circle({
              radius: 8,
              fill: new ol.style.Fill({color: '#00ccff'}),
              stroke: new ol.style.Stroke({color: '#333', width: 1})
            });


            this.map.on('postcompose', function(event) {

              var vectorContext = event.vectorContext;

              var frameState = event.frameState;

              vectorContext.setImageStyle(imageStyle);

              vectorContext.drawMultiPointGeometry(
                  new ol.geom.MultiPoint(self.temporary_annotations.polygons), null);

              vectorContext.drawMultiPointGeometry(
                  new ol.geom.MultiPoint(self.temporary_annotations.lines), null);

              self.map.requestRenderFrame();
            });




            // function onMoveEnd(evt) {
            //   var map = evt.map;
            //   var extent = map.getView().calculateExtent(map.getSize());
            //   console.log(extent);
            // }

            // this.map.on('moveend', onMoveEnd);
    
            // add zoom slider

            var zoomslider = new ol.control.ZoomSlider();
            this.map.addControl(zoomslider);
        }



        // Define the "instance" methods using the prototype
        // and standard prototypal inheritance.
        olViewer.prototype = {

            clearCurrentImage : function(){

                if(this.image_layer){
                    this.map.removeLayer(this.image_layer);
                }

            },

            hasTemporaryAnnotations : function (){

                var tempLength = this.temporary_annotations.polygons.length + Math.floor(this.temporary_annotations.lines.length / 2)+ this.temporary_annotations.points.length + this.temporary_annotations.select;
                // console.log('Temp length', tempLength);
                return tempLength > 0;

            },

            hasSavedAnnotations : function() {
                return this.saved_annotations.length > 0;
            },

            featureListFromAnnotation : function(annotation){

            	// console.log(annotation);

                var features_list = [];

                if (annotation.polygons.length > 0) {

                    var af_feature = new ol.Feature({
                        'classification' : annotation.classification
                    });

                    af_feature.setGeometry(new ol.geom.Polygon([annotation.polygons]))
                    features_list.push(af_feature)
                };


				if (annotation.lines.length > 0) {

                    var l_feature = new ol.Feature({
                        'classification' : annotation.classification
                    });

                    l_feature.setGeometry(new ol.geom.Polygon([annotation.lines]))
                    features_list.push(l_feature)

                };

                return features_list;

            },

            saveSelectionStack : function(selection_stack){

            	// if (this.saved_annotations.length > 0) {
	            // 	var lastAnnotation = this.saved_annotations[this.saved_annotations.length];
	            // 	lastAnnotation.select = selection_stack;
            	// }
            	// else {

					this.temporary_annotations.select = selection_stack;
            		this.temporary_annotations.classification = 'lesion';
					this.saved_annotations.push(this.temporary_annotations);
	
            	// }
            	// var temporary_annotations = $rootScope.imageviewer.saveTemporaryAnnotations($scope.step_config.classification)

            	console.log('temp', this.saved_annotations);

            	this.clearTemporary();
            },

            saveTemporaryAnnotations : function (classification){
                // Moves the temporary annotation to the saved annotation state

                this.temporary_annotations.createdate = new Date().valueOf();
                this.temporary_annotations.classification = classification
                
                var features = this.featureListFromAnnotation(this.temporary_annotations);

                for(var i=0; i<features.length;i++){
                    this.vector_source.addFeature(features[i])
                }

                this.saved_annotations.push(this.temporary_annotations)

				this.clearTemporary();
            },



            getSavedAnnotations : function(){

                var s = this.saved_annotations;

                this.saved_annotations = [];

                this.vector_source.clear();
                return s;

            },

            setAnnotations : function(annotations){

            	console.log('annotion to set', annotations)

            	if (annotations) {

            		var feature_list = [];	   

            		for(var key in annotations){

            			var features = this.featureListFromAnnotation(annotations[key]);	

		                for(var i=0; i<features.length;i++){
		                    this.vector_source.addFeature(features[i])
		                }

            		}

	            	this.saved_annotations = annotations;

            	};
            },

            addPoint : function(click_coords){

                var pointurl = 'point'
                var msg = {};
                msg['click'] = click_coords
                var self = this;
                // interesting hack to get the UI to update without external scopy applys
                $http.post(pointurl, msg).success(function(response){

                    self.temporary_annotations.lines.push(response.point.click)

                    // only store last two points if we're doing lines of symmetry
                    if (self.draw_mode == 'lines') {

	                    if(self.temporary_annotations.lines.length == 3){
	                        self.temporary_annotations.lines.splice(0,1);
	                    }
	                    	
                    };
                    
                });


            },

            clearTemporary : function(){

				this.temporary_annotations = {
	                polygons : [],
	                lines : [],	
	                points : [],
	                select : [],
	                classification : '',
	                createdate : -1
	            };

            },

            acceptPainting : function(){

                var annotation = this.segmentannotator.getAnnotation();

                var extent = this.map.getView().calculateExtent(this.map.getSize());
                var tr = ol.extent.getTopRight(extent)
                var tl = ol.extent.getTopLeft(extent)
                var bl = ol.extent.getBottomLeft(extent)

                var segmenturl = 'segment'

                var msg = {};
                msg['image'] = annotation
                msg['extent'] = [tr, bl]

                var self = this;
                // interesting hack to get the UI to update without external scopy applys
                $http.post(segmenturl, msg).success(function(response){

                    self.temporary_annotations.polygons = []

                    var contours = JSON.parse(response.contourstr);
                    console.log(contours[0]);

                    self.temporary_annotations.polygons = contours[0].slice()

                    delete self.segmentannotator;

                    $('#annotatorcontainer').empty();

                    self.map.unfreezeRendering();
                    self.map.requestRenderFrame();

                    // console.log(self.temporary_annotations.autofill);
                    // var inner = JSON.parse(response.contour.inner);
                    
                    // var transform = JSON.parse(response.xform);
                    
                    // self.segmentation_list = [];
                    // self.temporary_annotations.autofill = []

                    // var applyTransform = function(pt, _transform){
                    //     var px = (pt[0] / _transform.scale[0]) + _transform.offset[0];
                    //     var py = - (pt[1] / _transform.scale[1]) + _transform.offset[1];
                    //     return [px, py];
                    // }

                    // for (var j =0; j < outer.length; j++)
                    // {                        
                    //     var c = applyTransform(outer[j][0], transform);

                    //     self.temporary_annotations.autofill.push(c)
                    // }

                    // for (var j =0; j < inner.length; j++)
                    // {                        
                    //     var c = applyTransform(inner[j][0], transform);

                    //     self.temporary_annotations.autofill.push(c)
                    // }
                    // self.temporary_annotations.lines.push(response.point.click)

                    // if(self.temporary_annotations.lines.length == 3){
                    //     self.temporary_annotations.lines.splice(0,1);
                    // }
                    
                });

            },


            startPainting : function(){

            // if ('download' in exportPNGElement) {
            //   exportPNGElement.addEventListener('click', function(e) {
            //     map.once('postcompose', function(event) {
            //       var canvas = event.context.canvas;
            //       exportPNGElement.href = canvas.toDataURL('image/png');
            //     });
            //     map.render();
            //   }, false);

                var self = this;

                this.map.once('postcompose', function(event) {

                    var canvas = event.context.canvas;

                    self.segmentannotator = new SLICSegmentAnnotator(canvas, {
                        regionSize: 50,
                        container: document.getElementById('annotatorcontainer'),
                        backgroundColor: [0,0,0],
                        // annotation: 'annotation.png' // optional existing annotation data.
                        labels: [
                          {name: 'background', color: [255, 255, 255]},
                          'lesion',
                          'normal',
                          'other'
                          ],
                        onload: function() {
                          // initializeLegend(this);
                          // initializeLegendAdd(this);
                          // initializeButtons(this);
                        }
                      });


                    self.segmentannotator.setCurrentLabel(3);

                    self.map.freezeRendering();


                //   // exportPNGElement.href = canvas.toDataURL('image/png');
                });



                // this.map.freezeRendering();
                // this.map.render();



                // var self = this;

                // var extent = this.map.getView().calculateExtent(this.map.getSize());
                // var tr = ol.extent.getTopRight(extent)
                // var tl = ol.extent.getTopLeft(extent)
                // var bl = ol.extent.getBottomLeft(extent)

                // // think: if x is positive on left, subtract from total width
                // // if x on right is greater than width, x = width

                // var origin_x = 0;
                // var origin_y = 0;

                // var click_x_offset = 0;
                // var click_y_offset = 0;

                // var newWidth = this.nativeSize.w;

                // if(tr[0] < this.nativeSize.w) {
                //     newWidth = tr[0];
                // };
                // if(tl[0] > 0) {
                //     newWidth -= tl[0]
                //     origin_x = tl[0]
                //     click_x_offset
                // };

                // var newHeight = this.nativeSize.h;
                
                // if(- bl[1] < this.nativeSize.h) {
                //     newHeight = -bl[1];
                // };
                // if(tl[1] < 0) {
                //     newHeight += tl[1]
                //     origin_y = -tl[1];
                // }                

                // console.log(origin_x, origin_y, newWidth, newHeight);

                // if (newWidth <= 0 || newHeight <= 0){
                //     console.log('offscreen or invalid region')
                // };

                // var rel = []
                // rel[0] = origin_x / this.nativeSize.w;
                // rel[1] = origin_y / this.nativeSize.h;
                // rel[2] = newWidth / this.nativeSize.w;
                // rel[3] = newHeight / this.nativeSize.h;

                // var dataurl = function(rel, width){
                //     return '&WID=' + width + '&RGN=' + rel.join(',') + '&CVT=jpeg'
                // }

                // // var url_to_use = this.data_url + '&WID=400&RGN=0.25,0.25,0.5,0.5&CVT=jpeg'
                
                // var url_to_use = this.data_url + dataurl(rel, newWidth);


                // new SLICSegmentAnnotator(url_to_use, {
                //     regionSize: 70,
                //     container: document.getElementById('annotatorcontainer'),
                //     backgroundColor: [0,0,0],
                //     // annotation: 'annotation.png' // optional existing annotation data.
                //     labels: [
                //       {name: 'background', color: [255, 255, 255]},
                //       'lesion',
                //       'normal',
                //       'other'
                //       ],
                //     onload: function() {
                //       // initializeLegend(this);
                //       // initializeLegendAdd(this);
                //       // initializeButtons(this);
                //     }
                //   });

                // <a id="export-png" class="btn" download="map.png"><i class="icon-download"></i> Export PNG</a>
        

            },
            autofill : function(click_coords){

                var self = this;

                var extent = this.map.getView().calculateExtent(this.map.getSize());
                var tr = ol.extent.getTopRight(extent)
                var tl = ol.extent.getTopLeft(extent)
                var bl = ol.extent.getBottomLeft(extent)

                // think: if x is positive on left, subtract from total width
                // if x on right is greater than width, x = width

                var origin_x = 0;
                var origin_y = 0;

                var click_x_offset = 0;
                var click_y_offset = 0;

                var newWidth = this.nativeSize.w;

                if(tr[0] < this.nativeSize.w) {
                    newWidth = tr[0];
                };
                if(tl[0] > 0) {
                    newWidth -= tl[0]
                    origin_x = tl[0]
                    click_x_offset
                };

                var newHeight = this.nativeSize.h;
                
                if(- bl[1] < this.nativeSize.h) {
                    newHeight = -bl[1];
                };
                if(tl[1] < 0) {
                    newHeight += tl[1]
                    origin_y = -tl[1];
                }                

                console.log(origin_x, origin_y, newWidth, newHeight);

                if (newWidth <= 0 || newHeight <= 0){
                    console.log('offscreen or invalid region')
                };

                var rel = []
                rel[0] = origin_x / this.nativeSize.w;
                rel[1] = origin_y / this.nativeSize.h;
                rel[2] = newWidth / this.nativeSize.w;
                rel[3] = newHeight / this.nativeSize.h;

                var dataurl = function(rel, width){
                    return '&WID=' + width + '&RGN=' + rel.join(',') + '&CVT=jpeg'
                }

                // var url_to_use = this.data_url + '&WID=400&RGN=0.25,0.25,0.5,0.5&CVT=jpeg'
                
                var url_to_use = this.data_url + dataurl(rel, 500);

                var subimage = {}
                subimage.origin = [origin_x, origin_y]
                subimage.size = [newWidth, newHeight]

                var origimage = {}
                origimage.origin = [0,0]
                origimage.size = [this.nativeSize.w, this.nativeSize.h]


                // relative click is not based on the image origin, but rather the extent origin
                var click = {}
                click.absolute = click_coords;
                click.relative = [(click_coords[0])/this.nativeSize.w, (click_coords[1])/this.nativeSize.h]


                var msg = {}
                msg.image = {}
                msg.image.region = subimage
                msg.image.base = origimage
                msg.image.url = url_to_use
                msg.tolerance = 80;
                msg.click = click

                // console.log(msg);

                var segmentURL = 'fillrev1'

                $http.post(segmentURL, msg).success(function(response){

                    // var coords = 
                    var outer = JSON.parse(response.contour.outer);
                    // var inner = JSON.parse(response.contour.inner);
                    
                    var transform = JSON.parse(response.xform);
                    
                    // self.segmentation_list = [];
                    self.temporary_annotations.polygons = []

                    var applyTransform = function(pt, _transform){
                        var px = (pt[0] / _transform.scale[0]) + _transform.offset[0];
                        var py = - (pt[1] / _transform.scale[1]) + _transform.offset[1];
                        return [px, py];
                    }

                    for (var j =0; j < outer.length; j++)
                    {                        
                        var c = applyTransform(outer[j][0], transform);

                        self.temporary_annotations.polygons.push(c)
                    }

                    // console.log(self.temporary_annotations.polygons);

                    // for (var j =0; j < inner.length; j++)
                    // {                        
                    //     var c = applyTransform(inner[j][0], transform);
                    //     self.temporary_annotations.autofill.push(c)
                    // }

                });



            },

            setDrawMode : function(draw_mode) {

                this.draw_mode = draw_mode;

                if (draw_mode == 'navigate') {
                } else if (draw_mode == 'paintbrush') {
                } else if (draw_mode == 'autofill') {
                } else if (draw_mode == 'lines') {
                } 

            },

            loadImageWithURL : function(dzi_url) {

                var self = this;
                self.segmentation_list = [];

                var base_array = dzi_url.split('DeepZoom')
                var data_array = dzi_url.split('DeepZoom')

                base_array.splice(1, 0, "Zoomify");
                data_array.splice(1, 0, 'FIF')

                var zoomify_join = base_array.join('');
                var zoomify_url =  zoomify_join.substr(0, zoomify_join.length - 4);

                var data_join = data_array.join('')
                var data_url = data_join.substr(0, data_join.length - 4);

                self.zoomify_url = zoomify_url;
                self.data_url = data_url;

                var image_properties_xml = zoomify_url + '/ImageProperties.xml'

                $http.get(image_properties_xml).then(function (hresp) {

                    /* Parse a Zoomify protocol metadata request

                    */
                    var parseMetaData = function(response){
                        // Simply split the reponse as a string
                        var tmp = response.split('"');
                        var w = parseInt(tmp[1]);
                        var h = parseInt(tmp[3]);
                        var ts = parseInt(tmp[11]);
                        // Calculate the number of resolutions - smallest fits into a tile
                        var max = (w>h)? w : h;
                        var n = 1;
                        while( max > ts ){
                          max = Math.floor( max/2 );
                          n++;
                        }
                        var result = {
                          'max_size': { w: w, h: h },
                          'tileSize': { w: ts, h: ts },
                          'num_resolutions': n
                        };
                        return result;
                    }

                    var metadata = parseMetaData(hresp.data)
                    // console.log(metadata);

                    self.imageCenter = [metadata.max_size.w / 2, - metadata.max_size.h / 2];

                    self.proj = new ol.proj.Projection({
                        code: 'ZOOMIFY',
                        units: 'pixels',
                        extent: [0, 0, metadata.max_size.w, metadata.max_size.h]
                    });

                    var crossOrigin = 'anonymous';

                    self.image_source = new ol.source.Zoomify({
                        url: zoomify_url + '/',
                        size: [metadata.max_size.w, metadata.max_size.h],
                        crossOrigin: crossOrigin,

                    });

                    self.image_layer = new ol.layer.Tile({
                       source: self.image_source,
                       preload: 1
                    })

                    self.nativeSize = metadata.max_size;

                    self.view = new ol.View2D({
                      projection: self.proj,
                      center: self.imageCenter,
                      zoom: 2,
                      maxZoom: metadata.num_resolutions 
                    })       

                    self.map.addLayer(self.image_layer);
                    self.map.addLayer(self.vector_layer);
                    self.map.setView(self.view);

                })
            }
        }

        return( olViewer );

        }
    );
    


































// Initialization of angular app controller with necessary scope variables. Inline declaration of external variables
// needed within the controller's scope. State variables (available between controllers using $rootScope). Necessary to
// put these in rootScope to handle pushed data via websocket service.
var appController = derm_app.controller('ApplicationController', ['$scope', '$rootScope', '$location', '$timeout', '$http', 'imageList', 'decisionTree', 'olViewer',
    function ($scope, $rootScope, $location, $timeout, $http, imageList, decisionTree, olViewer) {

        // global ready state variable
        $rootScope.applicationReady = false;

        $rootScope.imageviewer = undefined;

         // pull user variables (via template render) in js app...
         var current_user = $("#user_email").val();
         var current_user_id = $("#user_id").val();
         $rootScope.user_email = current_user;
         $rootScope.user_id = current_user_id;


        // initial layout    
        $("#angular_id").height(window.innerHeight);
        $("#map").height(window.innerHeight);
        

        $rootScope.image_list = [];
        $rootScope.image_index = undefined;

        var useRandomStart = false;
        if(useRandomStart){
            $rootScope.startingIndex =  Math.floor(175 * Math.random());
        }
        else{
            $rootScope.startingIndex = 0;    
        }
        

        $timeout(function(){
            $rootScope.ApplicationInit();
        }, 300);


        // main application, gives a bit of a delay before loading everything
        $rootScope.ApplicationInit = function() {

             $rootScope.debug  = $location.url().indexOf('debug') > -1;

             // load subject list from json file
             var shouldShuffle = true;

             imageList.fromDB(current_user, $rootScope.startingIndex, 10, shouldShuffle).then(function(d){

                $rootScope.image_list = d;

             });

             decisionTree.fromLocal().then(function(d){
                $rootScope.decision_tree = d;
             });

            $rootScope.imageviewer = new olViewer({'div' : 'annotationView'});

            $rootScope.applicationReady = true;

        };


        $scope.safeApply = function( fn ) {
            var phase = this.$root.$$phase;
            if(phase == '$apply' || phase == '$digest') {
                if(fn) { fn(); }
            } else {
                this.$apply(fn);
            }
        };


        // effectively a callback from the initial subject query
        $rootScope.$watch('image_list', function(newValue, originalValue) {
            if($rootScope.applicationReady){
                $rootScope.image_index = 0;    
            }
        });


        $rootScope.getActiveImage = function(){
            if($rootScope.applicationReady){
                return $rootScope.image_list[$rootScope.image_index];
            }
            return undefined;
        }

        $rootScope.$watch('image_index', function(newValue, originalValue) {
            if ($rootScope.applicationReady) {
                var activeImage = $rootScope.getActiveImage();
                $rootScope.imageviewer.clearCurrentImage();
                $rootScope.imageviewer.loadImageWithURL(activeImage.dzi_source);
            };
        });

}]);


























var annotationTool = derm_app.controller('AnnotationTool', ['$scope', '$rootScope', '$timeout', '$sanitize', '$http',
    function ($scope, $rootScope, $timeout, $sanitize, $http) {

        console.log('Initialized annotation tool.');


        $scope.draw_mode = 'navigate';


        $scope.completedImages = 0;
        $scope.totalItems = 0;

        $scope.step = -1;
        $scope.totalSteps = 0;

        // local scope from nested vars
        $scope.step_config = undefined;
        $scope.tool_bar_state = undefined;
        $scope.active_image = undefined;
        $scope.step_options = undefined;
        $scope.step_base = '';

        $scope.select_stack = [];
        $scope.select_last = undefined;
        

        $scope.annotations = undefined;

        $rootScope.$watch('image_index', function(newValue, originalValue) {

            if ($rootScope.applicationReady) {
                $scope.active_image = $rootScope.getActiveImage();
            };
        });

		$rootScope.$watch('image_list', function(newValue, originalValue) {

            if ($rootScope.applicationReady) {

            	$scope.totalItems = $rootScope.image_list.length;

            	$scope.annotations = [];


            	$.each($rootScope.image_list, function(n, image_data){

                     var placeholder_obj = {
                         complete: false,
                         annotationid: undefined,
                         step: {},
                         userid: $rootScope.current_user_id,
                         imageid: image_data.DA_id,
                         mskccid: image_data.DA_key,
                         saved: false,
                         lastUpdateDate: -1
                     };

                     $scope.annotations.push(placeholder_obj);
                 });            		

            	
            	console.log('annotations?', $scope.annotations);
            };
        });


        // shortcut key bindings -> takes you home to task list
        Mousetrap.bind( ['ctrl+q'], function(evt) {
            if (typeof (evt.preventDefault) === 'function') {evt.preventDefault();}
            else {evt.returnValue = false}
            $rootScope.debug = !$rootScope.debug;
            $scope.$apply();
        });


        // watches

        // effectively a callback from the initial subject query
        $rootScope.$watch('decision_tree', function(newValue, originalValue) {

            if($rootScope.applicationReady){
            
                console.log("There are " + $rootScope.decision_tree.length + ' steps');

                $scope.totalSteps = $rootScope.decision_tree.length;



            }
        });




        // Accessors

        $scope.getCurrentStepConfig = function(){
            if ($scope.step >= 0) {
                return $rootScope.decision_tree[$scope.step]    
            };

            return undefined;
        }

        $scope.getCurrentAnnotation = function(){
        	if($rootScope.applicationReady){
        		if ($scope.annotations) {
        			return $scope.annotations[$scope.image_index];	
        		};
        	}
        	return undefined;
        }


        // setters

        $scope.saveStepAnnotation = function(annotations, step_to_save){

        	var currentAnnotation = $scope.getCurrentAnnotation();
        	currentAnnotation.step[step_to_save] = annotations;
        }

        $scope.getStepAnnotations = function(){

        	var currentAnnotation = $scope.getCurrentAnnotation();
        	console.log('current annotation', currentAnnotation);
        	return currentAnnotation.step[$scope.step]
        }



        // controls

        $scope.selectImage = function(selected_index){
            $rootScope.image_index = selected_index;
        }

        $scope.nextStep = function(){

            $scope.gotoStep($scope.step+1);
        }

        $scope.previousStep = function(){
            $scope.gotoStep($scope.step-1);
        }

        $scope.resetStep = function(){

        	$scope.clearPoints();


            // if we're returning from a selectadvanced workflow, keep stack and add 
            if ($scope.select_last){

            	console.log('completed annotation');

                $scope.select_stack.push($scope.select_last)

               	console.log($scope.step_options);

				$rootScope.imageviewer.saveSelectionStack($scope.select_stack);

            	$scope.select_last = undefined;


            }
            else {

	            $scope.step_config = $scope.getCurrentStepConfig();

	            if ($scope.step_config.default != "") {
					$rootScope.imageviewer.setDrawMode($scope.step_config.default);	
	            }
	            else {
	            	$rootScope.imageviewer.setDrawMode('navigate');	
	            }

            	$scope.step_options = $scope.step_config.options;
            	$scope.step_base = $scope.step_config.step;

            	$scope.select_stack = [];	
            }

            $scope.tool_bar_state = $scope.step_config.type; // load defaults, will adjust as navigating tree
        }




        $scope.gotoStep = function(step){

            if (step >= 0 && step < $scope.totalSteps) {

            	if ($rootScope.imageviewer.hasSavedAnnotations()){
            		$scope.saveStepAnnotation($rootScope.imageviewer.getSavedAnnotations(), $scope.step);
                };

                $scope.step = step;
                $scope.resetStep();

                var stepAnnotations = $scope.getStepAnnotations()
                
                console.log('step annotations', stepAnnotations);

                if (stepAnnotations) {

                	$rootScope.imageviewer.setAnnotations(stepAnnotations);	

                	for(var i=0; i<stepAnnotations.length;i++){
                		if(stepAnnotations[i].select.length > 0){
                			$scope.select_stack = stepAnnotations[i].select;	
                		}
                	}
                };
            }
            else if (step == $scope.totalSteps) {


            	console.log($scope.getCurrentAnnotation());

            	var msg ={};


				msg['user_id'] = $rootScope.user_id;
				msg['annotation'] = $scope.getCurrentAnnotation()

				// msg['image_id'] = $rootScope.u;
                var self = this;
                // interesting hack to get the UI to update without external scopy applys

                var annotation_url = 'annotation/'

                $http.post(annotation_url, msg).success(function(response){


                	console.log(response);

                	$scope.step = -1;
                	
                    // self.temporary_annotations.lines.push(response.point.click)

                    // // only store last two points if we're doing lines of symmetry
                    // if (self.draw_mode == 'lines') {

	                   //  if(self.temporary_annotations.lines.length == 3){
	                   //      self.temporary_annotations.lines.splice(0,1);
	                   //  }
	                    	
                    // };
                    
                });



            }
        }





        $scope.startLines = function(){

			$rootScope.imageviewer.setDrawMode('lines');

        }

        $scope.startPointList = function(){

        	$scope.tool_bar_state = 'pldefine';
        	$rootScope.imageviewer.setDrawMode('pointlist');
        }




        $scope.startMagicWand = function(){
            $scope.tool_bar_state = 'mwdefine';
            $rootScope.imageviewer.setDrawMode('autofill');
        }

        $scope.acceptMagicWand = function(){
            $scope.tool_bar_state = 'mwaccept';   
        }


        $scope.startRegionPaint = function(){

        	$scope.tool_bar_state = 'rpdefine';
            $rootScope.imageviewer.setDrawMode('paintbrush');	
        }

        $scope.runRegionPaint = function(){

        	$scope.tool_bar_state = 'rppaint';
        	$rootScope.imageviewer.startPainting();

        }

        $scope.finishRegionPaint = function(){

			$scope.tool_bar_state = 'rpreview';
            $rootScope.imageviewer.acceptPainting();

        }

        $scope.cancelRegionPaint = function(){

        	$rootScope.imageviewer.acceptPainting();
        	$rootScope.imageviewer.clearTemporary();

        	$scope.resetStep();
        }

        $scope.clearPoints = function(){

        	$rootScope.imageviewer.clearTemporary();
        };


		$scope.saveCurrentPointsAsPolygon = function(){

		     if ($rootScope.applicationReady)
		     {
		     	var temporary_annotations = $rootScope.imageviewer.saveTemporaryAnnotations($scope.step_config.classification)

		     	$scope.resetStep();

		        return temporary_annotations;
		     }
		}






		$scope.selectOption = function(key, option_to_select) {



			var selected_url = 'static/rev1/' + $scope.step_base + '/' + (key+1) + '.jpg'

			console.log('selected url', selected_url)

			var select_single = {
				url : selected_url,
				key : key
			}
			
			if(option_to_select.type == 'select'){

				$scope.select_stack.push(select_single);
				$scope.step_options = option_to_select.options;
				$scope.step_base = $scope.step_base + '/' + (key+1);

			}
			else if (option_to_select.type == 'review') {


				$scope.select_stack.push(select_single);
				$rootScope.imageviewer.saveSelectionStack($scope.select_stack);
	        	$scope.tool_bar_state = option_to_select.type;

			}
			else if (option_to_select.type == 'selectadvanced') {

				$scope.select_last = select_single;

				// $rootScope.imageviewer.saveSelectionStack($scope.select_stack);

				$scope.step_options = option_to_select.options;
				
				$scope.step_base = $scope.step_base + '/' + (key+1);

	        	$scope.tool_bar_state = option_to_select.type;


			}
			else if(option_to_select.type == 'next') {

				console.log('proceeding to next step');

				$scope.nextStep();

			}

		}


        // state functions 

        $scope.showIfStep = function(step){            
            return parseInt(step) == $scope.step;
        }

        $scope.showIfStepGTE = function(step){
        	return parseInt(step) <= $scope.step;	
        }

        $scope.compareState = function(target, current_value){
            return target == current_value;
        }


        //temporary annotations = points that need to be converted into a polygon
        $scope.hasTemporaryAnnotations = function(){

            if ($rootScope.applicationReady)
            {
                return $rootScope.imageviewer.hasTemporaryAnnotations();
            }
            return false;
        }

        // saved annotations = points that have been converted... NOT TO BE CONFUSED WITH STEP annotations
        $scope.hasSavedAnnotations = function(){
            if ($rootScope.applicationReady)
            {
            	console.log($rootScope.imageviewer.hasSavedAnnotations())

                return $rootScope.imageviewer.hasSavedAnnotations();
            }
            return false;
        }

        $scope.stepHasAnnotations = function(step){

            if ($rootScope.applicationReady)
            {
            	var current_annotation = this.getCurrentAnnotation();

            	if (current_annotation) {

	            	var step_annotation = current_annotation.step[step]

	            	if(step_annotation){

	            		// console.log('step', step_annotation)	
	            		return step_annotation.length > 0;
	            	}


            	};
            }
            return false;
        }







        $scope.updateCompleteState = function() {

            if($rootScope.annotation_list.length > 0)
            {
                // update current image state
                var o = $rootScope.annotation_list[$rootScope.image_index];
                var is_complete = true;
                is_complete = o.step[1].length > 0 && is_complete;
                is_complete = o.step[2].length > 0 && is_complete;
                is_complete = o.step[3].length > 0 && is_complete;
                // is_complete = o.details.length > 0 && is_complete;

                o.complete = is_complete;

                // recalculate the total complete count
                var completed = 0;

                $.each($rootScope.annotation_list, function(n, subject_data){

                    if(subject_data.complete == true){
                        console.log('complete: ', subject_data);
                        completed +=1;
                    }
                });

                return completed;
            }
            return 0;
        }


        $scope.drawModeIs = function(mode_query) {

            if($rootScope.applicationReady)
            {            
                return mode_query == $scope.draw_mode;
            }
            return false;
        }



    }]);





var annotationView = derm_app.controller('AnnotationView', ['$scope', '$rootScope', '$timeout',

    function ($scope, $rootScope, $timeout) {


    }]);





// utilities
var studyToImageSource = function (study_num) {
    var src = "http://dermannotator.org/cgi-bin/iipsrv.fcgi?DeepZoom=/RAW_IMAGE_DATA/bigdata2/PYRAMIDS/MSKCC/BATCH1/B1/"
            + study_num + ".tif.dzi.tif.dzi";
//    console.log(src);
    return src;
};


var iff_filter = derm_app.filter('iif', function () {
   return function(input, trueValue, falseValue) {
        return input ? trueValue : falseValue;
   };
});


// drag and drop list directive
// directive for a single list
// based on code from
// http://www.smartjava.org/content/drag-and-drop-angularjs-using-jquery-ui
var dndList = derm_app.directive('dndList', function() {

    return function(scope, element, attrs) {

        // variables used for dnd
        var toUpdate;
        var startIndex = -1;

        // watch the model, so we always know what element
        // is at a specific position
        scope.$watch(attrs.dndList, function(value) {
            toUpdate = value;
        },true);

        // use jquery to make the element sortable (dnd). This is called
        // when the element is rendered
        $(element[0]).sortable({
            items:'li',
            start:function (event, ui) {
                // on start we define where the item is dragged from
                startIndex = ($(ui.item).index());
            },
            stop:function (event, ui) {
                // on stop we determine the new index of the
                // item and store it there
                var newIndex = ($(ui.item).index());
                var toMove = toUpdate[startIndex];
                toUpdate.splice(startIndex,1);
                toUpdate.splice(newIndex,0,toMove);

                // we move items in the array, if we want
                // to trigger an update in angular use $apply()
                // since we're outside angulars lifecycle
                scope.$apply(scope.model);
            },
            axis:'y'
        })
    }
});







// data sources

var imageList = derm_app.factory('imageList', function($http) {

  // shuffle from SO: http://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
  function shuffle(array) {
      var currentIndex = array.length
        , temporaryValue
        , randomIndex
        ;

      // While there remain elements to shuffle...
      while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
      }

      return array;
  }

  var imageList= {
    fromServer: function() {
        var url = 'http://example.com/json.json';
            var promise = $http.jsonp(url).then(function (response) {
          return response.data;
        });
      return promise;
    },
    fromLocal: function() {
        var url = 'static/data/json_subj_list.json';
            var promise = $http.get(url).then(function (response) {
          return response.data;
        });
      return promise;
    },

    // fromDB -> perform API request with user_id, image offset, count to get, and whether it should be shuffled
    fromDB: function(user_id, offset, count, shouldShuffle) {
        console.log('Query:: fromDB: ' + user_id + " " + offset + " " + count + " " + shouldShuffle)
//        var url = 'static/data/json_subj_list.json';
            var url = 'images/' + offset + "/" + count + "/";

            var promise = $http.get(url).then(function (response) {

            if(shouldShuffle){
//                return shuffle(response.data.slice(offset,count));
                return shuffle(response.data);
            }
            else
            {
//                return response.data.slice(offset, count);
                return response.data;
            }
        });
      return promise;
    }

    };

  return imageList;
});





var decisionTree = derm_app.factory('decisionTree', function($http) {

  var decisionTree= {
    fromServer: function() {
        var url = 'http://example.com/json.json';
            var promise = $http.jsonp(url).then(function (response) {

                console.log(response.data);
          return response.data;
        });
      return promise;
    },
    fromLocal: function() {
        var url = 'static/rev1/decisiontree.json';
            var promise = $http.get(url).then(function (response) {
          return response.data;
        });
      return promise;
    }

    };

  return decisionTree;
});




// handle window resize events
function updateLayout() {

    var scope = angular.element($("#angular_id")).scope();
    scope.safeApply(function(){

        $("#angular_id").height(window.innerHeight);
        $("#annotationView").height(window.innerHeight);

    })
}

function toggleDebug() {

    var scope = angular.element($("#angular_id")).scope();

    console.log('Angular state before: ', scope.debug);

    scope.safeApply(function(){

       scope.debug = !scope.debug;

    })

    console.log('Angular state before: ', scope.debug);

}

window.onresize = updateLayout;














