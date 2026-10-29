#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Ettevalmistamine_võrk(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_ala);
int NET_BIND(int Fail_pide, uint32_t ADDRESS, unsigned pordinumber);
int NET_jälgima(int Fail_pide);
void 통신주소재사용(int Fail_pide);
int NET_Ühenda(int Fail_pide, uint32_t ADDRESS, unsigned pordinumber);
int NET_aktsepteerima(int Fail_pide);
int 통신읽기(int Fail_pide, void *andmed, unsigned kaup_COUNT);
int NET_kirjutamine(int Fail_pide, const void *andmed, unsigned kaup_COUNT);
int saatma_datagramm(int Fail_pide, const void *andmed, unsigned kaup_COUNT, uint32_t ADDRESS, unsigned pordinumber);
int saama_datagramm(int Fail_pide, void *andmed, unsigned kaup_COUNT);
unsigned võrk_pordinumber(int Fail_pide);
unsigned partner_pordinumber(int Fail_pide);
uint32_t NET_partner_ADDRESS(int Fail_pide);
void Sule_võrk(int Fail_pide);
int failiedastus_meede(int Nimi);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned kirje_VALUE, unsigned INDEX);
int konfigureerima_võrk(unsigned Nimi, uint32_t ADDRESS, uint32_t mask_VALUE, uint32_t lüüs_VALUE);
int 응답시험시작(uint32_t ADDRESS, unsigned tellimus_VALUE);
int 응답시험읽기(unsigned kirje_VALUE);
#endif
