/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _せんげん_ぶんしょせいぎょ
#define _せんげん_ぶんしょせいぎょ

#include <たいけい/しりょうがた.h>

#define よみとりせんようでひらく 0x0000
#define かきこみせんようでひらく 0x0001
#define よみかきりょうようでひらく 0x0002
#define りようほうしきちゅうしゅつち 0x0003
#define なければつくる 0x0040
#define しんきぶんしょのみゆるす 0x0080
#define きぞんないようをからにする 0x0200
#define まつびへついかする 0x0400
#define もくろくのみゆるす 0x10000

#define きじゅつばんごうふくせい 0
#define きじゅつばんごうひょうしきしゅとく 1
#define きじゅつばんごうひょうしきせってい 2
#define ぶんしょじょうたいひょうしきしゅとく 3
#define ぶんしょじょうたいひょうしきせってい 4
#define じっこうないようちかんじにとじる 1

#ifdef __cplusplus
extern "C" {
#endif
int ひらく(const char *けいろ, int ひらくさいのしてい, ...);
int ぶんしょをつくる(const char *けいろ, ぶんしょほうしきがた りようほうしき);
int ぶんしょをせいぎょする(int ぶんしょきじゅつばんごう, int せいぎょめいれい, ...);
#ifdef __cplusplus
}
#endif

#endif
