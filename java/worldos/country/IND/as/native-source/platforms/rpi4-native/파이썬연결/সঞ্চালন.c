#include "../명명/기계연결이름.h"
#include <string.h>
#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "호출.h"
static char 동적기억공간[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 한국어 API를 쓴다.
static mp_obj_t খোলক_ফাইল_অবজেক্ট(size_t 개수, const mp_obj_t *인수, mp_map_t *চয়ন_মান) {
    (void)개수; (void)인수; (void)চয়ন_মান;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, খোলক_ফাইল_অবজেক্ট);

mp_uint_t mp_hal_stdout_tx_strn(const char *টেক্সট, size_t দৈর্ঘ্য_মান) {
    intptr_t পৰিমাপ = 사용자호출(1, 1, (uintptr_t)টেক্সট, দৈর্ঘ্য_মান, 0, 0, 0);
    return পৰিমাপ < 0 ? 0 : পৰিমাপ;
}
void mp_hal_stdout_tx_str(const char *ষ্ট্ৰিং_ডাটা) { mp_hal_stdout_tx_strn(ষ্ট্ৰিং_ডাটা, strlen(ষ্ট্ৰিং_ডাটা)); }
void mp_hal_stdout_tx_strn_cooked(const char *ষ্ট্ৰিং_ডাটা, size_t 개수) { mp_hal_stdout_tx_strn(ষ্ট্ৰিং_ডাটা, 개수); }
void nlr_jump_fail(void *মান) {
    (void)মান;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *পথ) {
    intptr_t 종류 = 사용자호출(18, (uintptr_t)পথ, 0, 0, 0, 0, 0);
    return 종류 == 2 ? MP_IMPORT_STAT_DIR : 종류 == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr ফাইল_প্রবিষ্ট_নাম) {
    intptr_t ফাইল_হেণ্ডেল = 사용자호출(3, (uintptr_t)qstr_str(ফাইল_প্রবিষ্ট_নাম), 0, 0, 0, 0, 0);
    if (ফাইল_হেণ্ডেল < 0) mp_raise_OSError(-ফাইল_হেণ্ডেল);
    intptr_t 항목수 = 사용자호출(2, ফাইল_হেণ্ডেল, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, ফাইল_হেণ্ডেল, 0, 0, 0, 0, 0);
    if (항목수 < 0) mp_raise_OSError(-항목수);
    원본자료[항목수] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(ফাইল_প্রবিষ্ট_নাম, 원본자료, 항목수, 0);
}
int ব্যৱহাৰকৰ্তা_আৰম্ভ(int 미사용값) {
    (void)미사용값;
    int 항목수 = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < 항목수; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (항목수 >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/বাণ্ডল.py");
        for (int 순번 = 1; 순번 < 항목수 - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        항목수--;
    }
    if (!항목수 || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!항목수) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && 항목수 != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(동적기억공간, 동적기억공간 + sizeof(동적기억공간)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *স্থান_সলনি_কৰক_ইনডেক্স = 전달인수[0]; *স্থান_সলনি_কৰক_ইনডেক্স; স্থান_সলনি_কৰক_ইনডেক্স++) if (*স্থান_সলনি_কৰক_ইনডেক্স == '/') 끝 = স্থান_সলনি_কৰক_ইনডেক্স;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < 항목수; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int অৱস্থা_মান = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr নাম = 낱말해석기->source_name;
        mp_parse_tree_t ছিনটেক্স_ট্ৰি = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t 명령열 = mp_compile(&ছিনটেক্স_ট্ৰি, নাম, false);
        mp_call_function_0(명령열);
        nlr_pop();
    } else {
        mp_obj_t 예외 = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(예외)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t মান = mp_obj_exception_get_value(예외);
            অৱস্থা_মান = মান == mp_const_none ? 0 : mp_obj_is_int(মান) ? mp_obj_get_int(মান) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, 예외); অৱস্থা_মান = 1; }
    }
    mp_deinit(); return অৱস্থা_মান;
}
