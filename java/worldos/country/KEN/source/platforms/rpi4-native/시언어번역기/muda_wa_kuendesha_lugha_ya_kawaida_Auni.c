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
static int kosa;
int *__errno_location(void){return &kosa;}
void exit(int hali_thamani){사용자호출(6,hali_thamani,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *hundi_usemi,const char *faili,unsigned laini,const char *mbinu_ingizo_jina){fprintf(stderr,"cc assertion: %s %s:%u %s\n",hundi_usemi,faili,laini,mbinu_ingizo_jina);exit(1);}
size_t strlen(const char*tungo_data){const char*자료위치=tungo_data;while(*자료위치)자료위치++;return 자료위치-tungo_data;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char jira_x=*첫째값++,Kitufe_cha_Y_kiratibu=*둘째값++;if(jira_x!=Kitufe_cha_Y_kiratibu)return jira_x-Kitufe_cha_Y_kiratibu;if(!jira_x)return 0;}return 0;}
char *strcpy(char*fikio_data,const char*tungo_data){char*반환값=fikio_data;while((*fikio_data++=*tungo_data++)){}return 반환값;}
char *strchr(const char*tungo_data,int msimbo_wa_kibambo){do{if(*tungo_data==(char)msimbo_wa_kibambo)return (char*)tungo_data;}while(*tungo_data++);return 0;}
char *strrchr(const char*tungo_data,int msimbo_wa_kibambo){const char*반환값=0;do{if(*tungo_data==(char)msimbo_wa_kibambo)반환값=tungo_data;}while(*tungo_data++);return (char*)반환값;}
char *strstr(const char*tungo_data,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*tungo_data;tungo_data++)if(!strncmp(tungo_data,터미널항목,개수))return (char*)tungo_data;return 개수?0:(char*)tungo_data;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*jira_x=첫째값,*Kitufe_cha_Y_kiratibu=둘째값;while(개수--){if(*jira_x!=*Kitufe_cha_Y_kiratibu)return *jira_x-*Kitufe_cha_Y_kiratibu;jira_x++;Kitufe_cha_Y_kiratibu++;}return 0;}
void *memmove(void*fikio_data,const void*tungo_data,size_t 개수){unsigned char*jira_x=fikio_data;const unsigned char*Kitufe_cha_Y_kiratibu=tungo_data;if(jira_x<Kitufe_cha_Y_kiratibu){for(size_t 순번=0;순번<개수;순번++)jira_x[순번]=Kitufe_cha_Y_kiratibu[순번];}else while(개수){개수--;jira_x[개수]=Kitufe_cha_Y_kiratibu[개수];}return fikio_data;}
static unsigned char ugawaji_Uwanja_wa_mchezo[6*1024*1024] __attribute__((aligned(16)));
typedef struct data_zuia {size_t panga_ukubwa;struct data_zuia*다음;int 남은공간;int 채울크기;uint64_t mpangilio_funzo;} data_zuia;
static data_zuia *첫항목;
void free(void*자료위치){if(!자료위치)return;data_zuia*둘째값=(data_zuia*)자료위치-1;둘째값->남은공간=1;for(data_zuia*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->panga_ukubwa+=sizeof(data_zuia)+다음위치->다음->panga_ukubwa;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(ugawaji_Uwanja_wa_mchezo)-sizeof(data_zuia))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(data_zuia*)ugawaji_Uwanja_wa_mchezo;첫항목->panga_ukubwa=sizeof(ugawaji_Uwanja_wa_mchezo)-sizeof(data_zuia);첫항목->남은공간=1;첫항목->다음=0;}
    data_zuia*이전=자료위치?(data_zuia*)자료위치-1:0;if(이전&&이전->panga_ukubwa>=개수)return 자료위치;
    for(data_zuia*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->panga_ukubwa>=개수){
        if(둘째값->panga_ukubwa>=개수+sizeof(data_zuia)+16){data_zuia*나머지부분=(data_zuia*)((unsigned char*)(둘째값+1)+개수);나머지부분->panga_ukubwa=둘째값->panga_ukubwa-개수-sizeof(data_zuia);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->panga_ukubwa=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->panga_ukubwa);free(자료위치);}return 반환값;
    }kosa=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t tungo_data){if(tungo_data&&개수>SIZE_MAX/tungo_data)return 0;void*자료위치=malloc(개수*tungo_data);if(자료위치)memset(자료위치,0,개수*tungo_data);return 자료위치;}
unsigned long long strtoull(const char*tungo_data,char**tamatia_Chipua,int nyuma_thamani){
    const char*Anza_Chipua=tungo_data;while(*tungo_data==' '||(*tungo_data>=9&&*tungo_data<=13))tungo_data++;int 음수여부=0;if(*tungo_data=='-'||*tungo_data=='+')음수여부=*tungo_data++=='-';
    if((!nyuma_thamani||nyuma_thamani==16)&&tungo_data[0]=='0'&&(tungo_data[1]=='x'||tungo_data[1]=='X')){nyuma_thamani=16;tungo_data+=2;}if(!nyuma_thamani)nyuma_thamani=*tungo_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned msimbo_wa_kibambo=*tungo_data,fikio_data=msimbo_wa_kibambo>='0'&&msimbo_wa_kibambo<='9'?msimbo_wa_kibambo-'0':msimbo_wa_kibambo>='a'&&msimbo_wa_kibambo<='z'?msimbo_wa_kibambo-'a'+10:msimbo_wa_kibambo>='A'&&msimbo_wa_kibambo<='Z'?msimbo_wa_kibambo-'A'+10:99;if(fikio_data>=(unsigned)nyuma_thamani)break;하나라도=1;tungo_data++;if(임시값>(~0ull-fikio_data)/(unsigned)nyuma_thamani){임시값=~0ull;kosa=34;}else 임시값=임시값*nyuma_thamani+fikio_data;}
    if(tamatia_Chipua)*tamatia_Chipua=(char*)(하나라도?tungo_data:Anza_Chipua);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*tungo_data,char**보조항목,int 둘째값){return strtoull(tungo_data,보조항목,둘째값);}
long strtol(const char*tungo_data,char**보조항목,int 둘째값){return (long)strtoull(tungo_data,보조항목,둘째값);}
int atoi(const char*tungo_data){return (int)strtol(tungo_data,0,10);}
long double ldexpl(long double jira_x,int 개수){while(개수>0){jira_x*=2;개수--;}while(개수<0){jira_x/=2;개수++;}return jira_x;}
long double strtold(const char*tungo_data,char**tamatia_Chipua){
    const char*Anza_Chipua=tungo_data;while(*tungo_data==' '||(*tungo_data>=9&&*tungo_data<=13))tungo_data++;int 음수여부=0;if(*tungo_data=='-'||*tungo_data=='+')음수여부=*tungo_data++=='-';
    int nyuma_thamani=10;if(tungo_data[0]=='0'&&(tungo_data[1]=='x'||tungo_data[1]=='X')){nyuma_thamani=16;tungo_data+=2;}long double 임시값=0,rekebisha=1;int 소수부=0,하나라도=0;
    for(;;){int msimbo_wa_kibambo=*tungo_data,fikio_data=msimbo_wa_kibambo>='0'&&msimbo_wa_kibambo<='9'?msimbo_wa_kibambo-'0':msimbo_wa_kibambo>='a'&&msimbo_wa_kibambo<='f'?msimbo_wa_kibambo-'a'+10:msimbo_wa_kibambo>='A'&&msimbo_wa_kibambo<='F'?msimbo_wa_kibambo-'A'+10:99;
        if(msimbo_wa_kibambo=='.'&&!소수부){소수부=1;tungo_data++;continue;}if(fikio_data>=nyuma_thamani)break;하나라도=1;tungo_data++;임시값=임시값*nyuma_thamani+fikio_data;if(소수부)rekebisha*=nyuma_thamani;
    }임시값/=rekebisha;
    if((nyuma_thamani==10&&(*tungo_data=='e'||*tungo_data=='E'))||(nyuma_thamani==16&&(*tungo_data=='p'||*tungo_data=='P'))){const char*onyesha_thamani=tungo_data++;int 빼기=0;if(*tungo_data=='-'||*tungo_data=='+')빼기=*tungo_data++=='-';int 개수=0,항목수=0;while(*tungo_data>='0'&&*tungo_data<='9'){항목수++;if(개수<20000)개수=개수*10+*tungo_data-'0';tungo_data++;}if(!항목수)tungo_data=onyesha_thamani;else{long double namba_kamilifu=nyuma_thamani==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/namba_kamilifu:임시값*namba_kamilifu;}}
    if(tamatia_Chipua)*tamatia_Chipua=(char*)(하나라도?tungo_data:Anza_Chipua);return 음수여부?-임시값:임시값;
}
double strtod(const char*tungo_data,char**보조항목){return (double)strtold(tungo_data,보조항목);}float strtof(const char*tungo_data,char**보조항목){return (float)strtold(tungo_data,보조항목);}
void qsort(void*nyuma_thamani,size_t 개수,size_t panga_ukubwa,int(*Linganisha)(const void*,const void*)){
    unsigned char*자료위치=nyuma_thamani;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Linganisha(자료위치+(안쪽순번-1)*panga_ukubwa,자료위치+안쪽순번*panga_ukubwa)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<panga_ukubwa;셋째순번++){unsigned char msimbo_wa_kibambo=자료위치[(안쪽순번-1)*panga_ukubwa+셋째순번];자료위치[(안쪽순번-1)*panga_ukubwa+셋째순번]=자료위치[안쪽순번*panga_ukubwa+셋째순번];자료위치[안쪽순번*panga_ukubwa+셋째순번]=msimbo_wa_kibambo;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*Jina,int usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma,...){
    if(!strcmp(Jina,"/@cc-output")){if(출력열림){kosa=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Jina,번역기자원들[순번].Jina)){
        if(usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&3){kosa=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}kosa=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Jina,usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma,0,0,0,0);if(반환값<0){kosa=-반환값;return -1;}return 반환값;
}
int close(int faili_kishiko){if(faili_kishiko==100){출력열림=0;return 0;}if(faili_kishiko>=128&&faili_kishiko<152){열림[faili_kishiko-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,faili_kishiko,0,0,0,0,0);if(반환값<0){kosa=-반환값;return -1;}return 0;}
long read(int faili_kishiko,void*data,size_t 개수){
    if(faili_kishiko>=128&&faili_kishiko<152&&열림[faili_kishiko-128].사용량){int 순번=faili_kishiko-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->panga_ukubwa-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(data,반환값->data+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,faili_kishiko,(uintptr_t)data,개수,0,0,0);if(반환값<0){kosa=-반환값;return -1;}return 반환값;
}
long write(int faili_kishiko,const void*data,size_t 개수){
    if(faili_kishiko==100){if(개수>sizeof(출력결과)-출력위치){kosa=28;return -1;}memcpy(출력결과+출력위치,data,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,faili_kishiko,(uintptr_t)data,개수,0,0,0);if(반환값<0){kosa=-반환값;return -1;}return 반환값;
}
long lseek(int faili_kishiko,long Chipua_thamani,int 기준점){
    if(faili_kishiko==100){long 자료위치=Chipua_thamani+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){kosa=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(faili_kishiko>=128&&faili_kishiko<152&&열림[faili_kishiko-128].사용량){int 순번=faili_kishiko-128;long 자료위치=Chipua_thamani+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].panga_ukubwa);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].panga_ukubwa){kosa=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,faili_kishiko,Chipua_thamani,기준점,0,0,0);if(반환값<0){kosa=-반환값;return -1;}return 반환값;
}
int unlink(const char*Jina){intptr_t 반환값=사용자호출(11,(uintptr_t)Jina,0,0,0,0,0);if(반환값<0){kosa=-반환값;return -1;}return 반환값;}
char *realpath(const char*Jina,char*결과자료){if(!결과자료){결과자료=malloc(strlen(Jina)+1);if(!결과자료)return 0;}return strcpy(결과자료,Jina);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){kosa=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int faili_kishiko,const char*mbinu_hali_tumizi){(void)mbinu_hali_tumizi;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].kosa=0;흐름목록[순번].faili_kishiko=faili_kishiko;return &흐름목록[순번];}kosa=24;return 0;}
int fflush(FILE*faili_ingizo){return faili_ingizo&&faili_ingizo->kosa?-1:0;}
int fclose(FILE*faili_ingizo){int 반환값=close(faili_ingizo->faili_kishiko);if(faili_ingizo->kosa)반환값=-1;faili_ingizo->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t tungo_data,size_t 개수,FILE*faili_ingizo){if(!tungo_data)return 0;if(개수>SIZE_MAX/tungo_data){faili_ingizo->kosa=1;return 0;}long 반환값=write(faili_ingizo->faili_kishiko,자료위치,tungo_data*개수);if(반환값<0){faili_ingizo->kosa=1;return 0;}return (size_t)반환값/tungo_data;}
int fputc(int msimbo_wa_kibambo,FILE*faili_ingizo){unsigned char 둘째값=msimbo_wa_kibambo;return fwrite(&둘째값,1,1,faili_ingizo)==1?둘째값:EOF;}
int fputs(const char*tungo_data,FILE*faili_ingizo){return fwrite(tungo_data,1,strlen(tungo_data),faili_ingizo)==strlen(tungo_data)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char msimbo_wa_kibambo){if(*현재위치+1<용량한도)결과자료[*현재위치]=msimbo_wa_kibambo;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*umbiza,va_list 가변인수){
    size_t 현재위치=0;while(*umbiza){if(*umbiza!='%'){넣기(결과자료,용량한도,&현재위치,*umbiza++);continue;}umbiza++;
        int 왼쪽=0,영값=0,대체값=0;while(*umbiza=='-'||*umbiza=='0'||*umbiza=='#'||*umbiza=='+'||*umbiza==' '){if(*umbiza=='-')왼쪽=1;if(*umbiza=='0')영값=1;if(*umbiza=='#')대체값=1;umbiza++;}
        int 너비=0,정밀도=-1;if(*umbiza=='*'){너비=va_arg(가변인수,int);umbiza++;}else while(*umbiza>='0'&&*umbiza<='9')너비=너비*10+*umbiza++-'0';
        if(*umbiza=='.'){umbiza++;정밀도=0;if(*umbiza=='*'){정밀도=va_arg(가변인수,int);umbiza++;}else while(*umbiza>='0'&&*umbiza<='9')정밀도=정밀도*10+*umbiza++-'0';}
        int 넓은글자=0;while(*umbiza=='l'||*umbiza=='z'||*umbiza=='t'||*umbiza=='j'||*umbiza=='h'){if(*umbiza!='h')넓은글자=1;umbiza++;}
        char aina_kategoria=*umbiza?*umbiza++:0,bafa_Hifadhi[80];const char*tungo_data=bafa_Hifadhi;size_t 개수=0;
        if(aina_kategoria=='s'){tungo_data=va_arg(가변인수,const char*);if(!tungo_data)tungo_data="(null)";개수=strlen(tungo_data);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(aina_kategoria=='c'){bafa_Hifadhi[0]=va_arg(가변인수,int);개수=1;}
        else if(aina_kategoria=='%'){bafa_Hifadhi[0]='%';개수=1;}
        else if(aina_kategoria=='d'||aina_kategoria=='i'||aina_kategoria=='u'||aina_kategoria=='x'||aina_kategoria=='X'||aina_kategoria=='o'||aina_kategoria=='p'){
            unsigned long long thamani;int 음수표시=0;
            if(aina_kategoria=='d'||aina_kategoria=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;thamani=음수표시?0-(unsigned long long)임시값:임시값;}
            else thamani=aina_kategoria=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned nyuma_thamani=aina_kategoria=='x'||aina_kategoria=='X'||aina_kategoria=='p'?16:aina_kategoria=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[thamani%nyuma_thamani];thamani/=nyuma_thamani;}while(thamani);
            if(음수표시)bafa_Hifadhi[개수++]='-';if(aina_kategoria=='p'||(대체값&&nyuma_thamani==16)){bafa_Hifadhi[개수++]='0';bafa_Hifadhi[개수++]='x';}
            for(int jaza_thamani=(int)사용량;정밀도>jaza_thamani&&개수<sizeof(bafa_Hifadhi)-사용량;jaza_thamani++)bafa_Hifadhi[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(bafa_Hifadhi)-사용량)bafa_Hifadhi[개수++]='0';
            while(사용량)bafa_Hifadhi[개수++]=숫자수[--사용량];
        }else{bafa_Hifadhi[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,tungo_data[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*faili_ingizo,...){va_list 첫째값;va_start(첫째값,faili_ingizo);int 반환값=vsnprintf(결과자료,용량한도,faili_ingizo,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*faili_ingizo,...){va_list 첫째값;va_start(첫째값,faili_ingizo);int 반환값=vsnprintf(결과자료,SIZE_MAX,faili_ingizo,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_thamani,const char*faili_ingizo,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),faili_ingizo,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,Stream_thamani)==(size_t)개수?개수:-1;}
int fprintf(FILE*Stream_thamani,const char*faili_ingizo,...){va_list 첫째값;va_start(첫째값,faili_ingizo);int 반환값=vfprintf(Stream_thamani,faili_ingizo,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*faili_ingizo,...){va_list 첫째값;va_start(첫째값,faili_ingizo);int 반환값=vfprintf(stdout,faili_ingizo,첫째값);va_end(첫째값);return 반환값;}
