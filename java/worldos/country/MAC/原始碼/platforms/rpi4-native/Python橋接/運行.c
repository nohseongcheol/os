#include "../命名/計算機連接名稱列.h"
#include <string.h>
#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "調用.h"
static char 堆存儲裝置[256 * 1024];
static char 原始資料[16385];
static char 已轉發實際參數[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 中文 API를 쓴다.
static mp_obj_t 打開檔案物件(size_t 項目個數, const mp_obj_t *實參, mp_map_t *選中狀態值) {
    (void)項目個數; (void)實參; (void)選中狀態值;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, 打開檔案物件);

mp_uint_t mp_hal_stdout_tx_strn(const char *文本, size_t 長度) {
    intptr_t 結果 = 用戶調用(1, 1, (uintptr_t)文本, 長度, 0, 0, 0);
    return 結果 < 0 ? 0 : 結果;
}
void mp_hal_stdout_tx_str(const char *字符串資料) { mp_hal_stdout_tx_strn(字符串資料, strlen(字符串資料)); }
void mp_hal_stdout_tx_strn_cooked(const char *字符串資料, size_t 項目個數) { mp_hal_stdout_tx_strn(字符串資料, 項目個數); }
void nlr_jump_fail(void *值) {
    (void)值;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    用戶調用(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *路徑) {
    intptr_t 種類值 = 用戶調用(18, (uintptr_t)路徑, 0, 0, 0, 0, 0);
    return 種類值 == 2 ? MP_IMPORT_STAT_DIR : 種類值 == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr 檔案條目名稱) {
    intptr_t 檔案句柄 = 用戶調用(3, (uintptr_t)qstr_str(檔案條目名稱), 0, 0, 0, 0, 0);
    if (檔案句柄 < 0) mp_raise_OSError(-檔案句柄);
    intptr_t 條目個數 = 用戶調用(2, 檔案句柄, (uintptr_t)原始資料, 16384, 0, 0, 0);
    用戶調用(4, 檔案句柄, 0, 0, 0, 0, 0);
    if (條目個數 < 0) mp_raise_OSError(-條目個數);
    原始資料[條目個數] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(檔案條目名稱, 原始資料, 條目個數, 0);
}
int 用戶開始(int 未使用) {
    (void)未使用;
    int 條目個數 = 用戶調用(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 序數索引 = 0; 序數索引 < 條目個數; 序數索引++) 用戶調用(15, 序數索引, (uintptr_t)已轉發實際參數[序數索引], 256, 0, 0, 0);
    if (條目個數 >= 2 && !strcmp(已轉發實際參數[0], "-m") && !strcmp(已轉發實際參數[1], "pip")) {
        strcpy(已轉發實際參數[0], "/lib/軟件包.py");
        for (int 序數索引 = 1; 序數索引 < 條目個數 - 1; 序數索引++) strcpy(已轉發實際參數[序數索引], 已轉發實際參數[序數索引 + 1]);
        條目個數--;
    }
    if (!條目個數 || !strcmp(已轉發實際參數[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!條目個數) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(已轉發實際參數[0], "-c") && 條目個數 != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(堆存儲裝置, 堆存儲裝置 + sizeof(堆存儲裝置)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (已轉發實際參數[0][0] != '-') {
        const char *結尾 = NULL;
        for (const char *位置索引 = 已轉發實際參數[0]; *位置索引; 位置索引++) if (*位置索引 == '/') 結尾 = 位置索引;
        if (結尾) mp_obj_list_append(mp_sys_path, mp_obj_new_str(已轉發實際參數[0], 結尾 - 已轉發實際參數[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 序數索引 = 0; 序數索引 < 條目個數; 序數索引++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(已轉發實際參數[序數索引], strlen(已轉發實際參數[序數索引])));
    int 狀態值 = 0; nlr_buf_t 非局部發回;
    if (nlr_push(&非局部發回) == 0) {
        mp_lexer_t *詞法分析器 = !strcmp(已轉發實際參數[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 已轉發實際參數[1], strlen(已轉發實際參數[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(已轉發實際參數[0]));
        qstr 名稱 = 詞法分析器->source_name;
        mp_parse_tree_t 語法樹 = mp_parse(詞法分析器, MP_PARSE_FILE_INPUT);
        mp_obj_t 指令序列 = mp_compile(&語法樹, 名稱, false);
        mp_call_function_0(指令序列);
        nlr_pop();
    } else {
        mp_obj_t 異常 = MP_OBJ_FROM_PTR(非局部發回.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(異常)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t 值 = mp_obj_exception_get_value(異常);
            狀態值 = 值 == mp_const_none ? 0 : mp_obj_is_int(值) ? mp_obj_get_int(值) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, 異常); 狀態值 = 1; }
    }
    mp_deinit(); return 狀態值;
}
