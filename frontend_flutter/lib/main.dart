import 'dart:collection';
import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_polyline_points/flutter_polyline_points.dart';
import 'package:frontend_flutter/Vehicle.dart';
import 'package:frontend_flutter/VehiclesWidget.dart';
import 'package:frontend_flutter/Request.dart';
import 'package:frontend_flutter/VroomOutput.dart';
import 'package:frontend_flutter/dropdown_button.dart';
import 'package:google_maps_polyline/google_maps_polyline.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_map_geojson/flutter_map_geojson.dart';
import 'package:frontend_flutter/carousel.dart';
import 'package:latlong2/latlong.dart';
import 'package:frontend_flutter/VroomOutput.dart';

import 'package:flutter/services.dart' show rootBundle;

List<Vehicle> vehicles = [];
List<Color> vehicle_colors = [];
List<Request> requests = [];
List<Marker> markers = [];
VroomOutput ?output;

Map<int, VroomRoute> ?routes;

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

  List<Polyline> polylineCoordinates = [];  // To store decoded polyline coordinates

  void update(){
    setState(() {});
  }

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

  @override
  Widget build(BuildContext context) {

    // URL to fetch the encoded polyline
    const String polylineUrl = 'http://10.69.0.2:8000/routes';  // Replace with your actual URL

    vehicles = loadVehiclesFromJson("./vehicles.json");
    requests = loadRequestsFromJson("./requests.json");
    vehicle_colors = vehicles.map((v) => Color((Random().nextDouble() * 0xFFFFFFFF).toInt())).toList();

    markers = requests.map((r) {
      return Marker(
        point: r.pickupLocation,
        child: Stack(
          children: [Icon(Icons.emoji_people_rounded), Text("ID: ${r.id}")],
        )
      );
    }).toList();
    markers.addAll(requests.map((r) {
      return Marker(
        point: r.destination,
        child: Stack(
          children: [
            Icon(Icons.square, size: 32.0, color: Colors.white),
            Icon(Icons.local_hospital_outlined, size: 32.0, color: Colors.red),
          ],
        ),
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
          
          List<String> geometries = output?.routes.map((route) => route.geometry ?? "").toList() ?? [];

          List<List<LatLng>> lines = geometries.map((geo) {
            List<LatLng> coord = PolylinePoints().decodePolyline(geo).map((e) {
              return LatLng(e.latitude, e.longitude);
            }).toList();
            return coord;
          }).toList();
          List<Polyline> polylines = lines.map((line) {
            return Polyline(
              points: line,
              strokeWidth: 2.0,
              color: Color(0xFF0000FF),
              pattern: StrokePattern.dotted(),
            );
          }).toList();

          // Update the UI with the decoded coordinates
          polylineCoordinates = polylines;
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
              PolylineLayer(polylines: polylineCoordinates),
              MarkerLayer(markers: markers),
            ],
          ),
          Positioned(
            top: 16,
            right: 16,
            child: FloatingActionButton(
              onPressed: () {
                setState(() {
                  fetchAndDecodePolyline();
                  update();
                });
              },
              child: Icon(Icons.sync),
            ),
          ),
          VehiclesWidget(),
          //LocationPickerWidget(),
        ],
      ),
    );
  }
}


