/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <タイケイ/コノタイキ.h>
#include <ニュウシュツリョクトジッコウ.h>

static void デンブンヲカク(const char *モジレツ, unsigned int オオキサ)
{
    (void)カク(ヒョウジュンシュツリョクバンゴウ, モジレツ, オオキサ);
}

int main(void)
{
    volatile unsigned char *カイシイチ = (volatile unsigned char *)ドウテキキオクノシュウタンヲウツス(0);
    volatile unsigned char *キオクリョウイキ;
    ジッコウカテイバンゴウガタ コノイチ;
    int シュウリョウジョウタイ;

    デンブンヲカク("\nPOSIX-HEAP:START\n", 18);
    キオクリョウイキ = (volatile unsigned char *)ドウテキキオクノシュウタンヲウツス(32);
    if (カイシイチ == (void *)-1 || キオクリョウイキ != カイシイチ || ドウテキキオクノシュウタンヲウツス(0) != (void *)(カイシイチ + 32)) {
        デンブンヲカク("PTEST:FAIL:sbrk-grow\n", 22);
        タダチニシュウリョウスル(1);
    }
    デンブンヲカク("PTEST:PASS:sbrk-grow\n", 22);
    キオクリョウイキ[0] = 0x5a;
    キオクリョウイキ[31] = 0xa5;
    if (キオクリョウイキ[0] != 0x5a || キオクリョウイキ[31] != 0xa5) {
        デンブンヲカク("PTEST:FAIL:sbrk-memory\n", 24);
        タダチニシュウリョウスル(1);
    }
    デンブンヲカク("PTEST:PASS:sbrk-memory\n", 24);
    if (ドウテキキオクノシュウタンヲサダメル((void *)カイシイチ) != 0 || ドウテキキオクノシュウタンヲウツス(0) != (void *)カイシイチ) {
        デンブンヲカク("PTEST:FAIL:brk-restore\n", 24);
        タダチニシュウリョウスル(1);
    }
    デンブンヲカク("PTEST:PASS:brk-restore\n", 24);

    コノイチ = ジッコウカテイヲブンキスル();
    if (コノイチ == 0) {
        if (ドウテキキオクノシュウタンヲウツス(64) != (void *)カイシイチ)
            タダチニシュウリョウスル(2);
        タダチニシュウリョウスル(0);
    }
    if (コノイチ < 0 || シテイシタコヲマツ(コノイチ, &シュウリョウジョウタイ, 0) != コノイチ ||
        !セイジョウシュウリョウハンテイ(シュウリョウジョウタイ) || シュウリョウチトリダシ(シュウリョウジョウタイ) != 0 ||
        ドウテキキオクノシュウタンヲウツス(0) != (void *)カイシイチ) {
        デンブンヲカク("PTEST:FAIL:brk-process-isolation\n", 33);
        タダチニシュウリョウスル(1);
    }
    デンブンヲカク("PTEST:PASS:brk-process-isolation\n", 33);
    デンブンヲカク("POSIX-HEAP:PASS\n", 16);
    タダチニシュウリョウスル(0);
}
