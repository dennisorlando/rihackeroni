import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:frontend_flutter/Vehicle.dart';

class Vehicles extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: testVehicles.length,
      itemBuilder: (context, index) {
        return Card(
          child: ListTile(
          leading: Icon(Icons.car_crash),
          title: Text("${testVehicles[index].id}"),
        ),);
      },
    );
  }
}