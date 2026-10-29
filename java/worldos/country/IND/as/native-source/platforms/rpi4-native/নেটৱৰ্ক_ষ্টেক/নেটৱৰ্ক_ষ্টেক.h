#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void প্ৰস্তুত_কৰক_নেটৱৰ্ক(void);
void 통신망살피기(void);
int 통신끝점만들기(int প্ৰকাৰ_বর্গ);
int 망주소묶기(int ফাইল_হেণ্ডেল, uint32_t ঠিকনা, unsigned 접속번호);
int 연결기다리기(int ফাইল_হেণ্ডেল);
void 통신주소재사용(int ফাইল_হেণ্ডেল);
int 망연결하기(int ফাইল_হেণ্ডেল, uint32_t ঠিকনা, unsigned 접속번호);
int 망연결받기(int ফাইল_হেণ্ডেল);
int 통신읽기(int ফাইল_হেণ্ডেল, void *ডাটা, unsigned 개수);
int 통신쓰기(int ফাইল_হেণ্ডেল, const void *ডাটা, unsigned 개수);
int 전문보내기(int ফাইল_হেণ্ডেল, const void *ডাটা, unsigned 개수, uint32_t ঠিকনা, unsigned 접속번호);
int 전문받기(int ফাইল_হেণ্ডেল, void *ডাটা, unsigned 개수);
unsigned 통신접속번호(int ফাইল_হেণ্ডেল);
unsigned 상대접속번호(int ফাইল_হেণ্ডেল);
uint32_t 상대통신주소(int ফাইল_হেণ্ডেল);
void বন্ধ_কৰক_নেটৱৰ্ক(int ফাইল_হেণ্ডেল);
int ফাইল_স্থানান্তৰণ_নিয়ন্ত্রণ(int কাৰ্য্য);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned প্রবিষ্ট_মান, unsigned ইনডেক্স);
int কনফিগাৰ_কৰক_নেটৱৰ্ক(unsigned কাৰ্য্য, uint32_t ঠিকনা, uint32_t মাস্ক_মান, uint32_t গেটৱে_মান);
int 응답시험시작(uint32_t ঠিকনা, unsigned ক্ৰম_মান);
int 응답시험읽기(unsigned প্রবিষ্ট_মান);
#endif
