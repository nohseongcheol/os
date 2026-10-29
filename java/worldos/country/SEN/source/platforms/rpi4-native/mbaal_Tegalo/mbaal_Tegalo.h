#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void jël_matuwaay_mbaal(void);
void 통신망살피기(void);
int 통신끝점만들기(int xeet_ngiir);
int 망주소묶기(int bara_denc_yombal, uint32_t dëkkuwaay, unsigned 접속번호);
int 연결기다리기(int bara_denc_yombal);
void 통신주소재사용(int bara_denc_yombal);
int 망연결하기(int bara_denc_yombal, uint32_t dëkkuwaay, unsigned 접속번호);
int 망연결받기(int bara_denc_yombal);
int 통신읽기(int bara_denc_yombal, void *mbir, unsigned 개수);
int 통신쓰기(int bara_denc_yombal, const void *mbir, unsigned 개수);
int 전문보내기(int bara_denc_yombal, const void *mbir, unsigned 개수, uint32_t dëkkuwaay, unsigned 접속번호);
int 전문받기(int bara_denc_yombal, void *mbir, unsigned 개수);
unsigned 통신접속번호(int bara_denc_yombal);
unsigned 상대접속번호(int bara_denc_yombal);
uint32_t 상대통신주소(int bara_denc_yombal);
void Tej_mbaal(int bara_denc_yombal);
int bara_denc_toxal_Saytu_doxinu_ordinateur(int jëf);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned dugal_xabaar_xëyma, unsigned àlluwa_tur);
int Jokkale_ak_ab_ordinateur_mbaal(unsigned jëf, uint32_t dëkkuwaay, uint32_t muuraay_xëyma, uint32_t bunt_xëyma);
int 응답시험시작(uint32_t dëkkuwaay, unsigned toftale_xëyma);
int 응답시험읽기(unsigned dugal_xabaar_xëyma);
#endif
