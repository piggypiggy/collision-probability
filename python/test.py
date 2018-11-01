import numpy as np

def calc_collision(seqs, t, t_length, n):  
    total = t_length / n
    # 碰撞等于 ? 次的样本数
    n_col_samples = list(0 for i in range(n + 1))

    tmp = np.empty(t+1, np.int8)
    for i in range(int(total)):
        n_collisions = 0
        for k in range(n):
            tmp = seqs[:, i*n + k]
            for z in range(1, t+1):
                if(tmp[0] == tmp[z]):
                    n_collisions += 1
                    break
        
        n_col_samples[n_collisions] += 1
        n_collisions = 0
    
    return n_col_samples

def generate_seqs(n, m, t, t_length):
    a = np.arange(1, m+1, dtype=np.int8)
    seqs = np.empty([t+1, t_length], dtype=np.int8)
    total = int(t_length / n)
    for i in range(t+1):
        for k in range(total):
            np.random.shuffle(a)
            seqs[i, n*k : n*(k+1)] = a[0 : n]
    return seqs

# 仿真
def simulate(n, m, t, i):
    # 测试次数
    n_tests = 50
    
    # 每一次测试的样本数
    samples = 10000

    # 测试数列的长度
    t_length = samples * n

    # 总样本数
    total = samples * n_tests
    
    # 碰撞等于 ? 次的样本数
    n_col_samples = list(0 for i in range(n + 1))

    for _ in range(n_tests):
        # 生成 t+1 个随机数列
        seqs = generate_seqs(n, m, t, t_length)

        # 计算碰撞次数
        tmp = calc_collision(seqs, t, t_length, n)
        for i in range(n + 1):
            n_col_samples[i] += tmp[i]

    print("总共测试了", total, "个样本")
    for i in range(n + 1):
        print("碰撞次数等于", i, "的频率：", n_col_samples[i] / total)