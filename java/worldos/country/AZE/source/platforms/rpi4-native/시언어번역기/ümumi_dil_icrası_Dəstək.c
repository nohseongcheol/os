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
static int XƏTA;
int *__errno_location(void){return &XƏTA;}
void exit(int vəziyyət_VALUE){사용자호출(6,vəziyyət_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *çek_ifadə,const char *FAYL,unsigned Giriş,const char *metod_daxiletmə_ad){fprintf(stderr,"cc assertion: %s %s:%u %s\n",çek_ifadə,FAYL,Giriş,metod_daxiletmə_ad);exit(1);}
size_t strlen(const char*sətir_verilənlər){const char*verilənlər_yerinə_qoymaq=sətir_verilənlər;while(*verilənlər_yerinə_qoymaq)verilənlər_yerinə_qoymaq++;return verilənlər_yerinə_qoymaq-sətir_verilənlər;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t element_COUNT){while(element_COUNT--){unsigned char x_koordinatı=*첫째값++,Y_koordinat=*SECOND_VALUE++;if(x_koordinatı!=Y_koordinat)return x_koordinatı-Y_koordinat;if(!x_koordinatı)return 0;}return 0;}
char *strcpy(char*təyinat_verilənlər,const char*sətir_verilənlər){char*반환값=təyinat_verilənlər;while((*təyinat_verilənlər++=*sətir_verilənlər++)){}return 반환값;}
char *strchr(const char*sətir_verilənlər,int simvol_kodu){do{if(*sətir_verilənlər==(char)simvol_kodu)return (char*)sətir_verilənlər;}while(*sətir_verilənlər++);return 0;}
char *strrchr(const char*sətir_verilənlər,int simvol_kodu){const char*반환값=0;do{if(*sətir_verilənlər==(char)simvol_kodu)반환값=sətir_verilənlər;}while(*sətir_verilənlər++);return (char*)반환값;}
char *strstr(const char*sətir_verilənlər,const char*Terminal_daxiletmə){size_t element_COUNT=strlen(Terminal_daxiletmə);for(;*sətir_verilənlər;sətir_verilənlər++)if(!strncmp(sətir_verilənlər,Terminal_daxiletmə,element_COUNT))return (char*)sətir_verilənlər;return element_COUNT?0:(char*)sətir_verilənlər;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t element_COUNT){const unsigned char*x_koordinatı=첫째값,*Y_koordinat=SECOND_VALUE;while(element_COUNT--){if(*x_koordinatı!=*Y_koordinat)return *x_koordinatı-*Y_koordinat;x_koordinatı++;Y_koordinat++;}return 0;}
void *memmove(void*təyinat_verilənlər,const void*sətir_verilənlər,size_t element_COUNT){unsigned char*x_koordinatı=təyinat_verilənlər;const unsigned char*Y_koordinat=sətir_verilənlər;if(x_koordinatı<Y_koordinat){for(size_t 순번=0;순번<element_COUNT;순번++)x_koordinatı[순번]=Y_koordinat[순번];}else while(element_COUNT){element_COUNT--;x_koordinatı[element_COUNT]=Y_koordinat[element_COUNT];}return təyinat_verilənlər;}
static unsigned char ayırma_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct verilənlər_blokla {size_t Böyüklük;struct verilənlər_blokla*Sonrakı_element;int 남은공간;int 채울크기;uint64_t düzləndirmə_dərs;} verilənlər_blokla;
static verilənlər_blokla *첫항목;
void free(void*verilənlər_yerinə_qoymaq){if(!verilənlər_yerinə_qoymaq)return;verilənlər_blokla*SECOND_VALUE=(verilənlər_blokla*)verilənlər_yerinə_qoymaq-1;SECOND_VALUE->남은공간=1;for(verilənlər_blokla*Sonrakı_OFFSET=첫항목;Sonrakı_OFFSET&&Sonrakı_OFFSET->Sonrakı_element;){if(Sonrakı_OFFSET->남은공간&&Sonrakı_OFFSET->Sonrakı_element->남은공간){Sonrakı_OFFSET->Böyüklük+=sizeof(verilənlər_blokla)+Sonrakı_OFFSET->Sonrakı_element->Böyüklük;Sonrakı_OFFSET->Sonrakı_element=Sonrakı_OFFSET->Sonrakı_element->Sonrakı_element;}else Sonrakı_OFFSET=Sonrakı_OFFSET->Sonrakı_element;}}
void *realloc(void*verilənlər_yerinə_qoymaq,size_t element_COUNT){
    if(!element_COUNT){free(verilənlər_yerinə_qoymaq);return 0;}if(element_COUNT>sizeof(ayırma_Arena)-sizeof(verilənlər_blokla))return 0;element_COUNT=(element_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(verilənlər_blokla*)ayırma_Arena;첫항목->Böyüklük=sizeof(ayırma_Arena)-sizeof(verilənlər_blokla);첫항목->남은공간=1;첫항목->Sonrakı_element=0;}
    verilənlər_blokla*이전=verilənlər_yerinə_qoymaq?(verilənlər_blokla*)verilənlər_yerinə_qoymaq-1:0;if(이전&&이전->Böyüklük>=element_COUNT)return verilənlər_yerinə_qoymaq;
    for(verilənlər_blokla*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Sonrakı_element)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Böyüklük>=element_COUNT){
        if(SECOND_VALUE->Böyüklük>=element_COUNT+sizeof(verilənlər_blokla)+16){verilənlər_blokla*나머지부분=(verilənlər_blokla*)((unsigned char*)(SECOND_VALUE+1)+element_COUNT);나머지부분->Böyüklük=SECOND_VALUE->Böyüklük-element_COUNT-sizeof(verilənlər_blokla);나머지부분->Sonrakı_element=SECOND_VALUE->Sonrakı_element;나머지부분->남은공간=1;SECOND_VALUE->Sonrakı_element=나머지부분;SECOND_VALUE->Böyüklük=element_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,verilənlər_yerinə_qoymaq,이전->Böyüklük);free(verilənlər_yerinə_qoymaq);}return 반환값;
    }XƏTA=12;return 0;
}
void *malloc(size_t element_COUNT){return realloc(0,element_COUNT);}
void *calloc(size_t element_COUNT,size_t sətir_verilənlər){if(sətir_verilənlər&&element_COUNT>SIZE_MAX/sətir_verilənlər)return 0;void*verilənlər_yerinə_qoymaq=malloc(element_COUNT*sətir_verilənlər);if(verilənlər_yerinə_qoymaq)memset(verilənlər_yerinə_qoymaq,0,element_COUNT*sətir_verilənlər);return verilənlər_yerinə_qoymaq;}
unsigned long long strtoull(const char*sətir_verilənlər,char**bitirmək_OFFSET,int Fon_VALUE){
    const char*Başla_OFFSET=sətir_verilənlər;while(*sətir_verilənlər==' '||(*sətir_verilənlər>=9&&*sətir_verilənlər<=13))sətir_verilənlər++;int 음수여부=0;if(*sətir_verilənlər=='-'||*sətir_verilənlər=='+')음수여부=*sətir_verilənlər++=='-';
    if((!Fon_VALUE||Fon_VALUE==16)&&sətir_verilənlər[0]=='0'&&(sətir_verilənlər[1]=='x'||sətir_verilənlər[1]=='X')){Fon_VALUE=16;sətir_verilənlər+=2;}if(!Fon_VALUE)Fon_VALUE=*sətir_verilənlər=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned simvol_kodu=*sətir_verilənlər,təyinat_verilənlər=simvol_kodu>='0'&&simvol_kodu<='9'?simvol_kodu-'0':simvol_kodu>='a'&&simvol_kodu<='z'?simvol_kodu-'a'+10:simvol_kodu>='A'&&simvol_kodu<='Z'?simvol_kodu-'A'+10:99;if(təyinat_verilənlər>=(unsigned)Fon_VALUE)break;하나라도=1;sətir_verilənlər++;if(임시값>(~0ull-təyinat_verilənlər)/(unsigned)Fon_VALUE){임시값=~0ull;XƏTA=34;}else 임시값=임시값*Fon_VALUE+təyinat_verilənlər;}
    if(bitirmək_OFFSET)*bitirmək_OFFSET=(char*)(하나라도?sətir_verilənlər:Başla_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*sətir_verilənlər,char**보조항목,int SECOND_VALUE){return strtoull(sətir_verilənlər,보조항목,SECOND_VALUE);}
long strtol(const char*sətir_verilənlər,char**보조항목,int SECOND_VALUE){return (long)strtoull(sətir_verilənlər,보조항목,SECOND_VALUE);}
int atoi(const char*sətir_verilənlər){return (int)strtol(sətir_verilənlər,0,10);}
long double ldexpl(long double x_koordinatı,int element_COUNT){while(element_COUNT>0){x_koordinatı*=2;element_COUNT--;}while(element_COUNT<0){x_koordinatı/=2;element_COUNT++;}return x_koordinatı;}
long double strtold(const char*sətir_verilənlər,char**bitirmək_OFFSET){
    const char*Başla_OFFSET=sətir_verilənlər;while(*sətir_verilənlər==' '||(*sətir_verilənlər>=9&&*sətir_verilənlər<=13))sətir_verilənlər++;int 음수여부=0;if(*sətir_verilənlər=='-'||*sətir_verilənlər=='+')음수여부=*sətir_verilənlər++=='-';
    int Fon_VALUE=10;if(sətir_verilənlər[0]=='0'&&(sətir_verilənlər[1]=='x'||sətir_verilənlər[1]=='X')){Fon_VALUE=16;sətir_verilənlər+=2;}long double 임시값=0,miqyaslamaq=1;int 소수부=0,하나라도=0;
    for(;;){int simvol_kodu=*sətir_verilənlər,təyinat_verilənlər=simvol_kodu>='0'&&simvol_kodu<='9'?simvol_kodu-'0':simvol_kodu>='a'&&simvol_kodu<='f'?simvol_kodu-'a'+10:simvol_kodu>='A'&&simvol_kodu<='F'?simvol_kodu-'A'+10:99;
        if(simvol_kodu=='.'&&!소수부){소수부=1;sətir_verilənlər++;continue;}if(təyinat_verilənlər>=Fon_VALUE)break;하나라도=1;sətir_verilənlər++;임시값=임시값*Fon_VALUE+təyinat_verilənlər;if(소수부)miqyaslamaq*=Fon_VALUE;
    }임시값/=miqyaslamaq;
    if((Fon_VALUE==10&&(*sətir_verilənlər=='e'||*sətir_verilənlər=='E'))||(Fon_VALUE==16&&(*sətir_verilənlər=='p'||*sətir_verilənlər=='P'))){const char*göstərmək_VALUE=sətir_verilənlər++;int 빼기=0;if(*sətir_verilənlər=='-'||*sətir_verilənlər=='+')빼기=*sətir_verilənlər++=='-';int element_COUNT=0,daxiletmə_COUNT=0;while(*sətir_verilənlər>='0'&&*sətir_verilənlər<='9'){daxiletmə_COUNT++;if(element_COUNT<20000)element_COUNT=element_COUNT*10+*sətir_verilənlər-'0';sətir_verilənlər++;}if(!daxiletmə_COUNT)sətir_verilənlər=göstərmək_VALUE;else{long double faktor=Fon_VALUE==16?2:10;while(element_COUNT-->0&&element_COUNT<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(bitirmək_OFFSET)*bitirmək_OFFSET=(char*)(하나라도?sətir_verilənlər:Başla_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*sətir_verilənlər,char**보조항목){return (double)strtold(sətir_verilənlər,보조항목);}float strtof(const char*sətir_verilənlər,char**보조항목){return (float)strtold(sətir_verilənlər,보조항목);}
void qsort(void*Fon_VALUE,size_t element_COUNT,size_t Böyüklük,int(*Müqayisə)(const void*,const void*)){
    unsigned char*verilənlər_yerinə_qoymaq=Fon_VALUE;for(size_t 순번=1;순번<element_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Müqayisə(verilənlər_yerinə_qoymaq+(안쪽순번-1)*Böyüklük,verilənlər_yerinə_qoymaq+안쪽순번*Böyüklük)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Böyüklük;셋째순번++){unsigned char simvol_kodu=verilənlər_yerinə_qoymaq[(안쪽순번-1)*Böyüklük+셋째순번];verilənlər_yerinə_qoymaq[(안쪽순번-1)*Böyüklük+셋째순번]=verilənlər_yerinə_qoymaq[안쪽순번*Böyüklük+셋째순번];verilənlər_yerinə_qoymaq[안쪽순번*Böyüklük+셋째순번]=simvol_kodu;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t yerinə_qoymaq;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *element_COUNT){*element_COUNT=출력크기;return 출력결과;}
int open(const char*Ad,int konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti,...){
    if(!strcmp(Ad,"/@cc-output")){if(출력열림){XƏTA=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Ad,번역기자원들[순번].Ad)){
        if(konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&3){XƏTA=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].yerinə_qoymaq=0;return 128+안쪽순번;}XƏTA=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Ad,konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti,0,0,0,0);if(반환값<0){XƏTA=-반환값;return -1;}return 반환값;
}
int close(int fayl_tutacaq){if(fayl_tutacaq==100){출력열림=0;return 0;}if(fayl_tutacaq>=128&&fayl_tutacaq<152){열림[fayl_tutacaq-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,fayl_tutacaq,0,0,0,0,0);if(반환값<0){XƏTA=-반환값;return -1;}return 0;}
long read(int fayl_tutacaq,void*verilənlər,size_t element_COUNT){
    if(fayl_tutacaq>=128&&fayl_tutacaq<152&&열림[fayl_tutacaq-128].사용량){int 순번=fayl_tutacaq-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Böyüklük-열림[순번].yerinə_qoymaq;if(element_COUNT>왼쪽)element_COUNT=왼쪽;memcpy(verilənlər,반환값->verilənlər+열림[순번].yerinə_qoymaq,element_COUNT);열림[순번].yerinə_qoymaq+=element_COUNT;return element_COUNT;}
    intptr_t 반환값=사용자호출(2,fayl_tutacaq,(uintptr_t)verilənlər,element_COUNT,0,0,0);if(반환값<0){XƏTA=-반환값;return -1;}return 반환값;
}
long write(int fayl_tutacaq,const void*verilənlər,size_t element_COUNT){
    if(fayl_tutacaq==100){if(element_COUNT>sizeof(출력결과)-출력위치){XƏTA=28;return -1;}memcpy(출력결과+출력위치,verilənlər,element_COUNT);출력위치+=element_COUNT;if(출력크기<출력위치)출력크기=출력위치;return element_COUNT;}
    intptr_t 반환값=사용자호출(1,fayl_tutacaq,(uintptr_t)verilənlər,element_COUNT,0,0,0);if(반환값<0){XƏTA=-반환값;return -1;}return 반환값;
}
long lseek(int fayl_tutacaq,long OFFSET_VALUE,int 기준점){
    if(fayl_tutacaq==100){long verilənlər_yerinə_qoymaq=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(verilənlər_yerinə_qoymaq<0||(size_t)verilənlər_yerinə_qoymaq>sizeof(출력결과)){XƏTA=22;return -1;}출력위치=verilənlər_yerinə_qoymaq;return verilənlər_yerinə_qoymaq;}
    if(fayl_tutacaq>=128&&fayl_tutacaq<152&&열림[fayl_tutacaq-128].사용량){int 순번=fayl_tutacaq-128;long verilənlər_yerinə_qoymaq=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].yerinə_qoymaq:번역기자원들[열림[순번].LOOKUP_INDEX].Böyüklük);if(verilənlər_yerinə_qoymaq<0||(size_t)verilənlər_yerinə_qoymaq>번역기자원들[열림[순번].LOOKUP_INDEX].Böyüklük){XƏTA=22;return -1;}열림[순번].yerinə_qoymaq=verilənlər_yerinə_qoymaq;return verilənlər_yerinə_qoymaq;}
    intptr_t 반환값=사용자호출(5,fayl_tutacaq,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){XƏTA=-반환값;return -1;}return 반환값;
}
int unlink(const char*Ad){intptr_t 반환값=사용자호출(11,(uintptr_t)Ad,0,0,0,0,0);if(반환값<0){XƏTA=-반환값;return -1;}return 반환값;}
char *realpath(const char*Ad,char*ölçü_verilənlər){if(!ölçü_verilənlər){ölçü_verilənlər=malloc(strlen(Ad)+1);if(!ölçü_verilənlər)return 0;}return strcpy(ölçü_verilənlər,Ad);}
char *getcwd(char*verilənlər_yerinə_qoymaq,size_t element_COUNT){if(element_COUNT<2){XƏTA=34;return 0;}verilənlər_yerinə_qoymaq[0]='/';verilənlər_yerinə_qoymaq[1]=0;return verilənlər_yerinə_qoymaq;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_daxiletmə){time_t 임시값=0;if(Terminal_daxiletmə)*Terminal_daxiletmə=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_daxiletmə){(void)Terminal_daxiletmə;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int fayl_tutacaq,const char*metod_MODE){(void)metod_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].XƏTA=0;흐름목록[순번].fayl_tutacaq=fayl_tutacaq;return &흐름목록[순번];}XƏTA=24;return 0;}
int fflush(FILE*fayl_daxiletmə){return fayl_daxiletmə&&fayl_daxiletmə->XƏTA?-1:0;}
int fclose(FILE*fayl_daxiletmə){int 반환값=close(fayl_daxiletmə->fayl_tutacaq);if(fayl_daxiletmə->XƏTA)반환값=-1;fayl_daxiletmə->사용량=0;return 반환값;}
size_t fwrite(const void*verilənlər_yerinə_qoymaq,size_t sətir_verilənlər,size_t element_COUNT,FILE*fayl_daxiletmə){if(!sətir_verilənlər)return 0;if(element_COUNT>SIZE_MAX/sətir_verilənlər){fayl_daxiletmə->XƏTA=1;return 0;}long 반환값=write(fayl_daxiletmə->fayl_tutacaq,verilənlər_yerinə_qoymaq,sətir_verilənlər*element_COUNT);if(반환값<0){fayl_daxiletmə->XƏTA=1;return 0;}return (size_t)반환값/sətir_verilənlər;}
int fputc(int simvol_kodu,FILE*fayl_daxiletmə){unsigned char SECOND_VALUE=simvol_kodu;return fwrite(&SECOND_VALUE,1,1,fayl_daxiletmə)==1?SECOND_VALUE:EOF;}
int fputs(const char*sətir_verilənlər,FILE*fayl_daxiletmə){return fwrite(sətir_verilənlər,1,strlen(sətir_verilənlər),fayl_daxiletmə)==strlen(sətir_verilənlər)?0:EOF;}
static void 넣기(char*ölçü_verilənlər,size_t 용량한도,size_t*현재위치,char simvol_kodu){if(*현재위치+1<용량한도)ölçü_verilənlər[*현재위치]=simvol_kodu;(*현재위치)++;}
int vsnprintf(char*ölçü_verilənlər,size_t 용량한도,const char*format,va_list 가변인수){
    size_t 현재위치=0;while(*format){if(*format!='%'){넣기(ölçü_verilənlər,용량한도,&현재위치,*format++);continue;}format++;
        int 왼쪽=0,영값=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')영값=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,정밀도=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;정밀도=0;if(*format=='*'){정밀도=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')정밀도=정밀도*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char TYPE_sahə=*format?*format++:0,bufer_Yaddaş[80];const char*sətir_verilənlər=bufer_Yaddaş;size_t element_COUNT=0;
        if(TYPE_sahə=='s'){sətir_verilənlər=va_arg(가변인수,const char*);if(!sətir_verilənlər)sətir_verilənlər="(null)";element_COUNT=strlen(sətir_verilənlər);if(정밀도>=0&&element_COUNT>(size_t)정밀도)element_COUNT=정밀도;}
        else if(TYPE_sahə=='c'){bufer_Yaddaş[0]=va_arg(가변인수,int);element_COUNT=1;}
        else if(TYPE_sahə=='%'){bufer_Yaddaş[0]='%';element_COUNT=1;}
        else if(TYPE_sahə=='d'||TYPE_sahə=='i'||TYPE_sahə=='u'||TYPE_sahə=='x'||TYPE_sahə=='X'||TYPE_sahə=='o'||TYPE_sahə=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_sahə=='d'||TYPE_sahə=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_sahə=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Fon_VALUE=TYPE_sahə=='x'||TYPE_sahə=='X'||TYPE_sahə=='p'?16:TYPE_sahə=='o'?8:10;char rəqəm_COUNT[64];unsigned 사용량=0;
            do{rəqəm_COUNT[사용량++]="0123456789abcdef"[VALUE%Fon_VALUE];VALUE/=Fon_VALUE;}while(VALUE);
            if(음수표시)bufer_Yaddaş[element_COUNT++]='-';if(TYPE_sahə=='p'||(대체값&&Fon_VALUE==16)){bufer_Yaddaş[element_COUNT++]='0';bufer_Yaddaş[element_COUNT++]='x';}
            for(int doldurmaq_VALUE=(int)사용량;정밀도>doldurmaq_VALUE&&element_COUNT<sizeof(bufer_Yaddaş)-사용량;doldurmaq_VALUE++)bufer_Yaddaş[element_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(element_COUNT+사용량)&&element_COUNT<sizeof(bufer_Yaddaş)-사용량)bufer_Yaddaş[element_COUNT++]='0';
            while(사용량)bufer_Yaddaş[element_COUNT++]=rəqəm_COUNT[--사용량];
        }else{bufer_Yaddaş[0]='?';element_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)element_COUNT){넣기(ölçü_verilənlər,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<element_COUNT;순번++)넣기(ölçü_verilənlər,용량한도,&현재위치,sətir_verilənlər[순번]);while(왼쪽&&너비>(int)element_COUNT){넣기(ölçü_verilənlər,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)ölçü_verilənlər[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*ölçü_verilənlər,size_t 용량한도,const char*fayl_daxiletmə,...){va_list 첫째값;va_start(첫째값,fayl_daxiletmə);int 반환값=vsnprintf(ölçü_verilənlər,용량한도,fayl_daxiletmə,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*ölçü_verilənlər,const char*fayl_daxiletmə,...){va_list 첫째값;va_start(첫째값,fayl_daxiletmə);int 반환값=vsnprintf(ölçü_verilənlər,SIZE_MAX,fayl_daxiletmə,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*axın_VALUE,const char*fayl_daxiletmə,va_list 첫째값){char SECOND_VALUE[2048];int element_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),fayl_daxiletmə,첫째값);if(element_COUNT>2047)element_COUNT=2047;return fwrite(SECOND_VALUE,1,element_COUNT,axın_VALUE)==(size_t)element_COUNT?element_COUNT:-1;}
int fprintf(FILE*axın_VALUE,const char*fayl_daxiletmə,...){va_list 첫째값;va_start(첫째값,fayl_daxiletmə);int 반환값=vfprintf(axın_VALUE,fayl_daxiletmə,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*fayl_daxiletmə,...){va_list 첫째값;va_start(첫째값,fayl_daxiletmə);int 반환값=vfprintf(stdout,fayl_daxiletmə,첫째값);va_end(첫째값);return 반환값;}
