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
static char ढ़ेर_संग्रहण[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 हिंदी API를 쓴다.
static mp_obj_t जारी_फ़ाइल_ऑब्जेक्ट(size_t 개수, const mp_obj_t *तर्क, mp_map_t *चयन_मान) {
    (void)개수; (void)तर्क; (void)चयन_मान;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, जारी_फ़ाइल_ऑब्जेक्ट);

mp_uint_t mp_hal_stdout_tx_strn(const char *पाठ, size_t 길이) {
    intptr_t परिणाम = 사용자호출(1, 1, (uintptr_t)पाठ, 길이, 0, 0, 0);
    return परिणाम < 0 ? 0 : परिणाम;
}
void mp_hal_stdout_tx_str(const char *स्ट्रिंग_डेटा) { mp_hal_stdout_tx_strn(स्ट्रिंग_डेटा, strlen(स्ट्रिंग_डेटा)); }
void mp_hal_stdout_tx_strn_cooked(const char *स्ट्रिंग_डेटा, size_t 개수) { mp_hal_stdout_tx_strn(स्ट्रिंग_डेटा, 개수); }
void nlr_jump_fail(void *मान) {
    (void)मान;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *पथ) {
    intptr_t 종류 = 사용자호출(18, (uintptr_t)पथ, 0, 0, 0, 0, 0);
    return 종류 == 2 ? MP_IMPORT_STAT_DIR : 종류 == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr फ़ाइल_एन्ट्री_नाम) {
    intptr_t फ़ाइल_हैंडल = 사용자호출(3, (uintptr_t)qstr_str(फ़ाइल_एन्ट्री_नाम), 0, 0, 0, 0, 0);
    if (फ़ाइल_हैंडल < 0) mp_raise_OSError(-फ़ाइल_हैंडल);
    intptr_t 항목수 = 사용자호출(2, फ़ाइल_हैंडल, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, फ़ाइल_हैंडल, 0, 0, 0, 0, 0);
    if (항목수 < 0) mp_raise_OSError(-항목수);
    원본자료[항목수] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(फ़ाइल_एन्ट्री_नाम, 원본자료, 항목수, 0);
}
int उपयोगकर्ता_प्रारंभ(int 미사용값) {
    (void)미사용값;
    int 항목수 = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < 항목수; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (항목수 >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/बंडल.py");
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
    gc_init(ढ़ेर_संग्रहण, ढ़ेर_संग्रहण + sizeof(ढ़ेर_संग्रहण)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *पद_इंडेक्स = 전달인수[0]; *पद_इंडेक्स; पद_इंडेक्स++) if (*पद_इंडेक्स == '/') 끝 = पद_इंडेक्स;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < 항목수; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int अवस्था_मान = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr नाम = 낱말해석기->source_name;
        mp_parse_tree_t सिन्टैक्स_ट्री = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t 명령열 = mp_compile(&सिन्टैक्स_ट्री, नाम, false);
        mp_call_function_0(명령열);
        nlr_pop();
    } else {
        mp_obj_t अपवाद = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(अपवाद)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t मान = mp_obj_exception_get_value(अपवाद);
            अवस्था_मान = मान == mp_const_none ? 0 : mp_obj_is_int(मान) ? mp_obj_get_int(मान) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, अपवाद); अवस्था_मान = 1; }
    }
    mp_deinit(); return अवस्था_मान;
}
