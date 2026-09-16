/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _せんげん_たいけい_このたいき
#define _せんげん_たいけい_このたいき

#include <たいけい/しりょうがた.h>

#define みじゅんびならまたない 1
#define しゅうりょうちとりだし(しゅうりょうじょうたい) (((しゅうりょうじょうたい) >> 8) & 0xff)
#define せいじょうしゅうりょうはんてい(しゅうりょうじょうたい) (((しゅうりょうじょうたい) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
じっこうかていばんごうがた こをまつ(int *しゅうりょうじょうたい);
じっこうかていばんごうがた していしたこをまつ(じっこうかていばんごうがた じっこうかていばんごう, int *しゅうりょうじょうたい, int せんたくじこう);
#ifdef __cplusplus
}
#endif

#endif
