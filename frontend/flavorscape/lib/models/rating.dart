class Rating {
  final int recipeId;
  final int rating;

  const Rating({
    required this.recipeId,
    required this.rating,
  });

  Map<String, dynamic> toJson() => {
    'recipe_id': recipeId,
    'rating': rating,
  };
}
