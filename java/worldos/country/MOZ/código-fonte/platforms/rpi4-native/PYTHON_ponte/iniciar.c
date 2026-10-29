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
static char memória_dinâmica[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 Português API를 쓴다.
static mp_obj_t abrir_Arquivo_objeto(size_t item_CONT_NÚM, const mp_obj_t *argumentos, mp_map_t *seleção_VALOR) {
    (void)item_CONT_NÚM; (void)argumentos; (void)seleção_VALOR;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, abrir_Arquivo_objeto);

mp_uint_t mp_hal_stdout_tx_strn(const char *texto, size_t duração_VALOR) {
    intptr_t resultado = 사용자호출(1, 1, (uintptr_t)texto, duração_VALOR, 0, 0, 0);
    return resultado < 0 ? 0 : resultado;
}
void mp_hal_stdout_tx_str(const char *cadeia_dados) { mp_hal_stdout_tx_strn(cadeia_dados, strlen(cadeia_dados)); }
void mp_hal_stdout_tx_strn_cooked(const char *cadeia_dados, size_t item_CONT_NÚM) { mp_hal_stdout_tx_strn(cadeia_dados, item_CONT_NÚM); }
void nlr_jump_fail(void *VALOR) {
    (void)VALOR;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *caminho) {
    intptr_t Tipo_VALOR = 사용자호출(18, (uintptr_t)caminho, 0, 0, 0, 0, 0);
    return Tipo_VALOR == 2 ? MP_IMPORT_STAT_DIR : Tipo_VALOR == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr Arquivo_entrada_nome) {
    intptr_t identificador_de_arquivo = 사용자호출(3, (uintptr_t)qstr_str(Arquivo_entrada_nome), 0, 0, 0, 0, 0);
    if (identificador_de_arquivo < 0) mp_raise_OSError(-identificador_de_arquivo);
    intptr_t entrada_CONT_NÚM_8f7753a1 = 사용자호출(2, identificador_de_arquivo, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, identificador_de_arquivo, 0, 0, 0, 0, 0);
    if (entrada_CONT_NÚM_8f7753a1 < 0) mp_raise_OSError(-entrada_CONT_NÚM_8f7753a1);
    원본자료[entrada_CONT_NÚM_8f7753a1] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(Arquivo_entrada_nome, 원본자료, entrada_CONT_NÚM_8f7753a1, 0);
}
int usuário_START(int 미사용값) {
    (void)미사용값;
    int entrada_CONT_NÚM_8f7753a1 = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < entrada_CONT_NÚM_8f7753a1; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (entrada_CONT_NÚM_8f7753a1 >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/grupo.py");
        for (int 순번 = 1; 순번 < entrada_CONT_NÚM_8f7753a1 - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        entrada_CONT_NÚM_8f7753a1--;
    }
    if (!entrada_CONT_NÚM_8f7753a1 || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!entrada_CONT_NÚM_8f7753a1) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && entrada_CONT_NÚM_8f7753a1 != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(memória_dinâmica, memória_dinâmica + sizeof(memória_dinâmica)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *cargo_ÍNDICE = 전달인수[0]; *cargo_ÍNDICE; cargo_ÍNDICE++) if (*cargo_ÍNDICE == '/') 끝 = cargo_ÍNDICE;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < entrada_CONT_NÚM_8f7753a1; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int Estado_VALOR = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Nome = 낱말해석기->source_name;
        mp_parse_tree_t sintaxe_árvore = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t instrução_SEQUÊNCIA = mp_compile(&sintaxe_árvore, Nome, false);
        mp_call_function_0(instrução_SEQUÊNCIA);
        nlr_pop();
    } else {
        mp_obj_t exceção = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(exceção)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t VALOR = mp_obj_exception_get_value(exceção);
            Estado_VALOR = VALOR == mp_const_none ? 0 : mp_obj_is_int(VALOR) ? mp_obj_get_int(VALOR) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, exceção); Estado_VALOR = 1; }
    }
    mp_deinit(); return Estado_VALOR;
}
