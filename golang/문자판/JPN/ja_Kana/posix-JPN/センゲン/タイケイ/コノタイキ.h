/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _センゲン_タイケイ_コノタイキ
#define _センゲン_タイケイ_コノタイキ

#include <タイケイ/シリョウガタ.h>

#define ミジュンビナラマタナイ 1
#define シュウリョウチトリダシ(シュウリョウジョウタイ) (((シュウリョウジョウタイ) >> 8) & 0xff)
#define セイジョウシュウリョウハンテイ(シュウリョウジョウタイ) (((シュウリョウジョウタイ) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
ジッコウカテイバンゴウガタ コヲマツ(int *シュウリョウジョウタイ);
ジッコウカテイバンゴウガタ シテイシタコヲマツ(ジッコウカテイバンゴウガタ ジッコウカテイバンゴウ, int *シュウリョウジョウタイ, int センタクジコウ);
#ifdef __cplusplus
}
#endif

#endif
