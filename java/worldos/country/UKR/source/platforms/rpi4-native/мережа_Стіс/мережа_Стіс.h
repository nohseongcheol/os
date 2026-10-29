#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Готувати_мережа(void);
void 통신망살피기(void);
int Створення_сокет_учасник(int Тип_область);
int 망주소묶기(int Файл_маркер, uint32_t Адреса, unsigned номер_порту);
int 연결기다리기(int Файл_маркер);
void 통신주소재사용(int Файл_маркер);
int 망연결하기(int Файл_маркер, uint32_t Адреса, unsigned номер_порту);
int 망연결받기(int Файл_маркер);
int 통신읽기(int Файл_маркер, void *дані, unsigned 개수);
int 통신쓰기(int Файл_маркер, const void *дані, unsigned 개수);
int надсилати_дейтаграма(int Файл_маркер, const void *дані, unsigned 개수, uint32_t Адреса, unsigned номер_порту);
int отримувати_дейтаграма(int Файл_маркер, void *дані, unsigned 개수);
unsigned мережа_номер_порту(int Файл_маркер);
unsigned точка_номер_порту(int Файл_маркер);
uint32_t 상대통신주소(int Файл_маркер);
void Закрити_мережа(int Файл_маркер);
int передавання_файлу_керування(int Дія);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned запис_значення_962f286b, unsigned індекс);
int налаштовувати_мережа(unsigned Дія, uint32_t Адреса, uint32_t маска_значення, uint32_t шлюз_значення);
int 응답시험시작(uint32_t Адреса, unsigned порядок_значення);
int 응답시험읽기(unsigned запис_значення_962f286b);
#endif
