#include <通信番地/八桁組順序.h>
#include <体系/体系呼出.h>
#include <体系/通信端点.h>

enum { 通信端点体系呼出番号 = 102 };
enum {
    通信端点_通信端点を作る = 1, 通信端点_局所番地を結ぶ = 2, 通信端点_相手端点につなぐ = 3, 通信端点_接続要求に備える = 4,
    通信端点_接続要求を受け入れる = 5, 通信端点_局所端点の番地を得る = 6, 通信端点_相手端点の番地を得る = 7,
    通信端点_送る = 9, 通信端点_受け取る = 10, 通信端点_宛先に送る = 11, 通信端点_送信元と共に受け取る = 12,
    通信端点_通信方向を閉じる = 13, 通信端点_通信端点を設定する = 14
};

static long 通信端点を呼び出す(long 通信呼出番号, unsigned long *受渡引数一覧)
{
    return __syscall_result(
        __syscall6(通信端点体系呼出番号, 通信呼出番号, (long)受渡引数一覧, 0, 0, 0, 0));
}

符号なし16二進桁整数 通信網順に16桁を変える(符号なし16二進桁整数 値) { return (符号なし16二進桁整数)((値 << 8) | (値 >> 8)); }
符号なし16二進桁整数 機械順に16桁を変える(符号なし16二進桁整数 値) { return 通信網順に16桁を変える(値); }
符号なし32二進桁整数 通信網順に32桁を変える(符号なし32二進桁整数 値)
{
    return ((値 & 0x000000ffU) << 24) | ((値 & 0x0000ff00U) << 8) |
           ((値 & 0x00ff0000U) >> 8) | ((値 & 0xff000000U) >> 24);
}
符号なし32二進桁整数 機械順に32桁を変える(符号なし32二進桁整数 値) { return 通信網順に32桁を変える(値); }

int 通信端点を作る(int 番地系統, int 端点種類, int 通信規約)
{
    unsigned long 受渡値[3] = {(unsigned long)番地系統, (unsigned long)端点種類, (unsigned long)通信規約};
    return (int)通信端点を呼び出す(通信端点_通信端点を作る, 受渡値);
}

int 局所番地を結ぶ(int 文書記述番号, const struct 通信端点番地 *番地, 番地長型 長さ)
{
    unsigned long 受渡値[3] = {(unsigned long)文書記述番号, (unsigned long)番地, 長さ};
    return (int)通信端点を呼び出す(通信端点_局所番地を結ぶ, 受渡値);
}

int 相手端点につなぐ(int 文書記述番号, const struct 通信端点番地 *番地, 番地長型 長さ)
{
    unsigned long 受渡値[3] = {(unsigned long)文書記述番号, (unsigned long)番地, 長さ};
    return (int)通信端点を呼び出す(通信端点_相手端点につなぐ, 受渡値);
}

int 接続要求に備える(int 文書記述番号, int 待機上限)
{
    unsigned long 受渡値[2] = {(unsigned long)文書記述番号, (unsigned long)待機上限};
    return (int)通信端点を呼び出す(通信端点_接続要求に備える, 受渡値);
}

int 接続要求を受け入れる(int 文書記述番号, struct 通信端点番地 *番地, 番地長型 *長さ)
{
    unsigned long 受渡値[3] = {(unsigned long)文書記述番号, (unsigned long)番地, (unsigned long)長さ};
    return (int)通信端点を呼び出す(通信端点_接続要求を受け入れる, 受渡値);
}

int 局所端点の番地を得る(int 文書記述番号, struct 通信端点番地 *番地, 番地長型 *長さ)
{
    unsigned long 受渡値[3] = {(unsigned long)文書記述番号, (unsigned long)番地, (unsigned long)長さ};
    return (int)通信端点を呼び出す(通信端点_局所端点の番地を得る, 受渡値);
}

int 相手端点の番地を得る(int 文書記述番号, struct 通信端点番地 *番地, 番地長型 *長さ)
{
    unsigned long 受渡値[3] = {(unsigned long)文書記述番号, (unsigned long)番地, (unsigned long)長さ};
    return (int)通信端点を呼び出す(通信端点_相手端点の番地を得る, 受渡値);
}

符号付き大きさ型 送る(int 文書記述番号, const void *資料緩衝領域, 大きさ型 長さ, int 処理指定)
{
    unsigned long 受渡値[4] = {(unsigned long)文書記述番号, (unsigned long)資料緩衝領域, 長さ, (unsigned long)処理指定};
    return (符号付き大きさ型)通信端点を呼び出す(通信端点_送る, 受渡値);
}

符号付き大きさ型 受け取る(int 文書記述番号, void *資料緩衝領域, 大きさ型 長さ, int 処理指定)
{
    unsigned long 受渡値[4] = {(unsigned long)文書記述番号, (unsigned long)資料緩衝領域, 長さ, (unsigned long)処理指定};
    return (符号付き大きさ型)通信端点を呼び出す(通信端点_受け取る, 受渡値);
}

符号付き大きさ型 宛先に送る(int 文書記述番号, const void *資料緩衝領域, 大きさ型 長さ, int 処理指定,
               const struct 通信端点番地 *番地, 番地長型 番地長)
{
    unsigned long 受渡値[6] = {(unsigned long)文書記述番号, (unsigned long)資料緩衝領域, 長さ,
                          (unsigned long)処理指定, (unsigned long)番地, 番地長};
    return (符号付き大きさ型)通信端点を呼び出す(通信端点_宛先に送る, 受渡値);
}

符号付き大きさ型 送信元と共に受け取る(int 文書記述番号, void *資料緩衝領域, 大きさ型 長さ, int 処理指定,
                 struct 通信端点番地 *番地, 番地長型 *番地長)
{
    unsigned long 受渡値[6] = {(unsigned long)文書記述番号, (unsigned long)資料緩衝領域, 長さ,
                          (unsigned long)処理指定, (unsigned long)番地,
                          (unsigned long)番地長};
    return (符号付き大きさ型)通信端点を呼び出す(通信端点_送信元と共に受け取る, 受渡値);
}

int 通信方向を閉じる(int 文書記述番号, int 閉じる方向)
{
    unsigned long 受渡値[2] = {(unsigned long)文書記述番号, (unsigned long)閉じる方向};
    return (int)通信端点を呼び出す(通信端点_通信方向を閉じる, 受渡値);
}

int 通信端点を設定する(int 文書記述番号, int 設定階層, int 設定名,
               const void *設定値, 番地長型 設定長)
{
    unsigned long 受渡値[5] = {(unsigned long)文書記述番号, (unsigned long)設定階層,
                          (unsigned long)設定名, (unsigned long)設定値,
                          設定長};
    return (int)通信端点を呼び出す(通信端点_通信端点を設定する, 受渡値);
}
