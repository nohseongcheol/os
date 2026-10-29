#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void 통신망준비(void);
void 통신망살피기(void);
int 통신끝점만들기(int 유형);
int 망주소묶기(int anaajaalaa_aapaaya, uint32_t ejepüsee, unsigned 접속번호);
int 연결기다리기(int anaajaalaa_aapaaya);
void 통신주소재사용(int anaajaalaa_aapaaya);
int 망연결하기(int anaajaalaa_aapaaya, uint32_t ejepüsee, unsigned 접속번호);
int 망연결받기(int anaajaalaa_aapaaya);
int 통신읽기(int anaajaalaa_aapaaya, void *atijaaya, unsigned 개수);
int 통신쓰기(int anaajaalaa_aapaaya, const void *atijaaya, unsigned 개수);
int 전문보내기(int anaajaalaa_aapaaya, const void *atijaaya, unsigned 개수, uint32_t ejepüsee, unsigned 접속번호);
int 전문받기(int anaajaalaa_aapaaya, void *atijaaya, unsigned 개수);
unsigned 통신접속번호(int anaajaalaa_aapaaya);
unsigned 상대접속번호(int anaajaalaa_aapaaya);
uint32_t 상대통신주소(int anaajaalaa_aapaaya);
void asürülaa_kusu(int anaajaalaa_aapaaya);
int anaajaalaa_alate_eraa_aa_inmajia(int aa_inra_awai);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ekeroliaa_ajutuu, unsigned ee_iyatialujuna);
int anaatiraa_kusu(unsigned aa_inra_awai, uint32_t ejepüsee, uint32_t o_upünaa_utajana_ajutuu, uint32_t miicho_u_a_ttaalee_ajutuu);
int 응답시험시작(uint32_t ejepüsee, unsigned anaajiaakua_ipa_ajutuu);
int 응답시험읽기(unsigned ekeroliaa_ajutuu);
#endif
