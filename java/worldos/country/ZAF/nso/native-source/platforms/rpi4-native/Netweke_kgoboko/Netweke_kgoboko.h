#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Lokišetša_Netweke(void);
void 통신망살피기(void);
int 통신끝점만들기(int thaepa_legoro);
int 망주소묶기(int faele_tshwaro, uint32_t atrese, unsigned 접속번호);
int 연결기다리기(int faele_tshwaro);
void 통신주소재사용(int faele_tshwaro);
int 망연결하기(int faele_tshwaro, uint32_t atrese, unsigned 접속번호);
int 망연결받기(int faele_tshwaro);
int 통신읽기(int faele_tshwaro, void *data, unsigned 개수);
int 통신쓰기(int faele_tshwaro, const void *data, unsigned 개수);
int 전문보내기(int faele_tshwaro, const void *data, unsigned 개수, uint32_t atrese, unsigned 접속번호);
int 전문받기(int faele_tshwaro, void *data, unsigned 개수);
unsigned 통신접속번호(int faele_tshwaro);
unsigned 상대접속번호(int faele_tshwaro);
uint32_t 상대통신주소(int faele_tshwaro);
void tswalela_Netweke(int faele_tshwaro);
int faele_fetišetša_taolo(int Mogato);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned go_tsenya_tshedimošo_boleng, unsigned lokela);
int lomaganya_Netweke(unsigned Mogato, uint32_t atrese, uint32_t maseke_boleng, uint32_t tsela_ya_netweke_boleng);
int 응답시험시작(uint32_t atrese, unsigned thulaganyo_boleng);
int 응답시험읽기(unsigned go_tsenya_tshedimošo_boleng);
#endif
