#include <gmpxx.h>
#include <iostream>
#include <iomanip>

using namespace std;

mpz_t fac;
mpz_class fac_class1;
mpz_class fac_class2;

mpz_t cc, nn;

mpz_class  *_S_;
mpz_class **_T_;
mpz_class  *_N_;
mpq_class  *_Q_;
mpq_class  *_W_;

mpz_class C(unsigned int k, unsigned int n)
{
    mpz_set_ui(nn, n);

    /* C(k,n) */
    mpz_bin_ui(cc, nn, k);

    mpz_class ret(cc);
    return ret;
}

mpz_class S(int n)
{
    if(n <= 1)
        return 0;
    if(n == 2)
        return 1;

    if(cmp(_S_[n], 0) > 0)
    {
        return _S_[n];
    }
    else
    {
        _S_[n] = (n-1) * (S(n-1) + S(n-2));
        return _S_[n];
    }
}

mpz_class T(int n, int m)
{
    mpz_class ret;
    if(n == m)
    {
        if(n == 0)
            return 1;

        _T_[n][n] = S(n);
        return _T_[n][n];
    }

    if(cmp(_T_[n][m], 0) > 0)
    {
        return _T_[n][m];
    }

    mpz_class sumT = 0;
    int max_k = n < (m-n) ? n : (m-n);
    for(int k = 0; k < max_k; k++)
    {
        sumT = sumT + T(n, n+k) * T(m-n, m-n+k);
        mpz_fac_ui(fac, m-n);
        fac_class1 = mpz_class(fac);
        _T_[n][m] = (T(m, m) - sumT) / fac_class1;
    }
    return _T_[n][m];
}

/* i : 已经碰撞了几次，问题变成总共 m-i 个符号，分为左边 n-i 个符号和右边 m-n 个符号 */
mpz_class N(int n, int m, int i)
{
    if(cmp(_N_[i], 0) > 0)
        return _N_[i];

    /* max_k : 最多能向左边放入多少个符号 */
    int max_k = n-i < m-n ? n-i : m-n;
    for(int k = 0; k < (1 + max_k); k++)
    {
        /* 
           C(k, m-n) : 从右边 m-n 个符号中选取 k 个符号有多少种可能
           T(n-i, n-i+k) : ...
        */
        _N_[i] += C(k, m-n) * T(n-i, n-i+k);
    }
    return _N_[i];
}

void mpq_pow(mpq_class *base, unsigned int exp)
{
    mpz_ptr num = base->get_num_mpz_t();
    mpz_ptr den = base->get_den_mpz_t();

    mpz_pow_ui(num, num, exp);
    mpz_pow_ui(den, den, exp);
}

/* 碰撞限制在某 i 项中时，t+1 条数列碰撞次数小于等于 i 次的概率 */
mpq_class Q(int n, int m, int t, int i)
{
    if(cmp(_Q_[i], 0) > 0)
        return _Q_[i];

    mpz_class sum = 0;
    int max_i = i;
    for(int z = 0; z < (1 + max_i); z++)
    {
        sum = sum + C(z, i) * N(n, m, z);
    }
    mpz_fac_ui(fac, m);
    fac_class1 = mpz_class(fac);
    mpz_fac_ui(fac, m-n);
    fac_class2 = mpz_class(fac);

    sum *= fac_class2;
    _Q_[i] = mpq_class(sum, fac_class1);
    _Q_[i].canonicalize();

    mpq_pow(&_Q_[i], t);
    return _Q_[i];
}

mpq_class W(int n, int m, int t, int i)
{
    if(i == 0)
        if(cmp(_W_[0], 0) > 0)
            return _W_[0];
        else
        {
            _W_[0] = Q(n, m, t, 0);
            return _W_[0];
        }
    
    if(cmp(_W_[i], 0) > 0)
        return _W_[i];
    
    _W_[i] = Q(n, m, t, i);
    for(int z = 0; z < i; z++)
    {
        _W_[i] = _W_[i] - C(z, i) * W(n, m, t, z);
        _W_[i].canonicalize();
    }
    return _W_[i];
}

int main(int argc, char **argv)
{
    int n, m, t, i;
    
    if(argc == 4)
    {
        n = atoi(argv[1]);
        m = atoi(argv[2]);
        t = atoi(argv[3]);

        _S_ = new mpz_class[m+1];
        _T_ = new mpz_class*[m+1];
        for(int z = 0; z < m + 1; z++)
            _T_[z] = new mpz_class[m+1];
        _N_ = new mpz_class[m+1];
        _Q_ = new mpq_class[m+1];
        _W_ = new mpq_class[m+1];

        mpz_init(fac);
        mpz_init(cc);
        mpz_init(nn);
        
        cout << "n = " << n << endl;
        cout << "m = " << m << endl;
        cout << t+1 << "个数列" << endl;
        cout << endl << "理论值:" << endl;

        mpf_class prob(0, 50);
        for(i = 0; i <= n; i++)
        {
            prob = mpf_class(C(i, n) * W(n, m, t, i));
            cout << setprecision(15) << "碰撞次数等于" << i << "的概率: " << prob << endl;
            //gmp_printf("碰撞次数等于%d的概率: %.0Ff \n", i, prob.get_mpf_t ());
        }
    }

    /* delete ... */
    return 0;
}
