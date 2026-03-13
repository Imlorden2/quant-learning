



## python-dotenv 库

python-dotenv 是一个Python库，用于从 `.env` 文件中读取键值对并将它们作为环境变量设置。这是基于 **Twelve-Factor App**方法论的配置管理最佳实践。

**Twelve-Factor App** 

是由 Heroku 联合创始人 Adam Wiggins 在 2011年提出的现代应用程序开发方法论。它定义了构建 软件即服务 (SaaS)应用程序的12个最佳实践原则

**十二要素应用程序原则**：

```
1. 代码库 (Codebase)：一个代码库，多个部署
- 使用版本控制系统（如Git）管理代码
- 一个应用对应一个代码库
- 可以部署到多个环境（开发、测试、生产）

2. 依赖 (Dependencies)：显式声明和隔离依赖
# requirements.txt
pandas==1.5.0
tushare==1.2.89
python-dotenv==1.0.0

3. 配置 (Config)：在环境变量中存储配置
# 错误：硬编码配置
DATABASE_URL = "postgresql://user:pass@localhost/db"

# 正确：环境变量配置
DATABASE_URL = os.getenv('DATABASE_URL')

4. 后端服务 (Backing Services)：把后端服务当作附加资源
- 数据库、消息队列、缓存等都是附加服务
- 通过配置连接，可随时替换

5. 构建、发布、运行 (Build, Release, Run)：严格分离构建和运行阶段
# 构建阶段：代码 + 依赖 → 构建产物
docker build -t myapp .

# 发布阶段：构建产物 + 配置 → 发布版本
docker tag myapp:latest myapp:v1.2.3

# 运行阶段：启动发布版本
docker run -e DATABASE_URL=... myapp:v1.2.3

6. 进程 (Processes)：以一个或多个无状态进程运行应用
- 进程是无状态的
- 不依赖本地缓存
- 数据存储在后端服务中

7. 端口绑定 (Port Binding)：通过端口绑定提供服务
# Flask应用
app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

8. 并发 (Concurrency)：通过进程模型进行扩展
- 水平扩展：增加进程数量
- 不同类型的工作负载可以分配给不同的进程类型

9. 易处理 (Disposability)：快速启动和优雅终止可最大化健壮性
- 进程应该快速启动
- 收到SIGTERM信号时优雅关闭

10. 开发环境与线上环境等价 (Dev/Prod Parity)：尽可能的保持开发，预发布，线上环境相同
# docker-compose.yml - 保证环境一致性
services:
  app:
    image: python:3.9
    environment:
      - DATABASE_URL=postgresql://...
  db:
    image: postgres:13

11. 日志 (Logs)：把日志当作事件流
import logging
import sys

# 输出到stdout，不要写文件
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

12. 管理进程 (Admin Processes)：后台管理任务当作一次性进程运行
# 数据库迁移作为一次性任务
python manage.py migrate

# 数据导入脚本
python scripts/import_data.py
```





### .env 文件

---

`.env` 文件通常是用于存储**环境变量**的配置文件，在软件开发中广泛使用。

- 语法格式为 `KEY=VALUE`，无空格
- 同步创建 `.env.example` ，存放环境变量模式，从而方便其他开发者自行复制、配置
- **永远不要提交 .env 到 Git，记得在 `.gitignore` 文件中添加 `.env`**



### 使用方法

---

```python
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()
# 自行设置位置使用 load_dotenv('/path/to/your/.env')

# 读取环境变量
secret_key = os.getenv('SECRET_KEY')
```


## 概率论

### 一、大数定律

样本量足够大时，样本平均值会趋近于总体真实期望值。

```python
"""验证大数定律"""
import numpy as np
import matplotlib.pyplot as plt

n = 10000 # 实验次数
coin_exp = np.random.binomial(1, 0.5, n) # 100次硬币投掷结果

cumsum = np.cumsum(coin_exp) # 累计概率分布
trials = np.arange(1, 100+1)
running_prob = cumsum / trials # 计算样本平均值

plt.figure(figsize=(16, 9)) # 设置图像大小
plt.plot(trials, running_prob, 'b-', alpha=0.7) # 绘制累计概率曲线
plt.axhline(y=0.5, color='r', linestyle='--', label='theoretical = 0.5') # 添加理论概率水平线
plt.title('Toss the coin 100 times - Law of Large Numbers Demo') # 设置标题
plt.xlabel('Number of Trials') # 设置 x 轴标签
plt.ylabel('Probability of Heads') # 设置 y 轴标签
plt.ylim(0, 1) # 设置 y 轴范围
plt.legend() # 显示图例
plt.grid(True) # 添加网格
plt.show() # 显示图像
```



### 概率分布

```python
"""正态分布"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


x = np.linspace(-4, 4, 1000)
plt.figure(figsize=(16, 9))
for mu, sigma in [(0, 1), (0, 0.5), (1, 1)]:
    y = stats.norm.pdf(x, mu, sigma)
    plt.plot(x, y, label=f'N({mu}, {sigma}²)')
plt.title('normal distribution')
plt.legend()
plt.grid(True)
```

```python
"""t 分布"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


plt.figure(figsize=(16, 9))
x = np.linspace(-4, 4, 1000)
for df in (1, 5, 10):
    y = stats.t.pdf(x, df)
    plt.plot(x, y, label=f'df {df}')
plt.title('t distribution')
plt.grid(True)
plt.legend()
plt.show()
```


```python
"""对数正态分布"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

plt.figure(figsize=(16, 9))
x_log = np.linspace(0.01, 5, 1000)
for sigma in [0.5, 1, 1.5]:
    y = stats.lognorm.pdf(x_log, sigma)
    plt.plot(x_log, y, label=f'LogN(0, {sigma}²)')
plt.title('Log-normal Distribution')
plt.legend()
plt.grid(True)
plt.show()
```

```python
"""指数分布"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

plt.figure(figsize=(16, 9))
x_exp = np.linspace(0, 5, 1000)
for lam in [0.5, 1, 2]:
    y = stats.expon.pdf(x_exp, scale=1 / lam)
    plt.plot(x_exp, y, label=f'Exp(λ={lam})')
plt.title('Exponential Distribution')
plt.legend()
plt.grid(True)
plt.show()
```

```python
"""二项分布"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

plt.figure(figsize=(16, 9))
x_binom = np.arange(0, 21)
for n, p in [(20, 0.3), (20, 0.5), (20, 0.7)]:
    y = stats.binom.pmf(x_binom, n, p)
    plt.plot(x_binom, y, 'o-', label=f'B({n}, {p})')
plt.title('Binomial Distribution')
plt.legend()
plt.grid(True)
plt.show()
```

```python
"""泊松分布"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

plt.figure(figsize=(16, 9))
x_poisson = np.arange(0, 15)
for lam in [1, 3, 5]:
    y = stats.poisson.pmf(x_poisson, lam)
    plt.plot(x_poisson, y, 'o-', label=f'Poisson(λ={lam})')
plt.title('Poisson Distribution')
plt.legend()
plt.grid(True)
plt.show()
```