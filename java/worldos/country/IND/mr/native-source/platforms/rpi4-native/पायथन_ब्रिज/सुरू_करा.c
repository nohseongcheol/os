#include "../नामकरण/मशीन_लिंक_नावे.h"
#include <string.h>
#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "आवाहन.h"
static char गतिमानस्मृतिराशी_संग्रह[256 * 1024];
static char मूळ_डेटा[16385];
static char अग्रेषित_वितर्क[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 मराठी API를 쓴다.
static mp_obj_t संचिका_ऑब्जेक्ट_उघडा(size_t आयटम_संख्या, const mp_obj_t *बाबी, mp_map_t *निवड_मूल्य) {
    (void)आयटम_संख्या; (void)बाबी; (void)निवड_मूल्य;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, संचिका_ऑब्जेक्ट_उघडा);

mp_uint_t mp_hal_stdout_tx_strn(const char *पाठ्य, size_t लांबी_मूल्य) {
    intptr_t मोजमाप = प्रयोक्ता_आवाहन(1, 1, (uintptr_t)पाठ्य, लांबी_मूल्य, 0, 0, 0);
    return मोजमाप < 0 ? 0 : मोजमाप;
}
void mp_hal_stdout_tx_str(const char *स्ट्रींग_डेटा) { mp_hal_stdout_tx_strn(स्ट्रींग_डेटा, strlen(स्ट्रींग_डेटा)); }
void mp_hal_stdout_tx_strn_cooked(const char *स्ट्रींग_डेटा, size_t आयटम_संख्या) { mp_hal_stdout_tx_strn(स्ट्रींग_डेटा, आयटम_संख्या); }
void nlr_jump_fail(void *मूल्य) {
    (void)मूल्य;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    प्रयोक्ता_आवाहन(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *मार्ग) {
    intptr_t प्रकार_मूल्य = प्रयोक्ता_आवाहन(18, (uintptr_t)मार्ग, 0, 0, 0, 0, 0);
    return प्रकार_मूल्य == 2 ? MP_IMPORT_STAT_DIR : प्रकार_मूल्य == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr संचिका_प्रविष्टी_नाव) {
    intptr_t संचिका_हाताळा = प्रयोक्ता_आवाहन(3, (uintptr_t)qstr_str(संचिका_प्रविष्टी_नाव), 0, 0, 0, 0, 0);
    if (संचिका_हाताळा < 0) mp_raise_OSError(-संचिका_हाताळा);
    intptr_t प्रविष्टी_संख्या = प्रयोक्ता_आवाहन(2, संचिका_हाताळा, (uintptr_t)मूळ_डेटा, 16384, 0, 0, 0);
    प्रयोक्ता_आवाहन(4, संचिका_हाताळा, 0, 0, 0, 0, 0);
    if (प्रविष्टी_संख्या < 0) mp_raise_OSError(-प्रविष्टी_संख्या);
    मूळ_डेटा[प्रविष्टी_संख्या] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(संचिका_प्रविष्टी_नाव, मूळ_डेटा, प्रविष्टी_संख्या, 0);
}
int प्रयोक्ता_प्रारंभ(int नवापरलेले) {
    (void)नवापरलेले;
    int प्रविष्टी_संख्या = प्रयोक्ता_आवाहन(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int क्रमांक_अनुक्रमणिका = 0; क्रमांक_अनुक्रमणिका < प्रविष्टी_संख्या; क्रमांक_अनुक्रमणिका++) प्रयोक्ता_आवाहन(15, क्रमांक_अनुक्रमणिका, (uintptr_t)अग्रेषित_वितर्क[क्रमांक_अनुक्रमणिका], 256, 0, 0, 0);
    if (प्रविष्टी_संख्या >= 2 && !strcmp(अग्रेषित_वितर्क[0], "-m") && !strcmp(अग्रेषित_वितर्क[1], "pip")) {
        strcpy(अग्रेषित_वितर्क[0], "/lib/बंडल.py");
        for (int क्रमांक_अनुक्रमणिका = 1; क्रमांक_अनुक्रमणिका < प्रविष्टी_संख्या - 1; क्रमांक_अनुक्रमणिका++) strcpy(अग्रेषित_वितर्क[क्रमांक_अनुक्रमणिका], अग्रेषित_वितर्क[क्रमांक_अनुक्रमणिका + 1]);
        प्रविष्टी_संख्या--;
    }
    if (!प्रविष्टी_संख्या || !strcmp(अग्रेषित_वितर्क[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!प्रविष्टी_संख्या) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(अग्रेषित_वितर्क[0], "-c") && प्रविष्टी_संख्या != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(गतिमानस्मृतिराशी_संग्रह, गतिमानस्मृतिराशी_संग्रह + sizeof(गतिमानस्मृतिराशी_संग्रह)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (अग्रेषित_वितर्क[0][0] != '-') {
        const char *शेवट = NULL;
        for (const char *स्थान_अनुक्रमणिका = अग्रेषित_वितर्क[0]; *स्थान_अनुक्रमणिका; स्थान_अनुक्रमणिका++) if (*स्थान_अनुक्रमणिका == '/') शेवट = स्थान_अनुक्रमणिका;
        if (शेवट) mp_obj_list_append(mp_sys_path, mp_obj_new_str(अग्रेषित_वितर्क[0], शेवट - अग्रेषित_वितर्क[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int क्रमांक_अनुक्रमणिका = 0; क्रमांक_अनुक्रमणिका < प्रविष्टी_संख्या; क्रमांक_अनुक्रमणिका++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(अग्रेषित_वितर्क[क्रमांक_अनुक्रमणिका], strlen(अग्रेषित_वितर्क[क्रमांक_अनुक्रमणिका])));
    int राज्य_मूल्य = 0; nlr_buf_t अभाव_स्थानिक_परतकरा;
    if (nlr_push(&अभाव_स्थानिक_परतकरा) == 0) {
        mp_lexer_t *वर्णविश्लेषक = !strcmp(अग्रेषित_वितर्क[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, अग्रेषित_वितर्क[1], strlen(अग्रेषित_वितर्क[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(अग्रेषित_वितर्क[0]));
        qstr नाव = वर्णविश्लेषक->source_name;
        mp_parse_tree_t सिंटेक्स_ट्री = mp_parse(वर्णविश्लेषक, MP_PARSE_FILE_INPUT);
        mp_obj_t निर्देश_क्रम = mp_compile(&सिंटेक्स_ट्री, नाव, false);
        mp_call_function_0(निर्देश_क्रम);
        nlr_pop();
    } else {
        mp_obj_t अपवाद = MP_OBJ_FROM_PTR(अभाव_स्थानिक_परतकरा.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(अपवाद)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t मूल्य = mp_obj_exception_get_value(अपवाद);
            राज्य_मूल्य = मूल्य == mp_const_none ? 0 : mp_obj_is_int(मूल्य) ? mp_obj_get_int(मूल्य) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, अपवाद); राज्य_मूल्य = 1; }
    }
    mp_deinit(); return राज्य_मूल्य;
}
