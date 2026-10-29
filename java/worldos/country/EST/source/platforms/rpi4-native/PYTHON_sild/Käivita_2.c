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

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 Eesti API를 쓴다.
static mp_obj_t avama_Fail_objekt(size_t kaup_COUNT, const mp_obj_t *Argumendid, mp_map_t *valim_VALUE) {
    (void)kaup_COUNT; (void)Argumendid; (void)valim_VALUE;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, avama_Fail_objekt);

mp_uint_t mp_hal_stdout_tx_strn(const char *Tekst, size_t 길이) {
    intptr_t TULEMUS = 사용자호출(1, 1, (uintptr_t)Tekst, 길이, 0, 0, 0);
    return TULEMUS < 0 ? 0 : TULEMUS;
}
void mp_hal_stdout_tx_str(const char *string_andmed) { mp_hal_stdout_tx_strn(string_andmed, strlen(string_andmed)); }
void mp_hal_stdout_tx_strn_cooked(const char *string_andmed, size_t kaup_COUNT) { mp_hal_stdout_tx_strn(string_andmed, kaup_COUNT); }
void nlr_jump_fail(void *VALUE) {
    (void)VALUE;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *RADA) {
    intptr_t 종류 = 사용자호출(18, (uintptr_t)RADA, 0, 0, 0, 0, 0);
    return 종류 == 2 ? MP_IMPORT_STAT_DIR : 종류 == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr Fail_kirje_nimetus) {
    intptr_t Fail_pide = 사용자호출(3, (uintptr_t)qstr_str(Fail_kirje_nimetus), 0, 0, 0, 0, 0);
    if (Fail_pide < 0) mp_raise_OSError(-Fail_pide);
    intptr_t kirje_COUNT = 사용자호출(2, Fail_pide, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, Fail_pide, 0, 0, 0, 0, 0);
    if (kirje_COUNT < 0) mp_raise_OSError(-kirje_COUNT);
    원본자료[kirje_COUNT] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(Fail_kirje_nimetus, 원본자료, kirje_COUNT, 0);
}
int kasutaja_START(int 미사용값) {
    (void)미사용값;
    int kirje_COUNT = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < kirje_COUNT; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (kirje_COUNT >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/kogum.py");
        for (int 순번 = 1; 순번 < kirje_COUNT - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        kirje_COUNT--;
    }
    if (!kirje_COUNT || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!kirje_COUNT) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && kirje_COUNT != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(동적기억공간, 동적기억공간 + sizeof(동적기억공간)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *asukohaindeks = 전달인수[0]; *asukohaindeks; asukohaindeks++) if (*asukohaindeks == '/') 끝 = asukohaindeks;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < kirje_COUNT; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int Olek_VALUE = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Nimi_2 = 낱말해석기->source_name;
        mp_parse_tree_t süntaks_puu = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t 명령열 = mp_compile(&süntaks_puu, Nimi_2, false);
        mp_call_function_0(명령열);
        nlr_pop();
    } else {
        mp_obj_t erand = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(erand)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t VALUE = mp_obj_exception_get_value(erand);
            Olek_VALUE = VALUE == mp_const_none ? 0 : mp_obj_is_int(VALUE) ? mp_obj_get_int(VALUE) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, erand); Olek_VALUE = 1; }
    }
    mp_deinit(); return Olek_VALUE;
}
