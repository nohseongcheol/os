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
static int mmejọ;
int *__errno_location(void){return &mmejọ;}
void exit(int ọnọdụ_valuu){사용자호출(6,ọnọdụ_valuu,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *cheèk_njìekwu,const char *Faịlụ,unsigned ahịrī,const char *usoro_ndebà_akara_ahà){fprintf(stderr,"cc assertion: %s %s:%u %s\n",cheèk_njìekwu,Faịlụ,ahịrī,usoro_ndebà_akara_ahà);exit(1);}
size_t strlen(const char*ùsòròokwū_datà){const char*자료위치=ùsòròokwū_datà;while(*자료위치)자료위치++;return 자료위치-ùsòròokwū_datà;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char ngakọrịta_x=*첫째값++,세로좌표=*둘째값++;if(ngakọrịta_x!=세로좌표)return ngakọrịta_x-세로좌표;if(!ngakọrịta_x)return 0;}return 0;}
char *strcpy(char*ebemwèga_datà,const char*ùsòròokwū_datà){char*반환값=ebemwèga_datà;while((*ebemwèga_datà++=*ùsòròokwū_datà++)){}return 반환값;}
char *strchr(const char*ùsòròokwū_datà,int koòdù_nkeakàrà){do{if(*ùsòròokwū_datà==(char)koòdù_nkeakàrà)return (char*)ùsòròokwū_datà;}while(*ùsòròokwū_datà++);return 0;}
char *strrchr(const char*ùsòròokwū_datà,int koòdù_nkeakàrà){const char*반환값=0;do{if(*ùsòròokwū_datà==(char)koòdù_nkeakàrà)반환값=ùsòròokwū_datà;}while(*ùsòròokwū_datà++);return (char*)반환값;}
char *strstr(const char*ùsòròokwū_datà,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*ùsòròokwū_datà;ùsòròokwū_datà++)if(!strncmp(ùsòròokwū_datà,터미널항목,개수))return (char*)ùsòròokwū_datà;return 개수?0:(char*)ùsòròokwū_datà;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*ngakọrịta_x=첫째값,*세로좌표=둘째값;while(개수--){if(*ngakọrịta_x!=*세로좌표)return *ngakọrịta_x-*세로좌표;ngakọrịta_x++;세로좌표++;}return 0;}
void *memmove(void*ebemwèga_datà,const void*ùsòròokwū_datà,size_t 개수){unsigned char*ngakọrịta_x=ebemwèga_datà;const unsigned char*세로좌표=ùsòròokwū_datà;if(ngakọrịta_x<세로좌표){for(size_t 순번=0;순번<개수;순번++)ngakọrịta_x[순번]=세로좌표[순번];}else while(개수){개수--;ngakọrịta_x[개수]=세로좌표[개수];}return ebemwèga_datà;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct datà_gbochie {size_t Ụhara;struct datà_gbochie*다음;int 남은공간;int 채울크기;uint64_t nhàkọma_ihe_ọmụmụ;} datà_gbochie;
static datà_gbochie *첫항목;
void free(void*자료위치){if(!자료위치)return;datà_gbochie*둘째값=(datà_gbochie*)자료위치-1;둘째값->남은공간=1;for(datà_gbochie*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->Ụhara+=sizeof(datà_gbochie)+다음위치->다음->Ụhara;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(datà_gbochie))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(datà_gbochie*)할당마당;첫항목->Ụhara=sizeof(할당마당)-sizeof(datà_gbochie);첫항목->남은공간=1;첫항목->다음=0;}
    datà_gbochie*이전=자료위치?(datà_gbochie*)자료위치-1:0;if(이전&&이전->Ụhara>=개수)return 자료위치;
    for(datà_gbochie*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->Ụhara>=개수){
        if(둘째값->Ụhara>=개수+sizeof(datà_gbochie)+16){datà_gbochie*나머지부분=(datà_gbochie*)((unsigned char*)(둘째값+1)+개수);나머지부분->Ụhara=둘째값->Ụhara-개수-sizeof(datà_gbochie);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->Ụhara=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->Ụhara);free(자료위치);}return 반환값;
    }mmejọ=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t ùsòròokwū_datà){if(ùsòròokwū_datà&&개수>SIZE_MAX/ùsòròokwū_datà)return 0;void*자료위치=malloc(개수*ùsòròokwū_datà);if(자료위치)memset(자료위치,0,개수*ùsòròokwū_datà);return 자료위치;}
unsigned long long strtoull(const char*ùsòròokwū_datà,char**mèdebe_Nnokwata,int Bakgraụnd_valuu){
    const char*Mbido_Nnokwata=ùsòròokwū_datà;while(*ùsòròokwū_datà==' '||(*ùsòròokwū_datà>=9&&*ùsòròokwū_datà<=13))ùsòròokwū_datà++;int 음수여부=0;if(*ùsòròokwū_datà=='-'||*ùsòròokwū_datà=='+')음수여부=*ùsòròokwū_datà++=='-';
    if((!Bakgraụnd_valuu||Bakgraụnd_valuu==16)&&ùsòròokwū_datà[0]=='0'&&(ùsòròokwū_datà[1]=='x'||ùsòròokwū_datà[1]=='X')){Bakgraụnd_valuu=16;ùsòròokwū_datà+=2;}if(!Bakgraụnd_valuu)Bakgraụnd_valuu=*ùsòròokwū_datà=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned koòdù_nkeakàrà=*ùsòròokwū_datà,ebemwèga_datà=koòdù_nkeakàrà>='0'&&koòdù_nkeakàrà<='9'?koòdù_nkeakàrà-'0':koòdù_nkeakàrà>='a'&&koòdù_nkeakàrà<='z'?koòdù_nkeakàrà-'a'+10:koòdù_nkeakàrà>='A'&&koòdù_nkeakàrà<='Z'?koòdù_nkeakàrà-'A'+10:99;if(ebemwèga_datà>=(unsigned)Bakgraụnd_valuu)break;하나라도=1;ùsòròokwū_datà++;if(임시값>(~0ull-ebemwèga_datà)/(unsigned)Bakgraụnd_valuu){임시값=~0ull;mmejọ=34;}else 임시값=임시값*Bakgraụnd_valuu+ebemwèga_datà;}
    if(mèdebe_Nnokwata)*mèdebe_Nnokwata=(char*)(하나라도?ùsòròokwū_datà:Mbido_Nnokwata);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*ùsòròokwū_datà,char**보조항목,int 둘째값){return strtoull(ùsòròokwū_datà,보조항목,둘째값);}
long strtol(const char*ùsòròokwū_datà,char**보조항목,int 둘째값){return (long)strtoull(ùsòròokwū_datà,보조항목,둘째값);}
int atoi(const char*ùsòròokwū_datà){return (int)strtol(ùsòròokwū_datà,0,10);}
long double ldexpl(long double ngakọrịta_x,int 개수){while(개수>0){ngakọrịta_x*=2;개수--;}while(개수<0){ngakọrịta_x/=2;개수++;}return ngakọrịta_x;}
long double strtold(const char*ùsòròokwū_datà,char**mèdebe_Nnokwata){
    const char*Mbido_Nnokwata=ùsòròokwū_datà;while(*ùsòròokwū_datà==' '||(*ùsòròokwū_datà>=9&&*ùsòròokwū_datà<=13))ùsòròokwū_datà++;int 음수여부=0;if(*ùsòròokwū_datà=='-'||*ùsòròokwū_datà=='+')음수여부=*ùsòròokwū_datà++=='-';
    int Bakgraụnd_valuu=10;if(ùsòròokwū_datà[0]=='0'&&(ùsòròokwū_datà[1]=='x'||ùsòròokwū_datà[1]=='X')){Bakgraụnd_valuu=16;ùsòròokwū_datà+=2;}long double 임시값=0,sihàa=1;int 소수부=0,하나라도=0;
    for(;;){int koòdù_nkeakàrà=*ùsòròokwū_datà,ebemwèga_datà=koòdù_nkeakàrà>='0'&&koòdù_nkeakàrà<='9'?koòdù_nkeakàrà-'0':koòdù_nkeakàrà>='a'&&koòdù_nkeakàrà<='f'?koòdù_nkeakàrà-'a'+10:koòdù_nkeakàrà>='A'&&koòdù_nkeakàrà<='F'?koòdù_nkeakàrà-'A'+10:99;
        if(koòdù_nkeakàrà=='.'&&!소수부){소수부=1;ùsòròokwū_datà++;continue;}if(ebemwèga_datà>=Bakgraụnd_valuu)break;하나라도=1;ùsòròokwū_datà++;임시값=임시값*Bakgraụnd_valuu+ebemwèga_datà;if(소수부)sihàa*=Bakgraụnd_valuu;
    }임시값/=sihàa;
    if((Bakgraụnd_valuu==10&&(*ùsòròokwū_datà=='e'||*ùsòròokwū_datà=='E'))||(Bakgraụnd_valuu==16&&(*ùsòròokwū_datà=='p'||*ùsòròokwū_datà=='P'))){const char*gòsi_valuu=ùsòròokwū_datà++;int 빼기=0;if(*ùsòròokwū_datà=='-'||*ùsòròokwū_datà=='+')빼기=*ùsòròokwū_datà++=='-';int 개수=0,항목수=0;while(*ùsòròokwū_datà>='0'&&*ùsòròokwū_datà<='9'){항목수++;if(개수<20000)개수=개수*10+*ùsòròokwū_datà-'0';ùsòròokwū_datà++;}if(!항목수)ùsòròokwū_datà=gòsi_valuu;else{long double mụbara=Bakgraụnd_valuu==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/mụbara:임시값*mụbara;}}
    if(mèdebe_Nnokwata)*mèdebe_Nnokwata=(char*)(하나라도?ùsòròokwū_datà:Mbido_Nnokwata);return 음수여부?-임시값:임시값;
}
double strtod(const char*ùsòròokwū_datà,char**보조항목){return (double)strtold(ùsòròokwū_datà,보조항목);}float strtof(const char*ùsòròokwū_datà,char**보조항목){return (float)strtold(ùsòròokwū_datà,보조항목);}
void qsort(void*Bakgraụnd_valuu,size_t 개수,size_t Ụhara,int(*Tụlee)(const void*,const void*)){
    unsigned char*자료위치=Bakgraụnd_valuu;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Tụlee(자료위치+(안쪽순번-1)*Ụhara,자료위치+안쪽순번*Ụhara)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Ụhara;셋째순번++){unsigned char koòdù_nkeakàrà=자료위치[(안쪽순번-1)*Ụhara+셋째순번];자료위치[(안쪽순번-1)*Ụhara+셋째순번]=자료위치[안쪽순번*Ụhara+셋째순번];자료위치[안쪽순번*Ụhara+셋째순번]=koòdù_nkeakàrà;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*Aha,int 설정비트,...){
    if(!strcmp(Aha,"/@cc-output")){if(출력열림){mmejọ=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Aha,번역기자원들[순번].Aha)){
        if(설정비트&3){mmejọ=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}mmejọ=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Aha,설정비트,0,0,0,0);if(반환값<0){mmejọ=-반환값;return -1;}return 반환값;
}
int close(int ọbọakwụkwọ_ebenjìaka){if(ọbọakwụkwọ_ebenjìaka==100){출력열림=0;return 0;}if(ọbọakwụkwọ_ebenjìaka>=128&&ọbọakwụkwọ_ebenjìaka<152){열림[ọbọakwụkwọ_ebenjìaka-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,ọbọakwụkwọ_ebenjìaka,0,0,0,0,0);if(반환값<0){mmejọ=-반환값;return -1;}return 0;}
long read(int ọbọakwụkwọ_ebenjìaka,void*datà,size_t 개수){
    if(ọbọakwụkwọ_ebenjìaka>=128&&ọbọakwụkwọ_ebenjìaka<152&&열림[ọbọakwụkwọ_ebenjìaka-128].사용량){int 순번=ọbọakwụkwọ_ebenjìaka-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->Ụhara-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(datà,반환값->datà+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,ọbọakwụkwọ_ebenjìaka,(uintptr_t)datà,개수,0,0,0);if(반환값<0){mmejọ=-반환값;return -1;}return 반환값;
}
long write(int ọbọakwụkwọ_ebenjìaka,const void*datà,size_t 개수){
    if(ọbọakwụkwọ_ebenjìaka==100){if(개수>sizeof(출력결과)-출력위치){mmejọ=28;return -1;}memcpy(출력결과+출력위치,datà,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,ọbọakwụkwọ_ebenjìaka,(uintptr_t)datà,개수,0,0,0);if(반환값<0){mmejọ=-반환값;return -1;}return 반환값;
}
long lseek(int ọbọakwụkwọ_ebenjìaka,long Nnokwata_valuu,int 기준점){
    if(ọbọakwụkwọ_ebenjìaka==100){long 자료위치=Nnokwata_valuu+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){mmejọ=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(ọbọakwụkwọ_ebenjìaka>=128&&ọbọakwụkwọ_ebenjìaka<152&&열림[ọbọakwụkwọ_ebenjìaka-128].사용량){int 순번=ọbọakwụkwọ_ebenjìaka-128;long 자료위치=Nnokwata_valuu+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].Ụhara);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].Ụhara){mmejọ=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,ọbọakwụkwọ_ebenjìaka,Nnokwata_valuu,기준점,0,0,0);if(반환값<0){mmejọ=-반환값;return -1;}return 반환값;
}
int unlink(const char*Aha){intptr_t 반환값=사용자호출(11,(uintptr_t)Aha,0,0,0,0,0);if(반환값<0){mmejọ=-반환값;return -1;}return 반환값;}
char *realpath(const char*Aha,char*결과자료){if(!결과자료){결과자료=malloc(strlen(Aha)+1);if(!결과자료)return 0;}return strcpy(결과자료,Aha);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){mmejọ=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int ọbọakwụkwọ_ebenjìaka,const char*usoro_moòdù){(void)usoro_moòdù;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].mmejọ=0;흐름목록[순번].ọbọakwụkwọ_ebenjìaka=ọbọakwụkwọ_ebenjìaka;return &흐름목록[순번];}mmejọ=24;return 0;}
int fflush(FILE*ọbọakwụkwọ_ndebà){return ọbọakwụkwọ_ndebà&&ọbọakwụkwọ_ndebà->mmejọ?-1:0;}
int fclose(FILE*ọbọakwụkwọ_ndebà){int 반환값=close(ọbọakwụkwọ_ndebà->ọbọakwụkwọ_ebenjìaka);if(ọbọakwụkwọ_ndebà->mmejọ)반환값=-1;ọbọakwụkwọ_ndebà->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t ùsòròokwū_datà,size_t 개수,FILE*ọbọakwụkwọ_ndebà){if(!ùsòròokwū_datà)return 0;if(개수>SIZE_MAX/ùsòròokwū_datà){ọbọakwụkwọ_ndebà->mmejọ=1;return 0;}long 반환값=write(ọbọakwụkwọ_ndebà->ọbọakwụkwọ_ebenjìaka,자료위치,ùsòròokwū_datà*개수);if(반환값<0){ọbọakwụkwọ_ndebà->mmejọ=1;return 0;}return (size_t)반환값/ùsòròokwū_datà;}
int fputc(int koòdù_nkeakàrà,FILE*ọbọakwụkwọ_ndebà){unsigned char 둘째값=koòdù_nkeakàrà;return fwrite(&둘째값,1,1,ọbọakwụkwọ_ndebà)==1?둘째값:EOF;}
int fputs(const char*ùsòròokwū_datà,FILE*ọbọakwụkwọ_ndebà){return fwrite(ùsòròokwū_datà,1,strlen(ùsòròokwū_datà),ọbọakwụkwọ_ndebà)==strlen(ùsòròokwū_datà)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char koòdù_nkeakàrà){if(*현재위치+1<용량한도)결과자료[*현재위치]=koòdù_nkeakàrà;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*hàzie,va_list 가변인수){
    size_t 현재위치=0;while(*hàzie){if(*hàzie!='%'){넣기(결과자료,용량한도,&현재위치,*hàzie++);continue;}hàzie++;
        int 왼쪽=0,영값=0,대체값=0;while(*hàzie=='-'||*hàzie=='0'||*hàzie=='#'||*hàzie=='+'||*hàzie==' '){if(*hàzie=='-')왼쪽=1;if(*hàzie=='0')영값=1;if(*hàzie=='#')대체값=1;hàzie++;}
        int 너비=0,정밀도=-1;if(*hàzie=='*'){너비=va_arg(가변인수,int);hàzie++;}else while(*hàzie>='0'&&*hàzie<='9')너비=너비*10+*hàzie++-'0';
        if(*hàzie=='.'){hàzie++;정밀도=0;if(*hàzie=='*'){정밀도=va_arg(가변인수,int);hàzie++;}else while(*hàzie>='0'&&*hàzie<='9')정밀도=정밀도*10+*hàzie++-'0';}
        int 넓은글자=0;while(*hàzie=='l'||*hàzie=='z'||*hàzie=='t'||*hàzie=='j'||*hàzie=='h'){if(*hàzie!='h')넓은글자=1;hàzie++;}
        char pinye_otu=*hàzie?*hàzie++:0,ebenchekwatụ_Nchekwa[80];const char*ùsòròokwū_datà=ebenchekwatụ_Nchekwa;size_t 개수=0;
        if(pinye_otu=='s'){ùsòròokwū_datà=va_arg(가변인수,const char*);if(!ùsòròokwū_datà)ùsòròokwū_datà="(null)";개수=strlen(ùsòròokwū_datà);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(pinye_otu=='c'){ebenchekwatụ_Nchekwa[0]=va_arg(가변인수,int);개수=1;}
        else if(pinye_otu=='%'){ebenchekwatụ_Nchekwa[0]='%';개수=1;}
        else if(pinye_otu=='d'||pinye_otu=='i'||pinye_otu=='u'||pinye_otu=='x'||pinye_otu=='X'||pinye_otu=='o'||pinye_otu=='p'){
            unsigned long long valuu;int 음수표시=0;
            if(pinye_otu=='d'||pinye_otu=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;valuu=음수표시?0-(unsigned long long)임시값:임시값;}
            else valuu=pinye_otu=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Bakgraụnd_valuu=pinye_otu=='x'||pinye_otu=='X'||pinye_otu=='p'?16:pinye_otu=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[valuu%Bakgraụnd_valuu];valuu/=Bakgraụnd_valuu;}while(valuu);
            if(음수표시)ebenchekwatụ_Nchekwa[개수++]='-';if(pinye_otu=='p'||(대체값&&Bakgraụnd_valuu==16)){ebenchekwatụ_Nchekwa[개수++]='0';ebenchekwatụ_Nchekwa[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(ebenchekwatụ_Nchekwa)-사용량;채움++)ebenchekwatụ_Nchekwa[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(ebenchekwatụ_Nchekwa)-사용량)ebenchekwatụ_Nchekwa[개수++]='0';
            while(사용량)ebenchekwatụ_Nchekwa[개수++]=숫자수[--사용량];
        }else{ebenchekwatụ_Nchekwa[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,ùsòròokwū_datà[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*ọbọakwụkwọ_ndebà,...){va_list 첫째값;va_start(첫째값,ọbọakwụkwọ_ndebà);int 반환값=vsnprintf(결과자료,용량한도,ọbọakwụkwọ_ndebà,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*ọbọakwụkwọ_ndebà,...){va_list 첫째값;va_start(첫째값,ọbọakwụkwọ_ndebà);int 반환값=vsnprintf(결과자료,SIZE_MAX,ọbọakwụkwọ_ndebà,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*agịrị_valuu,const char*ọbọakwụkwọ_ndebà,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),ọbọakwụkwọ_ndebà,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,agịrị_valuu)==(size_t)개수?개수:-1;}
int fprintf(FILE*agịrị_valuu,const char*ọbọakwụkwọ_ndebà,...){va_list 첫째값;va_start(첫째값,ọbọakwụkwọ_ndebà);int 반환값=vfprintf(agịrị_valuu,ọbọakwụkwọ_ndebà,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*ọbọakwụkwọ_ndebà,...){va_list 첫째값;va_start(첫째값,ọbọakwụkwọ_ndebà);int 반환값=vfprintf(stdout,ọbọakwụkwọ_ndebà,첫째값);va_end(첫째값);return 반환값;}
