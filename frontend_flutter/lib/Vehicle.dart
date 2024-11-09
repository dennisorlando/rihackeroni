import 'dart:convert';
import 'package:latlong2/latlong.dart';


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
    startLocation: LatLng(data['start_location'][1], data['start_location'][0]),
    capacityWalking: data['capacity_walking'] as int,
    capacityWheelchair: data['capacity_wheelchair'] as int,
    capacityStretcher: data['capacity_stretcher'] as int,
    capacityWhiteCross: data['capacity_white_cross'] as int,
    maxCapacity: data['max_capacity'] as int,
  );


  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'start_location': [startLocation.longitude, startLocation.latitude],
      'capacity_walking': capacityWalking,
      'capacity_wheelchair': capacityWheelchair,
      'capacity_stretcher': capacityStretcher,
      'capacity_white_cross': capacityWhiteCross,
      'max_capacity': maxCapacity,
    };
  }

}
