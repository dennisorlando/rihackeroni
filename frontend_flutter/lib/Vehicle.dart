import 'dart:convert';

import 'package:latlong2/latlong.dart';

final List<Vehicle> testVehicles = [
  Vehicle(
      id: 0,
      startLocation: LatLng(11.142383863760358, 46.68177504064434),
      capacityWalking: 2, capacityWheelchair: 1, capacityStretcher: 1, capacityWhiteCross: 1, maxCapacity: 5),
  Vehicle(
      id: 1,
      startLocation: LatLng(10.586088739685124, 46.52801287430344),
      capacityWalking: 2, capacityWheelchair: 0, capacityStretcher: 1, capacityWhiteCross: 1, maxCapacity: 4),
  Vehicle(
      id: 2,
      startLocation: LatLng(10.546965347622773, 46.68666775159264),
      capacityWalking: 2, capacityWheelchair: 0, capacityStretcher: 1, capacityWhiteCross: 1, maxCapacity: 4),
  Vehicle(
      id: 3,
      startLocation: LatLng(11.559411986378848, 46.566069480907714),
      capacityWalking: 2, capacityWheelchair: 0, capacityStretcher: 1, capacityWhiteCross: 1, maxCapacity: 4),
  Vehicle(
      id: 4,
      startLocation: LatLng(11.247022718454986, 46.81304566387848),
      capacityWalking: 2, capacityWheelchair: 0, capacityStretcher: 0, capacityWhiteCross: 1, maxCapacity: 3),
  Vehicle(
      id: 5,
      startLocation: LatLng(11.35313114582766, 46.499820340432166),
      capacityWalking: 5, capacityWheelchair: 1, capacityStretcher: 1, capacityWhiteCross: 2, maxCapacity: 9),
];

class Vehicle {
  final int id;
  final LatLng startLocation;
  final int capacityWalking;
  final int capacityWheelchair;
  final int capacityStretcher;
  final int capacityWhiteCross;
  final int maxCapacity;


  Vehicle({
    required this.id,
    required this.startLocation,
    required this.capacityWalking,
    required this.capacityWheelchair,
    required this.capacityStretcher,
    required this.capacityWhiteCross,
    required this.maxCapacity,
  });

  factory Vehicle.fromDict(Map<String, dynamic> data) => Vehicle(
    id: data['id'] as int,
    startLocation: data['start_location'],
    capacityWalking: data['capacity_walking'] as int,
    capacityWheelchair: data['capacity_wheelchair'] as int,
    capacityStretcher: data['capacity_stretcher'] as int,
    capacityWhiteCross: data['capacity_white_cross'] as int,
    maxCapacity: data['max_capacity'] as int,
  );


  Map<String, dynamic> toDict() => {
    'id': id,
    'start_location': startLocation,
    'capacity_walking': capacityWalking,
    'capacity_wheelchair': capacityWheelchair,
    'capacity_stretcher': capacityStretcher,
    'capacity_white_cross': capacityWhiteCross,
    'max_capacity': maxCapacity,
  };

  String toJson() => json.encode(toDict());

  factory Vehicle.fromJson(String source) =>
      Vehicle.fromDict(json.decode(source) as Map<String, dynamic>);


  Map<String, dynamic> toVroomDict() => {
    "id": id,
    "start": startLocation,
    "end": startLocation,
    "capacity": [
      capacityWalking,
      capacityWheelchair,
      capacityStretcher,
      capacityWhiteCross
    ]
  };
}