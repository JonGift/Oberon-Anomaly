
def check_distance(ship1, ship2):
    x = abs(ship1.x - ship2.x)
    y = abs(ship1.y - ship2.y)
    return x + y


def ai_target_enemy(ship, all_ships):
    #Use this function for fighters and bombers, and also for the entire ai.
    ship_type = []
    min_dist = 99999
    min_dist_ship = None
    if ship.type_name == 'Fighter':
        for x in range(len(all_ships)):
            if all_ships[x] != ship:
                if all_ships[x].hp > 0:
                    if all_ships[x].team != ship.team:
                        if all_ships[x].type_name == 'Fighter':
                            ship_type.append(all_ships[x])
                        if all_ships[x].type_name == 'Bomber':
                            ship_type.append(all_ships[x])
    if ship.type_name == 'Bomber':
        for x in range(len(all_ships)):
            if all_ships[x] != ship:
                if all_ships[x].hp > 0:
                    if all_ships[x].team != ship.team:
                        if all_ships[x].type_name == 'Frigate':
                            ship_type.append(all_ships[x])
                        if all_ships[x].type_name == 'Cruiser':
                            ship_type.append(all_ships[x])
                        if all_ships[x].type_name == 'Flagship':
                            ship_type.append(all_ships[x])
    if ship.type_name == 'Frigate':
        for x in range(len(all_ships)):
            if all_ships[x] != ship:
                if all_ships[x].hp > 0:
                    if all_ships[x].team != ship.team:
                        if all_ships[x].type_name == 'Cruiser':
                            ship_type.append(all_ships[x])
                        if all_ships[x].type_name == 'Frigate':
                            ship_type.append(all_ships[x])
                        if all_ships[x].type_name == 'Flagship':
                            ship_type.append(all_ships[x])
    if ship.type_name == 'Cruiser':
        for x in range(len(all_ships)):
            if all_ships[x] != ship:
                if all_ships[x].hp > 0:
                    if all_ships[x].team != ship.team:
                        if all_ships[x].type_name == 'Cruiser':
                            ship_type.append(all_ships[x])
                        if all_ships[x].type_name == 'Frigate':
                            ship_type.append(all_ships[x])
                        if all_ships[x].type_name == 'Flagship':
                            ship_type.append(all_ships[x])
    if ship.type_name == 'Flagship':
        for x in range(len(all_ships)):
            if all_ships[x] != ship:
                if all_ships[x].hp > 0:
                    if all_ships[x].team != ship.team:
                        if all_ships[x].type_name == 'Cruiser':
                            ship_type.append(all_ships[x])
                        if all_ships[x].type_name == 'Flagship':
                            ship_type.append(all_ships[x])

    if not ship_type:
        for x in range(len(all_ships)):
            if all_ships[x] != ship:
                if all_ships[x].hp > 0:
                    if all_ships[x].team != ship.team:
                        return all_ships[x]


    for x in range(len(ship_type)):
        #Not working right I think, not certain.
        if check_distance(ship, ship_type[x]) < min_dist:
            min_dist_ship = ship_type[x]
            min_dist = check_distance(ship, ship_type[x])
    return min_dist_ship


