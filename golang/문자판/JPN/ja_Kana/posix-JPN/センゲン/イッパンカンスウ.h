/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _センゲン_イッパンカンスウ
#define _センゲン_イッパンカンスウ
#include <キホンテイギ.h>
typedef struct { int ショウ; int アマリ; } セイスウジョザンケッカガタ;
typedef struct { long ショウ; long アマリ; } チョウセイスウジョザンケッカガタ;
#define セイコウシュウリョウ 0
#define シッパイシュウリョウ 1
void *キオクリョウイキヲカクホスル(オオキサガタ オオキサ);
void *レイデミタシタハイレツリョウイキヲカクホスル(オオキサガタ スウリョウ, オオキサガタ ヨウソノオオキサ);
void *キオクリョウイキノオオキサヲカエル(void *バンチ, オオキサガタ オオキサ);
void キオクリョウイキヲカエス(void *バンチ);
long モジレツヲチョウセイスウトシテヨム(const char *モジレツ, char **ヘンカンシュウタンバンチ, int キスウ);
unsigned long モジレツヲフゴウナシチョウセイスウトシテヨム(const char *モジレツ, char **ヘンカンシュウタンバンチ, int キスウ);
int ジュッシンモジレツヲセイスウトシテヨム(const char *モジレツ);
long ジュッシンモジレツヲチョウセイスウトシテヨム(const char *モジレツ);
int セイスウノゼッタイチヲエル(int アタイ);
long チョウセイスウノゼッタイチヲエル(long アタイ);
セイスウジョザンケッカガタ セイスウノショウトアマリヲエル(int ヒダリノアタイ, int ミギノアタイ);
チョウセイスウジョザンケッカガタ チョウセイスウノショウトアマリヲエル(long ヒダリノアタイ, long ミギノアタイ);
void ヒカクキジュンデセイレツスル(void *ヨウソハイレツ, オオキサガタ スウリョウ, オオキサガタ ヨウソノオオキサ,
           int (*ヒカクカンスウ)(const void *, const void *));
void *セイレツズミハイレツヲニブンタンサクスル(const void *ヨミダシモト, const void *ヨウソハイレツ, オオキサガタ スウリョウ,
              オオキサガタ ヨウソノオオキサ, int (*ヒカクカンスウ)(const void *, const void *));
char *カンキョウヘンスウノアタイヲエル(const char *ナマエ);
#endif
