def main():
    gamestatebattle = False
    gamestatequit = False
    while gamestatequit != True:
        text = input("where will you go? ").lower()
        if text == "up":
            battle()
            gamestatequit = True
        else:
            continue


class Player:
    def __init__(self, health, defense, attack):
        self.health = health
        self.defense = defense
        self.attack = attack

class Enemy:
    def __init__(self, health, defense, attack):
        self.health = health
        self.defense = defense
        self.attack = attack
        

def battle():
    player = Player(health=10, defense=1, attack=2)
    print(player.health, player.defense, player.attack)
    enemy = Enemy(5, 1, 3)
    print(enemy.health, enemy.defense, enemy.attack)

    while player.health > 1:
        player.health = player.health - enemy.attack + player.defense
        print(player.health)
    
    print("GameOVER")





if __name__ == "__main__":
    main()