#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void 통신망준비(void);
void 통신망살피기(void);
int 통신끝점만들기(int TIPO_Categoría);
int 망주소묶기(int Ficheiro_agarradoira, uint32_t ENDEREZO, unsigned número_do_porto);
int 연결기다리기(int Ficheiro_agarradoira);
void 통신주소재사용(int Ficheiro_agarradoira);
int 망연결하기(int Ficheiro_agarradoira, uint32_t ENDEREZO, unsigned número_do_porto);
int 망연결받기(int Ficheiro_agarradoira);
int 통신읽기(int Ficheiro_agarradoira, void *datos, unsigned elemento_CONTAR);
int 통신쓰기(int Ficheiro_agarradoira, const void *datos, unsigned elemento_CONTAR);
int 전문보내기(int Ficheiro_agarradoira, const void *datos, unsigned elemento_CONTAR, uint32_t ENDEREZO, unsigned número_do_porto);
int 전문받기(int Ficheiro_agarradoira, void *datos, unsigned elemento_CONTAR);
unsigned Rede_número_do_porto(int Ficheiro_agarradoira);
unsigned punto_número_do_porto(int Ficheiro_agarradoira);
uint32_t 상대통신주소(int Ficheiro_agarradoira);
void peche_Rede(int Ficheiro_agarradoira);
int transferencia_de_ficheiros_control(int Acción);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned introdución_VALOR, unsigned ÍNDICE);
int configurar_Rede(unsigned Acción, uint32_t ENDEREZO, uint32_t máscara_VALOR, uint32_t pasarela_VALOR);
int 응답시험시작(uint32_t ENDEREZO, unsigned orde_VALOR);
int 응답시험읽기(unsigned introdución_VALOR);
#endif
