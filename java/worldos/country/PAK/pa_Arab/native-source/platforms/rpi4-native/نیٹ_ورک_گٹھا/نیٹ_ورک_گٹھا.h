#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void تیاری_کرو_نیٹ_ورک(void);
void 통신망살피기(void);
int 통신끝점만들기(int ٹائپ_کرو_زمرہ);
int 망주소묶기(int فائل_نبٹنا, uint32_t پتا, unsigned 접속번호);
int 연결기다리기(int فائل_نبٹنا);
void 통신주소재사용(int فائل_نبٹنا);
int 망연결하기(int فائل_نبٹنا, uint32_t پتا, unsigned 접속번호);
int 망연결받기(int فائل_نبٹنا);
int 통신읽기(int فائل_نبٹنا, void *کوائف, unsigned 개수);
int 통신쓰기(int فائل_نبٹنا, const void *کوائف, unsigned 개수);
int 전문보내기(int فائل_نبٹنا, const void *کوائف, unsigned 개수, uint32_t پتا, unsigned 접속번호);
int 전문받기(int فائل_نبٹنا, void *کوائف, unsigned 개수);
unsigned 통신접속번호(int فائل_نبٹنا);
unsigned 상대접속번호(int فائل_نبٹنا);
uint32_t 상대통신주소(int فائل_نبٹنا);
void بند_کرو_نیٹ_ورک(int فائل_نبٹنا);
int فائل_منتقلی_کنٹرول(int کم);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned داخلہ_قدر, unsigned اشاریہ);
int تشکیل_دو_نیٹ_ورک(unsigned کم, uint32_t پتا, uint32_t 가림, uint32_t 관문);
int 응답시험시작(uint32_t پتا, unsigned ترتیب_قدر);
int 응답시험읽기(unsigned داخلہ_قدر);
#endif
