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

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 Català API를 쓴다.
static mp_obj_t crear_arxiu_objecte(size_t element_COMPT, const mp_obj_t *인수, mp_map_t *selecció_VALOR) {
    (void)element_COMPT; (void)인수; (void)selecció_VALOR;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, crear_arxiu_objecte);

mp_uint_t mp_hal_stdout_tx_strn(const char *SMS, size_t durada_VALOR) {
    intptr_t RESULTAT = 사용자호출(1, 1, (uintptr_t)SMS, durada_VALOR, 0, 0, 0);
    return RESULTAT < 0 ? 0 : RESULTAT;
}
void mp_hal_stdout_tx_str(const char *cadena_dades) { mp_hal_stdout_tx_strn(cadena_dades, strlen(cadena_dades)); }
void mp_hal_stdout_tx_strn_cooked(const char *cadena_dades, size_t element_COMPT) { mp_hal_stdout_tx_strn(cadena_dades, element_COMPT); }
void nlr_jump_fail(void *VALOR) {
    (void)VALOR;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *Camí) {
    intptr_t 종류 = 사용자호출(18, (uintptr_t)Camí, 0, 0, 0, 0, 0);
    return 종류 == 2 ? MP_IMPORT_STAT_DIR : 종류 == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr arxiu_introducció_nom) {
    intptr_t arxiu_control_7f4cdfd5 = 사용자호출(3, (uintptr_t)qstr_str(arxiu_introducció_nom), 0, 0, 0, 0, 0);
    if (arxiu_control_7f4cdfd5 < 0) mp_raise_OSError(-arxiu_control_7f4cdfd5);
    intptr_t introducció_COMPT = 사용자호출(2, arxiu_control_7f4cdfd5, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, arxiu_control_7f4cdfd5, 0, 0, 0, 0, 0);
    if (introducció_COMPT < 0) mp_raise_OSError(-introducció_COMPT);
    원본자료[introducció_COMPT] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(arxiu_introducció_nom, 원본자료, introducció_COMPT, 0);
}
int usuari_Inici(int 미사용값) {
    (void)미사용값;
    int introducció_COMPT = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < introducció_COMPT; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (introducció_COMPT >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/paquet.py");
        for (int 순번 = 1; 순번 < introducció_COMPT - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        introducció_COMPT--;
    }
    if (!introducció_COMPT || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!introducció_COMPT) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && introducció_COMPT != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(동적기억공간, 동적기억공간 + sizeof(동적기억공간)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *càrrec_INDEX = 전달인수[0]; *càrrec_INDEX; càrrec_INDEX++) if (*càrrec_INDEX == '/') 끝 = càrrec_INDEX;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < introducció_COMPT; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int Estat_VALOR = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Nom = 낱말해석기->source_name;
        mp_parse_tree_t sintaxi_arbre = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t instrucció_SEQÜÈNCIA = mp_compile(&sintaxi_arbre, Nom, false);
        mp_call_function_0(instrucció_SEQÜÈNCIA);
        nlr_pop();
    } else {
        mp_obj_t excepció = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(excepció)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t VALOR = mp_obj_exception_get_value(excepció);
            Estat_VALOR = VALOR == mp_const_none ? 0 : mp_obj_is_int(VALOR) ? mp_obj_get_int(VALOR) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, excepció); Estat_VALOR = 1; }
    }
    mp_deinit(); return Estat_VALOR;
}
