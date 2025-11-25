class Flower:
    def __init__(self, name, stem_length, cost, freshness_days, color):
        self.name = name
        self.stem_length = stem_length
        self.cost = cost
        self.freshness_days = freshness_days
        self.color = color

    def __str__(self):
        return (f"{self.name} ({self.color}), {self.stem_length}см, "
                f" {self.cost}руб.")


class Rose(Flower):
    def __init__(self, color, stem_length, cost):
        super().__init__("Роза", stem_length, cost, 7, color)


class Tulip(Flower):
    def __init__(self, color, stem_length, cost):
        super().__init__("Тюльпан", stem_length, cost, 5, color)


class Lily(Flower):
    def __init__(self, color, stem_length, cost):
        super().__init__("Лилия", stem_length, cost, 10, color)


class Bouquet:
    def __init__(self):
        self.flowers = []

    def add_flower(self, flower):
        self.flowers.append(flower)

    def get_cost(self):
        return sum(flower.cost for flower in self.flowers)

    def get_wilting_time(self):
        return round(sum(f.freshness_days for f in self.flowers) / len(
            self.flowers)) if self.flowers else 0

    def sort_by(self, param, reverse=False):
        self.flowers.sort(key=lambda f: getattr(f, param), reverse=reverse)

    def find_by_freshness(self, min_days, max_days):
        return [f for f in self.flowers if
                min_days <= f.freshness_days <= max_days]

    def __str__(self):
        if not self.flowers:
            return "Букет пуст"
        flower_list = "\n".join(f"  - {f}" for f in self.flowers)
        return (f"Букет ({len(self.flowers)} цветов):\n{flower_list}\n "
                f"Стоимость: {self.get_cost()} руб.")


# Создаем цветы
rose1 = Rose("красный", 50, 15)
rose2 = Rose("белый", 40, 12)
tulip1 = Tulip("желтый", 30, 7)
lily1 = Lily("белый", 60, 20)

# Собираем букет
bouquet = Bouquet()
for flower in [rose1, tulip1, lily1, rose2]:
    bouquet.add_flower(flower)

print("=== БУКЕТ ===")
print(bouquet)
print(f"Время увядания: {bouquet.get_wilting_time():.1f} дней\n")

print("=== СОРТИРОВКА ===")
print("По стоимости:")
bouquet.sort_by("cost")
print(bouquet)

print("\nПо длине стебля:")
bouquet.sort_by("stem_length", reverse=True)
print(bouquet)

print("\n=== ПОИСК ===")
print("Цветы живущие 6+ дней:")
for flower in bouquet.find_by_freshness(6, 10):
    print(f"  - {flower.name} ({flower.freshness_days} дней)")
