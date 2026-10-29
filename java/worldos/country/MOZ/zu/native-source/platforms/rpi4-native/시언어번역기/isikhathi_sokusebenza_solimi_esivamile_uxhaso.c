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
static int Iphutha;
int *__errno_location(void){return &Iphutha;}
void exit(int isimo_inani){사용자호출(6,isimo_inani,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *hlola_ukusho,const char *Ihele,unsigned umugqa,const char *indlela_okufakwayo_igama){fprintf(stderr,"cc assertion: %s %s:%u %s\n",hlola_ukusho,Ihele,umugqa,indlela_okufakwayo_igama);exit(1);}
size_t strlen(const char*uchunge_imininingwane){const char*자료위치=uchunge_imininingwane;while(*자료위치)자료위치++;return 자료위치-uchunge_imininingwane;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char okuxhumanisa_u_x=*첫째값++,세로좌표=*둘째값++;if(okuxhumanisa_u_x!=세로좌표)return okuxhumanisa_u_x-세로좌표;if(!okuxhumanisa_u_x)return 0;}return 0;}
char *strcpy(char*isikhumulo_imininingwane,const char*uchunge_imininingwane){char*반환값=isikhumulo_imininingwane;while((*isikhumulo_imininingwane++=*uchunge_imininingwane++)){}return 반환값;}
char *strchr(const char*uchunge_imininingwane,int ikhodi_yohlamvu){do{if(*uchunge_imininingwane==(char)ikhodi_yohlamvu)return (char*)uchunge_imininingwane;}while(*uchunge_imininingwane++);return 0;}
char *strrchr(const char*uchunge_imininingwane,int ikhodi_yohlamvu){const char*반환값=0;do{if(*uchunge_imininingwane==(char)ikhodi_yohlamvu)반환값=uchunge_imininingwane;}while(*uchunge_imininingwane++);return (char*)반환값;}
char *strstr(const char*uchunge_imininingwane,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*uchunge_imininingwane;uchunge_imininingwane++)if(!strncmp(uchunge_imininingwane,터미널항목,개수))return (char*)uchunge_imininingwane;return 개수?0:(char*)uchunge_imininingwane;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*okuxhumanisa_u_x=첫째값,*세로좌표=둘째값;while(개수--){if(*okuxhumanisa_u_x!=*세로좌표)return *okuxhumanisa_u_x-*세로좌표;okuxhumanisa_u_x++;세로좌표++;}return 0;}
void *memmove(void*isikhumulo_imininingwane,const void*uchunge_imininingwane,size_t 개수){unsigned char*okuxhumanisa_u_x=isikhumulo_imininingwane;const unsigned char*세로좌표=uchunge_imininingwane;if(okuxhumanisa_u_x<세로좌표){for(size_t 순번=0;순번<개수;순번++)okuxhumanisa_u_x[순번]=세로좌표[순번];}else while(개수){개수--;okuxhumanisa_u_x[개수]=세로좌표[개수];}return isikhumulo_imininingwane;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct imininingwane_vimbela {size_t Ubungako;struct imininingwane_vimbela*다음;int 남은공간;int 채울크기;uint64_t ukuqondanisa_isifundo;} imininingwane_vimbela;
static imininingwane_vimbela *첫항목;
void free(void*자료위치){if(!자료위치)return;imininingwane_vimbela*둘째값=(imininingwane_vimbela*)자료위치-1;둘째값->남은공간=1;for(imininingwane_vimbela*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->Ubungako+=sizeof(imininingwane_vimbela)+다음위치->다음->Ubungako;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(imininingwane_vimbela))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(imininingwane_vimbela*)할당마당;첫항목->Ubungako=sizeof(할당마당)-sizeof(imininingwane_vimbela);첫항목->남은공간=1;첫항목->다음=0;}
    imininingwane_vimbela*이전=자료위치?(imininingwane_vimbela*)자료위치-1:0;if(이전&&이전->Ubungako>=개수)return 자료위치;
    for(imininingwane_vimbela*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->Ubungako>=개수){
        if(둘째값->Ubungako>=개수+sizeof(imininingwane_vimbela)+16){imininingwane_vimbela*나머지부분=(imininingwane_vimbela*)((unsigned char*)(둘째값+1)+개수);나머지부분->Ubungako=둘째값->Ubungako-개수-sizeof(imininingwane_vimbela);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->Ubungako=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->Ubungako);free(자료위치);}return 반환값;
    }Iphutha=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t uchunge_imininingwane){if(uchunge_imininingwane&&개수>SIZE_MAX/uchunge_imininingwane)return 0;void*자료위치=malloc(개수*uchunge_imininingwane);if(자료위치)memset(자료위치,0,개수*uchunge_imininingwane);return 자료위치;}
unsigned long long strtoull(const char*uchunge_imininingwane,char**yekisa_I_ofisethi,int ngemuva_inani){
    const char*qala_I_ofisethi=uchunge_imininingwane;while(*uchunge_imininingwane==' '||(*uchunge_imininingwane>=9&&*uchunge_imininingwane<=13))uchunge_imininingwane++;int 음수여부=0;if(*uchunge_imininingwane=='-'||*uchunge_imininingwane=='+')음수여부=*uchunge_imininingwane++=='-';
    if((!ngemuva_inani||ngemuva_inani==16)&&uchunge_imininingwane[0]=='0'&&(uchunge_imininingwane[1]=='x'||uchunge_imininingwane[1]=='X')){ngemuva_inani=16;uchunge_imininingwane+=2;}if(!ngemuva_inani)ngemuva_inani=*uchunge_imininingwane=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned ikhodi_yohlamvu=*uchunge_imininingwane,isikhumulo_imininingwane=ikhodi_yohlamvu>='0'&&ikhodi_yohlamvu<='9'?ikhodi_yohlamvu-'0':ikhodi_yohlamvu>='a'&&ikhodi_yohlamvu<='z'?ikhodi_yohlamvu-'a'+10:ikhodi_yohlamvu>='A'&&ikhodi_yohlamvu<='Z'?ikhodi_yohlamvu-'A'+10:99;if(isikhumulo_imininingwane>=(unsigned)ngemuva_inani)break;하나라도=1;uchunge_imininingwane++;if(임시값>(~0ull-isikhumulo_imininingwane)/(unsigned)ngemuva_inani){임시값=~0ull;Iphutha=34;}else 임시값=임시값*ngemuva_inani+isikhumulo_imininingwane;}
    if(yekisa_I_ofisethi)*yekisa_I_ofisethi=(char*)(하나라도?uchunge_imininingwane:qala_I_ofisethi);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*uchunge_imininingwane,char**보조항목,int 둘째값){return strtoull(uchunge_imininingwane,보조항목,둘째값);}
long strtol(const char*uchunge_imininingwane,char**보조항목,int 둘째값){return (long)strtoull(uchunge_imininingwane,보조항목,둘째값);}
int atoi(const char*uchunge_imininingwane){return (int)strtol(uchunge_imininingwane,0,10);}
long double ldexpl(long double okuxhumanisa_u_x,int 개수){while(개수>0){okuxhumanisa_u_x*=2;개수--;}while(개수<0){okuxhumanisa_u_x/=2;개수++;}return okuxhumanisa_u_x;}
long double strtold(const char*uchunge_imininingwane,char**yekisa_I_ofisethi){
    const char*qala_I_ofisethi=uchunge_imininingwane;while(*uchunge_imininingwane==' '||(*uchunge_imininingwane>=9&&*uchunge_imininingwane<=13))uchunge_imininingwane++;int 음수여부=0;if(*uchunge_imininingwane=='-'||*uchunge_imininingwane=='+')음수여부=*uchunge_imininingwane++=='-';
    int ngemuva_inani=10;if(uchunge_imininingwane[0]=='0'&&(uchunge_imininingwane[1]=='x'||uchunge_imininingwane[1]=='X')){ngemuva_inani=16;uchunge_imininingwane+=2;}long double 임시값=0,linganisa=1;int 소수부=0,하나라도=0;
    for(;;){int ikhodi_yohlamvu=*uchunge_imininingwane,isikhumulo_imininingwane=ikhodi_yohlamvu>='0'&&ikhodi_yohlamvu<='9'?ikhodi_yohlamvu-'0':ikhodi_yohlamvu>='a'&&ikhodi_yohlamvu<='f'?ikhodi_yohlamvu-'a'+10:ikhodi_yohlamvu>='A'&&ikhodi_yohlamvu<='F'?ikhodi_yohlamvu-'A'+10:99;
        if(ikhodi_yohlamvu=='.'&&!소수부){소수부=1;uchunge_imininingwane++;continue;}if(isikhumulo_imininingwane>=ngemuva_inani)break;하나라도=1;uchunge_imininingwane++;임시값=임시값*ngemuva_inani+isikhumulo_imininingwane;if(소수부)linganisa*=ngemuva_inani;
    }임시값/=linganisa;
    if((ngemuva_inani==10&&(*uchunge_imininingwane=='e'||*uchunge_imininingwane=='E'))||(ngemuva_inani==16&&(*uchunge_imininingwane=='p'||*uchunge_imininingwane=='P'))){const char*khombisa_inani=uchunge_imininingwane++;int 빼기=0;if(*uchunge_imininingwane=='-'||*uchunge_imininingwane=='+')빼기=*uchunge_imininingwane++=='-';int 개수=0,항목수=0;while(*uchunge_imininingwane>='0'&&*uchunge_imininingwane<='9'){항목수++;if(개수<20000)개수=개수*10+*uchunge_imininingwane-'0';uchunge_imininingwane++;}if(!항목수)uchunge_imininingwane=khombisa_inani;else{long double ifektha=ngemuva_inani==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/ifektha:임시값*ifektha;}}
    if(yekisa_I_ofisethi)*yekisa_I_ofisethi=(char*)(하나라도?uchunge_imininingwane:qala_I_ofisethi);return 음수여부?-임시값:임시값;
}
double strtod(const char*uchunge_imininingwane,char**보조항목){return (double)strtold(uchunge_imininingwane,보조항목);}float strtof(const char*uchunge_imininingwane,char**보조항목){return (float)strtold(uchunge_imininingwane,보조항목);}
void qsort(void*ngemuva_inani,size_t 개수,size_t Ubungako,int(*Qhathanisa)(const void*,const void*)){
    unsigned char*자료위치=ngemuva_inani;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Qhathanisa(자료위치+(안쪽순번-1)*Ubungako,자료위치+안쪽순번*Ubungako)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Ubungako;셋째순번++){unsigned char ikhodi_yohlamvu=자료위치[(안쪽순번-1)*Ubungako+셋째순번];자료위치[(안쪽순번-1)*Ubungako+셋째순번]=자료위치[안쪽순번*Ubungako+셋째순번];자료위치[안쪽순번*Ubungako+셋째순번]=ikhodi_yohlamvu;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*Igama,int 설정비트,...){
    if(!strcmp(Igama,"/@cc-output")){if(출력열림){Iphutha=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Igama,번역기자원들[순번].Igama)){
        if(설정비트&3){Iphutha=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}Iphutha=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Igama,설정비트,0,0,0,0);if(반환값<0){Iphutha=-반환값;return -1;}return 반환값;
}
int close(int ifayela_isibambo){if(ifayela_isibambo==100){출력열림=0;return 0;}if(ifayela_isibambo>=128&&ifayela_isibambo<152){열림[ifayela_isibambo-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,ifayela_isibambo,0,0,0,0,0);if(반환값<0){Iphutha=-반환값;return -1;}return 0;}
long read(int ifayela_isibambo,void*imininingwane,size_t 개수){
    if(ifayela_isibambo>=128&&ifayela_isibambo<152&&열림[ifayela_isibambo-128].사용량){int 순번=ifayela_isibambo-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->Ubungako-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(imininingwane,반환값->imininingwane+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,ifayela_isibambo,(uintptr_t)imininingwane,개수,0,0,0);if(반환값<0){Iphutha=-반환값;return -1;}return 반환값;
}
long write(int ifayela_isibambo,const void*imininingwane,size_t 개수){
    if(ifayela_isibambo==100){if(개수>sizeof(출력결과)-출력위치){Iphutha=28;return -1;}memcpy(출력결과+출력위치,imininingwane,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,ifayela_isibambo,(uintptr_t)imininingwane,개수,0,0,0);if(반환값<0){Iphutha=-반환값;return -1;}return 반환값;
}
long lseek(int ifayela_isibambo,long I_ofisethi_inani,int 기준점){
    if(ifayela_isibambo==100){long 자료위치=I_ofisethi_inani+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){Iphutha=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(ifayela_isibambo>=128&&ifayela_isibambo<152&&열림[ifayela_isibambo-128].사용량){int 순번=ifayela_isibambo-128;long 자료위치=I_ofisethi_inani+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].Ubungako);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].Ubungako){Iphutha=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,ifayela_isibambo,I_ofisethi_inani,기준점,0,0,0);if(반환값<0){Iphutha=-반환값;return -1;}return 반환값;
}
int unlink(const char*Igama){intptr_t 반환값=사용자호출(11,(uintptr_t)Igama,0,0,0,0,0);if(반환값<0){Iphutha=-반환값;return -1;}return 반환값;}
char *realpath(const char*Igama,char*결과자료){if(!결과자료){결과자료=malloc(strlen(Igama)+1);if(!결과자료)return 0;}return strcpy(결과자료,Igama);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){Iphutha=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int ifayela_isibambo,const char*indlela_inqubo){(void)indlela_inqubo;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Iphutha=0;흐름목록[순번].ifayela_isibambo=ifayela_isibambo;return &흐름목록[순번];}Iphutha=24;return 0;}
int fflush(FILE*ifayela_okufakwayo){return ifayela_okufakwayo&&ifayela_okufakwayo->Iphutha?-1:0;}
int fclose(FILE*ifayela_okufakwayo){int 반환값=close(ifayela_okufakwayo->ifayela_isibambo);if(ifayela_okufakwayo->Iphutha)반환값=-1;ifayela_okufakwayo->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t uchunge_imininingwane,size_t 개수,FILE*ifayela_okufakwayo){if(!uchunge_imininingwane)return 0;if(개수>SIZE_MAX/uchunge_imininingwane){ifayela_okufakwayo->Iphutha=1;return 0;}long 반환값=write(ifayela_okufakwayo->ifayela_isibambo,자료위치,uchunge_imininingwane*개수);if(반환값<0){ifayela_okufakwayo->Iphutha=1;return 0;}return (size_t)반환값/uchunge_imininingwane;}
int fputc(int ikhodi_yohlamvu,FILE*ifayela_okufakwayo){unsigned char 둘째값=ikhodi_yohlamvu;return fwrite(&둘째값,1,1,ifayela_okufakwayo)==1?둘째값:EOF;}
int fputs(const char*uchunge_imininingwane,FILE*ifayela_okufakwayo){return fwrite(uchunge_imininingwane,1,strlen(uchunge_imininingwane),ifayela_okufakwayo)==strlen(uchunge_imininingwane)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char ikhodi_yohlamvu){if(*현재위치+1<용량한도)결과자료[*현재위치]=ikhodi_yohlamvu;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*misa,va_list 가변인수){
    size_t 현재위치=0;while(*misa){if(*misa!='%'){넣기(결과자료,용량한도,&현재위치,*misa++);continue;}misa++;
        int 왼쪽=0,영값=0,대체값=0;while(*misa=='-'||*misa=='0'||*misa=='#'||*misa=='+'||*misa==' '){if(*misa=='-')왼쪽=1;if(*misa=='0')영값=1;if(*misa=='#')대체값=1;misa++;}
        int 너비=0,정밀도=-1;if(*misa=='*'){너비=va_arg(가변인수,int);misa++;}else while(*misa>='0'&&*misa<='9')너비=너비*10+*misa++-'0';
        if(*misa=='.'){misa++;정밀도=0;if(*misa=='*'){정밀도=va_arg(가변인수,int);misa++;}else while(*misa>='0'&&*misa<='9')정밀도=정밀도*10+*misa++-'0';}
        int 넓은글자=0;while(*misa=='l'||*misa=='z'||*misa=='t'||*misa=='j'||*misa=='h'){if(*misa!='h')넓은글자=1;misa++;}
        char thayipha_umunxa=*misa?*misa++:0,isikhumbulo_sesikhana_Indawo_yokugcina[80];const char*uchunge_imininingwane=isikhumbulo_sesikhana_Indawo_yokugcina;size_t 개수=0;
        if(thayipha_umunxa=='s'){uchunge_imininingwane=va_arg(가변인수,const char*);if(!uchunge_imininingwane)uchunge_imininingwane="(null)";개수=strlen(uchunge_imininingwane);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(thayipha_umunxa=='c'){isikhumbulo_sesikhana_Indawo_yokugcina[0]=va_arg(가변인수,int);개수=1;}
        else if(thayipha_umunxa=='%'){isikhumbulo_sesikhana_Indawo_yokugcina[0]='%';개수=1;}
        else if(thayipha_umunxa=='d'||thayipha_umunxa=='i'||thayipha_umunxa=='u'||thayipha_umunxa=='x'||thayipha_umunxa=='X'||thayipha_umunxa=='o'||thayipha_umunxa=='p'){
            unsigned long long inani;int 음수표시=0;
            if(thayipha_umunxa=='d'||thayipha_umunxa=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;inani=음수표시?0-(unsigned long long)임시값:임시값;}
            else inani=thayipha_umunxa=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned ngemuva_inani=thayipha_umunxa=='x'||thayipha_umunxa=='X'||thayipha_umunxa=='p'?16:thayipha_umunxa=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[inani%ngemuva_inani];inani/=ngemuva_inani;}while(inani);
            if(음수표시)isikhumbulo_sesikhana_Indawo_yokugcina[개수++]='-';if(thayipha_umunxa=='p'||(대체값&&ngemuva_inani==16)){isikhumbulo_sesikhana_Indawo_yokugcina[개수++]='0';isikhumbulo_sesikhana_Indawo_yokugcina[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(isikhumbulo_sesikhana_Indawo_yokugcina)-사용량;채움++)isikhumbulo_sesikhana_Indawo_yokugcina[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(isikhumbulo_sesikhana_Indawo_yokugcina)-사용량)isikhumbulo_sesikhana_Indawo_yokugcina[개수++]='0';
            while(사용량)isikhumbulo_sesikhana_Indawo_yokugcina[개수++]=숫자수[--사용량];
        }else{isikhumbulo_sesikhana_Indawo_yokugcina[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,uchunge_imininingwane[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*ifayela_okufakwayo,...){va_list 첫째값;va_start(첫째값,ifayela_okufakwayo);int 반환값=vsnprintf(결과자료,용량한도,ifayela_okufakwayo,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*ifayela_okufakwayo,...){va_list 첫째값;va_start(첫째값,ifayela_okufakwayo);int 반환값=vsnprintf(결과자료,SIZE_MAX,ifayela_okufakwayo,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_inani,const char*ifayela_okufakwayo,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),ifayela_okufakwayo,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,Stream_inani)==(size_t)개수?개수:-1;}
int fprintf(FILE*Stream_inani,const char*ifayela_okufakwayo,...){va_list 첫째값;va_start(첫째값,ifayela_okufakwayo);int 반환값=vfprintf(Stream_inani,ifayela_okufakwayo,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*ifayela_okufakwayo,...){va_list 첫째값;va_start(첫째값,ifayela_okufakwayo);int 반환값=vfprintf(stdout,ifayela_okufakwayo,첫째값);va_end(첫째값);return 반환값;}
