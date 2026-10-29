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
static int Phošo;
int *__errno_location(void){return &Phošo;}
void exit(int boemo_boleng){사용자호출(6,boemo_boleng,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *lekola_tlhagišo,const char *Faele,unsigned mothaladi,const char *mokgwa_go_tsenya_tshedimošo_leina){fprintf(stderr,"cc assertion: %s %s:%u %s\n",lekola_tlhagišo,Faele,mothaladi,mokgwa_go_tsenya_tshedimošo_leina);exit(1);}
size_t strlen(const char*molokoloko_data){const char*자료위치=molokoloko_data;while(*자료위치)자료위치++;return 자료위치-molokoloko_data;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char kamano_ya_x=*첫째값++,세로좌표=*둘째값++;if(kamano_ya_x!=세로좌표)return kamano_ya_x-세로좌표;if(!kamano_ya_x)return 0;}return 0;}
char *strcpy(char*boyo_data,const char*molokoloko_data){char*반환값=boyo_data;while((*boyo_data++=*molokoloko_data++)){}return 반환값;}
char *strchr(const char*molokoloko_data,int khouto_ya_tlhaka){do{if(*molokoloko_data==(char)khouto_ya_tlhaka)return (char*)molokoloko_data;}while(*molokoloko_data++);return 0;}
char *strrchr(const char*molokoloko_data,int khouto_ya_tlhaka){const char*반환값=0;do{if(*molokoloko_data==(char)khouto_ya_tlhaka)반환값=molokoloko_data;}while(*molokoloko_data++);return (char*)반환값;}
char *strstr(const char*molokoloko_data,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*molokoloko_data;molokoloko_data++)if(!strncmp(molokoloko_data,터미널항목,개수))return (char*)molokoloko_data;return 개수?0:(char*)molokoloko_data;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*kamano_ya_x=첫째값,*세로좌표=둘째값;while(개수--){if(*kamano_ya_x!=*세로좌표)return *kamano_ya_x-*세로좌표;kamano_ya_x++;세로좌표++;}return 0;}
void *memmove(void*boyo_data,const void*molokoloko_data,size_t 개수){unsigned char*kamano_ya_x=boyo_data;const unsigned char*세로좌표=molokoloko_data;if(kamano_ya_x<세로좌표){for(size_t 순번=0;순번<개수;순번++)kamano_ya_x[순번]=세로좌표[순번];}else while(개수){개수--;kamano_ya_x[개수]=세로좌표[개수];}return boyo_data;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct data_thibela {size_t Bogolo;struct data_thibela*다음;int 남은공간;int 채울크기;uint64_t tebanyo_thutišo;} data_thibela;
static data_thibela *첫항목;
void free(void*자료위치){if(!자료위치)return;data_thibela*둘째값=(data_thibela*)자료위치-1;둘째값->남은공간=1;for(data_thibela*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->Bogolo+=sizeof(data_thibela)+다음위치->다음->Bogolo;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(data_thibela))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(data_thibela*)할당마당;첫항목->Bogolo=sizeof(할당마당)-sizeof(data_thibela);첫항목->남은공간=1;첫항목->다음=0;}
    data_thibela*이전=자료위치?(data_thibela*)자료위치-1:0;if(이전&&이전->Bogolo>=개수)return 자료위치;
    for(data_thibela*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->Bogolo>=개수){
        if(둘째값->Bogolo>=개수+sizeof(data_thibela)+16){data_thibela*나머지부분=(data_thibela*)((unsigned char*)(둘째값+1)+개수);나머지부분->Bogolo=둘째값->Bogolo-개수-sizeof(data_thibela);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->Bogolo=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->Bogolo);free(자료위치);}return 반환값;
    }Phošo=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t molokoloko_data){if(molokoloko_data&&개수>SIZE_MAX/molokoloko_data)return 0;void*자료위치=malloc(개수*molokoloko_data);if(자료위치)memset(자료위치,0,개수*molokoloko_data);return 자료위치;}
unsigned long long strtoull(const char*molokoloko_data,char**fetša_E_Šetšego,int Bokamorago_boleng){
    const char*Thomišo_E_Šetšego=molokoloko_data;while(*molokoloko_data==' '||(*molokoloko_data>=9&&*molokoloko_data<=13))molokoloko_data++;int 음수여부=0;if(*molokoloko_data=='-'||*molokoloko_data=='+')음수여부=*molokoloko_data++=='-';
    if((!Bokamorago_boleng||Bokamorago_boleng==16)&&molokoloko_data[0]=='0'&&(molokoloko_data[1]=='x'||molokoloko_data[1]=='X')){Bokamorago_boleng=16;molokoloko_data+=2;}if(!Bokamorago_boleng)Bokamorago_boleng=*molokoloko_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned khouto_ya_tlhaka=*molokoloko_data,boyo_data=khouto_ya_tlhaka>='0'&&khouto_ya_tlhaka<='9'?khouto_ya_tlhaka-'0':khouto_ya_tlhaka>='a'&&khouto_ya_tlhaka<='z'?khouto_ya_tlhaka-'a'+10:khouto_ya_tlhaka>='A'&&khouto_ya_tlhaka<='Z'?khouto_ya_tlhaka-'A'+10:99;if(boyo_data>=(unsigned)Bokamorago_boleng)break;하나라도=1;molokoloko_data++;if(임시값>(~0ull-boyo_data)/(unsigned)Bokamorago_boleng){임시값=~0ull;Phošo=34;}else 임시값=임시값*Bokamorago_boleng+boyo_data;}
    if(fetša_E_Šetšego)*fetša_E_Šetšego=(char*)(하나라도?molokoloko_data:Thomišo_E_Šetšego);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*molokoloko_data,char**보조항목,int 둘째값){return strtoull(molokoloko_data,보조항목,둘째값);}
long strtol(const char*molokoloko_data,char**보조항목,int 둘째값){return (long)strtoull(molokoloko_data,보조항목,둘째값);}
int atoi(const char*molokoloko_data){return (int)strtol(molokoloko_data,0,10);}
long double ldexpl(long double kamano_ya_x,int 개수){while(개수>0){kamano_ya_x*=2;개수--;}while(개수<0){kamano_ya_x/=2;개수++;}return kamano_ya_x;}
long double strtold(const char*molokoloko_data,char**fetša_E_Šetšego){
    const char*Thomišo_E_Šetšego=molokoloko_data;while(*molokoloko_data==' '||(*molokoloko_data>=9&&*molokoloko_data<=13))molokoloko_data++;int 음수여부=0;if(*molokoloko_data=='-'||*molokoloko_data=='+')음수여부=*molokoloko_data++=='-';
    int Bokamorago_boleng=10;if(molokoloko_data[0]=='0'&&(molokoloko_data[1]=='x'||molokoloko_data[1]=='X')){Bokamorago_boleng=16;molokoloko_data+=2;}long double 임시값=0,lekanetša=1;int 소수부=0,하나라도=0;
    for(;;){int khouto_ya_tlhaka=*molokoloko_data,boyo_data=khouto_ya_tlhaka>='0'&&khouto_ya_tlhaka<='9'?khouto_ya_tlhaka-'0':khouto_ya_tlhaka>='a'&&khouto_ya_tlhaka<='f'?khouto_ya_tlhaka-'a'+10:khouto_ya_tlhaka>='A'&&khouto_ya_tlhaka<='F'?khouto_ya_tlhaka-'A'+10:99;
        if(khouto_ya_tlhaka=='.'&&!소수부){소수부=1;molokoloko_data++;continue;}if(boyo_data>=Bokamorago_boleng)break;하나라도=1;molokoloko_data++;임시값=임시값*Bokamorago_boleng+boyo_data;if(소수부)lekanetša*=Bokamorago_boleng;
    }임시값/=lekanetša;
    if((Bokamorago_boleng==10&&(*molokoloko_data=='e'||*molokoloko_data=='E'))||(Bokamorago_boleng==16&&(*molokoloko_data=='p'||*molokoloko_data=='P'))){const char*bontšha_boleng=molokoloko_data++;int 빼기=0;if(*molokoloko_data=='-'||*molokoloko_data=='+')빼기=*molokoloko_data++=='-';int 개수=0,항목수=0;while(*molokoloko_data>='0'&&*molokoloko_data<='9'){항목수++;if(개수<20000)개수=개수*10+*molokoloko_data-'0';molokoloko_data++;}if(!항목수)molokoloko_data=bontšha_boleng;else{long double katišani=Bokamorago_boleng==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/katišani:임시값*katišani;}}
    if(fetša_E_Šetšego)*fetša_E_Šetšego=(char*)(하나라도?molokoloko_data:Thomišo_E_Šetšego);return 음수여부?-임시값:임시값;
}
double strtod(const char*molokoloko_data,char**보조항목){return (double)strtold(molokoloko_data,보조항목);}float strtof(const char*molokoloko_data,char**보조항목){return (float)strtold(molokoloko_data,보조항목);}
void qsort(void*Bokamorago_boleng,size_t 개수,size_t Bogolo,int(*Papetšo)(const void*,const void*)){
    unsigned char*자료위치=Bokamorago_boleng;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Papetšo(자료위치+(안쪽순번-1)*Bogolo,자료위치+안쪽순번*Bogolo)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Bogolo;셋째순번++){unsigned char khouto_ya_tlhaka=자료위치[(안쪽순번-1)*Bogolo+셋째순번];자료위치[(안쪽순번-1)*Bogolo+셋째순번]=자료위치[안쪽순번*Bogolo+셋째순번];자료위치[안쪽순번*Bogolo+셋째순번]=khouto_ya_tlhaka;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*Leina,int 설정비트,...){
    if(!strcmp(Leina,"/@cc-output")){if(출력열림){Phošo=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Leina,번역기자원들[순번].Leina)){
        if(설정비트&3){Phošo=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}Phošo=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Leina,설정비트,0,0,0,0);if(반환값<0){Phošo=-반환값;return -1;}return 반환값;
}
int close(int faele_tshwaro){if(faele_tshwaro==100){출력열림=0;return 0;}if(faele_tshwaro>=128&&faele_tshwaro<152){열림[faele_tshwaro-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,faele_tshwaro,0,0,0,0,0);if(반환값<0){Phošo=-반환값;return -1;}return 0;}
long read(int faele_tshwaro,void*data,size_t 개수){
    if(faele_tshwaro>=128&&faele_tshwaro<152&&열림[faele_tshwaro-128].사용량){int 순번=faele_tshwaro-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->Bogolo-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(data,반환값->data+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,faele_tshwaro,(uintptr_t)data,개수,0,0,0);if(반환값<0){Phošo=-반환값;return -1;}return 반환값;
}
long write(int faele_tshwaro,const void*data,size_t 개수){
    if(faele_tshwaro==100){if(개수>sizeof(출력결과)-출력위치){Phošo=28;return -1;}memcpy(출력결과+출력위치,data,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,faele_tshwaro,(uintptr_t)data,개수,0,0,0);if(반환값<0){Phošo=-반환값;return -1;}return 반환값;
}
long lseek(int faele_tshwaro,long E_Šetšego_boleng,int 기준점){
    if(faele_tshwaro==100){long 자료위치=E_Šetšego_boleng+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){Phošo=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(faele_tshwaro>=128&&faele_tshwaro<152&&열림[faele_tshwaro-128].사용량){int 순번=faele_tshwaro-128;long 자료위치=E_Šetšego_boleng+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].Bogolo);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].Bogolo){Phošo=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,faele_tshwaro,E_Šetšego_boleng,기준점,0,0,0);if(반환값<0){Phošo=-반환값;return -1;}return 반환값;
}
int unlink(const char*Leina){intptr_t 반환값=사용자호출(11,(uintptr_t)Leina,0,0,0,0,0);if(반환값<0){Phošo=-반환값;return -1;}return 반환값;}
char *realpath(const char*Leina,char*결과자료){if(!결과자료){결과자료=malloc(strlen(Leina)+1);if(!결과자료)return 0;}return strcpy(결과자료,Leina);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){Phošo=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int faele_tshwaro,const char*mokgwa_mokgwa){(void)mokgwa_mokgwa;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Phošo=0;흐름목록[순번].faele_tshwaro=faele_tshwaro;return &흐름목록[순번];}Phošo=24;return 0;}
int fflush(FILE*faele_go_tsenya_tshedimošo){return faele_go_tsenya_tshedimošo&&faele_go_tsenya_tshedimošo->Phošo?-1:0;}
int fclose(FILE*faele_go_tsenya_tshedimošo){int 반환값=close(faele_go_tsenya_tshedimošo->faele_tshwaro);if(faele_go_tsenya_tshedimošo->Phošo)반환값=-1;faele_go_tsenya_tshedimošo->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t molokoloko_data,size_t 개수,FILE*faele_go_tsenya_tshedimošo){if(!molokoloko_data)return 0;if(개수>SIZE_MAX/molokoloko_data){faele_go_tsenya_tshedimošo->Phošo=1;return 0;}long 반환값=write(faele_go_tsenya_tshedimošo->faele_tshwaro,자료위치,molokoloko_data*개수);if(반환값<0){faele_go_tsenya_tshedimošo->Phošo=1;return 0;}return (size_t)반환값/molokoloko_data;}
int fputc(int khouto_ya_tlhaka,FILE*faele_go_tsenya_tshedimošo){unsigned char 둘째값=khouto_ya_tlhaka;return fwrite(&둘째값,1,1,faele_go_tsenya_tshedimošo)==1?둘째값:EOF;}
int fputs(const char*molokoloko_data,FILE*faele_go_tsenya_tshedimošo){return fwrite(molokoloko_data,1,strlen(molokoloko_data),faele_go_tsenya_tshedimošo)==strlen(molokoloko_data)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char khouto_ya_tlhaka){if(*현재위치+1<용량한도)결과자료[*현재위치]=khouto_ya_tlhaka;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*fomete,va_list 가변인수){
    size_t 현재위치=0;while(*fomete){if(*fomete!='%'){넣기(결과자료,용량한도,&현재위치,*fomete++);continue;}fomete++;
        int 왼쪽=0,영값=0,대체값=0;while(*fomete=='-'||*fomete=='0'||*fomete=='#'||*fomete=='+'||*fomete==' '){if(*fomete=='-')왼쪽=1;if(*fomete=='0')영값=1;if(*fomete=='#')대체값=1;fomete++;}
        int 너비=0,정밀도=-1;if(*fomete=='*'){너비=va_arg(가변인수,int);fomete++;}else while(*fomete>='0'&&*fomete<='9')너비=너비*10+*fomete++-'0';
        if(*fomete=='.'){fomete++;정밀도=0;if(*fomete=='*'){정밀도=va_arg(가변인수,int);fomete++;}else while(*fomete>='0'&&*fomete<='9')정밀도=정밀도*10+*fomete++-'0';}
        int 넓은글자=0;while(*fomete=='l'||*fomete=='z'||*fomete=='t'||*fomete=='j'||*fomete=='h'){if(*fomete!='h')넓은글자=1;fomete++;}
        char thaepa_legoro=*fomete?*fomete++:0,pafara_Bobolokelo[80];const char*molokoloko_data=pafara_Bobolokelo;size_t 개수=0;
        if(thaepa_legoro=='s'){molokoloko_data=va_arg(가변인수,const char*);if(!molokoloko_data)molokoloko_data="(null)";개수=strlen(molokoloko_data);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(thaepa_legoro=='c'){pafara_Bobolokelo[0]=va_arg(가변인수,int);개수=1;}
        else if(thaepa_legoro=='%'){pafara_Bobolokelo[0]='%';개수=1;}
        else if(thaepa_legoro=='d'||thaepa_legoro=='i'||thaepa_legoro=='u'||thaepa_legoro=='x'||thaepa_legoro=='X'||thaepa_legoro=='o'||thaepa_legoro=='p'){
            unsigned long long boleng;int 음수표시=0;
            if(thaepa_legoro=='d'||thaepa_legoro=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;boleng=음수표시?0-(unsigned long long)임시값:임시값;}
            else boleng=thaepa_legoro=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Bokamorago_boleng=thaepa_legoro=='x'||thaepa_legoro=='X'||thaepa_legoro=='p'?16:thaepa_legoro=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[boleng%Bokamorago_boleng];boleng/=Bokamorago_boleng;}while(boleng);
            if(음수표시)pafara_Bobolokelo[개수++]='-';if(thaepa_legoro=='p'||(대체값&&Bokamorago_boleng==16)){pafara_Bobolokelo[개수++]='0';pafara_Bobolokelo[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(pafara_Bobolokelo)-사용량;채움++)pafara_Bobolokelo[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(pafara_Bobolokelo)-사용량)pafara_Bobolokelo[개수++]='0';
            while(사용량)pafara_Bobolokelo[개수++]=숫자수[--사용량];
        }else{pafara_Bobolokelo[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,molokoloko_data[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*faele_go_tsenya_tshedimošo,...){va_list 첫째값;va_start(첫째값,faele_go_tsenya_tshedimošo);int 반환값=vsnprintf(결과자료,용량한도,faele_go_tsenya_tshedimošo,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*faele_go_tsenya_tshedimošo,...){va_list 첫째값;va_start(첫째값,faele_go_tsenya_tshedimošo);int 반환값=vsnprintf(결과자료,SIZE_MAX,faele_go_tsenya_tshedimošo,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_boleng,const char*faele_go_tsenya_tshedimošo,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),faele_go_tsenya_tshedimošo,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,Stream_boleng)==(size_t)개수?개수:-1;}
int fprintf(FILE*Stream_boleng,const char*faele_go_tsenya_tshedimošo,...){va_list 첫째값;va_start(첫째값,faele_go_tsenya_tshedimošo);int 반환값=vfprintf(Stream_boleng,faele_go_tsenya_tshedimošo,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*faele_go_tsenya_tshedimošo,...){va_list 첫째값;va_start(첫째값,faele_go_tsenya_tshedimošo);int 반환값=vfprintf(stdout,faele_go_tsenya_tshedimošo,첫째값);va_end(첫째값);return 반환값;}
