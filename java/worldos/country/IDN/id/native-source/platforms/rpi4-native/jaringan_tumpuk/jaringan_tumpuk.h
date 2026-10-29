#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Siapkan_jaringan(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_area);
int 망주소묶기(int file_handel, uint32_t surel, unsigned nomor_port);
int 연결기다리기(int file_handel);
void 통신주소재사용(int file_handel);
int 망연결하기(int file_handel, uint32_t surel, unsigned nomor_port);
int 망연결받기(int file_handel);
int 통신읽기(int file_handel, void *data, unsigned item_COUNT);
int 통신쓰기(int file_handel, const void *data, unsigned item_COUNT);
int 전문보내기(int file_handel, const void *data, unsigned item_COUNT, uint32_t surel, unsigned nomor_port);
int 전문받기(int file_handel, void *data, unsigned item_COUNT);
unsigned jaringan_nomor_port(int file_handel);
unsigned serekan_nomor_port(int file_handel);
uint32_t 상대통신주소(int file_handel);
void Tutup_jaringan(int file_handel);
int transfer_file_kontrol(int Aksi);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned entri_VALUE, unsigned INDEX);
int konfigurasikan_jaringan(unsigned Aksi, uint32_t surel, uint32_t masker_VALUE, uint32_t gateway_VALUE);
int 응답시험시작(uint32_t surel, unsigned urutan_VALUE);
int 응답시험읽기(unsigned entri_VALUE);
#endif
