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


import os
import json


class AI:
    def __init__(self, fname):
        self.table = {}
        if os.path.isfile(f'./{fname}'):
            with open(fname) as json_file:
                self.table = json.load(json_file)
                print(f"loaded AI from {fname}")

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
        with open(fname, 'w') as outfile:
            json.dump(self.table, outfile)


import random
import copy


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
            if ((random.randint(0, 100)) < 30):
                # случайный ход
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