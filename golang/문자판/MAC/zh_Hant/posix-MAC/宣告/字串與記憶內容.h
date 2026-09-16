/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣告_字串與記憶內容
#define _宣告_字串與記憶內容
#include <基本定義.h>
void *複製記憶內容(void *目標位置, const void *來源位置, 大小型別 長度);
void *允許重疊移動記憶內容(void *目標位置, const void *來源位置, 大小型別 長度);
void *以值填滿記憶區域(void *目標位置, int 字元值, 大小型別 長度);
int 比較記憶內容(const void *左值, const void *右值, 大小型別 長度);
void *在記憶中尋找值(const void *來源位置, int 字元值, 大小型別 長度);
大小型別 取得字串位元組數(const char *字串);
大小型別 取得限長字串位元組數(const char *字串, 大小型別 上限);
char *複製字串(char *目標位置, const char *來源位置);
char *定長填補複製字串(char *目標位置, const char *來源位置, 大小型別 上限);
char *複製字串並取得末端(char *目標位置, const char *來源位置);
char *定長填補複製並取得末端(char *目標位置, const char *來源位置, 大小型別 上限);
char *附加字串(char *目標位置, const char *來源位置);
char *限長附加字串(char *目標位置, const char *來源位置, 大小型別 上限);
int 比較字串(const char *左值, const char *右值);
int 限長比較字串(const char *左值, const char *右值, 大小型別 上限);
int 依排序規則比較字串(const char *左值, const char *右值);
大小型別 產生字串排序鍵(char *目標位置, const char *來源位置, 大小型別 上限);
char *尋找字串首個值(const char *字串, int 字元值);
char *尋找字串最後值(const char *字串, int 字元值);
char *尋找子字串(const char *字串, const char *來源位置);
大小型別 取得允許值前綴長度(const char *字串, const char *分隔值集合);
大小型別 取得無排除值前綴長度(const char *字串, const char *分隔值集合);
char *尋找字串中的集合值(const char *字串, const char *分隔值集合);
char *分割字串詞段(char *字串, const char *分隔值集合);
char *指定狀態分割字串詞段(char *字串, const char *分隔值集合, char **保存進度狀態);
char *在新空間複製字串(const char *字串);
char *限長在新空間複製字串(const char *字串, 大小型別 上限);
#endif
