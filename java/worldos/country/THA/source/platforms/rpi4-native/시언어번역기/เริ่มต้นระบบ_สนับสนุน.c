#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char อาร์กิวเมนต์_อาร์เรย์[8][256];
int ผู้ใช้_เริ่ม(int 미사용값){
    (void)미사용값;char *อาร์กิวเมนต์_รายการ[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)อาร์กิวเมนต์_อาร์เรย์[순번],256,0,0,0)<0)return 126;อาร์กิวเมนต์_รายการ[순번]=อาร์กิวเมนต์_อาร์เรย์[순번];}อาร์กิวเมนต์_รายการ[인수개수]=0;
    return main(인수개수,อาร์กิวเมนต์_รายการ);
}
void *memset(void*ข้อมูล_ตําแหน่ง,int รหัสอักขระ,size_t 개수){unsigned char*ปลายทาง_ข้อมูล=ข้อมูล_ตําแหน่ง;while(개수--)*ปลายทาง_ข้อมูล++=รหัสอักขระ;return ข้อมูล_ตําแหน่ง;}
void *memcpy(void*ปลายทาง_ข้อมูล,const void*สตริง_ข้อมูล,size_t 개수){unsigned char*첫째값=ปลายทาง_ข้อมูล;const unsigned char*둘째값=สตริง_ข้อมูล;while(개수--)*첫째값++=*둘째값++;return ปลายทาง_ข้อมูล;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned พิกัดแกน_x,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(พิกัดแกน_x,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int วาด_สี่เหลี่ยมผืนผ้า(unsigned 가로,unsigned แนวตั้ง_ตําแหน่ง,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,แนวตั้ง_ตําแหน่ง,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
