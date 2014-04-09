/**
 * Created by stonerri on 3/13/14.
 */

'use strict';

// Initialization of angular root application
var review_app = angular.module('DermApp', ['ngSanitize', 'mousetrap']);

var appController = review_app.controller('ApplicationController', ['$scope', '$rootScope', '$timeout', '$http',
    function ($scope, $rootScope, $timeout, $http) {


        $("#angular_id").height(window.innerHeight - 80);
        $("#gridcontainer").height(window.innerHeight - 100);

        $scope.searchurl = 'http://dev.dermoscopic.com/images';

        $scope.start = 0;
        $scope.count = 30;

        $scope.end = function(){
            return $scope.start + $scope.count;
        }

        $scope.hover_image = undefined;

        $scope.flagged_list = {}

        // global properties
        $scope.user_email = $("#user_email").val();

        $scope.nextSet = function(){
            $scope.image_list = [];
            $scope.show_flags = false;
            $scope.start = $scope.start + $scope.count;
            $scope.getImages();
        }

        $scope.previousSet = function(){
            $scope.image_list = [];
            $scope.show_flags = false;
            $scope.start = Math.max($scope.start - $scope.count, 0);
            $scope.getImages();
        }


        $scope.image_list = [];

        $scope.show_flags = false;

        $scope.download = function(){

            var flags = $scope.flagged_list;
            flags['user'] = $scope.user_email;

            var json = JSON.stringify(flags);
            var blob = new Blob([json], {type: "application/json"});

            // save as json to local computer
            saveAs(blob, "flagged_images.json");
        }


        $scope.getImages = function(){

            var url = $scope.searchurl + '/' + $scope.start + '/' + $scope.count + '/';

            $http.get(url).then(function (response) {

                console.log(response)

                var temporary_array = [];

                response.data.forEach(function(hit){

                    var simple_rep = {}
                    simple_rep['thumbnail'] = hit.thumbnail;
                    simple_rep['title'] = hit.pyramid_filename;
                    simple_rep['file_path'] = hit.full_file_path;

                    if(hit.annotation){
                        simple_rep['annotation'] = hit.annotation.length;
                    }
                    else{
                        simple_rep['annotation'] = 0;
                    }

                    temporary_array.push(simple_rep)

                })

                $scope.image_list = temporary_array;

                $scope.show_flags = true;

            });
        }



        $scope.mouse = {
            '.' : $scope.nextSet,
            ',' : $scope.previousSet
        }




        $scope.flagged = function(index){
            var t = $scope.flagged_list[index];
            return (t != undefined);
        }

        $scope.getOffset = function(index){
            return $scope.start + index;
        }


        $scope.toggleFlag = function(index){

            var t = $scope.flagged_list[index];
            if (t != undefined) {
                $scope.flagged_list[index] = undefined;
            }
            else {
                $scope.flagged_list[index] = $scope.image_list[index - $scope.start];
            }

            console.log($scope.flagged_list)
        }



        $scope.imageHasAnnotations = function(index){

            var res = $scope.image_list[index].annotation > 0;

            return res;
        }

        $scope.safeApply = function( fn ) {
            var phase = this.$root.$$phase;
            if(phase == '$apply' || phase == '$digest') {
                if(fn) { fn(); }
            } else {
                this.$apply(fn);
            }
        };


        // run me!

        $scope.getImages();


    }]);



