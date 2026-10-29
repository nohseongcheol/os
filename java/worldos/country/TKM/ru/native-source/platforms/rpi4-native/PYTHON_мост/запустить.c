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
static char динамическая_память[256 * 1024];
static char 원본자료[16385];
static char 전달인수[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 русский API를 쓴다.
static mp_obj_t открыть_файл_объект(size_t товар_СЧЁТ, const mp_obj_t *аргументы, mp_map_t *выделение_ЗНАЧЕН) {
    (void)товар_СЧЁТ; (void)аргументы; (void)выделение_ЗНАЧЕН;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, открыть_файл_объект);

mp_uint_t mp_hal_stdout_tx_strn(const char *текст, size_t длина_ЗНАЧЕН) {
    intptr_t результат = 사용자호출(1, 1, (uintptr_t)текст, длина_ЗНАЧЕН, 0, 0, 0);
    return результат < 0 ? 0 : результат;
}
void mp_hal_stdout_tx_str(const char *строка_данные) { mp_hal_stdout_tx_strn(строка_данные, strlen(строка_данные)); }
void mp_hal_stdout_tx_strn_cooked(const char *строка_данные, size_t товар_СЧЁТ) { mp_hal_stdout_tx_strn(строка_данные, товар_СЧЁТ); }
void nlr_jump_fail(void *ЗНАЧЕН) {
    (void)ЗНАЧЕН;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    사용자호출(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *путь) {
    intptr_t Вид_ЗНАЧЕН = 사용자호출(18, (uintptr_t)путь, 0, 0, 0, 0, 0);
    return Вид_ЗНАЧЕН == 2 ? MP_IMPORT_STAT_DIR : Вид_ЗНАЧЕН == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr файл_ввод_имя) {
    intptr_t дескриптор_файла = 사용자호출(3, (uintptr_t)qstr_str(файл_ввод_имя), 0, 0, 0, 0, 0);
    if (дескриптор_файла < 0) mp_raise_OSError(-дескриптор_файла);
    intptr_t ввод_СЧЁТ = 사용자호출(2, дескриптор_файла, (uintptr_t)원본자료, 16384, 0, 0, 0);
    사용자호출(4, дескриптор_файла, 0, 0, 0, 0, 0);
    if (ввод_СЧЁТ < 0) mp_raise_OSError(-ввод_СЧЁТ);
    원본자료[ввод_СЧЁТ] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(файл_ввод_имя, 원본자료, ввод_СЧЁТ, 0);
}
int пользователь_Пуск(int 미사용값) {
    (void)미사용값;
    int ввод_СЧЁТ = 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int 순번 = 0; 순번 < ввод_СЧЁТ; 순번++) 사용자호출(15, 순번, (uintptr_t)전달인수[순번], 256, 0, 0, 0);
    if (ввод_СЧЁТ >= 2 && !strcmp(전달인수[0], "-m") && !strcmp(전달인수[1], "pip")) {
        strcpy(전달인수[0], "/lib/пакет.py");
        for (int 순번 = 1; 순번 < ввод_СЧЁТ - 1; 순번++) strcpy(전달인수[순번], 전달인수[순번 + 1]);
        ввод_СЧЁТ--;
    }
    if (!ввод_СЧЁТ || !strcmp(전달인수[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!ввод_СЧЁТ) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(전달인수[0], "-c") && ввод_СЧЁТ != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(динамическая_память, динамическая_память + sizeof(динамическая_память)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (전달인수[0][0] != '-') {
        const char *끝 = NULL;
        for (const char *позиция_ИНДЕКС = 전달인수[0]; *позиция_ИНДЕКС; позиция_ИНДЕКС++) if (*позиция_ИНДЕКС == '/') 끝 = позиция_ИНДЕКС;
        if (끝) mp_obj_list_append(mp_sys_path, mp_obj_new_str(전달인수[0], 끝 - 전달인수[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int 순번 = 0; 순번 < ввод_СЧЁТ; 순번++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(전달인수[순번], strlen(전달인수[순번])));
    int Состояние_ЗНАЧЕН = 0; nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        mp_lexer_t *낱말해석기 = !strcmp(전달인수[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, 전달인수[1], strlen(전달인수[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(전달인수[0]));
        qstr Название = 낱말해석기->source_name;
        mp_parse_tree_t синтаксис_дерево = mp_parse(낱말해석기, MP_PARSE_FILE_INPUT);
        mp_obj_t 명령열 = mp_compile(&синтаксис_дерево, Название, false);
        mp_call_function_0(명령열);
        nlr_pop();
    } else {
        mp_obj_t исключение = MP_OBJ_FROM_PTR(비지역복귀.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(исключение)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t ЗНАЧЕН = mp_obj_exception_get_value(исключение);
            Состояние_ЗНАЧЕН = ЗНАЧЕН == mp_const_none ? 0 : mp_obj_is_int(ЗНАЧЕН) ? mp_obj_get_int(ЗНАЧЕН) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, исключение); Состояние_ЗНАЧЕН = 1; }
    }
    mp_deinit(); return Состояние_ЗНАЧЕН;
}
