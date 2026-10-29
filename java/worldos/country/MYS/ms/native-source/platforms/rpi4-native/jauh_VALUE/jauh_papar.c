/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Sambung, 제한된 입력 kepanjangan_VALUE, 비동기 e_mel_VALUE_f993dacd, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "jauh_VALUE.h"
#include "kriptografi_Sokongan.h"
#include "Profil.h"
#include "../rangkaian_tindan/rangkaian_tindan.h"
#include "../mesin/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Papan_Terminal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void lakukan_jauh_Kunci(void);
static int Mendengar_peserta=-1,rakan_VALUE=-1,pentas_VALUE,닫을예정;
static uintptr_t hubungan_TIME,다시받을때;
static unsigned char 입력[8192],출력[4096],cabaran_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,pel_saiz=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,merah_anjak=16,hijau_anjak=8,biru_anjak;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned jubin_COUNT,jubin_jawatan,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *data_jawatan){return(unsigned)data_jawatan[0]*256+data_jawatan[1];}
static uint32_t 읽기32(const unsigned char *data_jawatan){return(uint32_t)data_jawatan[0]<<24|(uint32_t)data_jawatan[1]<<16|(uint32_t)data_jawatan[2]<<8|data_jawatan[3];}
static void tulis_16(unsigned char *data_jawatan,unsigned VALUE){data_jawatan[0]=VALUE>>8;data_jawatan[1]=VALUE;}
static void tulis_32(unsigned char *data_jawatan,uint32_t VALUE){data_jawatan[0]=VALUE>>24;data_jawatan[1]=VALUE>>16;data_jawatan[2]=VALUE>>8;data_jawatan[3]=VALUE;}
static void Tutup(void){if(rakan_VALUE>=0)Tutup_rangkaian(rakan_VALUE);rakan_VALUE=-1;pentas_VALUE=0;입력수=출력수=보낸수=0;jubin_COUNT=jubin_jawatan=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned 수){memcpy(출력,data,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int kawalan_jauh_papar(unsigned Aksi){
    if(Aksi==0){Tutup();if(Mendengar_peserta>=0)Tutup_rangkaian(Mendengar_peserta);Mendengar_peserta=-1;return 0;}
    if(Aksi!=1)return Mendengar_peserta>=0;
    if(Mendengar_peserta>=0)return 0;
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int ukuran=망주소묶기(port_VALUE,0,5900);if(!ukuran)ukuran=연결기다리기(port_VALUE);
    if(ukuran<0){Tutup_rangkaian(port_VALUE);return ukuran;}Mendengar_peserta=port_VALUE;return 0;
}
static uint32_t jubin_ringkasan(unsigned 가로,unsigned Menegak_jawatan){
    uint32_t VALUE=2166136261u;
    for(unsigned Y_koordinat=Menegak_jawatan;Y_koordinat<Menegak_jawatan+16&&Y_koordinat<높이;Y_koordinat++)for(unsigned koordinat_x=가로;koordinat_x<가로+32&&koordinat_x<너비;koordinat_x++)VALUE=(VALUE^보드화면읽기(koordinat_x,Y_koordinat))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *data_jawatan){
    요청가로=읽기16(data_jawatan+2);요청세로=읽기16(data_jawatan+4);요청폭=읽기16(data_jawatan+6);요청높이=읽기16(data_jawatan+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    jubin_COUNT=jubin_jawatan=0;
    if(요청폭&&요청높이)for(unsigned Y_koordinat=요청세로/16;Y_koordinat<=(요청세로+요청높이-1)/16;Y_koordinat++)for(unsigned koordinat_x=요청가로/32;koordinat_x<=(요청가로+요청폭-1)/32;koordinat_x++){
        unsigned jawatan_INDEX=Y_koordinat*60+koordinat_x;uint32_t ringkasan_VALUE=jubin_ringkasan(koordinat_x*32,Y_koordinat*16);
        if(!data_jawatan[1]||지난요약[jawatan_INDEX]!=ringkasan_VALUE)바뀐타일[jubin_COUNT++]=jawatan_INDEX;
    }
    출력[0]=출력[1]=0;tulis_16(출력+2,jubin_COUNT);출력수=4;보낸수=0;
}
static void e_mel_jubin(void){
    unsigned jawatan_INDEX=바뀐타일[jubin_jawatan++],가로=(jawatan_INDEX%60)*32,Menegak_jawatan=(jawatan_INDEX/60)*16;
    unsigned tamat_X=가로+32,tamat_Y=Menegak_jawatan+16;if(tamat_X>너비)tamat_X=너비;if(tamat_Y>높이)tamat_Y=높이;
    /* 부분 타일 permintaan 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Menegak_jawatan>=요청세로&&tamat_X<=요청가로+요청폭&&tamat_Y<=요청세로+요청높이;
    if(전부)지난요약[jawatan_INDEX]=jubin_ringkasan(가로,Menegak_jawatan);
    if(가로<요청가로)가로=요청가로;if(Menegak_jawatan<요청세로)Menegak_jawatan=요청세로;
    if(tamat_X>요청가로+요청폭)tamat_X=요청가로+요청폭;if(tamat_Y>요청세로+요청높이)tamat_Y=요청세로+요청높이;
    tulis_16(출력,가로);tulis_16(출력+2,Menegak_jawatan);tulis_16(출력+4,tamat_X-가로);tulis_16(출력+6,tamat_Y-Menegak_jawatan);tulis_32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned Y_koordinat=Menegak_jawatan;Y_koordinat<tamat_Y;Y_koordinat++)for(unsigned koordinat_x=가로;koordinat_x<tamat_X;koordinat_x++){
        uint32_t 색=보드화면읽기(koordinat_x,Y_koordinat),VALUE=(((색>>16)&255)*빨강최대/255)<<merah_anjak|
            (((색>>8)&255)*초록최대/255)<<hijau_anjak|((색&255)*파랑최대/255)<<biru_anjak;
        for(unsigned 순번=0;순번<pel_saiz;순번++)출력[출력수++]=VALUE>>(8*(큰끝?pel_saiz-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Mendengar_peserta<0)return;
    if(rakan_VALUE<0){if(보드밀리초()<다시받을때)return;rakan_VALUE=망연결받기(Mendengar_peserta);if(rakan_VALUE<0)return;
        hubungan_TIME=보드밀리초();pentas_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        pel_saiz=4;큰끝=0;빨강최대=초록최대=파랑최대=255;merah_anjak=16;hijau_anjak=8;biru_anjak=0;}
    if(pentas_VALUE<5&&보드밀리초()-hubungan_TIME>15000){Tutup();return;}
    if(출력수){int 수=통신쓰기(rakan_VALUE,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Tutup();return;}}
    if(!출력수&&닫을예정){Tutup();return;}
    if(!출력수&&jubin_jawatan<jubin_COUNT)e_mel_jubin();
    if(입력수==sizeof(입력)){Tutup();return;}
    int RECEIVED_COUNT=통신읽기(rakan_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Tutup();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||jubin_jawatan<jubin_COUNT)return;
    if(pentas_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Tutup();return;}소비(12);const unsigned char kaedah_pengesahan[]={1,2};내보내기(kaedah_pengesahan,2);pentas_VALUE=2;return;}
    if(pentas_VALUE==2&&입력수){if(입력[0]!=2||jauh_rawak(cabaran_VALUE,16)){Tutup();return;}소비(1);내보내기(cabaran_VALUE,16);pentas_VALUE=3;return;}
    if(pentas_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys kata_laluan_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&kata_laluan_VALUE,열쇠,8);memcpy(정답,cabaran_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_VALUE[8]={0};br_des_ct_cbcenc_run(&kata_laluan_VALUE,vektor_VALUE,정답+순번,8);memset(vektor_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&kata_laluan_VALUE,0,sizeof(kata_laluan_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(cabaran_VALUE,0,16);
        tulis_32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){tulis_32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else pentas_VALUE=4;return;}
    if(pentas_VALUE==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Tutup();return;}
        if(!Papan_Terminal(7)){const unsigned char Peristiwa[]={30,2,1,0,0,0,0};원격입력넣기(Peristiwa,7);}
        memset(출력,0,40);tulis_16(출력,너비);tulis_16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        tulis_16(출력+8,255);tulis_16(출력+10,255);tulis_16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *Nama="jkoros native";tulis_32(출력+20,strlen(Nama));memcpy(출력+24,Nama,strlen(Nama));출력수=24+strlen(Nama);보낸수=0;pentas_VALUE=5;return;}
    if(pentas_VALUE!=5||!입력수)return;
    unsigned TYPE_bidang=입력[0],필요=TYPE_bidang==0?20:TYPE_bidang==2?4:TYPE_bidang==3?10:TYPE_bidang==4?8:TYPE_bidang==5?6:TYPE_bidang==6?8:0;
    if(!필요){Tutup();return;}if(입력수<필요)return;
    if(TYPE_bidang==2){unsigned 수=읽기16(입력+2);if(수>128){Tutup();return;}필요+=수*4;}
    if(TYPE_bidang==6){unsigned 수=읽기32(입력+4);if(수>4096){Tutup();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_bidang==0){unsigned bit_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),merah_Saluran_anjak=입력[14],hijau_Saluran_anjak=입력[15],biru_Saluran_anjak=입력[16];
        if((bit_VALUE!=16&&bit_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||merah_Saluran_anjak>24||hijau_Saluran_anjak>24||biru_Saluran_anjak>24||
           ((uint64_t)빨<<merah_Saluran_anjak)>((1ull<<bit_VALUE)-1)||((uint64_t)초<<hijau_Saluran_anjak)>((1ull<<bit_VALUE)-1)||((uint64_t)파<<biru_Saluran_anjak)>((1ull<<bit_VALUE)-1)){Tutup();return;}
        pel_saiz=bit_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;merah_anjak=merah_Saluran_anjak;hijau_anjak=hijau_Saluran_anjak;biru_anjak=biru_Saluran_anjak;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_bidang==3)화면요청(입력);
    else if(TYPE_bidang==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_bidang==5){unsigned koordinat_x=읽기16(입력+2),Y_koordinat=읽기16(입력+4);if(koordinat_x>=너비)koordinat_x=너비-1;if(Y_koordinat>=높이)Y_koordinat=높이-1;
        if(입력[1])lakukan_jauh_Kunci();
        unsigned char Peristiwa[]={30,1,입력[1],koordinat_x&255,koordinat_x>>8,Y_koordinat&255,Y_koordinat>>8};원격입력넣기(Peristiwa,sizeof(Peristiwa));}
    소비(필요);
}
