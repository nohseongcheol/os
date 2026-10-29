#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Бэлтгэх_Сүлжээ(void);
void 통신망살피기(void);
int 통신끝점만들기(int бичих_ангилал);
int 망주소묶기(int файл_барих, uint32_t хаяг, unsigned 접속번호);
int 연결기다리기(int файл_барих);
void 통신주소재사용(int файл_барих);
int 망연결하기(int файл_барих, uint32_t хаяг, unsigned 접속번호);
int 망연결받기(int файл_барих);
int 통신읽기(int файл_барих, void *өгөгдөл, unsigned 개수);
int 통신쓰기(int файл_барих, const void *өгөгдөл, unsigned 개수);
int 전문보내기(int файл_барих, const void *өгөгдөл, unsigned 개수, uint32_t хаяг, unsigned 접속번호);
int 전문받기(int файл_барих, void *өгөгдөл, unsigned 개수);
unsigned 통신접속번호(int файл_барих);
unsigned 상대접속번호(int файл_барих);
uint32_t 상대통신주소(int файл_барих);
void хаах_Сүлжээ(int файл_барих);
int файл_дамжуулах_хяналт(int Үйлдэл);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned оролт_утга, unsigned индекс);
int тохируулах_Сүлжээ(unsigned Үйлдэл, uint32_t хаяг, uint32_t маск_утга, uint32_t гарц_утга);
int 응답시험시작(uint32_t хаяг, unsigned дараалал_утга);
int 응답시험읽기(unsigned оролт_утга);
#endif
