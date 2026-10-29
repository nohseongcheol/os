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
static char memoria_dinamica[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 Italiano API를 쓴다.
static mp_obj_t aperto_File_oggetto(size_t articolo_CONTA_NUMERI, const mp_obj_t *argomenti, mp_map_t *selezione_VALORE) {
    (void)articolo_CONTA_NUMERI; (void)argomenti; (void)selezione_VALORE;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, aperto_File_oggetto);

mp_uint_t mp_hal_stdout_tx_strn(const char *testo, size_t durata_VALORE) {
    intptr_t risultato = 사용자호출(1, 1, (uintptr_t)testo, durata_VALORE, 0, 0, 0);
    return risultato < 0 ? 0 : risultato;
}
void mp_hal_stdout_tx_str(const char *stringa_dati) { mp_hal_stdout_tx_strn(stringa_dati, strlen(stringa_dati)); }
void mp_hal_stdout_tx_strn_cooked(const char *stringa_dati, size_t articolo_CONTA_NUMERI) { mp_hal_stdout_tx_strn(stringa_dati, articolo_CONTA_NUMERI); }
void nlr_jump_fail(void *VALORE) {
    (void)VALORE;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *percorso) {
    intptr_t Kind_VALORE = 사용자호출(18, (uintptr_t)percorso, 0, 0, 0, 0, 0);
    return Kind_VALORE == 2 ? MP_IMPORT_STAT_DIR : Kind_VALORE == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr File_voce_nome) {
    intptr_t handle_di_file = 사용자호출(3, (uintptr_t)qstr_str(File_voce_nome), 0, 0, 0, 0, 0);
    if (handle_di_file < 0) mp_raise_OSError(-handle_di_file);
    intptr_t voce_CONTA_NUMERI = 사용자호출(2, handle_di_file, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, handle_di_file, 0, 0, 0, 0, 0);
    if (voce_CONTA_NUMERI < 0) mp_raise_OSError(-voce_CONTA_NUMERI);
    원본자료[voce_CONTA_NUMERI] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(File_voce_nome, 원본자료, voce_CONTA_NUMERI, 0);
}
int USER_START(int 미사용값) {
    (void)미사용값;
    int voce_CONTA_NUMERI = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < voce_CONTA_NUMERI; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (voce_CONTA_NUMERI >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/aggregare.py");
        for (int 순번 = 1; 순번 < voce_CONTA_NUMERI - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        voce_CONTA_NUMERI--;
    }
    if (!voce_CONTA_NUMERI || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!voce_CONTA_NUMERI) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && voce_CONTA_NUMERI != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(memoria_dinamica, memoria_dinamica + sizeof(memoria_dinamica)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *funzione_INDICE = 전달인수[0]; *funzione_INDICE; funzione_INDICE++) if (*funzione_INDICE == '/') 끝 = funzione_INDICE;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < voce_CONTA_NUMERI; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int Stato_VALORE = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Nome = 낱말해석기->source_name;
        mp_parse_tree_t sintassi_albero = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t istruzione_SEQUENZA = mp_compile(&sintassi_albero, Nome, false);
        mp_call_function_0(istruzione_SEQUENZA);
        nlr_pop();
    } else {
        mp_obj_t eccezione = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(eccezione)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t VALORE = mp_obj_exception_get_value(eccezione);
            Stato_VALORE = VALORE == mp_const_none ? 0 : mp_obj_is_int(VALORE) ? mp_obj_get_int(VALORE) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, eccezione); Stato_VALORE = 1; }
    }
    mp_deinit(); return Stato_VALORE;
}
