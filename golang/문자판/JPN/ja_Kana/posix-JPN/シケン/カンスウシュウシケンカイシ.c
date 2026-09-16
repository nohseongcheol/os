/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <ニュウシュツリョクトジッコウ.h>
int カンスウシュウノドウサヲタメス(void);
int main(void)
{
    int シッパイギョウバンゴウ = カンスウシュウノドウサヲタメス();
    if (シッパイギョウバンゴウ) {
        char シリョウカンショウリョウイキ[16];
        int ナガサ = 0;
        カク(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { シリョウカンショウリョウイキ[ナガサ++] = (char)('0' + シッパイギョウバンゴウ % 10); シッパイギョウバンゴウ /= 10; } while (シッパイギョウバンゴウ);
        while (ナガサ) カク(1, &シリョウカンショウリョウイキ[--ナガサ], 1);
        カク(1, "\n", 1);
        return 1;
    }
    return カク(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
