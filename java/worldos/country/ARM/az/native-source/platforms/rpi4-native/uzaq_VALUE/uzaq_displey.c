/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Bağlan, 제한된 입력 uzunluq_VALUE, 비동기 göndərmək_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 verilənlər 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "uzaq_VALUE.h"
#include "암호기반.h"
#include "Profil.h"
#include "../Şəbəkə_Yığın/Şəbəkə_Yığın.h"
#include "../maşın/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t lövhə_Terminal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,eynisəviyyəli_VALUE=-1,səhnə_VALUE,닫을예정;
static uintptr_t qoşulma_TIME,다시받을때;
static unsigned char 입력[8192],출력[4096],yarış_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,piksel_ölçünü_dəyişmək=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned mozaika_COUNT,mozaika_yerinə_qoymaq,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *verilənlər_yerinə_qoymaq){return(unsigned)verilənlər_yerinə_qoymaq[0]*256+verilənlər_yerinə_qoymaq[1];}
static uint32_t 읽기32(const unsigned char *verilənlər_yerinə_qoymaq){return(uint32_t)verilənlər_yerinə_qoymaq[0]<<24|(uint32_t)verilənlər_yerinə_qoymaq[1]<<16|(uint32_t)verilənlər_yerinə_qoymaq[2]<<8|verilənlər_yerinə_qoymaq[3];}
static void yazmaq_16(unsigned char *verilənlər_yerinə_qoymaq,unsigned VALUE){verilənlər_yerinə_qoymaq[0]=VALUE>>8;verilənlər_yerinə_qoymaq[1]=VALUE;}
static void yazmaq_32(unsigned char *verilənlər_yerinə_qoymaq,uint32_t VALUE){verilənlər_yerinə_qoymaq[0]=VALUE>>24;verilənlər_yerinə_qoymaq[1]=VALUE>>16;verilənlər_yerinə_qoymaq[2]=VALUE>>8;verilənlər_yerinə_qoymaq[3]=VALUE;}
static void Bağla(void){if(eynisəviyyəli_VALUE>=0)bağlamaq_Şəbəkə(eynisəviyyəli_VALUE);eynisəviyyəli_VALUE=-1;səhnə_VALUE=0;입력수=출력수=보낸수=0;mozaika_COUNT=mozaika_yerinə_qoymaq=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *verilənlər,unsigned 수){memcpy(출력,verilənlər,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int nəzarət_uzaq_displey(unsigned Gedişat){
    if(Gedişat==0){Bağla();if(듣는곳>=0)bağlamaq_Şəbəkə(듣는곳);듣는곳=-1;return 0;}
    if(Gedişat!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int ölçü=망주소묶기(port_VALUE,0,5900);if(!ölçü)ölçü=연결기다리기(port_VALUE);
    if(ölçü<0){bağlamaq_Şəbəkə(port_VALUE);return ölçü;}듣는곳=port_VALUE;return 0;
}
static uint32_t mozaika_xülasə(unsigned 가로,unsigned Şaquli_yerinə_qoymaq){
    uint32_t VALUE=2166136261u;
    for(unsigned Y_koordinat=Şaquli_yerinə_qoymaq;Y_koordinat<Şaquli_yerinə_qoymaq+16&&Y_koordinat<높이;Y_koordinat++)for(unsigned x_koordinatı=가로;x_koordinatı<가로+32&&x_koordinatı<너비;x_koordinatı++)VALUE=(VALUE^보드화면읽기(x_koordinatı,Y_koordinat))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *verilənlər_yerinə_qoymaq){
    요청가로=읽기16(verilənlər_yerinə_qoymaq+2);요청세로=읽기16(verilənlər_yerinə_qoymaq+4);요청폭=읽기16(verilənlər_yerinə_qoymaq+6);요청높이=읽기16(verilənlər_yerinə_qoymaq+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    mozaika_COUNT=mozaika_yerinə_qoymaq=0;
    if(요청폭&&요청높이)for(unsigned Y_koordinat=요청세로/16;Y_koordinat<=(요청세로+요청높이-1)/16;Y_koordinat++)for(unsigned x_koordinatı=요청가로/32;x_koordinatı<=(요청가로+요청폭-1)/32;x_koordinatı++){
        unsigned yerinə_qoymaq_INDEX=Y_koordinat*60+x_koordinatı;uint32_t xülasə_VALUE=mozaika_xülasə(x_koordinatı*32,Y_koordinat*16);
        if(!verilənlər_yerinə_qoymaq[1]||지난요약[yerinə_qoymaq_INDEX]!=xülasə_VALUE)바뀐타일[mozaika_COUNT++]=yerinə_qoymaq_INDEX;
    }
    출력[0]=출력[1]=0;yazmaq_16(출력+2,mozaika_COUNT);출력수=4;보낸수=0;
}
static void göndərmək_mozaika(void){
    unsigned yerinə_qoymaq_INDEX=바뀐타일[mozaika_yerinə_qoymaq++],가로=(yerinə_qoymaq_INDEX%60)*32,Şaquli_yerinə_qoymaq=(yerinə_qoymaq_INDEX/60)*16;
    unsigned bitirmək_X=가로+32,bitirmək_Y=Şaquli_yerinə_qoymaq+16;if(bitirmək_X>너비)bitirmək_X=너비;if(bitirmək_Y>높이)bitirmək_Y=높이;
    /* 부분 타일 HTTP_sorğusu 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Şaquli_yerinə_qoymaq>=요청세로&&bitirmək_X<=요청가로+요청폭&&bitirmək_Y<=요청세로+요청높이;
    if(전부)지난요약[yerinə_qoymaq_INDEX]=mozaika_xülasə(가로,Şaquli_yerinə_qoymaq);
    if(가로<요청가로)가로=요청가로;if(Şaquli_yerinə_qoymaq<요청세로)Şaquli_yerinə_qoymaq=요청세로;
    if(bitirmək_X>요청가로+요청폭)bitirmək_X=요청가로+요청폭;if(bitirmək_Y>요청세로+요청높이)bitirmək_Y=요청세로+요청높이;
    yazmaq_16(출력,가로);yazmaq_16(출력+2,Şaquli_yerinə_qoymaq);yazmaq_16(출력+4,bitirmək_X-가로);yazmaq_16(출력+6,bitirmək_Y-Şaquli_yerinə_qoymaq);yazmaq_32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned Y_koordinat=Şaquli_yerinə_qoymaq;Y_koordinat<bitirmək_Y;Y_koordinat++)for(unsigned x_koordinatı=가로;x_koordinatı<bitirmək_X;x_koordinatı++){
        uint32_t 색=보드화면읽기(x_koordinatı,Y_koordinat),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<piksel_ölçünü_dəyişmək;순번++)출력[출력수++]=VALUE>>(8*(큰끝?piksel_ölçünü_dəyişmək-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(eynisəviyyəli_VALUE<0){if(보드밀리초()<다시받을때)return;eynisəviyyəli_VALUE=망연결받기(듣는곳);if(eynisəviyyəli_VALUE<0)return;
        qoşulma_TIME=보드밀리초();səhnə_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        piksel_ölçünü_dəyişmək=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(səhnə_VALUE<5&&보드밀리초()-qoşulma_TIME>15000){Bağla();return;}
    if(출력수){int 수=통신쓰기(eynisəviyyəli_VALUE,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Bağla();return;}}
    if(!출력수&&닫을예정){Bağla();return;}
    if(!출력수&&mozaika_yerinə_qoymaq<mozaika_COUNT)göndərmək_mozaika();
    if(입력수==sizeof(입력)){Bağla();return;}
    int RECEIVED_COUNT=통신읽기(eynisəviyyəli_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Bağla();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||mozaika_yerinə_qoymaq<mozaika_COUNT)return;
    if(səhnə_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Bağla();return;}소비(12);const unsigned char əslliyi_yoxlama_üsulu[]={1,2};내보내기(əslliyi_yoxlama_üsulu,2);səhnə_VALUE=2;return;}
    if(səhnə_VALUE==2&&입력수){if(입력[0]!=2||원격난수(yarış_VALUE,16)){Bağla();return;}소비(1);내보내기(yarış_VALUE,16);səhnə_VALUE=3;return;}
    if(səhnə_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys parol_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&parol_VALUE,열쇠,8);memcpy(정답,yarış_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_VALUE[8]={0};br_des_ct_cbcenc_run(&parol_VALUE,vektor_VALUE,정답+순번,8);memset(vektor_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&parol_VALUE,0,sizeof(parol_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(yarış_VALUE,0,16);
        yazmaq_32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){yazmaq_32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else səhnə_VALUE=4;return;}
    if(səhnə_VALUE==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Bağla();return;}
        if(!lövhə_Terminal(7)){const unsigned char hadisə[]={30,2,1,0,0,0,0};원격입력넣기(hadisə,7);}
        memset(출력,0,40);yazmaq_16(출력,너비);yazmaq_16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        yazmaq_16(출력+8,255);yazmaq_16(출력+10,255);yazmaq_16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *Ad="jkoros native";yazmaq_32(출력+20,strlen(Ad));memcpy(출력+24,Ad,strlen(Ad));출력수=24+strlen(Ad);보낸수=0;səhnə_VALUE=5;return;}
    if(səhnə_VALUE!=5||!입력수)return;
    unsigned TYPE_sahə=입력[0],필요=TYPE_sahə==0?20:TYPE_sahə==2?4:TYPE_sahə==3?10:TYPE_sahə==4?8:TYPE_sahə==5?6:TYPE_sahə==6?8:0;
    if(!필요){Bağla();return;}if(입력수<필요)return;
    if(TYPE_sahə==2){unsigned 수=읽기16(입력+2);if(수>128){Bağla();return;}필요+=수*4;}
    if(TYPE_sahə==6){unsigned 수=읽기32(입력+4);if(수>4096){Bağla();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_sahə==0){unsigned bit_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_VALUE!=16&&bit_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bit_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bit_VALUE)-1)){Bağla();return;}
        piksel_ölçünü_dəyişmək=bit_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_sahə==3)화면요청(입력);
    else if(TYPE_sahə==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_sahə==5){unsigned x_koordinatı=읽기16(입력+2),Y_koordinat=읽기16(입력+4);if(x_koordinatı>=너비)x_koordinatı=너비-1;if(Y_koordinat>=높이)Y_koordinat=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char hadisə[]={30,1,입력[1],x_koordinatı&255,x_koordinatı>>8,Y_koordinat&255,Y_koordinat>>8};원격입력넣기(hadisə,sizeof(hadisə));}
    소비(필요);
}
