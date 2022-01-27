from rest_framework import serializers

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title', )

    def validate_score(self, value):
        if not isinstance(value, int) or value not in range(1, 11):
            raise serializers.ValidationError(
                'Оценка должна быть целым числом в диапазоне от 1 до 10'
            )
        return value

    def validate(self, params):
        review = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id'))
        if review.exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв к этому произведению')
        return params


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
