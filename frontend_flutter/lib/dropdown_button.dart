import 'package:flutter/material.dart';
import 'package:frontend_flutter/VehiclesWidget.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<Map<String, dynamic>> fetchNominatimData(String query) async {
  final url = Uri.parse('https://nominatim.openstreetmap.org/search?q=$query&format=json');

  try {
    final response = await http.get(url);

    // Check if the request was successful (status code 200)
    if (response.statusCode == 200) {
      // Parse the JSON response
      List<dynamic> data = jsonDecode(response.body);

      // If there are results, return the first one as a map (JSON-like structure)
      if (data.isNotEmpty) {
        return data[0];  // Return the first result
      } else {
        return {};  // Return an empty map if no results
      }
    } else {
      throw Exception('Failed to fetch data: ${response.statusCode}');
    }
  } catch (e) {
    // Handle any errors (e.g., network issues)
    print('Error: $e');
    return {};
  }
}

class LocationPickerWidget extends StatefulWidget {
  const LocationPickerWidget({super.key});

  @override
  State<LocationPickerWidget> createState() => _LocationPickerWidgetState();
}

class _LocationPickerWidgetState extends State<LocationPickerWidget> {
  String? location1;
  String? location2;
  Map<String, dynamic>? location1Coords;
  Map<String, dynamic>? location2Coords;


  @override
  Widget build(BuildContext context) {

    final TextEditingController ambulanceid = TextEditingController();
    final TextEditingController place1 = TextEditingController();
    final TextEditingController place2 = TextEditingController();

    return Positioned(
      bottom: 0,
      right: 0,
      child: SizedBox(
        width: 300,
        height: 400,
        child: Card(
          child: Padding(padding: EdgeInsets.all(16.0), child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: ambulanceid,
              ),
              const SizedBox(height: 16),
              TextField(
                controller: place1,
              ),
              const SizedBox(height: 16),
              TextField(
                controller: place2,
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () async {
                  var start = await fetchNominatimData(place1.text);
                  var end = await fetchNominatimData(place2.text);
                  print(start['display_name']);
                  print(end['display_name']);
                  print(ambulanceid.text);
                },
                child: const Text('Done'),
              ),
            ],
          ),)
        ),
      ),
    );
  }
}