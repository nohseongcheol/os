#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Hazırla_Şəbəkə(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_sahə);
int 망주소묶기(int fayl_tutacaq, uint32_t ünvan, unsigned 접속번호);
int 연결기다리기(int fayl_tutacaq);
void 통신주소재사용(int fayl_tutacaq);
int 망연결하기(int fayl_tutacaq, uint32_t ünvan, unsigned 접속번호);
int 망연결받기(int fayl_tutacaq);
int 통신읽기(int fayl_tutacaq, void *verilənlər, unsigned element_COUNT);
int 통신쓰기(int fayl_tutacaq, const void *verilənlər, unsigned element_COUNT);
int 전문보내기(int fayl_tutacaq, const void *verilənlər, unsigned element_COUNT, uint32_t ünvan, unsigned 접속번호);
int 전문받기(int fayl_tutacaq, void *verilənlər, unsigned element_COUNT);
unsigned 통신접속번호(int fayl_tutacaq);
unsigned 상대접속번호(int fayl_tutacaq);
uint32_t 상대통신주소(int fayl_tutacaq);
void bağlamaq_Şəbəkə(int fayl_tutacaq);
int fayl_ötürmə_nəzarət(int Gedişat);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned daxiletmə_VALUE, unsigned INDEX);
int konfiqurasiya_etmək_Şəbəkə(unsigned Gedişat, uint32_t ünvan, uint32_t maska_VALUE, uint32_t şlüz_VALUE);
int 응답시험시작(uint32_t ünvan, unsigned ardıcıllıq_VALUE);
int 응답시험읽기(unsigned daxiletmə_VALUE);
#endif
