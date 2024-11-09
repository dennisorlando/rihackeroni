import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_polyline_points/flutter_polyline_points.dart';
import 'package:frontend_flutter/Vehicle.dart';
import 'package:frontend_flutter/VehiclesWidget.dart';
import 'package:frontend_flutter/Request.dart';
import 'package:frontend_flutter/dropdown_button.dart';
import 'package:google_maps_polyline/google_maps_polyline.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_map_geojson/flutter_map_geojson.dart';
import 'package:frontend_flutter/carousel.dart';
import 'package:latlong2/latlong.dart';

import 'package:flutter/services.dart' show rootBundle;

import 'VroomOutput.dart';

List<Vehicle> vehicles = [];
List<Color> vehicle_colors = [];
List<Request> requests = [];
List<Marker> markers = [];
VroomOutput ?output;
List<Polyline> rendered_polylines = [];

Map<int, VroomRoute> routes = {};

late _MyHomePageState homepage;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {

    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  List<Vehicle> loadVehiclesFromJson(String filePath) {
    final String jsonString = File(filePath).readAsStringSync();  // Synchronously read the file content
    final List<dynamic> jsonResponse = json.decode(jsonString);

    return jsonResponse.map((vehicle) => Vehicle.fromDict(vehicle)).toList();  // Map and convert to List<Vehicle>
  }

  List<Request> loadRequestsFromJson(String filePath) {
    final String jsonString = File(filePath).readAsStringSync();  // Synchronously read the file content
    final List<dynamic> jsonResponse = json.decode(jsonString);

    return jsonResponse.map((request) => Request.fromJson(request)).toList();  // Map and convert to List<Request>
  }

  void update() {
    setState(() {

    });
  }

  @override
  Widget build(BuildContext context) {

    homepage = this;

    // URL to fetch the encoded polyline
    const String polylineUrl = 'http://10.69.0.2:8000/routes';  // Replace with your actual URL

    //vehicles = loadVehiclesFromJson("./vehicles.json");
    //requests = loadRequestsFromJson("./requests.json");
    vehicles = loadVehiclesFromJson("./historic_vehicles.json");
    requests = loadRequestsFromJson("./historic_requests.json");
    vehicle_colors = vehicles.map((v) {
      Random random = Random(v.id);
      return Color.fromARGB(255, random.nextInt(255), random.nextInt(100), random.nextInt(255));
    }).toList();
    markers = requests.map((r) {
      return Marker(
        height: 60,
        point: r.pickupLocation,
        child: Column(
          children: [ Icon(Icons.emoji_people_rounded, size: 16.0,), Text("#${r.id}")],
        )
      );
    }).toList();
    markers.addAll(requests.map((r) {
      return Marker(
        point: r.destination,
        child: Stack(
          children: [
            Icon(Icons.square, size: 16.0, color: Colors.white),
            Icon(Icons.local_hospital_outlined, size: 16.0, color: Colors.red),
          ],
        ),
      );
    }));
    markers.addAll(vehicles.map((v) {
      return Marker(
          height: 44.0,
          point: v.startLocation,
          child: Column(children: [
            Icon(Icons.car_crash_rounded),
            Text("#${v.id}")
          ],),
      );
    }));

    Map<String, dynamic> jsonData = {
      'requests': requests,
      'vehicles': vehicles,
    };

    // Function to fetch and decode the polyline
    Future<void> fetchAndDecodePolyline() async {
        final response = await http.post(
            Uri.parse(polylineUrl),
            headers: <String, String>{
              'Content-Type': 'application/json; charset=UTF-8',
            },
            body: jsonEncode(jsonData),
        );

        if (response.statusCode == 200) {
          output = VroomOutput.fromJson(jsonDecode(response.body));

          routes = {for (var route in output!.routes) route.vehicle: route};

        }
        else {
          // print(response.body);
        }
    }


    GeoJsonParser myGeoJson = GeoJsonParser();
    String testgj = File("./test_geojson").readAsStringSync();
    myGeoJson.parseGeoJsonAsString(testgj);

    return Scaffold(
      body: Stack(
        children: [
          FlutterMap(
            options: const MapOptions(
              initialCenter: LatLng(46.6695547, 11.1594185),
              initialZoom: 9.2,
            ),
            children: [
              TileLayer( // Display map tiles from any source
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'noi.rihackeroni.techpark',
              ),
              PolylineLayer(polylines: rendered_polylines),
              MarkerLayer(markers: markers),
            ],
          ),
          Positioned(
            top: 16,
            right: 16,
            child: FloatingActionButton(
              onPressed: () {
                fetchAndDecodePolyline().whenComplete(() {
                  setState(() {
                    fetchAndDecodePolyline();
                    rendered_polylines = routes.entries.map((r) {
                      return r.value.geometry;
                    }).toList();
                    update();
                  });
                });
              },
              child: Icon(Icons.sync),
            ),
          ),
          VehiclesWidget(),
          LocationPickerWidget(),
        ],
      ),
    );
  }
}


