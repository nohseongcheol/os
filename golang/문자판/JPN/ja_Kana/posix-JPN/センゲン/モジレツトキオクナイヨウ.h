/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _センゲン_モジレツトキオクナイヨウ
#define _センゲン_モジレツトキオクナイヨウ
#include <キホンテイギ.h>
void *キオクナイヨウヲフクシャスル(void *カキコミサキ, const void *ヨミダシモト, オオキサガタ ナガサ);
void *カサナリヲユルシテキオクナイヨウヲウツス(void *カキコミサキ, const void *ヨミダシモト, オオキサガタ ナガサ);
void *キオクリョウイキヲアタイデミタス(void *カキコミサキ, int モジチ, オオキサガタ ナガサ);
int キオクナイヨウヲヒカクスル(const void *ヒダリノアタイ, const void *ミギノアタイ, オオキサガタ ナガサ);
void *キオクリョウイキカラアタイヲサガス(const void *ヨミダシモト, int モジチ, オオキサガタ ナガサ);
オオキサガタ モジレツノハチケタグミスウヲエル(const char *モジレツ);
オオキサガタ ジョウゲンナイノモジレツハチケタグミスウヲエル(const char *モジレツ, オオキサガタ ジョウゲン);
char *モジレツヲフクシャスル(char *カキコミサキ, const char *ヨミダシモト);
char *ジョウゲンマデウメテモジレツヲフクシャスル(char *カキコミサキ, const char *ヨミダシモト, オオキサガタ ジョウゲン);
char *モジレツヲフクシャシテシュウタンヲエル(char *カキコミサキ, const char *ヨミダシモト);
char *ジョウゲンマデウメテフクシャシシュウタンヲエル(char *カキコミサキ, const char *ヨミダシモト, オオキサガタ ジョウゲン);
char *モジレツヲツケタス(char *カキコミサキ, const char *ヨミダシモト);
char *ジョウゲンナイデモジレツヲツケタス(char *カキコミサキ, const char *ヨミダシモト, オオキサガタ ジョウゲン);
int モジレツヲヒカクスル(const char *ヒダリノアタイ, const char *ミギノアタイ);
int ジョウゲンナイデモジレツヲヒカクスル(const char *ヒダリノアタイ, const char *ミギノアタイ, オオキサガタ ジョウゲン);
int セイレツキソクデモジレツヲヒカクスル(const char *ヒダリノアタイ, const char *ミギノアタイ);
オオキサガタ モジレツノセイレツカギヲツクル(char *カキコミサキ, const char *ヨミダシモト, オオキサガタ ジョウゲン);
char *モジレツカラサイショノアタイヲサガス(const char *モジレツ, int モジチ);
char *モジレツカラサイゴノアタイヲサガス(const char *モジレツ, int モジチ);
char *モジレツカラブブンレツヲサガス(const char *モジレツ, const char *ヨミダシモト);
オオキサガタ キョヨウチカラナルセントウチョウヲエル(const char *モジレツ, const char *クギリチシュウゴウ);
オオキサガタ ジョガイチノナイセントウチョウヲエル(const char *モジレツ, const char *クギリチシュウゴウ);
char *モジレツカラシュウゴウノアタイヲサガス(const char *モジレツ, const char *クギリチシュウゴウ);
char *モジレツヲゴニワケル(char *モジレツ, const char *クギリチシュウゴウ);
char *シンコウジョウタイヲシテイシテモジレツヲゴニワケル(char *モジレツ, const char *クギリチシュウゴウ, char **ホゾンシンコウジョウタイ);
char *アタラシイリョウイキニモジレツヲフクセイスル(const char *モジレツ);
char *ジョウゲンナイデアタラシイリョウイキニモジレツヲフクセイスル(const char *モジレツ, オオキサガタ ジョウゲン);
#endif
