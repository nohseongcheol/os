#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*инициализатор_метод)(void);
extern инициализатор_метод __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Пуск_пользователь_программа(int);
int пользователь_Пуск(int 전달값) {
    for (инициализатор_метод *данные_позиция = __init_array_start; данные_позиция < __init_array_end; данные_позиция++) (*данные_позиция)();
    int результат = Пуск_пользователь_программа(전달값);
    for (инициализатор_метод *данные_позиция = __fini_array_end; данные_позиция != __fini_array_start;) (*--данные_позиция)();
    return результат;
}
void *memset(void *данные_позиция, int ЗНАЧЕН, size_t ввод_СЧЁТ) { unsigned char *цель_данные = данные_позиция; while (ввод_СЧЁТ--) *цель_данные++ = ЗНАЧЕН; return данные_позиция; }
void *memcpy(void *цель_данные, const void *строка_данные, size_t ввод_СЧЁТ) { unsigned char *첫째값 = цель_данные; const unsigned char *СЕКУНДЫ_ЗНАЧЕН = строка_данные; while (ввод_СЧЁТ--) *첫째값++ = *СЕКУНДЫ_ЗНАЧЕН++; return цель_данные; }
