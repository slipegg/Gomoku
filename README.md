# Gomoku

五子棋人机博弈游戏，基于极大极小值的 alpha_beta 剪枝来完成，用Python编写完成。

![image](https://user-images.githubusercontent.com/65942634/233085410-38603e3c-92b7-4ec5-bf14-7fe7317c3166.png)


![image](https://user-images.githubusercontent.com/65942634/233085279-39cc2956-dc0a-49cd-9742-4f714ed771b9.png)

核心的分数判断函数进行了多次优化，因为一开始使用的用5*5的矩阵从左上到右下进行遍历棋局，然后通过分别对横竖还有对角的值进行相加，按照相加和进行判断分类，但是这样子过于粗糙，而且速度也慢，对于2层深度的遍历，前期两三秒才能出结果，后期就需要六七秒了，体验很不好。之后对其进行了优化，通过判断行列和对角的列表的值进行判断和空相接的黑子和白子一共有多少进行计数，然后依据结果进行赋值，这样不仅更准确而且速度也更快了，粗略地看来这样子3层的时间相当于之前用矩阵的2层的时间，而2层的遍历基本能在2秒内出结果，体验较好。后续还可以对分数进行继续的优化，但限于当时的时间和精力有限就止步于此了。

## 算法说明

### 极大极小值算法原理

将搜索数的层数分为Max层和Min层，Max层是ai下棋，会向下选择对ai最好的情况，Min层是预测人下棋，会尽量选择对ai最不利的情况，最后ai就是在Min中寻找最大值，如果层数够多也就是逐步往下遍历，到达最底层之后，就会对前面下的棋最后的棋局进行评分，进行遍历所有可能的情况，Min最后选的是最小的值，Max选的是最大的值，然后就继续往上传递。

### alpha beta剪枝算法原理

极大极小值搜索算法的缺点就是当博弈树的层数变大时，需要搜索的节点数目会指数级增长。比如每一层的节点为50时，六层博弈树的节点就是50的6次方，运算时间会非常漫长，而这在运算过程中有很多是不需要进行预测的，Alpha-Beta剪枝就是用来将搜索树中不需要搜索的分支裁剪掉，以提高运算速度。基本的原理是：当一个 MIN 层节点的 α值 ≤ β值时 ，剪掉该节点的所有未搜索子节点当一个 MAX 层节点的 α值 ≥ β值时 ，剪掉该节点的所有未搜索子节点其中α值是该层节点当前最有利的评分，β值是父节点当前的α值，根节点因为是MAX层，所以 β值 初始化为正无穷大(+∞)。
初始化节点的α值，如果是MAX层，初始化α值为负无穷大(-∞)，这样子节点的评分肯定比这个值大。如果是MIN层，初始化α值为正无穷大(+∞)，这样子节点的评分肯定比这个值小。
例如一开始进行深度遍历的时候，到达了最底层的Min层，这时就需要对其最后的情况进行遍历，得到不同的值，然后选取最小的值，回去一层，将这个值为α进行赋值，，代表后面遍历时查找的范围是（α，+∞），因为如果小于α的话，因为这里是选取Max，所以是不会选取比α小的数据的，再继续，就又是一个Min层，如果对节点的评分进行预测，如果它的值比α小的话，那么就说明这一个Min节点最后会选择一个不大于α的值，那么对于再往上的Max层，它就不会选择这个Min的值，也就不需要继续往下判断了，这时候就可以进行剪枝。但是如果最后的值都没有小于α的话，那么就说明回到Max之后，它会选择这一个节点的值，所以这时候就需要把α更新为这个节点的值。以此类推，就可以完成这个算法。

### 棋局评估算法

这里先后使用了2个棋局评估算法，一个是5*5的矩阵为单位的评估算法，一个是以一列为单位的评估算法。

**矩阵评估**

因为棋局是20*20的大小，所以需要从（0,0）开始，遍历到（15,15），每次以这个坐标为最左上角的点来形成一个5*5的矩阵，然后通过矩阵相乘来提取出5行5列和2个对角线，然后通过计算每个的和，通过和的值来进行分类，对分数进行赋值。算法如下：

![image](https://user-images.githubusercontent.com/65942634/233086132-12a1d926-8e57-4376-b81e-50c836c7a8ed.png)


**列评估**

	对于一个20*20的棋盘，可以提取出20行20列以及31个从左上到右下、31个从左上到右下的长度大于等于5的数据。然后都转化为一行的列表。对这一个列表进行求和，步骤如下：先是从左往右遍历，找到不为0的值，即有棋子，计数+1，然后继续往右看，如果还是同一种棋子，就计数继续+1，如果后面遇到另一种棋子，就说明这里被堵了，所以就结束计数，还需要判断是不是这时是5个棋子，如果是5个就说明游戏结束了，如果不是5个，就对计数-1，因为它的一边已经有了对方的一个棋子了，这时这个棋子的评分就需要降低了，如果后面遇到的是0，即空，那么就再往后看一个，如果这个还是空或者是对方的棋子，那么就结束计数，并且进行赋值，如果再往后的那个是自己方的棋子，那么就不用结束，反而继续往后看，不过这个空格这里的计数不+1。遍历这一个列表结束之后，依据存储的值进行评分赋值。算法如下：
  
  ![image](https://user-images.githubusercontent.com/65942634/233086207-6b9d3f8c-26e7-4bf5-9ea6-4750206425a3.png)


![image](https://user-images.githubusercontent.com/65942634/233086219-2eb815a9-14ef-42cb-98d6-c0963eaa4d44.png)


## 结果展示

![image](https://user-images.githubusercontent.com/65942634/233086306-53c73c9f-b4ce-4e3b-8e03-e6b060166cbf.png)

![image](https://user-images.githubusercontent.com/65942634/233086330-d9c7e58b-cbcb-4489-8808-a9ed9e0c5e06.png)

![image](https://user-images.githubusercontent.com/65942634/233086362-8964cca2-e381-4140-a335-78ee478ed293.png)

