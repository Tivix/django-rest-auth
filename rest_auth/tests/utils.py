from knox.models import AuthToken


def create_knox_token(token_model, user, serializer):
    token = AuthToken.objects.create(user=user)
    return token
