#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int n;
long long *fib;

// 子线程执行的函数
void *generate_fibonacci(void *arg)
{
    if (n >= 1)
        fib[0] = 0;

    if (n >= 2)
        fib[1] = 1;

    for (int i = 2; i < n; i++)
    {
        fib[i] = fib[i - 1] + fib[i - 2];
    }

    pthread_exit(NULL);
    return NULL;
}

int main()
{
    pthread_t tid;

    // 从命令行输入要生成多少个 Fibonacci 数
    printf("Enter the number of Fibonacci numbers: ");
    scanf("%d", &n);

    // 创建共享数组
    fib = (long long *)malloc(n * sizeof(long long));

    // 创建子线程
    pthread_create(&tid, NULL, generate_fibonacci, NULL);

    // 等待子线程执行结束
    pthread_join(tid, NULL);

    // 子线程结束后，父线程输出结果
    printf("Fibonacci sequence:\n");

    for (int i = 0; i < n; i++)
    {
        printf("%lld ", fib[i]);
    }

    printf("\n");

    free(fib);

    return 0;
}