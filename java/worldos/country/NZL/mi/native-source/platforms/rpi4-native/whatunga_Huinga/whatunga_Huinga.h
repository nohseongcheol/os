#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Whakarite_whatunga(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_kāwai);
int 망주소묶기(int kōnae_raweke, uint32_t ADDRESS, unsigned 접속번호);
int 연결기다리기(int kōnae_raweke);
void 통신주소재사용(int kōnae_raweke);
int 망연결하기(int kōnae_raweke, uint32_t ADDRESS, unsigned 접속번호);
int 망연결받기(int kōnae_raweke);
int 통신읽기(int kōnae_raweke, void *raraunga, unsigned tuemi_COUNT);
int 통신쓰기(int kōnae_raweke, const void *raraunga, unsigned tuemi_COUNT);
int 전문보내기(int kōnae_raweke, const void *raraunga, unsigned tuemi_COUNT, uint32_t ADDRESS, unsigned 접속번호);
int 전문받기(int kōnae_raweke, void *raraunga, unsigned tuemi_COUNT);
unsigned 통신접속번호(int kōnae_raweke);
unsigned 상대접속번호(int kōnae_raweke);
uint32_t 상대통신주소(int kōnae_raweke);
void kati_whatunga(int kōnae_raweke);
int kōnae_whakawhiti_mana(int hohenga);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned tāurunga_uara, unsigned INDEX);
int whirihora_whatunga(unsigned hohenga, uint32_t ADDRESS, uint32_t hīpoki_uara, uint32_t waharoa_uara);
int 응답시험시작(uint32_t ADDRESS, unsigned whakaraupapa_uara);
int 응답시험읽기(unsigned tāurunga_uara);
#endif
