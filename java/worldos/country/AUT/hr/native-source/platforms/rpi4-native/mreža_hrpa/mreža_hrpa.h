#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Pripremi_mreža(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_područje);
int NET_BIND(int Datoteka_ustroj, uint32_t adresa, unsigned broj_priključka);
int NET_osluškivati(int Datoteka_ustroj);
void 통신주소재사용(int Datoteka_ustroj);
int NET_CONNECT(int Datoteka_ustroj, uint32_t adresa, unsigned broj_priključka);
int NET_prihvatiti(int Datoteka_ustroj);
int 통신읽기(int Datoteka_ustroj, void *podaci, unsigned artikl_COUNT);
int NET_zapisivanje(int Datoteka_ustroj, const void *podaci, unsigned artikl_COUNT);
int slati_datogram(int Datoteka_ustroj, const void *podaci, unsigned artikl_COUNT, uint32_t adresa, unsigned broj_priključka);
int primiti_datogram(int Datoteka_ustroj, void *podaci, unsigned artikl_COUNT);
unsigned mreža_broj_priključka(int Datoteka_ustroj);
unsigned ravnopravan_član_broj_priključka(int Datoteka_ustroj);
uint32_t NET_ravnopravan_član_adresa(int Datoteka_ustroj);
void Zatvori_mreža(int Datoteka_ustroj);
int prijenos_datoteka_kontrola(int Aktivnost);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned unos_VALUE, unsigned INDEX);
int 망설정하기(unsigned Aktivnost, uint32_t adresa, uint32_t maska_VALUE, uint32_t pristupnik_VALUE);
int 응답시험시작(uint32_t adresa, unsigned narudžba_VALUE);
int 응답시험읽기(unsigned unos_VALUE);
#endif
