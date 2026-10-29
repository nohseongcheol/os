#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Përgatit_rrjet(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_kategori);
int 망주소묶기(int skedar_dorezë, uint32_t email, unsigned numri_i_portës);
int 연결기다리기(int skedar_dorezë);
void 통신주소재사용(int skedar_dorezë);
int 망연결하기(int skedar_dorezë, uint32_t email, unsigned numri_i_portës);
int 망연결받기(int skedar_dorezë);
int 통신읽기(int skedar_dorezë, void *të_dhëna, unsigned njësi_COUNT);
int 통신쓰기(int skedar_dorezë, const void *të_dhëna, unsigned njësi_COUNT);
int 전문보내기(int skedar_dorezë, const void *të_dhëna, unsigned njësi_COUNT, uint32_t email, unsigned numri_i_portës);
int 전문받기(int skedar_dorezë, void *të_dhëna, unsigned njësi_COUNT);
unsigned rrjet_numri_i_portës(int skedar_dorezë);
unsigned homolog_numri_i_portës(int skedar_dorezë);
uint32_t 상대통신주소(int skedar_dorezë);
void mbyll_rrjet(int skedar_dorezë);
int skedar_transferim_kontroll(int Veprim);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned futje_VALUE, unsigned INDEX);
int konfiguroj_rrjet(unsigned Veprim, uint32_t email, uint32_t maskë_VALUE, uint32_t portëkalimi_VALUE);
int 응답시험시작(uint32_t email, unsigned renditja_VALUE);
int 응답시험읽기(unsigned futje_VALUE);
#endif
