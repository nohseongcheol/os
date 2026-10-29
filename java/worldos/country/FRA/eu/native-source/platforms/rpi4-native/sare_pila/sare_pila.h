#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void 통신망준비(void);
void 통신망살피기(void);
int 통신끝점만들기(int MOTA_Kategoria);
int 망주소묶기(int fitxategi_helduleku, uint32_t helbide, unsigned ataka_zenbaki);
int 연결기다리기(int fitxategi_helduleku);
void 통신주소재사용(int fitxategi_helduleku);
int 망연결하기(int fitxategi_helduleku, uint32_t helbide, unsigned ataka_zenbaki);
int 망연결받기(int fitxategi_helduleku);
int 통신읽기(int fitxategi_helduleku, void *datuak, unsigned elementu_ZENBATU);
int 통신쓰기(int fitxategi_helduleku, const void *datuak, unsigned elementu_ZENBATU);
int 전문보내기(int fitxategi_helduleku, const void *datuak, unsigned elementu_ZENBATU, uint32_t helbide, unsigned ataka_zenbaki);
int 전문받기(int fitxategi_helduleku, void *datuak, unsigned elementu_ZENBATU);
unsigned sare_ataka_zenbaki(int fitxategi_helduleku);
unsigned pareko_ataka_zenbaki(int fitxategi_helduleku);
uint32_t 상대통신주소(int fitxategi_helduleku);
void itxi_sare(int fitxategi_helduleku);
int fitxategi_transferitu_kontrol(int Ekintza);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned sarrera_balio, unsigned INDIZE);
int konfiguratu_sare(unsigned Ekintza, uint32_t helbide, uint32_t maskara_balio, uint32_t atebide_balio);
int 응답시험시작(uint32_t helbide, unsigned ordena_balio);
int 응답시험읽기(unsigned sarrera_balio);
#endif
