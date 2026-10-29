#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Pregătiți_rețea(void);
void 통신망살피기(void);
int 통신끝점만들기(int Tip_zonă);
int NET_BIND(int Fișier_handle, uint32_t adresa, unsigned număr_port);
int NET_asculta(int Fișier_handle);
void 통신주소재사용(int Fișier_handle);
int NET_conecta(int Fișier_handle, uint32_t adresa, unsigned număr_port);
int NET_accepta(int Fișier_handle);
int 통신읽기(int Fișier_handle, void *date, unsigned element_COUNT);
int NET_scriere(int Fișier_handle, const void *date, unsigned element_COUNT);
int trimite_diagramă_informații(int Fișier_handle, const void *date, unsigned element_COUNT, uint32_t adresa, unsigned număr_port);
int primi_diagramă_informații(int Fișier_handle, void *date, unsigned element_COUNT);
unsigned rețea_număr_port(int Fișier_handle);
unsigned pereche_număr_port(int Fișier_handle);
uint32_t NET_pereche_adresa(int Fișier_handle);
void închide_rețea(int Fișier_handle);
int transfer_de_fișiere_control(int Acțiuni);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned intrare_VALUE, unsigned INDEX);
int configura_rețea(unsigned Acțiuni, uint32_t adresa, uint32_t mască_VALUE, uint32_t gateway_VALUE);
int 응답시험시작(uint32_t adresa, unsigned ordine_VALUE);
int 응답시험읽기(unsigned intrare_VALUE);
#endif
