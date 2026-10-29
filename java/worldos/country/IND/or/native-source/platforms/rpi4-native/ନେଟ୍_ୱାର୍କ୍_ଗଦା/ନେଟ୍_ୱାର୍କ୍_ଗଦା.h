#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void ପ୍ରସ୍ତୁତ_ନେଟ୍_ୱାର୍କ୍(void);
void 통신망살피기(void);
int 통신끝점만들기(int ଟାଇପ୍_କରିବା_ବର୍ଗ);
int 망주소묶기(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, uint32_t ଠିକଣା, unsigned ପୋର୍ଟ୍_ନମ୍ଵର୍);
int 연결기다리기(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍);
void 통신주소재사용(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍);
int 망연결하기(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, uint32_t ଠିକଣା, unsigned ପୋର୍ଟ୍_ନମ୍ଵର୍);
int 망연결받기(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍);
int 통신읽기(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, void *ଡାଟା, unsigned 개수);
int 통신쓰기(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, const void *ଡାଟା, unsigned 개수);
int 전문보내기(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, const void *ଡାଟା, unsigned 개수, uint32_t ଠିକଣା, unsigned ପୋର୍ଟ୍_ନମ୍ଵର୍);
int 전문받기(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, void *ଡାଟା, unsigned 개수);
unsigned ନେଟ୍_ୱାର୍କ୍_ପୋର୍ଟ୍_ନମ୍ଵର୍(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍);
unsigned ସମକକ୍ଷ_ପୋର୍ଟ୍_ନମ୍ଵର୍(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍);
uint32_t 상대통신주소(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍);
void ବନ୍ଦ_ନେଟ୍_ୱାର୍କ୍(int ଫାଇଲ୍_ହାଣ୍ଡେଲ୍);
int ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ନିୟନ୍ତ୍ରଣ(int କାମ);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, unsigned ଅନୁକ୍ରମଣିକା);
int ବିନ୍ୟାସ_ନେଟ୍_ୱାର୍କ୍(unsigned କାମ, uint32_t ଠିକଣା, uint32_t ମାସ୍କ_ମୂଲ୍ୟ, uint32_t ପ୍ରବେଶ_ପଥ_ମୂଲ୍ୟ);
int 응답시험시작(uint32_t ଠିକଣା, unsigned କ୍ରମ_ମୂଲ୍ୟ);
int 응답시험읽기(unsigned ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ);
#endif
