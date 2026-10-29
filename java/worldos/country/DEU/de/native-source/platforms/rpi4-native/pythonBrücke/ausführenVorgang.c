#include "../benennung/maschineBindenNamen.h"
#include <string.h>
#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "aufrufen.h"
static char speicherhaldeSpeichergerät[256 * 1024];
static char ursprünglichDaten[16385];
static char weitergeleitetArgument[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 Deutsch API를 쓴다.
static mp_obj_t dateiObjektÖffnen(size_t elementeintragAnzahl, const mp_obj_t *argumente, mp_map_t *auswahlWert) {
    (void)elementeintragAnzahl; (void)argumente; (void)auswahlWert;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, dateiObjektÖffnen);

mp_uint_t mp_hal_stdout_tx_strn(const char *Text, size_t Länge) {
    intptr_t ergebnis = benutzerAufrufen(1, 1, (uintptr_t)Text, Länge, 0, 0, 0);
    return ergebnis < 0 ? 0 : ergebnis;
}
void mp_hal_stdout_tx_str(const char *zeichenketteDaten) { mp_hal_stdout_tx_strn(zeichenketteDaten, strlen(zeichenketteDaten)); }
void mp_hal_stdout_tx_strn_cooked(const char *zeichenketteDaten, size_t elementeintragAnzahl) { mp_hal_stdout_tx_strn(zeichenketteDaten, elementeintragAnzahl); }
void nlr_jump_fail(void *Wert) {
    (void)Wert;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    benutzerAufrufen(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *pfad) {
    intptr_t artWert = benutzerAufrufen(18, (uintptr_t)pfad, 0, 0, 0, 0, 0);
    return artWert == 2 ? MP_IMPORT_STAT_DIR : artWert == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr dateiEintragName) {
    intptr_t dateiKennwert = benutzerAufrufen(3, (uintptr_t)qstr_str(dateiEintragName), 0, 0, 0, 0, 0);
    if (dateiKennwert < 0) mp_raise_OSError(-dateiKennwert);
    intptr_t eintragAnzahl = benutzerAufrufen(2, dateiKennwert, (uintptr_t)ursprünglichDaten, 16384, 0, 0, 0);
    benutzerAufrufen(4, dateiKennwert, 0, 0, 0, 0, 0);
    if (eintragAnzahl < 0) mp_raise_OSError(-eintragAnzahl);
    ursprünglichDaten[eintragAnzahl] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(dateiEintragName, ursprünglichDaten, eintragAnzahl, 0);
}
int benutzerStarten(int unbenutzt) {
    (void)unbenutzt;
    int eintragAnzahl = benutzerAufrufen(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int ordnungszahlIndex = 0; ordnungszahlIndex < eintragAnzahl; ordnungszahlIndex++) benutzerAufrufen(15, ordnungszahlIndex, (uintptr_t)weitergeleitetArgument[ordnungszahlIndex], 256, 0, 0, 0);
    if (eintragAnzahl >= 2 && !strcmp(weitergeleitetArgument[0], "-m") && !strcmp(weitergeleitetArgument[1], "pip")) {
        strcpy(weitergeleitetArgument[0], "/lib/Paket.py");
        for (int ordnungszahlIndex = 1; ordnungszahlIndex < eintragAnzahl - 1; ordnungszahlIndex++) strcpy(weitergeleitetArgument[ordnungszahlIndex], weitergeleitetArgument[ordnungszahlIndex + 1]);
        eintragAnzahl--;
    }
    if (!eintragAnzahl || !strcmp(weitergeleitetArgument[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!eintragAnzahl) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(weitergeleitetArgument[0], "-c") && eintragAnzahl != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(speicherhaldeSpeichergerät, speicherhaldeSpeichergerät + sizeof(speicherhaldeSpeichergerät)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (weitergeleitetArgument[0][0] != '-') {
        const char *endung = NULL;
        for (const char *positionIndex = weitergeleitetArgument[0]; *positionIndex; positionIndex++) if (*positionIndex == '/') endung = positionIndex;
        if (endung) mp_obj_list_append(mp_sys_path, mp_obj_new_str(weitergeleitetArgument[0], endung - weitergeleitetArgument[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int ordnungszahlIndex = 0; ordnungszahlIndex < eintragAnzahl; ordnungszahlIndex++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(weitergeleitetArgument[ordnungszahlIndex], strlen(weitergeleitetArgument[ordnungszahlIndex])));
    int statuswertWert = 0; nlr_buf_t nichtLokalZurückkehren;
    if (nlr_push(&nichtLokalZurückkehren) == 0) {
        mp_lexer_t *Wortzerleger = !strcmp(weitergeleitetArgument[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, weitergeleitetArgument[1], strlen(weitergeleitetArgument[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(weitergeleitetArgument[0]));
        qstr Name = Wortzerleger->source_name;
        mp_parse_tree_t SatzbauBaum = mp_parse(Wortzerleger, MP_PARSE_FILE_INPUT);
        mp_obj_t befehlswortFolge = mp_compile(&SatzbauBaum, Name, false);
        mp_call_function_0(befehlswortFolge);
        nlr_pop();
    } else {
        mp_obj_t ausnahme = MP_OBJ_FROM_PTR(nichtLokalZurückkehren.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(ausnahme)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t Wert = mp_obj_exception_get_value(ausnahme);
            statuswertWert = Wert == mp_const_none ? 0 : mp_obj_is_int(Wert) ? mp_obj_get_int(Wert) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, ausnahme); statuswertWert = 1; }
    }
    mp_deinit(); return statuswertWert;
}
