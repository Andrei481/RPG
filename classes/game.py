import random


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, hp, mp, atk, df, magic, healing):
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk_low = atk - 10
        self.atk_high = atk + 10
        self.df = df
        self.magic = magic
        self.healing = healing
        self.actions = ["Attack", "Magic", "Healing"]

    def generate_damage(self):
        return random.randrange(self.atk_low, self.atk_high)

    def generate_magic_damage(self, spell_index):
        magic_atk_low = self.magic[spell_index]["DMG"] - 10
        magic_atk_high = self.magic[spell_index]["DMG"] + 10
        return random.randrange(magic_atk_low, magic_atk_high)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    def heal_damage(self, dmg):
        self.hp += dmg
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, spell_index):
        self.mp -= self.magic[spell_index]["Cost"]

    def restore_mp(self):
        self.mp += 20
        if self.mp > self.max_mp:
            self.mp = self.max_mp

    def get_spell_name(self, spell_index):
        return self.magic[spell_index]["Name"]

    def get_spell_cost(self, spell_index):
        return self.magic[spell_index]["Cost"]

    def get_spell_damage(self, spell_index):
        return self.magic[spell_index]["DMG"]

    def get_potion_name(self, potion_index):
        return self.healing[potion_index]["Name"]

    def get_potion_effect(self, potion_index):
        return self.healing[potion_index]["Restore"]

    def get_potion_quantity(self, potion_index):
        return self.healing[potion_index]["Quantity"]

    def consume_potion(self, potion_index):
        self.healing[potion_index]["Quantity"] -= 1

    def choose_action(self):
        action_index = 1
        print(BColors.OKBLUE + BColors.BOLD + "Actions" + BColors.ENDC)
        for action in self.actions:
            print(str(action_index) + ":", action)
            action_index += 1

    def choose_magic(self):
        spell_index = 1
        print(BColors.OKBLUE + BColors.BOLD + "Spells" + BColors.ENDC)
        for spell in self.magic:
            print(str(spell_index) + ":", spell["Name"], "(cost:", str(spell["Cost"]) + ")")
            spell_index += 1

    def choose_healing(self):
        potion_index = 1
        print(BColors.OKBLUE + BColors.BOLD + "Potions" + BColors.ENDC)
        for potion in self.healing:
            restore = str(potion["Restore"])
            qty = str(potion["Quantity"])
            print(str(potion_index) + ":", potion["Name"], "(Restores", restore + ")", "Quantity:", qty)
            potion_index += 1
