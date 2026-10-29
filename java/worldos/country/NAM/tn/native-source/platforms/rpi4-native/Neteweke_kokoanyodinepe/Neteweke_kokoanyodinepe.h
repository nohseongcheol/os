#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Baakanya_Neteweke(void);
void 통신망살피기(void);
int 통신끝점만들기(int tlanya_setlhopha);
int 망주소묶기(int faele_mokgwakamogelo, uint32_t aterese, unsigned 접속번호);
int 연결기다리기(int faele_mokgwakamogelo);
void 통신주소재사용(int faele_mokgwakamogelo);
int 망연결하기(int faele_mokgwakamogelo, uint32_t aterese, unsigned 접속번호);
int 망연결받기(int faele_mokgwakamogelo);
int 통신읽기(int faele_mokgwakamogelo, void *tshedimosetso, unsigned 개수);
int 통신쓰기(int faele_mokgwakamogelo, const void *tshedimosetso, unsigned 개수);
int 전문보내기(int faele_mokgwakamogelo, const void *tshedimosetso, unsigned 개수, uint32_t aterese, unsigned 접속번호);
int 전문받기(int faele_mokgwakamogelo, void *tshedimosetso, unsigned 개수);
unsigned 통신접속번호(int faele_mokgwakamogelo);
unsigned 상대접속번호(int faele_mokgwakamogelo);
uint32_t 상대통신주소(int faele_mokgwakamogelo);
void tswala_Neteweke(int faele_mokgwakamogelo);
int faele_fudusa_taolo(int tiro);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned tsenyo_Boleng, unsigned tshupane);
int Rulaganya_Neteweke(unsigned tiro, uint32_t aterese, uint32_t mmaseke_Boleng, uint32_t kgorotsamaiso_Boleng);
int 응답시험시작(uint32_t aterese, unsigned thulaganyo_Boleng);
int 응답시험읽기(unsigned tsenyo_Boleng);
#endif
