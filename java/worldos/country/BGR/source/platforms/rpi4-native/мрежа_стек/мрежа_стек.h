#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Подготвяне_мрежа(void);
void 통신망살피기(void);
int 통신끝점만들기(int Тип_област);
int 망주소묶기(int Файл_манипулатор, uint32_t адрес, unsigned номер_на_порт);
int 연결기다리기(int Файл_манипулатор);
void 통신주소재사용(int Файл_манипулатор);
int 망연결하기(int Файл_манипулатор, uint32_t адрес, unsigned номер_на_порт);
int 망연결받기(int Файл_манипулатор);
int 통신읽기(int Файл_манипулатор, void *данни, unsigned 개수);
int 통신쓰기(int Файл_манипулатор, const void *данни, unsigned 개수);
int изпращам_дейтаграма(int Файл_манипулатор, const void *данни, unsigned 개수, uint32_t адрес, unsigned номер_на_порт);
int получавам_дейтаграма(int Файл_манипулатор, void *данни, unsigned 개수);
unsigned мрежа_номер_на_порт(int Файл_манипулатор);
unsigned крайно_устройство_номер_на_порт(int Файл_манипулатор);
uint32_t 상대통신주소(int Файл_манипулатор);
void затварям_мрежа(int Файл_манипулатор);
int прехвърляне_на_файл_контрол(int Операция);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned запис_стойност, unsigned индекс);
int конфигурирам_мрежа(unsigned Операция, uint32_t адрес, uint32_t маска_стойност, uint32_t шлюз_стойност);
int 응답시험시작(uint32_t адрес, unsigned ред_стойност);
int 응답시험읽기(unsigned запис_стойност);
#endif
