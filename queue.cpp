#include <queue>
#include <iostream>
#include <time.h>

int main(int argc, char **argv)
{
    std :: queue<int> speed_test;
    clock_t begin, end;
    double time_spent;

    begin = clock();
    for (size_t i = 0; i <= 20000000; i++)
    {
        speed_test.push(i);
    }

    end = clock();
    time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

    std :: cout <<time_spent << std::endl;

    return 0;
}
