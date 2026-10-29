#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Պատրաստել_Ցանց(void);
void 통신망살피기(void);
int 통신끝점만들기(int մուտքագրել_անվանակարգ);
int 망주소묶기(int նիշք_բռնակ, uint32_t հասցե, unsigned 접속번호);
int 연결기다리기(int նիշք_բռնակ);
void 통신주소재사용(int նիշք_բռնակ);
int 망연결하기(int նիշք_բռնակ, uint32_t հասցե, unsigned 접속번호);
int 망연결받기(int նիշք_բռնակ);
int 통신읽기(int նիշք_բռնակ, void *տվյալ, unsigned 개수);
int 통신쓰기(int նիշք_բռնակ, const void *տվյալ, unsigned 개수);
int 전문보내기(int նիշք_բռնակ, const void *տվյալ, unsigned 개수, uint32_t հասցե, unsigned 접속번호);
int 전문받기(int նիշք_բռնակ, void *տվյալ, unsigned 개수);
unsigned 통신접속번호(int նիշք_բռնակ);
unsigned 상대접속번호(int նիշք_բռնակ);
uint32_t 상대통신주소(int նիշք_բռնակ);
void փակել_Ցանց(int նիշք_բռնակ);
int նիշք_փոխանցել_հսկում(int Գործողություն);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned մուտքագրում_արժեք, unsigned դասիչ);
int կազմաձեւել_Ցանց(unsigned Գործողություն, uint32_t հասցե, uint32_t դիմակ_արժեք, uint32_t անցուղի_արժեք);
int 응답시험시작(uint32_t հասցե, unsigned կարգ_արժեք);
int 응답시험읽기(unsigned մուտքագրում_արժեք);
#endif
