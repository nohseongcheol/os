#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Klargjer_Nettverk(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_kategori);
int 망주소묶기(int fil_handtak, uint32_t ADDRESS, unsigned portnummer);
int 연결기다리기(int fil_handtak);
void 통신주소재사용(int fil_handtak);
int 망연결하기(int fil_handtak, uint32_t ADDRESS, unsigned portnummer);
int 망연결받기(int fil_handtak);
int 통신읽기(int fil_handtak, void *data, unsigned vare_COUNT);
int 통신쓰기(int fil_handtak, const void *data, unsigned vare_COUNT);
int 전문보내기(int fil_handtak, const void *data, unsigned vare_COUNT, uint32_t ADDRESS, unsigned portnummer);
int 전문받기(int fil_handtak, void *data, unsigned vare_COUNT);
unsigned Nettverk_portnummer(int fil_handtak);
unsigned node_portnummer(int fil_handtak);
uint32_t 상대통신주소(int fil_handtak);
void Lukk_Nettverk(int fil_handtak);
int fil_Overfør_styring(int Handling);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned oppføring_VALUE, unsigned INDEX);
int konfigurere_Nettverk(unsigned Handling, uint32_t ADDRESS, uint32_t maske_VALUE, uint32_t gateway_VALUE);
int 응답시험시작(uint32_t ADDRESS, unsigned rekkjefølgje_VALUE);
int 응답시험읽기(unsigned oppføring_VALUE);
#endif
