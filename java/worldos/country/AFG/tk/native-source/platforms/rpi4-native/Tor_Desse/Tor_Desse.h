#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Taýýarla_Tor(void);
void 통신망살피기(void);
int 통신끝점만들기(int ýaz_kategoriýa);
int 망주소묶기(int faýl_ryçag, uint32_t salgy, unsigned 접속번호);
int 연결기다리기(int faýl_ryçag);
void 통신주소재사용(int faýl_ryçag);
int 망연결하기(int faýl_ryçag, uint32_t salgy, unsigned 접속번호);
int 망연결받기(int faýl_ryçag);
int 통신읽기(int faýl_ryçag, void *maglumat, unsigned 개수);
int 통신쓰기(int faýl_ryçag, const void *maglumat, unsigned 개수);
int 전문보내기(int faýl_ryçag, const void *maglumat, unsigned 개수, uint32_t salgy, unsigned 접속번호);
int 전문받기(int faýl_ryçag, void *maglumat, unsigned 개수);
unsigned 통신접속번호(int faýl_ryçag);
unsigned 상대접속번호(int faýl_ryçag);
uint32_t 상대통신주소(int faýl_ryçag);
void ýap_Tor(int faýl_ryçag);
int faýl_geçir_dolandyryş(int iş);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned girizmeklik_baha, unsigned indeks);
int düz_Tor(unsigned iş, uint32_t salgy, uint32_t örtük_baha, uint32_t şlýuz_baha);
int 응답시험시작(uint32_t salgy, unsigned tertip_baha);
int 응답시험읽기(unsigned girizmeklik_baha);
#endif
