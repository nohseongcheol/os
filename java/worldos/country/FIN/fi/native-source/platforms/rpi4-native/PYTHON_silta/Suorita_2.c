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
static char dynaaminen_muisti[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 suomi API를 쓴다.
static mp_obj_t avata_Tiedosto_objekti(size_t kohde_LASKE, const mp_obj_t *argumentit, mp_map_t *valinta_ARVO) {
    (void)kohde_LASKE; (void)argumentit; (void)valinta_ARVO;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, avata_Tiedosto_objekti);

mp_uint_t mp_hal_stdout_tx_strn(const char *teksti, size_t kesto_ARVO) {
    intptr_t TULOS = 사용자호출(1, 1, (uintptr_t)teksti, kesto_ARVO, 0, 0, 0);
    return TULOS < 0 ? 0 : TULOS;
}
void mp_hal_stdout_tx_str(const char *merkkijono_data) { mp_hal_stdout_tx_strn(merkkijono_data, strlen(merkkijono_data)); }
void mp_hal_stdout_tx_strn_cooked(const char *merkkijono_data, size_t kohde_LASKE) { mp_hal_stdout_tx_strn(merkkijono_data, kohde_LASKE); }
void nlr_jump_fail(void *ARVO) {
    (void)ARVO;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *polku_2) {
    intptr_t 종류 = 사용자호출(18, (uintptr_t)polku_2, 0, 0, 0, 0, 0);
    return 종류 == 2 ? MP_IMPORT_STAT_DIR : 종류 == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr Tiedosto_merkintä_nimi) {
    intptr_t Tiedosto_kahva = 사용자호출(3, (uintptr_t)qstr_str(Tiedosto_merkintä_nimi), 0, 0, 0, 0, 0);
    if (Tiedosto_kahva < 0) mp_raise_OSError(-Tiedosto_kahva);
    intptr_t merkintä_LASKE = 사용자호출(2, Tiedosto_kahva, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, Tiedosto_kahva, 0, 0, 0, 0, 0);
    if (merkintä_LASKE < 0) mp_raise_OSError(-merkintä_LASKE);
    원본자료[merkintä_LASKE] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(Tiedosto_merkintä_nimi, 원본자료, merkintä_LASKE, 0);
}
int käyttäjä_alku(int 미사용값) {
    (void)미사용값;
    int merkintä_LASKE = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < merkintä_LASKE; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (merkintä_LASKE >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/nippu.py");
        for (int 순번 = 1; 순번 < merkintä_LASKE - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        merkintä_LASKE--;
    }
    if (!merkintä_LASKE || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!merkintä_LASKE) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && merkintä_LASKE != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(dynaaminen_muisti, dynaaminen_muisti + sizeof(dynaaminen_muisti)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *sijainti = 전달인수[0]; *sijainti; sijainti++) if (*sijainti == '/') 끝 = sijainti;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < merkintä_LASKE; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int Tila_ARVO = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Nimi = 낱말해석기->source_name;
        mp_parse_tree_t syntaksi_puu = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t käsky_JONO = mp_compile(&syntaksi_puu, Nimi, false);
        mp_call_function_0(käsky_JONO);
        nlr_pop();
    } else {
        mp_obj_t poikkeus = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(poikkeus)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t ARVO = mp_obj_exception_get_value(poikkeus);
            Tila_ARVO = ARVO == mp_const_none ? 0 : mp_obj_is_int(ARVO) ? mp_obj_get_int(ARVO) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, poikkeus); Tila_ARVO = 1; }
    }
    mp_deinit(); return Tila_ARVO;
}
