#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void तयार_गर्नुहोस्_सञ्जाल(void);
void 통신망살피기(void);
int 통신끝점만들기(int प्रकार_कोटि);
int 망주소묶기(int फाइल_ह्यान्डल, uint32_t ठेगाना, unsigned 접속번호);
int 연결기다리기(int फाइल_ह्यान्डल);
void 통신주소재사용(int फाइल_ह्यान्डल);
int 망연결하기(int फाइल_ह्यान्डल, uint32_t ठेगाना, unsigned 접속번호);
int 망연결받기(int फाइल_ह्यान्डल);
int 통신읽기(int फाइल_ह्यान्डल, void *लगत, unsigned 개수);
int 통신쓰기(int फाइल_ह्यान्डल, const void *लगत, unsigned 개수);
int 전문보내기(int फाइल_ह्यान्डल, const void *लगत, unsigned 개수, uint32_t ठेगाना, unsigned 접속번호);
int 전문받기(int फाइल_ह्यान्डल, void *लगत, unsigned 개수);
unsigned 통신접속번호(int फाइल_ह्यान्डल);
unsigned 상대접속번호(int फाइल_ह्यान्डल);
uint32_t 상대통신주소(int फाइल_ह्यान्डल);
void बन्द_गर्नुहोस्_सञ्जाल(int फाइल_ह्यान्डल);
int फाइल_ट्रान्सफर_नियन्त्रण(int कार्य);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned प्रविष्टि_मान, unsigned अनुक्रमणिका);
int कन्फिगर_गर्नुहोस्_सञ्जाल(unsigned कार्य, uint32_t ठेगाना, uint32_t मकुन्डो_मान, uint32_t गेटवे_मान);
int 응답시험시작(uint32_t ठेगाना, unsigned अर्डर_मान);
int 응답시험읽기(unsigned प्रविष्टि_मान);
#endif
