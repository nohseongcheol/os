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
static char dynamická_paměť[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 čeština API를 쓴다.
static mp_obj_t otevřít_Soubor_objekt(size_t zboží_POČET, const mp_obj_t *argumenty, mp_map_t *výběr_HODNOTA) {
    (void)zboží_POČET; (void)argumenty; (void)výběr_HODNOTA;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, otevřít_Soubor_objekt);

mp_uint_t mp_hal_stdout_tx_strn(const char *text, size_t délka_HODNOTA) {
    intptr_t VÝSLEDEK = 사용자호출(1, 1, (uintptr_t)text, délka_HODNOTA, 0, 0, 0);
    return VÝSLEDEK < 0 ? 0 : VÝSLEDEK;
}
void mp_hal_stdout_tx_str(const char *řetězec_data) { mp_hal_stdout_tx_strn(řetězec_data, strlen(řetězec_data)); }
void mp_hal_stdout_tx_strn_cooked(const char *řetězec_data, size_t zboží_POČET) { mp_hal_stdout_tx_strn(řetězec_data, zboží_POČET); }
void nlr_jump_fail(void *HODNOTA) {
    (void)HODNOTA;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *cesta_2) {
    intptr_t Druh_HODNOTA = 사용자호출(18, (uintptr_t)cesta_2, 0, 0, 0, 0, 0);
    return Druh_HODNOTA == 2 ? MP_IMPORT_STAT_DIR : Druh_HODNOTA == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr Soubor_položka_název) {
    intptr_t popisovač_souboru = 사용자호출(3, (uintptr_t)qstr_str(Soubor_položka_název), 0, 0, 0, 0, 0);
    if (popisovač_souboru < 0) mp_raise_OSError(-popisovač_souboru);
    intptr_t položka_POČET = 사용자호출(2, popisovač_souboru, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, popisovač_souboru, 0, 0, 0, 0, 0);
    if (položka_POČET < 0) mp_raise_OSError(-položka_POČET);
    원본자료[položka_POČET] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(Soubor_položka_název, 원본자료, položka_POČET, 0);
}
int uživatel_START(int 미사용값) {
    (void)미사용값;
    int položka_POČET = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < položka_POČET; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (položka_POČET >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/sada.py");
        for (int 순번 = 1; 순번 < položka_POČET - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        položka_POČET--;
    }
    if (!položka_POČET || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!položka_POČET) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && položka_POČET != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(dynamická_paměť, dynamická_paměť + sizeof(dynamická_paměť)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *poziční_index = 전달인수[0]; *poziční_index; poziční_index++) if (*poziční_index == '/') 끝 = poziční_index;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < položka_POČET; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int Stav_HODNOTA = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Název = 낱말해석기->source_name;
        mp_parse_tree_t syntaxe_strom = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t 명령열 = mp_compile(&syntaxe_strom, Název, false);
        mp_call_function_0(명령열);
        nlr_pop();
    } else {
        mp_obj_t výjimka = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(výjimka)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t HODNOTA = mp_obj_exception_get_value(výjimka);
            Stav_HODNOTA = HODNOTA == mp_const_none ? 0 : mp_obj_is_int(HODNOTA) ? mp_obj_get_int(HODNOTA) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, výjimka); Stav_HODNOTA = 1; }
    }
    mp_deinit(); return Stav_HODNOTA;
}
