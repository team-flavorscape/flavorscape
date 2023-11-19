class OnboardRequest {
  final String diet;
  final List<int> allergens;
  final List<int> dislikes;

  const OnboardRequest({
    required this.diet,
    required this.allergens,
    required this.dislikes,
  });

  Map<String, dynamic> toJson() => {
    'diet': diet,
    'allergens': allergens,
    'dislikes': dislikes,
  };
}
