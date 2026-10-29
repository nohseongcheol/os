#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Ħejji_netwerk(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_kategorija);
int 망주소묶기(int fajl_handle, uint32_t ADDRESS, unsigned 접속번호);
int 연결기다리기(int fajl_handle);
void 통신주소재사용(int fajl_handle);
int 망연결하기(int fajl_handle, uint32_t ADDRESS, unsigned 접속번호);
int 망연결받기(int fajl_handle);
int 통신읽기(int fajl_handle, void *data, unsigned element_COUNT);
int 통신쓰기(int fajl_handle, const void *data, unsigned element_COUNT);
int 전문보내기(int fajl_handle, const void *data, unsigned element_COUNT, uint32_t ADDRESS, unsigned 접속번호);
int 전문받기(int fajl_handle, void *data, unsigned element_COUNT);
unsigned 통신접속번호(int fajl_handle);
unsigned 상대접속번호(int fajl_handle);
uint32_t 상대통신주소(int fajl_handle);
void agħlaq_netwerk(int fajl_handle);
int fajl_trasferiment_kontroll(int azzjoni);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned entrata_VALUE, unsigned INDEX);
int kkonfigura_netwerk(unsigned azzjoni, uint32_t ADDRESS, uint32_t maskra_VALUE, uint32_t gateway_VALUE);
int 응답시험시작(uint32_t ADDRESS, unsigned ordni_VALUE);
int 응답시험읽기(unsigned entrata_VALUE);
#endif
