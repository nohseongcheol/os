#ifndef nativní_síť_Nadpis
#define nativní_síť_Nadpis
#include <stdint.h>
#include <stddef.h>
void Připravit_síť(void);
void 통신망살피기(void);
int Create_soket_účastník(int TYP_oblast);
int čistý_vázat(int popisovač_souboru, uint32_t Adresa, unsigned číslo_portu);
int čistý_naslouchat(int popisovač_souboru);
void 통신주소재사용(int popisovač_souboru);
int čistý_spojit(int popisovač_souboru, uint32_t Adresa, unsigned číslo_portu);
int čistý_přijmout(int popisovač_souboru);
int 통신읽기(int popisovač_souboru, void *data, unsigned zboží_POČET);
int čistý_zápis(int popisovač_souboru, const void *data, unsigned zboží_POČET);
int poslat_datagram(int popisovač_souboru, const void *data, unsigned zboží_POČET, uint32_t Adresa, unsigned číslo_portu);
int dostat_datagram(int popisovač_souboru, void *data, unsigned zboží_POČET);
unsigned síť_číslo_portu(int popisovač_souboru);
unsigned partner_číslo_portu(int popisovač_souboru);
uint32_t čistý_partner_ODKAZ(int popisovač_souboru);
void Zavřít_síť(int popisovač_souboru);
int přenos_souborů_řízení(int Akce);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned položka_HODNOTA, unsigned INDEX);
int konfigurovat_síť(unsigned Akce, uint32_t Adresa, uint32_t maska_HODNOTA, uint32_t brána_HODNOTA);
int START_odpověď_test(uint32_t Adresa, unsigned pořadí_HODNOTA);
int 응답시험읽기(unsigned položka_HODNOTA);
#endif
