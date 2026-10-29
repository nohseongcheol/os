#include "../명명/စက်ချိတ်အမည်များ.h"
#include <string.h>
#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "ခေါ်လုပ်.h"
static char ပုံတင်မှတ်ဉာဏ်သိုလှောင်ရာ[256 * 1024];
static char မူရင်းဒေတာ[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 မြန်မာ API를 쓴다.
static mp_obj_t ဖိုင်အရာဝတ္ထုဖွင့်(size_t အရေအတွက်, const mp_obj_t *အချက်များ, mp_map_t *ရွေးချယ်မှုတန်ဖိုး) {
    (void)အရေအတွက်; (void)အချက်များ; (void)ရွေးချယ်မှုတန်ဖိုး;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, ဖိုင်အရာဝတ္ထုဖွင့်);

mp_uint_t mp_hal_stdout_tx_strn(const char *စာသား, size_t အလျား) {
    intptr_t ရလဒ် = သုံးစွဲသူခေါ်လုပ်(1, 1, (uintptr_t)စာသား, အလျား, 0, 0, 0);
    return ရလဒ် < 0 ? 0 : ရလဒ်;
}
void mp_hal_stdout_tx_str(const char *အက္ခရာစဉ်ဒေတာ) { mp_hal_stdout_tx_strn(အက္ခရာစဉ်ဒေတာ, strlen(အက္ခရာစဉ်ဒေတာ)); }
void mp_hal_stdout_tx_strn_cooked(const char *အက္ခရာစဉ်ဒေတာ, size_t အရေအတွက်) { mp_hal_stdout_tx_strn(အက္ခရာစဉ်ဒေတာ, အရေအတွက်); }
void nlr_jump_fail(void *တန်ဖိုး) {
    (void)တန်ဖိုး;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    သုံးစွဲသူခေါ်လုပ်(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *လမ်း) {
    intptr_t အမျိုးအစားတန်ဖိုး = သုံးစွဲသူခေါ်လုပ်(18, (uintptr_t)လမ်း, 0, 0, 0, 0, 0);
    return အမျိုးအစားတန်ဖိုး == 2 ? MP_IMPORT_STAT_DIR : အမျိုးအစားတန်ဖိုး == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr ဖိုင်အချက်အမည်) {
    intptr_t ဖိုင်ကိုင်တွယ်ရာ = သုံးစွဲသူခေါ်လုပ်(3, (uintptr_t)qstr_str(ဖိုင်အချက်အမည်), 0, 0, 0, 0, 0);
    if (ဖိုင်ကိုင်တွယ်ရာ < 0) mp_raise_OSError(-ဖိုင်ကိုင်တွယ်ရာ);
    intptr_t အချက်အရေအတွက် = သုံးစွဲသူခေါ်လုပ်(2, ဖိုင်ကိုင်တွယ်ရာ, (uintptr_t)မူရင်းဒေတာ, 16384, 0, 0, 0);
    သုံးစွဲသူခေါ်လုပ်(4, ဖိုင်ကိုင်တွယ်ရာ, 0, 0, 0, 0, 0);
    if (အချက်အရေအတွက် < 0) mp_raise_OSError(-အချက်အရေအတွက်);
    မူရင်းဒေတာ[အချက်အရေအတွက်] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(ဖိုင်အချက်အမည်, မူရင်းဒေတာ, အချက်အရေအတွက်, 0);
}
int သုံးစွဲသူစတင်(int 미사용값) {
    (void)미사용값;
    int အချက်အရေအတွက် = သုံးစွဲသူခေါ်လုပ်(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int အစဉ်အမှတ် = 0; အစဉ်အမှတ် < အချက်အရေအတွက်; အစဉ်အမှတ်++) သုံးစွဲသူခေါ်လုပ်(15, အစဉ်အမှတ်, (uintptr_t)전달인수[အစဉ်အမှတ်], 256, 0, 0, 0);
    if (အချက်အရေအတွက် >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/အထုပ်.py");
        for (int အစဉ်အမှတ် = 1; အစဉ်အမှတ် < အချက်အရေအတွက် - 1; အစဉ်အမှတ်++) strcpy(전달인수[အစဉ်အမှတ်], 전달인수[အစဉ်အမှတ် + 1]);
        အချက်အရေအတွက်--;
    }
    if (!အချက်အရေအတွက် || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!အချက်အရေအတွက်) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && အချက်အရေအတွက် != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(ပုံတင်မှတ်ဉာဏ်သိုလှောင်ရာ, ပုံတင်မှတ်ဉာဏ်သိုလှောင်ရာ + sizeof(ပုံတင်မှတ်ဉာဏ်သိုလှောင်ရာ)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *အဆုံး = NULL;
        for (const char *နေရာအညွှန်းကိန်း = 전달인수[0]; *နေရာအညွှန်းကိန်း; နေရာအညွှန်းကိန်း++) if (*နေရာအညွှန်းကိန်း == '/') အဆုံး = နေရာအညွှန်းကိန်း;
        if (အဆုံး) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], အဆုံး - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int အစဉ်အမှတ် = 0; အစဉ်အမှတ် < အချက်အရေအတွက်; အစဉ်အမှတ်++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[အစဉ်အမှတ်], strlen(전달인수[အစဉ်အမှတ်])));
    int အခြေအနေတန်ဖိုး = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr အမည် = 낱말해석기->source_name;
        mp_parse_tree_t သဒ္ဒါအပင်ဖွဲ့စည်းပုံ = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t စက်ညွှန်ကြားချက်အစဉ်လိုက် = mp_compile(&သဒ္ဒါအပင်ဖွဲ့စည်းပုံ, အမည်, false);
        mp_call_function_0(စက်ညွှန်ကြားချက်အစဉ်လိုက်);
        nlr_pop();
    } else {
        mp_obj_t ခြွင်းချက် = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(ခြွင်းချက်)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t တန်ဖိုး = mp_obj_exception_get_value(ခြွင်းချက်);
            အခြေအနေတန်ဖိုး = တန်ဖိုး == mp_const_none ? 0 : mp_obj_is_int(တန်ဖိုး) ? mp_obj_get_int(တန်ဖိုး) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, ခြွင်းချက်); အခြေအနေတန်ဖိုး = 1; }
    }
    mp_deinit(); return အခြေအနေတန်ဖိုး;
}
