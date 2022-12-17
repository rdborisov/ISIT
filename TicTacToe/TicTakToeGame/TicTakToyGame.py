import os
import json
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

# Интерфейс игры
class Game:

    def __init__(self, field=None):
        self.field = None
        if field:
            self.field = field
        else:
            self.start()

    def start(self):
        self.field = [' '] * 9

    def printField(self):
        row = ''
        for i in range(len(self.field)):
            cell = self.field[i]
            row += '['
            if cell != ' ':
                row += cell
            else:
                row += str(i + 1)
            row += ']'
            if (i % 3 == 2):
                print(row)
                row = ''

    def set(self, position, side):
        pos = int(position) - 1
        self.field[pos] = side

    def getFree(self):
        free = []
        for i in range(len(self.field)):
            cell = self.field[i]
            if (cell == ' '):
                free.append((i + 1))
        return free

    def isDraw(self):
        free = self.getFree();
        return len(free) == 0;

    def isWin(self, side):
        for i in range(3):
            isW = True
            for j in range(3):
                if self.field[i * 3 + j] != side:
                    isW = False
                    break
            if isW:
                return isW
        for i in range(3):
            isW = True
            for j in range(3):
                if self.field[j * 3 + i] != side:
                    isW = False
                    break
            if isW:
                return isW
        isW = True;
        for i in range(3):
            if self.field[i * 3 + i] != side:
                isW = False
                break
        if isW:
            return isW

        isWi = True;
        for i in range(3):
            if self.field[(i * 3 + 2 - i)] != side:
                isW = False
                break
        if isW:
            return isW
        return False

    def getState(self, side):
        if side == 'x':
            return self.field
        newField = ''
        for i in range(len(self.field)):
            if self.field[i] == 'x':
                newField += 'o'
            elif self.field[i] == 'o':
                newField += 'x'
            else:
                newField += self.field[i]
        return newField


# Описание логики памяти агента и оценка состояний игры
class AI:
    def __init__(self):
        self.table = {}
        if os.path.isfile('./rewards.json'):
            with open('rewards.json') as json_file:
                self.table = json.load(json_file)
                print("loaded AI from rewards.json")

    def getReward(self, state):
        game = Game(state)

        # если победитель - мы, то оценка состояния игры "1"
        if game.isWin('x'):
            return 1

        # если победиль - соперник, то оценка состояния игры "0"
        if game.isWin('o'):
            return 0

        # смотрим ценность по таблице
        strstate = ''.join(state)
        if strstate in self.table.keys():
            return self.table[strstate]

        # если в таблице нет, то считаем начальной ценностью "0.5"
        return 0.5

    def correct(self, state, newReward):
        oldReward = self.getReward(state)
        strstate = ''.join(state)
        self.table[strstate] = oldReward + 0.1 * (newReward - oldReward)

    def save(self):
        with open('rewards.json', 'w') as outfile:
            json.dump(self.table, outfile)


# Описание агента
class AIPlayer:

    def __init__(self, side, ai, isGreedy=True):
        self.side = side
        self.ai = ai
        self.oldState = None
        self.isGreedy = isGreedy

    def getSide(self):
        return self.side

    def makeStep(self, game):
        # получаем список доступных ходов
        free = game.getFree()

        # решаем, является ли текущий ход
        # зондирующим (случайным) или жадным (максимально выгодным)

        if not self.isGreedy:
            # случайный ход
            print('Random step')
            step = random.choice(free)
            game.set(step, self.side)
            self.oldState = game.getState(self.side)
            return step

        # жадный ход
        rewards = {}
        for step in free:
            # для каждого доступного хода оцениваем состояние игры после него
            newGame = copy.deepcopy(game)
            newGame.set(step, self.side)
            rewards[step] = self.ai.getReward(newGame.getState(self.side))

        # выясняем, какое вознаграждение оказалось максимальным
        maxReward = 0
        for reward in rewards.values():
            if reward > maxReward:
                maxReward = reward

        # находим все шаги с максимальным вознаграждением
        steps = []

        for step in rewards:
            reward = rewards[step]
            if (maxReward > (reward - 0.01)) and (maxReward < (reward + 0.01)):
                steps.append(step)

        # корректируем оценку прошлого состояния
        # с учетом ценности нового состояния
        if (self.oldState):
            self.ai.correct(self.oldState, maxReward)

        # выбираем ход из ходов с максимальный вознаграждением
        step = random.choice(steps)
        game.set(step, self.side)

        # сохраняем текущее состояние для того,
        # чтобы откорректировать её ценность на следующем ходе
        self.oldState = game.getState(self.side)
        return step

    def loose(self):
        # корректируем ценность предыдущего состояния при проигрыше
        if self.oldState:
            self.ai.correct(self.oldState, 0)

    def win(self):
        # корректируем ценность предыдущего состояния при выигрыше
        if self.oldState:
            self.ai.correct(self.oldState, 1)

    def draw(self):
        # корректируем ценность предыдущего состояния при ничьей
        if self.oldState:
            self.ai.correct(self.oldState, 0.5)


# Логика пользовательского ввода
class UserPlayer:

    def __init__(self, side):
        self.side = side

    def getSide(self):
        return self.side

    def makeStep(self, game):
        game.printField()

        free = game.getFree()

        inp = None
        while (True):
            inp = input()
            if int(inp) in free:
                break

        game.set(inp, self.side)

    def loose(self):
        print('you loose')

    def win(self):
        print('you win')

    def draw(self):
        print('draw')


# Класс запуска

plt.figure(figsize=(12, 7))

def graphic():
    print('x:', countX, 'o:', countO, 'draw:', countD)
    plt.legend(loc=5)
    plt.xlabel('Проведено игр')
    plt.ylabel('Победы')
    plt.title('График зависимости побед от общего кол-ва игр')
    plt.legend(['X', 'O', 'D'], loc=2)
    plt.grid(True)
    plt.show()

print('Choose your side:')
print('X) x')
print('O) o')
print('Any other symbol if you would like to run AI vs AI')
side = ' '  # input();

ai = AI()
gameCount = 1

playerX = AIPlayer('x', ai, True)
playerO = AIPlayer('o', ai, True)

if (side == 'X') or (side == 'x'):
    playerX = UserPlayer('x')
    playerO = AIPlayer('o', ai, True)
elif (side == 'O') or (side == 'o'):
    playerX = AIPlayer('x', ai, True)
    playerO = UserPlayer('o')
else:
    playerX = AIPlayer('x', ai, True)
    playerO = AIPlayer('o', ai, True)

    print('Enter games count:')
    gameCount = 500000  # int(input())

    if (gameCount <= 0):
        gameCount = 1

game = Game()

countX = 0
countO = 0
countD = 0

for i in range(gameCount):
    print('New game', i + 1)
    game.start()
    while (True):
        if game.isDraw():
            playerX.draw()
            playerO.draw()
            countD += 1
            break

        playerX.makeStep(game)
        if game.isWin(playerX.getSide()):
            playerX.win()
            playerO.loose()
            countX += 1
            break

        if game.isDraw():
            playerX.draw()
            playerO.draw()
            countD += 1
            break

        field = playerO.makeStep(game)
        if game.isWin(playerO.getSide()):
            playerO.win()
            playerX.loose()
            countO += 1
            break

    game.printField()

    plt.plot(i, countX, 'o-r', alpha=1, lw=2, color='k', mew=1, ms=1)
    plt.plot(i, countO, 'o-r', alpha=1, lw=2, color='g', mew=1, ms=1)
    plt.plot(i, countD, 'o-r', alpha=1, lw=2, color='b', mew=1, ms=1)

ai.save()
graphic()