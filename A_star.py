# -*- coding: utf-8 -*-

# 地图,列表（weight=height=9）
tm = [
    '111111111',
    '10000010E',
    '111010101',
    '100010001',
    '101010101',
    '101000101',
    '101010101',
    'S01000001',
    '111111111']

# 因为python里string不能直接改变某一元素，所以用test_map来存储搜索时的地图
test_map = []

#########################################################
class Node_Elem:
    """
    OPEN表、CLOSED表的元素类型，parent用来在成功的时候回溯路径
    """

    def __init__(self, parent, x, y, dist):
        self.parent = parent
        self.x = x  # 坐标系点(x,y)
        self.y = y
        self.dist = dist  # 当前节点路径长度


class A_Star:
    """
    A星算法实现类
    """

    # 注意w,h两个参数，如果修改地图，需要传入一个正确值或者此处修改默认参数
    def __init__(self, s_x, s_y, e_x, e_y, w=9, h=9):
        self.s_x = s_x
        self.s_y = s_y
        self.e_x = e_x
        self.e_y = e_y

        self.width = w
        self.height = h

        self.open = []  # OPEN表
        self.close = []  # CLOSED表
        self.path = []  # PATH路径

    # 查找路径的入口函数
    def find_path(self):
        # 构建开始节点
        p = Node_Elem(None, self.s_x, self.s_y, 0.0)
        while True:
            # 扩展评估函数F值最小的节点
            self.extend_round(p)
            # 如果OPEN表为空，则不存在路径，返回
            if not self.open:
                return
                # 获取F值最小的节点
            idx, p = self.get_best()
            # 找到路径，生成路径，返回
            if self.is_target(p):
                self.make_path(p)
                return
                # 把此节点压入CLOSED表，并从OPEN列表里删除
            self.close.append(p)
            del self.open[idx]

    def make_path(self, p):
        # 从结束点回溯到开始点，开始点的parent == None
        while p:
            self.path.append((p.x, p.y))
            p = p.parent

    def is_target(self, i):
        return i.x == self.e_x and i.y == self.e_y

    def get_best(self):
        best = None
        bv = 1000000
        bi = -1
        for idx, i in enumerate(self.open):
            value = self.get_dist(i)  # 获取F值
            if value < bv:  # 即F值更小
                best = i
                bv = value
                bi = idx
        return bi, best

    # 计算评估函数F值
    def get_dist(self, i):
        # F = G + H
        # G 为已经走过的路径长度， H为为当前节点到目标节点的曼哈顿距离
        return i.dist + (self.e_x - i.x) + (self.e_y - i.y)

    # 扩展节点
    def extend_round(self, p):
        # 只能走上下左右四个方向
        # 即下(0.-1)左(-1,0)右(1,0)上(0,1)
        xs = (0, -1, 1, 0)
        ys = (-1, 0, 0, 1)
        # zip(),返回元组列表[(0.-1), (-1,0), (1,0), (0,1)]
        for x, y in zip(xs, ys):
            new_x, new_y = x + p.x, y + p.y
            # 无效或者不可行走区域，则勿略
            if not self.is_valid_coord(new_x, new_y):
                continue
                # 构造新的节点
            node = Node_Elem(p, new_x, new_y, p.dist + self.get_cost(
                p.x, p.y, new_x, new_y))
            # 新节点在CLOSED列表，则忽略
            if self.node_in_close(node):
                continue
            i = self.node_in_open(node)
            if i != -1:
                # 新节点在OPEN列表
                if self.open[i].dist > node.dist:
                    # 现在的路径到比以前到这个节点的路径更好
                    # 则使用现在的路径
                    self.open[i].parent = p
                    self.open[i].dist = node.dist
                continue
            self.open.append(node)

    def get_cost(self, x1, y1, x2, y2):
            """
            上下左右直走，代价为1.0
            """
            if x1 == x2 or y1 == y2:
                return 1.0

    def node_in_close(self, node):
            for i in self.close:
                if node.x == i.x and node.y == i.y:
                    return True
            return False

    def node_in_open(self, node):
            for i, n in enumerate(self.open):
                if node.x == n.x and node.y == n.y:
                    return i
            return -1

    def is_valid_coord(self, x, y):
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return False
            return test_map[y][x] != '1'

    def get_searched(self):
            l = []
            for i in self.open:
                l.append((i.x, i.y))
            for i in self.close:
                l.append((i.x, i.y))
            return l

    #########################################################
def print_test_map():
    """
    打印搜索后的地图
    """
    for line in test_map:
        print(' '.join(line))


def get_start_XY():
    return get_symbol_XY('S')


def get_end_XY():
    return get_symbol_XY('E')


def get_symbol_XY(s):
    for y, line in enumerate(test_map):
        try:
            x = line.index(s)
        except:
            continue
        else:
            break
    return x, y


#########################################################
def mark_path(l):
    mark_symbol(l, '2')



def mark_symbol(l, s):
    for x, y in l:
        test_map[y][x] = s


def mark_start_end(s_x, s_y, e_x, e_y):
    test_map[s_y][s_x] = 'S'
    test_map[e_y][e_x] = 'E'


def tm_to_test_map():
    for line in tm:
        test_map.append(list(line))


def find_path():
    s_x, s_y = get_start_XY()
    e_x, e_y = get_end_XY()
    a_star = A_Star(s_x, s_y, e_x, e_y)
    a_star.find_path()
    searched = a_star.get_searched()
    path = a_star.path
    # 标记路径
    mark_path(path)
    print("path length is %d" % (len(path)))
    print("searched squares count is %d" % (len(searched)))
    # 标记开始、结束点
    mark_start_end(s_x, s_y, e_x, e_y)


if __name__ == "__main__":
    # 把字符串转成列表
    tm_to_test_map()
    find_path()
    print_test_map()
