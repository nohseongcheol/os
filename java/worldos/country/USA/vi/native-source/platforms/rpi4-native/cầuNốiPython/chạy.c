#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include <string.h>
#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "gọiThựcHiện.h"
static char lưuTrữVùngNhớĐộng[256 * 1024];
static char dữLiệuNguyênBản[16385];
static char đốiSốĐãChuyểnTiếp[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 tiếngViệt API를 쓴다.
static mp_obj_t mởĐốiTượngTệp(size_t sốLượngPhầnMục, const mp_obj_t *cácĐốiSố, mp_map_t *giáTrịViệcChọn) {
    (void)sốLượngPhầnMục; (void)cácĐốiSố; (void)giáTrịViệcChọn;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, mởĐốiTượngTệp);

mp_uint_t mp_hal_stdout_tx_strn(const char *vănBản, size_t độDài) {
    intptr_t kếtQuả = gọiThựcHiệnNgườiDùng(1, 1, (uintptr_t)vănBản, độDài, 0, 0, 0);
    return kếtQuả < 0 ? 0 : kếtQuả;
}
void mp_hal_stdout_tx_str(const char *dữLiệuChuỗi) { mp_hal_stdout_tx_strn(dữLiệuChuỗi, strlen(dữLiệuChuỗi)); }
void mp_hal_stdout_tx_strn_cooked(const char *dữLiệuChuỗi, size_t sốLượngPhầnMục) { mp_hal_stdout_tx_strn(dữLiệuChuỗi, sốLượngPhầnMục); }
void nlr_jump_fail(void *giáTrị) {
    (void)giáTrị;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    gọiThựcHiệnNgườiDùng(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *đườngDẫn) {
    intptr_t giáTrịLoại = gọiThựcHiệnNgườiDùng(18, (uintptr_t)đườngDẫn, 0, 0, 0, 0, 0);
    return giáTrịLoại == 2 ? MP_IMPORT_STAT_DIR : giáTrịLoại == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr tênMụcTệp) {
    intptr_t thẻXửLýTệp = gọiThựcHiệnNgườiDùng(3, (uintptr_t)qstr_str(tênMụcTệp), 0, 0, 0, 0, 0);
    if (thẻXửLýTệp < 0) mp_raise_OSError(-thẻXửLýTệp);
    intptr_t sốLượngMục = gọiThựcHiệnNgườiDùng(2, thẻXửLýTệp, (uintptr_t)dữLiệuNguyênBản, 16384, 0, 0, 0);
    gọiThựcHiệnNgườiDùng(4, thẻXửLýTệp, 0, 0, 0, 0, 0);
    if (sốLượngMục < 0) mp_raise_OSError(-sốLượngMục);
    dữLiệuNguyênBản[sốLượngMục] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(tênMụcTệp, dữLiệuNguyênBản, sốLượngMục, 0);
}
int bắtChạyNgườiDùng(int chưaDùng) {
    (void)chưaDùng;
    int sốLượngMục = gọiThựcHiệnNgườiDùng(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngMục; chỉSốThứBậc++) gọiThựcHiệnNgườiDùng(15, chỉSốThứBậc, (uintptr_t)đốiSốĐãChuyểnTiếp[chỉSốThứBậc], 256, 0, 0, 0);
    if (sốLượngMục >= 2 && !strcmp(đốiSốĐãChuyểnTiếp[0], "-m") && !strcmp(đốiSốĐãChuyểnTiếp[1], "pip")) {
        strcpy(đốiSốĐãChuyểnTiếp[0], "/lib/GóiGộp.py");
        for (int chỉSốThứBậc = 1; chỉSốThứBậc < sốLượngMục - 1; chỉSốThứBậc++) strcpy(đốiSốĐãChuyểnTiếp[chỉSốThứBậc], đốiSốĐãChuyểnTiếp[chỉSốThứBậc + 1]);
        sốLượngMục--;
    }
    if (!sốLượngMục || !strcmp(đốiSốĐãChuyểnTiếp[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!sốLượngMục) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(đốiSốĐãChuyểnTiếp[0], "-c") && sốLượngMục != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(lưuTrữVùngNhớĐộng, lưuTrữVùngNhớĐộng + sizeof(lưuTrữVùngNhớĐộng)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (đốiSốĐãChuyểnTiếp[0][0] != '-') {
        const char *phầnKết = NULL;
        for (const char *chỉSốVịTrí = đốiSốĐãChuyểnTiếp[0]; *chỉSốVịTrí; chỉSốVịTrí++) if (*chỉSốVịTrí == '/') phầnKết = chỉSốVịTrí;
        if (phầnKết) mp_obj_list_append(mp_sys_path, mp_obj_new_str(đốiSốĐãChuyểnTiếp[0], phầnKết - đốiSốĐãChuyểnTiếp[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngMục; chỉSốThứBậc++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(đốiSốĐãChuyểnTiếp[chỉSốThứBậc], strlen(đốiSốĐãChuyểnTiếp[chỉSốThứBậc])));
    int giáTrịTrạngThái = 0; nlr_buf_t trảVềCụcBộPhi;
    if (nlr_push(&trảVềCụcBộPhi) == 0) {
        mp_lexer_t *BộTáchTừ = !strcmp(đốiSốĐãChuyểnTiếp[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, đốiSốĐãChuyểnTiếp[1], strlen(đốiSốĐãChuyểnTiếp[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(đốiSốĐãChuyểnTiếp[0]));
        qstr tên = BộTáchTừ->source_name;
        mp_parse_tree_t CâyCúPháp = mp_parse(BộTáchTừ, MP_PARSE_FILE_INPUT);
        mp_obj_t dãyChỉLệnh = mp_compile(&CâyCúPháp, tên, false);
        mp_call_function_0(dãyChỉLệnh);
        nlr_pop();
    } else {
        mp_obj_t ngoạiLệ = MP_OBJ_FROM_PTR(trảVềCụcBộPhi.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(ngoạiLệ)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t giáTrị = mp_obj_exception_get_value(ngoạiLệ);
            giáTrịTrạngThái = giáTrị == mp_const_none ? 0 : mp_obj_is_int(giáTrị) ? mp_obj_get_int(giáTrị) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, ngoạiLệ); giáTrịTrạngThái = 1; }
    }
    mp_deinit(); return giáTrịTrạngThái;
}
