import 'dart:math';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:frontend_flutter/Vehicle.dart';

class VehiclesWidget extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => VehiclesWidgetState();

}

class VehiclesWidgetState extends State<VehiclesWidget> {

  late List<Vehicle> vehicles = testVehicles;
  late List<bool> viewed = List.generate(testVehicles.length, (index) => true);


  @override
  Widget build(BuildContext context) {
    return SizedBox(
        width: 200,
        child: Card(
          child: Column(
            children: [
              ...List.generate(vehicles.length, (index) {
                return ListTile(
                  leading: Icon(Icons.car_crash),
                  title: Text("ID: ${vehicles[index].id}"),
                  trailing: Checkbox(value: viewed[index], onChanged: (bool? value) {
                    setState(() {
                      viewed[index] = !viewed[index];
                    });
                    },),
                );
              })
            ],
          ),
        ),
    );
  }
}