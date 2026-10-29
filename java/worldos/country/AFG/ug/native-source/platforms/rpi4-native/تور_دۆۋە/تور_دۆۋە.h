#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void تەييارلىماق_تور(void);
void 통신망살피기(void);
int 통신끝점만들기(int تىپ_تۈر);
int 망주소묶기(int ھۆججەت_تۇتقۇچ, uint32_t ئادرېس, unsigned 접속번호);
int 연결기다리기(int ھۆججەت_تۇتقۇچ);
void 통신주소재사용(int ھۆججەت_تۇتقۇچ);
int 망연결하기(int ھۆججەت_تۇتقۇچ, uint32_t ئادرېس, unsigned 접속번호);
int 망연결받기(int ھۆججەت_تۇتقۇچ);
int 통신읽기(int ھۆججەت_تۇتقۇچ, void *مەلۇمات, unsigned 개수);
int 통신쓰기(int ھۆججەت_تۇتقۇچ, const void *مەلۇمات, unsigned 개수);
int 전문보내기(int ھۆججەت_تۇتقۇچ, const void *مەلۇمات, unsigned 개수, uint32_t ئادرېس, unsigned 접속번호);
int 전문받기(int ھۆججەت_تۇتقۇچ, void *مەلۇمات, unsigned 개수);
unsigned 통신접속번호(int ھۆججەت_تۇتقۇچ);
unsigned 상대접속번호(int ھۆججەت_تۇتقۇچ);
uint32_t 상대통신주소(int ھۆججەت_تۇتقۇچ);
void ئاياغ_تور(int ھۆججەت_تۇتقۇچ);
int ھۆججەت_يوللاش_كونترول(int مەشغۇلات);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned كىرگۈزۈش_قىممىتى, unsigned ئىندېكس);
int سەپلىمەك_تور(unsigned مەشغۇلات, uint32_t ئادرېس, uint32_t 가림, uint32_t 관문);
int 응답시험시작(uint32_t ئادرېس, unsigned تەرتىپ_قىممىتى);
int 응답시험읽기(unsigned كىرگۈزۈش_قىممىتى);
#endif
