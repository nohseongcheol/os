#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Әзерләү_Челтәр(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_категория);
int 망주소묶기(int файл_дескриптор, uint32_t адрес, unsigned 접속번호);
int 연결기다리기(int файл_дескриптор);
void 통신주소재사용(int файл_дескриптор);
int 망연결하기(int файл_дескриптор, uint32_t адрес, unsigned 접속번호);
int 망연결받기(int файл_дескриптор);
int 통신읽기(int файл_дескриптор, void *мәгълүмат, unsigned элемент_COUNT);
int 통신쓰기(int файл_дескриптор, const void *мәгълүмат, unsigned элемент_COUNT);
int 전문보내기(int файл_дескриптор, const void *мәгълүмат, unsigned элемент_COUNT, uint32_t адрес, unsigned 접속번호);
int 전문받기(int файл_дескриптор, void *мәгълүмат, unsigned элемент_COUNT);
unsigned 통신접속번호(int файл_дескриптор);
unsigned 상대접속번호(int файл_дескриптор);
uint32_t 상대통신주소(int файл_дескриптор);
void чик_Челтәр(int файл_дескриптор);
int файл_күчерү_идарә(int Гамәл);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned кертү_VALUE, unsigned INDEX);
int көйләү_Челтәр(unsigned Гамәл, uint32_t адрес, uint32_t үрнәк_VALUE, uint32_t шлюз_VALUE);
int 응답시험시작(uint32_t адрес, unsigned тәртипкә_салу_VALUE);
int 응답시험읽기(unsigned кертү_VALUE);
#endif
