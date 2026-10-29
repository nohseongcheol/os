/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Kapcsolódás, 제한된 bevitel_ÉRTÉK hossz_ÉRTÉK, 비동기 küld_ÉRTÉK, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 adat 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "távoli_ÉRTÉK.h"
#include "kriptográfia_támogat.h"
#include "Profil.h"
#include "../hálózat_Sor/hálózat_Sor.h"
#include "../gép/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t fal_Terminál(uintptr_t);
void távoli_Kulcs_tollvonás(unsigned,int);
void inicializál_távoli_Kulcs_tollvonás(void);
void véglegesít_távoli_Kulcs(void);
static int Hallgatás_végpont=-1,társ_ÉRTÉK=-1,fázis_ÉRTÉK,닫을예정;
static uintptr_t ismerős_IDŐ,다시받을때;
static unsigned char bevitel_ÉRTÉK[8192],Kimenet[4096],kihívás_ÉRTÉK[16];
static unsigned bevitel_DARAB,kimenet_DARAB,보낸수;
static unsigned 너비,높이,képpont_méretez=4,csökkenő_helyiértékű_ÉRTÉK,빨강최대=255,초록최대=255,파랑최대=255,piros_eltol=16,zöld_eltol=8,kék_eltol;
static uint32_t Előző_összegzés[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned csempe_DARAB,csempe_pozíció,igényelt_X,igényelt_Y,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *adat_pozíció){return(unsigned)adat_pozíció[0]*256+adat_pozíció[1];}
static uint32_t 읽기32(const unsigned char *adat_pozíció){return(uint32_t)adat_pozíció[0]<<24|(uint32_t)adat_pozíció[1]<<16|(uint32_t)adat_pozíció[2]<<8|adat_pozíció[3];}
static void ír_16(unsigned char *adat_pozíció,unsigned ÉRTÉK){adat_pozíció[0]=ÉRTÉK>>8;adat_pozíció[1]=ÉRTÉK;}
static void ír_32(unsigned char *adat_pozíció,uint32_t ÉRTÉK){adat_pozíció[0]=ÉRTÉK>>24;adat_pozíció[1]=ÉRTÉK>>16;adat_pozíció[2]=ÉRTÉK>>8;adat_pozíció[3]=ÉRTÉK;}
static void Bezárás(void){if(társ_ÉRTÉK>=0)bezár_hálózat(társ_ÉRTÉK);társ_ÉRTÉK=-1;fázis_ÉRTÉK=0;bevitel_DARAB=kimenet_DARAB=보낸수=0;csempe_DARAB=csempe_pozíció=0;닫을예정=0;inicializál_távoli_Kulcs_tollvonás();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *adat,unsigned szám){memcpy(Kimenet,adat,szám);kimenet_DARAB=szám;보낸수=0;}
static void felhasznál_ÉRTÉK(unsigned szám){bevitel_DARAB-=szám;memmove(bevitel_ÉRTÉK,bevitel_ÉRTÉK+szám,bevitel_DARAB);}
int vezérlő_távoli_kijelző(unsigned Művelet){
    if(Művelet==0){Bezárás();if(Hallgatás_végpont>=0)bezár_hálózat(Hallgatás_végpont);Hallgatás_végpont=-1;return 0;}
    if(Művelet!=1)return Hallgatás_végpont>=0;
    if(Hallgatás_végpont>=0)return 0;
    int port_ÉRTÉK=készít_szoftvercsatorna_végpont(1);if(port_ÉRTÉK<0)return port_ÉRTÉK;통신주소재사용(port_ÉRTÉK);
    int KR=NET_BIND(port_ÉRTÉK,0,5900);if(!KR)KR=NET_figyelés(port_ÉRTÉK);
    if(KR<0){bezár_hálózat(port_ÉRTÉK);return KR;}Hallgatás_végpont=port_ÉRTÉK;return 0;
}
static uint32_t csempe_összegzés(unsigned 가로,unsigned szektor_pozíció){
    uint32_t ÉRTÉK=2166136261u;
    for(unsigned Y_koordináta=szektor_pozíció;Y_koordináta<szektor_pozíció+16&&Y_koordináta<높이;Y_koordináta++)for(unsigned x_koordináta=가로;x_koordináta<가로+32&&x_koordináta<너비;x_koordináta++)ÉRTÉK=(ÉRTÉK^보드화면읽기(x_koordináta,Y_koordináta))*16777619u;
    return ÉRTÉK;
}
static void 화면요청(const unsigned char *adat_pozíció){
    igényelt_X=읽기16(adat_pozíció+2);igényelt_Y=읽기16(adat_pozíció+4);요청폭=읽기16(adat_pozíció+6);요청높이=읽기16(adat_pozíció+8);
    if(igényelt_X>=너비||igényelt_Y>=높이)요청폭=요청높이=0;
    if(요청폭>너비-igényelt_X&&igényelt_X<너비)요청폭=너비-igényelt_X;
    if(요청높이>높이-igényelt_Y&&igényelt_Y<높이)요청높이=높이-igényelt_Y;
    csempe_DARAB=csempe_pozíció=0;
    if(요청폭&&요청높이)for(unsigned Y_koordináta=igényelt_Y/16;Y_koordináta<=(igényelt_Y+요청높이-1)/16;Y_koordináta++)for(unsigned x_koordináta=igényelt_X/32;x_koordináta<=(igényelt_X+요청폭-1)/32;x_koordináta++){
        unsigned helyzetindex=Y_koordináta*60+x_koordináta;uint32_t összegzés_ÉRTÉK=csempe_összegzés(x_koordináta*32,Y_koordináta*16);
        if(!adat_pozíció[1]||Előző_összegzés[helyzetindex]!=összegzés_ÉRTÉK)바뀐타일[csempe_DARAB++]=helyzetindex;
    }
    Kimenet[0]=Kimenet[1]=0;ír_16(Kimenet+2,csempe_DARAB);kimenet_DARAB=4;보낸수=0;
}
static void küld_csempe(void){
    unsigned helyzetindex=바뀐타일[csempe_pozíció++],가로=(helyzetindex%60)*32,szektor_pozíció=(helyzetindex/60)*16;
    unsigned megszüntet_X=가로+32,megszüntet_Y=szektor_pozíció+16;if(megszüntet_X>너비)megszüntet_X=너비;if(megszüntet_Y>높이)megszüntet_Y=높이;
    /* 부분 타일 kérés 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=igényelt_X&&szektor_pozíció>=igényelt_Y&&megszüntet_X<=igényelt_X+요청폭&&megszüntet_Y<=igényelt_Y+요청높이;
    if(전부)Előző_összegzés[helyzetindex]=csempe_összegzés(가로,szektor_pozíció);
    if(가로<igényelt_X)가로=igényelt_X;if(szektor_pozíció<igényelt_Y)szektor_pozíció=igényelt_Y;
    if(megszüntet_X>igényelt_X+요청폭)megszüntet_X=igényelt_X+요청폭;if(megszüntet_Y>igényelt_Y+요청높이)megszüntet_Y=igényelt_Y+요청높이;
    ír_16(Kimenet,가로);ír_16(Kimenet+2,szektor_pozíció);ír_16(Kimenet+4,megszüntet_X-가로);ír_16(Kimenet+6,megszüntet_Y-szektor_pozíció);ír_32(Kimenet+8,0);
    kimenet_DARAB=12;보낸수=0;
    for(unsigned Y_koordináta=szektor_pozíció;Y_koordináta<megszüntet_Y;Y_koordináta++)for(unsigned x_koordináta=가로;x_koordináta<megszüntet_X;x_koordináta++){
        uint32_t 색=보드화면읽기(x_koordináta,Y_koordináta),ÉRTÉK=(((색>>16)&255)*빨강최대/255)<<piros_eltol|
            (((색>>8)&255)*초록최대/255)<<zöld_eltol|((색&255)*파랑최대/255)<<kék_eltol;
        for(unsigned 순번=0;순번<képpont_méretez;순번++)Kimenet[kimenet_DARAB++]=ÉRTÉK>>(8*(csökkenő_helyiértékű_ÉRTÉK?képpont_méretez-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Hallgatás_végpont<0)return;
    if(társ_ÉRTÉK<0){if(보드밀리초()<다시받을때)return;társ_ÉRTÉK=NET_elfogad(Hallgatás_végpont);if(társ_ÉRTÉK<0)return;
        ismerős_IDŐ=보드밀리초();fázis_ÉRTÉK=1;내보내기("RFB 003.008\n",12);memset(Előző_összegzés,0,sizeof(Előző_összegzés));
        képpont_méretez=4;csökkenő_helyiértékű_ÉRTÉK=0;빨강최대=초록최대=파랑최대=255;piros_eltol=16;zöld_eltol=8;kék_eltol=0;}
    if(fázis_ÉRTÉK<5&&보드밀리초()-ismerős_IDŐ>15000){Bezárás();return;}
    if(kimenet_DARAB){int szám=NET_ír(társ_ÉRTÉK,Kimenet+보낸수,kimenet_DARAB-보낸수);if(szám>0){보낸수+=szám;if(보낸수==kimenet_DARAB)kimenet_DARAB=보낸수=0;}else if(szám!=-11){Bezárás();return;}}
    if(!kimenet_DARAB&&닫을예정){Bezárás();return;}
    if(!kimenet_DARAB&&csempe_pozíció<csempe_DARAB)küld_csempe();
    if(bevitel_DARAB==sizeof(bevitel_ÉRTÉK)){Bezárás();return;}
    int KAPOTT_DARAB=통신읽기(társ_ÉRTÉK,bevitel_ÉRTÉK+bevitel_DARAB,sizeof(bevitel_ÉRTÉK)-bevitel_DARAB);
    if(KAPOTT_DARAB==0||(KAPOTT_DARAB<0&&KAPOTT_DARAB!=-11)){Bezárás();return;}if(KAPOTT_DARAB>0)bevitel_DARAB+=KAPOTT_DARAB;
    if(kimenet_DARAB||csempe_pozíció<csempe_DARAB)return;
    if(fázis_ÉRTÉK==1&&bevitel_DARAB>=12){if(memcmp(bevitel_ÉRTÉK,"RFB 003.008\n",12)){Bezárás();return;}felhasznál_ÉRTÉK(12);const unsigned char hitelesítési_módszer[]={1,2};내보내기(hitelesítési_módszer,2);fázis_ÉRTÉK=2;return;}
    if(fázis_ÉRTÉK==2&&bevitel_DARAB){if(bevitel_ÉRTÉK[0]!=2||távoli_véletlenszerű(kihívás_ÉRTÉK,16)){Bezárás();return;}felhasznál_ÉRTÉK(1);내보내기(kihívás_ÉRTÉK,16);fázis_ÉRTÉK=3;return;}
    if(fázis_ÉRTÉK==3&&bevitel_DARAB>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys jelszó_ÉRTÉK;
        for(unsigned 순번=0;순번<8;순번++){unsigned ÉRTÉK=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(ÉRTÉK&1);ÉRTÉK>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&jelszó_ÉRTÉK,열쇠,8);memcpy(정답,kihívás_ÉRTÉK,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_ÉRTÉK[8]={0};br_des_ct_cbcenc_run(&jelszó_ÉRTÉK,vektor_ÉRTÉK,정답+순번,8);memset(vektor_ÉRTÉK,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^bevitel_ÉRTÉK[순번];felhasznál_ÉRTÉK(16);memset(&jelszó_ÉRTÉK,0,sizeof(jelszó_ÉRTÉK));memset(열쇠,0,8);memset(정답,0,16);memset(kihívás_ÉRTÉK,0,16);
        ír_32(Kimenet,차이?1:0);kimenet_DARAB=4;보낸수=0;
        if(차이){ír_32(Kimenet+4,19);memcpy(Kimenet+8,"Authentication fail",19);kimenet_DARAB=27;닫을예정=1;}else fázis_ÉRTÉK=4;return;}
    if(fázis_ÉRTÉK==4&&bevitel_DARAB){felhasznál_ÉRTÉK(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Bezárás();return;}
        if(!fal_Terminál(7)){const unsigned char Esemény[]={30,2,1,0,0,0,0};csatorna_távoli_bevitel(Esemény,7);}
        memset(Kimenet,0,40);ír_16(Kimenet,너비);ír_16(Kimenet+2,높이);Kimenet[4]=32;Kimenet[5]=24;Kimenet[7]=1;
        ír_16(Kimenet+8,255);ír_16(Kimenet+10,255);ír_16(Kimenet+12,255);Kimenet[14]=16;Kimenet[15]=8;
        const char *Név="jkoros native";ír_32(Kimenet+20,strlen(Név));memcpy(Kimenet+24,Név,strlen(Név));kimenet_DARAB=24+strlen(Név);보낸수=0;fázis_ÉRTÉK=5;return;}
    if(fázis_ÉRTÉK!=5||!bevitel_DARAB)return;
    unsigned beír_terület=bevitel_ÉRTÉK[0],필요=beír_terület==0?20:beír_terület==2?4:beír_terület==3?10:beír_terület==4?8:beír_terület==5?6:beír_terület==6?8:0;
    if(!필요){Bezárás();return;}if(bevitel_DARAB<필요)return;
    if(beír_terület==2){unsigned szám=읽기16(bevitel_ÉRTÉK+2);if(szám>128){Bezárás();return;}필요+=szám*4;}
    if(beír_terület==6){unsigned szám=읽기32(bevitel_ÉRTÉK+4);if(szám>4096){Bezárás();return;}필요+=szám;}
    if(bevitel_DARAB<필요)return;
    if(beír_terület==0){unsigned bit_ÉRTÉK=bevitel_ÉRTÉK[4],빨=읽기16(bevitel_ÉRTÉK+8),초=읽기16(bevitel_ÉRTÉK+10),파=읽기16(bevitel_ÉRTÉK+12),piros_Csatorna_eltol=bevitel_ÉRTÉK[14],zöld_Csatorna_eltol=bevitel_ÉRTÉK[15],kék_Csatorna_eltol=bevitel_ÉRTÉK[16];
        if((bit_ÉRTÉK!=16&&bit_ÉRTÉK!=32)||!bevitel_ÉRTÉK[7]||bevitel_ÉRTÉK[6]>1||!빨||!초||!파||빨>255||초>255||파>255||piros_Csatorna_eltol>24||zöld_Csatorna_eltol>24||kék_Csatorna_eltol>24||
           ((uint64_t)빨<<piros_Csatorna_eltol)>((1ull<<bit_ÉRTÉK)-1)||((uint64_t)초<<zöld_Csatorna_eltol)>((1ull<<bit_ÉRTÉK)-1)||((uint64_t)파<<kék_Csatorna_eltol)>((1ull<<bit_ÉRTÉK)-1)){Bezárás();return;}
        képpont_méretez=bit_ÉRTÉK/8;csökkenő_helyiértékű_ÉRTÉK=bevitel_ÉRTÉK[6];빨강최대=빨;초록최대=초;파랑최대=파;piros_eltol=piros_Csatorna_eltol;zöld_eltol=zöld_Csatorna_eltol;kék_eltol=kék_Csatorna_eltol;memset(Előző_összegzés,0,sizeof(Előző_összegzés));
    }else if(beír_terület==3)화면요청(bevitel_ÉRTÉK);
    else if(beír_terület==4)távoli_Kulcs_tollvonás(읽기32(bevitel_ÉRTÉK+4),bevitel_ÉRTÉK[1]!=0);
    else if(beír_terület==5){unsigned x_koordináta=읽기16(bevitel_ÉRTÉK+2),Y_koordináta=읽기16(bevitel_ÉRTÉK+4);if(x_koordináta>=너비)x_koordináta=너비-1;if(Y_koordináta>=높이)Y_koordináta=높이-1;
        if(bevitel_ÉRTÉK[1])véglegesít_távoli_Kulcs();
        unsigned char Esemény[]={30,1,bevitel_ÉRTÉK[1],x_koordináta&255,x_koordináta>>8,Y_koordináta&255,Y_koordináta>>8};csatorna_távoli_bevitel(Esemény,sizeof(Esemény));}
    felhasznál_ÉRTÉK(필요);
}
