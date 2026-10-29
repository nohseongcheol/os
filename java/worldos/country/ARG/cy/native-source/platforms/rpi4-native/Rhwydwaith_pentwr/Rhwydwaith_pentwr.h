#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Paratoi_Rhwydwaith(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_ardal);
int 망주소묶기(int ffeil_dolen, uint32_t ADDRESS, unsigned rhif_porth);
int 연결기다리기(int ffeil_dolen);
void 통신주소재사용(int ffeil_dolen);
int 망연결하기(int ffeil_dolen, uint32_t ADDRESS, unsigned rhif_porth);
int 망연결받기(int ffeil_dolen);
int 통신읽기(int ffeil_dolen, void *data, unsigned eitem_COUNT);
int 통신쓰기(int ffeil_dolen, const void *data, unsigned eitem_COUNT);
int 전문보내기(int ffeil_dolen, const void *data, unsigned eitem_COUNT, uint32_t ADDRESS, unsigned rhif_porth);
int 전문받기(int ffeil_dolen, void *data, unsigned eitem_COUNT);
unsigned Rhwydwaith_rhif_porth(int ffeil_dolen);
unsigned cymar_rhif_porth(int ffeil_dolen);
uint32_t 상대통신주소(int ffeil_dolen);
void cau_Rhwydwaith(int ffeil_dolen);
int ffeil_trosglwyddo_rheoli(int Gweithrediad);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned cofnod_VALUE, unsigned INDEX);
int ffurfweddu_Rhwydwaith(unsigned Gweithrediad, uint32_t ADDRESS, uint32_t masgio_VALUE, uint32_t adwy_VALUE);
int 응답시험시작(uint32_t ADDRESS, unsigned trefn_VALUE);
int 응답시험읽기(unsigned cofnod_VALUE);
#endif
