

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend_flutter/VroomOutput.dart';

class VehiclesRoute extends StatefulWidget {
 VehiclesRoute({required this.route});
 final VroomRoute route;

  @override
  State<VehiclesRoute> createState() => VehiclesRouteState();
}

class VehiclesRouteState extends State<VehiclesRoute> {
  @override
  Widget build(BuildContext context) {
    return Positioned(
      bottom: 0,
      right: 0,
      child: SizedBox(
        width: 400,
        height: 800,
        child: Card(
          child: SingleChildScrollView(
            child: Column(
              children: [
                ...List.generate(widget.route.steps.length, (index) {
                  final step = widget.route.steps[index];
                  return ListTile(
                    leading: switch (step.type) {
                      "start" => Icon(Icons.directions_car),
                      "pickup" => Icon(Icons.chair),
                      "delivery" => Icon(Icons.local_hospital),
                      _ => Icon(Icons.question_mark),
                    },
                    title: Text("Patient ID: ${step.taskId ?? "N/A"}"),
                    subtitle: Text("Duration: ${step.duration}\nArrival: ${step.arrival ~/ 3600}:${step.arrival % 3600 ~/ 60}\nLoad: ${step.load![0]}"),
                  );
                })
              ],
            ),
          ),
        ),
      )
    );
  }
}

class RouteSelector extends StatefulWidget {
  RouteSelector({required this.routes});
  final List<VroomRoute> routes;

  @override
  State<RouteSelector> createState() => RouteSelectorState();
}

class RouteSelectorState extends State<RouteSelector> {
  RouteSelectorState();
  VroomRoute? route; 

  @override
  Widget build(BuildContext context) {
    final ctrl = TextEditingController();
    return Positioned(bottom: 0, right: 0, child: SizedBox(
      width: 300,
      child: Card(
        child: Column(
          children: [
            DropdownMenu<VroomRoute>(
              initialSelection: null,
              controller: null,
              requestFocusOnTap: true,
              label: const Text("Select a route"),
              onSelected: (VroomRoute? route) {
                print("Selected route: $route");
                setState(() {
                  this.route = route;
                });
              },
              dropdownMenuEntries: widget.routes.map((route) {
                return DropdownMenuEntry<VroomRoute>(
                  label: "Ambulance ${route.vehicle}",
                  value: route,
                );
              }).toList(),
            ),
            route != null ? VehiclesRoute(route: route!) : Placeholder(),
          ]
        )
      )
    ));
  }
}
