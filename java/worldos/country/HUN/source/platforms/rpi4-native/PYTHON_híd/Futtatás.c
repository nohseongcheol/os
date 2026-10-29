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
static char halommemória_tár[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 magyar API를 쓴다.
static mp_obj_t készít_Fájl_objektum(size_t cikk_DARAB, const mp_obj_t *Argumentumok, mp_map_t *kijelölés_ÉRTÉK) {
    (void)cikk_DARAB; (void)Argumentumok; (void)kijelölés_ÉRTÉK;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, készít_Fájl_objektum);

mp_uint_t mp_hal_stdout_tx_strn(const char *Szöveg, size_t hossz_ÉRTÉK) {
    intptr_t KR = 사용자호출(1, 1, (uintptr_t)Szöveg, hossz_ÉRTÉK, 0, 0, 0);
    return KR < 0 ? 0 : KR;
}
void mp_hal_stdout_tx_str(const char *sztring_adat) { mp_hal_stdout_tx_strn(sztring_adat, strlen(sztring_adat)); }
void mp_hal_stdout_tx_strn_cooked(const char *sztring_adat, size_t cikk_DARAB) { mp_hal_stdout_tx_strn(sztring_adat, cikk_DARAB); }
void nlr_jump_fail(void *ÉRTÉK) {
    (void)ÉRTÉK;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *ÚTVONAL) {
    intptr_t Altípus_ÉRTÉK = 사용자호출(18, (uintptr_t)ÚTVONAL, 0, 0, 0, 0, 0);
    return Altípus_ÉRTÉK == 2 ? MP_IMPORT_STAT_DIR : Altípus_ÉRTÉK == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr Fájl_bejegyzés_név) {
    intptr_t fájlleíró = 사용자호출(3, (uintptr_t)qstr_str(Fájl_bejegyzés_név), 0, 0, 0, 0, 0);
    if (fájlleíró < 0) mp_raise_OSError(-fájlleíró);
    intptr_t bejegyzés_DARAB = 사용자호출(2, fájlleíró, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, fájlleíró, 0, 0, 0, 0, 0);
    if (bejegyzés_DARAB < 0) mp_raise_OSError(-bejegyzés_DARAB);
    원본자료[bejegyzés_DARAB] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(Fájl_bejegyzés_név, 원본자료, bejegyzés_DARAB, 0);
}
int felhasználó_START(int 미사용값) {
    (void)미사용값;
    int bejegyzés_DARAB = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < bejegyzés_DARAB; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (bejegyzés_DARAB >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/köteg.py");
        for (int 순번 = 1; 순번 < bejegyzés_DARAB - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        bejegyzés_DARAB--;
    }
    if (!bejegyzés_DARAB || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!bejegyzés_DARAB) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && bejegyzés_DARAB != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(halommemória_tár, halommemória_tár + sizeof(halommemória_tár)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *helyzetindex = 전달인수[0]; *helyzetindex; helyzetindex++) if (*helyzetindex == '/') 끝 = helyzetindex;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < bejegyzés_DARAB; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int Állapot_ÉRTÉK = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Név = 낱말해석기->source_name;
        mp_parse_tree_t szintaxis_fa = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t 명령열 = mp_compile(&szintaxis_fa, Név, false);
        mp_call_function_0(명령열);
        nlr_pop();
    } else {
        mp_obj_t kivétel = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(kivétel)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t ÉRTÉK = mp_obj_exception_get_value(kivétel);
            Állapot_ÉRTÉK = ÉRTÉK == mp_const_none ? 0 : mp_obj_is_int(ÉRTÉK) ? mp_obj_get_int(ÉRTÉK) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, kivétel); Állapot_ÉRTÉK = 1; }
    }
    mp_deinit(); return Állapot_ÉRTÉK;
}
