/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <錯誤編號.h>
#include <系統/系統呼叫.h>

int 錯誤編號;
char **環境變數列表;

long __syscall_result(long 結果)
{
    if ((unsigned long)結果 >= (unsigned long)-4095) {
        錯誤編號 = (int)-結果;
        return -1;
    }
    return 結果;
}
