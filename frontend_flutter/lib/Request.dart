import 'dart:ffi';

import 'package:latlong2/latlong.dart';

class Request {
  final int id;
  final bool accompanied;
  final LatLng pickupLocation;
  final LatLng destination;
  final int appointmentTime;

  Request({
    required this.id,
    required this.accompanied,
    required this.pickupLocation,
    required this.destination,
    required this.appointmentTime,
  });

  // Factory constructor to create an instance from a JSON map
  factory Request.fromJson(Map<String, dynamic> json) {
    return Request(
      id: json['id'],
      accompanied: json['accompanied'],
      pickupLocation: LatLng(json['pickup_location'][0], json['pickup_location'][1]),
      destination: LatLng(json['destination'][0], json['destination'][1]),
      appointmentTime: json['appointment_time'],
    );
  }

  // Method to convert an instance to a JSON map
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'accompanied': accompanied,
      'pickup_location': pickupLocation,
      'destination': destination,
      'appointment_time': appointmentTime,
    };
  }
}
