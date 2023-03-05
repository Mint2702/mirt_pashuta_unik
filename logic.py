import uuid
import requests
from typing import List

from models import User
from settings import settings
from db_connection import get_session


def create_profile_description(
    user_facts: str, sex: str, user_description: str, fio: str
) -> str:
    promt = generate_prompt_for_profile_description(
        user_facts=user_facts, user_description=user_description, sex=sex, fio=fio
    )

    messages = [
        {"role": "system", "content": "Вы придумываете профили для социальных сетей"},
        {"role": "user", "content": promt},
    ]

    result = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json={"messages": messages, "model": "gpt-3.5-turbo", "temperature": 0.9},
        headers={"Authorization": f"Bearer {settings.openai_api_key}"},
    )
    if result.status_code not in [200, 201]:
        print(result.json())
        raise Exception
    else:
        result = result.json()

    return result["choices"][0]["message"]["content"]


def generate_prompt_for_profile_description(
    user_facts: str, sex: str, user_description: str, fio: str
) -> str:
    return f"""
ФИО: {fio}
Внешность: {user_description}
Пол: {sex}
Факты о человеке: {user_facts}
Описание профиля:"""


def create_image(promt: str, sex: str) -> str:
    base_promt = f"Реалистичная картинка человека в стиле bitmoji: пол = {sex}, дополнительное описание: "
    result = requests.post(
        "https://api.openai.com/v1/images/generations",
        json={"prompt": base_promt + promt, "n": 1, "size": "256x256"},
        headers={"Authorization": f"Bearer {settings.openai_api_key}"},
    )
    if result.status_code not in [200, 201]:
        print(result.json())
        raise Exception
    else:
        result = result.json()

    return result["data"][0]["url"]


def add_user(
    fio: str,
    user_description: str,
    user_facts: str,
    photo_url: str,
    profile_description: str,
) -> User:
    with get_session() as session:
        id = uuid.uuid4().hex
        user = User(
            id=id,
            fio=fio,
            photo_url=photo_url,
            user_description=user_description,
            user_facts=user_facts,
            profile_description=profile_description,
        )

        user.create(session=session)

        return user


def get_all_users() -> List[User]:
    with get_session() as session:
        users = session.query(User).all()
        return users
