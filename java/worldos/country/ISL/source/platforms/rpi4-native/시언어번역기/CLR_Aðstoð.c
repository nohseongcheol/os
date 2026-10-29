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
static int Villa;
int *__errno_location(void){return &Villa;}
void exit(int staða_VALUE_e10195a1){사용자호출(6,staða_VALUE_e10195a1,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *athuga_segð,const char *Skrá,unsigned Lína,const char *aðferð_færsla_heiti){fprintf(stderr,"cc assertion: %s %s:%u %s\n",athuga_segð,Skrá,Lína,aðferð_færsla_heiti);exit(1);}
size_t strlen(const char*strengur_gögn){const char*gögn_staða=strengur_gögn;while(*gögn_staða)gögn_staða++;return gögn_staða-strengur_gögn;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t vara_COUNT){while(vara_COUNT--){unsigned char x_hnit=*첫째값++,Y_hnit=*SECOND_VALUE++;if(x_hnit!=Y_hnit)return x_hnit-Y_hnit;if(!x_hnit)return 0;}return 0;}
char *strcpy(char*endastaður_gögn,const char*strengur_gögn){char*반환값=endastaður_gögn;while((*endastaður_gögn++=*strengur_gögn++)){}return 반환값;}
char *strchr(const char*strengur_gögn,int stafkóði){do{if(*strengur_gögn==(char)stafkóði)return (char*)strengur_gögn;}while(*strengur_gögn++);return 0;}
char *strrchr(const char*strengur_gögn,int stafkóði){const char*반환값=0;do{if(*strengur_gögn==(char)stafkóði)반환값=strengur_gögn;}while(*strengur_gögn++);return (char*)반환값;}
char *strstr(const char*strengur_gögn,const char*Endastöð_færsla){size_t vara_COUNT=strlen(Endastöð_færsla);for(;*strengur_gögn;strengur_gögn++)if(!strncmp(strengur_gögn,Endastöð_færsla,vara_COUNT))return (char*)strengur_gögn;return vara_COUNT?0:(char*)strengur_gögn;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t vara_COUNT){const unsigned char*x_hnit=첫째값,*Y_hnit=SECOND_VALUE;while(vara_COUNT--){if(*x_hnit!=*Y_hnit)return *x_hnit-*Y_hnit;x_hnit++;Y_hnit++;}return 0;}
void *memmove(void*endastaður_gögn,const void*strengur_gögn,size_t vara_COUNT){unsigned char*x_hnit=endastaður_gögn;const unsigned char*Y_hnit=strengur_gögn;if(x_hnit<Y_hnit){for(size_t 순번=0;순번<vara_COUNT;순번++)x_hnit[순번]=Y_hnit[순번];}else while(vara_COUNT){vara_COUNT--;x_hnit[vara_COUNT]=Y_hnit[vara_COUNT];}return endastaður_gögn;}
static unsigned char úthlutun_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct gögn_útiloka {size_t Stærð;struct gögn_útiloka*Áfram_vara;int 남은공간;int 채울크기;uint64_t stilling_eining;} gögn_útiloka;
static gögn_útiloka *첫항목;
void free(void*gögn_staða){if(!gögn_staða)return;gögn_útiloka*SECOND_VALUE=(gögn_útiloka*)gögn_staða-1;SECOND_VALUE->남은공간=1;for(gögn_útiloka*Áfram_OFFSET=첫항목;Áfram_OFFSET&&Áfram_OFFSET->Áfram_vara;){if(Áfram_OFFSET->남은공간&&Áfram_OFFSET->Áfram_vara->남은공간){Áfram_OFFSET->Stærð+=sizeof(gögn_útiloka)+Áfram_OFFSET->Áfram_vara->Stærð;Áfram_OFFSET->Áfram_vara=Áfram_OFFSET->Áfram_vara->Áfram_vara;}else Áfram_OFFSET=Áfram_OFFSET->Áfram_vara;}}
void *realloc(void*gögn_staða,size_t vara_COUNT){
    if(!vara_COUNT){free(gögn_staða);return 0;}if(vara_COUNT>sizeof(úthlutun_Arena)-sizeof(gögn_útiloka))return 0;vara_COUNT=(vara_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(gögn_útiloka*)úthlutun_Arena;첫항목->Stærð=sizeof(úthlutun_Arena)-sizeof(gögn_útiloka);첫항목->남은공간=1;첫항목->Áfram_vara=0;}
    gögn_útiloka*이전=gögn_staða?(gögn_útiloka*)gögn_staða-1:0;if(이전&&이전->Stærð>=vara_COUNT)return gögn_staða;
    for(gögn_útiloka*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Áfram_vara)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Stærð>=vara_COUNT){
        if(SECOND_VALUE->Stærð>=vara_COUNT+sizeof(gögn_útiloka)+16){gögn_útiloka*나머지부분=(gögn_útiloka*)((unsigned char*)(SECOND_VALUE+1)+vara_COUNT);나머지부분->Stærð=SECOND_VALUE->Stærð-vara_COUNT-sizeof(gögn_útiloka);나머지부분->Áfram_vara=SECOND_VALUE->Áfram_vara;나머지부분->남은공간=1;SECOND_VALUE->Áfram_vara=나머지부분;SECOND_VALUE->Stærð=vara_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,gögn_staða,이전->Stærð);free(gögn_staða);}return 반환값;
    }Villa=12;return 0;
}
void *malloc(size_t vara_COUNT){return realloc(0,vara_COUNT);}
void *calloc(size_t vara_COUNT,size_t strengur_gögn){if(strengur_gögn&&vara_COUNT>SIZE_MAX/strengur_gögn)return 0;void*gögn_staða=malloc(vara_COUNT*strengur_gögn);if(gögn_staða)memset(gögn_staða,0,vara_COUNT*strengur_gögn);return gögn_staða;}
unsigned long long strtoull(const char*strengur_gögn,char**ljúka_OFFSET,int veggfóður_VALUE){
    const char*Opna_OFFSET=strengur_gögn;while(*strengur_gögn==' '||(*strengur_gögn>=9&&*strengur_gögn<=13))strengur_gögn++;int 음수여부=0;if(*strengur_gögn=='-'||*strengur_gögn=='+')음수여부=*strengur_gögn++=='-';
    if((!veggfóður_VALUE||veggfóður_VALUE==16)&&strengur_gögn[0]=='0'&&(strengur_gögn[1]=='x'||strengur_gögn[1]=='X')){veggfóður_VALUE=16;strengur_gögn+=2;}if(!veggfóður_VALUE)veggfóður_VALUE=*strengur_gögn=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned stafkóði=*strengur_gögn,endastaður_gögn=stafkóði>='0'&&stafkóði<='9'?stafkóði-'0':stafkóði>='a'&&stafkóði<='z'?stafkóði-'a'+10:stafkóði>='A'&&stafkóði<='Z'?stafkóði-'A'+10:99;if(endastaður_gögn>=(unsigned)veggfóður_VALUE)break;하나라도=1;strengur_gögn++;if(임시값>(~0ull-endastaður_gögn)/(unsigned)veggfóður_VALUE){임시값=~0ull;Villa=34;}else 임시값=임시값*veggfóður_VALUE+endastaður_gögn;}
    if(ljúka_OFFSET)*ljúka_OFFSET=(char*)(하나라도?strengur_gögn:Opna_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*strengur_gögn,char**보조항목,int SECOND_VALUE){return strtoull(strengur_gögn,보조항목,SECOND_VALUE);}
long strtol(const char*strengur_gögn,char**보조항목,int SECOND_VALUE){return (long)strtoull(strengur_gögn,보조항목,SECOND_VALUE);}
int atoi(const char*strengur_gögn){return (int)strtol(strengur_gögn,0,10);}
long double ldexpl(long double x_hnit,int vara_COUNT){while(vara_COUNT>0){x_hnit*=2;vara_COUNT--;}while(vara_COUNT<0){x_hnit/=2;vara_COUNT++;}return x_hnit;}
long double strtold(const char*strengur_gögn,char**ljúka_OFFSET){
    const char*Opna_OFFSET=strengur_gögn;while(*strengur_gögn==' '||(*strengur_gögn>=9&&*strengur_gögn<=13))strengur_gögn++;int 음수여부=0;if(*strengur_gögn=='-'||*strengur_gögn=='+')음수여부=*strengur_gögn++=='-';
    int veggfóður_VALUE=10;if(strengur_gögn[0]=='0'&&(strengur_gögn[1]=='x'||strengur_gögn[1]=='X')){veggfóður_VALUE=16;strengur_gögn+=2;}long double 임시값=0,kvarða=1;int 소수부=0,하나라도=0;
    for(;;){int stafkóði=*strengur_gögn,endastaður_gögn=stafkóði>='0'&&stafkóði<='9'?stafkóði-'0':stafkóði>='a'&&stafkóði<='f'?stafkóði-'a'+10:stafkóði>='A'&&stafkóði<='F'?stafkóði-'A'+10:99;
        if(stafkóði=='.'&&!소수부){소수부=1;strengur_gögn++;continue;}if(endastaður_gögn>=veggfóður_VALUE)break;하나라도=1;strengur_gögn++;임시값=임시값*veggfóður_VALUE+endastaður_gögn;if(소수부)kvarða*=veggfóður_VALUE;
    }임시값/=kvarða;
    if((veggfóður_VALUE==10&&(*strengur_gögn=='e'||*strengur_gögn=='E'))||(veggfóður_VALUE==16&&(*strengur_gögn=='p'||*strengur_gögn=='P'))){const char*sýna_VALUE=strengur_gögn++;int 빼기=0;if(*strengur_gögn=='-'||*strengur_gögn=='+')빼기=*strengur_gögn++=='-';int vara_COUNT=0,færsla_COUNT=0;while(*strengur_gögn>='0'&&*strengur_gögn<='9'){færsla_COUNT++;if(vara_COUNT<20000)vara_COUNT=vara_COUNT*10+*strengur_gögn-'0';strengur_gögn++;}if(!færsla_COUNT)strengur_gögn=sýna_VALUE;else{long double þátta=veggfóður_VALUE==16?2:10;while(vara_COUNT-->0&&vara_COUNT<200000)임시값=빼기?임시값/þátta:임시값*þátta;}}
    if(ljúka_OFFSET)*ljúka_OFFSET=(char*)(하나라도?strengur_gögn:Opna_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*strengur_gögn,char**보조항목){return (double)strtold(strengur_gögn,보조항목);}float strtof(const char*strengur_gögn,char**보조항목){return (float)strtold(strengur_gögn,보조항목);}
void qsort(void*veggfóður_VALUE,size_t vara_COUNT,size_t Stærð,int(*bera_saman)(const void*,const void*)){
    unsigned char*gögn_staða=veggfóður_VALUE;for(size_t 순번=1;순번<vara_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&bera_saman(gögn_staða+(안쪽순번-1)*Stærð,gögn_staða+안쪽순번*Stærð)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Stærð;셋째순번++){unsigned char stafkóði=gögn_staða[(안쪽순번-1)*Stærð+셋째순번];gögn_staða[(안쪽순번-1)*Stærð+셋째순번]=gögn_staða[안쪽순번*Stærð+셋째순번];gögn_staða[안쪽순번*Stærð+셋째순번]=stafkóði;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Staðsetning;} 열림[24];
static unsigned char úttak_54cd5e1d[32768];static size_t úttak_breyta_stærð,úttak_staða;static int úttak_opið;
const unsigned char *시언어출력(size_t *vara_COUNT){*vara_COUNT=úttak_breyta_stærð;return úttak_54cd5e1d;}
int open(const char*Heiti,int afbrigði_Background_Intelligent_Transfer_Service,...){
    if(!strcmp(Heiti,"/@cc-output")){if(úttak_opið){Villa=16;return -1;}úttak_opið=1;úttak_breyta_stærð=úttak_staða=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Heiti,번역기자원들[순번].Heiti)){
        if(afbrigði_Background_Intelligent_Transfer_Service&3){Villa=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Staðsetning=0;return 128+안쪽순번;}Villa=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Heiti,afbrigði_Background_Intelligent_Transfer_Service,0,0,0,0);if(반환값<0){Villa=-반환값;return -1;}return 반환값;
}
int close(int skrá_hald){if(skrá_hald==100){úttak_opið=0;return 0;}if(skrá_hald>=128&&skrá_hald<152){열림[skrá_hald-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,skrá_hald,0,0,0,0,0);if(반환값<0){Villa=-반환값;return -1;}return 0;}
long read(int skrá_hald,void*gögn,size_t vara_COUNT){
    if(skrá_hald>=128&&skrá_hald<152&&열림[skrá_hald-128].사용량){int 순번=skrá_hald-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Stærð-열림[순번].Staðsetning;if(vara_COUNT>왼쪽)vara_COUNT=왼쪽;memcpy(gögn,반환값->gögn+열림[순번].Staðsetning,vara_COUNT);열림[순번].Staðsetning+=vara_COUNT;return vara_COUNT;}
    intptr_t 반환값=사용자호출(2,skrá_hald,(uintptr_t)gögn,vara_COUNT,0,0,0);if(반환값<0){Villa=-반환값;return -1;}return 반환값;
}
long write(int skrá_hald,const void*gögn,size_t vara_COUNT){
    if(skrá_hald==100){if(vara_COUNT>sizeof(úttak_54cd5e1d)-úttak_staða){Villa=28;return -1;}memcpy(úttak_54cd5e1d+úttak_staða,gögn,vara_COUNT);úttak_staða+=vara_COUNT;if(úttak_breyta_stærð<úttak_staða)úttak_breyta_stærð=úttak_staða;return vara_COUNT;}
    intptr_t 반환값=사용자호출(1,skrá_hald,(uintptr_t)gögn,vara_COUNT,0,0,0);if(반환값<0){Villa=-반환값;return -1;}return 반환값;
}
long lseek(int skrá_hald,long OFFSET_VALUE,int 기준점){
    if(skrá_hald==100){long gögn_staða=OFFSET_VALUE+(기준점==0?0:기준점==1?úttak_staða:úttak_breyta_stærð);if(gögn_staða<0||(size_t)gögn_staða>sizeof(úttak_54cd5e1d)){Villa=22;return -1;}úttak_staða=gögn_staða;return gögn_staða;}
    if(skrá_hald>=128&&skrá_hald<152&&열림[skrá_hald-128].사용량){int 순번=skrá_hald-128;long gögn_staða=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].Staðsetning:번역기자원들[열림[순번].LOOKUP_INDEX].Stærð);if(gögn_staða<0||(size_t)gögn_staða>번역기자원들[열림[순번].LOOKUP_INDEX].Stærð){Villa=22;return -1;}열림[순번].Staðsetning=gögn_staða;return gögn_staða;}
    intptr_t 반환값=사용자호출(5,skrá_hald,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){Villa=-반환값;return -1;}return 반환값;
}
int unlink(const char*Heiti){intptr_t 반환값=사용자호출(11,(uintptr_t)Heiti,0,0,0,0,0);if(반환값<0){Villa=-반환값;return -1;}return 반환값;}
char *realpath(const char*Heiti,char*mæld_stærð_gögn){if(!mæld_stærð_gögn){mæld_stærð_gögn=malloc(strlen(Heiti)+1);if(!mæld_stærð_gögn)return 0;}return strcpy(mæld_stærð_gögn,Heiti);}
char *getcwd(char*gögn_staða,size_t vara_COUNT){if(vara_COUNT<2){Villa=34;return 0;}gögn_staða[0]='/';gögn_staða[1]=0;return gögn_staða;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Endastöð_færsla){time_t 임시값=0;if(Endastöð_færsla)*Endastöð_færsla=임시값;return 임시값;}
struct tm *localtime(const time_t*Endastöð_færsla){(void)Endastöð_færsla;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int skrá_hald,const char*aðferð_MODE){(void)aðferð_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Villa=0;흐름목록[순번].skrá_hald=skrá_hald;return &흐름목록[순번];}Villa=24;return 0;}
int fflush(FILE*skrá_færsla_3d0c1245){return skrá_færsla_3d0c1245&&skrá_færsla_3d0c1245->Villa?-1:0;}
int fclose(FILE*skrá_færsla_3d0c1245){int 반환값=close(skrá_færsla_3d0c1245->skrá_hald);if(skrá_færsla_3d0c1245->Villa)반환값=-1;skrá_færsla_3d0c1245->사용량=0;return 반환값;}
size_t fwrite(const void*gögn_staða,size_t strengur_gögn,size_t vara_COUNT,FILE*skrá_færsla_3d0c1245){if(!strengur_gögn)return 0;if(vara_COUNT>SIZE_MAX/strengur_gögn){skrá_færsla_3d0c1245->Villa=1;return 0;}long 반환값=write(skrá_færsla_3d0c1245->skrá_hald,gögn_staða,strengur_gögn*vara_COUNT);if(반환값<0){skrá_færsla_3d0c1245->Villa=1;return 0;}return (size_t)반환값/strengur_gögn;}
int fputc(int stafkóði,FILE*skrá_færsla_3d0c1245){unsigned char SECOND_VALUE=stafkóði;return fwrite(&SECOND_VALUE,1,1,skrá_færsla_3d0c1245)==1?SECOND_VALUE:EOF;}
int fputs(const char*strengur_gögn,FILE*skrá_færsla_3d0c1245){return fwrite(strengur_gögn,1,strlen(strengur_gögn),skrá_færsla_3d0c1245)==strlen(strengur_gögn)?0:EOF;}
static void 넣기(char*mæld_stærð_gögn,size_t 용량한도,size_t*현재위치,char stafkóði){if(*현재위치+1<용량한도)mæld_stærð_gögn[*현재위치]=stafkóði;(*현재위치)++;}
int vsnprintf(char*mæld_stærð_gögn,size_t 용량한도,const char*snið,va_list 가변인수){
    size_t 현재위치=0;while(*snið){if(*snið!='%'){넣기(mæld_stærð_gögn,용량한도,&현재위치,*snið++);continue;}snið++;
        int 왼쪽=0,영값=0,대체값=0;while(*snið=='-'||*snið=='0'||*snið=='#'||*snið=='+'||*snið==' '){if(*snið=='-')왼쪽=1;if(*snið=='0')영값=1;if(*snið=='#')대체값=1;snið++;}
        int 너비=0,정밀도=-1;if(*snið=='*'){너비=va_arg(가변인수,int);snið++;}else while(*snið>='0'&&*snið<='9')너비=너비*10+*snið++-'0';
        if(*snið=='.'){snið++;정밀도=0;if(*snið=='*'){정밀도=va_arg(가변인수,int);snið++;}else while(*snið>='0'&&*snið<='9')정밀도=정밀도*10+*snið++-'0';}
        int 넓은글자=0;while(*snið=='l'||*snið=='z'||*snið=='t'||*snið=='j'||*snið=='h'){if(*snið!='h')넓은글자=1;snið++;}
        char TYPE_tegund=*snið?*snið++:0,biðminni_geymsla[80];const char*strengur_gögn=biðminni_geymsla;size_t vara_COUNT=0;
        if(TYPE_tegund=='s'){strengur_gögn=va_arg(가변인수,const char*);if(!strengur_gögn)strengur_gögn="(null)";vara_COUNT=strlen(strengur_gögn);if(정밀도>=0&&vara_COUNT>(size_t)정밀도)vara_COUNT=정밀도;}
        else if(TYPE_tegund=='c'){biðminni_geymsla[0]=va_arg(가변인수,int);vara_COUNT=1;}
        else if(TYPE_tegund=='%'){biðminni_geymsla[0]='%';vara_COUNT=1;}
        else if(TYPE_tegund=='d'||TYPE_tegund=='i'||TYPE_tegund=='u'||TYPE_tegund=='x'||TYPE_tegund=='X'||TYPE_tegund=='o'||TYPE_tegund=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_tegund=='d'||TYPE_tegund=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_tegund=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned veggfóður_VALUE=TYPE_tegund=='x'||TYPE_tegund=='X'||TYPE_tegund=='p'?16:TYPE_tegund=='o'?8:10;char tölustafur_COUNT[64];unsigned 사용량=0;
            do{tölustafur_COUNT[사용량++]="0123456789abcdef"[VALUE%veggfóður_VALUE];VALUE/=veggfóður_VALUE;}while(VALUE);
            if(음수표시)biðminni_geymsla[vara_COUNT++]='-';if(TYPE_tegund=='p'||(대체값&&veggfóður_VALUE==16)){biðminni_geymsla[vara_COUNT++]='0';biðminni_geymsla[vara_COUNT++]='x';}
            for(int fylla_VALUE=(int)사용량;정밀도>fylla_VALUE&&vara_COUNT<sizeof(biðminni_geymsla)-사용량;fylla_VALUE++)biðminni_geymsla[vara_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(vara_COUNT+사용량)&&vara_COUNT<sizeof(biðminni_geymsla)-사용량)biðminni_geymsla[vara_COUNT++]='0';
            while(사용량)biðminni_geymsla[vara_COUNT++]=tölustafur_COUNT[--사용량];
        }else{biðminni_geymsla[0]='?';vara_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)vara_COUNT){넣기(mæld_stærð_gögn,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<vara_COUNT;순번++)넣기(mæld_stærð_gögn,용량한도,&현재위치,strengur_gögn[순번]);while(왼쪽&&너비>(int)vara_COUNT){넣기(mæld_stærð_gögn,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)mæld_stærð_gögn[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*mæld_stærð_gögn,size_t 용량한도,const char*skrá_færsla_3d0c1245,...){va_list 첫째값;va_start(첫째값,skrá_færsla_3d0c1245);int 반환값=vsnprintf(mæld_stærð_gögn,용량한도,skrá_færsla_3d0c1245,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*mæld_stærð_gögn,const char*skrá_færsla_3d0c1245,...){va_list 첫째값;va_start(첫째값,skrá_færsla_3d0c1245);int 반환값=vsnprintf(mæld_stærð_gögn,SIZE_MAX,skrá_færsla_3d0c1245,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*skrá_færsla_3d0c1245,va_list 첫째값){char SECOND_VALUE[2048];int vara_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),skrá_færsla_3d0c1245,첫째값);if(vara_COUNT>2047)vara_COUNT=2047;return fwrite(SECOND_VALUE,1,vara_COUNT,Stream_VALUE)==(size_t)vara_COUNT?vara_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*skrá_færsla_3d0c1245,...){va_list 첫째값;va_start(첫째값,skrá_færsla_3d0c1245);int 반환값=vfprintf(Stream_VALUE,skrá_færsla_3d0c1245,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*skrá_færsla_3d0c1245,...){va_list 첫째값;va_start(첫째값,skrá_færsla_3d0c1245);int 반환값=vfprintf(stdout,skrá_færsla_3d0c1245,첫째값);va_end(첫째값);return 반환값;}
