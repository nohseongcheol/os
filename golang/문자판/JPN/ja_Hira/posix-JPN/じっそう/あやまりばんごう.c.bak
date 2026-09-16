#include <あやまりばんごう.h>
#include <たいけい/たいけいよびだし.h>

int あやまりばんごう;
char **かんきょうへんすういちらん;

long __syscall_result(long けっか)
{
    if ((unsigned long)けっか >= (unsigned long)-4095) {
        あやまりばんごう = (int)-けっか;
        return -1;
    }
    return けっか;
}
