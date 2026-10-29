#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Припремити_Мрежа(void);
void 통신망살피기(void);
int 통신끝점만들기(int тип_област);
int 망주소묶기(int фајл_хватиште, uint32_t адреса, unsigned број_порта);
int 연결기다리기(int фајл_хватиште);
void 통신주소재사용(int фајл_хватиште);
int 망연결하기(int фајл_хватиште, uint32_t адреса, unsigned број_порта);
int 망연결받기(int фајл_хватиште);
int 통신읽기(int фајл_хватиште, void *подаци, unsigned 개수);
int 통신쓰기(int фајл_хватиште, const void *подаци, unsigned 개수);
int 전문보내기(int фајл_хватиште, const void *подаци, unsigned 개수, uint32_t адреса, unsigned број_порта);
int 전문받기(int фајл_хватиште, void *подаци, unsigned 개수);
unsigned Мрежа_број_порта(int фајл_хватиште);
unsigned 상대접속번호(int фајл_хватиште);
uint32_t 상대통신주소(int фајл_хватиште);
void затварање_Мрежа(int фајл_хватиште);
int фајл_пренос_контрола(int радња);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned унос_вриједност, unsigned индекс);
int конфигурисати_Мрежа(unsigned радња, uint32_t адреса, uint32_t маска_вриједност, uint32_t мрежни_пролаз_вриједност);
int 응답시험시작(uint32_t адреса, unsigned поредати_вриједност);
int 응답시험읽기(unsigned унос_вриједност);
#endif
