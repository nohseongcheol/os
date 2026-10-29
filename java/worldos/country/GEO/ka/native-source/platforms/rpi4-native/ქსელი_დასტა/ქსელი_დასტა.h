#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void მომზადება_ქსელი(void);
void 통신망살피기(void);
int 통신끝점만들기(int აკრეფა_კატეგორია);
int 망주소묶기(int ფაილი_სახელური, uint32_t მისამართი, unsigned 접속번호);
int 연결기다리기(int ფაილი_სახელური);
void 통신주소재사용(int ფაილი_სახელური);
int 망연결하기(int ფაილი_სახელური, uint32_t მისამართი, unsigned 접속번호);
int 망연결받기(int ფაილი_სახელური);
int 통신읽기(int ფაილი_სახელური, void *მონაცემები, unsigned 개수);
int 통신쓰기(int ფაილი_სახელური, const void *მონაცემები, unsigned 개수);
int 전문보내기(int ფაილი_სახელური, const void *მონაცემები, unsigned 개수, uint32_t მისამართი, unsigned 접속번호);
int 전문받기(int ფაილი_სახელური, void *მონაცემები, unsigned 개수);
unsigned 통신접속번호(int ფაილი_სახელური);
unsigned 상대접속번호(int ფაილი_სახელური);
uint32_t 상대통신주소(int ფაილი_სახელური);
void დახურვა_ქსელი(int ფაილი_სახელური);
int ფაილი_გადატანა_მართვა(int ქმედება);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned შენატანი_მნიშვნელობა, unsigned ინდექსი);
int კონფიგურაცია_ქსელი(unsigned ქმედება, uint32_t მისამართი, uint32_t ნიღაბი_მნიშვნელობა, uint32_t კარიბჭე_მნიშვნელობა);
int 응답시험시작(uint32_t მისამართი, unsigned დახარისხების_თანმიმდევრობა_მნიშვნელობა);
int 응답시험읽기(unsigned შენატანი_მნიშვნელობა);
#endif
