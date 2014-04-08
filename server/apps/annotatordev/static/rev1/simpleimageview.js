
'use strict';


// Initialization of angular root application
var derm_app = angular.module('DermApp', ['ui.bootstrap', 'ngSanitize']);

// Initialization of angular app controller with necessary scope variables. Inline declaration of external variables
// needed within the controller's scope. State variables (available between controllers using $rootScope). Necessary to
// put these in rootScope to handle pushed data via websocket service.
var appController = derm_app.controller('ApplicationController', ['$scope', '$rootScope', '$location', '$timeout', '$http',
    function ($scope, $rootScope, $location, $timeout, $http) {

        // global ready state variable
        $rootScope.applicationReady = false;
        $rootScope.viewer = undefined;

        // wait for everything to load then call init script
        $timeout(function(){
            $rootScope.ApplicationInit();
        }, 300);

        // initial layout values
        $("#angular_id").height(window.innerHeight - 80);
        $("#annotationView").height(window.innerHeight - 80);

        $rootScope.annotation_state = undefined;




        // main application, gives a bit of a delay before loading everything
        $rootScope.ApplicationInit = function() {

             console.log("Initializing angular application controller");

             // pull user variables (via template render) in js app...
             var current_user = $("#user_email").val();
             var current_user_id = $("#user_id").val();

             $rootScope.user_email = current_user;
             $rootScope.user_id = current_user_id;

            // initialize the AnnotationState
            $rootScope.annotation_state = new AnnotationState();
            $rootScope.annotation_state.clearAnnotations();


            var pathArray = window.location.pathname.split( '/' );

            var mskcc_key = pathArray[pathArray.length - 1];


            var image_single = '/mskccimage/' + mskcc_key

            $rootScope.active_image = undefined;
            $http.get(image_single).then(function (response) {

                $rootScope.active_image = response.data;
            })


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

        // shortcut key bindings -> takes you home to task list
        Mousetrap.bind( ['ctrl+q'], function(evt) {
            if (typeof (evt.preventDefault) === 'function') {evt.preventDefault();}
            else {evt.returnValue = false}
//            $rootScope.state_machine.gohome();
            $rootScope.debug = !$rootScope.debug;

            $scope.$apply();
        });





        // get annotation from server

        $rootScope.getAnnotationFromServer = function() {

            // get current annotation
            var annotationForImageURL = '/image/' + $rootScope.active_image[0].DA_id + '/annotation'

            // we don't know which annotation_id this belongs too yet, get by image & user
            $http.get(annotationForImageURL).then(function (response) {

                console.log(response.data);

                if(response.data){

                    $rootScope.remote_annotation = response.data;
                }
            });

//            console.log()
//
//            var url = 'annotation/1';
//
//            $http.get(url).then(function (response) {
//
//                $rootScope.remote_annotation = response.data;
//
//            });

// ALTERNATIVE syntax -> use this if we need to handle anything on the error side of things

//          $http({method: 'GET', url: '/someUrl'}).
//          success(function(data, status, headers, config) {
//            // this callback will be called asynchronously
//            // when the response is available
//          }).
//          error(function(data, status, headers, config) {
//            // called asynchronously if an error occurs
//            // or server returns response with an error status.
//          });

        }


//        $scope.$watch('remote_annotation', function(newValue){
//
//            console.log(newValue);
//        });


//        // find a good location for this
//        $rootScope.updateProgressStack = function() {
////            console.log('Update progress stack');
//            $scope.stacked = [];
//
//            var per_segment_width = 100 / ($rootScope.annotation_list.length * 4);
//
//            for(var i=0; i<$rootScope.annotation_list.length; i++)
//            {
//
//                var base_type;
//                var rel_type;
//                var o = $rootScope.annotation_list[i];
//
//                if(o.complete){
//
//                    $scope.stacked.push({
//                        value: 4*per_segment_width,
//                        type: "success"
//                    })
//
//                }
//                else
//                {
//                    if(o.viewed) {
//                        base_type = 'info';
//                    }
//                    else {
//                        base_type = 'warning';
//                    }
//
//                    if($rootScope.annotation_list[i].markupnormal.length > 0) {
//                        rel_type = 'danger'
//                    }
//                    else {
//                        rel_type = base_type;
//                    }
//
//                    $scope.stacked.push({
//                        value: per_segment_width,
//                        type: rel_type
//                    })
//
//                    if($rootScope.annotation_list[i].markuplesion.length > 0) {
//                        rel_type = 'danger'
//                    }
//                    else {
//                        rel_type = base_type;
//                    }
//
//                    $scope.stacked.push({
//                        value: per_segment_width,
//                        type: rel_type
//                    })
//
//                    if($rootScope.annotation_list[i].patterns.length > 0) {
//                        rel_type = 'danger'
//                    }
//                    else {
//                        rel_type = base_type;
//                    }
//
//                    $scope.stacked.push({
//                        value: per_segment_width,
//                        type: rel_type
//                    })
//
//                    if($rootScope.annotation_list[i].details.length > 0) {
//                        rel_type = 'danger'
//                    }
//                    else {
//                        rel_type = base_type;
//                    }
//
//                    $scope.stacked.push({
//                        value: per_segment_width,
//                        type: rel_type
//                    })
//
//                }
//            }
//        }




}]);

























var annotationView = derm_app.controller('AnnotationView', ['$scope', '$rootScope', '$timeout',

    function ($scope, $rootScope, $timeout) {

        $rootScope.viewer = new OpenSeadragon.Viewer({
            id: "annotationView",
            prefixUrl: '/static/images/osd_icons/',
            showNavigator: true
        });

        $rootScope.viewer.addHandler('open', function(event){

            // image okay, now pull annotations from server

            $rootScope.getAnnotationFromServer();

//            $rootScope.annotation_state.clearAnnotations();
//            $rootScope.annotation_state.loadAnnotations($rootScope.pullDataForCurrentState());

        });

//        eventName, handler
        $rootScope.$watch('active_image', function(newImage, originalValue) {

            // verify viewer exists
            if($rootScope.applicationReady)
            {
                console.log(newImage[0])

                $rootScope.viewer.openDzi(newImage[0].dzi_source);

                if($rootScope.annotation_state.viewer) {}
                else {
                    $rootScope.annotation_state.setSeadragonViewer($rootScope.viewer);
                }
            }
        });
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








// handle window resize events
function updateLayout() {

    var scope = angular.element($("#angular_id")).scope();
    scope.safeApply(function(){

//        scope.useVerticalbar = (window.innerWidth / window.innerHeight) > 1.0;

        $("#angular_id").height(window.innerHeight - 80);
        $("#annotationView").height(window.innerHeight - 80);
        $("#verticalToolbar").height(window.innerHeight - 80);

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














