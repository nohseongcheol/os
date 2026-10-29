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
static char dinamik_bellek[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 Türkçe API를 쓴다.
static mp_obj_t açık_Dosya_nesne(size_t öğe_BAĞ_DEĞ_SAY, const mp_obj_t *bağımsız_değişkenler, mp_map_t *seçim_değer) {
    (void)öğe_BAĞ_DEĞ_SAY; (void)bağımsız_değişkenler; (void)seçim_değer;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, açık_Dosya_nesne);

mp_uint_t mp_hal_stdout_tx_strn(const char *metin, size_t süre_değer) {
    intptr_t sonuç = 사용자호출(1, 1, (uintptr_t)metin, süre_değer, 0, 0, 0);
    return sonuç < 0 ? 0 : sonuç;
}
void mp_hal_stdout_tx_str(const char *dize_veri) { mp_hal_stdout_tx_strn(dize_veri, strlen(dize_veri)); }
void mp_hal_stdout_tx_strn_cooked(const char *dize_veri, size_t öğe_BAĞ_DEĞ_SAY) { mp_hal_stdout_tx_strn(dize_veri, öğe_BAĞ_DEĞ_SAY); }
void nlr_jump_fail(void *değer) {
    (void)değer;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *yol) {
    intptr_t Tip_değer = 사용자호출(18, (uintptr_t)yol, 0, 0, 0, 0, 0);
    return Tip_değer == 2 ? MP_IMPORT_STAT_DIR : Tip_değer == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr Dosya_girdi_ad) {
    intptr_t dosya_tanıtıcısı = 사용자호출(3, (uintptr_t)qstr_str(Dosya_girdi_ad), 0, 0, 0, 0, 0);
    if (dosya_tanıtıcısı < 0) mp_raise_OSError(-dosya_tanıtıcısı);
    intptr_t girdi_BAĞ_DEĞ_SAY = 사용자호출(2, dosya_tanıtıcısı, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, dosya_tanıtıcısı, 0, 0, 0, 0, 0);
    if (girdi_BAĞ_DEĞ_SAY < 0) mp_raise_OSError(-girdi_BAĞ_DEĞ_SAY);
    원본자료[girdi_BAĞ_DEĞ_SAY] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(Dosya_girdi_ad, 원본자료, girdi_BAĞ_DEĞ_SAY, 0);
}
int kullanıcı_Start(int 미사용값) {
    (void)미사용값;
    int girdi_BAĞ_DEĞ_SAY = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < girdi_BAĞ_DEĞ_SAY; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (girdi_BAĞ_DEĞ_SAY >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/paket_iş.py");
        for (int 순번 = 1; 순번 < girdi_BAĞ_DEĞ_SAY - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        girdi_BAĞ_DEĞ_SAY--;
    }
    if (!girdi_BAĞ_DEĞ_SAY || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!girdi_BAĞ_DEĞ_SAY) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && girdi_BAĞ_DEĞ_SAY != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(dinamik_bellek, dinamik_bellek + sizeof(dinamik_bellek)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *konum_dizini = 전달인수[0]; *konum_dizini; konum_dizini++) if (*konum_dizini == '/') 끝 = konum_dizini;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < girdi_BAĞ_DEĞ_SAY; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int Durum_değer = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr İsim = 낱말해석기->source_name;
        mp_parse_tree_t söz_dizimi_ağaç = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t 명령열 = mp_compile(&söz_dizimi_ağaç, İsim, false);
        mp_call_function_0(명령열);
        nlr_pop();
    } else {
        mp_obj_t özel_durum = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(özel_durum)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t değer = mp_obj_exception_get_value(özel_durum);
            Durum_değer = değer == mp_const_none ? 0 : mp_obj_is_int(değer) ? mp_obj_get_int(değer) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, özel_durum); Durum_değer = 1; }
    }
    mp_deinit(); return Durum_değer;
}
