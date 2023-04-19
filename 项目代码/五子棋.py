from copy import deepcopy
from math import sqrt
from draw import *
GRID_WIDTH = 40
COLUMN = 20
ROW = 20

game_n=0#下了几轮棋

def geta_matri(checkerboard,star_n,n=1):#得到一个从star_n开始的5*5的矩阵
    matri=[]
    for i in range(25):
        matri.append(checkerboard[star_n+int(sqrt(len(checkerboard)))*(i//5)+i%5])
    return matri

def matrix_mul(board_matri,eva_matri):#矩阵对应元素相乘
    ans=0
    for i in range(25):
        ans+=board_matri[i]*eva_matri[i]
    return ans

def good_score(board_matri):#判断有没有一些好的棋局，展示未使用,可以进行拓展
    return 0
    add_scr=0
    good1=[0,1,1,1,0]
    good1_=[0,-1,-1,-1,0]
    # good2[]
    good_i=[[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15,16,17,18,19],[20,21,22,23,24],[0,6,12,18,24],[4,8,12,16,20]]
    for i in good_i:
        if [board_matri[i[0]],board_matri[i[1]],board_matri[i[2]],board_matri[i[3]],board_matri[i[4]]]==good1:
            add_scr+=2000
        if [board_matri[i[0]],board_matri[i[1]],board_matri[i[2]],board_matri[i[3]],board_matri[i[4]]]==good1_:
            add_scr-=2000
    return add_scr

def evaluate2(checkerboard):#对矩阵统计对分数进行计算
    length=int(sqrt(len(checkerboard)))
    is_win=False
    sc=0
    s0=[[0,0,0,0,0]]
    s1=[[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[]]
    score_dic={0:0,1:10+10*game_n,2:100+100*game_n,3:10000+10000*game_n,4:20000+20000*game_n,5:1000000+100000*game_n,-1:-(5+5*game_n),-2:-(50+50*game_n),-3:-(1000+1000*game_n),-4:-(10000+10000*game_n),-5:-(1000000+100000*game_n)}
    #用于提取的行列对角阵
    eva_matri=[[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
               [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0],
               [0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0],
               [0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
               [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0],
               [0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
               [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
               [0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0]]
    for i in range(length-5):#行
        for k in range(0,length-5,5):
            board_matri = geta_matri(checkerboard, k*length+i)#得到一个矩阵
            for j in range(5):
                temp = matrix_mul(board_matri, eva_matri[j])
                sc += score_dic.get(temp)
                sc += good_score(board_matri)
                if temp == 5:
                    is_win = True
                    return sc,is_win
    for i in range(0,length-5,5):#列
        for k in range(length-5):
            board_matri = geta_matri(checkerboard, k*length+i)
            for j in range(5,10):
                temp = matrix_mul(board_matri, eva_matri[j])
                sc += score_dic.get(temp)
                sc += good_score(board_matri)
                if temp == 5:
                    is_win = True
                    return sc,is_win
    for i in range(len(checkerboard)-int(sqrt(len(checkerboard)))*4-4):#到最右下角一个正方形就停止
        board_matri=geta_matri(checkerboard,i)
        for j in range(10,12):
            temp=matrix_mul(board_matri,eva_matri[j])
            sc+=score_dic.get(temp)
            sc+=good_score(board_matri)
            if temp==5:
                is_win = True
                return sc, is_win
    return sc,is_win

def get_lianxu(checkerboard):#得到一行有多少个连续的1、-1
    j = 0
    sum = {1: 0, -1: 0}
    is_sum = True
    while j < len(checkerboard):
        if checkerboard[ j] == 0:#前面的0
            is_sum = True
            j = j + 1
        else:
            if is_sum:#遇到不是0
                is_sum = False
                temp = checkerboard[j]
                s = 0
                kong=0
                if j+1 <len(checkerboard):#小心j+1超出范围
                    while (checkerboard[j] == temp) or (checkerboard[j] == 0 and checkerboard[j+1]==temp and kong==0):#有连续相同的temp，或者只是差一个0，就可以继续连在一起
                        if checkerboard[j] == temp:
                            s = s + 1
                        if(checkerboard[j] == 0 and checkerboard[j+1]==temp):#只连续统计一次带空格的，例如：1 0 1 1 1 1
                            kong = 1
                        j = j + 1
                        if j+1>=len(checkerboard):
                            break
                if j <len(checkerboard):
                    if checkerboard[j] ==-1*temp and s!=5:#如果连续的旁边有对方的子，数就-1，但是如果有5个了，就不减
                        s=s-1
                if s==5 and kong==1:#如果是经过一个空格才连起来的，就不算5个
                    s=s-1
                if s > sum[temp]:#更新
                    sum[temp] = s
            else:
                temp = checkerboard[j]
                s = 0
                while (checkerboard[j] == temp):#对这种情况：-1 1 1 1 1 -1 进行判断有没有5个联起来成功的
                    s=s+1
                    j=j+1
                    if j>=len(checkerboard):
                        break
                if s==5:
                    sum[temp] = s
    #从右往左基本相同
    is_sum = True
    j = len(checkerboard) - 1
    while j >= 0:
        if checkerboard[j] == 0:
            is_sum = True
            j = j - 1
        else:
            if is_sum:
                is_sum = False
                temp = checkerboard[j]
                s = 0
                while (checkerboard[j] == temp) or (checkerboard[j] == 0 and checkerboard[j-1]==temp and kong==0):
                    if checkerboard[j] == temp:
                        s = s + 1
                    if(checkerboard[j] == 0 and checkerboard[j-1]==temp):#0(1) 0 1 1 1 1
                        kong = 1
                    j = j - 1
                    if j<0:
                        break

                if j >=0:
                    if checkerboard[j] ==-1*temp and s!=5:
                        s=s-1
                if s == 5 and kong == 1:
                    s = s - 1
                if s > sum[temp]:
                    sum[temp] = s
            else:
                temp = checkerboard[j]
                s = 0
                while (checkerboard[j] == temp):  # -1 1 1 1 1 -1
                    s = s + 1
                    j = j - 1
                    if j<0:
                        break
                if s == 5:
                    sum[temp] = s
    return sum;

def get_row(n,checkerboard):#得到一行
    temp=[]
    for i in range(ROW):
        temp.append(checkerboard[n*COLUMN+i])
    return temp

def get_col(n,checkerboard):#得到一列
    temp=[]
    for i in range(COLUMN):
        temp.append(checkerboard[n+COLUMN*i])
    return temp

def get_left_top(n,checkerboard):#得到从左上到右下
    temp=[]
    # i=0
    if n>=0:
        for i in range(ROW-n):
            temp.append(checkerboard[i+COLUMN*i+n])
    else:
        for i in range(-1*n,ROW):
            temp.append(checkerboard[i+COLUMN*i+n])#164 167
    return temp

def get_right_top(n,checkerboard):#得到从右上到左下
    temp=[]
    if n>=0:
        for i in range(n+1):
            temp.append(checkerboard[COLUMN*i+n-i])
    else:
        for i in range(ROW+n):
            temp.append(checkerboard[COLUMN*(i-n)+20-i-1])
    return temp

def evaluate(checkerboard):#对棋局进行评分
    is_fin=False
    score_dic = {0: 0, 1: 10, 2: 100 , 3: 2000  , 4: 30000 ,
                 5: 2000000, -1: -5, -2: -50,
                 -3: -1000, -4: -10000, -5: -1000000}
    score=0
    for i in range(ROW):#一行一行算分
        t=get_row(i,checkerboard)
        t_sum=get_lianxu(t)
        score+=score_dic[t_sum[1]]
        score+=score_dic[-t_sum[-1]]
        if(t_sum[1]==5 or t_sum[-1]==5):#如果5个连起来就算游戏结束
            is_fin=True
            return score,is_fin
    #其余的列和对角线都相同
    for i in range(COLUMN):
        t=get_col(i,checkerboard)
        t_sum=get_lianxu(t)
        score+=score_dic[t_sum[1]]
        score+=score_dic[-t_sum[-1]]
        if(t_sum[1]==5 or t_sum[-1]==5):
            is_fin=True
            return score,is_fin
    for i in range(-15,16):
        t=get_left_top(i,checkerboard)
        t_sum=get_lianxu(t)
        score+=score_dic[t_sum[1]]
        score+=score_dic[-t_sum[-1]]
        if (t_sum[1] == 5 or t_sum[-1] == 5):
            is_fin = True
            return score, is_fin
    for i in range(4,20):
        t=get_right_top(i,checkerboard)
        # print(t)
        t_sum=get_lianxu(t)
        score+=score_dic[t_sum[1]]
        score+=score_dic[-t_sum[-1]]
        if (t_sum[1] == 5 or t_sum[-1] == 5):
            is_fin = True
            return score, is_fin
    for i in range(-15,0):
        t=get_right_top(i,checkerboard)
        t_sum=get_lianxu(t)
        score+=score_dic[t_sum[1]]
        score+=score_dic[-t_sum[-1]]
        if (t_sum[1] == 5 or t_sum[-1] == 5):
            is_fin = True
            return score, is_fin
    return score,is_fin

def get_map(checkerboard):#得到现在有的棋子的旁边一格的所有棋子，当做需要进行判断的棋
    map=[]
    length=int(sqrt(len(checkerboard)))
    dir=[-length-1,-length,-1,1,length,length-1,length+1,-length+1]
    if not 1 in checkerboard and not -1 in checkerboard:#棋盘上面没有棋子
        map.append(len(checkerboard)//2+length//2)
        return map
    for i in range(len(checkerboard)):
        if(checkerboard[i]!=0):
            for j in dir:
                print(i,'-',j,end=' ')
                if(i+j not in map and i+j>=0 and i+j<len(checkerboard) and not(i%length==0 and (i+j)%length==length-1) and not(i%length==19 and (i+j)%length==0)):#对边角的棋子进行了一些特判
                    if(checkerboard[i+j]==0):
                        map.append(i+j)
    return map

def calculus(is_ai,checkerboard,flag,depth,alpha=-999999999999,beta=999999999999):#alph_beta进行剪枝运算
    talpha=[-1,alpha]
    tbeta=[-1,beta]
    map=get_map(checkerboard)#得到要遍历的棋
    print('map:',map)
    if(flag=='max'):
        print('%s%d层：此时(alpha,beta)=(%d,%d),最优下子点为%d' % (flag, 3 - depth, talpha[1], tbeta[1], talpha[0]))
    else:
        print('%s%d层：此时(alpha,beta)=(%d,%d),最优下子点为%d' % (flag, 3 - depth, talpha[1], tbeta[1], tbeta[0]))
    for i in map:
        copyboard = deepcopy(checkerboard)
        if(copyboard[i])!=0:#已经下过棋了
            continue
        else:
            if(is_ai):#电脑回合
                copyboard[i]=1
            else:
                copyboard[i]=-1
            if flag=='max':
                temp,is_win=evaluate(copyboard)
                if (is_win):  # 游戏结束的棋法
                    print('(下子点：%d,得分：%d)'%(i,temp),end=' ')
                    print('此时游戏结束,不往下预测',end='')
                    return (i, temp)
                if (depth - 1 == 0):#到达最底的一层
                    print('(下子点：%d,得分：%d)'%(i,temp),end=' ')
                    if (temp > talpha[1]):
                        print('符合条件，更新alpha,beta为',(temp,tbeta[1]),end=' ')
                        talpha[0]=i
                        talpha[1] = temp
                    if (talpha[1]>=tbeta[1]):#查看是否需要剪枝
                        print('符合剪枝条件，剪枝')
                        return
                else:
                    print('%s%d下子点：%d'%(flag,3-depth,i))
                    sc=calculus(False,copyboard,'min',depth-1,talpha[1],tbeta[1])#不是最底一层就继续往下遍历
                    if sc:#如果没有被剪枝
                        if (sc[1]>talpha[1]):
                            talpha=(i,sc[1])
                    print('%s%d层：此时(alpha,beta)=(%d,%d),最优下子点为%d'%(flag,3-depth,talpha[1],tbeta[1],talpha[0]))
            #min层和max层是一样的
            elif flag=='min':
                temp,is_win = evaluate(copyboard)
                if (is_win):#游戏结束的棋法
                    print('(下子点：%d,得分：%d)'%(i,temp),end=' ')
                    print('此时游戏结束,不往下预测',end='')
                    return (i, temp)
                if (depth - 1 == 0):
                    print('(下子点：%d,得分：%d)'%(i,temp),end=' ')
                    if (temp < tbeta[1]):
                        print('符合条件，更新alpha,beta为',(talpha[1],temp),end=' ')
                        tbeta[0]=i
                        tbeta[1] = temp
                    if (talpha[1]>=tbeta[1]):
                        print('符合剪枝条件，剪枝')
                        return
                else:
                    print('%s%d下子点：%d'%(flag,3-depth,i))
                    sc = calculus(True, copyboard, 'max', depth - 1, talpha[1], tbeta[1])
                    if sc:
                        if sc[1]<tbeta[1]:
                            tbeta=(i,sc[1])
                    print('%s%d层：此时(alpha,beta)=(%d,%d)，最优下子点为%d' % (flag, 3 - depth, talpha[1], tbeta[1],tbeta[0]))
    if flag=='max':
        print('')
        return talpha
    elif flag=='min':
        print('')
        return tbeta

def isGameOver(checkerboard):#通过是否有5个连在一起的判断棋是否结束
    eva_matri = [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]]
    for i in range(len(checkerboard)-int(sqrt(len(checkerboard)))*4-4):
        # print(i)
        board_matri=geta_matri(checkerboard,i)
        for j in range(len(eva_matri)):
            temp=matrix_mul(board_matri,eva_matri[j])
            if temp==5:
                return '电脑获胜！'
            elif temp==-5:
                return '恭喜你获胜！'
    if not 0 in checkerboard:#棋盘满了
        return '平局~'
    else:
        return


def gamewin():#绘制棋盘
    win = GraphWin("五子棋", GRID_WIDTH * (COLUMN-1), GRID_WIDTH * (ROW-1))
    win.setBackground("#ebca8e")
    i1 = 0

    while i1 <= GRID_WIDTH * COLUMN:
        l = Line(Point(i1, 0), Point(i1, GRID_WIDTH * COLUMN))
        l.draw(win)
        i1 = i1 + GRID_WIDTH
    i2 = 0

    while i2 <= GRID_WIDTH * ROW:
        l = Line(Point(0, i2), Point(GRID_WIDTH * ROW, i2))
        l.draw(win)
        i2 = i2 + GRID_WIDTH
    return win

def star_win():#绘制开始界面
    win = GraphWin("五子棋", GRID_WIDTH * COLUMN, GRID_WIDTH * (ROW-3))
    for i in range(100, 300):
        win.plot(i, 300)
        win.plot(i, 400)
    for i in range(500, 700):
        win.plot(i, 300)
        win.plot(i, 400)
    for i in range(300, 400):
        win.plot(100, i)
        win.plot(300, i)
        win.plot(500, i)
        win.plot(700, i)
    message = Text(Point(200, 350), "玩家先手")
    message.setSize(30)
    message.draw(win)
    message2 = Text(Point(600, 350), "电脑先手")
    message2.setSize(30)
    message2.draw(win)
    message3 = Text(Point(400, 150), "五子棋游戏")
    message3.setSize(36)
    message3.draw(win)
    while (1):
        b = win.getMouse()
        if (b.x > 100 and b.x < 300 and b.y > 300 and b.y < 400):
            print('玩家先手')
            win.close()
            return False
        if (b.x > 500 and b.x < 700 and b.y > 300 and b.y < 400):
            print('电脑先手')
            win.close()
            return True

def game():#游戏进行
    checkerboard=[0]*400
    peo_pos=[0,0]
    ai_pos=[0,0]
    is_ai = star_win()
    ai_cor='black' if is_ai else 'white'
    peo_cor='black' if not is_ai else 'white'
    win = gamewin()
    n=1
    while(1):
        if not is_ai:#人回合
            p2 = win.getMouse()
            peo_pos[0] = round((p2.getX()) / GRID_WIDTH)
            peo_pos[1] = round((p2.getY()) / GRID_WIDTH)
            print(peo_pos)
            checkerboard[peo_pos[0]+peo_pos[1]*COLUMN]=-1
            piece = Circle(Point(GRID_WIDTH * peo_pos[0], GRID_WIDTH * peo_pos[1]), 16)
            piece.setFill(peo_cor)
            piece.draw(win)
            txt=isGameOver(checkerboard)
            if txt:
                break
        else:#机器回合
            score = calculus(is_ai, checkerboard, 'max', 2)
            checkerboard[score[0]] = 1
            ai_pos[0]=score[0]%COLUMN
            ai_pos[1]=score[0]//COLUMN
            piece = Circle(Point(GRID_WIDTH * ai_pos[0], GRID_WIDTH * ai_pos[1]), 16)
            piece.setFill(ai_cor)
            piece.draw(win)
            txt = isGameOver(checkerboard)
            if txt:
                break
        is_ai = not is_ai
        n=n+1
        if n%20==0:#每20个记录+1
            global game_n
            game_n+=1

    message = Text(Point(400, 300), txt+"点击任意处结束")
    message.setSize(30)
    message.draw(win)
    win.getMouse()
    win.close()

if __name__ == '__main__':
    game()