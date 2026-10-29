#include "../命名/计算机连接名称列.h"
#include <string.h>
#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "调用.h"
static char 堆存储装置[256 * 1024];
static char 原始数据[16385];
static char 已转发参数[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 中文 API를 쓴다.
static mp_obj_t 打开文件对象(size_t 项目个数, const mp_obj_t *实参, mp_map_t *选中状态值) {
    (void)项目个数; (void)实参; (void)选中状态值;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, 打开文件对象);

mp_uint_t mp_hal_stdout_tx_strn(const char *文本, size_t 长度) {
    intptr_t 结果 = 用户调用(1, 1, (uintptr_t)文本, 长度, 0, 0, 0);
    return 结果 < 0 ? 0 : 结果;
}
void mp_hal_stdout_tx_str(const char *字符串数据) { mp_hal_stdout_tx_strn(字符串数据, strlen(字符串数据)); }
void mp_hal_stdout_tx_strn_cooked(const char *字符串数据, size_t 项目个数) { mp_hal_stdout_tx_strn(字符串数据, 项目个数); }
void nlr_jump_fail(void *值) {
    (void)值;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    用户调用(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *路径) {
    intptr_t 种类值 = 用户调用(18, (uintptr_t)路径, 0, 0, 0, 0, 0);
    return 种类值 == 2 ? MP_IMPORT_STAT_DIR : 种类值 == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr 文件条目名称) {
    intptr_t 文件句柄 = 用户调用(3, (uintptr_t)qstr_str(文件条目名称), 0, 0, 0, 0, 0);
    if (文件句柄 < 0) mp_raise_OSError(-文件句柄);
    intptr_t 条目个数 = 用户调用(2, 文件句柄, (uintptr_t)原始数据, 16384, 0, 0, 0);
    用户调用(4, 文件句柄, 0, 0, 0, 0, 0);
    if (条目个数 < 0) mp_raise_OSError(-条目个数);
    原始数据[条目个数] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(文件条目名称, 原始数据, 条目个数, 0);
}
int 用户开始(int 未使用) {
    (void)未使用;
    int 条目个数 = 用户调用(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 序数索引 = 0; 序数索引 < 条目个数; 序数索引++) 用户调用(15, 序数索引, (uintptr_t)已转发参数[序数索引], 256, 0, 0, 0);
    if (条目个数 >= 2 && !strcmp(已转发参数[0], "-m") && !strcmp(已转发参数[1], "pip")) {
        strcpy(已转发参数[0], "/lib/软件包.py");
        for (int 序数索引 = 1; 序数索引 < 条目个数 - 1; 序数索引++) strcpy(已转发参数[序数索引], 已转发参数[序数索引 + 1]);
        条目个数--;
    }
    if (!条目个数 || !strcmp(已转发参数[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!条目个数) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(已转发参数[0], "-c") && 条目个数 != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(堆存储装置, 堆存储装置 + sizeof(堆存储装置)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (已转发参数[0][0] != '-') {
        const char *结尾 = NULL;
        for (const char *位置索引 = 已转发参数[0]; *位置索引; 位置索引++) if (*位置索引 == '/') 结尾 = 位置索引;
        if (结尾) mp_obj_list_append(mp_sys_path, mp_obj_new_str(已转发参数[0], 结尾 - 已转发参数[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 序数索引 = 0; 序数索引 < 条目个数; 序数索引++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(已转发参数[序数索引], strlen(已转发参数[序数索引])));
    int 状态值 = 0; nlr_buf_t 非局部发回;
    if (nlr_push(&非局部发回) == 0) {
        mp_lexer_t *词法分析器 = !strcmp(已转发参数[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 已转发参数[1], strlen(已转发参数[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(已转发参数[0]));
        qstr 名称 = 词法分析器->source_name;
        mp_parse_tree_t 语法树 = mp_parse(词法分析器, MP_PARSE_FILE_INPUT);
        mp_obj_t 指令序列 = mp_compile(&语法树, 名称, false);
        mp_call_function_0(指令序列);
        nlr_pop();
    } else {
        mp_obj_t 异常 = MP_OBJ_FROM_PTR(非局部发回.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(异常)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t 值 = mp_obj_exception_get_value(异常);
            状态值 = 值 == mp_const_none ? 0 : mp_obj_is_int(值) ? mp_obj_get_int(值) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, 异常); 状态值 = 1; }
    }
    mp_deinit(); return 状态值;
}
