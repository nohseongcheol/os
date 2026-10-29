#include "../命名/機械連結名前一覧.h"
#include <string.h>
#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "呼出.h"
static char ヒープ記憶装置[256 * 1024];
static char 原本データ[16385];
static char 転送済み引数[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 日本語 API를 쓴다.
static mp_obj_t ファイルオブジェクト開放(size_t 項目個数, const mp_obj_t *引数, mp_map_t *選択状態値) {
    (void)項目個数; (void)引数; (void)選択状態値;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, ファイルオブジェクト開放);

mp_uint_t mp_hal_stdout_tx_strn(const char *文, size_t 長さ) {
    intptr_t 結果 = 利用者呼出(1, 1, (uintptr_t)文, 長さ, 0, 0, 0);
    return 結果 < 0 ? 0 : 結果;
}
void mp_hal_stdout_tx_str(const char *文字列データ) { mp_hal_stdout_tx_strn(文字列データ, strlen(文字列データ)); }
void mp_hal_stdout_tx_strn_cooked(const char *文字列データ, size_t 項目個数) { mp_hal_stdout_tx_strn(文字列データ, 項目個数); }
void nlr_jump_fail(void *値) {
    (void)値;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    利用者呼出(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *経路) {
    intptr_t 種別値 = 利用者呼出(18, (uintptr_t)経路, 0, 0, 0, 0, 0);
    return 種別値 == 2 ? MP_IMPORT_STAT_DIR : 種別値 == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr ファイル入口名前) {
    intptr_t ファイル取扱い = 利用者呼出(3, (uintptr_t)qstr_str(ファイル入口名前), 0, 0, 0, 0, 0);
    if (ファイル取扱い < 0) mp_raise_OSError(-ファイル取扱い);
    intptr_t 入口個数 = 利用者呼出(2, ファイル取扱い, (uintptr_t)原本データ, 16384, 0, 0, 0);
    利用者呼出(4, ファイル取扱い, 0, 0, 0, 0, 0);
    if (入口個数 < 0) mp_raise_OSError(-入口個数);
    原本データ[入口個数] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(ファイル入口名前, 原本データ, 入口個数, 0);
}
int 利用者開始処理(int 未使用) {
    (void)未使用;
    int 入口個数 = 利用者呼出(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 序数添字 = 0; 序数添字 < 入口個数; 序数添字++) 利用者呼出(15, 序数添字, (uintptr_t)転送済み引数[序数添字], 256, 0, 0, 0);
    if (入口個数 >= 2 && !strcmp(転送済み引数[0], "-m") && !strcmp(転送済み引数[1], "pip")) {
        strcpy(転送済み引数[0], "/lib/パッケージ.py");
        for (int 序数添字 = 1; 序数添字 < 入口個数 - 1; 序数添字++) strcpy(転送済み引数[序数添字], 転送済み引数[序数添字 + 1]);
        入口個数--;
    }
    if (!入口個数 || !strcmp(転送済み引数[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!入口個数) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(転送済み引数[0], "-c") && 入口個数 != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(ヒープ記憶装置, ヒープ記憶装置 + sizeof(ヒープ記憶装置)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (転送済み引数[0][0] != '-') {
        const char *終端 = NULL;
        for (const char *位置添字 = 転送済み引数[0]; *位置添字; 位置添字++) if (*位置添字 == '/') 終端 = 位置添字;
        if (終端) mp_obj_list_append(mp_sys_path, mp_obj_new_str(転送済み引数[0], 終端 - 転送済み引数[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 序数添字 = 0; 序数添字 < 入口個数; 序数添字++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(転送済み引数[序数添字], strlen(転送済み引数[序数添字])));
    int 状況値 = 0; nlr_buf_t 非該当局所復帰;
    if (nlr_push(&非該当局所復帰) == 0) {
        mp_lexer_t *字句解析器 = !strcmp(転送済み引数[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 転送済み引数[1], strlen(転送済み引数[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(転送済み引数[0]));
        qstr 名前 = 字句解析器->source_name;
        mp_parse_tree_t 構文木 = mp_parse(字句解析器, MP_PARSE_FILE_INPUT);
        mp_obj_t 命令語列順 = mp_compile(&構文木, 名前, false);
        mp_call_function_0(命令語列順);
        nlr_pop();
    } else {
        mp_obj_t 例外 = MP_OBJ_FROM_PTR(非該当局所復帰.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(例外)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t 値 = mp_obj_exception_get_value(例外);
            状況値 = 値 == mp_const_none ? 0 : mp_obj_is_int(値) ? mp_obj_get_int(値) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, 例外); 状況値 = 1; }
    }
    mp_deinit(); return 状況値;
}
