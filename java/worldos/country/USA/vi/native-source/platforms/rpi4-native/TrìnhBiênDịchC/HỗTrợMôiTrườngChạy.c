#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
/* Freestanding compiler support. All file I/O goes through the native SVC ABI. */
#include "gọiThựcHiện.h"
#include "stdio.h"
#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "resources.h"
static int lỗi;
int *__errno_location(void){return &lỗi;}
void exit(int giáTrịTrạngThái){gọiThựcHiệnNgườiDùng(6,giáTrịTrạngThái,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *kiểmTraBiểuThức,const char *Tệp,unsigned dòng,const char *tênMụcPhươngThức){fprintf(stderr,"cc assertion: %s %s:%u %s\n",kiểmTraBiểuThức,Tệp,dòng,tênMụcPhươngThức);exit(1);}
size_t strlen(const char*dữLiệuChuỗi){const char*vịTríDữLiệu=dữLiệuChuỗi;while(*vịTríDữLiệu)vịTríDữLiệu++;return vịTríDữLiệu-dữLiệuChuỗi;}
int strcmp(const char*giáTrịĐầuTiên,const char*giáTrịThứHai){while(*giáTrịĐầuTiên&&*giáTrịĐầuTiên==*giáTrịThứHai){giáTrịĐầuTiên++;giáTrịThứHai++;}return (unsigned char)*giáTrịĐầuTiên-(unsigned char)*giáTrịThứHai;}
int strncmp(const char*giáTrịĐầuTiên,const char*giáTrịThứHai,size_t sốLượngPhầnMục){while(sốLượngPhầnMục--){unsigned char tọaĐộX=*giáTrịĐầuTiên++,tọaĐộY=*giáTrịThứHai++;if(tọaĐộX!=tọaĐộY)return tọaĐộX-tọaĐộY;if(!tọaĐộX)return 0;}return 0;}
char *strcpy(char*dữLiệuĐích,const char*dữLiệuChuỗi){char*giáTrịĐãTrảVề=dữLiệuĐích;while((*dữLiệuĐích++=*dữLiệuChuỗi++)){}return giáTrịĐãTrảVề;}
char *strchr(const char*dữLiệuChuỗi,int mãKýTự){do{if(*dữLiệuChuỗi==(char)mãKýTự)return (char*)dữLiệuChuỗi;}while(*dữLiệuChuỗi++);return 0;}
char *strrchr(const char*dữLiệuChuỗi,int mãKýTự){const char*giáTrịĐãTrảVề=0;do{if(*dữLiệuChuỗi==(char)mãKýTự)giáTrịĐãTrảVề=dữLiệuChuỗi;}while(*dữLiệuChuỗi++);return (char*)giáTrịĐãTrảVề;}
char *strstr(const char*dữLiệuChuỗi,const char*mụcThiếtBịCuối){size_t sốLượngPhầnMục=strlen(mụcThiếtBịCuối);for(;*dữLiệuChuỗi;dữLiệuChuỗi++)if(!strncmp(dữLiệuChuỗi,mụcThiếtBịCuối,sốLượngPhầnMục))return (char*)dữLiệuChuỗi;return sốLượngPhầnMục?0:(char*)dữLiệuChuỗi;}
int memcmp(const void*giáTrịĐầuTiên,const void*giáTrịThứHai,size_t sốLượngPhầnMục){const unsigned char*tọaĐộX=giáTrịĐầuTiên,*tọaĐộY=giáTrịThứHai;while(sốLượngPhầnMục--){if(*tọaĐộX!=*tọaĐộY)return *tọaĐộX-*tọaĐộY;tọaĐộX++;tọaĐộY++;}return 0;}
void *memmove(void*dữLiệuĐích,const void*dữLiệuChuỗi,size_t sốLượngPhầnMục){unsigned char*tọaĐộX=dữLiệuĐích;const unsigned char*tọaĐộY=dữLiệuChuỗi;if(tọaĐộX<tọaĐộY){for(size_t chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++)tọaĐộX[chỉSốThứBậc]=tọaĐộY[chỉSốThứBậc];}else while(sốLượngPhầnMục){sốLượngPhầnMục--;tọaĐộX[sốLượngPhầnMục]=tọaĐộY[sốLượngPhầnMục];}return dữLiệuĐích;}
static unsigned char vùngCấpPhátViệcCấpPhát[6*1024*1024] __attribute__((aligned(16)));
typedef struct khốiDữLiệu {size_t cỡ;struct khốiDữLiệu*phầnMụcKếTiếp;int sứcChứaCònLại;int phầnĐệm;uint64_t đơnVịCáchCănChỉnh;} khốiDữLiệu;
static khốiDữLiệu *mụcĐầuTiên;
void free(void*vịTríDữLiệu){if(!vịTríDữLiệu)return;khốiDữLiệu*giáTrịThứHai=(khốiDữLiệu*)vịTríDữLiệu-1;giáTrịThứHai->sứcChứaCònLại=1;for(khốiDữLiệu*độLệchKếTiếp=mụcĐầuTiên;độLệchKếTiếp&&độLệchKếTiếp->phầnMụcKếTiếp;){if(độLệchKếTiếp->sứcChứaCònLại&&độLệchKếTiếp->phầnMụcKếTiếp->sứcChứaCònLại){độLệchKếTiếp->cỡ+=sizeof(khốiDữLiệu)+độLệchKếTiếp->phầnMụcKếTiếp->cỡ;độLệchKếTiếp->phầnMụcKếTiếp=độLệchKếTiếp->phầnMụcKếTiếp->phầnMụcKếTiếp;}else độLệchKếTiếp=độLệchKếTiếp->phầnMụcKếTiếp;}}
void *realloc(void*vịTríDữLiệu,size_t sốLượngPhầnMục){
    if(!sốLượngPhầnMục){free(vịTríDữLiệu);return 0;}if(sốLượngPhầnMục>sizeof(vùngCấpPhátViệcCấpPhát)-sizeof(khốiDữLiệu))return 0;sốLượngPhầnMục=(sốLượngPhầnMục+15)&~(size_t)15;
    if(!mụcĐầuTiên){mụcĐầuTiên=(khốiDữLiệu*)vùngCấpPhátViệcCấpPhát;mụcĐầuTiên->cỡ=sizeof(vùngCấpPhátViệcCấpPhát)-sizeof(khốiDữLiệu);mụcĐầuTiên->sứcChứaCònLại=1;mụcĐầuTiên->phầnMụcKếTiếp=0;}
    khốiDữLiệu*phầnMụcTrướcĐó=vịTríDữLiệu?(khốiDữLiệu*)vịTríDữLiệu-1:0;if(phầnMụcTrướcĐó&&phầnMụcTrướcĐó->cỡ>=sốLượngPhầnMục)return vịTríDữLiệu;
    for(khốiDữLiệu*giáTrịThứHai=mụcĐầuTiên;giáTrịThứHai;giáTrịThứHai=giáTrịThứHai->phầnMụcKếTiếp)if(giáTrịThứHai->sứcChứaCònLại&&giáTrịThứHai->cỡ>=sốLượngPhầnMục){
        if(giáTrịThứHai->cỡ>=sốLượngPhầnMục+sizeof(khốiDữLiệu)+16){khốiDữLiệu*phầnCònLại=(khốiDữLiệu*)((unsigned char*)(giáTrịThứHai+1)+sốLượngPhầnMục);phầnCònLại->cỡ=giáTrịThứHai->cỡ-sốLượngPhầnMục-sizeof(khốiDữLiệu);phầnCònLại->phầnMụcKếTiếp=giáTrịThứHai->phầnMụcKếTiếp;phầnCònLại->sứcChứaCònLại=1;giáTrịThứHai->phầnMụcKếTiếp=phầnCònLại;giáTrịThứHai->cỡ=sốLượngPhầnMục;}
        giáTrịThứHai->sứcChứaCònLại=0;void*giáTrịĐãTrảVề=giáTrịThứHai+1;if(phầnMụcTrướcĐó){memcpy(giáTrịĐãTrảVề,vịTríDữLiệu,phầnMụcTrướcĐó->cỡ);free(vịTríDữLiệu);}return giáTrịĐãTrảVề;
    }lỗi=12;return 0;
}
void *malloc(size_t sốLượngPhầnMục){return realloc(0,sốLượngPhầnMục);}
void *calloc(size_t sốLượngPhầnMục,size_t dữLiệuChuỗi){if(dữLiệuChuỗi&&sốLượngPhầnMục>SIZE_MAX/dữLiệuChuỗi)return 0;void*vịTríDữLiệu=malloc(sốLượngPhầnMục*dữLiệuChuỗi);if(vịTríDữLiệu)memset(vịTríDữLiệu,0,sốLượngPhầnMục*dữLiệuChuỗi);return vịTríDữLiệu;}
unsigned long long strtoull(const char*dữLiệuChuỗi,char**độLệchKếtThúc,int giáTrịNền){
    const char*bắtChạyĐộLệch=dữLiệuChuỗi;while(*dữLiệuChuỗi==' '||(*dữLiệuChuỗi>=9&&*dữLiệuChuỗi<=13))dữLiệuChuỗi++;int làÂm=0;if(*dữLiệuChuỗi=='-'||*dữLiệuChuỗi=='+')làÂm=*dữLiệuChuỗi++=='-';
    if((!giáTrịNền||giáTrịNền==16)&&dữLiệuChuỗi[0]=='0'&&(dữLiệuChuỗi[1]=='x'||dữLiệuChuỗi[1]=='X')){giáTrịNền=16;dữLiệuChuỗi+=2;}if(!giáTrịNền)giáTrịNền=*dữLiệuChuỗi=='0'?8:10;
    unsigned long long dữLiệuTạm=0;int giáTrịBấtKỳ=0;for(;;){unsigned mãKýTự=*dữLiệuChuỗi,dữLiệuĐích=mãKýTự>='0'&&mãKýTự<='9'?mãKýTự-'0':mãKýTự>='a'&&mãKýTự<='z'?mãKýTự-'a'+10:mãKýTự>='A'&&mãKýTự<='Z'?mãKýTự-'A'+10:99;if(dữLiệuĐích>=(unsigned)giáTrịNền)break;giáTrịBấtKỳ=1;dữLiệuChuỗi++;if(dữLiệuTạm>(~0ull-dữLiệuĐích)/(unsigned)giáTrịNền){dữLiệuTạm=~0ull;lỗi=34;}else dữLiệuTạm=dữLiệuTạm*giáTrịNền+dữLiệuĐích;}
    if(độLệchKếtThúc)*độLệchKếtThúc=(char*)(giáTrịBấtKỳ?dữLiệuChuỗi:bắtChạyĐộLệch);return làÂm?0-dữLiệuTạm:dữLiệuTạm;
}
unsigned long strtoul(const char*dữLiệuChuỗi,char**mụcPhụTrợ,int giáTrịThứHai){return strtoull(dữLiệuChuỗi,mụcPhụTrợ,giáTrịThứHai);}
long strtol(const char*dữLiệuChuỗi,char**mụcPhụTrợ,int giáTrịThứHai){return (long)strtoull(dữLiệuChuỗi,mụcPhụTrợ,giáTrịThứHai);}
int atoi(const char*dữLiệuChuỗi){return (int)strtol(dữLiệuChuỗi,0,10);}
long double ldexpl(long double tọaĐộX,int sốLượngPhầnMục){while(sốLượngPhầnMục>0){tọaĐộX*=2;sốLượngPhầnMục--;}while(sốLượngPhầnMục<0){tọaĐộX/=2;sốLượngPhầnMục++;}return tọaĐộX;}
long double strtold(const char*dữLiệuChuỗi,char**độLệchKếtThúc){
    const char*bắtChạyĐộLệch=dữLiệuChuỗi;while(*dữLiệuChuỗi==' '||(*dữLiệuChuỗi>=9&&*dữLiệuChuỗi<=13))dữLiệuChuỗi++;int làÂm=0;if(*dữLiệuChuỗi=='-'||*dữLiệuChuỗi=='+')làÂm=*dữLiệuChuỗi++=='-';
    int giáTrịNền=10;if(dữLiệuChuỗi[0]=='0'&&(dữLiệuChuỗi[1]=='x'||dữLiệuChuỗi[1]=='X')){giáTrịNền=16;dữLiệuChuỗi+=2;}long double dữLiệuTạm=0,tỷLệ=1;int phầnLẻ=0,giáTrịBấtKỳ=0;
    for(;;){int mãKýTự=*dữLiệuChuỗi,dữLiệuĐích=mãKýTự>='0'&&mãKýTự<='9'?mãKýTự-'0':mãKýTự>='a'&&mãKýTự<='f'?mãKýTự-'a'+10:mãKýTự>='A'&&mãKýTự<='F'?mãKýTự-'A'+10:99;
        if(mãKýTự=='.'&&!phầnLẻ){phầnLẻ=1;dữLiệuChuỗi++;continue;}if(dữLiệuĐích>=giáTrịNền)break;giáTrịBấtKỳ=1;dữLiệuChuỗi++;dữLiệuTạm=dữLiệuTạm*giáTrịNền+dữLiệuĐích;if(phầnLẻ)tỷLệ*=giáTrịNền;
    }dữLiệuTạm/=tỷLệ;
    if((giáTrịNền==10&&(*dữLiệuChuỗi=='e'||*dữLiệuChuỗi=='E'))||(giáTrịNền==16&&(*dữLiệuChuỗi=='p'||*dữLiệuChuỗi=='P'))){const char*hiệnGiáTrị=dữLiệuChuỗi++;int trừCácGiáTrị=0;if(*dữLiệuChuỗi=='-'||*dữLiệuChuỗi=='+')trừCácGiáTrị=*dữLiệuChuỗi++=='-';int sốLượngPhầnMục=0,sốLượngMục=0;while(*dữLiệuChuỗi>='0'&&*dữLiệuChuỗi<='9'){sốLượngMục++;if(sốLượngPhầnMục<20000)sốLượngPhầnMục=sốLượngPhầnMục*10+*dữLiệuChuỗi-'0';dữLiệuChuỗi++;}if(!sốLượngMục)dữLiệuChuỗi=hiệnGiáTrị;else{long double thừaSố=giáTrịNền==16?2:10;while(sốLượngPhầnMục-->0&&sốLượngPhầnMục<200000)dữLiệuTạm=trừCácGiáTrị?dữLiệuTạm/thừaSố:dữLiệuTạm*thừaSố;}}
    if(độLệchKếtThúc)*độLệchKếtThúc=(char*)(giáTrịBấtKỳ?dữLiệuChuỗi:bắtChạyĐộLệch);return làÂm?-dữLiệuTạm:dữLiệuTạm;
}
double strtod(const char*dữLiệuChuỗi,char**mụcPhụTrợ){return (double)strtold(dữLiệuChuỗi,mụcPhụTrợ);}float strtof(const char*dữLiệuChuỗi,char**mụcPhụTrợ){return (float)strtold(dữLiệuChuỗi,mụcPhụTrợ);}
void qsort(void*giáTrịNền,size_t sốLượngPhầnMục,size_t cỡ,int(*soSánh)(const void*,const void*)){
    unsigned char*vịTríDữLiệu=giáTrịNền;for(size_t chỉSốThứBậc=1;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++)for(size_t thứBậcPhíaTrong=chỉSốThứBậc;thứBậcPhíaTrong&&soSánh(vịTríDữLiệu+(thứBậcPhíaTrong-1)*cỡ,vịTríDữLiệu+thứBậcPhíaTrong*cỡ)>0;thứBậcPhíaTrong--)for(size_t chỉSốThứBa=0;chỉSốThứBa<cỡ;chỉSốThứBa++){unsigned char mãKýTự=vịTríDữLiệu[(thứBậcPhíaTrong-1)*cỡ+chỉSốThứBa];vịTríDữLiệu[(thứBậcPhíaTrong-1)*cỡ+chỉSốThứBa]=vịTríDữLiệu[thứBậcPhíaTrong*cỡ+chỉSốThứBa];vịTríDữLiệu[thứBậcPhíaTrong*cỡ+chỉSốThứBa]=mãKýTự;}
}
static struct {int sứcChứaĐãDùng,chỉSốTraCứu;size_t vịTrí;} đãMở[24];
static unsigned char đầuRa[32768];static size_t cỡĐầuRa,vịTríĐầuRa;static int mởĐầuRa;
const unsigned char *đầuRaC(size_t *sốLượngPhầnMục){*sốLượngPhầnMục=cỡĐầuRa;return đầuRa;}
int open(const char*tên,int cácBitCấuHình,...){
    if(!strcmp(tên,"/@cc-output")){if(mởĐầuRa){lỗi=16;return -1;}mởĐầuRa=1;cỡĐầuRa=vịTríĐầuRa=0;return 100;}
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sizeof(cácTàiNguyênTrìnhBiênDịch)/sizeof(cácTàiNguyênTrìnhBiênDịch[0]);chỉSốThứBậc++)if(!strcmp(tên,cácTàiNguyênTrìnhBiênDịch[chỉSốThứBậc].tên)){
        if(cácBitCấuHình&3){lỗi=30;return -1;}for(int thứBậcPhíaTrong=0;thứBậcPhíaTrong<24;thứBậcPhíaTrong++)if(!đãMở[thứBậcPhíaTrong].sứcChứaĐãDùng){đãMở[thứBậcPhíaTrong].sứcChứaĐãDùng=1;đãMở[thứBậcPhíaTrong].chỉSốTraCứu=chỉSốThứBậc;đãMở[thứBậcPhíaTrong].vịTrí=0;return 128+thứBậcPhíaTrong;}lỗi=24;return -1;
    }
    intptr_t giáTrịĐãTrảVề=gọiThựcHiệnNgườiDùng(3,(uintptr_t)tên,cácBitCấuHình,0,0,0,0);if(giáTrịĐãTrảVề<0){lỗi=-giáTrịĐãTrảVề;return -1;}return giáTrịĐãTrảVề;
}
int close(int thẻXửLýTệp){if(thẻXửLýTệp==100){mởĐầuRa=0;return 0;}if(thẻXửLýTệp>=128&&thẻXửLýTệp<152){đãMở[thẻXửLýTệp-128].sứcChứaĐãDùng=0;return 0;}intptr_t giáTrịĐãTrảVề=gọiThựcHiệnNgườiDùng(4,thẻXửLýTệp,0,0,0,0,0);if(giáTrịĐãTrảVề<0){lỗi=-giáTrịĐãTrảVề;return -1;}return 0;}
long read(int thẻXửLýTệp,void*DữLiệu,size_t sốLượngPhầnMục){
    if(thẻXửLýTệp>=128&&thẻXửLýTệp<152&&đãMở[thẻXửLýTệp-128].sứcChứaĐãDùng){int chỉSốThứBậc=thẻXửLýTệp-128;const tàiNguyênTrìnhBiênDịch*giáTrịĐãTrảVề=&cácTàiNguyênTrìnhBiênDịch[đãMở[chỉSốThứBậc].chỉSốTraCứu];size_t bênTrái=giáTrịĐãTrảVề->cỡ-đãMở[chỉSốThứBậc].vịTrí;if(sốLượngPhầnMục>bênTrái)sốLượngPhầnMục=bênTrái;memcpy(DữLiệu,giáTrịĐãTrảVề->DữLiệu+đãMở[chỉSốThứBậc].vịTrí,sốLượngPhầnMục);đãMở[chỉSốThứBậc].vịTrí+=sốLượngPhầnMục;return sốLượngPhầnMục;}
    intptr_t giáTrịĐãTrảVề=gọiThựcHiệnNgườiDùng(2,thẻXửLýTệp,(uintptr_t)DữLiệu,sốLượngPhầnMục,0,0,0);if(giáTrịĐãTrảVề<0){lỗi=-giáTrịĐãTrảVề;return -1;}return giáTrịĐãTrảVề;
}
long write(int thẻXửLýTệp,const void*DữLiệu,size_t sốLượngPhầnMục){
    if(thẻXửLýTệp==100){if(sốLượngPhầnMục>sizeof(đầuRa)-vịTríĐầuRa){lỗi=28;return -1;}memcpy(đầuRa+vịTríĐầuRa,DữLiệu,sốLượngPhầnMục);vịTríĐầuRa+=sốLượngPhầnMục;if(cỡĐầuRa<vịTríĐầuRa)cỡĐầuRa=vịTríĐầuRa;return sốLượngPhầnMục;}
    intptr_t giáTrịĐãTrảVề=gọiThựcHiệnNgườiDùng(1,thẻXửLýTệp,(uintptr_t)DữLiệu,sốLượngPhầnMục,0,0,0);if(giáTrịĐãTrảVề<0){lỗi=-giáTrịĐãTrảVề;return -1;}return giáTrịĐãTrảVề;
}
long lseek(int thẻXửLýTệp,long giáTrịĐộLệch,int dịchVịGốc){
    if(thẻXửLýTệp==100){long vịTríDữLiệu=giáTrịĐộLệch+(dịchVịGốc==0?0:dịchVịGốc==1?vịTríĐầuRa:cỡĐầuRa);if(vịTríDữLiệu<0||(size_t)vịTríDữLiệu>sizeof(đầuRa)){lỗi=22;return -1;}vịTríĐầuRa=vịTríDữLiệu;return vịTríDữLiệu;}
    if(thẻXửLýTệp>=128&&thẻXửLýTệp<152&&đãMở[thẻXửLýTệp-128].sứcChứaĐãDùng){int chỉSốThứBậc=thẻXửLýTệp-128;long vịTríDữLiệu=giáTrịĐộLệch+(dịchVịGốc==0?0:dịchVịGốc==1?đãMở[chỉSốThứBậc].vịTrí:cácTàiNguyênTrìnhBiênDịch[đãMở[chỉSốThứBậc].chỉSốTraCứu].cỡ);if(vịTríDữLiệu<0||(size_t)vịTríDữLiệu>cácTàiNguyênTrìnhBiênDịch[đãMở[chỉSốThứBậc].chỉSốTraCứu].cỡ){lỗi=22;return -1;}đãMở[chỉSốThứBậc].vịTrí=vịTríDữLiệu;return vịTríDữLiệu;}
    intptr_t giáTrịĐãTrảVề=gọiThựcHiệnNgườiDùng(5,thẻXửLýTệp,giáTrịĐộLệch,dịchVịGốc,0,0,0);if(giáTrịĐãTrảVề<0){lỗi=-giáTrịĐãTrảVề;return -1;}return giáTrịĐãTrảVề;
}
int unlink(const char*tên){intptr_t giáTrịĐãTrảVề=gọiThựcHiệnNgườiDùng(11,(uintptr_t)tên,0,0,0,0,0);if(giáTrịĐãTrảVề<0){lỗi=-giáTrịĐãTrảVề;return -1;}return giáTrịĐãTrảVề;}
char *realpath(const char*tên,char*dữLiệuKếtQuả){if(!dữLiệuKếtQuả){dữLiệuKếtQuả=malloc(strlen(tên)+1);if(!dữLiệuKếtQuả)return 0;}return strcpy(dữLiệuKếtQuả,tên);}
char *getcwd(char*vịTríDữLiệu,size_t sốLượngPhầnMục){if(sốLượngPhầnMục<2){lỗi=34;return 0;}vịTríDữLiệu[0]='/';vịTríDữLiệu[1]=0;return vịTríDữLiệu;}
char *strerror(int mụcPhụTrợ){(void)mụcPhụTrợ;return "native compiler I/O error";}
time_t time(time_t*mụcThiếtBịCuối){time_t dữLiệuTạm=0;if(mụcThiếtBịCuối)*mụcThiếtBịCuối=dữLiệuTạm;return dữLiệuTạm;}
struct tm *localtime(const time_t*mụcThiếtBịCuối){(void)mụcThiếtBịCuối;static struct tm dữLiệuTạm={.tm_year=126,.tm_mon=0,.tm_mday=1};return &dữLiệuTạm;}
static FILE cácLuồng[18]={{1,0,1},{2,0,1}};FILE*stdout=&cácLuồng[0],*stderr=&cácLuồng[1];
FILE*fdopen(int thẻXửLýTệp,const char*chếĐộPhươngThức){(void)chếĐộPhươngThức;for(unsigned chỉSốThứBậc=2;chỉSốThứBậc<18;chỉSốThứBậc++)if(!cácLuồng[chỉSốThứBậc].sứcChứaĐãDùng){cácLuồng[chỉSốThứBậc].sứcChứaĐãDùng=1;cácLuồng[chỉSốThứBậc].lỗi=0;cácLuồng[chỉSốThứBậc].thẻXửLýTệp=thẻXửLýTệp;return &cácLuồng[chỉSốThứBậc];}lỗi=24;return 0;}
int fflush(FILE*mụcTệp){return mụcTệp&&mụcTệp->lỗi?-1:0;}
int fclose(FILE*mụcTệp){int giáTrịĐãTrảVề=close(mụcTệp->thẻXửLýTệp);if(mụcTệp->lỗi)giáTrịĐãTrảVề=-1;mụcTệp->sứcChứaĐãDùng=0;return giáTrịĐãTrảVề;}
size_t fwrite(const void*vịTríDữLiệu,size_t dữLiệuChuỗi,size_t sốLượngPhầnMục,FILE*mụcTệp){if(!dữLiệuChuỗi)return 0;if(sốLượngPhầnMục>SIZE_MAX/dữLiệuChuỗi){mụcTệp->lỗi=1;return 0;}long giáTrịĐãTrảVề=write(mụcTệp->thẻXửLýTệp,vịTríDữLiệu,dữLiệuChuỗi*sốLượngPhầnMục);if(giáTrịĐãTrảVề<0){mụcTệp->lỗi=1;return 0;}return (size_t)giáTrịĐãTrảVề/dữLiệuChuỗi;}
int fputc(int mãKýTự,FILE*mụcTệp){unsigned char giáTrịThứHai=mãKýTự;return fwrite(&giáTrịThứHai,1,1,mụcTệp)==1?giáTrịThứHai:EOF;}
int fputs(const char*dữLiệuChuỗi,FILE*mụcTệp){return fwrite(dữLiệuChuỗi,1,strlen(dữLiệuChuỗi),mụcTệp)==strlen(dữLiệuChuỗi)?0:EOF;}
static void đặtGiáTrị(char*dữLiệuKếtQuả,size_t tốiĐaSứcChứa,size_t*vịTríHiệnTại,char mãKýTự){if(*vịTríHiệnTại+1<tốiĐaSứcChứa)dữLiệuKếtQuả[*vịTríHiệnTại]=mãKýTự;(*vịTríHiệnTại)++;}
int vsnprintf(char*dữLiệuKếtQuả,size_t tốiĐaSứcChứa,const char*địnhDạng,va_list cácĐốiSốBiếnĐốiSố){
    size_t vịTríHiệnTại=0;while(*địnhDạng){if(*địnhDạng!='%'){đặtGiáTrị(dữLiệuKếtQuả,tốiĐaSứcChứa,&vịTríHiệnTại,*địnhDạng++);continue;}địnhDạng++;
        int bênTrái=0,giáTrịKhôngSố=0,giáTrịDựPhòng=0;while(*địnhDạng=='-'||*địnhDạng=='0'||*địnhDạng=='#'||*địnhDạng=='+'||*địnhDạng==' '){if(*địnhDạng=='-')bênTrái=1;if(*địnhDạng=='0')giáTrịKhôngSố=1;if(*địnhDạng=='#')giáTrịDựPhòng=1;địnhDạng++;}
        int giáTrịRộng=0,giáTrịĐộChínhXác=-1;if(*địnhDạng=='*'){giáTrịRộng=va_arg(cácĐốiSốBiếnĐốiSố,int);địnhDạng++;}else while(*địnhDạng>='0'&&*địnhDạng<='9')giáTrịRộng=giáTrịRộng*10+*địnhDạng++-'0';
        if(*địnhDạng=='.'){địnhDạng++;giáTrịĐộChínhXác=0;if(*địnhDạng=='*'){giáTrịĐộChínhXác=va_arg(cácĐốiSốBiếnĐốiSố,int);địnhDạng++;}else while(*địnhDạng>='0'&&*địnhDạng<='9')giáTrịĐộChínhXác=giáTrịĐộChínhXác*10+*địnhDạng++-'0';}
        int kýTựRộngKiểu=0;while(*địnhDạng=='l'||*địnhDạng=='z'||*địnhDạng=='t'||*địnhDạng=='j'||*địnhDạng=='h'){if(*địnhDạng!='h')kýTựRộngKiểu=1;địnhDạng++;}
        char loạiMụcKiểu=*địnhDạng?*địnhDạng++:0,lưuTrữBộĐệm[80];const char*dữLiệuChuỗi=lưuTrữBộĐệm;size_t sốLượngPhầnMục=0;
        if(loạiMụcKiểu=='s'){dữLiệuChuỗi=va_arg(cácĐốiSốBiếnĐốiSố,const char*);if(!dữLiệuChuỗi)dữLiệuChuỗi="(null)";sốLượngPhầnMục=strlen(dữLiệuChuỗi);if(giáTrịĐộChínhXác>=0&&sốLượngPhầnMục>(size_t)giáTrịĐộChínhXác)sốLượngPhầnMục=giáTrịĐộChínhXác;}
        else if(loạiMụcKiểu=='c'){lưuTrữBộĐệm[0]=va_arg(cácĐốiSốBiếnĐốiSố,int);sốLượngPhầnMục=1;}
        else if(loạiMụcKiểu=='%'){lưuTrữBộĐệm[0]='%';sốLượngPhầnMục=1;}
        else if(loạiMụcKiểu=='d'||loạiMụcKiểu=='i'||loạiMụcKiểu=='u'||loạiMụcKiểu=='x'||loạiMụcKiểu=='X'||loạiMụcKiểu=='o'||loạiMụcKiểu=='p'){
            unsigned long long giáTrị;int âm=0;
            if(loạiMụcKiểu=='d'||loạiMụcKiểu=='i'){long long dữLiệuTạm=kýTựRộngKiểu?va_arg(cácĐốiSốBiếnĐốiSố,long long):va_arg(cácĐốiSốBiếnĐốiSố,int);âm=dữLiệuTạm<0;giáTrị=âm?0-(unsigned long long)dữLiệuTạm:dữLiệuTạm;}
            else giáTrị=loạiMụcKiểu=='p'?(uintptr_t)va_arg(cácĐốiSốBiếnĐốiSố,void*):kýTựRộngKiểu?va_arg(cácĐốiSốBiếnĐốiSố,unsigned long long):va_arg(cácĐốiSốBiếnĐốiSố,unsigned);
            unsigned giáTrịNền=loạiMụcKiểu=='x'||loạiMụcKiểu=='X'||loạiMụcKiểu=='p'?16:loạiMụcKiểu=='o'?8:10;char sốLượngChữSố[64];unsigned sứcChứaĐãDùng=0;
            do{sốLượngChữSố[sứcChứaĐãDùng++]="0123456789abcdef"[giáTrị%giáTrịNền];giáTrị/=giáTrịNền;}while(giáTrị);
            if(âm)lưuTrữBộĐệm[sốLượngPhầnMục++]='-';if(loạiMụcKiểu=='p'||(giáTrịDựPhòng&&giáTrịNền==16)){lưuTrữBộĐệm[sốLượngPhầnMục++]='0';lưuTrữBộĐệm[sốLượngPhầnMục++]='x';}
            for(int lấpGiáTrị=(int)sứcChứaĐãDùng;giáTrịĐộChínhXác>lấpGiáTrị&&sốLượngPhầnMục<sizeof(lưuTrữBộĐệm)-sứcChứaĐãDùng;lấpGiáTrị++)lưuTrữBộĐệm[sốLượngPhầnMục++]='0';
            if(giáTrịKhôngSố&&!bênTrái&&giáTrịĐộChínhXác<0)while(giáTrịRộng>(int)(sốLượngPhầnMục+sứcChứaĐãDùng)&&sốLượngPhầnMục<sizeof(lưuTrữBộĐệm)-sứcChứaĐãDùng)lưuTrữBộĐệm[sốLượngPhầnMục++]='0';
            while(sứcChứaĐãDùng)lưuTrữBộĐệm[sốLượngPhầnMục++]=sốLượngChữSố[--sứcChứaĐãDùng];
        }else{lưuTrữBộĐệm[0]='?';sốLượngPhầnMục=1;}
        if(giáTrịRộng>4096)giáTrịRộng=4096;while(!bênTrái&&giáTrịRộng>(int)sốLượngPhầnMục){đặtGiáTrị(dữLiệuKếtQuả,tốiĐaSứcChứa,&vịTríHiệnTại,' ');giáTrịRộng--;}
        for(size_t chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++)đặtGiáTrị(dữLiệuKếtQuả,tốiĐaSứcChứa,&vịTríHiệnTại,dữLiệuChuỗi[chỉSốThứBậc]);while(bênTrái&&giáTrịRộng>(int)sốLượngPhầnMục){đặtGiáTrị(dữLiệuKếtQuả,tốiĐaSứcChứa,&vịTríHiệnTại,' ');giáTrịRộng--;}
    }if(tốiĐaSứcChứa)dữLiệuKếtQuả[vịTríHiệnTại<tốiĐaSứcChứa?vịTríHiệnTại:tốiĐaSứcChứa-1]=0;return vịTríHiệnTại;
}
int snprintf(char*dữLiệuKếtQuả,size_t tốiĐaSứcChứa,const char*mụcTệp,...){va_list giáTrịĐầuTiên;va_start(giáTrịĐầuTiên,mụcTệp);int giáTrịĐãTrảVề=vsnprintf(dữLiệuKếtQuả,tốiĐaSứcChứa,mụcTệp,giáTrịĐầuTiên);va_end(giáTrịĐầuTiên);return giáTrịĐãTrảVề;}
int sprintf(char*dữLiệuKếtQuả,const char*mụcTệp,...){va_list giáTrịĐầuTiên;va_start(giáTrịĐầuTiên,mụcTệp);int giáTrịĐãTrảVề=vsnprintf(dữLiệuKếtQuả,SIZE_MAX,mụcTệp,giáTrịĐầuTiên);va_end(giáTrịĐầuTiên);return giáTrịĐãTrảVề;}
int vfprintf(FILE*giáTrịLuồng,const char*mụcTệp,va_list giáTrịĐầuTiên){char giáTrịThứHai[2048];int sốLượngPhầnMục=vsnprintf(giáTrịThứHai,sizeof(giáTrịThứHai),mụcTệp,giáTrịĐầuTiên);if(sốLượngPhầnMục>2047)sốLượngPhầnMục=2047;return fwrite(giáTrịThứHai,1,sốLượngPhầnMục,giáTrịLuồng)==(size_t)sốLượngPhầnMục?sốLượngPhầnMục:-1;}
int fprintf(FILE*giáTrịLuồng,const char*mụcTệp,...){va_list giáTrịĐầuTiên;va_start(giáTrịĐầuTiên,mụcTệp);int giáTrịĐãTrảVề=vfprintf(giáTrịLuồng,mụcTệp,giáTrịĐầuTiên);va_end(giáTrịĐầuTiên);return giáTrịĐãTrảVề;}
int printf(const char*mụcTệp,...){va_list giáTrịĐầuTiên;va_start(giáTrịĐầuTiên,mụcTệp);int giáTrịĐãTrảVề=vfprintf(stdout,mụcTệp,giáTrịĐầuTiên);va_end(giáTrịĐầuTiên);return giáTrịĐãTrảVề;}
