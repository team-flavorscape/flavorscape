class IngredientResponse {
  final int id;
  final String name;

  const IngredientResponse({
    required this.id,
    required this.name,
  });

  factory IngredientResponse.fromJson(Map<String, dynamic> json) {
    return IngredientResponse(
      id: json['id'] as int,
      name: json['name'] as String,
    );
  }
}
