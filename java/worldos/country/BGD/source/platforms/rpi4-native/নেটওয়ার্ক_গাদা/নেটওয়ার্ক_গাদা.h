#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void প্রস্তুত_করুন_নেটওয়ার্ক(void);
void 통신망살피기(void);
int 통신끝점만들기(int টাইপ_করুন_বিভাগ);
int 망주소묶기(int ফাইল_হাতল, uint32_t ইমেইল, unsigned পোর্ট_নম্বর);
int 연결기다리기(int ফাইল_হাতল);
void 통신주소재사용(int ফাইল_হাতল);
int 망연결하기(int ফাইল_হাতল, uint32_t ইমেইল, unsigned পোর্ট_নম্বর);
int 망연결받기(int ফাইল_হাতল);
int 통신읽기(int ফাইল_হাতল, void *ডাটা, unsigned 개수);
int 통신쓰기(int ফাইল_হাতল, const void *ডাটা, unsigned 개수);
int 전문보내기(int ফাইল_হাতল, const void *ডাটা, unsigned 개수, uint32_t ইমেইল, unsigned পোর্ট_নম্বর);
int 전문받기(int ফাইল_হাতল, void *ডাটা, unsigned 개수);
unsigned নেটওয়ার্ক_পোর্ট_নম্বর(int ফাইল_হাতল);
unsigned পিয়ার_পোর্ট_নম্বর(int ফাইল_হাতল);
uint32_t 상대통신주소(int ফাইল_হাতল);
void বন্ধ_নেটওয়ার্ক(int ফাইল_হাতল);
int ফাইল_স্থানান্তর_নিয়ন্ত্রণ(int কাজ);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ভুক্তি_মান, unsigned সূচি);
int সেট_আপ_করা_নেটওয়ার্ক(unsigned কাজ, uint32_t ইমেইল, uint32_t মাস্ক_মান, uint32_t গেটওয়ে_মান);
int 응답시험시작(uint32_t ইমেইল, unsigned ক্রম_মান);
int 응답시험읽기(unsigned ভুক্তি_মান);
#endif
