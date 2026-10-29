#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void தயார்படுத்த_பிணையம்(void);
void 통신망살피기(void);
int 통신끝점만들기(int வகை_வகை);
int 망주소묶기(int கோப்பு_நடத்தி, uint32_t முகவரி, unsigned முனைய_எண்);
int 연결기다리기(int கோப்பு_நடத்தி);
void 통신주소재사용(int கோப்பு_நடத்தி);
int 망연결하기(int கோப்பு_நடத்தி, uint32_t முகவரி, unsigned முனைய_எண்);
int 망연결받기(int கோப்பு_நடத்தி);
int 통신읽기(int கோப்பு_நடத்தி, void *தரவு, unsigned 개수);
int 통신쓰기(int கோப்பு_நடத்தி, const void *தரவு, unsigned 개수);
int 전문보내기(int கோப்பு_நடத்தி, const void *தரவு, unsigned 개수, uint32_t முகவரி, unsigned முனைய_எண்);
int 전문받기(int கோப்பு_நடத்தி, void *தரவு, unsigned 개수);
unsigned பிணையம்_முனைய_எண்(int கோப்பு_நடத்தி);
unsigned பியர்_முனைய_எண்(int கோப்பு_நடத்தி);
uint32_t 상대통신주소(int கோப்பு_நடத்தி);
void மூடு_பிணையம்(int கோப்பு_நடத்தி);
int கோப்பு_இடமாற்று_கட்டுப்பாடு(int செயல்);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned உள்ளீடு_மதிப்பு, unsigned அடைவு);
int உள்ளமை_பிணையம்(unsigned செயல், uint32_t முகவரி, uint32_t முகமூடி_மதிப்பு, uint32_t நுழைவாயில்_மதிப்பு);
int 응답시험시작(uint32_t முகவரி, unsigned வரிசை_மதிப்பு);
int 응답시험읽기(unsigned உள்ளீடு_மதிப்பு);
#endif
