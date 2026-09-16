/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <誤り番号.h>
#include <体系/体系呼出.h>

int 誤り番号;
char **環境変数一覧;

long __syscall_result(long 結果)
{
    if ((unsigned long)結果 >= (unsigned long)-4095) {
        誤り番号 = (int)-結果;
        return -1;
    }
    return 結果;
}
