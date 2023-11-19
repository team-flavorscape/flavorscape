import 'dart:convert';
import 'dart:developer';

import 'package:flavorscape/models/recipe.dart';

class RecipesResponse {
  final List<Recipe> recipes;

  const RecipesResponse({
    required this.recipes
  });

  factory RecipesResponse.fromJson(List<dynamic> json) {
    return RecipesResponse(
        recipes: json.map((recipe) =>
            Recipe.fromJson(recipe)).toList(),
    );
  }
}
