#include "../nommage/nomsLierMachine.h"
#include <string.h>
#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "invoquer.h"
static char stockageTas[256 * 1024];
static char donnéesOriginal[16385];
static char argumentTransféré[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 français API를 쓴다.
static mp_obj_t ouvrirObjetFichier(size_t nombreÉlémentsÉlémentListe, const mp_obj_t *arguments, mp_map_t *valeurSélection) {
    (void)nombreÉlémentsÉlémentListe; (void)arguments; (void)valeurSélection;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, ouvrirObjetFichier);

mp_uint_t mp_hal_stdout_tx_strn(const char *texte, size_t longueur) {
    intptr_t résultat = invoquerUtilisateur(1, 1, (uintptr_t)texte, longueur, 0, 0, 0);
    return résultat < 0 ? 0 : résultat;
}
void mp_hal_stdout_tx_str(const char *donnéesChaîne) { mp_hal_stdout_tx_strn(donnéesChaîne, strlen(donnéesChaîne)); }
void mp_hal_stdout_tx_strn_cooked(const char *donnéesChaîne, size_t nombreÉlémentsÉlémentListe) { mp_hal_stdout_tx_strn(donnéesChaîne, nombreÉlémentsÉlémentListe); }
void nlr_jump_fail(void *valeur) {
    (void)valeur;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    invoquerUtilisateur(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *chemin) {
    intptr_t valeurGenre = invoquerUtilisateur(18, (uintptr_t)chemin, 0, 0, 0, 0, 0);
    return valeurGenre == 2 ? MP_IMPORT_STAT_DIR : valeurGenre == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr nomEntréeÉlémentFichier) {
    intptr_t poignéeFichier = invoquerUtilisateur(3, (uintptr_t)qstr_str(nomEntréeÉlémentFichier), 0, 0, 0, 0, 0);
    if (poignéeFichier < 0) mp_raise_OSError(-poignéeFichier);
    intptr_t nombreÉlémentsEntréeÉlément = invoquerUtilisateur(2, poignéeFichier, (uintptr_t)donnéesOriginal, 16384, 0, 0, 0);
    invoquerUtilisateur(4, poignéeFichier, 0, 0, 0, 0, 0);
    if (nombreÉlémentsEntréeÉlément < 0) mp_raise_OSError(-nombreÉlémentsEntréeÉlément);
    donnéesOriginal[nombreÉlémentsEntréeÉlément] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(nomEntréeÉlémentFichier, donnéesOriginal, nombreÉlémentsEntréeÉlément, 0);
}
int démarrerUtilisateur(int inutilisé) {
    (void)inutilisé;
    int nombreÉlémentsEntréeÉlément = invoquerUtilisateur(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsEntréeÉlément; indiceOrdinal++) invoquerUtilisateur(15, indiceOrdinal, (uintptr_t)argumentTransféré[indiceOrdinal], 256, 0, 0, 0);
    if (nombreÉlémentsEntréeÉlément >= 2 && !strcmp(argumentTransféré[0], "-m") && !strcmp(argumentTransféré[1], "pip")) {
        strcpy(argumentTransféré[0], "/lib/Paquet.py");
        for (int indiceOrdinal = 1; indiceOrdinal < nombreÉlémentsEntréeÉlément - 1; indiceOrdinal++) strcpy(argumentTransféré[indiceOrdinal], argumentTransféré[indiceOrdinal + 1]);
        nombreÉlémentsEntréeÉlément--;
    }
    if (!nombreÉlémentsEntréeÉlément || !strcmp(argumentTransféré[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!nombreÉlémentsEntréeÉlément) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(argumentTransféré[0], "-c") && nombreÉlémentsEntréeÉlément != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(stockageTas, stockageTas + sizeof(stockageTas)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (argumentTransféré[0][0] != '-') {
        const char *terminaison = NULL;
        for (const char *indicePosition = argumentTransféré[0]; *indicePosition; indicePosition++) if (*indicePosition == '/') terminaison = indicePosition;
        if (terminaison) mp_obj_list_append(mp_sys_path, mp_obj_new_str(argumentTransféré[0], terminaison - argumentTransféré[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsEntréeÉlément; indiceOrdinal++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(argumentTransféré[indiceOrdinal], strlen(argumentTransféré[indiceOrdinal])));
    int valeurÉtatValeur = 0; nlr_buf_t retournerLocalNon;
    if (nlr_push(&retournerLocalNon) == 0) {
        mp_lexer_t *AnalyseurLexical = !strcmp(argumentTransféré[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, argumentTransféré[1], strlen(argumentTransféré[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(argumentTransféré[0]));
        qstr nom = AnalyseurLexical->source_name;
        mp_parse_tree_t ArbreSyntaxe = mp_parse(AnalyseurLexical, MP_PARSE_FILE_INPUT);
        mp_obj_t séquenceInstructionMachine = mp_compile(&ArbreSyntaxe, nom, false);
        mp_call_function_0(séquenceInstructionMachine);
        nlr_pop();
    } else {
        mp_obj_t exception = MP_OBJ_FROM_PTR(retournerLocalNon.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(exception)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t valeur = mp_obj_exception_get_value(exception);
            valeurÉtatValeur = valeur == mp_const_none ? 0 : mp_obj_is_int(valeur) ? mp_obj_get_int(valeur) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, exception); valeurÉtatValeur = 1; }
    }
    mp_deinit(); return valeurÉtatValeur;
}
