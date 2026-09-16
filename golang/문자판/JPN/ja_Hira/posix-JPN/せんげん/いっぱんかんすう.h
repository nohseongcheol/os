/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _せんげん_いっぱんかんすう
#define _せんげん_いっぱんかんすう
#include <きほんていぎ.h>
typedef struct { int しょう; int あまり; } せいすうじょざんけっかがた;
typedef struct { long しょう; long あまり; } ちょうせいすうじょざんけっかがた;
#define せいこうしゅうりょう 0
#define しっぱいしゅうりょう 1
void *きおくりょういきをかくほする(おおきさがた おおきさ);
void *れいでみたしたはいれつりょういきをかくほする(おおきさがた すうりょう, おおきさがた ようそのおおきさ);
void *きおくりょういきのおおきさをかえる(void *ばんち, おおきさがた おおきさ);
void きおくりょういきをかえす(void *ばんち);
long もじれつをちょうせいすうとしてよむ(const char *もじれつ, char **へんかんしゅうたんばんち, int きすう);
unsigned long もじれつをふごうなしちょうせいすうとしてよむ(const char *もじれつ, char **へんかんしゅうたんばんち, int きすう);
int じゅっしんもじれつをせいすうとしてよむ(const char *もじれつ);
long じゅっしんもじれつをちょうせいすうとしてよむ(const char *もじれつ);
int せいすうのぜったいちをえる(int あたい);
long ちょうせいすうのぜったいちをえる(long あたい);
せいすうじょざんけっかがた せいすうのしょうとあまりをえる(int ひだりのあたい, int みぎのあたい);
ちょうせいすうじょざんけっかがた ちょうせいすうのしょうとあまりをえる(long ひだりのあたい, long みぎのあたい);
void ひかくきじゅんでせいれつする(void *ようそはいれつ, おおきさがた すうりょう, おおきさがた ようそのおおきさ,
           int (*ひかくかんすう)(const void *, const void *));
void *せいれつずみはいれつをにぶんたんさくする(const void *よみだしもと, const void *ようそはいれつ, おおきさがた すうりょう,
              おおきさがた ようそのおおきさ, int (*ひかくかんすう)(const void *, const void *));
char *かんきょうへんすうのあたいをえる(const char *なまえ);
#endif
