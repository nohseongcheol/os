/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣言_体系_文書状態
#define _宣言_体系_文書状態

#include <体系/資料型.h>

#define 文書種類抽出値 0170000
#define 目録種類 0040000
#define 文字装置種類 0020000
#define 通常文書種類 0100000
#define 所有者読取権限 0400
#define 所有者書込権限 0200
#define 所有者実行権限 0100
#define 所属組読取権限 0040
#define 所属組書込権限 0020
#define 所属組実行権限 0010
#define 他者読取権限 0004
#define 他者書込権限 0002
#define 他者実行権限 0001
#define 目録方式判定(検査方式) (((検査方式) & 文書種類抽出値) == 目録種類)
#define 文字装置方式判定(検査方式) (((検査方式) & 文書種類抽出値) == 文字装置種類)
#define 通常文書方式判定(検査方式) (((検査方式) & 文書種類抽出値) == 通常文書種類)

struct 文書状態 {
    装置番号型 所属装置番号;
    文書固有番号型 文書固有番号;
    文書方式型 文書種類と権限;
    直接連結数型 直接連結数;
    利用者番号型 所有利用者番号;
    所属組番号型 所有組番号;
    装置番号型 表す装置番号;
    文書位置型 文書の大きさ;
    区画長型 推奨入出力区画長;
    区画数型 割当区画数;
    時刻値型 最終参照時刻;
    int 最終参照十億分秒;
    時刻値型 最終内容変更時刻;
    int 最終内容変更十億分秒;
    時刻値型 最終状態変更時刻;
    int 最終状態変更十億分秒;
};

#ifdef __cplusplus
extern "C" {
#endif
int 文書状態(const char *経路, struct 文書状態 *緩衝領域);
int 連結自体の状態を得る(const char *経路, struct 文書状態 *緩衝領域);
int 開いた文書の状態を得る(int 文書記述番号, struct 文書状態 *緩衝領域);
#ifdef __cplusplus
}
#endif

#endif
