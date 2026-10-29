#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Pripremiti_Mreža(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_oblast);
int 망주소묶기(int fajl_hvatište, uint32_t adresa, unsigned broj_priključka);
int 연결기다리기(int fajl_hvatište);
void 통신주소재사용(int fajl_hvatište);
int 망연결하기(int fajl_hvatište, uint32_t adresa, unsigned broj_priključka);
int 망연결받기(int fajl_hvatište);
int 통신읽기(int fajl_hvatište, void *podaci, unsigned stavka_COUNT);
int 통신쓰기(int fajl_hvatište, const void *podaci, unsigned stavka_COUNT);
int 전문보내기(int fajl_hvatište, const void *podaci, unsigned stavka_COUNT, uint32_t adresa, unsigned broj_priključka);
int 전문받기(int fajl_hvatište, void *podaci, unsigned stavka_COUNT);
unsigned Mreža_broj_priključka(int fajl_hvatište);
unsigned peer_broj_priključka(int fajl_hvatište);
uint32_t 상대통신주소(int fajl_hvatište);
void zatvoriti_Mreža(int fajl_hvatište);
int fajl_prijenos_kontrola(int radnja);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned unos_VALUE, unsigned INDEX);
int konfigurirati_Mreža(unsigned radnja, uint32_t adresa, uint32_t maska_VALUE, uint32_t pristupni_uređaj_VALUE);
int 응답시험시작(uint32_t adresa, unsigned redoslijed_VALUE);
int 응답시험읽기(unsigned unos_VALUE);
#endif
