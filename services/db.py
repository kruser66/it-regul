from app.models import TgUser


def get_user(telegram_id: int) -> TgUser | None:

    user = TgUser.objects.filter(telegram_id=telegram_id)

    return user.first() if user else None


def update_or_create_user(telegram_id: int, **kwargs) -> None:

    user, _ = TgUser.objects.update_or_create(telegram_id=telegram_id, defaults=kwargs)

    return user
