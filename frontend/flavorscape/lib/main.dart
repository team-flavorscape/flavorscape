import 'dart:convert';

import 'package:flavorscape/constants.dart' as constants;
import 'package:flavorscape/views/meal_planner.dart';
import 'package:flavorscape/views/onboarding.dart';
import 'package:flavorscape/widgets/loading.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'models/onboard_check.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'flavorscape',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.green, brightness: Brightness.light),
        useMaterial3: true,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool isOnboarded = false;
  var loading = true;


  Future<void> fetchIsOnboarded() async {
    final response = await http
        .get(Uri.http(constants.apiAddress, constants.onboardCheckPath));
    if (response.statusCode == 200) {
      setState(() {
        isOnboarded = OnboardCheck.fromJson(
                jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>)
            .isOnboarded;
        loading = false;
      });
    } else {
      throw Exception('OnboardCheck failed!');
    }
  }

  void onboardingDoneCallback() {
    setState(() {
      isOnboarded = true;
    });
  }

  Widget getWidget() {
    if (loading) {
      return const Loading(text: "Connecting to server ...");
    } else {
      if (isOnboarded) {
        return const MealPlanner();
      } else {
        return Onboarding(onboardingDoneCallback: onboardingDoneCallback,);
      }
    }
  }

  @override
  void initState() {
    super.initState();
    fetchIsOnboarded();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Center(
      child: SafeArea(
        child: Padding(
            padding: const EdgeInsets.all(10),
            child: Container(
              constraints: const BoxConstraints(maxWidth: 800),
              child: getWidget(),
            )),
      ),
    ) // This trailing comma makes auto-formatting nicer for build methods.
        );
  }
}
