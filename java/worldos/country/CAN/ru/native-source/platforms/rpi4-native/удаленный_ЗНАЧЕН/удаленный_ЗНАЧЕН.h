#ifndef собственный_удаленное_подключение_Заголовок
#define собственный_удаленное_подключение_Заголовок
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Подготовить_удаленный(void);
void 원격살피기(void);
void удаленный_выход(unsigned char);
int удаленный_входные_данные(void);
int канал_удаленный_входные_данные(const unsigned char *,unsigned);
uintptr_t Доска_удаленное_управление(uintptr_t,uintptr_t);
uintptr_t 보드원격명령끝(uintptr_t);
uintptr_t Доска_удаленный_минутку(uintptr_t);
void 원격화면살피기(void);
int управление_удаленный_дисплей(unsigned);
#endif
