#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Pripraviť_sieť(void);
void 통신망살피기(void);
int Create_soket_účastník(int Typ_oblasť);
int NET_BIND(int Súbor_rukoväť, uint32_t adresa, unsigned číslo_portu);
int NET_načúvať(int Súbor_rukoväť);
void 통신주소재사용(int Súbor_rukoväť);
int NET_spojiť(int Súbor_rukoväť, uint32_t adresa, unsigned číslo_portu);
int NET_prijať(int Súbor_rukoväť);
int 통신읽기(int Súbor_rukoväť, void *údaje, unsigned položka_COUNT);
int NET_zapísať(int Súbor_rukoväť, const void *údaje, unsigned položka_COUNT);
int odoslať_datagram(int Súbor_rukoväť, const void *údaje, unsigned položka_COUNT, uint32_t adresa, unsigned číslo_portu);
int dostať_datagram(int Súbor_rukoväť, void *údaje, unsigned položka_COUNT);
unsigned sieť_číslo_portu(int Súbor_rukoväť);
unsigned partnerský_uzol_číslo_portu(int Súbor_rukoväť);
uint32_t NET_partnerský_uzol_adresa(int Súbor_rukoväť);
void Zavrieť_sieť(int Súbor_rukoväť);
int prenos_súborov_riadenie(int Akcia);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned položka_VALUE, unsigned INDEX);
int konfigurovať_sieť(unsigned Akcia, uint32_t adresa, uint32_t maska_VALUE, uint32_t brána_VALUE);
int START_odpoveď_test(uint32_t adresa, unsigned poradie_VALUE);
int 응답시험읽기(unsigned položka_VALUE);
#endif
