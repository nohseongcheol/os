#ifndef 自前遠隔接続状態ヘッダー
#define 自前遠隔接続状態ヘッダー
#include "../命名/機械連結名前一覧.h"
#include <stdint.h>
void 遠隔用意(void);
void 遠隔調査(void);
void 遠隔出力(unsigned char);
int 遠隔入力(void);
int 供給遠隔入力(const unsigned char *,unsigned);
uintptr_t 基板遠隔制御(uintptr_t,uintptr_t);
uintptr_t 基板終端位置遠隔命令(uintptr_t);
uintptr_t 基板遠隔待合(uintptr_t);
void 遠隔表示処理調査(void);
int 制御遠隔表示処理(unsigned);
#endif
