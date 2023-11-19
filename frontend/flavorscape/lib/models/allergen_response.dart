class AllergenResponse {
  final int id;
  final String name;

  const AllergenResponse({
    required this.id,
    required this.name,
  });

  factory AllergenResponse.fromJson(Map<String, dynamic> json) {
    return AllergenResponse(
      id: json['id'] as int,
      name: json['name'] as String,
    );
  }
}
