#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Asli 네 Tetingkap 합성과 UTF-8 Terminal. 바뀐 영역의 Selesai_VALUE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t mesin_Word;
extern mesin_Word Papan_pel(mesin_Word,mesin_Word,mesin_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_fon[];
#define 최대열수 237
#define Sejarah_baris_COUNT 160
typedef struct {
    uint32_t 글자칸들[Sejarah_baris_COUNT][최대열수]; uint8_t 모양들[Sejarah_baris_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,koordinat_x,Y_koordinat,ROW_jawatan,lajur_jawatan,맨위,skrol,전경색,배경색,탈출상태,parameter_VALUE[4],parameter_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Senarai[4];
static int Fokus=-1,출력결과,tertib_VALUE[4],pemasukan_COUNT,seret_VALUE=-1,seret_X,seret_Y;
static unsigned teknologi_maklumat_belum_selesai,단추들,meja_lihat,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_pemasukan;
static unsigned aksara_lebar(unsigned titik_kod){return titik_kod>=256?2:1;}
static void 사각영역(unsigned koordinat_x,unsigned Y_koordinat,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Papan_segi_empat_tepat_isi(koordinat_x,Y_koordinat,너비값,높이값,색상);
}
void Terminal_glif(unsigned koordinat_x,unsigned Y_koordinat,unsigned titik_kod,unsigned 전경색,unsigned 배경색){
    unsigned 너비=aksara_lebar(titik_kod)*8;if(titik_kod==0xffffffffu)return;
    int 왼쪽=koordinat_x,위쪽=Y_koordinat,폭=너비,kepanjangan_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&kepanjangan_VALUE))return;
    if(titik_kod==' '){Papan_segi_empat_tepat_isi(왼쪽,위쪽,폭,kepanjangan_VALUE,배경색);return;}
    unsigned Carian_INDEX=titik_kod<65536?titik_kod:titik_kod>=0x1f600&&titik_kod<0x1f650?65536+titik_kod-0x1f600:0xfffd;
    const unsigned char *fon_VALUE=Terminal_fon+Carian_INDEX*32;
    for(int baris=위쪽;baris<위쪽+kepanjangan_VALUE;baris++){unsigned Background_Intelligent_Transfer_Service_Senarai=fon_VALUE[(baris-Y_koordinat)*2]*256+fon_VALUE[(baris-Y_koordinat)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)Papan_pel(칸,baris,(Background_Intelligent_Transfer_Service_Senarai&(0x8000>>(칸-koordinat_x)))?전경색:배경색);}
}
static void nama_jadual(unsigned koordinat_x,unsigned Y_koordinat,const char *rentetan_data,unsigned 전경색,unsigned 배경색){while(*rentetan_data){unsigned titik_kod=(unsigned char)*rentetan_data++, 남은수=0;if(titik_kod>=0xc0){남은수=titik_kod<0xe0?1:titik_kod<0xf0?2:3;titik_kod&=(1u<<(6-남은수))-1;while(남은수--&&*rentetan_data)titik_kod=(titik_kod<<6)|((unsigned char)*rentetan_data++&63);}Terminal_glif(koordinat_x,Y_koordinat,titik_kod,전경색,배경색);koordinat_x+=aksara_lebar(titik_kod)*8;}}
static unsigned 첫항목(void){return Terminal_pemasukan->맨위;}
static int 보이는지(void){return Terminal_pemasukan->살아있음&&Fokus>=0&&Terminal_pemasukan==&Windows_Senarai[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ROW_jawatan,unsigned lajur_jawatan){
    if(!보이는지()||ROW_jawatan<첫항목()-Terminal_pemasukan->skrol||ROW_jawatan>=첫항목()-Terminal_pemasukan->skrol+Terminal_pemasukan->ROW_COUNT||lajur_jawatan>=Terminal_pemasukan->COLUMNS)return;
    unsigned titik_kod=Terminal_pemasukan->글자칸들[ROW_jawatan%Sejarah_baris_COUNT][lajur_jawatan],rentetan_data=Terminal_pemasukan->모양들[ROW_jawatan%Sejarah_baris_COUNT][lajur_jawatan];
    if(aksara_lebar(titik_kod)==2&&lajur_jawatan+1>=Terminal_pemasukan->COLUMNS)titik_kod=' ';
    Terminal_glif(Terminal_pemasukan->koordinat_x+12+lajur_jawatan*8,Terminal_pemasukan->Y_koordinat+36+(ROW_jawatan-첫항목()+Terminal_pemasukan->skrol)*16,titik_kod?titik_kod:' ',색상들[rentetan_data&15],색상들[rentetan_data>>4]);
}
static void karet_VALUE(int tayang_tetingkap){if(!보이는지()||Terminal_pemasukan->skrol||Terminal_pemasukan->lajur_jawatan>=Terminal_pemasukan->COLUMNS||Terminal_pemasukan->ROW_jawatan<Terminal_pemasukan->맨위||Terminal_pemasukan->ROW_jawatan>=Terminal_pemasukan->맨위+Terminal_pemasukan->ROW_COUNT)return;
    if(!tayang_tetingkap||!Terminal_pemasukan->가리개보임)그리기(Terminal_pemasukan->ROW_jawatan,Terminal_pemasukan->lajur_jawatan);else 사각영역(Terminal_pemasukan->koordinat_x+12+Terminal_pemasukan->lajur_jawatan*8,Terminal_pemasukan->Y_koordinat+36+(Terminal_pemasukan->ROW_jawatan-Terminal_pemasukan->맨위)*16+14,8,2,색상들[Terminal_pemasukan->전경색]);}
static void Kandungan_VALUE(void){
    사각영역(Terminal_pemasukan->koordinat_x+12,Terminal_pemasukan->Y_koordinat+36,Terminal_pemasukan->COLUMNS*8,Terminal_pemasukan->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_pemasukan->koordinat_x+12,Menegak_jawatan=Terminal_pemasukan->Y_koordinat+36,폭=Terminal_pemasukan->COLUMNS*8,kepanjangan_VALUE=Terminal_pemasukan->ROW_COUNT*16;
    if(보드그림범위(&가로,&Menegak_jawatan,&폭,&kepanjangan_VALUE)){
    unsigned 첫줄=(Menegak_jawatan-Terminal_pemasukan->Y_koordinat-36)/16,끝줄=(Menegak_jawatan+kepanjangan_VALUE-Terminal_pemasukan->Y_koordinat-36+15)/16;
    unsigned 첫칸=(가로-Terminal_pemasukan->koordinat_x-12)/8,끝칸=(가로+폭-Terminal_pemasukan->koordinat_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned titik_kod=첫칸;titik_kod<끝칸;titik_kod++){
        unsigned ROW_jawatan=첫항목()-Terminal_pemasukan->skrol+반환값,aksara_VALUE=Terminal_pemasukan->글자칸들[ROW_jawatan%Sejarah_baris_COUNT][titik_kod],rentetan_data=Terminal_pemasukan->모양들[ROW_jawatan%Sejarah_baris_COUNT][titik_kod];
        if(aksara_lebar(aksara_VALUE)==2&&titik_kod+1>=Terminal_pemasukan->COLUMNS)aksara_VALUE=' ';
        if((aksara_VALUE==0||aksara_VALUE==' ')&&(rentetan_data>>4)==0)continue;
        Terminal_glif(Terminal_pemasukan->koordinat_x+12+titik_kod*8,Terminal_pemasukan->Y_koordinat+36+반환값*16,aksara_VALUE?aksara_VALUE:' ',색상들[rentetan_data&15],색상들[rentetan_data>>4]);
    }}
    nama_jadual(Terminal_pemasukan->koordinat_x+12,Terminal_pemasukan->Y_koordinat+Terminal_pemasukan->높이-18,Terminal_pemasukan->skrol?"PgDn: recent output":Terminal_pemasukan->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);karet_VALUE(1);
}
static void 실행틀(int 식별자){
    Terminal_pemasukan=&Windows_Senarai[식별자];
    int 가로=Terminal_pemasukan->koordinat_x,Menegak_jawatan=Terminal_pemasukan->Y_koordinat,폭=Terminal_pemasukan->너비,kepanjangan_VALUE=Terminal_pemasukan->높이;
    if(!보드그림범위(&가로,&Menegak_jawatan,&폭,&kepanjangan_VALUE))return;
    사각영역(Terminal_pemasukan->koordinat_x,Terminal_pemasukan->Y_koordinat,Terminal_pemasukan->너비,Terminal_pemasukan->높이,0x403127);
    unsigned 색상=식별자==Fokus?0x905020:0x604438;사각영역(Terminal_pemasukan->koordinat_x,Terminal_pemasukan->Y_koordinat,Terminal_pemasukan->너비,30,색상);
    nama_jadual(Terminal_pemasukan->koordinat_x+12,Terminal_pemasukan->Y_koordinat+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+식별자),0};nama_jadual(Terminal_pemasukan->koordinat_x+148,Terminal_pemasukan->Y_koordinat+7,수치,0xffffff,색상);
    nama_jadual(Terminal_pemasukan->koordinat_x+240,Terminal_pemasukan->Y_koordinat+7,Terminal_pemasukan->너비>=500?(한글입력?"[MS] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[MS]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_pemasukan->koordinat_x+Terminal_pemasukan->너비-32,Terminal_pemasukan->Y_koordinat+4,26,22,0x5555b8);nama_jadual(Terminal_pemasukan->koordinat_x+Terminal_pemasukan->너비-24,Terminal_pemasukan->Y_koordinat+7,"X",0xffffff,0x5555b8);
    Kandungan_VALUE();
}
static void 장면그리기(void){
    if(!meja_lihat)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nama_jadual(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Senarai[순번].살아있음){unsigned titik_kod=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,titik_kod);nama_jadual(160+순번*112,8,"Terminal",0xffffff,titik_kod);char rentetan_data[2]={(char)('1'+순번),0};nama_jadual(232+순번*112,8,rentetan_data,0xffffff,titik_kod);}
    if(!pemasukan_COUNT)nama_jadual(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<pemasukan_COUNT;순번++)실행틀(tertib_VALUE[순번]);화면다시그림(Fokus);Terminal_pemasukan=&Windows_Senarai[출력결과];
}
static void Paint_rantau(int 가로,int Menegak_jawatan,int 폭,int kepanjangan_VALUE){
    if(!meja_lihat||!보드그림범위(&가로,&Menegak_jawatan,&폭,&kepanjangan_VALUE))return;
    for(int baris=Menegak_jawatan;baris<Menegak_jawatan+kepanjangan_VALUE;baris+=32){
        int 띠높이=Menegak_jawatan+kepanjangan_VALUE-baris;if(띠높이>32)띠높이=32;
        if(Papan_Mula_lukisan(가로,baris,폭,띠높이)){장면그리기();Papan_Tamat_lukisan();}
    }
}
static void 다시그리기(void){Paint_rantau(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Tetingkap 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Menegak_jawatan,int 폭,int kepanjangan_VALUE,Terminal_d413d4bc *Tetingkap){
    int 왼쪽=가로>(int)Tetingkap->koordinat_x?가로:(int)Tetingkap->koordinat_x;
    int 위쪽=Menegak_jawatan>(int)Tetingkap->Y_koordinat?Menegak_jawatan:(int)Tetingkap->Y_koordinat;
    int RIGHT=가로+폭<(int)(Tetingkap->koordinat_x+Tetingkap->너비)?가로+폭:(int)(Tetingkap->koordinat_x+Tetingkap->너비);
    int 아래쪽=Menegak_jawatan+kepanjangan_VALUE<(int)(Tetingkap->Y_koordinat+Tetingkap->높이)?Menegak_jawatan+kepanjangan_VALUE:(int)(Tetingkap->Y_koordinat+Tetingkap->높이);
    Paint_rantau(Tetingkap->koordinat_x,Tetingkap->Y_koordinat,Tetingkap->너비,Tetingkap->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){Paint_rantau(가로,Menegak_jawatan,폭,kepanjangan_VALUE);return;}
    Paint_rantau(가로,Menegak_jawatan,폭,위쪽-Menegak_jawatan);
    Paint_rantau(가로,아래쪽,폭,Menegak_jawatan+kepanjangan_VALUE-아래쪽);
    Paint_rantau(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_rantau(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void isyarat_Fokus(void){teknologi_maklumat_belum_selesai=(teknologi_maklumat_belum_selesai&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal_d413d4bc *tetingkap_pemasukan=&Windows_Senarai[Fokus];
        nama_jadual(tetingkap_pemasukan->koordinat_x+240,tetingkap_pemasukan->Y_koordinat+7,tetingkap_pemasukan->너비>=500?(한글입력?"[MS] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[MS]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int 식별자){if(식별자<0||식별자>=4||!Windows_Senarai[식별자].살아있음)return;int 현재위치=0;while(현재위치<pemasukan_COUNT&&tertib_VALUE[현재위치]!=식별자)현재위치++;for(;현재위치+1<pemasukan_COUNT;현재위치++)tertib_VALUE[현재위치]=tertib_VALUE[현재위치+1];tertib_VALUE[pemasukan_COUNT-1]=식별자;Fokus=식별자;isyarat_Fokus();다시그리기();}
static void kosong(unsigned ROW_jawatan){for(unsigned titik_kod=0;titik_kod<최대열수;titik_kod++){Terminal_pemasukan->글자칸들[ROW_jawatan%Sejarah_baris_COUNT][titik_kod]=0;Terminal_pemasukan->모양들[ROW_jawatan%Sejarah_baris_COUNT][titik_kod]=Terminal_pemasukan->전경색|(Terminal_pemasukan->배경색<<4);}}
static void buang_TOC(void){Terminal_pemasukan->ROW_jawatan=Terminal_pemasukan->lajur_jawatan=Terminal_pemasukan->맨위=Terminal_pemasukan->skrol=0;for(unsigned 반환값=0;반환값<Sejarah_baris_COUNT;반환값++)kosong(반환값);if(보이는지())Kandungan_VALUE();}
static int cipta_pemasukan(void){
    if(!보드화면기억공간())return -19;int 식별자=0;while(식별자<4&&Windows_Senarai[식별자].살아있음)식별자++;if(식별자==4)return -28;
    meja_lihat=1;Terminal_pemasukan=&Windows_Senarai[식별자];memset(Terminal_pemasukan,0,sizeof(*Terminal_pemasukan));Terminal_pemasukan->살아있음=1;Terminal_pemasukan->너비=568;Terminal_pemasukan->높이=360;Terminal_pemasukan->COLUMNS=68;Terminal_pemasukan->ROW_COUNT=19;Terminal_pemasukan->koordinat_x=12+식별자*16;Terminal_pemasukan->Y_koordinat=48+식별자*18;Terminal_pemasukan->전경색=7;Terminal_pemasukan->가리개보임=1;
    for(unsigned 반환값=0;반환값<Sejarah_baris_COUNT;반환값++)kosong(반환값);tertib_VALUE[pemasukan_COUNT++]=식별자;Fokus=식별자;teknologi_maklumat_belum_selesai|=1u<<(4+식별자);isyarat_Fokus();다시그리기();return 식별자+1;
}
static void Tutup_tetingkap(int 식별자){
    if(식별자<0||식별자>=4||!Windows_Senarai[식별자].살아있음)return;Windows_Senarai[식별자].살아있음=0;teknologi_maklumat_belum_selesai|=1u<<(8+식별자);
    int 현재위치=0;while(현재위치<pemasukan_COUNT&&tertib_VALUE[현재위치]!=식별자)현재위치++;for(;현재위치+1<pemasukan_COUNT;현재위치++)tertib_VALUE[현재위치]=tertib_VALUE[현재위치+1];pemasukan_COUNT--;
    if(Fokus==식별자)Fokus=pemasukan_COUNT?tertib_VALUE[pemasukan_COUNT-1]:-1;isyarat_Fokus();다시그리기();
}
static void 줄바꿈(void){Terminal_pemasukan->lajur_jawatan=0;Terminal_pemasukan->ROW_jawatan++;if(Terminal_pemasukan->ROW_jawatan>=Terminal_pemasukan->맨위+Terminal_pemasukan->ROW_COUNT){Terminal_pemasukan->맨위++;kosong(Terminal_pemasukan->ROW_jawatan);if(보이는지())Kandungan_VALUE();}}
static void titik_kod_451f2815(unsigned titik_kod){
    if(titik_kod==13){Terminal_pemasukan->lajur_jawatan=0;return;}if(titik_kod==10){줄바꿈();return;}if(titik_kod==8){if(Terminal_pemasukan->lajur_jawatan)Terminal_pemasukan->lajur_jawatan--;return;}
    if(titik_kod==9){unsigned item_COUNT=8-Terminal_pemasukan->lajur_jawatan%8;while(item_COUNT--)titik_kod_451f2815(' ');return;}if(titik_kod<32||titik_kod==127)return;
    unsigned 너비값=aksara_lebar(titik_kod);if(Terminal_pemasukan->lajur_jawatan+너비값>Terminal_pemasukan->COLUMNS)줄바꿈();
    if(Terminal_pemasukan->글자칸들[Terminal_pemasukan->ROW_jawatan%Sejarah_baris_COUNT][Terminal_pemasukan->lajur_jawatan]==0xffffffffu&&Terminal_pemasukan->lajur_jawatan){Terminal_pemasukan->글자칸들[Terminal_pemasukan->ROW_jawatan%Sejarah_baris_COUNT][Terminal_pemasukan->lajur_jawatan-1]=' ';그리기(Terminal_pemasukan->ROW_jawatan,Terminal_pemasukan->lajur_jawatan-1);}
    if(aksara_lebar(Terminal_pemasukan->글자칸들[Terminal_pemasukan->ROW_jawatan%Sejarah_baris_COUNT][Terminal_pemasukan->lajur_jawatan])==2&&Terminal_pemasukan->lajur_jawatan+1<Terminal_pemasukan->COLUMNS){Terminal_pemasukan->글자칸들[Terminal_pemasukan->ROW_jawatan%Sejarah_baris_COUNT][Terminal_pemasukan->lajur_jawatan+1]=' ';그리기(Terminal_pemasukan->ROW_jawatan,Terminal_pemasukan->lajur_jawatan+1);}
    Terminal_pemasukan->글자칸들[Terminal_pemasukan->ROW_jawatan%Sejarah_baris_COUNT][Terminal_pemasukan->lajur_jawatan]=titik_kod;Terminal_pemasukan->모양들[Terminal_pemasukan->ROW_jawatan%Sejarah_baris_COUNT][Terminal_pemasukan->lajur_jawatan]=Terminal_pemasukan->전경색|(Terminal_pemasukan->배경색<<4);
    if(너비값==2)Terminal_pemasukan->글자칸들[Terminal_pemasukan->ROW_jawatan%Sejarah_baris_COUNT][Terminal_pemasukan->lajur_jawatan+1]=0xffffffffu;
    그리기(Terminal_pemasukan->ROW_jawatan,Terminal_pemasukan->lajur_jawatan);Terminal_pemasukan->lajur_jawatan+=너비값;
}
static void pemegang_kawalan_jujukan(unsigned titik_kod){
    unsigned item_COUNT=Terminal_pemasukan->parameter_VALUE[0]?Terminal_pemasukan->parameter_VALUE[0]:1;
    if(titik_kod=='m')for(unsigned 순번=0;순번<=Terminal_pemasukan->parameter_INDEX;순번++){unsigned data_jawatan=Terminal_pemasukan->parameter_VALUE[순번];if(!data_jawatan){Terminal_pemasukan->전경색=7;Terminal_pemasukan->배경색=0;}if(data_jawatan==1&&Terminal_pemasukan->전경색<8)Terminal_pemasukan->전경색+=8;if(data_jawatan==7){unsigned 유지=Terminal_pemasukan->전경색;Terminal_pemasukan->전경색=Terminal_pemasukan->배경색;Terminal_pemasukan->배경색=유지;}if(data_jawatan>=30&&data_jawatan<=37)Terminal_pemasukan->전경색=data_jawatan-30;if(data_jawatan>=90&&data_jawatan<=97)Terminal_pemasukan->전경색=data_jawatan-90+8;if(data_jawatan>=40&&data_jawatan<=47)Terminal_pemasukan->배경색=data_jawatan-40;if(data_jawatan>=100&&data_jawatan<=107)Terminal_pemasukan->배경색=data_jawatan-100+8;if(data_jawatan==39)Terminal_pemasukan->전경색=7;if(data_jawatan==49)Terminal_pemasukan->배경색=0;}
    if(titik_kod=='J'&&(Terminal_pemasukan->parameter_VALUE[0]==2||Terminal_pemasukan->parameter_VALUE[0]==3))buang_TOC();
    if(titik_kod=='K'){unsigned 출발위치=Terminal_pemasukan->parameter_VALUE[0]==2?0:Terminal_pemasukan->lajur_jawatan,도착위치=Terminal_pemasukan->parameter_VALUE[0]==1?Terminal_pemasukan->lajur_jawatan+1:Terminal_pemasukan->COLUMNS;if(Terminal_pemasukan->parameter_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_pemasukan->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_pemasukan->ROW_jawatan%Sejarah_baris_COUNT,aksara_VALUE=Terminal_pemasukan->글자칸들[ROW_VALUE][순번],bentuk_VALUE=Terminal_pemasukan->전경색|(Terminal_pemasukan->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 fon_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(aksara_VALUE!=0&&aksara_VALUE!=' ')||Terminal_pemasukan->모양들[ROW_VALUE][순번]!=bentuk_VALUE;
        Terminal_pemasukan->글자칸들[ROW_VALUE][순번]=' ';Terminal_pemasukan->모양들[ROW_VALUE][순번]=bentuk_VALUE;
        if(바뀜)그리기(Terminal_pemasukan->ROW_jawatan,순번);
    }}
    if(titik_kod=='D')Terminal_pemasukan->lajur_jawatan=item_COUNT>Terminal_pemasukan->lajur_jawatan?0:Terminal_pemasukan->lajur_jawatan-item_COUNT;if(titik_kod=='C')Terminal_pemasukan->lajur_jawatan=Terminal_pemasukan->lajur_jawatan+item_COUNT>=Terminal_pemasukan->COLUMNS?Terminal_pemasukan->COLUMNS-1:Terminal_pemasukan->lajur_jawatan+item_COUNT;
    if(titik_kod=='G')Terminal_pemasukan->lajur_jawatan=item_COUNT>Terminal_pemasukan->COLUMNS?Terminal_pemasukan->COLUMNS-1:item_COUNT-1;if(titik_kod=='A')Terminal_pemasukan->ROW_jawatan=item_COUNT>Terminal_pemasukan->ROW_jawatan-Terminal_pemasukan->맨위?Terminal_pemasukan->맨위:Terminal_pemasukan->ROW_jawatan-item_COUNT;
    if(titik_kod=='B')Terminal_pemasukan->ROW_jawatan=Terminal_pemasukan->ROW_jawatan+item_COUNT>=Terminal_pemasukan->맨위+Terminal_pemasukan->ROW_COUNT?Terminal_pemasukan->맨위+Terminal_pemasukan->ROW_COUNT-1:Terminal_pemasukan->ROW_jawatan+item_COUNT;
    if(titik_kod=='H'||titik_kod=='f'){Terminal_pemasukan->ROW_jawatan=Terminal_pemasukan->맨위+(item_COUNT>Terminal_pemasukan->ROW_COUNT?Terminal_pemasukan->ROW_COUNT:item_COUNT)-1;unsigned koordinat_x=Terminal_pemasukan->parameter_VALUE[1]?Terminal_pemasukan->parameter_VALUE[1]:1;Terminal_pemasukan->lajur_jawatan=(koordinat_x>Terminal_pemasukan->COLUMNS?Terminal_pemasukan->COLUMNS:koordinat_x)-1;}
    if(titik_kod=='s'){Terminal_pemasukan->저장행=Terminal_pemasukan->ROW_jawatan;Terminal_pemasukan->저장열=Terminal_pemasukan->lajur_jawatan;}if(titik_kod=='u'){Terminal_pemasukan->ROW_jawatan=Terminal_pemasukan->저장행;Terminal_pemasukan->lajur_jawatan=Terminal_pemasukan->저장열<Terminal_pemasukan->COLUMNS?Terminal_pemasukan->저장열:Terminal_pemasukan->COLUMNS-1;}
    if((titik_kod=='h'||titik_kod=='l')&&Terminal_pemasukan->parameter_VALUE[0]==25)Terminal_pemasukan->가리개보임=titik_kod=='h';
}
void Terminal_bait(unsigned SECOND_VALUE){
    Terminal_pemasukan=&Windows_Senarai[출력결과];if(!Terminal_pemasukan->살아있음)return;karet_VALUE(0);if(Terminal_pemasukan->skrol){Terminal_pemasukan->skrol=0;if(보이는지())Kandungan_VALUE();}
    if(Terminal_pemasukan->탈출상태==1){Terminal_pemasukan->탈출상태=SECOND_VALUE=='['?2:0;Terminal_pemasukan->parameter_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_pemasukan->parameter_VALUE[순번]=0;}
    else if(Terminal_pemasukan->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_pemasukan->parameter_VALUE[Terminal_pemasukan->parameter_INDEX]<10000)Terminal_pemasukan->parameter_VALUE[Terminal_pemasukan->parameter_INDEX]=Terminal_pemasukan->parameter_VALUE[Terminal_pemasukan->parameter_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_pemasukan->parameter_INDEX<3)Terminal_pemasukan->parameter_INDEX++;else{pemegang_kawalan_jujukan(SECOND_VALUE);Terminal_pemasukan->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_pemasukan->긴부호없는값=0;Terminal_pemasukan->탈출상태=1;}else{
        if(Terminal_pemasukan->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_pemasukan->긴부호없는값=0;titik_kod_451f2815(0xfffd);}
        if(Terminal_pemasukan->긴부호없는값){Terminal_pemasukan->부호없는결과=Terminal_pemasukan->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_pemasukan->긴부호없는값==0)titik_kod_451f2815(Terminal_pemasukan->부호없는결과<Terminal_pemasukan->SMALL_VALUE||Terminal_pemasukan->부호없는결과>0x10ffff||(Terminal_pemasukan->부호없는결과>=0xd800&&Terminal_pemasukan->부호없는결과<=0xdfff)?0xfffd:Terminal_pemasukan->부호없는결과);}
        else if(SECOND_VALUE<128)titik_kod_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_pemasukan->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_pemasukan->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_pemasukan->긴부호없는값))-1);Terminal_pemasukan->SMALL_VALUE=Terminal_pemasukan->긴부호없는값==1?128:Terminal_pemasukan->긴부호없는값==2?2048:65536;}else titik_kod_451f2815(0xfffd);
    }karet_VALUE(1);
}
int Terminal_belum_selesai(void){return teknologi_maklumat_belum_selesai!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int saiz_semula_seret=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Menegak_jawatan) {
    for(int jujukan_VALUE=pemasukan_COUNT-1;jujukan_VALUE>=0;jujukan_VALUE--){
        int 식별자=tertib_VALUE[jujukan_VALUE];Terminal_d413d4bc *Tetingkap=&Windows_Senarai[식별자];
        if(가로>=(int)Tetingkap->koordinat_x&&Menegak_jawatan>=(int)Tetingkap->Y_koordinat&&
           가로<(int)(Tetingkap->koordinat_x+Tetingkap->너비)&&Menegak_jawatan<(int)(Tetingkap->Y_koordinat+Tetingkap->높이))return 식별자;
    }return -1;
}
static int 모서리찾기(int 식별자,int 가로,int Menegak_jawatan) {
    if(식별자<0)return 0;Terminal_d413d4bc *Tetingkap=&Windows_Senarai[식별자];
    int 왼쪽=가로<(int)Tetingkap->koordinat_x+8,RIGHT=가로>=(int)(Tetingkap->koordinat_x+Tetingkap->너비)-8;
    int 위쪽=Menegak_jawatan<(int)Tetingkap->Y_koordinat+8,아래쪽=Menegak_jawatan>=(int)(Tetingkap->Y_koordinat+Tetingkap->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int pemisah_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void alih_saiz_semula(int 가로,int Menegak_jawatan) {
    Terminal_d413d4bc *Tetingkap=&Windows_Senarai[saiz_semula_seret];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=pemisah_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=pemisah_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=pemisah_VALUE(처음세로+Menegak_jawatan-잡은세로,34,아래쪽-216);
    else 아래쪽=pemisah_VALUE(처음세로+처음높이+Menegak_jawatan-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(Tetingkap->COLUMNS!=COLUMNS||Tetingkap->ROW_COUNT!=ROW_COUNT){
        Tetingkap->크기바뀜=1;Tetingkap->COLUMNS=COLUMNS;Tetingkap->ROW_COUNT=ROW_COUNT;
        if(Tetingkap->lajur_jawatan>=COLUMNS)Tetingkap->lajur_jawatan=COLUMNS-1;
        if(Tetingkap->ROW_jawatan>=Tetingkap->맨위+ROW_COUNT)Tetingkap->맨위=Tetingkap->ROW_jawatan-ROW_COUNT+1;
        unsigned 한도=Tetingkap->맨위;if(한도>Sejarah_baris_COUNT-ROW_COUNT)한도=Sejarah_baris_COUNT-ROW_COUNT;
        if(Tetingkap->skrol>한도)Tetingkap->skrol=한도;
    }
    int 옛가로=Tetingkap->koordinat_x,옛세로=Tetingkap->Y_koordinat,옛폭=Tetingkap->너비,옛길이=Tetingkap->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    Tetingkap->koordinat_x=왼쪽;Tetingkap->Y_koordinat=위쪽;Tetingkap->너비=RIGHT-왼쪽;Tetingkap->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Tetingkap);
}
void Terminal_penuding(unsigned Seterusnya_item,int koordinat_x,int Y_koordinat){
    unsigned 눌림=Seterusnya_item&~단추들;단추들=Seterusnya_item;
    if(!meja_lihat){seret_VALUE=-1;saiz_semula_seret=-1;Papan_penuding(koordinat_x,Y_koordinat,1);return;}
    if(!(Seterusnya_item&1)){seret_VALUE=-1;saiz_semula_seret=-1;}
    if(saiz_semula_seret>=0&&!Windows_Senarai[saiz_semula_seret].살아있음)saiz_semula_seret=-1;
    if(seret_VALUE>=0&&!Windows_Senarai[seret_VALUE].살아있음)seret_VALUE=-1;
    if(saiz_semula_seret>=0){
        alih_saiz_semula(koordinat_x,Y_koordinat);Papan_penuding(koordinat_x,Y_koordinat,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Papan_penuding(koordinat_x,Y_koordinat,1);
    if(seret_VALUE>=0){
        Terminal_d413d4bc *Tetingkap=&Windows_Senarai[seret_VALUE];
        int 옛가로=Tetingkap->koordinat_x,옛세로=Tetingkap->Y_koordinat;
        Tetingkap->koordinat_x=pemisah_VALUE(koordinat_x-seret_X,0,보드화면너비()-Tetingkap->너비);
        Tetingkap->Y_koordinat=pemisah_VALUE(Y_koordinat-seret_Y,34,보드화면높이()-Tetingkap->높이);
        if(옛가로!=(int)Tetingkap->koordinat_x||옛세로!=(int)Tetingkap->Y_koordinat)창자리그리기(옛가로,옛세로,Tetingkap->너비,Tetingkap->높이,Tetingkap);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,koordinat_x,Y_koordinat)){화면가리킴(Fokus,눌림,koordinat_x,Y_koordinat);return;}
    int 식별자=가리킨창(koordinat_x,Y_koordinat),모서리=모서리찾기(식별자,koordinat_x,Y_koordinat);
    if(모서리)Papan_penuding(koordinat_x,Y_koordinat,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *Tetingkap=&Windows_Senarai[식별자];saiz_semula_seret=식별자;잡은모서리=모서리;잡은가로=koordinat_x;잡은세로=Y_koordinat;
            처음가로=Tetingkap->koordinat_x;처음세로=Tetingkap->Y_koordinat;처음너비=Tetingkap->너비;처음높이=Tetingkap->높이;
            if(식별자!=Fokus)앞으로올리기(식별자);return;
        }
        if(Y_koordinat<32&&koordinat_x>=6&&koordinat_x<142){cipta_pemasukan();return;}
        if(Y_koordinat<32&&koordinat_x>=154&&koordinat_x<602){앞으로올리기((koordinat_x-154)/112);return;}
        if(식별자>=0){
            Terminal_d413d4bc *Tetingkap=&Windows_Senarai[식별자];
            if(Y_koordinat<(int)Tetingkap->Y_koordinat+30&&koordinat_x>=(int)(Tetingkap->koordinat_x+Tetingkap->너비)-32){Tutup_tetingkap(식별자);return;}
            if(식별자!=Fokus)앞으로올리기(식별자);
            if(Y_koordinat<(int)Tetingkap->Y_koordinat+30){seret_VALUE=식별자;seret_X=koordinat_x-Tetingkap->koordinat_x;seret_Y=Y_koordinat-Tetingkap->Y_koordinat;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_pemasukan=&Windows_Senarai[Fokus];if(눌림&8){unsigned 한도=Terminal_pemasukan->맨위;if(한도>Sejarah_baris_COUNT-Terminal_pemasukan->ROW_COUNT)한도=Sejarah_baris_COUNT-Terminal_pemasukan->ROW_COUNT;Terminal_pemasukan->skrol=Terminal_pemasukan->skrol+9>한도?한도:Terminal_pemasukan->skrol+9;}else Terminal_pemasukan->skrol=Terminal_pemasukan->skrol<9?0:Terminal_pemasukan->skrol-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)cipta_pemasukan();if(누름값==2&&pemasukan_COUNT)앞으로올리기(tertib_VALUE[0]);if(누름값==3)Tutup_tetingkap(Fokus);}
mesin_Word Papan_Terminal(mesin_Word Aksi){
    if(Aksi==300){if(!Windows_Senarai[출력결과].살아있음)return cipta_pemasukan();meja_lihat=1;다시그리기();return 0;}
    if(Aksi==0){Tutup_tetingkap(Fokus);return 0;}if(Aksi==1)return (uint32_t)cipta_pemasukan();if(Aksi==2)return Fokus>=0;
    if(Aksi==9){meja_lihat=0;return 0;}if(Aksi==7)return pemasukan_COUNT;if(Aksi==10)return Fokus+1;if(Aksi==11)return 출력결과;
    if(Aksi==13){Terminal_d413d4bc *Tetingkap=&Windows_Senarai[출력결과];return Tetingkap->살아있음?(Tetingkap->ROW_COUNT<<16)|Tetingkap->COLUMNS:(19<<16)|68;}
    if(Aksi==14){unsigned VALUE=Windows_Senarai[출력결과].크기바뀜;Windows_Senarai[출력결과].크기바뀜=0;return VALUE;}
    if(Aksi==12){unsigned VALUE=teknologi_maklumat_belum_selesai;teknologi_maklumat_belum_selesai=0;return VALUE;}
    if(Aksi>=20&&Aksi<24)return Windows_Senarai[Aksi-20].살아있음;
    if(Aksi>=100&&Aksi<104){출력결과=Aksi-100;Terminal_pemasukan=&Windows_Senarai[출력결과];return 0;}
    if(Aksi>=200&&Aksi<204){앞으로올리기(Aksi-200);return 0;}
    if(Aksi==3){다시그리기();return 0;}Terminal_pemasukan=&Windows_Senarai[출력결과];if(!Terminal_pemasukan->살아있음)return 0;
    if(Aksi==4)buang_TOC();if(Aksi==5||Aksi==6){unsigned 이전=단추들;Terminal_penuding(Aksi==5?8:16,0,0);단추들=이전;}return 1;
}
