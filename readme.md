# Plants VS ZOMBIES

Python开发植物大战僵尸游戏用pygame框架。

本实现参考了仓库：https://github.com/371854496/pygame.git，感谢。

## 玩法：

鼠标左键：种植太阳花，收取阳光。

鼠标右键：种植植物

空格：调出铲子。

空格+左键：铲除植物。

## 先决条件

```bash
python==3.9.16
pygame==2.6.1
```

## 运行游戏

```bash
git clone https://github.com/yinlikestudy/Plants-vs.-Zombies-Simple-Version.git
cd Plants-vs.-Zombies-Simple-Version
python mygame.py
```

## 已完成功能 (do)

### v0.5:

1. 战斗场景
2. 植物种
3. 僵尸移动，攻击
4. 死亡动画，胜利结算画面
5. 设置关卡的等级，改造成无尽模式

### v1.0:

1. 添加太阳花，豌豆射手，僵尸默认动态动画
2. 添加种植音效，下一关的音效，被咬的音效，攻击的音效
3. 太阳花产生的阳光改成点击收取式
   - 太阳4秒没人收自动收取
4. 僵尸的死亡动画，添加一个死亡僵尸列表实现
5. 添加背景音乐
6. 植物死亡音效，子弹命中的音效
7. 铲子，按空格呼出铲子

## 待完成功能 (todo)

1. 植物卡槽，植物冷却



-----



# Plants VS ZOMBIES

Develop Plants vs Zombies game using Pygame framework in Python.

This implementation references the repository: https://github.com/371854496/pygame.git, thanks.

## Gameplay:

Left Mouse Button: Plant Sunflower, collect sunlight.

Right Mouse Button: Plant other plants.

Space: Bring up the shovel.

Space + Left Mouse Button: Remove plants.

## Prerequisites

```bash
python==3.9.16
pygame==2.6.1
```

## Run the Game

```bash
git clone https://github.com/yinlikestudy/Plants-vs.-Zombies-Simple-Version.git
cd Plants-vs.-Zombies-Simple-Version
python mygame.py
```

## Completed Features (do)

### v0.5:

1. Battle scenes
2. Planting plants
3. Zombie movement and attack
4. Death animation, victory screen
5. Set level difficulty, transformed into endless mode

### v1.0:

1. Added Sunflower, Peashooter, default zombie animations
2. Added planting sound effects, next level sound effects, biting sound effects, attack sound effects
3. Sunflower's sunlight changed to click-to-collect
   - Sunlight auto-collects after 4 seconds if not collected
4. Zombie death animation, added a dead zombie list implementation
5. Added background music
6. Plant death sound effects, bullet hit sound effects
7. Shovel, press space to bring up the shovel

## To-Do Features (todo)

1. Plant card slots, plant cooldown