#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Parengti_tinklas(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_sritis);
int NET_BIND(int Failas_rodyklė, uint32_t ADDRESS, unsigned prievado_numeris);
int NET_laukti(int Failas_rodyklė);
void 통신주소재사용(int Failas_rodyklė);
int NET_ryšys(int Failas_rodyklė, uint32_t ADDRESS, unsigned prievado_numeris);
int NET_priimti(int Failas_rodyklė);
int 통신읽기(int Failas_rodyklė, void *duomenys, unsigned prekė_COUNT);
int NET_rašymas(int Failas_rodyklė, const void *duomenys, unsigned prekė_COUNT);
int siųsti_paketų_kelio_schema(int Failas_rodyklė, const void *duomenys, unsigned prekė_COUNT, uint32_t ADDRESS, unsigned prievado_numeris);
int gauti_paketų_kelio_schema(int Failas_rodyklė, void *duomenys, unsigned prekė_COUNT);
unsigned tinklas_prievado_numeris(int Failas_rodyklė);
unsigned lygiavertis_mazgas_prievado_numeris(int Failas_rodyklė);
uint32_t NET_lygiavertis_mazgas_ADDRESS(int Failas_rodyklė);
void Uždaryti_tinklas(int Failas_rodyklė);
int failo_perdavimas_valdymas(int Veiksmas);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned įrašas_VALUE, unsigned INDEX);
int konfigūruoti_tinklas(unsigned Veiksmas, uint32_t ADDRESS, uint32_t šablonas_VALUE, uint32_t šliuzas_VALUE);
int 응답시험시작(uint32_t ADDRESS, unsigned tvarka_VALUE);
int 응답시험읽기(unsigned įrašas_VALUE);
#endif
