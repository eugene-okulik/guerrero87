import faker
import random

fake = faker.Faker()
possible_sizes = ['small', 'medium', 'big']


def create_fake_data():
    fake_size = random.choice(possible_sizes)
    fake_color = fake.color_name()
    fake_name = fake.name()

    return {
        "name": fake_name,
        "data": {
            "color": fake_color,
            "size": fake_size
        }
    }
