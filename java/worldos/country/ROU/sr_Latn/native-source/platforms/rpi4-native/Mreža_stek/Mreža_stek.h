#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Pripremi_Mreža(void);
void 통신망살피기(void);
int 통신끝점만들기(int tip_oblast);
int NET_povezati(int Datoteka_pokazivač, uint32_t adresa, unsigned broj_porta);
int NET_slušati(int Datoteka_pokazivač);
void 통신주소재사용(int Datoteka_pokazivač);
int NET_veze(int Datoteka_pokazivač, uint32_t adresa, unsigned broj_porta);
int NET_prihvatiti(int Datoteka_pokazivač);
int 통신읽기(int Datoteka_pokazivač, void *podaci, unsigned stavka_COUNT);
int 통신쓰기(int Datoteka_pokazivač, const void *podaci, unsigned stavka_COUNT);
int poslati_datagram(int Datoteka_pokazivač, const void *podaci, unsigned stavka_COUNT, uint32_t adresa, unsigned broj_porta);
int primiti_datagram(int Datoteka_pokazivač, void *podaci, unsigned stavka_COUNT);
unsigned Mreža_broj_porta(int Datoteka_pokazivač);
unsigned ravnopravni_uređaj_broj_porta(int Datoteka_pokazivač);
uint32_t NET_ravnopravni_uređaj_adresa(int Datoteka_pokazivač);
void Zatvori_Mreža(int Datoteka_pokazivač);
int prenos_datoteka_kontrola(int radnja);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned stavka_VALUE, unsigned INDEX);
int konfigurisati_Mreža(unsigned radnja, uint32_t adresa, uint32_t maska_VALUE, uint32_t mrežni_prolaz_VALUE);
int 응답시험시작(uint32_t adresa, unsigned poručiti_VALUE);
int 응답시험읽기(unsigned stavka_VALUE);
#endif
