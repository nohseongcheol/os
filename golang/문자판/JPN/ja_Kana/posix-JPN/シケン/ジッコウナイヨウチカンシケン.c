#include <アヤマリバンゴウ.h>
#include <ブンショセイギョ.h>
#include <タイケイ/コノタイキ.h>
#include <ニュウシュツリョクトジッコウ.h>

static void デンブンヲカク(const char *モジレツ, unsigned int オオキサ)
{
    (void)カク(ヒョウジュンシュツリョクバンゴウ, モジレツ, オオキサ);
}

int main(void)
{
    int シュウリョウジョウタイ;
    int ブンショキジュツバンゴウ;
    char *ヒキスウイチラン[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *カンキョウイチラン[] = {(char *)"POSIX_TEST=1", (char *)0};

    デンブンヲカク("\nPOSIX-EXEC:START\n", 18);
    アヤマリバンゴウ = 0;
    if (シテイシタコヲマツ(-1, &シュウリョウジョウタイ, ミジュンビナラマタナイ) == -1 && アヤマリバンゴウ == アヤマリコジッコウカテイナシ)
        デンブンヲカク("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        デンブンヲカク("PTEST:FAIL:waitpid-echild-empty\n", 32);
    アヤマリバンゴウ = 0;
    if (コヲマツ(&シュウリョウジョウタイ) == -1 && アヤマリバンゴウ == アヤマリコジッコウカテイナシ)
        デンブンヲカク("PTEST:PASS:wait-echild-empty\n", 29);
    else
        デンブンヲカク("PTEST:FAIL:wait-echild-empty\n", 29);

    ブンショキジュツバンゴウ = ヒラク("/USER2", ヨミトリセンヨウデヒラク);
    if (ブンショキジュツバンゴウ < 0 || シテイバンゴウニブンショサンショウヲフクセイスル(ブンショキジュツバンゴウ, 10) != 10 || ブンショヲセイギョスル(10, キジュツバンゴウヒョウシキセッテイ, ジッコウナイヨウチカンジニトジル) != 0) {
        デンブンヲカク("PTEST:FAIL:cloexec-setup\n", 25);
        タダチニシュウリョウスル(98);
    }
    if (ブンショキジュツバンゴウ != 10)
        (void)トジル(ブンショキジュツバンゴウ);

    (void)ジッコウナイヨウヲオキカエル("/PXEXEC", ヒキスウイチラン, カンキョウイチラン);
    デンブンヲカク("PTEST:FAIL:exec-image\n", 22);
    タダチニシュウリョウスル(99);
}
