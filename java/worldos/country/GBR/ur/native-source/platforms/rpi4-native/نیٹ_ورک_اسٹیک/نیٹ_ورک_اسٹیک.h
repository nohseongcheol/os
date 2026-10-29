#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void تیار_کریں_نیٹ_ورک(void);
void 통신망살피기(void);
int 통신끝점만들기(int ٹائپ_کریں_زمرہ);
int 망주소묶기(int فائل_ہینڈل, uint32_t پتہ, unsigned دہانہ_نمبر);
int 연결기다리기(int فائل_ہینڈل);
void 통신주소재사용(int فائل_ہینڈل);
int 망연결하기(int فائل_ہینڈل, uint32_t پتہ, unsigned دہانہ_نمبر);
int 망연결받기(int فائل_ہینڈل);
int 통신읽기(int فائل_ہینڈل, void *کوائف, unsigned 개수);
int 통신쓰기(int فائل_ہینڈل, const void *کوائف, unsigned 개수);
int 전문보내기(int فائل_ہینڈل, const void *کوائف, unsigned 개수, uint32_t پتہ, unsigned دہانہ_نمبر);
int 전문받기(int فائل_ہینڈل, void *کوائف, unsigned 개수);
unsigned نیٹ_ورک_دہانہ_نمبر(int فائل_ہینڈل);
unsigned ساتھی_دہانہ_نمبر(int فائل_ہینڈل);
uint32_t 상대통신주소(int فائل_ہینڈل);
void بند_نیٹ_ورک(int فائل_ہینڈل);
int فائل_منتقلی_کنٹرول(int عمل);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned اندراج_قدر, unsigned اشاریہ);
int تشکیل_کریں_نیٹ_ورک(unsigned عمل, uint32_t پتہ, uint32_t ماسک_پہنائیں_قدر, uint32_t گیٹ_وے_قدر);
int 응답시험시작(uint32_t پتہ, unsigned ترتیم_قدر);
int 응답시험읽기(unsigned اندراج_قدر);
#endif
