/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <ニュウシュツリョクトジッコウ.h>

static void デンブンヲカク(const char *モジレツ, unsigned int オオキサ)
{
    (void)カク(ヒョウジュンシュツリョクバンゴウ, モジレツ, オオキサ);
}

int main(void)
{
    char ニュウリョクイチ[4];
    フゴウツキオオキサガタ スウリョウ;

    デンブンヲカク("\nPOSIX-STDIN:READY\n", 19);
    スウリョウ = ヨム(ヒョウジュンニュウリョクバンゴウ, ニュウリョクイチ, sizeof(ニュウリョクイチ));
    if (スウリョウ == 2 && ニュウリョクイチ[0] == 'a' && ニュウリョクイチ[1] == '\n') {
        デンブンヲカク("POSIX-STDIN:PASS\n", 17);
        タダチニシュウリョウスル(0);
    }
    デンブンヲカク("POSIX-STDIN:FAIL\n", 17);
    タダチニシュウリョウスル(1);
}
