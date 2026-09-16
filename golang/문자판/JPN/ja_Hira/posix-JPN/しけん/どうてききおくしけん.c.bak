#include <たいけい/このたいき.h>
#include <にゅうしゅつりょくとじっこう.h>

static void でんぶんをかく(const char *もじれつ, unsigned int おおきさ)
{
    (void)かく(ひょうじゅんしゅつりょくばんごう, もじれつ, おおきさ);
}

int main(void)
{
    volatile unsigned char *かいしいち = (volatile unsigned char *)どうてききおくのしゅうたんをうつす(0);
    volatile unsigned char *きおくりょういき;
    じっこうかていばんごうがた このいち;
    int しゅうりょうじょうたい;

    でんぶんをかく("\nPOSIX-HEAP:START\n", 18);
    きおくりょういき = (volatile unsigned char *)どうてききおくのしゅうたんをうつす(32);
    if (かいしいち == (void *)-1 || きおくりょういき != かいしいち || どうてききおくのしゅうたんをうつす(0) != (void *)(かいしいち + 32)) {
        でんぶんをかく("PTEST:FAIL:sbrk-grow\n", 22);
        ただちにしゅうりょうする(1);
    }
    でんぶんをかく("PTEST:PASS:sbrk-grow\n", 22);
    きおくりょういき[0] = 0x5a;
    きおくりょういき[31] = 0xa5;
    if (きおくりょういき[0] != 0x5a || きおくりょういき[31] != 0xa5) {
        でんぶんをかく("PTEST:FAIL:sbrk-memory\n", 24);
        ただちにしゅうりょうする(1);
    }
    でんぶんをかく("PTEST:PASS:sbrk-memory\n", 24);
    if (どうてききおくのしゅうたんをさだめる((void *)かいしいち) != 0 || どうてききおくのしゅうたんをうつす(0) != (void *)かいしいち) {
        でんぶんをかく("PTEST:FAIL:brk-restore\n", 24);
        ただちにしゅうりょうする(1);
    }
    でんぶんをかく("PTEST:PASS:brk-restore\n", 24);

    このいち = じっこうかていをぶんきする();
    if (このいち == 0) {
        if (どうてききおくのしゅうたんをうつす(64) != (void *)かいしいち)
            ただちにしゅうりょうする(2);
        ただちにしゅうりょうする(0);
    }
    if (このいち < 0 || していしたこをまつ(このいち, &しゅうりょうじょうたい, 0) != このいち ||
        !せいじょうしゅうりょうはんてい(しゅうりょうじょうたい) || しゅうりょうちとりだし(しゅうりょうじょうたい) != 0 ||
        どうてききおくのしゅうたんをうつす(0) != (void *)かいしいち) {
        でんぶんをかく("PTEST:FAIL:brk-process-isolation\n", 33);
        ただちにしゅうりょうする(1);
    }
    でんぶんをかく("PTEST:PASS:brk-process-isolation\n", 33);
    でんぶんをかく("POSIX-HEAP:PASS\n", 16);
    ただちにしゅうりょうする(0);
}
