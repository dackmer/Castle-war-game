# card_system.py
import random

# Card rarity constants
CARD_RARITY = {
    "LEGENDARY": 1.6,
    "EPIC": 3.0,
    "RARE": 10.0,
    "COMMON": 42.37,
    "NONE": 42.37
}

# Special cards and their effects
SPECIAL_CARDS = {
    "Counter Shield": "Blocks next attack and reflects 50% of damage.",
    "Steal Card": "Randomly steal one opponent's card.",
    "Double Draw": "Draw 2 random cards on your next turn.",
    "Rebirth Card": "Revive with 10 hearts if health reaches 0 (one-time use).",
    "Lucky Charm": "Temporarily increases chances to get a better rarity card.",
    "Trap Card": "If attacked, enemy loses 10 hearts and has 20% less damage for 2 turns.",
    "Heal Card": "Heal 10 hearts or 5 per turn if below 20 hearts.",
    "Population Card": "Add 20 population or store extra.",
    "Attack Boost Card": "+30 damage to next attack."
}


class Card:
    def __init__(self, name, rarity, description, effect_function=None):
        self.name = name
        self.rarity = rarity  # LEGENDARY, EPIC, RARE, COMMON
        self.description = description
        self.effect_function = effect_function
        self.is_active = False
        self.duration = 0  # For cards with duration effects

    def use(self, player, opponent=None):
        """Apply the card effect"""
        if self.effect_function:
            return self.effect_function(player, opponent)
        return False

    def __str__(self):
        return f"{self.name} ({self.rarity}): {self.description}"


class CardSystem:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.setup_special_cards()

    def setup_special_cards(self):
        """Define special cards and their effects"""
        self.special_cards = {
            "Counter Shield": Card("Counter Shield", "LEGENDARY",
                                   "Blocks next attack and reflects 50% of damage.",
                                   self.effect_counter_shield),
            "Steal Card": Card("Steal Card", "EPIC",
                               "Randomly steal one opponent's card.",
                               self.effect_steal_card),
            "Double Draw": Card("Double Draw", "RARE",
                                "Draw 2 random cards on your next turn.",
                                self.effect_double_draw),
            "Rebirth Card": Card("Rebirth Card", "LEGENDARY",
                                 "Revive with 10 hearts if health reaches 0 (one-time use).",
                                 self.effect_rebirth),
            "Lucky Charm": Card("Lucky Charm", "EPIC",
                                "Temporarily increases chances to get a better rarity card.",
                                self.effect_lucky_charm),
            "Trap Card": Card("Trap Card", "RARE",
                              "If attacked, enemy loses 10 hearts and has 20% less damage for 2 turns.",
                              self.effect_trap_card),
            "Heal Card": Card("Heal Card", "COMMON",
                              "Heal 10 hearts or 5 per turn if below 20 hearts.",
                              self.effect_heal),
            "Population Card": Card("Population Card", "COMMON",
                                    "Add 20 population or store extra.",
                                    self.effect_population),
            "Attack Boost Card": Card("Attack Boost Card", "RARE",
                                      "+30 damage to next attack.",
                                      self.effect_attack_boost)
        }

    def get_random_rarity(self, lucky_boost=0):
        """Determine the rarity of a card based on probabilities"""
        roll = random.random() * 100

        # Apply lucky charm boost if active
        if lucky_boost > 0:
            # Increase chances for better cards
            roll = max(0, roll - (lucky_boost * 10))

        if roll < CARD_RARITY["LEGENDARY"]:
            return "LEGENDARY"
        elif roll < CARD_RARITY["LEGENDARY"] + CARD_RARITY["EPIC"]:
            return "EPIC"
        elif roll < CARD_RARITY["LEGENDARY"] + CARD_RARITY["EPIC"] + CARD_RARITY["RARE"]:
            return "RARE"
        elif roll < CARD_RARITY["LEGENDARY"] + CARD_RARITY["EPIC"] + CARD_RARITY["RARE"] + CARD_RARITY["COMMON"]:
            return "COMMON"
        else:
            return "NONE"

    def get_random_card_by_rarity(self, rarity):
        """Get a random card of the specified rarity"""
        if rarity == "NONE":
            return None

        # Filter cards by rarity
        cards_of_rarity = [card for card in self.special_cards.values() if card.rarity == rarity]

        if cards_of_rarity:
            return random.choice(cards_of_rarity)
        return None

    def check_battle_chest(self, player):
        """10% chance at start of turn to draw a special card"""
        if random.random() < 0.1:  # 10% chance
            # First determine rarity
            rarity = self.get_random_rarity(player.lucky_boost if hasattr(player, "lucky_boost") else 0)

            if rarity != "NONE":
                # Get a random card of that rarity
                new_card = self.get_random_card_by_rarity(rarity)
                if new_card:
                    # Create a copy of the card to give to the player
                    card_copy = Card(new_card.name, new_card.rarity, new_card.description, new_card.effect_function)
                    return card_copy
        return None

    def check_endangered_mode(self, player):
        """If hearts < 10, automatically get a random special card"""
        if player.hearts < 10:
            # Get a random special card (not based on rarity)
            card_name = random.choice(list(self.special_cards.keys()))
            card = self.special_cards[card_name]

            # Create a copy of the card to give to the player
            card_copy = Card(card.name, card.rarity, card.description, card.effect_function)
            return card_copy
        return None

    # Card effect implementations
    def effect_counter_shield(self, player, opponent):
        player.has_counter_shield = True
        return True

    def effect_steal_card(self, player, opponent):
        if opponent.cards and len(opponent.cards) > 0:
            stolen_card = random.choice(opponent.cards)
            opponent.cards.remove(stolen_card)
            player.cards.append(stolen_card)
            return True
        return False

    def effect_double_draw(self, player, opponent):
        player.double_draw = True
        return True

    def effect_rebirth(self, player, opponent):
        player.has_rebirth = True
        return True

    def effect_lucky_charm(self, player, opponent):
        if not hasattr(player, "lucky_boost"):
            player.lucky_boost = 0
        player.lucky_boost += 1
        return True

    def effect_trap_card(self, player, opponent):
        player.has_trap = True
        player.trap_duration = 2
        return True

    def effect_heal(self, player, opponent):
        if player.hearts < 20:
            healing = min(10, 20 - player.hearts)
            player.hearts += healing
            return True
        return False

    def effect_population(self, player, opponent):
        player.population += 20
        return True

    def effect_attack_boost(self, player, opponent):
        player.damage_bonus += 30
        return True