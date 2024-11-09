import 'dart:math';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:frontend_flutter/Vehicle.dart';

import 'main.dart';

class VehiclesWidget extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => VehiclesWidgetState();

}

class VehiclesWidgetState extends State<VehiclesWidget> {

  final List<bool> viewed = List.generate(vehicles.length, (index) => true);

  @override
  Widget build(BuildContext context) {

    return SizedBox(
        width: 200,
        child: Card(
          child: SingleChildScrollView(
            child: Column(
              children: [
                ...List.generate(vehicles.length, (index) {
                  return ListTile(
                    leading: Icon(Icons.car_crash),
                    title: Text("ID: ${vehicles[index].id}"),
                    trailing: Checkbox(value: viewed[index], onChanged: (bool? value) {
                      setState(() {
                        viewed[index] = !viewed[index];
                        rendered_polylines = routes.entries.where((v) => viewed[v.key]).map((r) {
                          return r.value.geometry;
                        }).toList();
                        homepage.setState(() {

                        });
                      });
                    },
                      activeColor: vehicle_colors[index],
                    ),
                  );
                }),
              ],
            ),
          ),
        ),
    );
  }
}