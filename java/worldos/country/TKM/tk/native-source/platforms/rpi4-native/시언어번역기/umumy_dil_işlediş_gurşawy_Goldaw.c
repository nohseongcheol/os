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
static int Hata;
int *__errno_location(void){return &Hata;}
void exit(int ýagdaý_baha){사용자호출(6,ýagdaý_baha,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *derňe_aňlatma,const char *Faýl,unsigned setir,const char *usul_girizmeklik_at){fprintf(stderr,"cc assertion: %s %s:%u %s\n",derňe_aňlatma,Faýl,setir,usul_girizmeklik_at);exit(1);}
size_t strlen(const char*setir_maglumat){const char*자료위치=setir_maglumat;while(*자료위치)자료위치++;return 자료위치-setir_maglumat;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char x_koordinatasy=*첫째값++,세로좌표=*둘째값++;if(x_koordinatasy!=세로좌표)return x_koordinatasy-세로좌표;if(!x_koordinatasy)return 0;}return 0;}
char *strcpy(char*barylmaly_ýer_maglumat,const char*setir_maglumat){char*반환값=barylmaly_ýer_maglumat;while((*barylmaly_ýer_maglumat++=*setir_maglumat++)){}return 반환값;}
char *strchr(const char*setir_maglumat,int nyşanyň_kody){do{if(*setir_maglumat==(char)nyşanyň_kody)return (char*)setir_maglumat;}while(*setir_maglumat++);return 0;}
char *strrchr(const char*setir_maglumat,int nyşanyň_kody){const char*반환값=0;do{if(*setir_maglumat==(char)nyşanyň_kody)반환값=setir_maglumat;}while(*setir_maglumat++);return (char*)반환값;}
char *strstr(const char*setir_maglumat,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*setir_maglumat;setir_maglumat++)if(!strncmp(setir_maglumat,터미널항목,개수))return (char*)setir_maglumat;return 개수?0:(char*)setir_maglumat;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*x_koordinatasy=첫째값,*세로좌표=둘째값;while(개수--){if(*x_koordinatasy!=*세로좌표)return *x_koordinatasy-*세로좌표;x_koordinatasy++;세로좌표++;}return 0;}
void *memmove(void*barylmaly_ýer_maglumat,const void*setir_maglumat,size_t 개수){unsigned char*x_koordinatasy=barylmaly_ýer_maglumat;const unsigned char*세로좌표=setir_maglumat;if(x_koordinatasy<세로좌표){for(size_t 순번=0;순번<개수;순번++)x_koordinatasy[순번]=세로좌표[순번];}else while(개수){개수--;x_koordinatasy[개수]=세로좌표[개수];}return barylmaly_ýer_maglumat;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct maglumat_bökde {size_t Ululyk;struct maglumat_bökde*다음;int 남은공간;int 채울크기;uint64_t deňlemeklik_sapak;} maglumat_bökde;
static maglumat_bökde *첫항목;
void free(void*자료위치){if(!자료위치)return;maglumat_bökde*둘째값=(maglumat_bökde*)자료위치-1;둘째값->남은공간=1;for(maglumat_bökde*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->Ululyk+=sizeof(maglumat_bökde)+다음위치->다음->Ululyk;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(maglumat_bökde))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(maglumat_bökde*)할당마당;첫항목->Ululyk=sizeof(할당마당)-sizeof(maglumat_bökde);첫항목->남은공간=1;첫항목->다음=0;}
    maglumat_bökde*이전=자료위치?(maglumat_bökde*)자료위치-1:0;if(이전&&이전->Ululyk>=개수)return 자료위치;
    for(maglumat_bökde*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->Ululyk>=개수){
        if(둘째값->Ululyk>=개수+sizeof(maglumat_bökde)+16){maglumat_bökde*나머지부분=(maglumat_bökde*)((unsigned char*)(둘째값+1)+개수);나머지부분->Ululyk=둘째값->Ululyk-개수-sizeof(maglumat_bökde);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->Ululyk=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->Ululyk);free(자료위치);}return 반환값;
    }Hata=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t setir_maglumat){if(setir_maglumat&&개수>SIZE_MAX/setir_maglumat)return 0;void*자료위치=malloc(개수*setir_maglumat);if(자료위치)memset(자료위치,0,개수*setir_maglumat);return 자료위치;}
unsigned long long strtoull(const char*setir_maglumat,char**tamamla_Süýşüriş,int Fon_baha){
    const char*başlat_Süýşüriş=setir_maglumat;while(*setir_maglumat==' '||(*setir_maglumat>=9&&*setir_maglumat<=13))setir_maglumat++;int 음수여부=0;if(*setir_maglumat=='-'||*setir_maglumat=='+')음수여부=*setir_maglumat++=='-';
    if((!Fon_baha||Fon_baha==16)&&setir_maglumat[0]=='0'&&(setir_maglumat[1]=='x'||setir_maglumat[1]=='X')){Fon_baha=16;setir_maglumat+=2;}if(!Fon_baha)Fon_baha=*setir_maglumat=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned nyşanyň_kody=*setir_maglumat,barylmaly_ýer_maglumat=nyşanyň_kody>='0'&&nyşanyň_kody<='9'?nyşanyň_kody-'0':nyşanyň_kody>='a'&&nyşanyň_kody<='z'?nyşanyň_kody-'a'+10:nyşanyň_kody>='A'&&nyşanyň_kody<='Z'?nyşanyň_kody-'A'+10:99;if(barylmaly_ýer_maglumat>=(unsigned)Fon_baha)break;하나라도=1;setir_maglumat++;if(임시값>(~0ull-barylmaly_ýer_maglumat)/(unsigned)Fon_baha){임시값=~0ull;Hata=34;}else 임시값=임시값*Fon_baha+barylmaly_ýer_maglumat;}
    if(tamamla_Süýşüriş)*tamamla_Süýşüriş=(char*)(하나라도?setir_maglumat:başlat_Süýşüriş);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*setir_maglumat,char**보조항목,int 둘째값){return strtoull(setir_maglumat,보조항목,둘째값);}
long strtol(const char*setir_maglumat,char**보조항목,int 둘째값){return (long)strtoull(setir_maglumat,보조항목,둘째값);}
int atoi(const char*setir_maglumat){return (int)strtol(setir_maglumat,0,10);}
long double ldexpl(long double x_koordinatasy,int 개수){while(개수>0){x_koordinatasy*=2;개수--;}while(개수<0){x_koordinatasy/=2;개수++;}return x_koordinatasy;}
long double strtold(const char*setir_maglumat,char**tamamla_Süýşüriş){
    const char*başlat_Süýşüriş=setir_maglumat;while(*setir_maglumat==' '||(*setir_maglumat>=9&&*setir_maglumat<=13))setir_maglumat++;int 음수여부=0;if(*setir_maglumat=='-'||*setir_maglumat=='+')음수여부=*setir_maglumat++=='-';
    int Fon_baha=10;if(setir_maglumat[0]=='0'&&(setir_maglumat[1]=='x'||setir_maglumat[1]=='X')){Fon_baha=16;setir_maglumat+=2;}long double 임시값=0,masştablaşdyr=1;int 소수부=0,하나라도=0;
    for(;;){int nyşanyň_kody=*setir_maglumat,barylmaly_ýer_maglumat=nyşanyň_kody>='0'&&nyşanyň_kody<='9'?nyşanyň_kody-'0':nyşanyň_kody>='a'&&nyşanyň_kody<='f'?nyşanyň_kody-'a'+10:nyşanyň_kody>='A'&&nyşanyň_kody<='F'?nyşanyň_kody-'A'+10:99;
        if(nyşanyň_kody=='.'&&!소수부){소수부=1;setir_maglumat++;continue;}if(barylmaly_ýer_maglumat>=Fon_baha)break;하나라도=1;setir_maglumat++;임시값=임시값*Fon_baha+barylmaly_ýer_maglumat;if(소수부)masştablaşdyr*=Fon_baha;
    }임시값/=masştablaşdyr;
    if((Fon_baha==10&&(*setir_maglumat=='e'||*setir_maglumat=='E'))||(Fon_baha==16&&(*setir_maglumat=='p'||*setir_maglumat=='P'))){const char*görkez_baha_487749b8=setir_maglumat++;int 빼기=0;if(*setir_maglumat=='-'||*setir_maglumat=='+')빼기=*setir_maglumat++=='-';int 개수=0,항목수=0;while(*setir_maglumat>='0'&&*setir_maglumat<='9'){항목수++;if(개수<20000)개수=개수*10+*setir_maglumat-'0';setir_maglumat++;}if(!항목수)setir_maglumat=görkez_baha_487749b8;else{long double köpeldiji=Fon_baha==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/köpeldiji:임시값*köpeldiji;}}
    if(tamamla_Süýşüriş)*tamamla_Süýşüriş=(char*)(하나라도?setir_maglumat:başlat_Süýşüriş);return 음수여부?-임시값:임시값;
}
double strtod(const char*setir_maglumat,char**보조항목){return (double)strtold(setir_maglumat,보조항목);}float strtof(const char*setir_maglumat,char**보조항목){return (float)strtold(setir_maglumat,보조항목);}
void qsort(void*Fon_baha,size_t 개수,size_t Ululyk,int(*deňeşdir)(const void*,const void*)){
    unsigned char*자료위치=Fon_baha;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&deňeşdir(자료위치+(안쪽순번-1)*Ululyk,자료위치+안쪽순번*Ululyk)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Ululyk;셋째순번++){unsigned char nyşanyň_kody=자료위치[(안쪽순번-1)*Ululyk+셋째순번];자료위치[(안쪽순번-1)*Ululyk+셋째순번]=자료위치[안쪽순번*Ululyk+셋째순번];자료위치[안쪽순번*Ululyk+셋째순번]=nyşanyň_kody;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*Ad,int 설정비트,...){
    if(!strcmp(Ad,"/@cc-output")){if(출력열림){Hata=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Ad,번역기자원들[순번].Ad)){
        if(설정비트&3){Hata=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}Hata=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Ad,설정비트,0,0,0,0);if(반환값<0){Hata=-반환값;return -1;}return 반환값;
}
int close(int faýl_ryçag){if(faýl_ryçag==100){출력열림=0;return 0;}if(faýl_ryçag>=128&&faýl_ryçag<152){열림[faýl_ryçag-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,faýl_ryçag,0,0,0,0,0);if(반환값<0){Hata=-반환값;return -1;}return 0;}
long read(int faýl_ryçag,void*maglumat,size_t 개수){
    if(faýl_ryçag>=128&&faýl_ryçag<152&&열림[faýl_ryçag-128].사용량){int 순번=faýl_ryçag-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->Ululyk-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(maglumat,반환값->maglumat+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,faýl_ryçag,(uintptr_t)maglumat,개수,0,0,0);if(반환값<0){Hata=-반환값;return -1;}return 반환값;
}
long write(int faýl_ryçag,const void*maglumat,size_t 개수){
    if(faýl_ryçag==100){if(개수>sizeof(출력결과)-출력위치){Hata=28;return -1;}memcpy(출력결과+출력위치,maglumat,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,faýl_ryçag,(uintptr_t)maglumat,개수,0,0,0);if(반환값<0){Hata=-반환값;return -1;}return 반환값;
}
long lseek(int faýl_ryçag,long Süýşüriş_baha,int 기준점){
    if(faýl_ryçag==100){long 자료위치=Süýşüriş_baha+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){Hata=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(faýl_ryçag>=128&&faýl_ryçag<152&&열림[faýl_ryçag-128].사용량){int 순번=faýl_ryçag-128;long 자료위치=Süýşüriş_baha+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].Ululyk);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].Ululyk){Hata=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,faýl_ryçag,Süýşüriş_baha,기준점,0,0,0);if(반환값<0){Hata=-반환값;return -1;}return 반환값;
}
int unlink(const char*Ad){intptr_t 반환값=사용자호출(11,(uintptr_t)Ad,0,0,0,0,0);if(반환값<0){Hata=-반환값;return -1;}return 반환값;}
char *realpath(const char*Ad,char*결과자료){if(!결과자료){결과자료=malloc(strlen(Ad)+1);if(!결과자료)return 0;}return strcpy(결과자료,Ad);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){Hata=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int faýl_ryçag,const char*usul_reje){(void)usul_reje;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Hata=0;흐름목록[순번].faýl_ryçag=faýl_ryçag;return &흐름목록[순번];}Hata=24;return 0;}
int fflush(FILE*faýl_girizmeklik){return faýl_girizmeklik&&faýl_girizmeklik->Hata?-1:0;}
int fclose(FILE*faýl_girizmeklik){int 반환값=close(faýl_girizmeklik->faýl_ryçag);if(faýl_girizmeklik->Hata)반환값=-1;faýl_girizmeklik->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t setir_maglumat,size_t 개수,FILE*faýl_girizmeklik){if(!setir_maglumat)return 0;if(개수>SIZE_MAX/setir_maglumat){faýl_girizmeklik->Hata=1;return 0;}long 반환값=write(faýl_girizmeklik->faýl_ryçag,자료위치,setir_maglumat*개수);if(반환값<0){faýl_girizmeklik->Hata=1;return 0;}return (size_t)반환값/setir_maglumat;}
int fputc(int nyşanyň_kody,FILE*faýl_girizmeklik){unsigned char 둘째값=nyşanyň_kody;return fwrite(&둘째값,1,1,faýl_girizmeklik)==1?둘째값:EOF;}
int fputs(const char*setir_maglumat,FILE*faýl_girizmeklik){return fwrite(setir_maglumat,1,strlen(setir_maglumat),faýl_girizmeklik)==strlen(setir_maglumat)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char nyşanyň_kody){if(*현재위치+1<용량한도)결과자료[*현재위치]=nyşanyň_kody;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*format,va_list 가변인수){
    size_t 현재위치=0;while(*format){if(*format!='%'){넣기(결과자료,용량한도,&현재위치,*format++);continue;}format++;
        int 왼쪽=0,영값=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')영값=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,정밀도=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;정밀도=0;if(*format=='*'){정밀도=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')정밀도=정밀도*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char ýaz_kategoriýa=*format?*format++:0,bufer_Ammar[80];const char*setir_maglumat=bufer_Ammar;size_t 개수=0;
        if(ýaz_kategoriýa=='s'){setir_maglumat=va_arg(가변인수,const char*);if(!setir_maglumat)setir_maglumat="(null)";개수=strlen(setir_maglumat);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(ýaz_kategoriýa=='c'){bufer_Ammar[0]=va_arg(가변인수,int);개수=1;}
        else if(ýaz_kategoriýa=='%'){bufer_Ammar[0]='%';개수=1;}
        else if(ýaz_kategoriýa=='d'||ýaz_kategoriýa=='i'||ýaz_kategoriýa=='u'||ýaz_kategoriýa=='x'||ýaz_kategoriýa=='X'||ýaz_kategoriýa=='o'||ýaz_kategoriýa=='p'){
            unsigned long long baha;int 음수표시=0;
            if(ýaz_kategoriýa=='d'||ýaz_kategoriýa=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;baha=음수표시?0-(unsigned long long)임시값:임시값;}
            else baha=ýaz_kategoriýa=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Fon_baha=ýaz_kategoriýa=='x'||ýaz_kategoriýa=='X'||ýaz_kategoriýa=='p'?16:ýaz_kategoriýa=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[baha%Fon_baha];baha/=Fon_baha;}while(baha);
            if(음수표시)bufer_Ammar[개수++]='-';if(ýaz_kategoriýa=='p'||(대체값&&Fon_baha==16)){bufer_Ammar[개수++]='0';bufer_Ammar[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(bufer_Ammar)-사용량;채움++)bufer_Ammar[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(bufer_Ammar)-사용량)bufer_Ammar[개수++]='0';
            while(사용량)bufer_Ammar[개수++]=숫자수[--사용량];
        }else{bufer_Ammar[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,setir_maglumat[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*faýl_girizmeklik,...){va_list 첫째값;va_start(첫째값,faýl_girizmeklik);int 반환값=vsnprintf(결과자료,용량한도,faýl_girizmeklik,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*faýl_girizmeklik,...){va_list 첫째값;va_start(첫째값,faýl_girizmeklik);int 반환값=vsnprintf(결과자료,SIZE_MAX,faýl_girizmeklik,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_baha,const char*faýl_girizmeklik,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),faýl_girizmeklik,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,Stream_baha)==(size_t)개수?개수:-1;}
int fprintf(FILE*Stream_baha,const char*faýl_girizmeklik,...){va_list 첫째값;va_start(첫째값,faýl_girizmeklik);int 반환값=vfprintf(Stream_baha,faýl_girizmeklik,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*faýl_girizmeklik,...){va_list 첫째값;va_start(첫째값,faýl_girizmeklik);int 반환값=vfprintf(stdout,faýl_girizmeklik,첫째값);va_end(첫째값);return 반환값;}
