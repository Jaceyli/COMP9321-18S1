var the_url= "http://127.0.0.1:5000";

var app = angular.module('myApp', []);
var token = "";

//create areas by Iganame or postcode
app.controller('ngc0', function($scope, $http) {
    $scope.mySubmit0 = function () {
        $http({
            method: 'GET',
            url: the_url + '/auth',
            params: { username: $scope.username, password: $scope.password},//params作为url的参数

        }).then(function successCallback(response) {
            $scope.login_response_status = "Status: " + response.status;
            $scope.login_response = "Welcome, " + response.data.type;
            token = response.data.token;
            console.log(token);
            $scope.username = '';
            $scope.password = '';
        }, function errorCallback(response) {
            console.log(response);
            $scope.login_response_status = "Status: " + response.status;
            $scope.login_response = response.data;
            $scope.username = '';
            $scope.password = '';
        });
    }
});

//create areas by Iganame or postcode
app.controller('ngc1', function($scope, $http) {
    $scope.mySubmit1 = function () {
         $scope.import_response_status ='Loading...';
         $scope.import_response='';
        $http({
            method: 'POST',
            url: the_url + '/create_area/' + $scope.lganame,
            headers: {
                // 'Accept': 'application/xml',
                'AUTH_TOKEN': token,
            }
        }).then(function successCallback(response) {
            $scope.import_response_status = "Status: " + response.status;
            $scope.import_response = response.data;
            console.log(response);
        }, function errorCallback(response) {
            console.log(response);
            $scope.import_response_status = "Status: " + response.status;
            $scope.import_response = response.data;
        });
    }
});


//get all areas
app.controller('ngc2', function($scope, $http) {
    $scope.mySubmit2 = function () {
        $scope.all_response_status ='Loading...';
         $scope.all_response='';
        console.log($scope.json1);
        $http({
            method: 'GET',
            url: the_url + '/get_all_areas',
            headers: {
                'Accept': $scope.json1,
                'auth_token':token
            }
        }).then(function successCallback(response) {
            $scope.all_response_status = "Status: " + response.status;
            if ($scope.json1 != "application/json"){
                $scope.all_response = response.data;
            }else{
                 $scope.all_response =  JSON.stringify(response.data,null, 2);
            }

            console.log(response);
        }, function errorCallback(response) {
            console.log(response);
            $scope.all_response_status = "Status: " + response.status;
            $scope.all_response = response.data;
        });
    }
});

//get one area by id
app.controller('ngc3', function($scope, $http) {
    $scope.mySubmit3 = function () {
        $scope.one_response_status ='Loading...';
         $scope.one_response='';
        console.log($scope.json2);
        $http({
            method: 'GET',
            url: the_url + '/get_one_area/' + $scope.get_tid,
            headers: {
                'Accept': $scope.json2,
                'auth_token':token
            }
        }).then(function successCallback(response) {
            $scope.one_response_status = "Status: " + response.status;
            if ($scope.json2 != "application/json"){
                $scope.one_response = response.data;
            }else{
                 $scope.one_response =  JSON.stringify(response.data,null, 2);
            }
            console.log(response);
        }, function errorCallback(response) {
            console.log(response);
            $scope.one_response_status = "Status: " + response.status;
            $scope.one_response = response.data;
        });
    }
});


//delete one area by id
app.controller('ngc4', function($scope, $http) {
    $scope.mySubmit4 = function () {
        $scope.del_response_status ='Loading...';
         $scope.del_response='';
        $http({
            method: 'DELETE',
            url: the_url + '/delete_one_area/' + $scope.del_tid,
            headers: {
                // 'Accept': 'application/xml',
                'auth_token':token
            }
        }).then(function successCallback(response) {
            $scope.del_response_status = "Status: " + response.status;
            $scope.del_response = response.data;
            console.log(response);
        }, function errorCallback(response) {
            console.log(response);
            $scope.del_response_status = "Status: " + response.status;
            $scope.del_response = response.data;
        });
    }
});


//select data by filter
app.controller('ngc5', function($scope, $http) {
    $scope.mySubmit5 = function () {
        $scope.filter_response_status ='Loading...';
         $scope.filter_response='';
        console.log($scope.json3);
        $http({
            method: 'GET',
            url: the_url + '/get_areas_with_filters',
            headers: {
                'Accept': $scope.json3,
                'auth_token':token
            },
            params: { filter: $scope.filter}
        }).then(function successCallback(response) {
            $scope.filter_response_status = "Status: " + response.status;
            if ($scope.json3 != "application/json"){
                $scope.filter_response = response.data;
            }else{
                 $scope.filter_response =  JSON.stringify(response.data,null, 2);
            }
            console.log(response);
        }, function errorCallback(response) {
            console.log(response);
            $scope.filter_response_status = "Status: " + response.status;
            $scope.filter_response = response.data;
        });
    }
});