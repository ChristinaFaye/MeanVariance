>在这篇里主要讲用另一种方法求解均值方差理论，通过拉格朗日乘子法把二次规划问题转换成多元一次方程组，进而求解。

**我们先回顾一下，用数学的方式表达均值方差理论是什么样的：**
$$
\mathop{min}\limits_{\omega}\sigma^2(R_p)=\bm{\omega^T\Sigma\omega}\\
s.t.\begin{cases}\bm{\mu\omega}=\mu_0\\ \bm{\varphi\omega}=1 \quad where\,\bm{\varphi}=(\underbrace{1,1,\cdots,1}_n)
\end{cases}
$$
在限制条件**①加权平均收益率=期望收益率**和**②权重总和=1**下求出满足方差最小的参数ω1、ω2…ωn。
为了比较好理解，我们先从简单的例子入手，假设我们现在只有两只股票，那么问题就简化为：
$$
\mathop{min}\limits_{\omega_1,\omega_2}\sigma^2(R_p)=\omega_1^2\sigma_{11}+\omega_2^2\sigma_{22}+2\omega_1\omega_2\sigma_{12} \\s.t.\begin{cases}\mu_1\omega_1+\mu_2\omega_2=\mu_0\\\omega_1+\omega_2=1\end{cases}
$$
根据拉格朗日乘子法，我们设
$$
\begin{cases}f(\omega_1,\omega_2)=\omega_1^2\sigma_{11}+\omega_2^2\sigma_{22}+2\omega_1\omega_2\sigma_{12}\\g(\omega_1,\omega_2)=\mu_1\omega_1+\mu_2\omega_2-\mu_0\\h(\omega_1,\omega_2)=\omega_1+\omega_2-1\end{cases}
$$
然后构造函数：
$$
f(\omega_1,\omega_2)-\lambda_1g(\omega_1,\omega_2)-\lambda_2h(\omega_1,\omega_2)=0
$$
分别对ω1，ω2，λ1，λ2求导得：
$$
\begin{cases}2\omega_1\sigma_{11}+2\omega_2\sigma_{12}-\lambda_1\mu_1-\lambda_2=0\\2\omega_2\sigma_{22}+2\omega_1\sigma_{12}-\lambda_1\mu_2-\lambda_2=0\\\mu_1\omega_1+\mu_2\omega_2-\mu_0=0\\\omega_1+\omega_2-1=0
\end{cases}
$$
通过上面四个方程，我们可以轻松求出ω1，ω2，λ1，λ2。
现在，我们把这个例子推广到n只股票上：
$$
\begin{cases}2\omega_1\sigma_{11}+2\omega_2\sigma_{12}+\cdots+2\omega_n\sigma_{2n}-\lambda_1\mu_1-\lambda_2=0\\2\omega_1\sigma_{21}+2\omega_2\sigma_{22}+\cdots+2\omega_n\sigma_{2n}-\lambda_1\mu_2-\lambda_2=0\\\vdots\\2\omega_1\sigma_{n1}+2\omega_2\sigma_{n2}+\cdots+2\omega_n\sigma_{nn}-\lambda_1\mu_n-\lambda_2=0\\\mu_1\omega_1+\mu_2\omega_2+\cdots+\mu_n\omega_n-\mu_0=0\\\omega_1+\omega_2+\cdots+\omega_n-1=0
\end{cases}
$$
用矩阵形式来表示，为了使式子更加简洁，把方程组前n个式子分别除以2，并用新的λ1,λ2来代替-λ1/2,-λ2/2，因为我们并不关心λ1,λ2的具体值，这样我们可以设：
$$
\bm{L}=\left(\begin{matrix}\sigma_{11}&\sigma_{12}&\cdots&\sigma_{1n}&\mu_1&1\\\sigma_{21}&\sigma_{22}&\cdots&\sigma_{2n}&\mu_2&1\\\vdots&\vdots&\ddots&\vdots&\vdots&\vdots\\\sigma_{n1}&\sigma_{n2}&\cdots&\sigma_{nn}&\mu_n&1\\\mu_1&\mu_2&\cdots&\mu_n&0&0\\1&1&\cdots&1&0&0
  \end{matrix}\right)
$$
$$
\bm{X}=\left(\begin{matrix}\omega_1\\\omega_2\\\vdots\\\omega_n\\\lambda_1\\\lambda_2\end{matrix}\right) \;\bm{B}=\left(\begin{matrix}0\\0\\\vdots\\0\\\mu_0\\1\end{matrix}\right)
$$
我们需要求解的式子就是
$$
\bm{LX=B}
$$
