#include "../명명/기계연결이름.h"
/* Freestanding compiler support. All file I/O goes through the native SVC ABI. */
#include "호출.h"
#include "stdio.h"
#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "resources.h"
static int hata;
int *__errno_location(void){return &hata;}
void exit(int Durum_değer){사용자호출(6,Durum_değer,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *çek_ifade,const char *dosya,unsigned girdi_satırı,const char *metot_girdi_ad){fprintf(stderr,"cc assertion: %s %s:%u %s\n",çek_ifade,dosya,girdi_satırı,metot_girdi_ad);exit(1);}
size_t strlen(const char*dize_veri){const char*veri_konum=dize_veri;while(*veri_konum)veri_konum++;return veri_konum-dize_veri;}
int strcmp(const char*첫째값,const char*SANİYE_değer){while(*첫째값&&*첫째값==*SANİYE_değer){첫째값++;SANİYE_değer++;}return (unsigned char)*첫째값-(unsigned char)*SANİYE_değer;}
int strncmp(const char*첫째값,const char*SANİYE_değer,size_t öğe_BAĞ_DEĞ_SAY){while(öğe_BAĞ_DEĞ_SAY--){unsigned char x_koordinatı=*첫째값++,Y_koordinat=*SANİYE_değer++;if(x_koordinatı!=Y_koordinat)return x_koordinatı-Y_koordinat;if(!x_koordinatı)return 0;}return 0;}
char *strcpy(char*hedef_veri,const char*dize_veri){char*반환값=hedef_veri;while((*hedef_veri++=*dize_veri++)){}return 반환값;}
char *strchr(const char*dize_veri,int kod_noktası){do{if(*dize_veri==(char)kod_noktası)return (char*)dize_veri;}while(*dize_veri++);return 0;}
char *strrchr(const char*dize_veri,int kod_noktası){const char*반환값=0;do{if(*dize_veri==(char)kod_noktası)반환값=dize_veri;}while(*dize_veri++);return (char*)반환값;}
char *strstr(const char*dize_veri,const char*Terminal_girdi){size_t öğe_BAĞ_DEĞ_SAY=strlen(Terminal_girdi);for(;*dize_veri;dize_veri++)if(!strncmp(dize_veri,Terminal_girdi,öğe_BAĞ_DEĞ_SAY))return (char*)dize_veri;return öğe_BAĞ_DEĞ_SAY?0:(char*)dize_veri;}
int memcmp(const void*첫째값,const void*SANİYE_değer,size_t öğe_BAĞ_DEĞ_SAY){const unsigned char*x_koordinatı=첫째값,*Y_koordinat=SANİYE_değer;while(öğe_BAĞ_DEĞ_SAY--){if(*x_koordinatı!=*Y_koordinat)return *x_koordinatı-*Y_koordinat;x_koordinatı++;Y_koordinat++;}return 0;}
void *memmove(void*hedef_veri,const void*dize_veri,size_t öğe_BAĞ_DEĞ_SAY){unsigned char*x_koordinatı=hedef_veri;const unsigned char*Y_koordinat=dize_veri;if(x_koordinatı<Y_koordinat){for(size_t 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++)x_koordinatı[순번]=Y_koordinat[순번];}else while(öğe_BAĞ_DEĞ_SAY){öğe_BAĞ_DEĞ_SAY--;x_koordinatı[öğe_BAĞ_DEĞ_SAY]=Y_koordinat[öğe_BAĞ_DEĞ_SAY];}return hedef_veri;}
static unsigned char ayırma_Alan[6*1024*1024] __attribute__((aligned(16)));
typedef struct veri_bloğu {size_t Boyut;struct veri_bloğu*Sonraki_öğe;int 남은공간;int doldurma;uint64_t hizalama_ders;} veri_bloğu;
static veri_bloğu *첫항목;
void free(void*veri_konum){if(!veri_konum)return;veri_bloğu*SANİYE_değer=(veri_bloğu*)veri_konum-1;SANİYE_değer->남은공간=1;for(veri_bloğu*Sonraki_Ofset=첫항목;Sonraki_Ofset&&Sonraki_Ofset->Sonraki_öğe;){if(Sonraki_Ofset->남은공간&&Sonraki_Ofset->Sonraki_öğe->남은공간){Sonraki_Ofset->Boyut+=sizeof(veri_bloğu)+Sonraki_Ofset->Sonraki_öğe->Boyut;Sonraki_Ofset->Sonraki_öğe=Sonraki_Ofset->Sonraki_öğe->Sonraki_öğe;}else Sonraki_Ofset=Sonraki_Ofset->Sonraki_öğe;}}
void *realloc(void*veri_konum,size_t öğe_BAĞ_DEĞ_SAY){
    if(!öğe_BAĞ_DEĞ_SAY){free(veri_konum);return 0;}if(öğe_BAĞ_DEĞ_SAY>sizeof(ayırma_Alan)-sizeof(veri_bloğu))return 0;öğe_BAĞ_DEĞ_SAY=(öğe_BAĞ_DEĞ_SAY+15)&~(size_t)15;
    if(!첫항목){첫항목=(veri_bloğu*)ayırma_Alan;첫항목->Boyut=sizeof(ayırma_Alan)-sizeof(veri_bloğu);첫항목->남은공간=1;첫항목->Sonraki_öğe=0;}
    veri_bloğu*Önceki_öğe=veri_konum?(veri_bloğu*)veri_konum-1:0;if(Önceki_öğe&&Önceki_öğe->Boyut>=öğe_BAĞ_DEĞ_SAY)return veri_konum;
    for(veri_bloğu*SANİYE_değer=첫항목;SANİYE_değer;SANİYE_değer=SANİYE_değer->Sonraki_öğe)if(SANİYE_değer->남은공간&&SANİYE_değer->Boyut>=öğe_BAĞ_DEĞ_SAY){
        if(SANİYE_değer->Boyut>=öğe_BAĞ_DEĞ_SAY+sizeof(veri_bloğu)+16){veri_bloğu*나머지부분=(veri_bloğu*)((unsigned char*)(SANİYE_değer+1)+öğe_BAĞ_DEĞ_SAY);나머지부분->Boyut=SANİYE_değer->Boyut-öğe_BAĞ_DEĞ_SAY-sizeof(veri_bloğu);나머지부분->Sonraki_öğe=SANİYE_değer->Sonraki_öğe;나머지부분->남은공간=1;SANİYE_değer->Sonraki_öğe=나머지부분;SANİYE_değer->Boyut=öğe_BAĞ_DEĞ_SAY;}
        SANİYE_değer->남은공간=0;void*반환값=SANİYE_değer+1;if(Önceki_öğe){memcpy(반환값,veri_konum,Önceki_öğe->Boyut);free(veri_konum);}return 반환값;
    }hata=12;return 0;
}
void *malloc(size_t öğe_BAĞ_DEĞ_SAY){return realloc(0,öğe_BAĞ_DEĞ_SAY);}
void *calloc(size_t öğe_BAĞ_DEĞ_SAY,size_t dize_veri){if(dize_veri&&öğe_BAĞ_DEĞ_SAY>SIZE_MAX/dize_veri)return 0;void*veri_konum=malloc(öğe_BAĞ_DEĞ_SAY*dize_veri);if(veri_konum)memset(veri_konum,0,öğe_BAĞ_DEĞ_SAY*dize_veri);return veri_konum;}
unsigned long long strtoull(const char*dize_veri,char**Bitiş_Ofset,int Arka_Plan_değer){
    const char*Start_Ofset=dize_veri;while(*dize_veri==' '||(*dize_veri>=9&&*dize_veri<=13))dize_veri++;int bilgi_teknolojisi_Negatif=0;if(*dize_veri=='-'||*dize_veri=='+')bilgi_teknolojisi_Negatif=*dize_veri++=='-';
    if((!Arka_Plan_değer||Arka_Plan_değer==16)&&dize_veri[0]=='0'&&(dize_veri[1]=='x'||dize_veri[1]=='X')){Arka_Plan_değer=16;dize_veri+=2;}if(!Arka_Plan_değer)Arka_Plan_değer=*dize_veri=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kod_noktası=*dize_veri,hedef_veri=kod_noktası>='0'&&kod_noktası<='9'?kod_noktası-'0':kod_noktası>='a'&&kod_noktası<='z'?kod_noktası-'a'+10:kod_noktası>='A'&&kod_noktası<='Z'?kod_noktası-'A'+10:99;if(hedef_veri>=(unsigned)Arka_Plan_değer)break;하나라도=1;dize_veri++;if(임시값>(~0ull-hedef_veri)/(unsigned)Arka_Plan_değer){임시값=~0ull;hata=34;}else 임시값=임시값*Arka_Plan_değer+hedef_veri;}
    if(Bitiş_Ofset)*Bitiş_Ofset=(char*)(하나라도?dize_veri:Start_Ofset);return bilgi_teknolojisi_Negatif?0-임시값:임시값;
}
unsigned long strtoul(const char*dize_veri,char**보조항목,int SANİYE_değer){return strtoull(dize_veri,보조항목,SANİYE_değer);}
long strtol(const char*dize_veri,char**보조항목,int SANİYE_değer){return (long)strtoull(dize_veri,보조항목,SANİYE_değer);}
int atoi(const char*dize_veri){return (int)strtol(dize_veri,0,10);}
long double ldexpl(long double x_koordinatı,int öğe_BAĞ_DEĞ_SAY){while(öğe_BAĞ_DEĞ_SAY>0){x_koordinatı*=2;öğe_BAĞ_DEĞ_SAY--;}while(öğe_BAĞ_DEĞ_SAY<0){x_koordinatı/=2;öğe_BAĞ_DEĞ_SAY++;}return x_koordinatı;}
long double strtold(const char*dize_veri,char**Bitiş_Ofset){
    const char*Start_Ofset=dize_veri;while(*dize_veri==' '||(*dize_veri>=9&&*dize_veri<=13))dize_veri++;int bilgi_teknolojisi_Negatif=0;if(*dize_veri=='-'||*dize_veri=='+')bilgi_teknolojisi_Negatif=*dize_veri++=='-';
    int Arka_Plan_değer=10;if(dize_veri[0]=='0'&&(dize_veri[1]=='x'||dize_veri[1]=='X')){Arka_Plan_değer=16;dize_veri+=2;}long double 임시값=0,ölçek=1;int 소수부=0,하나라도=0;
    for(;;){int kod_noktası=*dize_veri,hedef_veri=kod_noktası>='0'&&kod_noktası<='9'?kod_noktası-'0':kod_noktası>='a'&&kod_noktası<='f'?kod_noktası-'a'+10:kod_noktası>='A'&&kod_noktası<='F'?kod_noktası-'A'+10:99;
        if(kod_noktası=='.'&&!소수부){소수부=1;dize_veri++;continue;}if(hedef_veri>=Arka_Plan_değer)break;하나라도=1;dize_veri++;임시값=임시값*Arka_Plan_değer+hedef_veri;if(소수부)ölçek*=Arka_Plan_değer;
    }임시값/=ölçek;
    if((Arka_Plan_değer==10&&(*dize_veri=='e'||*dize_veri=='E'))||(Arka_Plan_değer==16&&(*dize_veri=='p'||*dize_veri=='P'))){const char*şov_değer=dize_veri++;int 빼기=0;if(*dize_veri=='-'||*dize_veri=='+')빼기=*dize_veri++=='-';int öğe_BAĞ_DEĞ_SAY=0,girdi_BAĞ_DEĞ_SAY=0;while(*dize_veri>='0'&&*dize_veri<='9'){girdi_BAĞ_DEĞ_SAY++;if(öğe_BAĞ_DEĞ_SAY<20000)öğe_BAĞ_DEĞ_SAY=öğe_BAĞ_DEĞ_SAY*10+*dize_veri-'0';dize_veri++;}if(!girdi_BAĞ_DEĞ_SAY)dize_veri=şov_değer;else{long double faktör=Arka_Plan_değer==16?2:10;while(öğe_BAĞ_DEĞ_SAY-->0&&öğe_BAĞ_DEĞ_SAY<200000)임시값=빼기?임시값/faktör:임시값*faktör;}}
    if(Bitiş_Ofset)*Bitiş_Ofset=(char*)(하나라도?dize_veri:Start_Ofset);return bilgi_teknolojisi_Negatif?-임시값:임시값;
}
double strtod(const char*dize_veri,char**보조항목){return (double)strtold(dize_veri,보조항목);}float strtof(const char*dize_veri,char**보조항목){return (float)strtold(dize_veri,보조항목);}
void qsort(void*Arka_Plan_değer,size_t öğe_BAĞ_DEĞ_SAY,size_t Boyut,int(*Karşılaştır)(const void*,const void*)){
    unsigned char*veri_konum=Arka_Plan_değer;for(size_t 순번=1;순번<öğe_BAĞ_DEĞ_SAY;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Karşılaştır(veri_konum+(안쪽순번-1)*Boyut,veri_konum+안쪽순번*Boyut)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Boyut;셋째순번++){unsigned char kod_noktası=veri_konum[(안쪽순번-1)*Boyut+셋째순번];veri_konum[(안쪽순번-1)*Boyut+셋째순번]=veri_konum[안쪽순번*Boyut+셋째순번];veri_konum[안쪽순번*Boyut+셋째순번]=kod_noktası;}
}
static struct {int 사용량,ARA_Dizin;size_t konum;} 열림[24];
static unsigned char çıktı[32768];static size_t çıktı_boyutlandırmak,çıktı_konum;static int çıktı_açık;
const unsigned char *C_çıktı(size_t *öğe_BAĞ_DEĞ_SAY){*öğe_BAĞ_DEĞ_SAY=çıktı_boyutlandırmak;return çıktı;}
int open(const char*İsim,int Yapılandırma_BITS,...){
    if(!strcmp(İsim,"/@cc-output")){if(çıktı_açık){hata=16;return -1;}çıktı_açık=1;çıktı_boyutlandırmak=çıktı_konum=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(derleyici_Kaynaklar)/sizeof(derleyici_Kaynaklar[0]);순번++)if(!strcmp(İsim,derleyici_Kaynaklar[순번].İsim)){
        if(Yapılandırma_BITS&3){hata=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].ARA_Dizin=순번;열림[안쪽순번].konum=0;return 128+안쪽순번;}hata=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)İsim,Yapılandırma_BITS,0,0,0,0);if(반환값<0){hata=-반환값;return -1;}return 반환값;
}
int close(int dosya_tanıtıcısı){if(dosya_tanıtıcısı==100){çıktı_açık=0;return 0;}if(dosya_tanıtıcısı>=128&&dosya_tanıtıcısı<152){열림[dosya_tanıtıcısı-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,dosya_tanıtıcısı,0,0,0,0,0);if(반환값<0){hata=-반환값;return -1;}return 0;}
long read(int dosya_tanıtıcısı,void*veri,size_t öğe_BAĞ_DEĞ_SAY){
    if(dosya_tanıtıcısı>=128&&dosya_tanıtıcısı<152&&열림[dosya_tanıtıcısı-128].사용량){int 순번=dosya_tanıtıcısı-128;const derleyici_kaynak*반환값=&derleyici_Kaynaklar[열림[순번].ARA_Dizin];size_t 왼쪽=반환값->Boyut-열림[순번].konum;if(öğe_BAĞ_DEĞ_SAY>왼쪽)öğe_BAĞ_DEĞ_SAY=왼쪽;memcpy(veri,반환값->veri+열림[순번].konum,öğe_BAĞ_DEĞ_SAY);열림[순번].konum+=öğe_BAĞ_DEĞ_SAY;return öğe_BAĞ_DEĞ_SAY;}
    intptr_t 반환값=사용자호출(2,dosya_tanıtıcısı,(uintptr_t)veri,öğe_BAĞ_DEĞ_SAY,0,0,0);if(반환값<0){hata=-반환값;return -1;}return 반환값;
}
long write(int dosya_tanıtıcısı,const void*veri,size_t öğe_BAĞ_DEĞ_SAY){
    if(dosya_tanıtıcısı==100){if(öğe_BAĞ_DEĞ_SAY>sizeof(çıktı)-çıktı_konum){hata=28;return -1;}memcpy(çıktı+çıktı_konum,veri,öğe_BAĞ_DEĞ_SAY);çıktı_konum+=öğe_BAĞ_DEĞ_SAY;if(çıktı_boyutlandırmak<çıktı_konum)çıktı_boyutlandırmak=çıktı_konum;return öğe_BAĞ_DEĞ_SAY;}
    intptr_t 반환값=사용자호출(1,dosya_tanıtıcısı,(uintptr_t)veri,öğe_BAĞ_DEĞ_SAY,0,0,0);if(반환값<0){hata=-반환값;return -1;}return 반환값;
}
long lseek(int dosya_tanıtıcısı,long Ofset_değer,int arama_origin){
    if(dosya_tanıtıcısı==100){long veri_konum=Ofset_değer+(arama_origin==0?0:arama_origin==1?çıktı_konum:çıktı_boyutlandırmak);if(veri_konum<0||(size_t)veri_konum>sizeof(çıktı)){hata=22;return -1;}çıktı_konum=veri_konum;return veri_konum;}
    if(dosya_tanıtıcısı>=128&&dosya_tanıtıcısı<152&&열림[dosya_tanıtıcısı-128].사용량){int 순번=dosya_tanıtıcısı-128;long veri_konum=Ofset_değer+(arama_origin==0?0:arama_origin==1?열림[순번].konum:derleyici_Kaynaklar[열림[순번].ARA_Dizin].Boyut);if(veri_konum<0||(size_t)veri_konum>derleyici_Kaynaklar[열림[순번].ARA_Dizin].Boyut){hata=22;return -1;}열림[순번].konum=veri_konum;return veri_konum;}
    intptr_t 반환값=사용자호출(5,dosya_tanıtıcısı,Ofset_değer,arama_origin,0,0,0);if(반환값<0){hata=-반환값;return -1;}return 반환값;
}
int unlink(const char*İsim){intptr_t 반환값=사용자호출(11,(uintptr_t)İsim,0,0,0,0,0);if(반환값<0){hata=-반환값;return -1;}return 반환값;}
char *realpath(const char*İsim,char*KR_veri){if(!KR_veri){KR_veri=malloc(strlen(İsim)+1);if(!KR_veri)return 0;}return strcpy(KR_veri,İsim);}
char *getcwd(char*veri_konum,size_t öğe_BAĞ_DEĞ_SAY){if(öğe_BAĞ_DEĞ_SAY<2){hata=34;return 0;}veri_konum[0]='/';veri_konum[1]=0;return veri_konum;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_girdi){time_t 임시값=0;if(Terminal_girdi)*Terminal_girdi=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_girdi){(void)Terminal_girdi;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Akışlar[18]={{1,0,1},{2,0,1}};FILE*stdout=&Akışlar[0],*stderr=&Akışlar[1];
FILE*fdopen(int dosya_tanıtıcısı,const char*metot_mod){(void)metot_mod;for(unsigned 순번=2;순번<18;순번++)if(!Akışlar[순번].사용량){Akışlar[순번].사용량=1;Akışlar[순번].hata=0;Akışlar[순번].dosya_tanıtıcısı=dosya_tanıtıcısı;return &Akışlar[순번];}hata=24;return 0;}
int fflush(FILE*Dosya_girdi){return Dosya_girdi&&Dosya_girdi->hata?-1:0;}
int fclose(FILE*Dosya_girdi){int 반환값=close(Dosya_girdi->dosya_tanıtıcısı);if(Dosya_girdi->hata)반환값=-1;Dosya_girdi->사용량=0;return 반환값;}
size_t fwrite(const void*veri_konum,size_t dize_veri,size_t öğe_BAĞ_DEĞ_SAY,FILE*Dosya_girdi){if(!dize_veri)return 0;if(öğe_BAĞ_DEĞ_SAY>SIZE_MAX/dize_veri){Dosya_girdi->hata=1;return 0;}long 반환값=write(Dosya_girdi->dosya_tanıtıcısı,veri_konum,dize_veri*öğe_BAĞ_DEĞ_SAY);if(반환값<0){Dosya_girdi->hata=1;return 0;}return (size_t)반환값/dize_veri;}
int fputc(int kod_noktası,FILE*Dosya_girdi){unsigned char SANİYE_değer=kod_noktası;return fwrite(&SANİYE_değer,1,1,Dosya_girdi)==1?SANİYE_değer:EOF;}
int fputs(const char*dize_veri,FILE*Dosya_girdi){return fwrite(dize_veri,1,strlen(dize_veri),Dosya_girdi)==strlen(dize_veri)?0:EOF;}
static void 넣기(char*KR_veri,size_t 용량한도,size_t*geçerli_konum,char kod_noktası){if(*geçerli_konum+1<용량한도)KR_veri[*geçerli_konum]=kod_noktası;(*geçerli_konum)++;}
int vsnprintf(char*KR_veri,size_t 용량한도,const char*biçim,va_list 가변인수){
    size_t geçerli_konum=0;while(*biçim){if(*biçim!='%'){넣기(KR_veri,용량한도,&geçerli_konum,*biçim++);continue;}biçim++;
        int 왼쪽=0,sıfır_değer=0,대체값=0;while(*biçim=='-'||*biçim=='0'||*biçim=='#'||*biçim=='+'||*biçim==' '){if(*biçim=='-')왼쪽=1;if(*biçim=='0')sıfır_değer=1;if(*biçim=='#')대체값=1;biçim++;}
        int 너비=0,duyarlık_değer=-1;if(*biçim=='*'){너비=va_arg(가변인수,int);biçim++;}else while(*biçim>='0'&&*biçim<='9')너비=너비*10+*biçim++-'0';
        if(*biçim=='.'){biçim++;duyarlık_değer=0;if(*biçim=='*'){duyarlık_değer=va_arg(가변인수,int);biçim++;}else while(*biçim>='0'&&*biçim<='9')duyarlık_değer=duyarlık_değer*10+*biçim++-'0';}
        int geniş_karakter=0;while(*biçim=='l'||*biçim=='z'||*biçim=='t'||*biçim=='j'||*biçim=='h'){if(*biçim!='h')geniş_karakter=1;biçim++;}
        char TÜR_alan=*biçim?*biçim++:0,arabellek_depolama_alanı[80];const char*dize_veri=arabellek_depolama_alanı;size_t öğe_BAĞ_DEĞ_SAY=0;
        if(TÜR_alan=='s'){dize_veri=va_arg(가변인수,const char*);if(!dize_veri)dize_veri="(null)";öğe_BAĞ_DEĞ_SAY=strlen(dize_veri);if(duyarlık_değer>=0&&öğe_BAĞ_DEĞ_SAY>(size_t)duyarlık_değer)öğe_BAĞ_DEĞ_SAY=duyarlık_değer;}
        else if(TÜR_alan=='c'){arabellek_depolama_alanı[0]=va_arg(가변인수,int);öğe_BAĞ_DEĞ_SAY=1;}
        else if(TÜR_alan=='%'){arabellek_depolama_alanı[0]='%';öğe_BAĞ_DEĞ_SAY=1;}
        else if(TÜR_alan=='d'||TÜR_alan=='i'||TÜR_alan=='u'||TÜR_alan=='x'||TÜR_alan=='X'||TÜR_alan=='o'||TÜR_alan=='p'){
            unsigned long long değer;int Negatif=0;
            if(TÜR_alan=='d'||TÜR_alan=='i'){long long 임시값=geniş_karakter?va_arg(가변인수,long long):va_arg(가변인수,int);Negatif=임시값<0;değer=Negatif?0-(unsigned long long)임시값:임시값;}
            else değer=TÜR_alan=='p'?(uintptr_t)va_arg(가변인수,void*):geniş_karakter?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Arka_Plan_değer=TÜR_alan=='x'||TÜR_alan=='X'||TÜR_alan=='p'?16:TÜR_alan=='o'?8:10;char rakam_BAĞ_DEĞ_SAY[64];unsigned 사용량=0;
            do{rakam_BAĞ_DEĞ_SAY[사용량++]="0123456789abcdef"[değer%Arka_Plan_değer];değer/=Arka_Plan_değer;}while(değer);
            if(Negatif)arabellek_depolama_alanı[öğe_BAĞ_DEĞ_SAY++]='-';if(TÜR_alan=='p'||(대체값&&Arka_Plan_değer==16)){arabellek_depolama_alanı[öğe_BAĞ_DEĞ_SAY++]='0';arabellek_depolama_alanı[öğe_BAĞ_DEĞ_SAY++]='x';}
            for(int dolgu_değer=(int)사용량;duyarlık_değer>dolgu_değer&&öğe_BAĞ_DEĞ_SAY<sizeof(arabellek_depolama_alanı)-사용량;dolgu_değer++)arabellek_depolama_alanı[öğe_BAĞ_DEĞ_SAY++]='0';
            if(sıfır_değer&&!왼쪽&&duyarlık_değer<0)while(너비>(int)(öğe_BAĞ_DEĞ_SAY+사용량)&&öğe_BAĞ_DEĞ_SAY<sizeof(arabellek_depolama_alanı)-사용량)arabellek_depolama_alanı[öğe_BAĞ_DEĞ_SAY++]='0';
            while(사용량)arabellek_depolama_alanı[öğe_BAĞ_DEĞ_SAY++]=rakam_BAĞ_DEĞ_SAY[--사용량];
        }else{arabellek_depolama_alanı[0]='?';öğe_BAĞ_DEĞ_SAY=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)öğe_BAĞ_DEĞ_SAY){넣기(KR_veri,용량한도,&geçerli_konum,' ');너비--;}
        for(size_t 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++)넣기(KR_veri,용량한도,&geçerli_konum,dize_veri[순번]);while(왼쪽&&너비>(int)öğe_BAĞ_DEĞ_SAY){넣기(KR_veri,용량한도,&geçerli_konum,' ');너비--;}
    }if(용량한도)KR_veri[geçerli_konum<용량한도?geçerli_konum:용량한도-1]=0;return geçerli_konum;
}
int snprintf(char*KR_veri,size_t 용량한도,const char*Dosya_girdi,...){va_list 첫째값;va_start(첫째값,Dosya_girdi);int 반환값=vsnprintf(KR_veri,용량한도,Dosya_girdi,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_veri,const char*Dosya_girdi,...){va_list 첫째값;va_start(첫째값,Dosya_girdi);int 반환값=vsnprintf(KR_veri,SIZE_MAX,Dosya_girdi,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*akış_değer,const char*Dosya_girdi,va_list 첫째값){char SANİYE_değer[2048];int öğe_BAĞ_DEĞ_SAY=vsnprintf(SANİYE_değer,sizeof(SANİYE_değer),Dosya_girdi,첫째값);if(öğe_BAĞ_DEĞ_SAY>2047)öğe_BAĞ_DEĞ_SAY=2047;return fwrite(SANİYE_değer,1,öğe_BAĞ_DEĞ_SAY,akış_değer)==(size_t)öğe_BAĞ_DEĞ_SAY?öğe_BAĞ_DEĞ_SAY:-1;}
int fprintf(FILE*akış_değer,const char*Dosya_girdi,...){va_list 첫째값;va_start(첫째값,Dosya_girdi);int 반환값=vfprintf(akış_değer,Dosya_girdi,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Dosya_girdi,...){va_list 첫째값;va_start(첫째값,Dosya_girdi);int 반환값=vfprintf(stdout,Dosya_girdi,첫째값);va_end(첫째값);return 반환값;}
