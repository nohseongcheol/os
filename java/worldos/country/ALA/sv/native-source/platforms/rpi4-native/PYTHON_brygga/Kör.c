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
static char dynamiskt_minne[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 Svenska API를 쓴다.
static mp_obj_t skapa_fil_objekt(size_t objekt_ANTAL, const mp_obj_t *argument, mp_map_t *markering_värde) {
    (void)objekt_ANTAL; (void)argument; (void)markering_värde;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, skapa_fil_objekt);

mp_uint_t mp_hal_stdout_tx_strn(const char *text, size_t längd_värde) {
    intptr_t RESULTAT = 사용자호출(1, 1, (uintptr_t)text, längd_värde, 0, 0, 0);
    return RESULTAT < 0 ? 0 : RESULTAT;
}
void mp_hal_stdout_tx_str(const char *sträng_data) { mp_hal_stdout_tx_strn(sträng_data, strlen(sträng_data)); }
void mp_hal_stdout_tx_strn_cooked(const char *sträng_data, size_t objekt_ANTAL) { mp_hal_stdout_tx_strn(sträng_data, objekt_ANTAL); }
void nlr_jump_fail(void *värde) {
    (void)värde;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *sökväg_2) {
    intptr_t variant_värde = 사용자호출(18, (uintptr_t)sökväg_2, 0, 0, 0, 0, 0);
    return variant_värde == 2 ? MP_IMPORT_STAT_DIR : variant_värde == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr fil_post_namn) {
    intptr_t filreferens = 사용자호출(3, (uintptr_t)qstr_str(fil_post_namn), 0, 0, 0, 0, 0);
    if (filreferens < 0) mp_raise_OSError(-filreferens);
    intptr_t post_ANTAL = 사용자호출(2, filreferens, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, filreferens, 0, 0, 0, 0, 0);
    if (post_ANTAL < 0) mp_raise_OSError(-post_ANTAL);
    원본자료[post_ANTAL] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(fil_post_namn, 원본자료, post_ANTAL, 0);
}
int användare_START(int 미사용값) {
    (void)미사용값;
    int post_ANTAL = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < post_ANTAL; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (post_ANTAL >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/bunt.py");
        for (int 순번 = 1; 순번 < post_ANTAL - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        post_ANTAL--;
    }
    if (!post_ANTAL || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!post_ANTAL) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && post_ANTAL != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(dynamiskt_minne, dynamiskt_minne + sizeof(dynamiskt_minne)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *positionsindex = 전달인수[0]; *positionsindex; positionsindex++) if (*positionsindex == '/') 끝 = positionsindex;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < post_ANTAL; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int status_värde = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Namn = 낱말해석기->source_name;
        mp_parse_tree_t syntax_träd = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t instruktion_SEKVENS = mp_compile(&syntax_träd, Namn, false);
        mp_call_function_0(instruktion_SEKVENS);
        nlr_pop();
    } else {
        mp_obj_t fel_31f743d2 = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(fel_31f743d2)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t värde = mp_obj_exception_get_value(fel_31f743d2);
            status_värde = värde == mp_const_none ? 0 : mp_obj_is_int(värde) ? mp_obj_get_int(värde) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, fel_31f743d2); status_värde = 1; }
    }
    mp_deinit(); return status_värde;
}
