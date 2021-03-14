import math
import json

def get_current_xp(data_levels):
    tmp = input("Quel est-votre niveau actuel ?\n")
    try:
        level = float(tmp)
        assert 0 <= level
        decimal_part, integer_part = math.modf(level)
        integer_part = int(integer_part)
        current_level = next((item for item in data_levels if item['lvl'] == integer_part), None)
        next_level = next((item for item in data_levels if item['lvl'] == (integer_part + 1)), None)
        assert current_level is not None and next_level is not None
        xp_for_next_level = next_level['xp'] - current_level['xp']
        xp_decimal_part = int(xp_for_next_level * decimal_part)
        current_xp = current_level['xp'] + xp_decimal_part
        return current_xp

    except ValueError:
        print("Vous n'avez pas saisi un nombre flotant")
        exit()
    except AssertionError:
        print("Votre niveau doit être compris entre 0 et 29")
        exit()

def get_projected_xp():
    xp_next_project = get_xp_next_project()
    grade = get_grade_next_project()
    return (xp_next_project * grade / 100)

def get_xp_next_project():
    tmp = input("Combien d'xp rapportent votre prochain projet ?\n")
    try:
        projected_xp = int(tmp)
        assert projected_xp > 0
        return projected_xp
    except ValueError:
        print("Vous n'avez pas saisi un nombre entier")
        exit()
    except AssertionError:
        print("Le projet doit rapporter plus de 0 d'xp")
        exit()

def get_grade_next_project():
    tmp = input("Quelle note allez vous obtenir ?\n")
    try:
        grade = int(tmp)
        assert grade > 0 and grade <= 125
        return grade
    except ValueError:
        print("Vous n'avez pas saisi un nombre entier")
        exit()
    except AssertionError:
        print("La note doit être comprise entre 0 et 125")
        exit()

def get_projected_level(data_levels, xp):
    new_level = next((item for item in data_levels if item['lvl'] == 0), None)
    for level in data_levels:
        if xp > level['xp'] and new_level['lvl'] < level['lvl']:
            new_level = level
    next_level = next((item for item in data_levels if item['lvl'] == (new_level['lvl'] + 1)), None)
    xp_for_next_level = next_level['xp'] - new_level['xp']
    xp_current_level = xp - new_level['xp']
    decimal_part_new_level = xp_current_level / xp_for_next_level
    return new_level['lvl'] + decimal_part_new_level

def main():
    with open('levels.json') as json_levels:
        data_levels = json.load(json_levels)
        current_xp = get_current_xp(data_levels)
        projected_xp = get_projected_xp() + current_xp
        next_level = get_projected_level(data_levels, projected_xp)
        print("Vous serez niveau : {:.2f}".format(next_level))

if __name__ == "__main__":
    main()