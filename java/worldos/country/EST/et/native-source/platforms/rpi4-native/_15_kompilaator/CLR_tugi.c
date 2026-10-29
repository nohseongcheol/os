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
static int VIGA;
int *__errno_location(void){return &VIGA;}
void exit(int Olek_VALUE){사용자호출(6,Olek_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *tšekk_avaldis,const char *Fail,unsigned Joon,const char *meetod_kirje_nimetus){fprintf(stderr,"cc assertion: %s %s:%u %s\n",tšekk_avaldis,Fail,Joon,meetod_kirje_nimetus);exit(1);}
size_t strlen(const char*string_andmed){const char*andmed_ametikoht=string_andmed;while(*andmed_ametikoht)andmed_ametikoht++;return andmed_ametikoht-string_andmed;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t kaup_COUNT){while(kaup_COUNT--){unsigned char 가로좌표=*첫째값++,세로좌표=*SECOND_VALUE++;if(가로좌표!=세로좌표)return 가로좌표-세로좌표;if(!가로좌표)return 0;}return 0;}
char *strcpy(char*sihtkoht_andmed,const char*string_andmed){char*반환값=sihtkoht_andmed;while((*sihtkoht_andmed++=*string_andmed++)){}return 반환값;}
char *strchr(const char*string_andmed,int koodipunkt){do{if(*string_andmed==(char)koodipunkt)return (char*)string_andmed;}while(*string_andmed++);return 0;}
char *strrchr(const char*string_andmed,int koodipunkt){const char*반환값=0;do{if(*string_andmed==(char)koodipunkt)반환값=string_andmed;}while(*string_andmed++);return (char*)반환값;}
char *strstr(const char*string_andmed,const char*terminal_kirje){size_t kaup_COUNT=strlen(terminal_kirje);for(;*string_andmed;string_andmed++)if(!strncmp(string_andmed,terminal_kirje,kaup_COUNT))return (char*)string_andmed;return kaup_COUNT?0:(char*)string_andmed;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t kaup_COUNT){const unsigned char*가로좌표=첫째값,*세로좌표=SECOND_VALUE;while(kaup_COUNT--){if(*가로좌표!=*세로좌표)return *가로좌표-*세로좌표;가로좌표++;세로좌표++;}return 0;}
void *memmove(void*sihtkoht_andmed,const void*string_andmed,size_t kaup_COUNT){unsigned char*가로좌표=sihtkoht_andmed;const unsigned char*세로좌표=string_andmed;if(가로좌표<세로좌표){for(size_t 순번=0;순번<kaup_COUNT;순번++)가로좌표[순번]=세로좌표[순번];}else while(kaup_COUNT){kaup_COUNT--;가로좌표[kaup_COUNT]=세로좌표[kaup_COUNT];}return sihtkoht_andmed;}
static unsigned char eraldus_Areen[6*1024*1024] __attribute__((aligned(16)));
typedef struct andmeplokk {size_t Suurus;struct andmeplokk*Edasi_kaup;int 남은공간;int täidis;uint64_t joondus_ühik;} andmeplokk;
static andmeplokk *첫항목;
void free(void*andmed_ametikoht){if(!andmed_ametikoht)return;andmeplokk*SECOND_VALUE=(andmeplokk*)andmed_ametikoht-1;SECOND_VALUE->남은공간=1;for(andmeplokk*Edasi_nihe=첫항목;Edasi_nihe&&Edasi_nihe->Edasi_kaup;){if(Edasi_nihe->남은공간&&Edasi_nihe->Edasi_kaup->남은공간){Edasi_nihe->Suurus+=sizeof(andmeplokk)+Edasi_nihe->Edasi_kaup->Suurus;Edasi_nihe->Edasi_kaup=Edasi_nihe->Edasi_kaup->Edasi_kaup;}else Edasi_nihe=Edasi_nihe->Edasi_kaup;}}
void *realloc(void*andmed_ametikoht,size_t kaup_COUNT){
    if(!kaup_COUNT){free(andmed_ametikoht);return 0;}if(kaup_COUNT>sizeof(eraldus_Areen)-sizeof(andmeplokk))return 0;kaup_COUNT=(kaup_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(andmeplokk*)eraldus_Areen;첫항목->Suurus=sizeof(eraldus_Areen)-sizeof(andmeplokk);첫항목->남은공간=1;첫항목->Edasi_kaup=0;}
    andmeplokk*이전=andmed_ametikoht?(andmeplokk*)andmed_ametikoht-1:0;if(이전&&이전->Suurus>=kaup_COUNT)return andmed_ametikoht;
    for(andmeplokk*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Edasi_kaup)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Suurus>=kaup_COUNT){
        if(SECOND_VALUE->Suurus>=kaup_COUNT+sizeof(andmeplokk)+16){andmeplokk*나머지부분=(andmeplokk*)((unsigned char*)(SECOND_VALUE+1)+kaup_COUNT);나머지부분->Suurus=SECOND_VALUE->Suurus-kaup_COUNT-sizeof(andmeplokk);나머지부분->Edasi_kaup=SECOND_VALUE->Edasi_kaup;나머지부분->남은공간=1;SECOND_VALUE->Edasi_kaup=나머지부분;SECOND_VALUE->Suurus=kaup_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,andmed_ametikoht,이전->Suurus);free(andmed_ametikoht);}return 반환값;
    }VIGA=12;return 0;
}
void *malloc(size_t kaup_COUNT){return realloc(0,kaup_COUNT);}
void *calloc(size_t kaup_COUNT,size_t string_andmed){if(string_andmed&&kaup_COUNT>SIZE_MAX/string_andmed)return 0;void*andmed_ametikoht=malloc(kaup_COUNT*string_andmed);if(andmed_ametikoht)memset(andmed_ametikoht,0,kaup_COUNT*string_andmed);return andmed_ametikoht;}
unsigned long long strtoull(const char*string_andmed,char**lõpeta_kõne_nihe,int taust_VALUE){
    const char*START_nihe=string_andmed;while(*string_andmed==' '||(*string_andmed>=9&&*string_andmed<=13))string_andmed++;int 음수여부=0;if(*string_andmed=='-'||*string_andmed=='+')음수여부=*string_andmed++=='-';
    if((!taust_VALUE||taust_VALUE==16)&&string_andmed[0]=='0'&&(string_andmed[1]=='x'||string_andmed[1]=='X')){taust_VALUE=16;string_andmed+=2;}if(!taust_VALUE)taust_VALUE=*string_andmed=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned koodipunkt=*string_andmed,sihtkoht_andmed=koodipunkt>='0'&&koodipunkt<='9'?koodipunkt-'0':koodipunkt>='a'&&koodipunkt<='z'?koodipunkt-'a'+10:koodipunkt>='A'&&koodipunkt<='Z'?koodipunkt-'A'+10:99;if(sihtkoht_andmed>=(unsigned)taust_VALUE)break;하나라도=1;string_andmed++;if(임시값>(~0ull-sihtkoht_andmed)/(unsigned)taust_VALUE){임시값=~0ull;VIGA=34;}else 임시값=임시값*taust_VALUE+sihtkoht_andmed;}
    if(lõpeta_kõne_nihe)*lõpeta_kõne_nihe=(char*)(하나라도?string_andmed:START_nihe);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*string_andmed,char**보조항목,int SECOND_VALUE){return strtoull(string_andmed,보조항목,SECOND_VALUE);}
long strtol(const char*string_andmed,char**보조항목,int SECOND_VALUE){return (long)strtoull(string_andmed,보조항목,SECOND_VALUE);}
int atoi(const char*string_andmed){return (int)strtol(string_andmed,0,10);}
long double ldexpl(long double 가로좌표,int kaup_COUNT){while(kaup_COUNT>0){가로좌표*=2;kaup_COUNT--;}while(kaup_COUNT<0){가로좌표/=2;kaup_COUNT++;}return 가로좌표;}
long double strtold(const char*string_andmed,char**lõpeta_kõne_nihe){
    const char*START_nihe=string_andmed;while(*string_andmed==' '||(*string_andmed>=9&&*string_andmed<=13))string_andmed++;int 음수여부=0;if(*string_andmed=='-'||*string_andmed=='+')음수여부=*string_andmed++=='-';
    int taust_VALUE=10;if(string_andmed[0]=='0'&&(string_andmed[1]=='x'||string_andmed[1]=='X')){taust_VALUE=16;string_andmed+=2;}long double 임시값=0,skaleerima=1;int 소수부=0,하나라도=0;
    for(;;){int koodipunkt=*string_andmed,sihtkoht_andmed=koodipunkt>='0'&&koodipunkt<='9'?koodipunkt-'0':koodipunkt>='a'&&koodipunkt<='f'?koodipunkt-'a'+10:koodipunkt>='A'&&koodipunkt<='F'?koodipunkt-'A'+10:99;
        if(koodipunkt=='.'&&!소수부){소수부=1;string_andmed++;continue;}if(sihtkoht_andmed>=taust_VALUE)break;하나라도=1;string_andmed++;임시값=임시값*taust_VALUE+sihtkoht_andmed;if(소수부)skaleerima*=taust_VALUE;
    }임시값/=skaleerima;
    if((taust_VALUE==10&&(*string_andmed=='e'||*string_andmed=='E'))||(taust_VALUE==16&&(*string_andmed=='p'||*string_andmed=='P'))){const char*saade_VALUE=string_andmed++;int 빼기=0;if(*string_andmed=='-'||*string_andmed=='+')빼기=*string_andmed++=='-';int kaup_COUNT=0,kirje_COUNT=0;while(*string_andmed>='0'&&*string_andmed<='9'){kirje_COUNT++;if(kaup_COUNT<20000)kaup_COUNT=kaup_COUNT*10+*string_andmed-'0';string_andmed++;}if(!kirje_COUNT)string_andmed=saade_VALUE;else{long double tegur=taust_VALUE==16?2:10;while(kaup_COUNT-->0&&kaup_COUNT<200000)임시값=빼기?임시값/tegur:임시값*tegur;}}
    if(lõpeta_kõne_nihe)*lõpeta_kõne_nihe=(char*)(하나라도?string_andmed:START_nihe);return 음수여부?-임시값:임시값;
}
double strtod(const char*string_andmed,char**보조항목){return (double)strtold(string_andmed,보조항목);}float strtof(const char*string_andmed,char**보조항목){return (float)strtold(string_andmed,보조항목);}
void qsort(void*taust_VALUE,size_t kaup_COUNT,size_t Suurus,int(*Võrdlus)(const void*,const void*)){
    unsigned char*andmed_ametikoht=taust_VALUE;for(size_t 순번=1;순번<kaup_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Võrdlus(andmed_ametikoht+(안쪽순번-1)*Suurus,andmed_ametikoht+안쪽순번*Suurus)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Suurus;셋째순번++){unsigned char koodipunkt=andmed_ametikoht[(안쪽순번-1)*Suurus+셋째순번];andmed_ametikoht[(안쪽순번-1)*Suurus+셋째순번]=andmed_ametikoht[안쪽순번*Suurus+셋째순번];andmed_ametikoht[안쪽순번*Suurus+셋째순번]=koodipunkt;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Asukoht;} 열림[24];
static unsigned char toodang[32768];static size_t toodang_suurust_muutma,toodang_ametikoht;static int toodang_avama;
const unsigned char *_15_toodang(size_t *kaup_COUNT){*kaup_COUNT=toodang_suurust_muutma;return toodang;}
int open(const char*Nimi_2,int konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus,...){
    if(!strcmp(Nimi_2,"/@cc-output")){if(toodang_avama){VIGA=16;return -1;}toodang_avama=1;toodang_suurust_muutma=toodang_ametikoht=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(kompilaator_Ressursid)/sizeof(kompilaator_Ressursid[0]);순번++)if(!strcmp(Nimi_2,kompilaator_Ressursid[순번].Nimi_2)){
        if(konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&3){VIGA=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Asukoht=0;return 128+안쪽순번;}VIGA=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nimi_2,konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus,0,0,0,0);if(반환값<0){VIGA=-반환값;return -1;}return 반환값;
}
int close(int Fail_pide){if(Fail_pide==100){toodang_avama=0;return 0;}if(Fail_pide>=128&&Fail_pide<152){열림[Fail_pide-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Fail_pide,0,0,0,0,0);if(반환값<0){VIGA=-반환값;return -1;}return 0;}
long read(int Fail_pide,void*andmed,size_t kaup_COUNT){
    if(Fail_pide>=128&&Fail_pide<152&&열림[Fail_pide-128].사용량){int 순번=Fail_pide-128;const kompilaator_ressurss*반환값=&kompilaator_Ressursid[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Suurus-열림[순번].Asukoht;if(kaup_COUNT>왼쪽)kaup_COUNT=왼쪽;memcpy(andmed,반환값->andmed+열림[순번].Asukoht,kaup_COUNT);열림[순번].Asukoht+=kaup_COUNT;return kaup_COUNT;}
    intptr_t 반환값=사용자호출(2,Fail_pide,(uintptr_t)andmed,kaup_COUNT,0,0,0);if(반환값<0){VIGA=-반환값;return -1;}return 반환값;
}
long write(int Fail_pide,const void*andmed,size_t kaup_COUNT){
    if(Fail_pide==100){if(kaup_COUNT>sizeof(toodang)-toodang_ametikoht){VIGA=28;return -1;}memcpy(toodang+toodang_ametikoht,andmed,kaup_COUNT);toodang_ametikoht+=kaup_COUNT;if(toodang_suurust_muutma<toodang_ametikoht)toodang_suurust_muutma=toodang_ametikoht;return kaup_COUNT;}
    intptr_t 반환값=사용자호출(1,Fail_pide,(uintptr_t)andmed,kaup_COUNT,0,0,0);if(반환값<0){VIGA=-반환값;return -1;}return 반환값;
}
long lseek(int Fail_pide,long nihe_VALUE,int 기준점){
    if(Fail_pide==100){long andmed_ametikoht=nihe_VALUE+(기준점==0?0:기준점==1?toodang_ametikoht:toodang_suurust_muutma);if(andmed_ametikoht<0||(size_t)andmed_ametikoht>sizeof(toodang)){VIGA=22;return -1;}toodang_ametikoht=andmed_ametikoht;return andmed_ametikoht;}
    if(Fail_pide>=128&&Fail_pide<152&&열림[Fail_pide-128].사용량){int 순번=Fail_pide-128;long andmed_ametikoht=nihe_VALUE+(기준점==0?0:기준점==1?열림[순번].Asukoht:kompilaator_Ressursid[열림[순번].LOOKUP_INDEX].Suurus);if(andmed_ametikoht<0||(size_t)andmed_ametikoht>kompilaator_Ressursid[열림[순번].LOOKUP_INDEX].Suurus){VIGA=22;return -1;}열림[순번].Asukoht=andmed_ametikoht;return andmed_ametikoht;}
    intptr_t 반환값=사용자호출(5,Fail_pide,nihe_VALUE,기준점,0,0,0);if(반환값<0){VIGA=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nimi_2){intptr_t 반환값=사용자호출(11,(uintptr_t)Nimi_2,0,0,0,0,0);if(반환값<0){VIGA=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nimi_2,char*näitaja_andmed){if(!näitaja_andmed){näitaja_andmed=malloc(strlen(Nimi_2)+1);if(!näitaja_andmed)return 0;}return strcpy(näitaja_andmed,Nimi_2);}
char *getcwd(char*andmed_ametikoht,size_t kaup_COUNT){if(kaup_COUNT<2){VIGA=34;return 0;}andmed_ametikoht[0]='/';andmed_ametikoht[1]=0;return andmed_ametikoht;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*terminal_kirje){time_t 임시값=0;if(terminal_kirje)*terminal_kirje=임시값;return 임시값;}
struct tm *localtime(const time_t*terminal_kirje){(void)terminal_kirje;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Vood[18]={{1,0,1},{2,0,1}};FILE*stdout=&Vood[0],*stderr=&Vood[1];
FILE*fdopen(int Fail_pide,const char*meetod_MODE){(void)meetod_MODE;for(unsigned 순번=2;순번<18;순번++)if(!Vood[순번].사용량){Vood[순번].사용량=1;Vood[순번].VIGA=0;Vood[순번].Fail_pide=Fail_pide;return &Vood[순번];}VIGA=24;return 0;}
int fflush(FILE*Fail_kirje){return Fail_kirje&&Fail_kirje->VIGA?-1:0;}
int fclose(FILE*Fail_kirje){int 반환값=close(Fail_kirje->Fail_pide);if(Fail_kirje->VIGA)반환값=-1;Fail_kirje->사용량=0;return 반환값;}
size_t fwrite(const void*andmed_ametikoht,size_t string_andmed,size_t kaup_COUNT,FILE*Fail_kirje){if(!string_andmed)return 0;if(kaup_COUNT>SIZE_MAX/string_andmed){Fail_kirje->VIGA=1;return 0;}long 반환값=write(Fail_kirje->Fail_pide,andmed_ametikoht,string_andmed*kaup_COUNT);if(반환값<0){Fail_kirje->VIGA=1;return 0;}return (size_t)반환값/string_andmed;}
int fputc(int koodipunkt,FILE*Fail_kirje){unsigned char SECOND_VALUE=koodipunkt;return fwrite(&SECOND_VALUE,1,1,Fail_kirje)==1?SECOND_VALUE:EOF;}
int fputs(const char*string_andmed,FILE*Fail_kirje){return fwrite(string_andmed,1,strlen(string_andmed),Fail_kirje)==strlen(string_andmed)?0:EOF;}
static void 넣기(char*näitaja_andmed,size_t 용량한도,size_t*tähtaja_piires_ametikoht,char koodipunkt){if(*tähtaja_piires_ametikoht+1<용량한도)näitaja_andmed[*tähtaja_piires_ametikoht]=koodipunkt;(*tähtaja_piires_ametikoht)++;}
int vsnprintf(char*näitaja_andmed,size_t 용량한도,const char*vorming,va_list 가변인수){
    size_t tähtaja_piires_ametikoht=0;while(*vorming){if(*vorming!='%'){넣기(näitaja_andmed,용량한도,&tähtaja_piires_ametikoht,*vorming++);continue;}vorming++;
        int 왼쪽=0,null_VALUE=0,대체값=0;while(*vorming=='-'||*vorming=='0'||*vorming=='#'||*vorming=='+'||*vorming==' '){if(*vorming=='-')왼쪽=1;if(*vorming=='0')null_VALUE=1;if(*vorming=='#')대체값=1;vorming++;}
        int 너비=0,tabavusmäär_VALUE=-1;if(*vorming=='*'){너비=va_arg(가변인수,int);vorming++;}else while(*vorming>='0'&&*vorming<='9')너비=너비*10+*vorming++-'0';
        if(*vorming=='.'){vorming++;tabavusmäär_VALUE=0;if(*vorming=='*'){tabavusmäär_VALUE=va_arg(가변인수,int);vorming++;}else while(*vorming>='0'&&*vorming<='9')tabavusmäär_VALUE=tabavusmäär_VALUE*10+*vorming++-'0';}
        int lai_tähemärk=0;while(*vorming=='l'||*vorming=='z'||*vorming=='t'||*vorming=='j'||*vorming=='h'){if(*vorming!='h')lai_tähemärk=1;vorming++;}
        char TYPE_ala=*vorming?*vorming++:0,puhvri_salvestusruum[80];const char*string_andmed=puhvri_salvestusruum;size_t kaup_COUNT=0;
        if(TYPE_ala=='s'){string_andmed=va_arg(가변인수,const char*);if(!string_andmed)string_andmed="(null)";kaup_COUNT=strlen(string_andmed);if(tabavusmäär_VALUE>=0&&kaup_COUNT>(size_t)tabavusmäär_VALUE)kaup_COUNT=tabavusmäär_VALUE;}
        else if(TYPE_ala=='c'){puhvri_salvestusruum[0]=va_arg(가변인수,int);kaup_COUNT=1;}
        else if(TYPE_ala=='%'){puhvri_salvestusruum[0]='%';kaup_COUNT=1;}
        else if(TYPE_ala=='d'||TYPE_ala=='i'||TYPE_ala=='u'||TYPE_ala=='x'||TYPE_ala=='X'||TYPE_ala=='o'||TYPE_ala=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_ala=='d'||TYPE_ala=='i'){long long 임시값=lai_tähemärk?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_ala=='p'?(uintptr_t)va_arg(가변인수,void*):lai_tähemärk?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned taust_VALUE=TYPE_ala=='x'||TYPE_ala=='X'||TYPE_ala=='p'?16:TYPE_ala=='o'?8:10;char number_COUNT[64];unsigned 사용량=0;
            do{number_COUNT[사용량++]="0123456789abcdef"[VALUE%taust_VALUE];VALUE/=taust_VALUE;}while(VALUE);
            if(음수표시)puhvri_salvestusruum[kaup_COUNT++]='-';if(TYPE_ala=='p'||(대체값&&taust_VALUE==16)){puhvri_salvestusruum[kaup_COUNT++]='0';puhvri_salvestusruum[kaup_COUNT++]='x';}
            for(int täide_VALUE=(int)사용량;tabavusmäär_VALUE>täide_VALUE&&kaup_COUNT<sizeof(puhvri_salvestusruum)-사용량;täide_VALUE++)puhvri_salvestusruum[kaup_COUNT++]='0';
            if(null_VALUE&&!왼쪽&&tabavusmäär_VALUE<0)while(너비>(int)(kaup_COUNT+사용량)&&kaup_COUNT<sizeof(puhvri_salvestusruum)-사용량)puhvri_salvestusruum[kaup_COUNT++]='0';
            while(사용량)puhvri_salvestusruum[kaup_COUNT++]=number_COUNT[--사용량];
        }else{puhvri_salvestusruum[0]='?';kaup_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)kaup_COUNT){넣기(näitaja_andmed,용량한도,&tähtaja_piires_ametikoht,' ');너비--;}
        for(size_t 순번=0;순번<kaup_COUNT;순번++)넣기(näitaja_andmed,용량한도,&tähtaja_piires_ametikoht,string_andmed[순번]);while(왼쪽&&너비>(int)kaup_COUNT){넣기(näitaja_andmed,용량한도,&tähtaja_piires_ametikoht,' ');너비--;}
    }if(용량한도)näitaja_andmed[tähtaja_piires_ametikoht<용량한도?tähtaja_piires_ametikoht:용량한도-1]=0;return tähtaja_piires_ametikoht;
}
int snprintf(char*näitaja_andmed,size_t 용량한도,const char*Fail_kirje,...){va_list 첫째값;va_start(첫째값,Fail_kirje);int 반환값=vsnprintf(näitaja_andmed,용량한도,Fail_kirje,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*näitaja_andmed,const char*Fail_kirje,...){va_list 첫째값;va_start(첫째값,Fail_kirje);int 반환값=vsnprintf(näitaja_andmed,SIZE_MAX,Fail_kirje,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*voog_VALUE,const char*Fail_kirje,va_list 첫째값){char SECOND_VALUE[2048];int kaup_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),Fail_kirje,첫째값);if(kaup_COUNT>2047)kaup_COUNT=2047;return fwrite(SECOND_VALUE,1,kaup_COUNT,voog_VALUE)==(size_t)kaup_COUNT?kaup_COUNT:-1;}
int fprintf(FILE*voog_VALUE,const char*Fail_kirje,...){va_list 첫째값;va_start(첫째값,Fail_kirje);int 반환값=vfprintf(voog_VALUE,Fail_kirje,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Fail_kirje,...){va_list 첫째값;va_start(첫째값,Fail_kirje);int 반환값=vfprintf(stdout,Fail_kirje,첫째값);va_end(첫째값);return 반환값;}
