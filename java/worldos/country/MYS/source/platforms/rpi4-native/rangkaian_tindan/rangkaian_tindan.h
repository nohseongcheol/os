#ifndef asal_rangkaian_Pengepala
#define asal_rangkaian_Pengepala
#include <stdint.h>
#include <stddef.h>
void Sediakan_rangkaian(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_bidang);
int 망주소묶기(int fail_pemegang, uint32_t e_mel, unsigned nombor_port);
int 연결기다리기(int fail_pemegang);
void 통신주소재사용(int fail_pemegang);
int 망연결하기(int fail_pemegang, uint32_t e_mel, unsigned nombor_port);
int 망연결받기(int fail_pemegang);
int 통신읽기(int fail_pemegang, void *data, unsigned item_COUNT);
int 통신쓰기(int fail_pemegang, const void *data, unsigned item_COUNT);
int 전문보내기(int fail_pemegang, const void *data, unsigned item_COUNT, uint32_t e_mel, unsigned nombor_port);
int 전문받기(int fail_pemegang, void *data, unsigned item_COUNT);
unsigned rangkaian_nombor_port(int fail_pemegang);
unsigned rakan_nombor_port(int fail_pemegang);
uint32_t 상대통신주소(int fail_pemegang);
void Tutup_rangkaian(int fail_pemegang);
int pemindahan_fail_kawalan(int Aksi);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned pemasukan_VALUE, unsigned INDEX);
int konfigurasi_rangkaian(unsigned Aksi, uint32_t e_mel, uint32_t topeng_VALUE, uint32_t get_laluan_VALUE);
int Mula_respons_ujian(uint32_t e_mel, unsigned tertib_VALUE);
int 응답시험읽기(unsigned pemasukan_VALUE);
#endif
