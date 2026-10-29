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
static int àṣìṣe;
int *__errno_location(void){return &àṣìṣe;}
void exit(int ipò_iye){사용자호출(6,ipò_iye,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *ṣàyẹ̀wò_ìsọ̀rọ̀sí,const char *Fáìlì,unsigned ìlà,const char *ìlànà_ìgbéwọlé_orúkọ){fprintf(stderr,"cc assertion: %s %s:%u %s\n",ṣàyẹ̀wò_ìsọ̀rọ̀sí,Fáìlì,ìlà,ìlànà_ìgbéwọlé_orúkọ);exit(1);}
size_t strlen(const char*fọ́nrán_détà){const char*자료위치=fọ́nrán_détà;while(*자료위치)자료위치++;return 자료위치-fọ́nrán_détà;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char ibi_ìtọ́kasí_x=*첫째값++,세로좌표=*둘째값++;if(ibi_ìtọ́kasí_x!=세로좌표)return ibi_ìtọ́kasí_x-세로좌표;if(!ibi_ìtọ́kasí_x)return 0;}return 0;}
char *strcpy(char*èbúté_détà,const char*fọ́nrán_détà){char*반환값=èbúté_détà;while((*èbúté_détà++=*fọ́nrán_détà++)){}return 반환값;}
char *strchr(const char*fọ́nrán_détà,int kóòdù_ẹyọ_ọ̀rọ̀){do{if(*fọ́nrán_détà==(char)kóòdù_ẹyọ_ọ̀rọ̀)return (char*)fọ́nrán_détà;}while(*fọ́nrán_détà++);return 0;}
char *strrchr(const char*fọ́nrán_détà,int kóòdù_ẹyọ_ọ̀rọ̀){const char*반환값=0;do{if(*fọ́nrán_détà==(char)kóòdù_ẹyọ_ọ̀rọ̀)반환값=fọ́nrán_détà;}while(*fọ́nrán_détà++);return (char*)반환값;}
char *strstr(const char*fọ́nrán_détà,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*fọ́nrán_détà;fọ́nrán_détà++)if(!strncmp(fọ́nrán_détà,터미널항목,개수))return (char*)fọ́nrán_détà;return 개수?0:(char*)fọ́nrán_détà;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*ibi_ìtọ́kasí_x=첫째값,*세로좌표=둘째값;while(개수--){if(*ibi_ìtọ́kasí_x!=*세로좌표)return *ibi_ìtọ́kasí_x-*세로좌표;ibi_ìtọ́kasí_x++;세로좌표++;}return 0;}
void *memmove(void*èbúté_détà,const void*fọ́nrán_détà,size_t 개수){unsigned char*ibi_ìtọ́kasí_x=èbúté_détà;const unsigned char*세로좌표=fọ́nrán_détà;if(ibi_ìtọ́kasí_x<세로좌표){for(size_t 순번=0;순번<개수;순번++)ibi_ìtọ́kasí_x[순번]=세로좌표[순번];}else while(개수){개수--;ibi_ìtọ́kasí_x[개수]=세로좌표[개수];}return èbúté_détà;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct détà_sèdíwọ {size_t Ìwọ̀n;struct détà_sèdíwọ*다음;int 남은공간;int 채울크기;uint64_t ìmúdọ́gba_ìkẹ́kọ̀ọ́;} détà_sèdíwọ;
static détà_sèdíwọ *첫항목;
void free(void*자료위치){if(!자료위치)return;détà_sèdíwọ*둘째값=(détà_sèdíwọ*)자료위치-1;둘째값->남은공간=1;for(détà_sèdíwọ*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->Ìwọ̀n+=sizeof(détà_sèdíwọ)+다음위치->다음->Ìwọ̀n;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(détà_sèdíwọ))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(détà_sèdíwọ*)할당마당;첫항목->Ìwọ̀n=sizeof(할당마당)-sizeof(détà_sèdíwọ);첫항목->남은공간=1;첫항목->다음=0;}
    détà_sèdíwọ*이전=자료위치?(détà_sèdíwọ*)자료위치-1:0;if(이전&&이전->Ìwọ̀n>=개수)return 자료위치;
    for(détà_sèdíwọ*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->Ìwọ̀n>=개수){
        if(둘째값->Ìwọ̀n>=개수+sizeof(détà_sèdíwọ)+16){détà_sèdíwọ*나머지부분=(détà_sèdíwọ*)((unsigned char*)(둘째값+1)+개수);나머지부분->Ìwọ̀n=둘째값->Ìwọ̀n-개수-sizeof(détà_sèdíwọ);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->Ìwọ̀n=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->Ìwọ̀n);free(자료위치);}return 반환값;
    }àṣìṣe=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t fọ́nrán_détà){if(fọ́nrán_détà&&개수>SIZE_MAX/fọ́nrán_détà)return 0;void*자료위치=malloc(개수*fọ́nrán_détà);if(자료위치)memset(자료위치,0,개수*fọ́nrán_détà);return 자료위치;}
unsigned long long strtoull(const char*fọ́nrán_détà,char**parí_Ìtayọ,int Àgbétẹ́lẹ̀_iye){
    const char*bẹ̀rẹ̀_Ìtayọ=fọ́nrán_détà;while(*fọ́nrán_détà==' '||(*fọ́nrán_détà>=9&&*fọ́nrán_détà<=13))fọ́nrán_détà++;int 음수여부=0;if(*fọ́nrán_détà=='-'||*fọ́nrán_détà=='+')음수여부=*fọ́nrán_détà++=='-';
    if((!Àgbétẹ́lẹ̀_iye||Àgbétẹ́lẹ̀_iye==16)&&fọ́nrán_détà[0]=='0'&&(fọ́nrán_détà[1]=='x'||fọ́nrán_détà[1]=='X')){Àgbétẹ́lẹ̀_iye=16;fọ́nrán_détà+=2;}if(!Àgbétẹ́lẹ̀_iye)Àgbétẹ́lẹ̀_iye=*fọ́nrán_détà=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kóòdù_ẹyọ_ọ̀rọ̀=*fọ́nrán_détà,èbúté_détà=kóòdù_ẹyọ_ọ̀rọ̀>='0'&&kóòdù_ẹyọ_ọ̀rọ̀<='9'?kóòdù_ẹyọ_ọ̀rọ̀-'0':kóòdù_ẹyọ_ọ̀rọ̀>='a'&&kóòdù_ẹyọ_ọ̀rọ̀<='z'?kóòdù_ẹyọ_ọ̀rọ̀-'a'+10:kóòdù_ẹyọ_ọ̀rọ̀>='A'&&kóòdù_ẹyọ_ọ̀rọ̀<='Z'?kóòdù_ẹyọ_ọ̀rọ̀-'A'+10:99;if(èbúté_détà>=(unsigned)Àgbétẹ́lẹ̀_iye)break;하나라도=1;fọ́nrán_détà++;if(임시값>(~0ull-èbúté_détà)/(unsigned)Àgbétẹ́lẹ̀_iye){임시값=~0ull;àṣìṣe=34;}else 임시값=임시값*Àgbétẹ́lẹ̀_iye+èbúté_détà;}
    if(parí_Ìtayọ)*parí_Ìtayọ=(char*)(하나라도?fọ́nrán_détà:bẹ̀rẹ̀_Ìtayọ);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*fọ́nrán_détà,char**보조항목,int 둘째값){return strtoull(fọ́nrán_détà,보조항목,둘째값);}
long strtol(const char*fọ́nrán_détà,char**보조항목,int 둘째값){return (long)strtoull(fọ́nrán_détà,보조항목,둘째값);}
int atoi(const char*fọ́nrán_détà){return (int)strtol(fọ́nrán_détà,0,10);}
long double ldexpl(long double ibi_ìtọ́kasí_x,int 개수){while(개수>0){ibi_ìtọ́kasí_x*=2;개수--;}while(개수<0){ibi_ìtọ́kasí_x/=2;개수++;}return ibi_ìtọ́kasí_x;}
long double strtold(const char*fọ́nrán_détà,char**parí_Ìtayọ){
    const char*bẹ̀rẹ̀_Ìtayọ=fọ́nrán_détà;while(*fọ́nrán_détà==' '||(*fọ́nrán_détà>=9&&*fọ́nrán_détà<=13))fọ́nrán_détà++;int 음수여부=0;if(*fọ́nrán_détà=='-'||*fọ́nrán_détà=='+')음수여부=*fọ́nrán_détà++=='-';
    int Àgbétẹ́lẹ̀_iye=10;if(fọ́nrán_détà[0]=='0'&&(fọ́nrán_détà[1]=='x'||fọ́nrán_détà[1]=='X')){Àgbétẹ́lẹ̀_iye=16;fọ́nrán_détà+=2;}long double 임시값=0,ṣe_nírégí=1;int 소수부=0,하나라도=0;
    for(;;){int kóòdù_ẹyọ_ọ̀rọ̀=*fọ́nrán_détà,èbúté_détà=kóòdù_ẹyọ_ọ̀rọ̀>='0'&&kóòdù_ẹyọ_ọ̀rọ̀<='9'?kóòdù_ẹyọ_ọ̀rọ̀-'0':kóòdù_ẹyọ_ọ̀rọ̀>='a'&&kóòdù_ẹyọ_ọ̀rọ̀<='f'?kóòdù_ẹyọ_ọ̀rọ̀-'a'+10:kóòdù_ẹyọ_ọ̀rọ̀>='A'&&kóòdù_ẹyọ_ọ̀rọ̀<='F'?kóòdù_ẹyọ_ọ̀rọ̀-'A'+10:99;
        if(kóòdù_ẹyọ_ọ̀rọ̀=='.'&&!소수부){소수부=1;fọ́nrán_détà++;continue;}if(èbúté_détà>=Àgbétẹ́lẹ̀_iye)break;하나라도=1;fọ́nrán_détà++;임시값=임시값*Àgbétẹ́lẹ̀_iye+èbúté_détà;if(소수부)ṣe_nírégí*=Àgbétẹ́lẹ̀_iye;
    }임시값/=ṣe_nírégí;
    if((Àgbétẹ́lẹ̀_iye==10&&(*fọ́nrán_détà=='e'||*fọ́nrán_détà=='E'))||(Àgbétẹ́lẹ̀_iye==16&&(*fọ́nrán_détà=='p'||*fọ́nrán_détà=='P'))){const char*ṣàfihàn_iye=fọ́nrán_détà++;int 빼기=0;if(*fọ́nrán_détà=='-'||*fọ́nrán_détà=='+')빼기=*fọ́nrán_détà++=='-';int 개수=0,항목수=0;while(*fọ́nrán_détà>='0'&&*fọ́nrán_détà<='9'){항목수++;if(개수<20000)개수=개수*10+*fọ́nrán_détà-'0';fọ́nrán_détà++;}if(!항목수)fọ́nrán_détà=ṣàfihàn_iye;else{long double àsọmọ́gbè_nọ́ńbà=Àgbétẹ́lẹ̀_iye==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/àsọmọ́gbè_nọ́ńbà:임시값*àsọmọ́gbè_nọ́ńbà;}}
    if(parí_Ìtayọ)*parí_Ìtayọ=(char*)(하나라도?fọ́nrán_détà:bẹ̀rẹ̀_Ìtayọ);return 음수여부?-임시값:임시값;
}
double strtod(const char*fọ́nrán_détà,char**보조항목){return (double)strtold(fọ́nrán_détà,보조항목);}float strtof(const char*fọ́nrán_détà,char**보조항목){return (float)strtold(fọ́nrán_détà,보조항목);}
void qsort(void*Àgbétẹ́lẹ̀_iye,size_t 개수,size_t Ìwọ̀n,int(*fi_wé)(const void*,const void*)){
    unsigned char*자료위치=Àgbétẹ́lẹ̀_iye;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&fi_wé(자료위치+(안쪽순번-1)*Ìwọ̀n,자료위치+안쪽순번*Ìwọ̀n)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Ìwọ̀n;셋째순번++){unsigned char kóòdù_ẹyọ_ọ̀rọ̀=자료위치[(안쪽순번-1)*Ìwọ̀n+셋째순번];자료위치[(안쪽순번-1)*Ìwọ̀n+셋째순번]=자료위치[안쪽순번*Ìwọ̀n+셋째순번];자료위치[안쪽순번*Ìwọ̀n+셋째순번]=kóòdù_ẹyọ_ọ̀rọ̀;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*Orúkọ,int 설정비트,...){
    if(!strcmp(Orúkọ,"/@cc-output")){if(출력열림){àṣìṣe=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Orúkọ,번역기자원들[순번].Orúkọ)){
        if(설정비트&3){àṣìṣe=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}àṣìṣe=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Orúkọ,설정비트,0,0,0,0);if(반환값<0){àṣìṣe=-반환값;return -1;}return 반환값;
}
int close(int fáìlì_èkù){if(fáìlì_èkù==100){출력열림=0;return 0;}if(fáìlì_èkù>=128&&fáìlì_èkù<152){열림[fáìlì_èkù-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,fáìlì_èkù,0,0,0,0,0);if(반환값<0){àṣìṣe=-반환값;return -1;}return 0;}
long read(int fáìlì_èkù,void*détà,size_t 개수){
    if(fáìlì_èkù>=128&&fáìlì_èkù<152&&열림[fáìlì_èkù-128].사용량){int 순번=fáìlì_èkù-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->Ìwọ̀n-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(détà,반환값->détà+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,fáìlì_èkù,(uintptr_t)détà,개수,0,0,0);if(반환값<0){àṣìṣe=-반환값;return -1;}return 반환값;
}
long write(int fáìlì_èkù,const void*détà,size_t 개수){
    if(fáìlì_èkù==100){if(개수>sizeof(출력결과)-출력위치){àṣìṣe=28;return -1;}memcpy(출력결과+출력위치,détà,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,fáìlì_èkù,(uintptr_t)détà,개수,0,0,0);if(반환값<0){àṣìṣe=-반환값;return -1;}return 반환값;
}
long lseek(int fáìlì_èkù,long Ìtayọ_iye,int 기준점){
    if(fáìlì_èkù==100){long 자료위치=Ìtayọ_iye+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){àṣìṣe=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(fáìlì_èkù>=128&&fáìlì_èkù<152&&열림[fáìlì_èkù-128].사용량){int 순번=fáìlì_èkù-128;long 자료위치=Ìtayọ_iye+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].Ìwọ̀n);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].Ìwọ̀n){àṣìṣe=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,fáìlì_èkù,Ìtayọ_iye,기준점,0,0,0);if(반환값<0){àṣìṣe=-반환값;return -1;}return 반환값;
}
int unlink(const char*Orúkọ){intptr_t 반환값=사용자호출(11,(uintptr_t)Orúkọ,0,0,0,0,0);if(반환값<0){àṣìṣe=-반환값;return -1;}return 반환값;}
char *realpath(const char*Orúkọ,char*결과자료){if(!결과자료){결과자료=malloc(strlen(Orúkọ)+1);if(!결과자료)return 0;}return strcpy(결과자료,Orúkọ);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){àṣìṣe=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int fáìlì_èkù,const char*ìlànà_móòdù){(void)ìlànà_móòdù;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].àṣìṣe=0;흐름목록[순번].fáìlì_èkù=fáìlì_èkù;return &흐름목록[순번];}àṣìṣe=24;return 0;}
int fflush(FILE*fáìlì_ìgbéwọlé){return fáìlì_ìgbéwọlé&&fáìlì_ìgbéwọlé->àṣìṣe?-1:0;}
int fclose(FILE*fáìlì_ìgbéwọlé){int 반환값=close(fáìlì_ìgbéwọlé->fáìlì_èkù);if(fáìlì_ìgbéwọlé->àṣìṣe)반환값=-1;fáìlì_ìgbéwọlé->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t fọ́nrán_détà,size_t 개수,FILE*fáìlì_ìgbéwọlé){if(!fọ́nrán_détà)return 0;if(개수>SIZE_MAX/fọ́nrán_détà){fáìlì_ìgbéwọlé->àṣìṣe=1;return 0;}long 반환값=write(fáìlì_ìgbéwọlé->fáìlì_èkù,자료위치,fọ́nrán_détà*개수);if(반환값<0){fáìlì_ìgbéwọlé->àṣìṣe=1;return 0;}return (size_t)반환값/fọ́nrán_détà;}
int fputc(int kóòdù_ẹyọ_ọ̀rọ̀,FILE*fáìlì_ìgbéwọlé){unsigned char 둘째값=kóòdù_ẹyọ_ọ̀rọ̀;return fwrite(&둘째값,1,1,fáìlì_ìgbéwọlé)==1?둘째값:EOF;}
int fputs(const char*fọ́nrán_détà,FILE*fáìlì_ìgbéwọlé){return fwrite(fọ́nrán_détà,1,strlen(fọ́nrán_détà),fáìlì_ìgbéwọlé)==strlen(fọ́nrán_détà)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char kóòdù_ẹyọ_ọ̀rọ̀){if(*현재위치+1<용량한도)결과자료[*현재위치]=kóòdù_ẹyọ_ọ̀rọ̀;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*ìgúnrégé,va_list 가변인수){
    size_t 현재위치=0;while(*ìgúnrégé){if(*ìgúnrégé!='%'){넣기(결과자료,용량한도,&현재위치,*ìgúnrégé++);continue;}ìgúnrégé++;
        int 왼쪽=0,영값=0,대체값=0;while(*ìgúnrégé=='-'||*ìgúnrégé=='0'||*ìgúnrégé=='#'||*ìgúnrégé=='+'||*ìgúnrégé==' '){if(*ìgúnrégé=='-')왼쪽=1;if(*ìgúnrégé=='0')영값=1;if(*ìgúnrégé=='#')대체값=1;ìgúnrégé++;}
        int 너비=0,정밀도=-1;if(*ìgúnrégé=='*'){너비=va_arg(가변인수,int);ìgúnrégé++;}else while(*ìgúnrégé>='0'&&*ìgúnrégé<='9')너비=너비*10+*ìgúnrégé++-'0';
        if(*ìgúnrégé=='.'){ìgúnrégé++;정밀도=0;if(*ìgúnrégé=='*'){정밀도=va_arg(가변인수,int);ìgúnrégé++;}else while(*ìgúnrégé>='0'&&*ìgúnrégé<='9')정밀도=정밀도*10+*ìgúnrégé++-'0';}
        int 넓은글자=0;while(*ìgúnrégé=='l'||*ìgúnrégé=='z'||*ìgúnrégé=='t'||*ìgúnrégé=='j'||*ìgúnrégé=='h'){if(*ìgúnrégé!='h')넓은글자=1;ìgúnrégé++;}
        char irú_ìsọ̀rí=*ìgúnrégé?*ìgúnrégé++:0,àká_Ibi_ìpamọ́[80];const char*fọ́nrán_détà=àká_Ibi_ìpamọ́;size_t 개수=0;
        if(irú_ìsọ̀rí=='s'){fọ́nrán_détà=va_arg(가변인수,const char*);if(!fọ́nrán_détà)fọ́nrán_détà="(null)";개수=strlen(fọ́nrán_détà);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(irú_ìsọ̀rí=='c'){àká_Ibi_ìpamọ́[0]=va_arg(가변인수,int);개수=1;}
        else if(irú_ìsọ̀rí=='%'){àká_Ibi_ìpamọ́[0]='%';개수=1;}
        else if(irú_ìsọ̀rí=='d'||irú_ìsọ̀rí=='i'||irú_ìsọ̀rí=='u'||irú_ìsọ̀rí=='x'||irú_ìsọ̀rí=='X'||irú_ìsọ̀rí=='o'||irú_ìsọ̀rí=='p'){
            unsigned long long iye;int 음수표시=0;
            if(irú_ìsọ̀rí=='d'||irú_ìsọ̀rí=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;iye=음수표시?0-(unsigned long long)임시값:임시값;}
            else iye=irú_ìsọ̀rí=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Àgbétẹ́lẹ̀_iye=irú_ìsọ̀rí=='x'||irú_ìsọ̀rí=='X'||irú_ìsọ̀rí=='p'?16:irú_ìsọ̀rí=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[iye%Àgbétẹ́lẹ̀_iye];iye/=Àgbétẹ́lẹ̀_iye;}while(iye);
            if(음수표시)àká_Ibi_ìpamọ́[개수++]='-';if(irú_ìsọ̀rí=='p'||(대체값&&Àgbétẹ́lẹ̀_iye==16)){àká_Ibi_ìpamọ́[개수++]='0';àká_Ibi_ìpamọ́[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(àká_Ibi_ìpamọ́)-사용량;채움++)àká_Ibi_ìpamọ́[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(àká_Ibi_ìpamọ́)-사용량)àká_Ibi_ìpamọ́[개수++]='0';
            while(사용량)àká_Ibi_ìpamọ́[개수++]=숫자수[--사용량];
        }else{àká_Ibi_ìpamọ́[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,fọ́nrán_détà[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*fáìlì_ìgbéwọlé,...){va_list 첫째값;va_start(첫째값,fáìlì_ìgbéwọlé);int 반환값=vsnprintf(결과자료,용량한도,fáìlì_ìgbéwọlé,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*fáìlì_ìgbéwọlé,...){va_list 첫째값;va_start(첫째값,fáìlì_ìgbéwọlé);int 반환값=vsnprintf(결과자료,SIZE_MAX,fáìlì_ìgbéwọlé,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_iye,const char*fáìlì_ìgbéwọlé,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),fáìlì_ìgbéwọlé,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,Stream_iye)==(size_t)개수?개수:-1;}
int fprintf(FILE*Stream_iye,const char*fáìlì_ìgbéwọlé,...){va_list 첫째값;va_start(첫째값,fáìlì_ìgbéwọlé);int 반환값=vfprintf(Stream_iye,fáìlì_ìgbéwọlé,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*fáìlì_ìgbéwọlé,...){va_list 첫째값;va_start(첫째값,fáìlì_ìgbéwọlé);int 반환값=vfprintf(stdout,fáìlì_ìgbéwọlé,첫째값);va_end(첫째값);return 반환값;}
