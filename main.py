from enum import Enum
from typing import List
import sys


class Pos:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x


class Response(Enum):
    NOT_BROKEN = 0
    BROKEN = 1
    FINISH = 2
    INVALID = -1


class Field:

    # 全部掘られていないで初期化
    def __init__(self, N: int, C: int):
        self.C = C
        self.is_broken = [[False] * N for _ in range(N)]
        self.total_cost = 0
        
    # クエリを投げるのとそのレスポンス
    def query(self, y: int, x: int, power: int, pos_all: Pos) -> Response:
        self.total_cost += power + self.C
        print(f"{y} {x} {power}", flush=True)
        res = Response(int(input()))
        if res in (Response.BROKEN, Response.FINISH):
            self.is_broken[y][x] = True
            pos_all.append(Pos(y,x))
        return res


class Solver:

    # Field の初期化
    def __init__(self, N: int, source_pos: List[Pos], house_pos: List[Pos], C: int, W: int, K: int):
        self.N = N
        self.W = W
        self.K = K
        self.source_pos = source_pos
        self.source_pos_all = source_pos
        self.house_pos = house_pos
        self.C = C
        self.field = Field(N, C)
    
        if C <= 1:
            self.power = 5
        elif C <= 2:
            self.power = 7
        elif C <= 4:
            self.power = 16
        elif C <= 8:
            self.power = 21
        elif C <= 16:
            self.power = 41
        elif C <= 32:
            self.power = 50
        elif C <= 64:
            self.power = 87
        elif C <= 128:
            self.power = 97

    def solve(self):
        # ! OUT
        # f = open('w.txt', 'w')
        # f.close()
        
        # if self.W <= 2:
        #     source_sum = Pos(0,0)
        #     for source in self.source_pos:
        #         source_sum.y += source.y
        #         source_sum.x += source.x
        #     source_sum.y //= self.W
        #     source_sum.x //= self.W

        #     data = self.house_pos
        #     sorted_data = sorted(data,key=lambda p:(abs(source_sum.y - p.y) + abs(source_sum.x - p.x)))
        # else:
        #     data = self.house_pos
        #     sorted_data = sorted(data,key=lambda p:(abs(100 - p.y) + abs(100 - p.x)))

        data = self.house_pos
        
        # if self.W == 1:
        if False:
            sorted_data = sorted(data,key=lambda p:(
                    (self.source_pos[0].y - p.y) ** 2 + (self.source_pos[0].x - p.x) ** 2)
                     )
        else:
            sorted_data = sorted(data,key=lambda p:(
                    abs(100 - p.y) + abs(100 - p.x)
                    ))
            

        for house in sorted_data:
            min_length = 10**5
            min_source = Pos(self.source_pos_all[0].y,self.source_pos_all[0].x)
            for source in self.source_pos_all:
                # length = abs(source.y - house.y) + abs(source.x - house.x)
                # length = ((source.y - house.y)**2 + abs(source.x - house.x)**2)**0.5
                length = abs(source.y - house.y)**1.9 + abs(source.x - house.x)**2
                if min_length > length:
                    min_length = length
                    min_source = Pos(source.y,source.x)
            
            self.move(house, min_source)

        # should receive Response.FINISH and exit before entering here
        raise AssertionError()

    def move(self, start: Pos, goal: Pos):

        dy = start.y - goal.y
        dx = start.x - goal.x

        self.destruct(start.y, start.x)
        
        if True:
            d = abs(abs(dy) - abs(dx))
            p = 1
            if abs(dy) < abs(dx):
                ty = start.y
                # right/left
                if start.x < goal.x:
                    tx = start.x + int(d*p)
                    for x in range(start.x, tx + 1, 1):
                        self.destruct(ty, x)
                else:
                    tx = start.x - int(d*p)
                    for x in range(start.x, tx - 1, -1):
                        self.destruct(ty, x)
            else:
                tx = start.x 
                # down/up
                if start.y < goal.y:
                    ty = start.y + int(d*p)
                    for y in range(start.y, ty + 1, 1):
                        self.destruct(y, tx)
                else:
                    ty = start.y - int(d*p)
                    for y in range(start.y, ty - 1, -1):
                        self.destruct(y, tx)

            dd = min(abs(dy),abs(dx)) * 2

            for e in range(dd):
                # if e >= dd - 4:
                if False:
                    break
                else:
                    # if e % 6 == 0 or e % 6 == 1 or e % 6 == 2:
                    # if e % 8 == 0 or e % 8 == 1 or e % 8 == 2 or e % 8 == 3:
                    if e % 2 == 0:
                        if ty < goal.y:
                            ty += 1
                        else:
                            ty -= 1
                    else:
                        if tx < goal.x:
                            tx += 1
                        else:
                            tx -= 1
                    self.destruct(ty, tx)


            if tx < goal.x:
                for x in range(tx, goal.x + 1,  1):
                    self.destruct(ty, x)
            else:
                for x in range(tx, goal.x - 1, -1):
                    self.destruct(ty, x)
            if ty < goal.y:
                for y in range(ty, goal.y + 1,  1):
                    self.destruct(y, goal.x)
            else:
                for y in range(ty, goal.y - 1, -1):
                    self.destruct(y, goal.x)



    def destruct(self, y: int, x: int):
        cnt = 1
        while not self.field.is_broken[y][x]:
            
            # result = self.field.query(
            #     y, x,
            #     max(
            #         self.power * 
            #         min(int(-0.00003  * (cnt-53) ** 3 + 500),
            #             int(cnt ** 0.3)),
            #         1
            #     ),
            #     self.source_pos_all)

            result = self.field.query(
                y, x, 
                int(self.power * cnt ** 0.30),
                self.source_pos_all)

            cnt += 28
            if result == Response.FINISH:
                # ! OUT
                f = open('score.txt', 'a')
                f.write(" " + str(self.field.total_cost) + "\n")
                f.close()
                # f = open('score_C.txt', 'a')
                # f.write(str(self.C) + " " + str(self.field.total_cost) + "\n\n")
                # f.close()
                sys.exit(0)
            elif result == Response.INVALID:
                # ! OUT
                f = open('score.txt', 'a')
                f.write(" " + str(self.field.total_cost) + "\n")
                f.close()
                sys.exit(1)


def main():
    # 入力の受け取り
    N, W, K, C = [int(v) for v in input().split(" ")]
    source_pos = []
    house_pos = []
    for _ in range(W):
        y, x = (int(v) for v in input().split(" "))
        source_pos.append(Pos(y, x))
    for _ in range(K):
        y, x = (int(v) for v in input().split(" "))
        house_pos.append(Pos(y, x))

    solver = Solver(N, source_pos, house_pos, C,W,K)
    solver.solve()


if __name__ == "__main__":
    main()
