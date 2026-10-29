#ifndef собственный_шифрование_Заголовок
#define собственный_шифрование_Заголовок
#include <stddef.h>
#include <stdint.h>
void *выделить_удаленный(size_t);
void выпуск_удаленный(void *);
void *원격재할당(void *, size_t);
int удаленный_случайный(unsigned char *, unsigned);
void удаленный_сводка(const void *, size_t, unsigned char [32]);
#endif
