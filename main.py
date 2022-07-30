from classes.game import Person, BColors

magic = [{"Name": "Flames", "Cost": 50, "DMG": 80},
         {"Name": "Blizzard", "Cost": 60, "DMG": 90},
         {"Name": "Sparks", "Cost": 40, "DMG": 70},
         {"Name": "Fireball", "Cost": 70, "DMG": 100},
         {"Name": "Thunderbolt", "Cost": 80, "DMG": 110}]

healing_potions = [{"Name": "Potion of Minor Healing", "Restore": 25, "Quantity": 5},
                   {"Name": "Potion of Healing", "Restore": 50, "Quantity": 4},
                   {"Name": "Potion of Plentiful Healing", "Restore": 75, "Quantity": 2},
                   {"Name": "Potion of Vigorous Healing", "Restore": 100, "Quantity": 2},
                   {"Name": "Potion of Extreme Healing", "Restore": 150, "Quantity": 1}]

player = Person(500, 300, 60, 50, magic, healing_potions)
enemy = Person(1200, 300, 45, 50, None, None)

running = True

print(BColors.FAIL + BColors.BOLD + "AN ENEMY ATTACKS!" + BColors.ENDC)


def check_cheapest_spell_cost():
    cheap_cost = 9999999999
    for spell in magic:
        if spell["Cost"] < cheap_cost:
            cheap_cost = spell["Cost"]
    return cheap_cost


def check_remaining_potions():
    total_qty = 0
    for potion in healing_potions:
        total_qty += potion["Quantity"]
    if total_qty > 0:
        return True
    return False


def choose_spell(current_mp):
    player.choose_magic()
    print("Player MP: " + BColors.OKBLUE + BColors.BOLD + str(current_mp) + "/" + str(player.get_max_mp()) + BColors.ENDC)
    spell_choice = input("Choose your spell: ")
    spell_choice_index = int(spell_choice) - 1
    if current_mp < player.get_spell_cost(spell_choice_index):
        print(BColors.WARNING + BColors.BOLD + "You don't have enough magic points to cast " + player.get_spell_name(spell_choice_index) + "! Choose another spell!")
        choose_spell(player.get_mp())
    else:
        print("Chosen spell:", player.get_spell_name(spell_choice_index))
        dmg = player.generate_magic_damage(spell_choice_index)
        enemy.take_damage(dmg)
        player.reduce_mp(spell_choice_index)
        print("Enemy was struck for", BColors.WARNING + BColors.BOLD, dmg, BColors.ENDC, "points of damage! Enemy HP:", BColors.FAIL + BColors.BOLD + str(enemy.get_hp()) +"/" + str(enemy.get_max_hp()) + BColors.ENDC)


def choose_potion():
    player.choose_healing()
    potion_choice = input("Choose your potion: ")
    potion_choice_index = int(potion_choice) - 1
    if player.get_potion_quantity(potion_choice_index) > 0:
        restored_hp = player.get_potion_effect(potion_choice_index)
        player.heal_damage(restored_hp)
        player.consume_potion(potion_choice_index)
        print(BColors.OKGREEN + BColors.BOLD + "Player healed for", restored_hp, "health points. Player HP:", str(player.get_hp()) + BColors.ENDC)
    else:
        print("You don't have any more of that potion left. Choose another potion!")
        choose_potion()


def make_choice():
    player.restore_mp()
    player.choose_action()
    choice = input("Choose your action: ")
    if int(choice) == 1:
        print("You chose to attack!")
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("Enemy was struck for", BColors.WARNING + BColors.BOLD, dmg , BColors.ENDC, "points of damage! Enemy HP:", BColors.FAIL + BColors.BOLD + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + BColors.ENDC)
    elif int(choice) == 2:
        current_mp = player.get_mp()
        if check_cheapest_spell_cost() <= current_mp:
            choose_spell(current_mp)
        else:
            print(BColors.WARNING + BColors.BOLD + "You don't have enough magic points to cast any spells. Choose another action!" + BColors.ENDC)
            make_choice()

    elif int(choice) == 3:
        if check_remaining_potions():
            player.choose_healing()
            potion_choice = input("Choose your potion: ")
            potion_choice_index = int(potion_choice) - 1
            if player.get_potion_quantity(potion_choice_index) > 0:
                restored_hp = player.get_potion_effect(potion_choice_index)
                player.heal_damage(restored_hp)
                player.consume_potion(potion_choice_index)
                print(BColors.OKGREEN + BColors.BOLD + "Player healed for", str(restored_hp), "health points. Player HP:",  str(player.get_hp()) + "/" + str(player.get_max_hp()) + BColors.ENDC)
            else:
                print(BColors.WARNING + BColors.BOLD + "You don't have any more of that potion left. Choose another potion!" + BColors.ENDC)
                choose_potion()
        else:
            print(BColors.WARNING + BColors.BOLD + "You have got no potions left. Choose another action!" + BColors.ENDC)
            make_choice()


while running:
    make_choice()
    if enemy.get_hp() == 0:
        running = False
        print(BColors.OKBLUE + BColors.BOLD + "You have slain the enemy!" + BColors.ENDC)
        break
    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("You have been struck for", BColors.WARNING + BColors.BOLD + str(enemy_dmg) + BColors.ENDC, "points of damage! Player HP:", BColors.FAIL + BColors.BOLD + str(player.get_hp()) + "/" + str(player.get_max_hp()) + BColors.ENDC)
    if player.get_hp() == 0:
        running = False
        print(BColors.FAIL + BColors.BOLD + "You have been slain!" + BColors.ENDC)
