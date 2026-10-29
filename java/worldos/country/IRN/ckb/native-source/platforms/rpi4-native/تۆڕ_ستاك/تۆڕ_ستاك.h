#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void ئامادە_کردن_تۆڕ(void);
void 통신망살피기(void);
int 통신끝점만들기(int چاپکردن_پۆل);
int 망주소묶기(int فایل_دەسک, uint32_t ناونیشان, unsigned 접속번호);
int 연결기다리기(int فایل_دەسک);
void 통신주소재사용(int فایل_دەسک);
int 망연결하기(int فایل_دەسک, uint32_t ناونیشان, unsigned 접속번호);
int 망연결받기(int فایل_دەسک);
int 통신읽기(int فایل_دەسک, void *دەیتا, unsigned 개수);
int 통신쓰기(int فایل_دەسک, const void *دەیتا, unsigned 개수);
int 전문보내기(int فایل_دەسک, const void *دەیتا, unsigned 개수, uint32_t ناونیشان, unsigned 접속번호);
int 전문받기(int فایل_دەسک, void *دەیتا, unsigned 개수);
unsigned 통신접속번호(int فایل_دەسک);
unsigned 상대접속번호(int فایل_دەسک);
uint32_t 상대통신주소(int فایل_دەسک);
void داخستن_تۆڕ(int فایل_دەسک);
int فایل_گواستنەوە_کۆنترۆڵ(int ئاکشن);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned تێنووسین_نرخ, unsigned پێرست);
int شێوەبەندی_کردن_تۆڕ(unsigned ئاکشن, uint32_t ناونیشان, uint32_t 가림, uint32_t 관문);
int 응답시험시작(uint32_t ناونیشان, unsigned ئۆردەر_نرخ);
int 응답시험읽기(unsigned تێنووسین_نرخ);
#endif
