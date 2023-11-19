class ResultResponse {
  final bool success;

  const ResultResponse({
    required this.success,
  });

  factory ResultResponse.fromJson(Map<String, dynamic> json) {
    return ResultResponse(success: json['success']);
  }
}
