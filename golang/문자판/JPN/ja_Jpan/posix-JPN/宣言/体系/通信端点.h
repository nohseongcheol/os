/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣言_体系_通信端点
#define _宣言_体系_通信端点

#include <基本定義.h>
#include <体系/資料型.h>

typedef unsigned short 番地系統型;

struct 通信端点番地 {
    番地系統型 端点番地系統;
    char 番地資料[14];
};

#define 番地系統未指定 0
#define 相互接続網番地系統 2
#define 相互接続網規約系統 相互接続網番地系統

#define 資料流端点 1
#define 資料電文端点 2

#define 受信停止 0
#define 送信停止 1
#define 双方向停止 2

#ifdef __cplusplus
extern "C" {
#endif
int 通信端点を作る(int 番地系統, int 端点種類, int 通信規約);
int 局所番地を結ぶ(int 文書記述番号, const struct 通信端点番地 *番地, 番地長型 番地寸法);
int 相手端点につなぐ(int 文書記述番号, const struct 通信端点番地 *番地, 番地長型 番地寸法);
int 接続要求に備える(int 文書記述番号, int 待機上限);
int 接続要求を受け入れる(int 文書記述番号, struct 通信端点番地 *番地, 番地長型 *番地寸法);
int 局所端点の番地を得る(int 文書記述番号, struct 通信端点番地 *番地, 番地長型 *番地寸法);
int 相手端点の番地を得る(int 文書記述番号, struct 通信端点番地 *番地, 番地長型 *番地寸法);
符号付き大きさ型 送る(int 文書記述番号, const void *資料緩衝領域, 大きさ型 長さ, int 処理指定);
符号付き大きさ型 受け取る(int 文書記述番号, void *資料緩衝領域, 大きさ型 長さ, int 処理指定);
符号付き大きさ型 宛先に送る(int 文書記述番号, const void *電文, 大きさ型 長さ, int 処理指定,
               const struct 通信端点番地 *宛先番地, 番地長型 宛先番地長);
符号付き大きさ型 送信元と共に受け取る(int 文書記述番号, void *資料緩衝領域, 大きさ型 長さ, int 処理指定,
                 struct 通信端点番地 *番地, 番地長型 *番地寸法);
int 通信方向を閉じる(int 文書記述番号, int 閉じる方向);
int 通信端点を設定する(int 文書記述番号, int 設定階層, int 設定名,
               const void *設定値, 番地長型 設定長);
#ifdef __cplusplus
}
#endif

#endif
