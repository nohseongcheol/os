#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Pripravi_mreža(void);
void 통신망살피기(void);
int Ustvari_vtičnica_končna_točka(int Tip_območje);
int NET_BIND(int Datoteka_ročica, uint32_t naslov, unsigned številka_vrat);
int NET_poslušati(int Datoteka_ročica);
void 통신주소재사용(int Datoteka_ročica);
int NET_POVEŽI(int Datoteka_ročica, uint32_t naslov, unsigned številka_vrat);
int NET_sprejeti(int Datoteka_ročica);
int 통신읽기(int Datoteka_ročica, void *podatki, unsigned element_COUNT);
int NET_pisati(int Datoteka_ročica, const void *podatki, unsigned element_COUNT);
int poslati_datagram(int Datoteka_ročica, const void *podatki, unsigned element_COUNT, uint32_t naslov, unsigned številka_vrat);
int sprejeti_sprejemati_prejeti_prejemati_datagram(int Datoteka_ročica, void *podatki, unsigned element_COUNT);
unsigned mreža_številka_vrat(int Datoteka_ročica);
unsigned enakovreden_številka_vrat(int Datoteka_ročica);
uint32_t NET_enakovreden_naslov(int Datoteka_ročica);
void Zapri_mreža(int Datoteka_ročica);
int prenos_datotek_nadzor(int Dejanje);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned vnos_VALUE, unsigned INDEX);
int konfigurirati_mreža(unsigned Dejanje, uint32_t naslov, uint32_t maska_VALUE, uint32_t prehod_VALUE);
int Start_odziv_preskusiti(uint32_t naslov, unsigned naročilo_VALUE);
int 응답시험읽기(unsigned vnos_VALUE);
#endif
