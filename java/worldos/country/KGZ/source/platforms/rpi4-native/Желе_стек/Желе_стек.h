#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Даярдоо_Желе(void);
void 통신망살피기(void);
int 통신끝점만들기(int түрү_категория);
int 망주소묶기(int файл_тутка, uint32_t дарек, unsigned 접속번호);
int 연결기다리기(int файл_тутка);
void 통신주소재사용(int файл_тутка);
int 망연결하기(int файл_тутка, uint32_t дарек, unsigned 접속번호);
int 망연결받기(int файл_тутка);
int 통신읽기(int файл_тутка, void *берилмелер, unsigned 개수);
int 통신쓰기(int файл_тутка, const void *берилмелер, unsigned 개수);
int 전문보내기(int файл_тутка, const void *берилмелер, unsigned 개수, uint32_t дарек, unsigned 접속번호);
int 전문받기(int файл_тутка, void *берилмелер, unsigned 개수);
unsigned 통신접속번호(int файл_тутка);
unsigned 상대접속번호(int файл_тутка);
uint32_t 상대통신주소(int файл_тутка);
void жабуу_Желе(int файл_тутка);
int файл_ташүү_башкаруу(int Аракети);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned киргизме_жазуу_маани, unsigned индекс);
int конфигурациялоо_Желе(unsigned Аракети, uint32_t дарек, uint32_t маска_маани, uint32_t шлюз_маани);
int 응답시험시작(uint32_t дарек, unsigned ылгоо_ирети_маани);
int 응답시험읽기(unsigned киргизме_жазуу_маани);
#endif
