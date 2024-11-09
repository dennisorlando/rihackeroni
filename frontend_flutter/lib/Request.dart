class Request {
  final String id;
  final bool accompanied;
  final String pickupLocation;
  final String destination;
  final DateTime appointmentTime;

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
      pickupLocation: json['pickup_location'],
      destination: json['destination'],
      appointmentTime: DateTime.parse(json['appointment_time']),
    );
  }

  // Method to convert an instance to a JSON map
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'accompanied': accompanied,
      'pickup_location': pickupLocation,
      'destination': destination,
      'appointment_time': appointmentTime.toIso8601String(),
    };
  }
}
