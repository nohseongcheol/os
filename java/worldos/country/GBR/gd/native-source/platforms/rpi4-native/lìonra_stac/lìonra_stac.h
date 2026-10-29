#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Ullaich_lìonra(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_roinn_seòrsa);
int 망주소묶기(int faidhle_làmhrachan, uint32_t ADDRESS, unsigned 접속번호);
int 연결기다리기(int faidhle_làmhrachan);
void 통신주소재사용(int faidhle_làmhrachan);
int 망연결하기(int faidhle_làmhrachan, uint32_t ADDRESS, unsigned 접속번호);
int 망연결받기(int faidhle_làmhrachan);
int 통신읽기(int faidhle_làmhrachan, void *dàta, unsigned nì_COUNT);
int 통신쓰기(int faidhle_làmhrachan, const void *dàta, unsigned nì_COUNT);
int 전문보내기(int faidhle_làmhrachan, const void *dàta, unsigned nì_COUNT, uint32_t ADDRESS, unsigned 접속번호);
int 전문받기(int faidhle_làmhrachan, void *dàta, unsigned nì_COUNT);
unsigned 통신접속번호(int faidhle_làmhrachan);
unsigned 상대접속번호(int faidhle_làmhrachan);
uint32_t 상대통신주소(int faidhle_làmhrachan);
void dùin_lìonra(int faidhle_làmhrachan);
int faidhle_tar_chur_smachd(int Gnìomh);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned cur_a_steach_VALUE, unsigned INDEX);
int rèitich_lìonra(unsigned Gnìomh, uint32_t ADDRESS, uint32_t 가림, uint32_t 관문);
int 응답시험시작(uint32_t ADDRESS, unsigned òrdugh_VALUE);
int 응답시험읽기(unsigned cur_a_steach_VALUE);
#endif
