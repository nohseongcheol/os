#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void ᎭᏛᏅᎢᏍᏓ_ᏧᎾᏚᏓᎵ(void);
void 통신망살피기(void);
int 통신끝점만들기(int 유형);
int 망주소묶기(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, uint32_t ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, unsigned 접속번호);
int 연결기다리기(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ);
void 통신주소재사용(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ);
int 망연결하기(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, uint32_t ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, unsigned 접속번호);
int 망연결받기(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ);
int 통신읽기(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, void *ᎦᏟᏌᏅᎯ, unsigned 개수);
int 통신쓰기(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, const void *ᎦᏟᏌᏅᎯ, unsigned 개수);
int 전문보내기(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, const void *ᎦᏟᏌᏅᎯ, unsigned 개수, uint32_t ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, unsigned 접속번호);
int 전문받기(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, void *ᎦᏟᏌᏅᎯ, unsigned 개수);
unsigned 통신접속번호(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ);
unsigned 상대접속번호(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ);
uint32_t 상대통신주소(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ);
void ᎯᏍᏚᎲᎦ_ᏧᎾᏚᏓᎵ(int ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ);
int ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎠᎯᎸᏍᏗ(int ᎠᏛᏁᎵᏓ);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ, unsigned ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
int ᎢᏳᎵᏍᏙᏗ_ᎨᏒ_ᏅᎦ_ᏧᎾᏚᏓᎵ(unsigned ᎠᏛᏁᎵᏓ, uint32_t ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, uint32_t 가림, uint32_t 관문);
int 응답시험시작(uint32_t ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, unsigned ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ);
int 응답시험읽기(unsigned Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ);
#endif
