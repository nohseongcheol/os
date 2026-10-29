#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Ihanda_Network(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_kategorya);
int 망주소묶기(int file_hawakán, uint32_t email, unsigned numero_ng_port);
int 연결기다리기(int file_hawakán);
void 통신주소재사용(int file_hawakán);
int 망연결하기(int file_hawakán, uint32_t email, unsigned numero_ng_port);
int 망연결받기(int file_hawakán);
int 통신읽기(int file_hawakán, void *data, unsigned item_COUNT);
int 통신쓰기(int file_hawakán, const void *data, unsigned item_COUNT);
int 전문보내기(int file_hawakán, const void *data, unsigned item_COUNT, uint32_t email, unsigned numero_ng_port);
int 전문받기(int file_hawakán, void *data, unsigned item_COUNT);
unsigned Network_numero_ng_port(int file_hawakán);
unsigned peer_numero_ng_port(int file_hawakán);
uint32_t 상대통신주소(int file_hawakán);
void isara_Network(int file_hawakán);
int file_lipat_control(int aksyon);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned pagpasok_VALUE, unsigned INDEX);
int magkompigura_Network(unsigned aksyon, uint32_t email, uint32_t mask_VALUE, uint32_t entrada_VALUE);
int 응답시험시작(uint32_t email, unsigned pagkakasunud_sunod_VALUE);
int 응답시험읽기(unsigned pagpasok_VALUE);
#endif
