#!usr/bin/python3
# -*- coding: utf-8 -*-
# author: zzZ5

import numpy as np
from queue import Queue


class _Position():
    """
    细胞在棋盘中的位置信息.

    Attribute:
        position(list): 细胞在棋盘中的位置. 用list确保细胞位置可以扩展到三维甚至更高维的空间.
    """

    def __init__(self, position):
        self.position = position

    def __eq__(self, value):
        return self.position == value.position


class Board():
    """
    生命游戏棋盘.

    Parameter:
        board(list): 输入的棋盘, 其中数值为 1 表示有细胞, 数值为 0 表示无细胞.
        liveNum(list[int]): 细胞存活的条件, 只要细胞周围有 liveNum 列表中数量的细胞, 则该细胞存活, 否则该细胞死亡.
        generateNum(list[int]): 生成细胞的条件, 只要空格子周围有 generateNum 列表中数量的细胞, 则在该位置生成一个新细胞.

    Attribute:
        board(ndarry): 现在的棋盘.
        shape(tuple): 棋盘的形状, 其中 0 位置为 x 轴大小, 1 位置为 y 轴大小, 可以扩展到z轴甚至更多轴.
        dimension(int): 维度.
        liveNum(list[int]): 细胞存活的条件, 只要细胞周围有 liveNum 列表中数量的细胞, 则该细胞存活, 否则该细胞死亡.
        generateNum(list[int]): 生成细胞的条件, 只要空格子周围有 generateNum 列表中数量的细胞, 则在该位置生成一个新细胞.
    """

    def __init__(self, board, liveNum=[2, 3], generateNum=[3]):
        self.board = np.array(board, np.int)
        self.shape = self.board.shape
        self.dimension = len(self.shape)
        self.liveNum = liveNum
        self.generateNum = generateNum

    def _isInside(self, pos: _Position):
        """
        确认该位置是否在棋盘内.

        Parameter:
            pos(_Position): 需要确认的位置.

        Return:
            bool: 在棋盘中返回 True, 不在棋盘中返回 False.
        """

        for i in range(len(pos.position)):
            if(pos.position[i] < 0 or pos.position[i] >= self.shape[i]):
                return False
        return True

    def _getAroundPosition(self, pos: _Position):
        """
        迭代获取该位置周围所有的位置.

        Parameter:
            pos(_Position): 需要获取周围位置的位置.

        Return:
            _Position: 迭代返回该位置周围所有的位置.
        """

    # 广度优先遍历该坐标周围的所有坐标, 并迭代返回.
        q = Queue()
        # 防止重复返回, 已返回的值为 1, 未返回的为 0.
        map = np.zeros(self.shape, np.int)

        # 从最小的位置开始遍历
        startList = pos.position[:]
        for i in range(self.dimension):
            if startList[i] > 0:
                startList[i] -= 1

        q.put(_Position(startList))
        while not q.empty():
            temp1 = q.get()
            if temp1.position != pos.position:
                yield temp1

            for d in range(self.dimension):
                temp2 = _Position(temp1.position[:])
                temp2.position[d] += 1
                if temp2.position[d] <= (pos.position[d] + 1) and self._isInside(temp2):
                    idx = tuple(temp2.position)
                    if map[idx]:
                        continue
                    else:
                        q.put(temp2)
                        map[idx] = 1

    def _calcNum(self, pos):
        """
        计算一个位置周围活细胞的总量.

        Parameter:
            position(_Position): 该点的位置.
        return:
            int: 该位置周围活细胞的总数(不同维度之下周围位置数量不同, 一维2个, 二维8个, 三维26个).
        """

        totalNum = 0

        # 统计点周围的活细胞数
        for p in self._getAroundPosition(pos):
            if(self.board[tuple(p.position)]):
                totalNum += 1

        return totalNum

    def next(self):
        """
        计算下一次棋盘, 并将当前棋盘设置为下一次的棋盘

        return:
            ndarry: 下一次的棋盘.
        """

        # 先创建一个空棋盘.
        nextBoard = np.zeros(self.shape, np.int)

        # 从最小的点开始遍历
        initList = []
        for i in range(self.dimension):
            initList.append(0)
        p = _Position(initList)

    # 广度优先遍历所有坐标,
        q = Queue()
        q.put(p)
        # 防止重复遍历, 已遍历的值为 1, 未遍历的为 0.
        map = np.zeros(self.shape, np.int)
        map[tuple(p.position)] = 1

        while not q.empty():
            temp1 = q.get()
            totalNum = self._calcNum(temp1)
            index = tuple(temp1.position)

            if (not self.board[index]):
                if (totalNum in self.generateNum):
                    nextBoard[index] = 1
            elif (totalNum in self.liveNum):
                nextBoard[index] = 1

            for d in range(self.dimension):
                temp2 = _Position(temp1.position[:])
                temp2.position[d] += 1
                if temp2.position[d] < self.shape[d]:
                    idx = tuple(temp2.position)
                    if map[idx]:
                        continue
                    else:
                        q.put(temp2)
                        map[idx] = 1

        # 将下一次的棋盘赋值到当前棋盘
        self.board = nextBoard

        return self.board
