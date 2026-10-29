#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Prepara_xarxa(void);
void 통신망살피기(void);
int 통신끝점만들기(int TIPUS_Categoria);
int 망주소묶기(int arxiu_control_7f4cdfd5, uint32_t Adreça, unsigned número_de_port);
int 연결기다리기(int arxiu_control_7f4cdfd5);
void 통신주소재사용(int arxiu_control_7f4cdfd5);
int 망연결하기(int arxiu_control_7f4cdfd5, uint32_t Adreça, unsigned número_de_port);
int 망연결받기(int arxiu_control_7f4cdfd5);
int 통신읽기(int arxiu_control_7f4cdfd5, void *dades, unsigned element_COMPT);
int 통신쓰기(int arxiu_control_7f4cdfd5, const void *dades, unsigned element_COMPT);
int 전문보내기(int arxiu_control_7f4cdfd5, const void *dades, unsigned element_COMPT, uint32_t Adreça, unsigned número_de_port);
int 전문받기(int arxiu_control_7f4cdfd5, void *dades, unsigned element_COMPT);
unsigned xarxa_número_de_port(int arxiu_control_7f4cdfd5);
unsigned homòleg_número_de_port(int arxiu_control_7f4cdfd5);
uint32_t 상대통신주소(int arxiu_control_7f4cdfd5);
void Tanca_xarxa(int arxiu_control_7f4cdfd5);
int transferència_de_fitxers_control(int Acció);
void 파일전송살피기(void);
uint32_t tancar_xarxa_estat(unsigned introducció_VALOR, unsigned INDEX);
int configurar_xarxa(unsigned Acció, uint32_t Adreça, uint32_t màscara_VALOR, uint32_t passarel_la_VALOR);
int 응답시험시작(uint32_t Adreça, unsigned comanda_VALOR);
int 응답시험읽기(unsigned introducció_VALOR);
#endif
