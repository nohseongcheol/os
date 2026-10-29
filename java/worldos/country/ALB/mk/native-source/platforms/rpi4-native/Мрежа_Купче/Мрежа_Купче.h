#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Подготви_Мрежа(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_област);
int 망주소묶기(int датотека_рачка, uint32_t адреса, unsigned број_на_порта);
int 연결기다리기(int датотека_рачка);
void 통신주소재사용(int датотека_рачка);
int 망연결하기(int датотека_рачка, uint32_t адреса, unsigned број_на_порта);
int 망연결받기(int датотека_рачка);
int 통신읽기(int датотека_рачка, void *податоци, unsigned ставка_COUNT);
int 통신쓰기(int датотека_рачка, const void *податоци, unsigned ставка_COUNT);
int 전문보내기(int датотека_рачка, const void *податоци, unsigned ставка_COUNT, uint32_t адреса, unsigned број_на_порта);
int 전문받기(int датотека_рачка, void *податоци, unsigned ставка_COUNT);
unsigned Мрежа_број_на_порта(int датотека_рачка);
unsigned рамноправен_уред_број_на_порта(int датотека_рачка);
uint32_t 상대통신주소(int датотека_рачка);
void затвори_Мрежа(int датотека_рачка);
int датотека_пренос_контрола(int Дејство);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned внес_VALUE, unsigned INDEX);
int конфигурирање_Мрежа(unsigned Дејство, uint32_t адреса, uint32_t маска_VALUE, uint32_t капија_VALUE);
int 응답시험시작(uint32_t адреса, unsigned редослед_VALUE);
int 응답시험읽기(unsigned внес_VALUE);
#endif
