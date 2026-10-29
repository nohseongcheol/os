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
static int phoso;
int *__errno_location(void){return &phoso;}
void exit(int kemo_Boleng){사용자호출(6,kemo_Boleng,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *tlhola_Tlhaloso,const char *faele,unsigned Mola,const char *mokgwa_tsenyo_leina){fprintf(stderr,"cc assertion: %s %s:%u %s\n",tlhola_Tlhaloso,faele,Mola,mokgwa_tsenyo_leina);exit(1);}
size_t strlen(const char*dikwalwa_tshedimosetso){const char*자료위치=dikwalwa_tshedimosetso;while(*자료위치)자료위치++;return 자료위치-dikwalwa_tshedimosetso;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char kgokagano_ya_x=*첫째값++,세로좌표=*둘째값++;if(kgokagano_ya_x!=세로좌표)return kgokagano_ya_x-세로좌표;if(!kgokagano_ya_x)return 0;}return 0;}
char *strcpy(char*bogorogelo_tshedimosetso,const char*dikwalwa_tshedimosetso){char*반환값=bogorogelo_tshedimosetso;while((*bogorogelo_tshedimosetso++=*dikwalwa_tshedimosetso++)){}return 반환값;}
char *strchr(const char*dikwalwa_tshedimosetso,int khoutuletshwao){do{if(*dikwalwa_tshedimosetso==(char)khoutuletshwao)return (char*)dikwalwa_tshedimosetso;}while(*dikwalwa_tshedimosetso++);return 0;}
char *strrchr(const char*dikwalwa_tshedimosetso,int khoutuletshwao){const char*반환값=0;do{if(*dikwalwa_tshedimosetso==(char)khoutuletshwao)반환값=dikwalwa_tshedimosetso;}while(*dikwalwa_tshedimosetso++);return (char*)반환값;}
char *strstr(const char*dikwalwa_tshedimosetso,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*dikwalwa_tshedimosetso;dikwalwa_tshedimosetso++)if(!strncmp(dikwalwa_tshedimosetso,터미널항목,개수))return (char*)dikwalwa_tshedimosetso;return 개수?0:(char*)dikwalwa_tshedimosetso;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*kgokagano_ya_x=첫째값,*세로좌표=둘째값;while(개수--){if(*kgokagano_ya_x!=*세로좌표)return *kgokagano_ya_x-*세로좌표;kgokagano_ya_x++;세로좌표++;}return 0;}
void *memmove(void*bogorogelo_tshedimosetso,const void*dikwalwa_tshedimosetso,size_t 개수){unsigned char*kgokagano_ya_x=bogorogelo_tshedimosetso;const unsigned char*세로좌표=dikwalwa_tshedimosetso;if(kgokagano_ya_x<세로좌표){for(size_t 순번=0;순번<개수;순번++)kgokagano_ya_x[순번]=세로좌표[순번];}else while(개수){개수--;kgokagano_ya_x[개수]=세로좌표[개수];}return bogorogelo_tshedimosetso;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct tshedimosetso_thibela {size_t lekanya;struct tshedimosetso_thibela*다음;int 남은공간;int 채울크기;uint64_t tlhamalatso_thuto;} tshedimosetso_thibela;
static tshedimosetso_thibela *첫항목;
void free(void*자료위치){if(!자료위치)return;tshedimosetso_thibela*둘째값=(tshedimosetso_thibela*)자료위치-1;둘째값->남은공간=1;for(tshedimosetso_thibela*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->lekanya+=sizeof(tshedimosetso_thibela)+다음위치->다음->lekanya;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(tshedimosetso_thibela))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(tshedimosetso_thibela*)할당마당;첫항목->lekanya=sizeof(할당마당)-sizeof(tshedimosetso_thibela);첫항목->남은공간=1;첫항목->다음=0;}
    tshedimosetso_thibela*이전=자료위치?(tshedimosetso_thibela*)자료위치-1:0;if(이전&&이전->lekanya>=개수)return 자료위치;
    for(tshedimosetso_thibela*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->lekanya>=개수){
        if(둘째값->lekanya>=개수+sizeof(tshedimosetso_thibela)+16){tshedimosetso_thibela*나머지부분=(tshedimosetso_thibela*)((unsigned char*)(둘째값+1)+개수);나머지부분->lekanya=둘째값->lekanya-개수-sizeof(tshedimosetso_thibela);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->lekanya=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->lekanya);free(자료위치);}return 반환값;
    }phoso=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t dikwalwa_tshedimosetso){if(dikwalwa_tshedimosetso&&개수>SIZE_MAX/dikwalwa_tshedimosetso)return 0;void*자료위치=malloc(개수*dikwalwa_tshedimosetso);if(자료위치)memset(자료위치,0,개수*dikwalwa_tshedimosetso);return 자료위치;}
unsigned long long strtoull(const char*dikwalwa_tshedimosetso,char**kgaola_Baya_ka_Tekatekanyo,int Lemorago_Boleng){
    const char*simolola_Baya_ka_Tekatekanyo=dikwalwa_tshedimosetso;while(*dikwalwa_tshedimosetso==' '||(*dikwalwa_tshedimosetso>=9&&*dikwalwa_tshedimosetso<=13))dikwalwa_tshedimosetso++;int 음수여부=0;if(*dikwalwa_tshedimosetso=='-'||*dikwalwa_tshedimosetso=='+')음수여부=*dikwalwa_tshedimosetso++=='-';
    if((!Lemorago_Boleng||Lemorago_Boleng==16)&&dikwalwa_tshedimosetso[0]=='0'&&(dikwalwa_tshedimosetso[1]=='x'||dikwalwa_tshedimosetso[1]=='X')){Lemorago_Boleng=16;dikwalwa_tshedimosetso+=2;}if(!Lemorago_Boleng)Lemorago_Boleng=*dikwalwa_tshedimosetso=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned khoutuletshwao=*dikwalwa_tshedimosetso,bogorogelo_tshedimosetso=khoutuletshwao>='0'&&khoutuletshwao<='9'?khoutuletshwao-'0':khoutuletshwao>='a'&&khoutuletshwao<='z'?khoutuletshwao-'a'+10:khoutuletshwao>='A'&&khoutuletshwao<='Z'?khoutuletshwao-'A'+10:99;if(bogorogelo_tshedimosetso>=(unsigned)Lemorago_Boleng)break;하나라도=1;dikwalwa_tshedimosetso++;if(임시값>(~0ull-bogorogelo_tshedimosetso)/(unsigned)Lemorago_Boleng){임시값=~0ull;phoso=34;}else 임시값=임시값*Lemorago_Boleng+bogorogelo_tshedimosetso;}
    if(kgaola_Baya_ka_Tekatekanyo)*kgaola_Baya_ka_Tekatekanyo=(char*)(하나라도?dikwalwa_tshedimosetso:simolola_Baya_ka_Tekatekanyo);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*dikwalwa_tshedimosetso,char**보조항목,int 둘째값){return strtoull(dikwalwa_tshedimosetso,보조항목,둘째값);}
long strtol(const char*dikwalwa_tshedimosetso,char**보조항목,int 둘째값){return (long)strtoull(dikwalwa_tshedimosetso,보조항목,둘째값);}
int atoi(const char*dikwalwa_tshedimosetso){return (int)strtol(dikwalwa_tshedimosetso,0,10);}
long double ldexpl(long double kgokagano_ya_x,int 개수){while(개수>0){kgokagano_ya_x*=2;개수--;}while(개수<0){kgokagano_ya_x/=2;개수++;}return kgokagano_ya_x;}
long double strtold(const char*dikwalwa_tshedimosetso,char**kgaola_Baya_ka_Tekatekanyo){
    const char*simolola_Baya_ka_Tekatekanyo=dikwalwa_tshedimosetso;while(*dikwalwa_tshedimosetso==' '||(*dikwalwa_tshedimosetso>=9&&*dikwalwa_tshedimosetso<=13))dikwalwa_tshedimosetso++;int 음수여부=0;if(*dikwalwa_tshedimosetso=='-'||*dikwalwa_tshedimosetso=='+')음수여부=*dikwalwa_tshedimosetso++=='-';
    int Lemorago_Boleng=10;if(dikwalwa_tshedimosetso[0]=='0'&&(dikwalwa_tshedimosetso[1]=='x'||dikwalwa_tshedimosetso[1]=='X')){Lemorago_Boleng=16;dikwalwa_tshedimosetso+=2;}long double 임시값=0,Sekale=1;int 소수부=0,하나라도=0;
    for(;;){int khoutuletshwao=*dikwalwa_tshedimosetso,bogorogelo_tshedimosetso=khoutuletshwao>='0'&&khoutuletshwao<='9'?khoutuletshwao-'0':khoutuletshwao>='a'&&khoutuletshwao<='f'?khoutuletshwao-'a'+10:khoutuletshwao>='A'&&khoutuletshwao<='F'?khoutuletshwao-'A'+10:99;
        if(khoutuletshwao=='.'&&!소수부){소수부=1;dikwalwa_tshedimosetso++;continue;}if(bogorogelo_tshedimosetso>=Lemorago_Boleng)break;하나라도=1;dikwalwa_tshedimosetso++;임시값=임시값*Lemorago_Boleng+bogorogelo_tshedimosetso;if(소수부)Sekale*=Lemorago_Boleng;
    }임시값/=Sekale;
    if((Lemorago_Boleng==10&&(*dikwalwa_tshedimosetso=='e'||*dikwalwa_tshedimosetso=='E'))||(Lemorago_Boleng==16&&(*dikwalwa_tshedimosetso=='p'||*dikwalwa_tshedimosetso=='P'))){const char*bontsha_Boleng=dikwalwa_tshedimosetso++;int 빼기=0;if(*dikwalwa_tshedimosetso=='-'||*dikwalwa_tshedimosetso=='+')빼기=*dikwalwa_tshedimosetso++=='-';int 개수=0,항목수=0;while(*dikwalwa_tshedimosetso>='0'&&*dikwalwa_tshedimosetso<='9'){항목수++;if(개수<20000)개수=개수*10+*dikwalwa_tshedimosetso-'0';dikwalwa_tshedimosetso++;}if(!항목수)dikwalwa_tshedimosetso=bontsha_Boleng;else{long double palo_katiso=Lemorago_Boleng==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/palo_katiso:임시값*palo_katiso;}}
    if(kgaola_Baya_ka_Tekatekanyo)*kgaola_Baya_ka_Tekatekanyo=(char*)(하나라도?dikwalwa_tshedimosetso:simolola_Baya_ka_Tekatekanyo);return 음수여부?-임시값:임시값;
}
double strtod(const char*dikwalwa_tshedimosetso,char**보조항목){return (double)strtold(dikwalwa_tshedimosetso,보조항목);}float strtof(const char*dikwalwa_tshedimosetso,char**보조항목){return (float)strtold(dikwalwa_tshedimosetso,보조항목);}
void qsort(void*Lemorago_Boleng,size_t 개수,size_t lekanya,int(*Bapisa)(const void*,const void*)){
    unsigned char*자료위치=Lemorago_Boleng;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Bapisa(자료위치+(안쪽순번-1)*lekanya,자료위치+안쪽순번*lekanya)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<lekanya;셋째순번++){unsigned char khoutuletshwao=자료위치[(안쪽순번-1)*lekanya+셋째순번];자료위치[(안쪽순번-1)*lekanya+셋째순번]=자료위치[안쪽순번*lekanya+셋째순번];자료위치[안쪽순번*lekanya+셋째순번]=khoutuletshwao;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*leina,int 설정비트,...){
    if(!strcmp(leina,"/@cc-output")){if(출력열림){phoso=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(leina,번역기자원들[순번].leina)){
        if(설정비트&3){phoso=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}phoso=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)leina,설정비트,0,0,0,0);if(반환값<0){phoso=-반환값;return -1;}return 반환값;
}
int close(int faele_mokgwakamogelo){if(faele_mokgwakamogelo==100){출력열림=0;return 0;}if(faele_mokgwakamogelo>=128&&faele_mokgwakamogelo<152){열림[faele_mokgwakamogelo-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,faele_mokgwakamogelo,0,0,0,0,0);if(반환값<0){phoso=-반환값;return -1;}return 0;}
long read(int faele_mokgwakamogelo,void*tshedimosetso,size_t 개수){
    if(faele_mokgwakamogelo>=128&&faele_mokgwakamogelo<152&&열림[faele_mokgwakamogelo-128].사용량){int 순번=faele_mokgwakamogelo-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->lekanya-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(tshedimosetso,반환값->tshedimosetso+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,faele_mokgwakamogelo,(uintptr_t)tshedimosetso,개수,0,0,0);if(반환값<0){phoso=-반환값;return -1;}return 반환값;
}
long write(int faele_mokgwakamogelo,const void*tshedimosetso,size_t 개수){
    if(faele_mokgwakamogelo==100){if(개수>sizeof(출력결과)-출력위치){phoso=28;return -1;}memcpy(출력결과+출력위치,tshedimosetso,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,faele_mokgwakamogelo,(uintptr_t)tshedimosetso,개수,0,0,0);if(반환값<0){phoso=-반환값;return -1;}return 반환값;
}
long lseek(int faele_mokgwakamogelo,long Baya_ka_Tekatekanyo_Boleng,int 기준점){
    if(faele_mokgwakamogelo==100){long 자료위치=Baya_ka_Tekatekanyo_Boleng+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){phoso=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(faele_mokgwakamogelo>=128&&faele_mokgwakamogelo<152&&열림[faele_mokgwakamogelo-128].사용량){int 순번=faele_mokgwakamogelo-128;long 자료위치=Baya_ka_Tekatekanyo_Boleng+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].lekanya);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].lekanya){phoso=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,faele_mokgwakamogelo,Baya_ka_Tekatekanyo_Boleng,기준점,0,0,0);if(반환값<0){phoso=-반환값;return -1;}return 반환값;
}
int unlink(const char*leina){intptr_t 반환값=사용자호출(11,(uintptr_t)leina,0,0,0,0,0);if(반환값<0){phoso=-반환값;return -1;}return 반환값;}
char *realpath(const char*leina,char*결과자료){if(!결과자료){결과자료=malloc(strlen(leina)+1);if(!결과자료)return 0;}return strcpy(결과자료,leina);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){phoso=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int faele_mokgwakamogelo,const char*mokgwa_mokgwa){(void)mokgwa_mokgwa;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].phoso=0;흐름목록[순번].faele_mokgwakamogelo=faele_mokgwakamogelo;return &흐름목록[순번];}phoso=24;return 0;}
int fflush(FILE*faele_tsenyo){return faele_tsenyo&&faele_tsenyo->phoso?-1:0;}
int fclose(FILE*faele_tsenyo){int 반환값=close(faele_tsenyo->faele_mokgwakamogelo);if(faele_tsenyo->phoso)반환값=-1;faele_tsenyo->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t dikwalwa_tshedimosetso,size_t 개수,FILE*faele_tsenyo){if(!dikwalwa_tshedimosetso)return 0;if(개수>SIZE_MAX/dikwalwa_tshedimosetso){faele_tsenyo->phoso=1;return 0;}long 반환값=write(faele_tsenyo->faele_mokgwakamogelo,자료위치,dikwalwa_tshedimosetso*개수);if(반환값<0){faele_tsenyo->phoso=1;return 0;}return (size_t)반환값/dikwalwa_tshedimosetso;}
int fputc(int khoutuletshwao,FILE*faele_tsenyo){unsigned char 둘째값=khoutuletshwao;return fwrite(&둘째값,1,1,faele_tsenyo)==1?둘째값:EOF;}
int fputs(const char*dikwalwa_tshedimosetso,FILE*faele_tsenyo){return fwrite(dikwalwa_tshedimosetso,1,strlen(dikwalwa_tshedimosetso),faele_tsenyo)==strlen(dikwalwa_tshedimosetso)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char khoutuletshwao){if(*현재위치+1<용량한도)결과자료[*현재위치]=khoutuletshwao;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*fometa,va_list 가변인수){
    size_t 현재위치=0;while(*fometa){if(*fometa!='%'){넣기(결과자료,용량한도,&현재위치,*fometa++);continue;}fometa++;
        int 왼쪽=0,영값=0,대체값=0;while(*fometa=='-'||*fometa=='0'||*fometa=='#'||*fometa=='+'||*fometa==' '){if(*fometa=='-')왼쪽=1;if(*fometa=='0')영값=1;if(*fometa=='#')대체값=1;fometa++;}
        int 너비=0,정밀도=-1;if(*fometa=='*'){너비=va_arg(가변인수,int);fometa++;}else while(*fometa>='0'&&*fometa<='9')너비=너비*10+*fometa++-'0';
        if(*fometa=='.'){fometa++;정밀도=0;if(*fometa=='*'){정밀도=va_arg(가변인수,int);fometa++;}else while(*fometa>='0'&&*fometa<='9')정밀도=정밀도*10+*fometa++-'0';}
        int 넓은글자=0;while(*fometa=='l'||*fometa=='z'||*fometa=='t'||*fometa=='j'||*fometa=='h'){if(*fometa!='h')넓은글자=1;fometa++;}
        char tlanya_setlhopha=*fometa?*fometa++:0,kemelwa_Polokelo[80];const char*dikwalwa_tshedimosetso=kemelwa_Polokelo;size_t 개수=0;
        if(tlanya_setlhopha=='s'){dikwalwa_tshedimosetso=va_arg(가변인수,const char*);if(!dikwalwa_tshedimosetso)dikwalwa_tshedimosetso="(null)";개수=strlen(dikwalwa_tshedimosetso);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(tlanya_setlhopha=='c'){kemelwa_Polokelo[0]=va_arg(가변인수,int);개수=1;}
        else if(tlanya_setlhopha=='%'){kemelwa_Polokelo[0]='%';개수=1;}
        else if(tlanya_setlhopha=='d'||tlanya_setlhopha=='i'||tlanya_setlhopha=='u'||tlanya_setlhopha=='x'||tlanya_setlhopha=='X'||tlanya_setlhopha=='o'||tlanya_setlhopha=='p'){
            unsigned long long Boleng;int 음수표시=0;
            if(tlanya_setlhopha=='d'||tlanya_setlhopha=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;Boleng=음수표시?0-(unsigned long long)임시값:임시값;}
            else Boleng=tlanya_setlhopha=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Lemorago_Boleng=tlanya_setlhopha=='x'||tlanya_setlhopha=='X'||tlanya_setlhopha=='p'?16:tlanya_setlhopha=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[Boleng%Lemorago_Boleng];Boleng/=Lemorago_Boleng;}while(Boleng);
            if(음수표시)kemelwa_Polokelo[개수++]='-';if(tlanya_setlhopha=='p'||(대체값&&Lemorago_Boleng==16)){kemelwa_Polokelo[개수++]='0';kemelwa_Polokelo[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(kemelwa_Polokelo)-사용량;채움++)kemelwa_Polokelo[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(kemelwa_Polokelo)-사용량)kemelwa_Polokelo[개수++]='0';
            while(사용량)kemelwa_Polokelo[개수++]=숫자수[--사용량];
        }else{kemelwa_Polokelo[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,dikwalwa_tshedimosetso[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*faele_tsenyo,...){va_list 첫째값;va_start(첫째값,faele_tsenyo);int 반환값=vsnprintf(결과자료,용량한도,faele_tsenyo,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*faele_tsenyo,...){va_list 첫째값;va_start(첫째값,faele_tsenyo);int 반환값=vsnprintf(결과자료,SIZE_MAX,faele_tsenyo,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*moela_Boleng,const char*faele_tsenyo,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),faele_tsenyo,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,moela_Boleng)==(size_t)개수?개수:-1;}
int fprintf(FILE*moela_Boleng,const char*faele_tsenyo,...){va_list 첫째값;va_start(첫째값,faele_tsenyo);int 반환값=vfprintf(moela_Boleng,faele_tsenyo,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*faele_tsenyo,...){va_list 첫째값;va_start(첫째값,faele_tsenyo);int 반환값=vfprintf(stdout,faele_tsenyo,첫째값);va_end(첫째값);return 반환값;}
