import 'package:flavorscape/models/rating.dart';

class RatingsRequest {
  final List<Rating> ratings;

  const RatingsRequest({
    required this.ratings,
  });

  List<dynamic> toJson() => ratings.map((rating) => rating.toJson()).toList();
}
