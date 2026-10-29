#ifndef 自前通信網ヘッダー
#define 自前通信網ヘッダー
#include <stdint.h>
#include <stddef.h>
void 通信網用意(void);
void 通信網調査(void);
int ソケット通信端点作成(int 型分類);
int 網結合(int ファイル取扱い, uint32_t 番地, unsigned ポート番号);
int 網接続待機(int ファイル取扱い);
void 再利用ソケット番地(int ファイル取扱い);
int 網接続(int ファイル取扱い, uint32_t 番地, unsigned ポート番号);
int 網受理(int ファイル取扱い);
int 網読取(int ファイル取扱い, void *データ, unsigned 項目個数);
int 網書込(int ファイル取扱い, const void *データ, unsigned 項目個数);
int データグラム送信(int ファイル取扱い, const void *データ, unsigned 項目個数, uint32_t 番地, unsigned ポート番号);
int データグラム受取(int ファイル取扱い, void *データ, unsigned 項目個数);
unsigned 通信網ポート番号(int ファイル取扱い);
unsigned 通信相手ポート番号(int ファイル取扱い);
uint32_t 網通信相手番地(int ファイル取扱い);
void 通信網閉鎖(int ファイル取扱い);
int ファイル転送制御(int 動作);
void ファイル転送調査(void);
uint32_t 通信網状態読取(unsigned 入口値, unsigned 番号);
int 通信網構成(unsigned 動作, uint32_t 番地, uint32_t マスク値, uint32_t 中継門値);
int 応答試験開始処理(uint32_t 番地, unsigned 順序値);
int 応答試験読取(unsigned 入口値);
#endif
