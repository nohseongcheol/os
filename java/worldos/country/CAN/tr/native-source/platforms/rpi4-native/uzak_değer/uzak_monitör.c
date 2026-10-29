/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Bağlan, 제한된 artış_değer süre_değer, 비동기 göndermek_değer, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 veri 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "uzak_değer.h"
#include "şifreleme_Destek.h"
#include "Profil.h"
#include "../ağ_Yığın/ağ_Yığın.h"
#include "../makine/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Pano_Terminal(uintptr_t);
void uzak_tuş_vuruş(unsigned,int);
void 원격글쇠초기화(void);
void commit_uzak_tuş(void);
static int Dinleniyor_uç_nokta=-1,eş_değer=-1,aşama_değer,닫을예정;
static uintptr_t cxn_saat,다시받을때;
static unsigned char artış_değer[8192],metinÇıktısı[4096],görev_değer[16];
static unsigned artış_BAĞ_DEĞ_SAY,çıktı_BAĞ_DEĞ_SAY,보낸수;
static unsigned 너비,높이,piksel_boyutlandırmak=4,big_endian_değer,빨강최대=255,초록최대=255,파랑최대=255,kırmızı_kaydırmak=16,yeşil_kaydırmak=8,mavi_kaydırmak;
static uint32_t Önceki_özet[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned parça_BAĞ_DEĞ_SAY,parça_konum,istendi_X,istendi_Y,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *veri_konum){return(unsigned)veri_konum[0]*256+veri_konum[1];}
static uint32_t 읽기32(const unsigned char *veri_konum){return(uint32_t)veri_konum[0]<<24|(uint32_t)veri_konum[1]<<16|(uint32_t)veri_konum[2]<<8|veri_konum[3];}
static void yazma_16(unsigned char *veri_konum,unsigned değer){veri_konum[0]=değer>>8;veri_konum[1]=değer;}
static void yazma_32(unsigned char *veri_konum,uint32_t değer){veri_konum[0]=değer>>24;veri_konum[1]=değer>>16;veri_konum[2]=değer>>8;veri_konum[3]=değer;}
static void Kapat(void){if(eş_değer>=0)Kapat_ağ(eş_değer);eş_değer=-1;aşama_değer=0;artış_BAĞ_DEĞ_SAY=çıktı_BAĞ_DEĞ_SAY=보낸수=0;parça_BAĞ_DEĞ_SAY=parça_konum=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *veri,unsigned 수){memcpy(metinÇıktısı,veri,수);çıktı_BAĞ_DEĞ_SAY=수;보낸수=0;}
static void tüketmek_değer(unsigned 수){artış_BAĞ_DEĞ_SAY-=수;memmove(artış_değer,artış_değer+수,artış_BAĞ_DEĞ_SAY);}
int denetim_uzak_monitör(unsigned Eylem){
    if(Eylem==0){Kapat();if(Dinleniyor_uç_nokta>=0)Kapat_ağ(Dinleniyor_uç_nokta);Dinleniyor_uç_nokta=-1;return 0;}
    if(Eylem!=1)return Dinleniyor_uç_nokta>=0;
    if(Dinleniyor_uç_nokta>=0)return 0;
    int taşımak_değer=açmak_yuva_uç_nokta(1);if(taşımak_değer<0)return taşımak_değer;통신주소재사용(taşımak_değer);
    int sonuç=NET_BIND(taşımak_değer,0,5900);if(!sonuç)sonuç=NET_dinlemek(taşımak_değer);
    if(sonuç<0){Kapat_ağ(taşımak_değer);return sonuç;}Dinleniyor_uç_nokta=taşımak_değer;return 0;
}
static uint32_t parça_özet(unsigned 가로,unsigned Dikey_konum){
    uint32_t değer=2166136261u;
    for(unsigned Y_koordinat=Dikey_konum;Y_koordinat<Dikey_konum+16&&Y_koordinat<높이;Y_koordinat++)for(unsigned x_koordinatı=가로;x_koordinatı<가로+32&&x_koordinatı<너비;x_koordinatı++)değer=(değer^보드화면읽기(x_koordinatı,Y_koordinat))*16777619u;
    return değer;
}
static void 화면요청(const unsigned char *veri_konum){
    istendi_X=읽기16(veri_konum+2);istendi_Y=읽기16(veri_konum+4);요청폭=읽기16(veri_konum+6);요청높이=읽기16(veri_konum+8);
    if(istendi_X>=너비||istendi_Y>=높이)요청폭=요청높이=0;
    if(요청폭>너비-istendi_X&&istendi_X<너비)요청폭=너비-istendi_X;
    if(요청높이>높이-istendi_Y&&istendi_Y<높이)요청높이=높이-istendi_Y;
    parça_BAĞ_DEĞ_SAY=parça_konum=0;
    if(요청폭&&요청높이)for(unsigned Y_koordinat=istendi_Y/16;Y_koordinat<=(istendi_Y+요청높이-1)/16;Y_koordinat++)for(unsigned x_koordinatı=istendi_X/32;x_koordinatı<=(istendi_X+요청폭-1)/32;x_koordinatı++){
        unsigned konum_dizini=Y_koordinat*60+x_koordinatı;uint32_t özet_değer=parça_özet(x_koordinatı*32,Y_koordinat*16);
        if(!veri_konum[1]||Önceki_özet[konum_dizini]!=özet_değer)바뀐타일[parça_BAĞ_DEĞ_SAY++]=konum_dizini;
    }
    metinÇıktısı[0]=metinÇıktısı[1]=0;yazma_16(metinÇıktısı+2,parça_BAĞ_DEĞ_SAY);çıktı_BAĞ_DEĞ_SAY=4;보낸수=0;
}
static void göndermek_parça(void){
    unsigned konum_dizini=바뀐타일[parça_konum++],가로=(konum_dizini%60)*32,Dikey_konum=(konum_dizini/60)*16;
    unsigned Bitiş_X=가로+32,Bitiş_Y=Dikey_konum+16;if(Bitiş_X>너비)Bitiş_X=너비;if(Bitiş_Y>높이)Bitiş_Y=높이;
    /* 부분 타일 istek 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=istendi_X&&Dikey_konum>=istendi_Y&&Bitiş_X<=istendi_X+요청폭&&Bitiş_Y<=istendi_Y+요청높이;
    if(전부)Önceki_özet[konum_dizini]=parça_özet(가로,Dikey_konum);
    if(가로<istendi_X)가로=istendi_X;if(Dikey_konum<istendi_Y)Dikey_konum=istendi_Y;
    if(Bitiş_X>istendi_X+요청폭)Bitiş_X=istendi_X+요청폭;if(Bitiş_Y>istendi_Y+요청높이)Bitiş_Y=istendi_Y+요청높이;
    yazma_16(metinÇıktısı,가로);yazma_16(metinÇıktısı+2,Dikey_konum);yazma_16(metinÇıktısı+4,Bitiş_X-가로);yazma_16(metinÇıktısı+6,Bitiş_Y-Dikey_konum);yazma_32(metinÇıktısı+8,0);
    çıktı_BAĞ_DEĞ_SAY=12;보낸수=0;
    for(unsigned Y_koordinat=Dikey_konum;Y_koordinat<Bitiş_Y;Y_koordinat++)for(unsigned x_koordinatı=가로;x_koordinatı<Bitiş_X;x_koordinatı++){
        uint32_t 색=보드화면읽기(x_koordinatı,Y_koordinat),değer=(((색>>16)&255)*빨강최대/255)<<kırmızı_kaydırmak|
            (((색>>8)&255)*초록최대/255)<<yeşil_kaydırmak|((색&255)*파랑최대/255)<<mavi_kaydırmak;
        for(unsigned 순번=0;순번<piksel_boyutlandırmak;순번++)metinÇıktısı[çıktı_BAĞ_DEĞ_SAY++]=değer>>(8*(big_endian_değer?piksel_boyutlandırmak-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Dinleniyor_uç_nokta<0)return;
    if(eş_değer<0){if(보드밀리초()<다시받을때)return;eş_değer=NET_kabul_etmek(Dinleniyor_uç_nokta);if(eş_değer<0)return;
        cxn_saat=보드밀리초();aşama_değer=1;내보내기("RFB 003.008\n",12);memset(Önceki_özet,0,sizeof(Önceki_özet));
        piksel_boyutlandırmak=4;big_endian_değer=0;빨강최대=초록최대=파랑최대=255;kırmızı_kaydırmak=16;yeşil_kaydırmak=8;mavi_kaydırmak=0;}
    if(aşama_değer<5&&보드밀리초()-cxn_saat>15000){Kapat();return;}
    if(çıktı_BAĞ_DEĞ_SAY){int 수=NET_yazma(eş_değer,metinÇıktısı+보낸수,çıktı_BAĞ_DEĞ_SAY-보낸수);if(수>0){보낸수+=수;if(보낸수==çıktı_BAĞ_DEĞ_SAY)çıktı_BAĞ_DEĞ_SAY=보낸수=0;}else if(수!=-11){Kapat();return;}}
    if(!çıktı_BAĞ_DEĞ_SAY&&닫을예정){Kapat();return;}
    if(!çıktı_BAĞ_DEĞ_SAY&&parça_konum<parça_BAĞ_DEĞ_SAY)göndermek_parça();
    if(artış_BAĞ_DEĞ_SAY==sizeof(artış_değer)){Kapat();return;}
    int GETİRİ_BAĞ_DEĞ_SAY=통신읽기(eş_değer,artış_değer+artış_BAĞ_DEĞ_SAY,sizeof(artış_değer)-artış_BAĞ_DEĞ_SAY);
    if(GETİRİ_BAĞ_DEĞ_SAY==0||(GETİRİ_BAĞ_DEĞ_SAY<0&&GETİRİ_BAĞ_DEĞ_SAY!=-11)){Kapat();return;}if(GETİRİ_BAĞ_DEĞ_SAY>0)artış_BAĞ_DEĞ_SAY+=GETİRİ_BAĞ_DEĞ_SAY;
    if(çıktı_BAĞ_DEĞ_SAY||parça_konum<parça_BAĞ_DEĞ_SAY)return;
    if(aşama_değer==1&&artış_BAĞ_DEĞ_SAY>=12){if(memcmp(artış_değer,"RFB 003.008\n",12)){Kapat();return;}tüketmek_değer(12);const unsigned char kimlik_doğrulama_yöntemi[]={1,2};내보내기(kimlik_doğrulama_yöntemi,2);aşama_değer=2;return;}
    if(aşama_değer==2&&artış_BAĞ_DEĞ_SAY){if(artış_değer[0]!=2||uzak_rastgele(görev_değer,16)){Kapat();return;}tüketmek_değer(1);내보내기(görev_değer,16);aşama_değer=3;return;}
    if(aşama_değer==3&&artış_BAĞ_DEĞ_SAY>=16){unsigned char tuş_malzeme[8],정답[16];br_des_ct_cbcenc_keys parola_değer;
        for(unsigned 순번=0;순번<8;순번++){unsigned değer=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(değer&1);değer>>=1;}tuş_malzeme[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&parola_değer,tuş_malzeme,8);memcpy(정답,görev_değer,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektör_değer[8]={0};br_des_ct_cbcenc_run(&parola_değer,vektör_değer,정답+순번,8);memset(vektör_değer,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^artış_değer[순번];tüketmek_değer(16);memset(&parola_değer,0,sizeof(parola_değer));memset(tuş_malzeme,0,8);memset(정답,0,16);memset(görev_değer,0,16);
        yazma_32(metinÇıktısı,차이?1:0);çıktı_BAĞ_DEĞ_SAY=4;보낸수=0;
        if(차이){yazma_32(metinÇıktısı+4,19);memcpy(metinÇıktısı+8,"Authentication fail",19);çıktı_BAĞ_DEĞ_SAY=27;닫을예정=1;}else aşama_değer=4;return;}
    if(aşama_değer==4&&artış_BAĞ_DEĞ_SAY){tüketmek_değer(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Kapat();return;}
        if(!Pano_Terminal(7)){const unsigned char Olay[]={30,2,1,0,0,0,0};akış_uzak_artış(Olay,7);}
        memset(metinÇıktısı,0,40);yazma_16(metinÇıktısı,너비);yazma_16(metinÇıktısı+2,높이);metinÇıktısı[4]=32;metinÇıktısı[5]=24;metinÇıktısı[7]=1;
        yazma_16(metinÇıktısı+8,255);yazma_16(metinÇıktısı+10,255);yazma_16(metinÇıktısı+12,255);metinÇıktısı[14]=16;metinÇıktısı[15]=8;
        const char *İsim="jkoros native";yazma_32(metinÇıktısı+20,strlen(İsim));memcpy(metinÇıktısı+24,İsim,strlen(İsim));çıktı_BAĞ_DEĞ_SAY=24+strlen(İsim);보낸수=0;aşama_değer=5;return;}
    if(aşama_değer!=5||!artış_BAĞ_DEĞ_SAY)return;
    unsigned TÜR_alan=artış_değer[0],필요=TÜR_alan==0?20:TÜR_alan==2?4:TÜR_alan==3?10:TÜR_alan==4?8:TÜR_alan==5?6:TÜR_alan==6?8:0;
    if(!필요){Kapat();return;}if(artış_BAĞ_DEĞ_SAY<필요)return;
    if(TÜR_alan==2){unsigned 수=읽기16(artış_değer+2);if(수>128){Kapat();return;}필요+=수*4;}
    if(TÜR_alan==6){unsigned 수=읽기32(artış_değer+4);if(수>4096){Kapat();return;}필요+=수;}
    if(artış_BAĞ_DEĞ_SAY<필요)return;
    if(TÜR_alan==0){unsigned bit_değer=artış_değer[4],빨=읽기16(artış_değer+8),초=읽기16(artış_değer+10),파=읽기16(artış_değer+12),kırmızı_Kanal_kaydırmak=artış_değer[14],yeşil_Kanal_kaydırmak=artış_değer[15],mavi_Kanal_kaydırmak=artış_değer[16];
        if((bit_değer!=16&&bit_değer!=32)||!artış_değer[7]||artış_değer[6]>1||!빨||!초||!파||빨>255||초>255||파>255||kırmızı_Kanal_kaydırmak>24||yeşil_Kanal_kaydırmak>24||mavi_Kanal_kaydırmak>24||
           ((uint64_t)빨<<kırmızı_Kanal_kaydırmak)>((1ull<<bit_değer)-1)||((uint64_t)초<<yeşil_Kanal_kaydırmak)>((1ull<<bit_değer)-1)||((uint64_t)파<<mavi_Kanal_kaydırmak)>((1ull<<bit_değer)-1)){Kapat();return;}
        piksel_boyutlandırmak=bit_değer/8;big_endian_değer=artış_değer[6];빨강최대=빨;초록최대=초;파랑최대=파;kırmızı_kaydırmak=kırmızı_Kanal_kaydırmak;yeşil_kaydırmak=yeşil_Kanal_kaydırmak;mavi_kaydırmak=mavi_Kanal_kaydırmak;memset(Önceki_özet,0,sizeof(Önceki_özet));
    }else if(TÜR_alan==3)화면요청(artış_değer);
    else if(TÜR_alan==4)uzak_tuş_vuruş(읽기32(artış_değer+4),artış_değer[1]!=0);
    else if(TÜR_alan==5){unsigned x_koordinatı=읽기16(artış_değer+2),Y_koordinat=읽기16(artış_değer+4);if(x_koordinatı>=너비)x_koordinatı=너비-1;if(Y_koordinat>=높이)Y_koordinat=높이-1;
        if(artış_değer[1])commit_uzak_tuş();
        unsigned char Olay[]={30,1,artış_değer[1],x_koordinatı&255,x_koordinatı>>8,Y_koordinat&255,Y_koordinat>>8};akış_uzak_artış(Olay,sizeof(Olay));}
    tüketmek_değer(필요);
}
