

def ai_target_enemy(ship, all_ships):
	ship_type = {}
	if ship.type_name == 'Fighter':
		for x in range(len(all_ships)):
			if all_ships[x] != ship:
				if all_ships[x].hp > 0:
					if all_ships[x].team != ship.team:
						if all_ships[x].ship_type == 'Fighter':
							ship_type[all_ships[x]] = 'Fighter'

	print(ship_type)
				