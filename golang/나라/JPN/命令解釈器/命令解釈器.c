/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <通信番地/八桁組順序.h>
#include <誤り番号.h>
#include <文書制御.h>
#include <相互接続網/番地.h>
#include <基本定義.h>
#include <体系/通信端点.h>
#include <体系/文書状態.h>
#include <体系/体系情報.h>
#include <体系/子の待機.h>
#include <入出力と実行.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { 入力行容量 = 512, 最大引数数 = 16, 命令文書の最大入れ子数 = 4 };
static int 命令文書の入れ子の深さ;
struct 入力資料流 {
    int 入力記述番号;
    char 転送緩衝領域[256];
    大きさ型 位置;
    大きさ型 長さ;
};

static 大きさ型 文字列の八桁組数(const char *文字列)
{
    大きさ型 長さ = 0;
    while (文字列[長さ] != '\0')
        長さ++;
    return 長さ;
}

static int 文字列一致(const char *左, const char *右)
{
    大きさ型 位置 = 0;
    while (左[位置] == 右[位置]) {
        if (左[位置] == '\0')
            return 1;
        位置++;
    }
    return 0;
}

static void 文字列を書き出す(const char *文字列)
{
    大きさ型 長さ = 文字列の八桁組数(文字列);
    while (長さ > 0U) {
        符号付き大きさ型 書き出した八桁組数 = 書く(標準出力番号, 文字列, 長さ);
        if (書き出した八桁組数 <= 0)
            return;
        文字列 += 書き出した八桁組数;
        長さ -= (大きさ型)書き出した八桁組数;
    }
}

static void 整数を書き出す(int 値)
{
    char 数字の文字列[16];
    unsigned int 桁数;
    unsigned int 符号なしの大きさ;

    if (値 < 0) {
        文字列を書き出す("-");
        符号なしの大きさ = (unsigned int)(-(値 + 1)) + 1U;
    } else {
        符号なしの大きさ = (unsigned int)値;
    }
    桁数 = 0;
    do {
        数字の文字列[桁数++] = (char)('0' + 符号なしの大きさ % 10U);
        符号なしの大きさ /= 10U;
    } while (符号なしの大きさ != 0U);
    while (桁数 > 0U) {
        桁数--;
        (void)書く(標準出力番号, &数字の文字列[桁数], 1);
    }
}

static void 誤りを知らせる(const char *処理)
{
    文字列を書き出す("error: ");
    文字列を書き出す(処理);
    文字列を書き出す(" errno=");
    整数を書き出す(誤り番号);
    文字列を書き出す("\n");
}

static int 入力行を読む(struct 入力資料流 *入力, char *入力行, 大きさ型 容量)
{
    大きさ型 位置 = 0;
    int 不正な入力行 = 0;
    char 文字;
    符号付き大きさ型 読んだ八桁組の数;
    if (容量 < 2U)
        return -2;
    for (;;) {
        if (入力->位置 == 入力->長さ) {
            読んだ八桁組の数 = 読む(入力->入力記述番号, 入力->転送緩衝領域, sizeof(入力->転送緩衝領域));
            if (読んだ八桁組の数 < 0) {
                if (誤り番号 == 誤り操作中断)
                    continue;
                return -1;
            }
            if (読んだ八桁組の数 == 0) {
                if (位置 == 0 && !不正な入力行)
                    return -1;
                break;
            }
            入力->長さ = (大きさ型)読んだ八桁組の数;
            入力->位置 = 0;
        }
        文字 = 入力->転送緩衝領域[入力->位置++];
        if (文字 == '\n')
            break;
        if (入力->入力記述番号 == 標準入力番号 && 文字 == 4) {
            if (位置 == 0 && !不正な入力行)
                return -1;
            break;
        }
        if (入力->入力記述番号 == 標準入力番号 && (文字 == 8 || 文字 == 127)) {
            if (位置 > 0) {
                do {
                    位置--;
                } while (位置 > 0 && ((unsigned char)入力行[位置] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (文字 == '\r')
            continue;
        if (文字 == '\0') {
            不正な入力行 = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (位置 + 1U < 容量)
            入力行[位置++] = 文字;
        else
            不正な入力行 = 1;
    }
    入力行[位置] = '\0';
    return 不正な入力行 ? -2 : (int)位置;
}

static int 引数を分ける(char *入力行, char **引数列)
{
    int 引数の数_2 = 0;
    char *現在位置 = 入力行;
    char *出力位置 = 入力行;

    while (*現在位置 != '\0') {
        char 引用符 = '\0';
        while (*現在位置 == ' ' || *現在位置 == '\t')
            現在位置++;
        if (*現在位置 == '\0' || *現在位置 == '#')
            break;
        if (引数の数_2 == 最大引数数 - 1)
            return -1;
        引数列[引数の数_2++] = 出力位置;
        while (*現在位置 != '\0') {
            char 文字 = *現在位置++;
            if (引用符 == '\0' && (文字 == ' ' || 文字 == '\t'))
                break;
            if (文字 == '\\' && 引用符 != '\'') {
                if (*現在位置 == '\0')
                    return -1;
                *出力位置++ = *現在位置++;
            } else if (文字 == '\'' || 文字 == '"') {
                if (引用符 == '\0')
                    引用符 = 文字;
                else if (引用符 == 文字)
                    引用符 = '\0';
                else
                    *出力位置++ = 文字;
            } else {
                *出力位置++ = 文字;
            }
        }
        if (引用符 != '\0')
            return -1;
        *出力位置++ = '\0';
    }
    引数列[引数の数_2] = (char *)0;
    return 引数の数_2;
}

static void 使い方を示す(void)
{
    大きさ型 位置;
    文字列を書き出す(
        "WorldOS command interpreter commands:\n"
        "  help                 show this help\n"
        "  echo TEXT            print text\n"
        "  pwd                  show current directory\n"
        "  cd PATH              change directory\n"
        "  cat FILE             print a FAT file\n"
        "  stat FILE            show file size\n"
        "  pid                  show process identifiers\n"
        "  uname                show operating-system identity\n"
        "  run FILE [ARGS...]   execute a user ELF program\n"
        "  udp [TEXT]           call POSIX UDP and loop back TEXT\n"
        "  source FILE          interpret a UTF-8 command file\n"
        "  exit                 leave the shell\n");
    文字列を書き出す("Native command proposals (ASCII aliases remain available):\n");
    for (位置 = 0; 位置 < sizeof(基準命令) / sizeof(基準命令[0]); 位置++) {
        文字列を書き出す(現地語命令別名[位置]);
        文字列を書き出す(" = ");
        文字列を書き出す(基準命令[位置]);
        文字列を書き出す("\n");
    }
}

static int 命令が一致する(const char *文字列, const char *命令)
{
    大きさ型 位置;
    if (文字列一致(文字列, 命令))
        return 1;
    for (位置 = 0; 位置 < sizeof(基準命令) / sizeof(基準命令[0]); 位置++)
        if (文字列一致(命令, 基準命令[位置]))
            return 文字列一致(文字列, 現地語命令別名[位置]);
    return 0;
}

static int 入力を解釈する(int 入力記述番号);

static int 命令文書を解釈する(const char *文書名)
{
    int 文書記述番号_2;
    int 状態;
    if (命令文書の入れ子の深さ >= 命令文書の最大入れ子数) {
        文字列を書き出す("source: nesting limit\n");
        return 0;
    }
    文書記述番号_2 = 開く(文書名, 読取専用で開く);
    if (文書記述番号_2 < 0) {
        誤りを知らせる(文書名);
        return 0;
    }
    命令文書の入れ子の深さ++;
    状態 = 入力を解釈する(文書記述番号_2);
    命令文書の入れ子の深さ--;
    (void)閉じる(文書記述番号_2);
    return 状態;
}

static void 引数を表示する(int 引数の数_2, char **引数列)
{
    int 位置;
    for (位置 = 1; 位置 < 引数の数_2; 位置++) {
        if (位置 != 1)
            文字列を書き出す(" ");
        文字列を書き出す(引数列[位置]);
    }
    文字列を書き出す("\n");
}

static void 現在の場所を示す(void)
{
    char 経路[128];
    if (作業目録の経路を得る(経路, sizeof(経路)) == (char *)0) {
        誤りを知らせる("pwd");
        return;
    }
    文字列を書き出す(経路);
    文字列を書き出す("\n");
}

static void 文書の内容を表示する(const char *文書名)
{
    char 転送緩衝領域[128];
    int 文書記述番号_2 = 開く(文書名, 読取専用で開く);
    符号付き大きさ型 読んだ八桁組の数;

    if (文書記述番号_2 < 0) {
        誤りを知らせる("cat");
        return;
    }
    while ((読んだ八桁組の数 = 読む(文書記述番号_2, 転送緩衝領域, sizeof(転送緩衝領域))) > 0)
        (void)書く(標準出力番号, 転送緩衝領域, (大きさ型)読んだ八桁組の数);
    if (読んだ八桁組の数 < 0)
        誤りを知らせる("cat/read");
    (void)閉じる(文書記述番号_2);
    文字列を書き出す("\n");
}

static void 文書の情報を示す(const char *文書名)
{
    struct 文書状態 状態;
    if (文書状態(文書名, &状態) < 0) {
        誤りを知らせる("stat");
        return;
    }
    文字列を書き出す("size=");
    整数を書き出す((int)状態.文書の大きさ);
    文字列を書き出す(目録方式判定(状態.文書種類と権限) ? " type=directory\n" : " type=file\n");
}

static void 実行過程の番号を示す(void)
{
    文字列を書き出す("pid=");
    整数を書き出す((int)実行過程番号を得る());
    文字列を書き出す(" ppid=");
    整数を書き出す((int)親実行過程番号を得る());
    文字列を書き出す("\n");
}

static void 基本体系の情報を示す(void)
{
    struct 体系情報 体系識別情報;
    if (体系情報を得る(&体系識別情報) < 0) {
        誤りを知らせる("uname");
        return;
    }
    文字列を書き出す(体系識別情報.体系名);
    文字列を書き出す(" ");
    文字列を書き出す(体系識別情報.体系配布版);
    文字列を書き出す(" ");
    文字列を書き出す(体系識別情報.機械種類);
    文字列を書き出す("\n");
}

static void 実行形式を起動する(int 引数の数_2, char **引数列)
{
    実行過程番号型 子実行過程の番号;
    int 子実行過程の終了状態 = 0;

    if (引数の数_2 < 2) {
        文字列を書き出す("usage: run FILE [ARGS...]\n");
        return;
    }
    子実行過程の番号 = 実行過程を分岐する();
    if (子実行過程の番号 < 0) {
        誤りを知らせる("fork");
        return;
    }
    if (子実行過程の番号 == 0) {
        実行内容を置き換える(引数列[1], &引数列[1], (char *const *)0);
        誤りを知らせる("execve");
        直ちに終了する(127);
    }
    if (指定した子を待つ(子実行過程の番号, &子実行過程の終了状態, 0) < 0) {
        誤りを知らせる("waitpid");
        return;
    }
    文字列を書き出す("exit-status=");
    整数を書き出す(終了値取出し(子実行過程の終了状態));
    文字列を書き出す("\n");
}

static void 独立電文の折り返しを試す(const char *電文)
{
    struct 相互接続網端点番地 受信端点の番地 = {0};
    struct 相互接続網端点番地 送信端点の番地 = {0};
    番地長型 送信元番地の長さ = sizeof(送信端点の番地);
    char 受信資料[96];
    大きさ型 電文の八桁組数 = 文字列の八桁組数(電文);
    int 受信通信端点 = -1;
    int 送信通信端点 = -1;
    符号付き大きさ型 受信八桁組数;

    if (電文の八桁組数 >= sizeof(受信資料)) {
        文字列を書き出す("udp: message exceeds 95 bytes\n");
        return;
    }
    受信通信端点 = 通信端点を作る(相互接続網番地系統, 資料電文端点, 利用者資料電文規約);
    送信通信端点 = 通信端点を作る(相互接続網番地系統, 資料電文端点, 利用者資料電文規約);
    if (受信通信端点 < 0 || 送信通信端点 < 0) {
        誤りを知らせる("socket");
        goto 通信端点を閉じる;
    }
    受信端点の番地.接続網番地系統 = 相互接続網番地系統;
    受信端点の番地.通信窓口番号 = 通信網順に16桁を変える(40404);
    受信端点の番地.接続網番地内容.番地値 = 通信網順に32桁を変える(自己折返し番地);
    if (局所番地を結ぶ(受信通信端点, (const struct 通信端点番地 *)&受信端点の番地, sizeof(受信端点の番地)) < 0) {
        誤りを知らせる("bind");
        goto 通信端点を閉じる;
    }
    if (相手端点につなぐ(送信通信端点, (const struct 通信端点番地 *)&受信端点の番地, sizeof(受信端点の番地)) < 0) {
        誤りを知らせる("connect");
        goto 通信端点を閉じる;
    }
    if (送る(送信通信端点, 電文, 電文の八桁組数, 0) != (符号付き大きさ型)電文の八桁組数) {
        誤りを知らせる("send");
        goto 通信端点を閉じる;
    }
    受信八桁組数 = 送信元と共に受け取る(受信通信端点, 受信資料, sizeof(受信資料) - 1U, 0,
                         (struct 通信端点番地 *)&送信端点の番地, &送信元番地の長さ);
    if (受信八桁組数 < 0) {
        誤りを知らせる("recvfrom");
        goto 通信端点を閉じる;
    }
    受信資料[受信八桁組数] = '\0';
    文字列を書き出す("udp-received: ");
    文字列を書き出す(受信資料);
    文字列を書き出す("\n");

通信端点を閉じる:
    if (送信通信端点 >= 0)
        (void)閉じる(送信通信端点);
    if (受信通信端点 >= 0)
        (void)閉じる(受信通信端点);
}

static int 入力を解釈する(int 入力記述番号)
{
    char 入力行[入力行容量];
    char *引数列[最大引数数];
    struct 入力資料流 入力 = {0};
    入力.入力記述番号 = 入力記述番号;

    for (;;) {
        int 引数の数_2;
        int 状態;
        if (入力記述番号 == 標準入力番号)
            文字列を書き出す("worldos$ ");
        状態 = 入力行を読む(&入力, 入力行, sizeof(入力行));
        if (状態 == -1)
            return 0;
        if (状態 == -2) {
            文字列を書き出す("input rejected: overlong or binary line\n");
            continue;
        }
        引数の数_2 = 引数を分ける(入力行, 引数列);
        if (引数の数_2 < 0) {
            文字列を書き出す("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (引数の数_2 == 0)
            continue;
        if (命令が一致する(引数列[0], "help"))
            使い方を示す();
        else if (命令が一致する(引数列[0], "echo"))
            引数を表示する(引数の数_2, 引数列);
        else if (命令が一致する(引数列[0], "pwd"))
            現在の場所を示す();
        else if (命令が一致する(引数列[0], "cd")) {
            if (引数の数_2 < 2)
                文字列を書き出す("usage: cd PATH\n");
            else if (作業目録を変える(引数列[1]) < 0)
                誤りを知らせる("cd");
        } else if (命令が一致する(引数列[0], "cat")) {
            if (引数の数_2 < 2)
                文字列を書き出す("usage: cat FILE\n");
            else
                文書の内容を表示する(引数列[1]);
        } else if (命令が一致する(引数列[0], "stat")) {
            if (引数の数_2 < 2)
                文字列を書き出す("usage: stat FILE\n");
            else
                文書の情報を示す(引数列[1]);
        } else if (命令が一致する(引数列[0], "pid"))
            実行過程の番号を示す();
        else if (命令が一致する(引数列[0], "uname"))
            基本体系の情報を示す();
        else if (命令が一致する(引数列[0], "run"))
            実行形式を起動する(引数の数_2, 引数列);
        else if (命令が一致する(引数列[0], "udp"))
            独立電文の折り返しを試す(引数の数_2 >= 2 ? 引数列[1] : "ping");
        else if (命令が一致する(引数列[0], "source")) {
            if (引数の数_2 < 2)
                文字列を書き出す("usage: source FILE\n");
            else if (命令文書を解釈する(引数列[1]))
                return 1;
        } else if (命令が一致する(引数列[0], "exit"))
            return 1;
        else
            文字列を書き出す("unknown command; type help\n");
    }
}

int main(void)
{
    文字列を書き出す("WORLDOS-SHELL:READY\n");
    (void)入力を解釈する(標準入力番号);
    文字列を書き出す("WORLDOS-SHELL:EXIT\n");
    return 0;
}
