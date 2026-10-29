#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Омода_кардан_Шабака(void);
void 통신망살피기(void);
int 통신끝점만들기(int навъ_категория);
int 망주소묶기(int файл_дастак, uint32_t суроға, unsigned 접속번호);
int 연결기다리기(int файл_дастак);
void 통신주소재사용(int файл_дастак);
int 망연결하기(int файл_дастак, uint32_t суроға, unsigned 접속번호);
int 망연결받기(int файл_дастак);
int 통신읽기(int файл_дастак, void *иттилоот, unsigned 개수);
int 통신쓰기(int файл_дастак, const void *иттилоот, unsigned 개수);
int 전문보내기(int файл_дастак, const void *иттилоот, unsigned 개수, uint32_t суроға, unsigned 접속번호);
int 전문받기(int файл_дастак, void *иттилоот, unsigned 개수);
unsigned 통신접속번호(int файл_дастак);
unsigned 상대접속번호(int файл_дастак);
uint32_t 상대통신주소(int файл_дастак);
void пӯшидан_Шабака(int файл_дастак);
int файл_интиқол_идоракунӣ(int Амал);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ворида_қимат, unsigned индекс);
int конфигуратсия_кардан_Шабака(unsigned Амал, uint32_t суроға, uint32_t 가림, uint32_t 관문);
int 응답시험시작(uint32_t суроға, unsigned тартиб_қимат);
int 응답시험읽기(unsigned ворида_қимат);
#endif
