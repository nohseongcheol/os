/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <あやまりばんごう.h>
#include <ぶんしょせいぎょ.h>
#include <たいけい/このたいき.h>
#include <にゅうしゅつりょくとじっこう.h>

static void でんぶんをかく(const char *もじれつ, unsigned int おおきさ)
{
    (void)かく(ひょうじゅんしゅつりょくばんごう, もじれつ, おおきさ);
}

int main(void)
{
    int しゅうりょうじょうたい;
    int ぶんしょきじゅつばんごう;
    char *ひきすういちらん[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *かんきょういちらん[] = {(char *)"POSIX_TEST=1", (char *)0};

    でんぶんをかく("\nPOSIX-EXEC:START\n", 18);
    あやまりばんごう = 0;
    if (していしたこをまつ(-1, &しゅうりょうじょうたい, みじゅんびならまたない) == -1 && あやまりばんごう == あやまりこじっこうかていなし)
        でんぶんをかく("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        でんぶんをかく("PTEST:FAIL:waitpid-echild-empty\n", 32);
    あやまりばんごう = 0;
    if (こをまつ(&しゅうりょうじょうたい) == -1 && あやまりばんごう == あやまりこじっこうかていなし)
        でんぶんをかく("PTEST:PASS:wait-echild-empty\n", 29);
    else
        でんぶんをかく("PTEST:FAIL:wait-echild-empty\n", 29);

    ぶんしょきじゅつばんごう = ひらく("/USER2", よみとりせんようでひらく);
    if (ぶんしょきじゅつばんごう < 0 || していばんごうにぶんしょさんしょうをふくせいする(ぶんしょきじゅつばんごう, 10) != 10 || ぶんしょをせいぎょする(10, きじゅつばんごうひょうしきせってい, じっこうないようちかんじにとじる) != 0) {
        でんぶんをかく("PTEST:FAIL:cloexec-setup\n", 25);
        ただちにしゅうりょうする(98);
    }
    if (ぶんしょきじゅつばんごう != 10)
        (void)とじる(ぶんしょきじゅつばんごう);

    (void)じっこうないようをおきかえる("/PXEXEC", ひきすういちらん, かんきょういちらん);
    でんぶんをかく("PTEST:FAIL:exec-image\n", 22);
    ただちにしゅうりょうする(99);
}
