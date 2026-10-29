#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void آماده_کردن_شبکه(void);
void 통신망살피기(void);
int 통신끝점만들기(int تایپ_کردن_دسته);
int 망주소묶기(int فایل_دستگیره, uint32_t آدرس, unsigned شماره_درگاه);
int 연결기다리기(int فایل_دستگیره);
void 통신주소재사용(int فایل_دستگیره);
int 망연결하기(int فایل_دستگیره, uint32_t آدرس, unsigned شماره_درگاه);
int 망연결받기(int فایل_دستگیره);
int 통신읽기(int فایل_دستگیره, void *داده_ها, unsigned 개수);
int 통신쓰기(int فایل_دستگیره, const void *داده_ها, unsigned 개수);
int 전문보내기(int فایل_دستگیره, const void *داده_ها, unsigned 개수, uint32_t آدرس, unsigned شماره_درگاه);
int 전문받기(int فایل_دستگیره, void *داده_ها, unsigned 개수);
unsigned شبکه_شماره_درگاه(int فایل_دستگیره);
unsigned مشابه_شماره_درگاه(int فایل_دستگیره);
uint32_t 상대통신주소(int فایل_دستگیره);
void بستن_شبکه(int فایل_دستگیره);
int فایل_انتقال_کنترل(int کنش);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ورودی_مقدار, unsigned فهرست);
int پیکربندی_کردن_شبکه(unsigned کنش, uint32_t آدرس, uint32_t ماسک_مقدار, uint32_t دروازه_مقدار);
int 응답시험시작(uint32_t آدرس, unsigned ترتیب_مقدار);
int 응답시험읽기(unsigned ورودی_مقدار);
#endif
