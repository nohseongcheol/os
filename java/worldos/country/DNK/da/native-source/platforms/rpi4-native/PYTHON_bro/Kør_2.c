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
static char heap_Lager[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 Dansk API를 쓴다.
static mp_obj_t åben_fil_objekt(size_t vare_TÆL, const mp_obj_t *Argumenter, mp_map_t *markering_VÆRDI) {
    (void)vare_TÆL; (void)Argumenter; (void)markering_VÆRDI;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, åben_fil_objekt);

mp_uint_t mp_hal_stdout_tx_strn(const char *Tekst, size_t varighed_VÆRDI) {
    intptr_t KR = 사용자호출(1, 1, (uintptr_t)Tekst, varighed_VÆRDI, 0, 0, 0);
    return KR < 0 ? 0 : KR;
}
void mp_hal_stdout_tx_str(const char *streng_data) { mp_hal_stdout_tx_strn(streng_data, strlen(streng_data)); }
void mp_hal_stdout_tx_strn_cooked(const char *streng_data, size_t vare_TÆL) { mp_hal_stdout_tx_strn(streng_data, vare_TÆL); }
void nlr_jump_fail(void *VÆRDI) {
    (void)VÆRDI;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *Sti) {
    intptr_t 종류 = 사용자호출(18, (uintptr_t)Sti, 0, 0, 0, 0, 0);
    return 종류 == 2 ? MP_IMPORT_STAT_DIR : 종류 == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr fil_post_navn) {
    intptr_t fil_handle = 사용자호출(3, (uintptr_t)qstr_str(fil_post_navn), 0, 0, 0, 0, 0);
    if (fil_handle < 0) mp_raise_OSError(-fil_handle);
    intptr_t post_TÆL_8f7753a1 = 사용자호출(2, fil_handle, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, fil_handle, 0, 0, 0, 0, 0);
    if (post_TÆL_8f7753a1 < 0) mp_raise_OSError(-post_TÆL_8f7753a1);
    원본자료[post_TÆL_8f7753a1] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(fil_post_navn, 원본자료, post_TÆL_8f7753a1, 0);
}
int bruger_START(int 미사용값) {
    (void)미사용값;
    int post_TÆL_8f7753a1 = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < post_TÆL_8f7753a1; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (post_TÆL_8f7753a1 >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/bundt.py");
        for (int 순번 = 1; 순번 < post_TÆL_8f7753a1 - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        post_TÆL_8f7753a1--;
    }
    if (!post_TÆL_8f7753a1 || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!post_TÆL_8f7753a1) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && post_TÆL_8f7753a1 != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(heap_Lager, heap_Lager + sizeof(heap_Lager)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *positionsindeks = 전달인수[0]; *positionsindeks; positionsindeks++) if (*positionsindeks == '/') 끝 = positionsindeks;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < post_TÆL_8f7753a1; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int status_VÆRDI = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Navn = 낱말해석기->source_name;
        mp_parse_tree_t syntaks_træ = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t 명령열 = mp_compile(&syntaks_træ, Navn, false);
        mp_call_function_0(명령열);
        nlr_pop();
    } else {
        mp_obj_t undtagelse = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(undtagelse)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t VÆRDI = mp_obj_exception_get_value(undtagelse);
            status_VÆRDI = VÆRDI == mp_const_none ? 0 : mp_obj_is_int(VÆRDI) ? mp_obj_get_int(VÆRDI) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, undtagelse); status_VÆRDI = 1; }
    }
    mp_deinit(); return status_VÆRDI;
}
