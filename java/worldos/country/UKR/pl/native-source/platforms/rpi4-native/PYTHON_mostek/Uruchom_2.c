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
static char pamięć_dynamiczna[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 polski API를 쓴다.
static mp_obj_t otwarty_Plik_obiekt(size_t towar_ILE_LICZB, const mp_obj_t *argumenty, mp_map_t *zaznaczenie_WARTOŚĆ) {
    (void)towar_ILE_LICZB; (void)argumenty; (void)zaznaczenie_WARTOŚĆ;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, otwarty_Plik_obiekt);

mp_uint_t mp_hal_stdout_tx_strn(const char *tekst, size_t długość_WARTOŚĆ) {
    intptr_t WYNIK = 사용자호출(1, 1, (uintptr_t)tekst, długość_WARTOŚĆ, 0, 0, 0);
    return WYNIK < 0 ? 0 : WYNIK;
}
void mp_hal_stdout_tx_str(const char *ciąg_dane) { mp_hal_stdout_tx_strn(ciąg_dane, strlen(ciąg_dane)); }
void mp_hal_stdout_tx_strn_cooked(const char *ciąg_dane, size_t towar_ILE_LICZB) { mp_hal_stdout_tx_strn(ciąg_dane, towar_ILE_LICZB); }
void nlr_jump_fail(void *WARTOŚĆ) {
    (void)WARTOŚĆ;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *ścieżka_2) {
    intptr_t Rodzaj_WARTOŚĆ = 사용자호출(18, (uintptr_t)ścieżka_2, 0, 0, 0, 0, 0);
    return Rodzaj_WARTOŚĆ == 2 ? MP_IMPORT_STAT_DIR : Rodzaj_WARTOŚĆ == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr Plik_wpis_nazwa) {
    intptr_t dojście_do_pliku = 사용자호출(3, (uintptr_t)qstr_str(Plik_wpis_nazwa), 0, 0, 0, 0, 0);
    if (dojście_do_pliku < 0) mp_raise_OSError(-dojście_do_pliku);
    intptr_t wpis_ILE_LICZB = 사용자호출(2, dojście_do_pliku, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, dojście_do_pliku, 0, 0, 0, 0, 0);
    if (wpis_ILE_LICZB < 0) mp_raise_OSError(-wpis_ILE_LICZB);
    원본자료[wpis_ILE_LICZB] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(Plik_wpis_nazwa, 원본자료, wpis_ILE_LICZB, 0);
}
int użytkownik_START(int 미사용값) {
    (void)미사용값;
    int wpis_ILE_LICZB = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < wpis_ILE_LICZB; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (wpis_ILE_LICZB >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/pakiet.py");
        for (int 순번 = 1; 순번 < wpis_ILE_LICZB - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        wpis_ILE_LICZB--;
    }
    if (!wpis_ILE_LICZB || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!wpis_ILE_LICZB) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && wpis_ILE_LICZB != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(pamięć_dynamiczna, pamięć_dynamiczna + sizeof(pamięć_dynamiczna)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *indeks_pozycji = 전달인수[0]; *indeks_pozycji; indeks_pozycji++) if (*indeks_pozycji == '/') 끝 = indeks_pozycji;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < wpis_ILE_LICZB; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int Stan_WARTOŚĆ = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Nazwa = 낱말해석기->source_name;
        mp_parse_tree_t składnia_drzewo = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t instrukcja_SEKWENCJA = mp_compile(&składnia_drzewo, Nazwa, false);
        mp_call_function_0(instrukcja_SEKWENCJA);
        nlr_pop();
    } else {
        mp_obj_t wyjątek = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(wyjątek)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t WARTOŚĆ = mp_obj_exception_get_value(wyjątek);
            Stan_WARTOŚĆ = WARTOŚĆ == mp_const_none ? 0 : mp_obj_is_int(WARTOŚĆ) ? mp_obj_get_int(WARTOŚĆ) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, wyjątek); Stan_WARTOŚĆ = 1; }
    }
    mp_deinit(); return Stan_WARTOŚĆ;
}
