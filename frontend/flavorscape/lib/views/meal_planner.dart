import 'dart:convert';
import 'dart:developer';

import 'package:flavorscape/widgets/loading.dart';
import 'package:flutter/material.dart';
import 'package:flutter_card_swiper/flutter_card_swiper.dart';
import 'package:flavorscape/constants.dart' as constants;
import 'package:http/http.dart' as http;
import 'package:material_symbols_icons/symbols.dart';

import '../models/recipe.dart';
import '../models/recipes_response.dart';

class MealPlanner extends StatefulWidget {
  const MealPlanner({super.key});

  @override
  State<StatefulWidget> createState() => _MealPlanner();
}

class _MealPlanner extends State<MealPlanner> {
  bool loading = true;
  List<List<Widget>> cards = [];

  Future<void> fetchRecommendedRecipes() async {
    var response = await http.get(Uri.http(
        constants.apiAddress, constants.recommendedRecipes, {'count': '10'}));
    if (response.statusCode == 200) {
      setState(() {
        List<Recipe> recipes = RecipesResponse.fromJson(
                jsonDecode(utf8.decode(response.bodyBytes)) as List<dynamic>)
            .recipes;

        for (int i = 0; i < recipes.length; i += 2) {
          List<Widget> pair = recipes
              .skip(i)
              .take(2)
              .map((recipe) => getSwipeCard(recipe, context))
              .toList();
          cards.add(pair);
        }

        loading = false;
      });
    } else {
      throw Exception("Fetching recommended recipes failed!");
    }
  }

  Future<void> fetchRecommendedRecipeAndReplace(
      int mealIndex, int cardIndex) async {
    var response = await http.get(Uri.http(
        constants.apiAddress, constants.recommendedRecipes, {'count': '1'}));
    if (response.statusCode == 200) {
      setState(() {
        cards[mealIndex][cardIndex] = getSwipeCard(
            RecipesResponse.fromJson(jsonDecode(utf8.decode(response.bodyBytes))
                    as List<dynamic>)
                .recipes
                .first,
            context);
      });
    } else {
      throw Exception("Fetching recommended recipes failed!");
    }
  }

  bool swiped(oldCardIndex, newCardIndex, direction, mealIndex) {
    fetchRecommendedRecipeAndReplace(mealIndex, oldCardIndex);
    return true;
  }

  @override
  void initState() {
    super.initState();
    fetchRecommendedRecipes();
  }

  Widget getSwipeCard(Recipe recipe, BuildContext context) {
    return LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
      return Stack(
        children: [
          Positioned.fill(
            child: Card(
              elevation: 8,
              clipBehavior: Clip.hardEdge,
              child: Image.network(
                recipe.imgUrl,
                fit: BoxFit.cover,
              ),
            ),
          ),
          Positioned(
            left: 15,
            bottom: 15,
            width: constraints.maxWidth - 30,
            child: Text(
              recipe.name,
              maxLines: 2,
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                color: Colors.white,
                shadows: [
                  const Shadow(
                    color: Colors.black,
                    offset: Offset(1.0, 1.0),
                    blurRadius: 8.0,
                  ),
                  const Shadow(
                    color: Colors.black,
                    offset: Offset(1.0, 1.0),
                    blurRadius: 20.0,
                  ),
                ],
              ),
            ),
          ),
        ],
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return const Loading(text: "Fetching recipe recommendations...");
    }

    return Column(
      children: [
        const SizedBox(height: 10),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              "flavorscape",
              style: Theme.of(context)
                  .textTheme
                  .titleLarge
                  ?.copyWith(fontFamily: "DMMono", fontWeight: FontWeight.bold),
            ),
            Text(
              " Weekly Plan",
              style: Theme.of(context).textTheme.titleLarge,
            ),
          ],
        ),
        const SizedBox(height: 10),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: List<Widget>.generate(
              cards.length,
              (mealIndex) => Expanded(
                child: CardSwiper(
                    padding: const EdgeInsets.all(4),
                    backCardOffset: const Offset(0, 12),
                    allowedSwipeDirection:
                        AllowedSwipeDirection.only(left: true, right: true),
                    onSwipe: (oldCardIndex, newCardIndex, direction) => swiped(
                        oldCardIndex, newCardIndex, direction, mealIndex),
                    cardBuilder: (context, index2, percentThresholdX,
                            percentThresholdY) =>
                        cards[mealIndex][index2],
                    cardsCount: cards[mealIndex].length),
              ),
            ),
          ),
        ),
        const SizedBox(height: 20),
        OutlinedButton(
          onPressed: () => {},
          child: const Row(
            mainAxisSize: MainAxisSize.min,
            children: [Icon(Symbols.shopping_bag), Text("Order Now")],
          ),
        ),
      ],
    );
  }
}
