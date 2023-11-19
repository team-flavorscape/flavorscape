class Recipe {
  final int id;
  final String name;
  final String imgUrl;
  final List<String> ingredients;
  final List<String> allergens;

  const Recipe({
    required this.id,
    required this.name,
    required this.imgUrl,
    required this.ingredients,
    required this.allergens,
  });

  factory Recipe.fromJson(Map<String, dynamic> json) {
    return Recipe(
      id: json['id'] as int,
      name: json['name'] as String,
      imgUrl: json['img_url'] as String,
      ingredients: (json['ingredients'] as List).map((ingredient) => ingredient as String).toList(),
      allergens: (json['allergens'] as List).map((allergen) => allergen as String).toList(),
    );
  }
}
