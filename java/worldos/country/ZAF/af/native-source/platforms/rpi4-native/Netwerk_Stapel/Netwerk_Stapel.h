#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Maak_gereed_Netwerk(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_kategorie);
int 망주소묶기(int lêer_handvatsel, uint32_t adres, unsigned 접속번호);
int 연결기다리기(int lêer_handvatsel);
void 통신주소재사용(int lêer_handvatsel);
int 망연결하기(int lêer_handvatsel, uint32_t adres, unsigned 접속번호);
int 망연결받기(int lêer_handvatsel);
int 통신읽기(int lêer_handvatsel, void *data, unsigned item_COUNT);
int 통신쓰기(int lêer_handvatsel, const void *data, unsigned item_COUNT);
int 전문보내기(int lêer_handvatsel, const void *data, unsigned item_COUNT, uint32_t adres, unsigned 접속번호);
int 전문받기(int lêer_handvatsel, void *data, unsigned item_COUNT);
unsigned 통신접속번호(int lêer_handvatsel);
unsigned 상대접속번호(int lêer_handvatsel);
uint32_t 상대통신주소(int lêer_handvatsel);
void sluit_Netwerk(int lêer_handvatsel);
int lêer_oordra_kontrole(int Aksie);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned inskrywing_VALUE, unsigned INDEX);
int konfigureer_Netwerk(unsigned Aksie, uint32_t adres, uint32_t masker_VALUE, uint32_t deurgang_VALUE);
int 응답시험시작(uint32_t adres, unsigned volgorde_VALUE);
int 응답시험읽기(unsigned inskrywing_VALUE);
#endif
