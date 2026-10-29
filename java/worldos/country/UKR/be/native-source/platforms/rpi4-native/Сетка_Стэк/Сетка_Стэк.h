#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Падрыхтаваць_Сетка(void);
void 통신망살피기(void);
int 통신끝점만들기(int друкаваць_катэгорыя);
int 망주소묶기(int файл_маркер, uint32_t адрас, unsigned нумар_порта);
int 연결기다리기(int файл_маркер);
void 통신주소재사용(int файл_маркер);
int 망연결하기(int файл_маркер, uint32_t адрас, unsigned нумар_порта);
int 망연결받기(int файл_маркер);
int 통신읽기(int файл_маркер, void *дадзеныя, unsigned 개수);
int 통신쓰기(int файл_маркер, const void *дадзеныя, unsigned 개수);
int 전문보내기(int файл_маркер, const void *дадзеныя, unsigned 개수, uint32_t адрас, unsigned нумар_порта);
int 전문받기(int файл_маркер, void *дадзеныя, unsigned 개수);
unsigned Сетка_нумар_порта(int файл_маркер);
unsigned аднарангавы_нумар_порта(int файл_маркер);
uint32_t 상대통신주소(int файл_маркер);
void закрыць_Сетка(int файл_маркер);
int файл_перанос_кіраванне(int Дзеянне);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned увядзенне_значэнне, unsigned індэкс);
int cканфігураваць_Сетка(unsigned Дзеянне, uint32_t адрас, uint32_t 가림, uint32_t 관문);
int 응답시험시작(uint32_t адрас, unsigned парадак_значэнне);
int 응답시험읽기(unsigned увядзенне_значэнне);
#endif
