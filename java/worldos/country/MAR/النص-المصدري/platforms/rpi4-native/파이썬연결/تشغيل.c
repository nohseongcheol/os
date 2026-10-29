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
static char ذاكرة_ديناميكية[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 العربية API를 쓴다.
static mp_obj_t فتح_ملف_عنصر(size_t 개수, const mp_obj_t *وسائط, mp_map_t *تحديد_قيمة) {
    (void)개수; (void)وسائط; (void)تحديد_قيمة;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, فتح_ملف_عنصر);

mp_uint_t mp_hal_stdout_tx_strn(const char *نص, size_t 길이) {
    intptr_t نتيجة = 사용자호출(1, 1, (uintptr_t)نص, 길이, 0, 0, 0);
    return نتيجة < 0 ? 0 : نتيجة;
}
void mp_hal_stdout_tx_str(const char *سلسلة_بيانات) { mp_hal_stdout_tx_strn(سلسلة_بيانات, strlen(سلسلة_بيانات)); }
void mp_hal_stdout_tx_strn_cooked(const char *سلسلة_بيانات, size_t 개수) { mp_hal_stdout_tx_strn(سلسلة_بيانات, 개수); }
void nlr_jump_fail(void *قيمة) {
    (void)قيمة;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *مسار) {
    intptr_t 종류 = 사용자호출(18, (uintptr_t)مسار, 0, 0, 0, 0, 0);
    return 종류 == 2 ? MP_IMPORT_STAT_DIR : 종류 == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr ملف_إدخال_اسم) {
    intptr_t ملف_مؤشر = 사용자호출(3, (uintptr_t)qstr_str(ملف_إدخال_اسم), 0, 0, 0, 0, 0);
    if (ملف_مؤشر < 0) mp_raise_OSError(-ملف_مؤشر);
    intptr_t 항목수 = 사용자호출(2, ملف_مؤشر, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, ملف_مؤشر, 0, 0, 0, 0, 0);
    if (항목수 < 0) mp_raise_OSError(-항목수);
    원본자료[항목수] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(ملف_إدخال_اسم, 원본자료, 항목수, 0);
}
int مستخدم_بدء(int 미사용값) {
    (void)미사용값;
    int 항목수 = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < 항목수; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (항목수 >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/يُجمع.py");
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
    gc_init(ذاكرة_ديناميكية, ذاكرة_ديناميكية + sizeof(ذاكرة_ديناميكية)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *منصب_فهرس = 전달인수[0]; *منصب_فهرس; منصب_فهرس++) if (*منصب_فهرس == '/') 끝 = منصب_فهرس;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < 항목수; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int حالة_قيمة = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr اسم = 낱말해석기->source_name;
        mp_parse_tree_t بناء_الجملة_شجرة = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t تعليمة_تسلسل = mp_compile(&بناء_الجملة_شجرة, اسم, false);
        mp_call_function_0(تعليمة_تسلسل);
        nlr_pop();
    } else {
        mp_obj_t استثناء = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(استثناء)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t قيمة = mp_obj_exception_get_value(استثناء);
            حالة_قيمة = قيمة == mp_const_none ? 0 : mp_obj_is_int(قيمة) ? mp_obj_get_int(قيمة) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, استثناء); حالة_قيمة = 1; }
    }
    mp_deinit(); return حالة_قيمة;
}
