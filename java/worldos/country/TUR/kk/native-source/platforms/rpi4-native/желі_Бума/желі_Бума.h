#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Дайындау_желі(void);
void 통신망살피기(void);
int 통신끝점만들기(int Түрі_Санат);
int 망주소묶기(int файл_дескриптор, uint32_t мекенжай, unsigned порт_нөмірі);
int 연결기다리기(int файл_дескриптор);
void 통신주소재사용(int файл_дескриптор);
int 망연결하기(int файл_дескриптор, uint32_t мекенжай, unsigned порт_нөмірі);
int 망연결받기(int файл_дескриптор);
int 통신읽기(int файл_дескриптор, void *деректер, unsigned 개수);
int 통신쓰기(int файл_дескриптор, const void *деректер, unsigned 개수);
int 전문보내기(int файл_дескриптор, const void *деректер, unsigned 개수, uint32_t мекенжай, unsigned порт_нөмірі);
int 전문받기(int файл_дескриптор, void *деректер, unsigned 개수);
unsigned желі_порт_нөмірі(int файл_дескриптор);
unsigned бір_рангілі_порт_нөмірі(int файл_дескриптор);
uint32_t 상대통신주소(int файл_дескриптор);
void Жабу_желі(int файл_дескриптор);
int файл_тасымалдау_Басқару(int Әрекет);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned енгізу_мән, unsigned индекс);
int конфигурациялау_желі(unsigned Әрекет, uint32_t мекенжай, uint32_t бүркеніш_мән, uint32_t шлюз_мән);
int 응답시험시작(uint32_t мекенжай, unsigned рет_мән);
int 응답시험읽기(unsigned енгізу_мән);
#endif
