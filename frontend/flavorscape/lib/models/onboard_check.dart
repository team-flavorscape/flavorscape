class OnboardCheck {
  final bool isOnboarded;

  const OnboardCheck({
    required this.isOnboarded,
  });

  factory OnboardCheck.fromJson(Map<String, dynamic> json) {
    return OnboardCheck(
      isOnboarded: json['isOnboarded'] as bool,
    );
  }
}
