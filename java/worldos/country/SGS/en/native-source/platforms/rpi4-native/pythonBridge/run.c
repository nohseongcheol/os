#include "../naming/machineLinkNames.h"
#include <string.h>
#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "invoke.h"
static char heapStorage[256 * 1024];
static char originalData[16385];
static char forwardedArgument[8][256];

// JSON이 사용하는 StringIO/BytesIO를 제공한다. 디스크 FileIO는 기존 English API를 쓴다.
static mp_obj_t openFileObject(size_t itemCount, const mp_obj_t *arguments, mp_map_t *selectionValue) {
    (void)itemCount; (void)arguments; (void)selectionValue;
    mp_raise_msg(&mp_type_NotImplementedError, MP_ERROR_TEXT("use jkoros.read/write or Korean file API"));
}
MP_DEFINE_CONST_FUN_OBJ_KW(mp_builtin_open_obj, 1, openFileObject);

mp_uint_t mp_hal_stdout_tx_strn(const char *text, size_t lengthValue) {
    intptr_t result = userInvoke(1, 1, (uintptr_t)text, lengthValue, 0, 0, 0);
    return result < 0 ? 0 : result;
}
void mp_hal_stdout_tx_str(const char *stringData) { mp_hal_stdout_tx_strn(stringData, strlen(stringData)); }
void mp_hal_stdout_tx_strn_cooked(const char *stringData, size_t itemCount) { mp_hal_stdout_tx_strn(stringData, itemCount); }
void nlr_jump_fail(void *value) {
    (void)value;
    mp_hal_stdout_tx_str("MicroPython fatal exception\n");
    userInvoke(6, 1, 0, 0, 0, 0, 0); for (;;) {}
}
void abort(void) { nlr_jump_fail(NULL); }
void gc_collect(void) { gc_collect_start(); gc_helper_collect_regs_and_stack(); gc_collect_end(); }
mp_import_stat_t mp_import_stat(const char *path) {
    intptr_t kindValue = userInvoke(18, (uintptr_t)path, 0, 0, 0, 0, 0);
    return kindValue == 2 ? MP_IMPORT_STAT_DIR : kindValue == 1 ? MP_IMPORT_STAT_FILE : MP_IMPORT_STAT_NO_EXIST;
}
mp_lexer_t *mp_lexer_new_from_file(qstr fileEntryName) {
    intptr_t fileHandle = userInvoke(3, (uintptr_t)qstr_str(fileEntryName), 0, 0, 0, 0, 0);
    if (fileHandle < 0) mp_raise_OSError(-fileHandle);
    intptr_t entryCount = userInvoke(2, fileHandle, (uintptr_t)originalData, 16384, 0, 0, 0);
    userInvoke(4, fileHandle, 0, 0, 0, 0, 0);
    if (entryCount < 0) mp_raise_OSError(-entryCount);
    originalData[entryCount] = 0;
    // Parsing completes before execution/import can reuse this buffer.
    return mp_lexer_new_from_str_len(fileEntryName, originalData, entryCount, 0);
}
int userStart(int unused) {
    (void)unused;
    int entryCount = userInvoke(15, UINTPTR_MAX, 0, 0, 0, 0, 0);
    for (int ordinalIndex = 0; ordinalIndex < entryCount; ordinalIndex++) userInvoke(15, ordinalIndex, (uintptr_t)forwardedArgument[ordinalIndex], 256, 0, 0, 0);
    if (entryCount >= 2 && !strcmp(forwardedArgument[0], "-m") && !strcmp(forwardedArgument[1], "pip")) {
        strcpy(forwardedArgument[0], "/lib/Bundle.py");
        for (int ordinalIndex = 1; ordinalIndex < entryCount - 1; ordinalIndex++) strcpy(forwardedArgument[ordinalIndex], forwardedArgument[ordinalIndex + 1]);
        entryCount--;
    }
    if (!entryCount || !strcmp(forwardedArgument[0], "--version")) {
        mp_hal_stdout_tx_str("MicroPython 1.24.1 / jkoros AArch64 EL0 (not CPython; integer build)\n");
        if (!entryCount) mp_hal_stdout_tx_str("Usage: python FILE.py [ARGS] | python -c 'CODE'\n");
        return 0;
    }
    if (!strcmp(forwardedArgument[0], "-c") && entryCount != 2) {
        mp_hal_stdout_tx_str("Usage: python -c 'CODE'\n"); return 2;
    }
    mp_stack_ctrl_init(); mp_stack_set_limit(48 * 1024);
    gc_init(heapStorage, heapStorage + sizeof(heapStorage)); mp_init();
    mp_obj_list_append(mp_sys_path, mp_obj_new_str("/lib", 4));
    if (forwardedArgument[0][0] != '-') {
        const char *ending = NULL;
        for (const char *positionIndex = forwardedArgument[0]; *positionIndex; positionIndex++) if (*positionIndex == '/') ending = positionIndex;
        if (ending) mp_obj_list_append(mp_sys_path, mp_obj_new_str(forwardedArgument[0], ending - forwardedArgument[0]));
    }
    // argv[0] is script name or -c; subsequent arguments follow it.
    for (int ordinalIndex = 0; ordinalIndex < entryCount; ordinalIndex++) mp_obj_list_append(MP_OBJ_FROM_PTR(&MP_STATE_VM(mp_sys_argv_obj)), mp_obj_new_str(forwardedArgument[ordinalIndex], strlen(forwardedArgument[ordinalIndex])));
    int stateValue = 0; nlr_buf_t nonLocalReturn;
    if (nlr_push(&nonLocalReturn) == 0) {
        mp_lexer_t *Lexer = !strcmp(forwardedArgument[0], "-c")
            ? mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, forwardedArgument[1], strlen(forwardedArgument[1]), 0)
            : mp_lexer_new_from_file(qstr_from_str(forwardedArgument[0]));
        qstr name = Lexer->source_name;
        mp_parse_tree_t SyntaxTree = mp_parse(Lexer, MP_PARSE_FILE_INPUT);
        mp_obj_t instructionSequence = mp_compile(&SyntaxTree, name, false);
        mp_call_function_0(instructionSequence);
        nlr_pop();
    } else {
        mp_obj_t exception = MP_OBJ_FROM_PTR(nonLocalReturn.ret_val);
        if (mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(mp_obj_get_type(exception)), MP_OBJ_FROM_PTR(&mp_type_SystemExit))) {
            mp_obj_t value = mp_obj_exception_get_value(exception);
            stateValue = value == mp_const_none ? 0 : mp_obj_is_int(value) ? mp_obj_get_int(value) : 1;
        } else { mp_obj_print_exception(&mp_plat_print, exception); stateValue = 1; }
    }
    mp_deinit(); return stateValue;
}
