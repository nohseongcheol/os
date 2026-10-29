#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Shirya_Hanyar_sadarwa(void);
void 통신망살피기(void);
int 통신끝점만들기(int rubuta_ɓangare);
int 망주소묶기(int Fayil_Mariki, uint32_t imel, unsigned lambar_kafa);
int 연결기다리기(int Fayil_Mariki);
void 통신주소재사용(int Fayil_Mariki);
int 망연결하기(int Fayil_Mariki, uint32_t imel, unsigned lambar_kafa);
int 망연결받기(int Fayil_Mariki);
int 통신읽기(int Fayil_Mariki, void *Tarin_bayani, unsigned 개수);
int 통신쓰기(int Fayil_Mariki, const void *Tarin_bayani, unsigned 개수);
int 전문보내기(int Fayil_Mariki, const void *Tarin_bayani, unsigned 개수, uint32_t imel, unsigned lambar_kafa);
int 전문받기(int Fayil_Mariki, void *Tarin_bayani, unsigned 개수);
unsigned Hanyar_sadarwa_lambar_kafa(int Fayil_Mariki);
unsigned Fiya_lambar_kafa(int Fayil_Mariki);
uint32_t 상대통신주소(int Fayil_Mariki);
void Rufe_Hanyar_sadarwa(int Fayil_Mariki);
int Fayil_Gusar_da_masarrafa(int Aiki);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned Mashigar_bayanai_Daraja, unsigned Indes);
int hada_kayan_Hanyar_sadarwa(unsigned Aiki, uint32_t imel, uint32_t Burtu_Daraja, uint32_t Mashiga_Daraja);
int 응답시험시작(uint32_t imel, unsigned Hanyar_jejjerawa_Daraja);
int 응답시험읽기(unsigned Mashigar_bayanai_Daraja);
#endif
