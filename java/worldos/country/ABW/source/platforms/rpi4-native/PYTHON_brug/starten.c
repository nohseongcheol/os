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
static char dynamisch_geheugen[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 Nederlands API를 쓴다.
static mp_obj_t open_Bestand_object(size_t item_AANTAL, const mp_obj_t *argumenten, mp_map_t *selectie_WAARDE) {
    (void)item_AANTAL; (void)argumenten; (void)selectie_WAARDE;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, open_Bestand_object);

mp_uint_t mp_hal_stdout_tx_strn(const char *tekst, size_t tijdsduur_WAARDE) {
    intptr_t resultaat = 사용자호출(1, 1, (uintptr_t)tekst, tijdsduur_WAARDE, 0, 0, 0);
    return resultaat < 0 ? 0 : resultaat;
}
void mp_hal_stdout_tx_str(const char *tekenreeks_gegevens) { mp_hal_stdout_tx_strn(tekenreeks_gegevens, strlen(tekenreeks_gegevens)); }
void mp_hal_stdout_tx_strn_cooked(const char *tekenreeks_gegevens, size_t item_AANTAL) { mp_hal_stdout_tx_strn(tekenreeks_gegevens, item_AANTAL); }
void nlr_jump_fail(void *WAARDE) {
    (void)WAARDE;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *pad) {
    intptr_t soort_WAARDE = 사용자호출(18, (uintptr_t)pad, 0, 0, 0, 0, 0);
    return soort_WAARDE == 2 ? MP_IMPORT_STAT_DIR : soort_WAARDE == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr Bestand_invoer_naam) {
    intptr_t bestandsingang = 사용자호출(3, (uintptr_t)qstr_str(Bestand_invoer_naam), 0, 0, 0, 0, 0);
    if (bestandsingang < 0) mp_raise_OSError(-bestandsingang);
    intptr_t invoer_AANTAL_8f7753a1 = 사용자호출(2, bestandsingang, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, bestandsingang, 0, 0, 0, 0, 0);
    if (invoer_AANTAL_8f7753a1 < 0) mp_raise_OSError(-invoer_AANTAL_8f7753a1);
    원본자료[invoer_AANTAL_8f7753a1] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(Bestand_invoer_naam, 원본자료, invoer_AANTAL_8f7753a1, 0);
}
int gebruiker_START(int 미사용값) {
    (void)미사용값;
    int invoer_AANTAL_8f7753a1 = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < invoer_AANTAL_8f7753a1; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (invoer_AANTAL_8f7753a1 >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/bundel.py");
        for (int 순번 = 1; 순번 < invoer_AANTAL_8f7753a1 - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        invoer_AANTAL_8f7753a1--;
    }
    if (!invoer_AANTAL_8f7753a1 || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!invoer_AANTAL_8f7753a1) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && invoer_AANTAL_8f7753a1 != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(dynamisch_geheugen, dynamisch_geheugen + sizeof(dynamisch_geheugen)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *plaatsingsindex = 전달인수[0]; *plaatsingsindex; plaatsingsindex++) if (*plaatsingsindex == '/') 끝 = plaatsingsindex;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < invoer_AANTAL_8f7753a1; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int Status_WAARDE = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Naam = 낱말해석기->source_name;
        mp_parse_tree_t syntaxis_structuur = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t instructie_REEKS = mp_compile(&syntaxis_structuur, Naam, false);
        mp_call_function_0(instructie_REEKS);
        nlr_pop();
    } else {
        mp_obj_t uitzondering = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(uitzondering)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t WAARDE = mp_obj_exception_get_value(uitzondering);
            Status_WAARDE = WAARDE == mp_const_none ? 0 : mp_obj_is_int(WAARDE) ? mp_obj_get_int(WAARDE) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, uitzondering); Status_WAARDE = 1; }
    }
    mp_deinit(); return Status_WAARDE;
}
