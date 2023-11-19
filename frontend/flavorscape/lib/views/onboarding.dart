import 'dart:convert';
import 'dart:developer';

import 'package:flavorscape/models/ingredient_response.dart';
import 'package:flavorscape/models/onboard_request.dart';
import 'package:flavorscape/models/recipe.dart';
import 'package:flavorscape/models/ratings_request.dart';
import 'package:flavorscape/models/result_response.dart';
import 'package:flutter/material.dart';
import 'package:flutter_card_swiper/flutter_card_swiper.dart';
import 'package:http/http.dart' as http;
import 'package:flavorscape/constants.dart' as constants;
import 'package:material_symbols_icons/symbols.dart';

import '../models/allergen_response.dart';
import '../models/rating.dart';
import '../models/recipes_response.dart';
import '../widgets/loading.dart';

class Onboarding extends StatefulWidget {
  const Onboarding({
    super.key,
    required this.onboardingDoneCallback,
  });

  final VoidCallback onboardingDoneCallback;

  @override
  State<StatefulWidget> createState() => _Onboarding();
}

enum DietType { all, veggie, vegan }

class _Onboarding extends State<Onboarding> {
  bool loading = false;
  var pageNumber = 1;
  var currentRatingRecipeIndex = 0;

  late List<Recipe> ratingRecipes;
  List<Rating> ratings = [];
  List<Widget> cards = [];
  CardSwiperController cardSwiperController = CardSwiperController();

  List<int> selectedAllergenIds = [];
  List<int> selectedIngredientsIds = [];
  DietType selectedDiet = DietType.all;

  Future<void> postOnboard() async {
    setState(() {
      loading = true;
    });
    OnboardRequest onboard = OnboardRequest(
      diet: selectedDiet.name,
      allergens: selectedAllergenIds,
      dislikes: selectedIngredientsIds,
    );
    var response =
        await http.post(Uri.http(constants.apiAddress, constants.onboardPath),
            headers: {
              'Content-Type': 'application/json',
            },
            body: jsonEncode(onboard.toJson()));
    if (response.statusCode == 200) {
      final success = ResultResponse.fromJson(
              jsonDecode(utf8.decode(response.bodyBytes))
                  as Map<String, dynamic>)
          .success;
      log("Post onboard response: $success");

      if (success) {
        getRatingRecipes();

        setState(() {
          pageNumber++;
        });
      }
    } else {
      throw Exception('OnboardCheck failed!');
    }
  }

  Future<void> getRatingRecipes() async {
    var response = await http
        .get(Uri.http(constants.apiAddress, constants.ratingRecipesPath));
    if (response.statusCode == 200) {
      setState(() {
        ratingRecipes = RecipesResponse.fromJson(
                jsonDecode(utf8.decode(response.bodyBytes)) as List<dynamic>)
            .recipes;
        cards = ratingRecipes
            .map((recipe) => getSwipeCard(recipe, context))
            .toList();
        loading = false;
      });
    } else {
      throw Exception("Fetching rating recipe failed!");
    }
  }

  Future<void> postRatings() async {
    var response =
        await http.post(Uri.http(constants.apiAddress, constants.ratingsPath),
            headers: {
              'Content-Type': 'application/json',
            },
            body: jsonEncode(RatingsRequest(ratings: ratings).toJson()));
    if (response.statusCode != 200) {
      throw Exception("Could not post ratings!");
    }
  }

  void dietSelectionChanged(double value) {
    selectedDiet = DietType.values[value.toInt()];
  }

  void allergenSelectionChanged(List<int> allergenIds) {
    selectedAllergenIds = allergenIds;
  }

  void ingredientSelectionChanged(List<int> ingredientIds) {
    selectedIngredientsIds = ingredientIds;
  }

  Widget getSwipeCard(Recipe recipe, BuildContext context) {
    return LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        double size = constraints.maxWidth < constraints.maxHeight
            ? constraints.maxWidth
            : constraints.maxHeight;

        return Stack(
          children: [
            Card(
              elevation: 8,
              clipBehavior: Clip.hardEdge,
              child: SizedBox(
                width: size,
                height: size,
                child: Image.network(
                  recipe.imgUrl,
                  fit: BoxFit.cover,
                ),
              ),
            ),
            Positioned(
              width: size - 30,
              left: 15,
              bottom: 15,
              child: Text(
                maxLines: 2,
                recipe.name,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: Colors.white,
                  shadows: [
                    const Shadow(
                      color: Colors.black,
                      offset: Offset(1.0, 1.0),
                      blurRadius: 8.0,
                    ),
                  ],
                ),
              ),
            ),
          ],
        );
      },
    );
  }

  bool swiped(oldCardIndex, newCardIndex, direction) {
    int rating;
    if (direction == CardSwiperDirection.left) {
      rating = -1;
    } else if (direction == CardSwiperDirection.top) {
      rating = 0;
    } else if (direction == CardSwiperDirection.right) {
      rating = 1;
    } else {
      throw Exception("Card swipe error!");
    }

    ratings
        .add(Rating(recipeId: ratingRecipes[oldCardIndex].id, rating: rating));
    return true;
  }

  void cardDeckEmpty() {
    postRatings();
    widget.onboardingDoneCallback();
  }

  @override
  Widget build(BuildContext context) {
    List<Widget> getWidgetList() {
      if (loading) {
        switch (pageNumber) {
          case 1:
            return [
              const Loading(text: "Submitting allergies and dislikes ...")
            ];
          case 2:
            return [const Loading(text: "Loading recipes to rate ...")];
        }
      }

      switch (pageNumber) {
        case 1:
          return <Widget>[
            DietSelection(selectionChanged: dietSelectionChanged),
            AllergenSelection(selectionChanged: allergenSelectionChanged),
            DislikeSelection(selectionChanged: ingredientSelectionChanged),
            const SizedBox(
              height: 20,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                FilledButton(
                    onPressed: () => {postOnboard()},
                    child: const Text("Next")),
              ],
            ),
          ];
        case 2:
          return <Widget>[
            Expanded(
                child: Center(
              child: CardSwiper(
                padding: const EdgeInsets.symmetric(vertical: 100, horizontal: 25),
                controller: cardSwiperController,
                allowedSwipeDirection: AllowedSwipeDirection.only(
                    left: true, right: true, up: true),
                onSwipe: (oldCardIndex, newCardIndex, direction) =>
                    swiped(oldCardIndex, newCardIndex, direction),
                onEnd: cardDeckEmpty,
                cardBuilder:
                    (context, index, percentThresholdX, percentThresholdY) =>
                        cards[index],
                cardsCount: cards.length,
                isLoop: false,
              ),
            )),
            const SizedBox(
              height: 20,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                IconButton(
                  onPressed: () {
                    setState(() {
                      cardSwiperController.swipeLeft();
                    });
                  },
                  icon: const Icon(
                    Symbols.thumb_down,
                    color: Colors.red,
                    fill: 1,
                  ),
                  iconSize: 40,
                ),
                IconButton(
                  onPressed: () {
                    setState(() {
                      cardSwiperController.swipeTop();
                    });
                  },
                  icon: const Icon(
                    Symbols.thumbs_up_down,
                    color: Colors.blue,
                    fill: 1,
                  ),
                  iconSize: 40,
                ),
                IconButton(
                  onPressed: () {
                    setState(() {
                      cardSwiperController.swipeRight();
                    });
                  },
                  icon: const Icon(
                    Symbols.thumb_up,
                    color: Colors.green,
                    fill: 1,
                  ),
                  iconSize: 40,
                ),
              ],
            ),
            const SizedBox(
              height: 20,
            ),
          ];
      }
      return [const Text("Something went wrong!")];
    }

    return Column(
      children: [
        const SizedBox(
          height: 20,
        ),
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
              " Generation ($pageNumber/2)",
              style: Theme.of(context).textTheme.titleLarge,
            ),
          ],
        ),
        const SizedBox(
          height: 20,
        ),
        ...getWidgetList(),
      ],
    );
  }
}

class DietSelection extends StatefulWidget {
  const DietSelection({super.key, required this.selectionChanged});

  final Function(double) selectionChanged;

  @override
  State<StatefulWidget> createState() => _DietSelection();
}

class _DietSelection extends State<DietSelection> {
  double _currentSliderValue = 0;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Text("Diet"),
              ],
            ),
            const SizedBox(height: 10),
            Slider(
              value: _currentSliderValue,
              max: 2,
              divisions: 2,
              onChanged: (double value) {
                setState(() {
                  _currentSliderValue = value;
                });
                widget.selectionChanged(value);
              },
            ),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 10),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(child: Text("All")),
                  Expanded(
                      child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [Text("Veggie")],
                  )),
                  Expanded(
                      child: Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [Text("Vegan")],
                  )),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}

class AllergenSelection extends StatefulWidget {
  const AllergenSelection({super.key, required this.selectionChanged});

  final Function(List<int>) selectionChanged;

  @override
  State<StatefulWidget> createState() => _AllergenSelection();
}

class _AllergenSelection extends State<AllergenSelection> {
  bool loading = true;
  late List<AllergenResponse> allergens;
  List<int> selectedAllergensIds = [];

  Future<void> getAllergens() async {
    final response =
        await http.get(Uri.http(constants.apiAddress, constants.allergensPath));
    if (response.statusCode == 200) {
      setState(() {
        allergens = (jsonDecode(response.body) as List)
            .map((allergen) => AllergenResponse.fromJson(allergen))
            .toList();
        loading = false;
      });
    } else {
      throw Exception('Fetching allergens failed!');
    }
  }

  @override
  void initState() {
    super.initState();
    getAllergens();
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return const Loading(text: "Test");
    }

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Text("Allergens"),
              ],
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8.0, // Adjust the spacing between chips
              runSpacing: 8.0, // Adjust the spacing between rows
              children: allergens.map((allergen) {
                return FilterChip(
                  iconTheme: Theme.of(context).iconTheme,
                  showCheckmark: false,
                  avatar: selectedAllergensIds.contains(allergen.id)
                      ? Icon(
                          Symbols.skull,
                          color: Theme.of(context).iconTheme.color,
                        )
                      : Icon(
                          Symbols.add,
                          color: Theme.of(context).iconTheme.color,
                        ),
                  selectedColor: const Color.fromRGBO(255, 0, 0, 0.5),
                  label: Text(allergen.name),
                  selected: selectedAllergensIds.contains(allergen.id),
                  onSelected: (bool selected) {
                    setState(() {
                      if (selected) {
                        selectedAllergensIds.add(allergen.id);
                      } else {
                        selectedAllergensIds.remove(allergen.id);
                      }
                    });
                    widget.selectionChanged(selectedAllergensIds);
                  },
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}

class DislikeSelection extends StatefulWidget {
  const DislikeSelection({super.key, required this.selectionChanged});

  final Function(List<int>) selectionChanged;

  @override
  State<StatefulWidget> createState() => _DislikeSelection();
}

class _DislikeSelection extends State<DislikeSelection> {
  bool loading = true;
  late List<IngredientResponse> ingredients;
  List<int> selectedIngredients = [];

  Future<void> getIngredients() async {
    final response = await http
        .get(Uri.http(constants.apiAddress, constants.ingredientsPath));
    if (response.statusCode == 200) {
      setState(() {
        ingredients = (jsonDecode(response.body) as List)
            .map((ingredient) => IngredientResponse.fromJson(ingredient))
            .toList();
        loading = false;
      });
    } else {
      throw Exception('Fetching ingredients failed!');
    }
  }

  @override
  void initState() {
    super.initState();
    getIngredients();
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return const Loading(text: "Test");
    }

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Text("Dislikes"),
              ],
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8.0, // Adjust the spacing between chips
              runSpacing: 8.0, // Adjust the spacing between rows
              children: ingredients.map((ingredient) {
                return FilterChip(
                  showCheckmark: false,
                  avatar: selectedIngredients.contains(ingredient.id)
                      ? Icon(
                          Symbols.thumb_down,
                          color: Theme.of(context).iconTheme.color,
                        )
                      : Icon(
                          Symbols.add,
                          color: Theme.of(context).iconTheme.color,
                        ),
                  selectedColor: const Color.fromRGBO(255, 0, 0, 0.5),
                  label: Text(ingredient.name),
                  selected: selectedIngredients.contains(ingredient.id),
                  onSelected: (bool selected) {
                    setState(() {
                      if (selected) {
                        selectedIngredients.add(ingredient.id);
                      } else {
                        selectedIngredients.remove(ingredient.id);
                      }
                    });
                    widget.selectionChanged(selectedIngredients);
                  },
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}
