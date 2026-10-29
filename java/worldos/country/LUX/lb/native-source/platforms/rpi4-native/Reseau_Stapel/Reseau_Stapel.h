#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Préparéieren_Reseau(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_Kategorie);
int 망주소묶기(int Fichier_Handle, uint32_t Adress, unsigned 접속번호);
int 연결기다리기(int Fichier_Handle);
void 통신주소재사용(int Fichier_Handle);
int 망연결하기(int Fichier_Handle, uint32_t Adress, unsigned 접속번호);
int 망연결받기(int Fichier_Handle);
int 통신읽기(int Fichier_Handle, void *Daten, unsigned Element_COUNT);
int 통신쓰기(int Fichier_Handle, const void *Daten, unsigned Element_COUNT);
int 전문보내기(int Fichier_Handle, const void *Daten, unsigned Element_COUNT, uint32_t Adress, unsigned 접속번호);
int 전문받기(int Fichier_Handle, void *Daten, unsigned Element_COUNT);
unsigned 통신접속번호(int Fichier_Handle);
unsigned 상대접속번호(int Fichier_Handle);
uint32_t 상대통신주소(int Fichier_Handle);
void Clôture_Reseau(int Fichier_Handle);
int Fichier_Transfer_Kontroll(int Aktioun);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned Agab_VALUE, unsigned INDEX);
int konfiguréieren_Reseau(unsigned Aktioun, uint32_t Adress, uint32_t Mask_VALUE, uint32_t Gateway_VALUE);
int 응답시험시작(uint32_t Adress, unsigned Reiefolleg_VALUE);
int 응답시험읽기(unsigned Agab_VALUE);
#endif
