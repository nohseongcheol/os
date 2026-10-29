#include "../denominación/nombresEnlazarMáquina.h"
#include <string.h>
#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "invocar.h"
static char almacenamientoMontículo[256 * 1024];
static char datosOriginal[16385];
static char argumentoReenviado[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 español API를 쓴다.
static mp_obj_t abrirObjetoArchivo(size_t númeroElementosElementoLista, const mp_obj_t *argumentos, mp_map_t *valorSelección) {
    (void)númeroElementosElementoLista; (void)argumentos; (void)valorSelección;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, abrirObjetoArchivo);

mp_uint_t mp_hal_stdout_tx_strn(const char *texto, size_t longitud) {
    intptr_t resultado = invocarUsuario(1, 1, (uintptr_t)texto, longitud, 0, 0, 0);
    return resultado < 0 ? 0 : resultado;
}
void mp_hal_stdout_tx_str(const char *datosCadena) { mp_hal_stdout_tx_strn(datosCadena, strlen(datosCadena)); }
void mp_hal_stdout_tx_strn_cooked(const char *datosCadena, size_t númeroElementosElementoLista) { mp_hal_stdout_tx_strn(datosCadena, númeroElementosElementoLista); }
void nlr_jump_fail(void *valor) {
    (void)valor;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    invocarUsuario(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *ruta) {
    intptr_t valorClaseTipo = invocarUsuario(18, (uintptr_t)ruta, 0, 0, 0, 0, 0);
    return valorClaseTipo == 2 ? MP_IMPORT_STAT_DIR : valorClaseTipo == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr nombreEntradaElementoArchivo) {
    intptr_t manejadorArchivo = invocarUsuario(3, (uintptr_t)qstr_str(nombreEntradaElementoArchivo), 0, 0, 0, 0, 0);
    if (manejadorArchivo < 0) mp_raise_OSError(-manejadorArchivo);
    intptr_t númeroElementosEntradaElemento = invocarUsuario(2, manejadorArchivo, (uintptr_t)datosOriginal, 16384, 0, 0, 0);
    invocarUsuario(4, manejadorArchivo, 0, 0, 0, 0, 0);
    if (númeroElementosEntradaElemento < 0) mp_raise_OSError(-númeroElementosEntradaElemento);
    datosOriginal[númeroElementosEntradaElemento] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(nombreEntradaElementoArchivo, datosOriginal, númeroElementosEntradaElemento, 0);
}
int iniciarUsuario(int sinUsar) {
    (void)sinUsar;
    int númeroElementosEntradaElemento = invocarUsuario(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int índiceOrdinal = 0; índiceOrdinal < númeroElementosEntradaElemento; índiceOrdinal++) invocarUsuario(15, índiceOrdinal, (uintptr_t)argumentoReenviado[índiceOrdinal], 256, 0, 0, 0);
    if (númeroElementosEntradaElemento >= 2 && !strcmp(argumentoReenviado[0], "-m") && !strcmp(argumentoReenviado[1], "pip")) {
        strcpy(argumentoReenviado[0], "/lib/Paquete.py");
        for (int índiceOrdinal = 1; índiceOrdinal < númeroElementosEntradaElemento - 1; índiceOrdinal++) strcpy(argumentoReenviado[índiceOrdinal], argumentoReenviado[índiceOrdinal + 1]);
        númeroElementosEntradaElemento--;
    }
    if (!númeroElementosEntradaElemento || !strcmp(argumentoReenviado[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!númeroElementosEntradaElemento) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(argumentoReenviado[0], "-c") && númeroElementosEntradaElemento != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(almacenamientoMontículo, almacenamientoMontículo + sizeof(almacenamientoMontículo)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (argumentoReenviado[0][0] != '-') {
        const char *terminación = NULL;
        for (const char *índicePosición = argumentoReenviado[0]; *índicePosición; índicePosición++) if (*índicePosición == '/') terminación = índicePosición;
        if (terminación) mp_obj_list_append(mp_sys_path, mp_obj_new_str(argumentoReenviado[0], terminación - argumentoReenviado[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int índiceOrdinal = 0; índiceOrdinal < númeroElementosEntradaElemento; índiceOrdinal++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(argumentoReenviado[índiceOrdinal], strlen(argumentoReenviado[índiceOrdinal])));
    int valorEstadoValor = 0; nlr_buf_t retornarLocalNoCondición;
    if (nlr_push(&retornarLocalNoCondición) == 0) {
        mp_lexer_t *AnalizadorLéxico = !strcmp(argumentoReenviado[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, argumentoReenviado[1], strlen(argumentoReenviado[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(argumentoReenviado[0]));
        qstr nombre = AnalizadorLéxico->source_name;
        mp_parse_tree_t ÁrbolSintaxis = mp_parse(AnalizadorLéxico, MP_PARSE_FILE_INPUT);
        mp_obj_t secuenciaInstrucciónMáquina = mp_compile(&ÁrbolSintaxis, nombre, false);
        mp_call_function_0(secuenciaInstrucciónMáquina);
        nlr_pop();
    } else {
        mp_obj_t excepción = MP_OBJ_FROM_PTR(retornarLocalNoCondición.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(excepción)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t valor = mp_obj_exception_get_value(excepción);
            valorEstadoValor = valor == mp_const_none ? 0 : mp_obj_is_int(valor) ? mp_obj_get_int(valor) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, excepción); valorEstadoValor = 1; }
    }
    mp_deinit(); return valorEstadoValor;
}
