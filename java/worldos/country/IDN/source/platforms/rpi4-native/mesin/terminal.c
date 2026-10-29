#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Asli 네 Jendela 합성과 UTF-8 terminal. 바뀐 영역의 Selesai_VALUE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t mesin_Kata;
extern mesin_Kata Papan_elgam(mesin_Kata,mesin_Kata,mesin_Kata),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_font[];
#define 최대열수 237
#define Riwayat_baris_COUNT 160
typedef struct {
    uint32_t 글자칸들[Riwayat_baris_COUNT][최대열수]; uint8_t 모양들[Riwayat_baris_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,koordinat_x,Y_koordinat,ROW_posisi,kolom_posisi,맨위,gulir,전경색,배경색,탈출상태,parameter_VALUE[4],parameter_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal;
static Terminal Windows_Daftar[4];
static int Fokus=-1,출력결과,urutan_VALUE[4],entri_COUNT,seret_VALUE=-1,seret_X,seret_Y;
static unsigned teknologi_informasi_sedang_diproses,단추들,desktop_Tampilan,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal *Terminal_entri;
static unsigned 넓은글자(unsigned kode_karakter){return kode_karakter>=256?2:1;}
static void 사각영역(unsigned koordinat_x,unsigned Y_koordinat,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Papan_persegi_isi(koordinat_x,Y_koordinat,너비값,높이값,색상);
}
void Terminal_glif(unsigned koordinat_x,unsigned Y_koordinat,unsigned kode_karakter,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(kode_karakter)*8;if(kode_karakter==0xffffffffu)return;
    int 왼쪽=koordinat_x,위쪽=Y_koordinat,폭=너비,panjang_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&panjang_VALUE))return;
    if(kode_karakter==' '){Papan_persegi_isi(왼쪽,위쪽,폭,panjang_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=kode_karakter<65536?kode_karakter:kode_karakter>=0x1f600&&kode_karakter<0x1f650?65536+kode_karakter-0x1f600:0xfffd;
    const unsigned char *font_VALUE=Terminal_font+LOOKUP_INDEX*32;
    for(int baris_masukan=위쪽;baris_masukan<위쪽+panjang_VALUE;baris_masukan++){unsigned Background_Intelligent_Transfer_Service_Daftar=font_VALUE[(baris_masukan-Y_koordinat)*2]*256+font_VALUE[(baris_masukan-Y_koordinat)*2+1];for(int slot_entri=왼쪽;slot_entri<왼쪽+폭;slot_entri++)Papan_elgam(slot_entri,baris_masukan,(Background_Intelligent_Transfer_Service_Daftar&(0x8000>>(slot_entri-koordinat_x)))?전경색:배경색);}
}
static void nama_tabel(unsigned koordinat_x,unsigned Y_koordinat,const char *string_data,unsigned 전경색,unsigned 배경색){while(*string_data){unsigned kode_karakter=(unsigned char)*string_data++, 남은수=0;if(kode_karakter>=0xc0){남은수=kode_karakter<0xe0?1:kode_karakter<0xf0?2:3;kode_karakter&=(1u<<(6-남은수))-1;while(남은수--&&*string_data)kode_karakter=(kode_karakter<<6)|((unsigned char)*string_data++&63);}Terminal_glif(koordinat_x,Y_koordinat,kode_karakter,전경색,배경색);koordinat_x+=넓은글자(kode_karakter)*8;}}
static unsigned 첫항목(void){return Terminal_entri->맨위;}
static int 보이는지(void){return Terminal_entri->살아있음&&Fokus>=0&&Terminal_entri==&Windows_Daftar[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ROW_posisi,unsigned kolom_posisi){
    if(!보이는지()||ROW_posisi<첫항목()-Terminal_entri->gulir||ROW_posisi>=첫항목()-Terminal_entri->gulir+Terminal_entri->ROW_COUNT||kolom_posisi>=Terminal_entri->COLUMNS)return;
    unsigned kode_karakter=Terminal_entri->글자칸들[ROW_posisi%Riwayat_baris_COUNT][kolom_posisi],string_data=Terminal_entri->모양들[ROW_posisi%Riwayat_baris_COUNT][kolom_posisi];
    if(넓은글자(kode_karakter)==2&&kolom_posisi+1>=Terminal_entri->COLUMNS)kode_karakter=' ';
    Terminal_glif(Terminal_entri->koordinat_x+12+kolom_posisi*8,Terminal_entri->Y_koordinat+36+(ROW_posisi-첫항목()+Terminal_entri->gulir)*16,kode_karakter?kode_karakter:' ',색상들[string_data&15],색상들[string_data>>4]);
}
static void tanda_sisipan_VALUE(int show_jendela){if(!보이는지()||Terminal_entri->gulir||Terminal_entri->kolom_posisi>=Terminal_entri->COLUMNS||Terminal_entri->ROW_posisi<Terminal_entri->맨위||Terminal_entri->ROW_posisi>=Terminal_entri->맨위+Terminal_entri->ROW_COUNT)return;
    if(!show_jendela||!Terminal_entri->가리개보임)그리기(Terminal_entri->ROW_posisi,Terminal_entri->kolom_posisi);else 사각영역(Terminal_entri->koordinat_x+12+Terminal_entri->kolom_posisi*8,Terminal_entri->Y_koordinat+36+(Terminal_entri->ROW_posisi-Terminal_entri->맨위)*16+14,8,2,색상들[Terminal_entri->전경색]);}
static void Isi_VALUE(void){
    사각영역(Terminal_entri->koordinat_x+12,Terminal_entri->Y_koordinat+36,Terminal_entri->COLUMNS*8,Terminal_entri->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_entri->koordinat_x+12,Vertikal_posisi=Terminal_entri->Y_koordinat+36,폭=Terminal_entri->COLUMNS*8,panjang_VALUE=Terminal_entri->ROW_COUNT*16;
    if(보드그림범위(&가로,&Vertikal_posisi,&폭,&panjang_VALUE)){
    unsigned 첫줄=(Vertikal_posisi-Terminal_entri->Y_koordinat-36)/16,끝줄=(Vertikal_posisi+panjang_VALUE-Terminal_entri->Y_koordinat-36+15)/16;
    unsigned 첫칸=(가로-Terminal_entri->koordinat_x-12)/8,끝칸=(가로+폭-Terminal_entri->koordinat_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 slot_entri 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned kode_karakter=첫칸;kode_karakter<끝칸;kode_karakter++){
        unsigned ROW_posisi=첫항목()-Terminal_entri->gulir+반환값,karakter_VALUE=Terminal_entri->글자칸들[ROW_posisi%Riwayat_baris_COUNT][kode_karakter],string_data=Terminal_entri->모양들[ROW_posisi%Riwayat_baris_COUNT][kode_karakter];
        if(넓은글자(karakter_VALUE)==2&&kode_karakter+1>=Terminal_entri->COLUMNS)karakter_VALUE=' ';
        if((karakter_VALUE==0||karakter_VALUE==' ')&&(string_data>>4)==0)continue;
        Terminal_glif(Terminal_entri->koordinat_x+12+kode_karakter*8,Terminal_entri->Y_koordinat+36+반환값*16,karakter_VALUE?karakter_VALUE:' ',색상들[string_data&15],색상들[string_data>>4]);
    }}
    nama_tabel(Terminal_entri->koordinat_x+12,Terminal_entri->Y_koordinat+Terminal_entri->높이-18,Terminal_entri->gulir?"PgDn: recent output":Terminal_entri->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);tanda_sisipan_VALUE(1);
}
static void 실행틀(int pengidentifikasi_VALUE){
    Terminal_entri=&Windows_Daftar[pengidentifikasi_VALUE];
    int 가로=Terminal_entri->koordinat_x,Vertikal_posisi=Terminal_entri->Y_koordinat,폭=Terminal_entri->너비,panjang_VALUE=Terminal_entri->높이;
    if(!보드그림범위(&가로,&Vertikal_posisi,&폭,&panjang_VALUE))return;
    사각영역(Terminal_entri->koordinat_x,Terminal_entri->Y_koordinat,Terminal_entri->너비,Terminal_entri->높이,0x403127);
    unsigned 색상=pengidentifikasi_VALUE==Fokus?0x905020:0x604438;사각영역(Terminal_entri->koordinat_x,Terminal_entri->Y_koordinat,Terminal_entri->너비,30,색상);
    nama_tabel(Terminal_entri->koordinat_x+12,Terminal_entri->Y_koordinat+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+pengidentifikasi_VALUE),0};nama_tabel(Terminal_entri->koordinat_x+148,Terminal_entri->Y_koordinat+7,수치,0xffffff,색상);
    nama_tabel(Terminal_entri->koordinat_x+240,Terminal_entri->Y_koordinat+7,Terminal_entri->너비>=500?(한글입력?"[ID] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[ID]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_entri->koordinat_x+Terminal_entri->너비-32,Terminal_entri->Y_koordinat+4,26,22,0x5555b8);nama_tabel(Terminal_entri->koordinat_x+Terminal_entri->너비-24,Terminal_entri->Y_koordinat+7,"X",0xffffff,0x5555b8);
    Isi_VALUE();
}
static void 장면그리기(void){
    if(!desktop_Tampilan)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nama_tabel(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Daftar[순번].살아있음){unsigned kode_karakter=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,kode_karakter);nama_tabel(160+순번*112,8,"Terminal",0xffffff,kode_karakter);char string_data[2]={(char)('1'+순번),0};nama_tabel(232+순번*112,8,string_data,0xffffff,kode_karakter);}
    if(!entri_COUNT)nama_tabel(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<entri_COUNT;순번++)실행틀(urutan_VALUE[순번]);화면다시그림(Fokus);Terminal_entri=&Windows_Daftar[출력결과];
}
static void Paint_wilayah(int 가로,int Vertikal_posisi,int 폭,int panjang_VALUE){
    if(!desktop_Tampilan||!보드그림범위(&가로,&Vertikal_posisi,&폭,&panjang_VALUE))return;
    for(int baris_masukan=Vertikal_posisi;baris_masukan<Vertikal_posisi+panjang_VALUE;baris_masukan+=32){
        int 띠높이=Vertikal_posisi+panjang_VALUE-baris_masukan;if(띠높이>32)띠높이=32;
        if(Papan_Mulai_gambar(가로,baris_masukan,폭,띠높이)){장면그리기();Papan_Selesai_gambar();}
    }
}
static void pelacakan(void){Paint_wilayah(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Jendela 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Vertikal_posisi,int 폭,int panjang_VALUE,Terminal *Jendela){
    int 왼쪽=가로>(int)Jendela->koordinat_x?가로:(int)Jendela->koordinat_x;
    int 위쪽=Vertikal_posisi>(int)Jendela->Y_koordinat?Vertikal_posisi:(int)Jendela->Y_koordinat;
    int RIGHT=가로+폭<(int)(Jendela->koordinat_x+Jendela->너비)?가로+폭:(int)(Jendela->koordinat_x+Jendela->너비);
    int 아래쪽=Vertikal_posisi+panjang_VALUE<(int)(Jendela->Y_koordinat+Jendela->높이)?Vertikal_posisi+panjang_VALUE:(int)(Jendela->Y_koordinat+Jendela->높이);
    Paint_wilayah(Jendela->koordinat_x,Jendela->Y_koordinat,Jendela->너비,Jendela->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){Paint_wilayah(가로,Vertikal_posisi,폭,panjang_VALUE);return;}
    Paint_wilayah(가로,Vertikal_posisi,폭,위쪽-Vertikal_posisi);
    Paint_wilayah(가로,아래쪽,폭,Vertikal_posisi+panjang_VALUE-아래쪽);
    Paint_wilayah(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_wilayah(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void sinyal_Fokus(void){teknologi_informasi_sedang_diproses=(teknologi_informasi_sedang_diproses&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal *jendela_entri=&Windows_Daftar[Fokus];
        nama_tabel(jendela_entri->koordinat_x+240,jendela_entri->Y_koordinat+7,jendela_entri->너비>=500?(한글입력?"[ID] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[ID]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int pengidentifikasi_VALUE){if(pengidentifikasi_VALUE<0||pengidentifikasi_VALUE>=4||!Windows_Daftar[pengidentifikasi_VALUE].살아있음)return;int saat_ini_posisi=0;while(saat_ini_posisi<entri_COUNT&&urutan_VALUE[saat_ini_posisi]!=pengidentifikasi_VALUE)saat_ini_posisi++;for(;saat_ini_posisi+1<entri_COUNT;saat_ini_posisi++)urutan_VALUE[saat_ini_posisi]=urutan_VALUE[saat_ini_posisi+1];urutan_VALUE[entri_COUNT-1]=pengidentifikasi_VALUE;Fokus=pengidentifikasi_VALUE;sinyal_Fokus();pelacakan();}
static void kosong(unsigned ROW_posisi){for(unsigned kode_karakter=0;kode_karakter<최대열수;kode_karakter++){Terminal_entri->글자칸들[ROW_posisi%Riwayat_baris_COUNT][kode_karakter]=0;Terminal_entri->모양들[ROW_posisi%Riwayat_baris_COUNT][kode_karakter]=Terminal_entri->전경색|(Terminal_entri->배경색<<4);}}
static void bersihkan_Isi(void){Terminal_entri->ROW_posisi=Terminal_entri->kolom_posisi=Terminal_entri->맨위=Terminal_entri->gulir=0;for(unsigned 반환값=0;반환값<Riwayat_baris_COUNT;반환값++)kosong(반환값);if(보이는지())Isi_VALUE();}
static int Buat_entri(void){
    if(!보드화면기억공간())return -19;int pengidentifikasi_VALUE=0;while(pengidentifikasi_VALUE<4&&Windows_Daftar[pengidentifikasi_VALUE].살아있음)pengidentifikasi_VALUE++;if(pengidentifikasi_VALUE==4)return -28;
    desktop_Tampilan=1;Terminal_entri=&Windows_Daftar[pengidentifikasi_VALUE];memset(Terminal_entri,0,sizeof(*Terminal_entri));Terminal_entri->살아있음=1;Terminal_entri->너비=568;Terminal_entri->높이=360;Terminal_entri->COLUMNS=68;Terminal_entri->ROW_COUNT=19;Terminal_entri->koordinat_x=12+pengidentifikasi_VALUE*16;Terminal_entri->Y_koordinat=48+pengidentifikasi_VALUE*18;Terminal_entri->전경색=7;Terminal_entri->가리개보임=1;
    for(unsigned 반환값=0;반환값<Riwayat_baris_COUNT;반환값++)kosong(반환값);urutan_VALUE[entri_COUNT++]=pengidentifikasi_VALUE;Fokus=pengidentifikasi_VALUE;teknologi_informasi_sedang_diproses|=1u<<(4+pengidentifikasi_VALUE);sinyal_Fokus();pelacakan();return pengidentifikasi_VALUE+1;
}
static void Tutup_jendela(int pengidentifikasi_VALUE){
    if(pengidentifikasi_VALUE<0||pengidentifikasi_VALUE>=4||!Windows_Daftar[pengidentifikasi_VALUE].살아있음)return;Windows_Daftar[pengidentifikasi_VALUE].살아있음=0;teknologi_informasi_sedang_diproses|=1u<<(8+pengidentifikasi_VALUE);
    int saat_ini_posisi=0;while(saat_ini_posisi<entri_COUNT&&urutan_VALUE[saat_ini_posisi]!=pengidentifikasi_VALUE)saat_ini_posisi++;for(;saat_ini_posisi+1<entri_COUNT;saat_ini_posisi++)urutan_VALUE[saat_ini_posisi]=urutan_VALUE[saat_ini_posisi+1];entri_COUNT--;
    if(Fokus==pengidentifikasi_VALUE)Fokus=entri_COUNT?urutan_VALUE[entri_COUNT-1]:-1;sinyal_Fokus();pelacakan();
}
static void 줄바꿈(void){Terminal_entri->kolom_posisi=0;Terminal_entri->ROW_posisi++;if(Terminal_entri->ROW_posisi>=Terminal_entri->맨위+Terminal_entri->ROW_COUNT){Terminal_entri->맨위++;kosong(Terminal_entri->ROW_posisi);if(보이는지())Isi_VALUE();}}
static void poin_kode(unsigned kode_karakter){
    if(kode_karakter==13){Terminal_entri->kolom_posisi=0;return;}if(kode_karakter==10){줄바꿈();return;}if(kode_karakter==8){if(Terminal_entri->kolom_posisi)Terminal_entri->kolom_posisi--;return;}
    if(kode_karakter==9){unsigned item_COUNT=8-Terminal_entri->kolom_posisi%8;while(item_COUNT--)poin_kode(' ');return;}if(kode_karakter<32||kode_karakter==127)return;
    unsigned 너비값=넓은글자(kode_karakter);if(Terminal_entri->kolom_posisi+너비값>Terminal_entri->COLUMNS)줄바꿈();
    if(Terminal_entri->글자칸들[Terminal_entri->ROW_posisi%Riwayat_baris_COUNT][Terminal_entri->kolom_posisi]==0xffffffffu&&Terminal_entri->kolom_posisi){Terminal_entri->글자칸들[Terminal_entri->ROW_posisi%Riwayat_baris_COUNT][Terminal_entri->kolom_posisi-1]=' ';그리기(Terminal_entri->ROW_posisi,Terminal_entri->kolom_posisi-1);}
    if(넓은글자(Terminal_entri->글자칸들[Terminal_entri->ROW_posisi%Riwayat_baris_COUNT][Terminal_entri->kolom_posisi])==2&&Terminal_entri->kolom_posisi+1<Terminal_entri->COLUMNS){Terminal_entri->글자칸들[Terminal_entri->ROW_posisi%Riwayat_baris_COUNT][Terminal_entri->kolom_posisi+1]=' ';그리기(Terminal_entri->ROW_posisi,Terminal_entri->kolom_posisi+1);}
    Terminal_entri->글자칸들[Terminal_entri->ROW_posisi%Riwayat_baris_COUNT][Terminal_entri->kolom_posisi]=kode_karakter;Terminal_entri->모양들[Terminal_entri->ROW_posisi%Riwayat_baris_COUNT][Terminal_entri->kolom_posisi]=Terminal_entri->전경색|(Terminal_entri->배경색<<4);
    if(너비값==2)Terminal_entri->글자칸들[Terminal_entri->ROW_posisi%Riwayat_baris_COUNT][Terminal_entri->kolom_posisi+1]=0xffffffffu;
    그리기(Terminal_entri->ROW_posisi,Terminal_entri->kolom_posisi);Terminal_entri->kolom_posisi+=너비값;
}
static void handel_kontrol_urutan(unsigned kode_karakter){
    unsigned item_COUNT=Terminal_entri->parameter_VALUE[0]?Terminal_entri->parameter_VALUE[0]:1;
    if(kode_karakter=='m')for(unsigned 순번=0;순번<=Terminal_entri->parameter_INDEX;순번++){unsigned data_posisi=Terminal_entri->parameter_VALUE[순번];if(!data_posisi){Terminal_entri->전경색=7;Terminal_entri->배경색=0;}if(data_posisi==1&&Terminal_entri->전경색<8)Terminal_entri->전경색+=8;if(data_posisi==7){unsigned 유지=Terminal_entri->전경색;Terminal_entri->전경색=Terminal_entri->배경색;Terminal_entri->배경색=유지;}if(data_posisi>=30&&data_posisi<=37)Terminal_entri->전경색=data_posisi-30;if(data_posisi>=90&&data_posisi<=97)Terminal_entri->전경색=data_posisi-90+8;if(data_posisi>=40&&data_posisi<=47)Terminal_entri->배경색=data_posisi-40;if(data_posisi>=100&&data_posisi<=107)Terminal_entri->배경색=data_posisi-100+8;if(data_posisi==39)Terminal_entri->전경색=7;if(data_posisi==49)Terminal_entri->배경색=0;}
    if(kode_karakter=='J'&&(Terminal_entri->parameter_VALUE[0]==2||Terminal_entri->parameter_VALUE[0]==3))bersihkan_Isi();
    if(kode_karakter=='K'){unsigned 출발위치=Terminal_entri->parameter_VALUE[0]==2?0:Terminal_entri->kolom_posisi,도착위치=Terminal_entri->parameter_VALUE[0]==1?Terminal_entri->kolom_posisi+1:Terminal_entri->COLUMNS;if(Terminal_entri->parameter_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_entri->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_entri->ROW_posisi%Riwayat_baris_COUNT,karakter_VALUE=Terminal_entri->글자칸들[ROW_VALUE][순번],bentuk_VALUE=Terminal_entri->전경색|(Terminal_entri->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 font_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(karakter_VALUE!=0&&karakter_VALUE!=' ')||Terminal_entri->모양들[ROW_VALUE][순번]!=bentuk_VALUE;
        Terminal_entri->글자칸들[ROW_VALUE][순번]=' ';Terminal_entri->모양들[ROW_VALUE][순번]=bentuk_VALUE;
        if(바뀜)그리기(Terminal_entri->ROW_posisi,순번);
    }}
    if(kode_karakter=='D')Terminal_entri->kolom_posisi=item_COUNT>Terminal_entri->kolom_posisi?0:Terminal_entri->kolom_posisi-item_COUNT;if(kode_karakter=='C')Terminal_entri->kolom_posisi=Terminal_entri->kolom_posisi+item_COUNT>=Terminal_entri->COLUMNS?Terminal_entri->COLUMNS-1:Terminal_entri->kolom_posisi+item_COUNT;
    if(kode_karakter=='G')Terminal_entri->kolom_posisi=item_COUNT>Terminal_entri->COLUMNS?Terminal_entri->COLUMNS-1:item_COUNT-1;if(kode_karakter=='A')Terminal_entri->ROW_posisi=item_COUNT>Terminal_entri->ROW_posisi-Terminal_entri->맨위?Terminal_entri->맨위:Terminal_entri->ROW_posisi-item_COUNT;
    if(kode_karakter=='B')Terminal_entri->ROW_posisi=Terminal_entri->ROW_posisi+item_COUNT>=Terminal_entri->맨위+Terminal_entri->ROW_COUNT?Terminal_entri->맨위+Terminal_entri->ROW_COUNT-1:Terminal_entri->ROW_posisi+item_COUNT;
    if(kode_karakter=='H'||kode_karakter=='f'){Terminal_entri->ROW_posisi=Terminal_entri->맨위+(item_COUNT>Terminal_entri->ROW_COUNT?Terminal_entri->ROW_COUNT:item_COUNT)-1;unsigned koordinat_x=Terminal_entri->parameter_VALUE[1]?Terminal_entri->parameter_VALUE[1]:1;Terminal_entri->kolom_posisi=(koordinat_x>Terminal_entri->COLUMNS?Terminal_entri->COLUMNS:koordinat_x)-1;}
    if(kode_karakter=='s'){Terminal_entri->저장행=Terminal_entri->ROW_posisi;Terminal_entri->저장열=Terminal_entri->kolom_posisi;}if(kode_karakter=='u'){Terminal_entri->ROW_posisi=Terminal_entri->저장행;Terminal_entri->kolom_posisi=Terminal_entri->저장열<Terminal_entri->COLUMNS?Terminal_entri->저장열:Terminal_entri->COLUMNS-1;}
    if((kode_karakter=='h'||kode_karakter=='l')&&Terminal_entri->parameter_VALUE[0]==25)Terminal_entri->가리개보임=kode_karakter=='h';
}
void Terminal_byte(unsigned SECOND_VALUE){
    Terminal_entri=&Windows_Daftar[출력결과];if(!Terminal_entri->살아있음)return;tanda_sisipan_VALUE(0);if(Terminal_entri->gulir){Terminal_entri->gulir=0;if(보이는지())Isi_VALUE();}
    if(Terminal_entri->탈출상태==1){Terminal_entri->탈출상태=SECOND_VALUE=='['?2:0;Terminal_entri->parameter_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_entri->parameter_VALUE[순번]=0;}
    else if(Terminal_entri->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_entri->parameter_VALUE[Terminal_entri->parameter_INDEX]<10000)Terminal_entri->parameter_VALUE[Terminal_entri->parameter_INDEX]=Terminal_entri->parameter_VALUE[Terminal_entri->parameter_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_entri->parameter_INDEX<3)Terminal_entri->parameter_INDEX++;else{handel_kontrol_urutan(SECOND_VALUE);Terminal_entri->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_entri->긴부호없는값=0;Terminal_entri->탈출상태=1;}else{
        if(Terminal_entri->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_entri->긴부호없는값=0;poin_kode(0xfffd);}
        if(Terminal_entri->긴부호없는값){Terminal_entri->부호없는결과=Terminal_entri->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_entri->긴부호없는값==0)poin_kode(Terminal_entri->부호없는결과<Terminal_entri->SMALL_VALUE||Terminal_entri->부호없는결과>0x10ffff||(Terminal_entri->부호없는결과>=0xd800&&Terminal_entri->부호없는결과<=0xdfff)?0xfffd:Terminal_entri->부호없는결과);}
        else if(SECOND_VALUE<128)poin_kode(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_entri->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_entri->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_entri->긴부호없는값))-1);Terminal_entri->SMALL_VALUE=Terminal_entri->긴부호없는값==1?128:Terminal_entri->긴부호없는값==2?2048:65536;}else poin_kode(0xfffd);
    }tanda_sisipan_VALUE(1);
}
int Terminal_sedang_diproses(void){return teknologi_informasi_sedang_diproses!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int ubah_ukuran_seret=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Vertikal_posisi) {
    for(int urutan_VALUE_e9fa7815=entri_COUNT-1;urutan_VALUE_e9fa7815>=0;urutan_VALUE_e9fa7815--){
        int pengidentifikasi_VALUE=urutan_VALUE[urutan_VALUE_e9fa7815];Terminal *Jendela=&Windows_Daftar[pengidentifikasi_VALUE];
        if(가로>=(int)Jendela->koordinat_x&&Vertikal_posisi>=(int)Jendela->Y_koordinat&&
           가로<(int)(Jendela->koordinat_x+Jendela->너비)&&Vertikal_posisi<(int)(Jendela->Y_koordinat+Jendela->높이))return pengidentifikasi_VALUE;
    }return -1;
}
static int 모서리찾기(int pengidentifikasi_VALUE,int 가로,int Vertikal_posisi) {
    if(pengidentifikasi_VALUE<0)return 0;Terminal *Jendela=&Windows_Daftar[pengidentifikasi_VALUE];
    int 왼쪽=가로<(int)Jendela->koordinat_x+8,RIGHT=가로>=(int)(Jendela->koordinat_x+Jendela->너비)-8;
    int 위쪽=Vertikal_posisi<(int)Jendela->Y_koordinat+8,아래쪽=Vertikal_posisi>=(int)(Jendela->Y_koordinat+Jendela->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int pemisah_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void gerak_ubah_ukuran(int 가로,int Vertikal_posisi) {
    Terminal *Jendela=&Windows_Daftar[ubah_ukuran_seret];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=pemisah_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=pemisah_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=pemisah_VALUE(처음세로+Vertikal_posisi-잡은세로,34,아래쪽-216);
    else 아래쪽=pemisah_VALUE(처음세로+처음높이+Vertikal_posisi-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(Jendela->COLUMNS!=COLUMNS||Jendela->ROW_COUNT!=ROW_COUNT){
        Jendela->크기바뀜=1;Jendela->COLUMNS=COLUMNS;Jendela->ROW_COUNT=ROW_COUNT;
        if(Jendela->kolom_posisi>=COLUMNS)Jendela->kolom_posisi=COLUMNS-1;
        if(Jendela->ROW_posisi>=Jendela->맨위+ROW_COUNT)Jendela->맨위=Jendela->ROW_posisi-ROW_COUNT+1;
        unsigned 한도=Jendela->맨위;if(한도>Riwayat_baris_COUNT-ROW_COUNT)한도=Riwayat_baris_COUNT-ROW_COUNT;
        if(Jendela->gulir>한도)Jendela->gulir=한도;
    }
    int 옛가로=Jendela->koordinat_x,옛세로=Jendela->Y_koordinat,옛폭=Jendela->너비,옛길이=Jendela->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    Jendela->koordinat_x=왼쪽;Jendela->Y_koordinat=위쪽;Jendela->너비=RIGHT-왼쪽;Jendela->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Jendela);
}
void Terminal_pointer(unsigned Berikutnya_item,int koordinat_x,int Y_koordinat){
    unsigned 눌림=Berikutnya_item&~단추들;단추들=Berikutnya_item;
    if(!desktop_Tampilan){seret_VALUE=-1;ubah_ukuran_seret=-1;Papan_pointer(koordinat_x,Y_koordinat,1);return;}
    if(!(Berikutnya_item&1)){seret_VALUE=-1;ubah_ukuran_seret=-1;}
    if(ubah_ukuran_seret>=0&&!Windows_Daftar[ubah_ukuran_seret].살아있음)ubah_ukuran_seret=-1;
    if(seret_VALUE>=0&&!Windows_Daftar[seret_VALUE].살아있음)seret_VALUE=-1;
    if(ubah_ukuran_seret>=0){
        gerak_ubah_ukuran(koordinat_x,Y_koordinat);Papan_pointer(koordinat_x,Y_koordinat,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Papan_pointer(koordinat_x,Y_koordinat,1);
    if(seret_VALUE>=0){
        Terminal *Jendela=&Windows_Daftar[seret_VALUE];
        int 옛가로=Jendela->koordinat_x,옛세로=Jendela->Y_koordinat;
        Jendela->koordinat_x=pemisah_VALUE(koordinat_x-seret_X,0,보드화면너비()-Jendela->너비);
        Jendela->Y_koordinat=pemisah_VALUE(Y_koordinat-seret_Y,34,보드화면높이()-Jendela->높이);
        if(옛가로!=(int)Jendela->koordinat_x||옛세로!=(int)Jendela->Y_koordinat)창자리그리기(옛가로,옛세로,Jendela->너비,Jendela->높이,Jendela);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,koordinat_x,Y_koordinat)){화면가리킴(Fokus,눌림,koordinat_x,Y_koordinat);return;}
    int pengidentifikasi_VALUE=가리킨창(koordinat_x,Y_koordinat),모서리=모서리찾기(pengidentifikasi_VALUE,koordinat_x,Y_koordinat);
    if(모서리)Papan_pointer(koordinat_x,Y_koordinat,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal *Jendela=&Windows_Daftar[pengidentifikasi_VALUE];ubah_ukuran_seret=pengidentifikasi_VALUE;잡은모서리=모서리;잡은가로=koordinat_x;잡은세로=Y_koordinat;
            처음가로=Jendela->koordinat_x;처음세로=Jendela->Y_koordinat;처음너비=Jendela->너비;처음높이=Jendela->높이;
            if(pengidentifikasi_VALUE!=Fokus)앞으로올리기(pengidentifikasi_VALUE);return;
        }
        if(Y_koordinat<32&&koordinat_x>=6&&koordinat_x<142){Buat_entri();return;}
        if(Y_koordinat<32&&koordinat_x>=154&&koordinat_x<602){앞으로올리기((koordinat_x-154)/112);return;}
        if(pengidentifikasi_VALUE>=0){
            Terminal *Jendela=&Windows_Daftar[pengidentifikasi_VALUE];
            if(Y_koordinat<(int)Jendela->Y_koordinat+30&&koordinat_x>=(int)(Jendela->koordinat_x+Jendela->너비)-32){Tutup_jendela(pengidentifikasi_VALUE);return;}
            if(pengidentifikasi_VALUE!=Fokus)앞으로올리기(pengidentifikasi_VALUE);
            if(Y_koordinat<(int)Jendela->Y_koordinat+30){seret_VALUE=pengidentifikasi_VALUE;seret_X=koordinat_x-Jendela->koordinat_x;seret_Y=Y_koordinat-Jendela->Y_koordinat;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_entri=&Windows_Daftar[Fokus];if(눌림&8){unsigned 한도=Terminal_entri->맨위;if(한도>Riwayat_baris_COUNT-Terminal_entri->ROW_COUNT)한도=Riwayat_baris_COUNT-Terminal_entri->ROW_COUNT;Terminal_entri->gulir=Terminal_entri->gulir+9>한도?한도:Terminal_entri->gulir+9;}else Terminal_entri->gulir=Terminal_entri->gulir<9?0:Terminal_entri->gulir-9;pelacakan();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Buat_entri();if(누름값==2&&entri_COUNT)앞으로올리기(urutan_VALUE[0]);if(누름값==3)Tutup_jendela(Fokus);}
mesin_Kata Papan_Terminal(mesin_Kata Aksi){
    if(Aksi==300){if(!Windows_Daftar[출력결과].살아있음)return Buat_entri();desktop_Tampilan=1;pelacakan();return 0;}
    if(Aksi==0){Tutup_jendela(Fokus);return 0;}if(Aksi==1)return (uint32_t)Buat_entri();if(Aksi==2)return Fokus>=0;
    if(Aksi==9){desktop_Tampilan=0;return 0;}if(Aksi==7)return entri_COUNT;if(Aksi==10)return Fokus+1;if(Aksi==11)return 출력결과;
    if(Aksi==13){Terminal *Jendela=&Windows_Daftar[출력결과];return Jendela->살아있음?(Jendela->ROW_COUNT<<16)|Jendela->COLUMNS:(19<<16)|68;}
    if(Aksi==14){unsigned VALUE=Windows_Daftar[출력결과].크기바뀜;Windows_Daftar[출력결과].크기바뀜=0;return VALUE;}
    if(Aksi==12){unsigned VALUE=teknologi_informasi_sedang_diproses;teknologi_informasi_sedang_diproses=0;return VALUE;}
    if(Aksi>=20&&Aksi<24)return Windows_Daftar[Aksi-20].살아있음;
    if(Aksi>=100&&Aksi<104){출력결과=Aksi-100;Terminal_entri=&Windows_Daftar[출력결과];return 0;}
    if(Aksi>=200&&Aksi<204){앞으로올리기(Aksi-200);return 0;}
    if(Aksi==3){pelacakan();return 0;}Terminal_entri=&Windows_Daftar[출력결과];if(!Terminal_entri->살아있음)return 0;
    if(Aksi==4)bersihkan_Isi();if(Aksi==5||Aksi==6){unsigned 이전=단추들;Terminal_pointer(Aksi==5?8:16,0,0);단추들=이전;}return 1;
}
