#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Ullmhaigh_Líonra(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_catagóir);
int 망주소묶기(int comhad_hanla, uint32_t ADDRESS, unsigned uimhir_phoirt);
int 연결기다리기(int comhad_hanla);
void 통신주소재사용(int comhad_hanla);
int 망연결하기(int comhad_hanla, uint32_t ADDRESS, unsigned uimhir_phoirt);
int 망연결받기(int comhad_hanla);
int 통신읽기(int comhad_hanla, void *sonraí, unsigned mír_COUNT);
int 통신쓰기(int comhad_hanla, const void *sonraí, unsigned mír_COUNT);
int 전문보내기(int comhad_hanla, const void *sonraí, unsigned mír_COUNT, uint32_t ADDRESS, unsigned uimhir_phoirt);
int 전문받기(int comhad_hanla, void *sonraí, unsigned mír_COUNT);
unsigned Líonra_uimhir_phoirt(int comhad_hanla);
unsigned piara_uimhir_phoirt(int comhad_hanla);
uint32_t 상대통신주소(int comhad_hanla);
void dún_Líonra(int comhad_hanla);
int comhad_traschur_rialú(int Gníomh);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned iontráil_VALUE, unsigned INDEX);
int cumraigh_Líonra(unsigned Gníomh, uint32_t ADDRESS, uint32_t masc_VALUE, uint32_t geata_VALUE);
int 응답시험시작(uint32_t ADDRESS, unsigned ord_VALUE);
int 응답시험읽기(unsigned iontráil_VALUE);
#endif
