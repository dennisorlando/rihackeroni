import 'dart:convert';
import 'dart:math';
import 'dart:ui';

import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_polyline_points/flutter_polyline_points.dart';
import 'package:latlong2/latlong.dart';

Polyline fromString(String s){
  var points = PolylinePoints().decodePolyline(s);
  List<LatLng> yay = points.map((p) => LatLng(p.latitude, p.longitude)).toList();
  return Polyline(
      points: yay,
      strokeWidth: 5.0,
      color: Color((Random().nextDouble() * 0xFFFFFFFF).toInt())
  );
}

class VroomRoute {
  int vehicle;
  List<Step> steps;
  int cost;
  int setup;
  int service;
  int duration;
  int waitingTime;
  int priority;
  List<Violation>? violations;
  List<int>? delivery;
  List<int>? pickup;
  String? description;
  Polyline geometry;
  int? distance;

  VroomRoute({
    required this.vehicle,
    required this.steps,
    required this.cost,
    required this.setup,
    required this.service,
    required this.duration,
    required this.waitingTime,
    required this.priority,
    this.violations,
    this.delivery,
    this.pickup,
    this.description,
    required this.geometry,
    this.distance,
  });

  // Factory constructor for creating a new Route instance from a map (JSON)
  factory VroomRoute.fromJson(Map<String, dynamic> json) {

    print("uh?");
    print(jsonEncode(json));
    print("aaaaaaa");
    Polyline geo = fromString(json['geometry']);

    return VroomRoute(
      vehicle: json['vehicle'] as int,
      steps: (json['steps'] as List).map((e) => Step.fromJson(e)).toList(),
      cost: json['cost'] as int,
      setup: json['setup'] as int,
      service: json['service'] as int,
      duration: json['duration'] as int,
      waitingTime: json['waiting_time'] as int,
      priority: json['priority'] as int,
      violations: json['violations'] != null
          ? (json['violations'] as List).map((v) => Violation.fromJson(v)).toList()
          : null,
      delivery: json['delivery'] != null ? List<int>.from(json['delivery']) : null,
      pickup: json['pickup'] != null ? List<int>.from(json['pickup']) : null,
      description: json['description'] as String?,
      geometry:  geo,
      distance: json['distance'] as int?,
    );
  }

  // Method to convert the Route instance back into a map (JSON)
  Map<String, dynamic> toJson() {
    return {
      'vehicle': vehicle,
      'steps': steps.map((e) => e.toJson()).toList(),
      'cost': cost,
      'setup': setup,
      'service': service,
      'duration': duration,
      'waiting_time': waitingTime,
      'priority': priority,
      'violations': violations?.map((v) => v.toJson()).toList(),
      'delivery': delivery,
      'pickup': pickup,
      'description': description,
      'geometry': geometry,
      'distance': distance,
    };
  }
}

class Step {
  String type;
  int arrival;
  int duration;
  int setup;
  int service;
  int waitingTime;
  List<Violation>? violations;
  String? description;
  List<double>? location;
  int? locationIndex;
  int? taskId;
  List<int>? load;
  int? distance;

  Step({
    required this.type,
    required this.arrival,
    required this.duration,
    required this.setup,
    required this.service,
    required this.waitingTime,
    this.violations,
    this.description,
    this.location,
    this.locationIndex,
    this.taskId,
    this.load,
    this.distance,
  });

  // Factory constructor for creating a new Step instance from a map (JSON)
  factory Step.fromJson(Map<String, dynamic> json) {
    return Step(
      type: json['type'] as String,
      arrival: json['arrival'] as int,
      duration: json['duration'] as int,
      setup: json['setup'] as int,
      service: json['service'] as int,
      waitingTime: json['waiting_time'] as int,
      violations: json['violations'] != null
          ? (json['violations'] as List).map((v) => Violation.fromJson(v)).toList()
          : null,
      description: json['description'] as String?,
      location: json['location'] != null
          ? List<double>.from(json['location'].map((loc) => loc as double))
          : null,
      locationIndex: json['location_index'] as int?,
      taskId: json['task_id'] as int?,
      load: json['load'] != null ? List<int>.from(json['load']) : null,
      distance: json['distance'] as int?,
    );
  }

  // Method to convert the Step instance back into a map (JSON)
  Map<String, dynamic> toJson() {
    return {
      'type': type,
      'arrival': arrival,
      'duration': duration,
      'setup': setup,
      'service': service,
      'waiting_time': waitingTime,
      'violations': violations?.map((v) => v.toJson()).toList(),
      'description': description,
      'location': location,
      'location_index': locationIndex,
      'task_id': taskId,
      'load': load,
      'distance': distance,
    };
  }
}

class Violation {
  String cause;
  int? duration;

  Violation({
    required this.cause,
    this.duration,
  });

  // Factory constructor for creating a new Violation instance from a map (JSON)
  factory Violation.fromJson(Map<String, dynamic> json) {
    return Violation(
      cause: json['cause'] as String,
      duration: json['duration'] as int?,
    );
  }

  // Method to convert the Violation instance back into a map (JSON)
  Map<String, dynamic> toJson() {
    return {
      'cause': cause,
      'duration': duration,
    };
  }
}

class VroomOutput {
  List<VroomRoute> routes;

  VroomOutput({
    required this.routes,
  });

  factory VroomOutput.fromJson(Map<String, dynamic> json) {
    var routesJson = json['routes'] as List;
    List<VroomRoute> routesList = routesJson.map((i) => VroomRoute.fromJson(i)).toList();

    return VroomOutput(routes: routesList);
  }

  // Method to convert the VroomOutput instance back into a map (JSON)
  Map<String, dynamic> toJson() {
    return {
      'routes': routes.map((route) => route.toJson()).toList(),
    };
  }
}
