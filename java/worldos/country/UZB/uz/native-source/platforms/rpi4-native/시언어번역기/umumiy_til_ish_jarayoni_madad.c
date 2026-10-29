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
static int Xato;
int *__errno_location(void){return &Xato;}
void exit(int holat_VALUE_e10195a1){사용자호출(6,holat_VALUE_e10195a1,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *chek_ifoda,const char *Fayl,unsigned satr,const char *uslub_kiritish_nom){fprintf(stderr,"cc assertion: %s %s:%u %s\n",chek_ifoda,Fayl,satr,uslub_kiritish_nom);exit(1);}
size_t strlen(const char*satr_ma_lumotlar){const char*ma_lumotlar_holat=satr_ma_lumotlar;while(*ma_lumotlar_holat)ma_lumotlar_holat++;return ma_lumotlar_holat-satr_ma_lumotlar;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t element_COUNT){while(element_COUNT--){unsigned char x_koordinata=*첫째값++,Y_tugmasi_koordinat=*SECOND_VALUE++;if(x_koordinata!=Y_tugmasi_koordinat)return x_koordinata-Y_tugmasi_koordinat;if(!x_koordinata)return 0;}return 0;}
char *strcpy(char*ko_chirish_joyi_ma_lumotlar,const char*satr_ma_lumotlar){char*반환값=ko_chirish_joyi_ma_lumotlar;while((*ko_chirish_joyi_ma_lumotlar++=*satr_ma_lumotlar++)){}return 반환값;}
char *strchr(const char*satr_ma_lumotlar,int belgi_kodi){do{if(*satr_ma_lumotlar==(char)belgi_kodi)return (char*)satr_ma_lumotlar;}while(*satr_ma_lumotlar++);return 0;}
char *strrchr(const char*satr_ma_lumotlar,int belgi_kodi){const char*반환값=0;do{if(*satr_ma_lumotlar==(char)belgi_kodi)반환값=satr_ma_lumotlar;}while(*satr_ma_lumotlar++);return (char*)반환값;}
char *strstr(const char*satr_ma_lumotlar,const char*Terminal_kiritish){size_t element_COUNT=strlen(Terminal_kiritish);for(;*satr_ma_lumotlar;satr_ma_lumotlar++)if(!strncmp(satr_ma_lumotlar,Terminal_kiritish,element_COUNT))return (char*)satr_ma_lumotlar;return element_COUNT?0:(char*)satr_ma_lumotlar;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t element_COUNT){const unsigned char*x_koordinata=첫째값,*Y_tugmasi_koordinat=SECOND_VALUE;while(element_COUNT--){if(*x_koordinata!=*Y_tugmasi_koordinat)return *x_koordinata-*Y_tugmasi_koordinat;x_koordinata++;Y_tugmasi_koordinat++;}return 0;}
void *memmove(void*ko_chirish_joyi_ma_lumotlar,const void*satr_ma_lumotlar,size_t element_COUNT){unsigned char*x_koordinata=ko_chirish_joyi_ma_lumotlar;const unsigned char*Y_tugmasi_koordinat=satr_ma_lumotlar;if(x_koordinata<Y_tugmasi_koordinat){for(size_t 순번=0;순번<element_COUNT;순번++)x_koordinata[순번]=Y_tugmasi_koordinat[순번];}else while(element_COUNT){element_COUNT--;x_koordinata[element_COUNT]=Y_tugmasi_koordinat[element_COUNT];}return ko_chirish_joyi_ma_lumotlar;}
static unsigned char joylashuv_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct ma_lumotlar_bloklash {size_t Hajmi;struct ma_lumotlar_bloklash*Keyingi_element;int 남은공간;int 채울크기;uint64_t tenglashtirish_dars;} ma_lumotlar_bloklash;
static ma_lumotlar_bloklash *첫항목;
void free(void*ma_lumotlar_holat){if(!ma_lumotlar_holat)return;ma_lumotlar_bloklash*SECOND_VALUE=(ma_lumotlar_bloklash*)ma_lumotlar_holat-1;SECOND_VALUE->남은공간=1;for(ma_lumotlar_bloklash*Keyingi_OFFSET=첫항목;Keyingi_OFFSET&&Keyingi_OFFSET->Keyingi_element;){if(Keyingi_OFFSET->남은공간&&Keyingi_OFFSET->Keyingi_element->남은공간){Keyingi_OFFSET->Hajmi+=sizeof(ma_lumotlar_bloklash)+Keyingi_OFFSET->Keyingi_element->Hajmi;Keyingi_OFFSET->Keyingi_element=Keyingi_OFFSET->Keyingi_element->Keyingi_element;}else Keyingi_OFFSET=Keyingi_OFFSET->Keyingi_element;}}
void *realloc(void*ma_lumotlar_holat,size_t element_COUNT){
    if(!element_COUNT){free(ma_lumotlar_holat);return 0;}if(element_COUNT>sizeof(joylashuv_Arena)-sizeof(ma_lumotlar_bloklash))return 0;element_COUNT=(element_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(ma_lumotlar_bloklash*)joylashuv_Arena;첫항목->Hajmi=sizeof(joylashuv_Arena)-sizeof(ma_lumotlar_bloklash);첫항목->남은공간=1;첫항목->Keyingi_element=0;}
    ma_lumotlar_bloklash*이전=ma_lumotlar_holat?(ma_lumotlar_bloklash*)ma_lumotlar_holat-1:0;if(이전&&이전->Hajmi>=element_COUNT)return ma_lumotlar_holat;
    for(ma_lumotlar_bloklash*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Keyingi_element)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Hajmi>=element_COUNT){
        if(SECOND_VALUE->Hajmi>=element_COUNT+sizeof(ma_lumotlar_bloklash)+16){ma_lumotlar_bloklash*나머지부분=(ma_lumotlar_bloklash*)((unsigned char*)(SECOND_VALUE+1)+element_COUNT);나머지부분->Hajmi=SECOND_VALUE->Hajmi-element_COUNT-sizeof(ma_lumotlar_bloklash);나머지부분->Keyingi_element=SECOND_VALUE->Keyingi_element;나머지부분->남은공간=1;SECOND_VALUE->Keyingi_element=나머지부분;SECOND_VALUE->Hajmi=element_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,ma_lumotlar_holat,이전->Hajmi);free(ma_lumotlar_holat);}return 반환값;
    }Xato=12;return 0;
}
void *malloc(size_t element_COUNT){return realloc(0,element_COUNT);}
void *calloc(size_t element_COUNT,size_t satr_ma_lumotlar){if(satr_ma_lumotlar&&element_COUNT>SIZE_MAX/satr_ma_lumotlar)return 0;void*ma_lumotlar_holat=malloc(element_COUNT*satr_ma_lumotlar);if(ma_lumotlar_holat)memset(ma_lumotlar_holat,0,element_COUNT*satr_ma_lumotlar);return ma_lumotlar_holat;}
unsigned long long strtoull(const char*satr_ma_lumotlar,char**to_xtatmoq_OFFSET,int Fon_VALUE){
    const char*Start_OFFSET=satr_ma_lumotlar;while(*satr_ma_lumotlar==' '||(*satr_ma_lumotlar>=9&&*satr_ma_lumotlar<=13))satr_ma_lumotlar++;int 음수여부=0;if(*satr_ma_lumotlar=='-'||*satr_ma_lumotlar=='+')음수여부=*satr_ma_lumotlar++=='-';
    if((!Fon_VALUE||Fon_VALUE==16)&&satr_ma_lumotlar[0]=='0'&&(satr_ma_lumotlar[1]=='x'||satr_ma_lumotlar[1]=='X')){Fon_VALUE=16;satr_ma_lumotlar+=2;}if(!Fon_VALUE)Fon_VALUE=*satr_ma_lumotlar=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned belgi_kodi=*satr_ma_lumotlar,ko_chirish_joyi_ma_lumotlar=belgi_kodi>='0'&&belgi_kodi<='9'?belgi_kodi-'0':belgi_kodi>='a'&&belgi_kodi<='z'?belgi_kodi-'a'+10:belgi_kodi>='A'&&belgi_kodi<='Z'?belgi_kodi-'A'+10:99;if(ko_chirish_joyi_ma_lumotlar>=(unsigned)Fon_VALUE)break;하나라도=1;satr_ma_lumotlar++;if(임시값>(~0ull-ko_chirish_joyi_ma_lumotlar)/(unsigned)Fon_VALUE){임시값=~0ull;Xato=34;}else 임시값=임시값*Fon_VALUE+ko_chirish_joyi_ma_lumotlar;}
    if(to_xtatmoq_OFFSET)*to_xtatmoq_OFFSET=(char*)(하나라도?satr_ma_lumotlar:Start_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*satr_ma_lumotlar,char**보조항목,int SECOND_VALUE){return strtoull(satr_ma_lumotlar,보조항목,SECOND_VALUE);}
long strtol(const char*satr_ma_lumotlar,char**보조항목,int SECOND_VALUE){return (long)strtoull(satr_ma_lumotlar,보조항목,SECOND_VALUE);}
int atoi(const char*satr_ma_lumotlar){return (int)strtol(satr_ma_lumotlar,0,10);}
long double ldexpl(long double x_koordinata,int element_COUNT){while(element_COUNT>0){x_koordinata*=2;element_COUNT--;}while(element_COUNT<0){x_koordinata/=2;element_COUNT++;}return x_koordinata;}
long double strtold(const char*satr_ma_lumotlar,char**to_xtatmoq_OFFSET){
    const char*Start_OFFSET=satr_ma_lumotlar;while(*satr_ma_lumotlar==' '||(*satr_ma_lumotlar>=9&&*satr_ma_lumotlar<=13))satr_ma_lumotlar++;int 음수여부=0;if(*satr_ma_lumotlar=='-'||*satr_ma_lumotlar=='+')음수여부=*satr_ma_lumotlar++=='-';
    int Fon_VALUE=10;if(satr_ma_lumotlar[0]=='0'&&(satr_ma_lumotlar[1]=='x'||satr_ma_lumotlar[1]=='X')){Fon_VALUE=16;satr_ma_lumotlar+=2;}long double 임시값=0,masshtabni_o_zgartirmoq=1;int 소수부=0,하나라도=0;
    for(;;){int belgi_kodi=*satr_ma_lumotlar,ko_chirish_joyi_ma_lumotlar=belgi_kodi>='0'&&belgi_kodi<='9'?belgi_kodi-'0':belgi_kodi>='a'&&belgi_kodi<='f'?belgi_kodi-'a'+10:belgi_kodi>='A'&&belgi_kodi<='F'?belgi_kodi-'A'+10:99;
        if(belgi_kodi=='.'&&!소수부){소수부=1;satr_ma_lumotlar++;continue;}if(ko_chirish_joyi_ma_lumotlar>=Fon_VALUE)break;하나라도=1;satr_ma_lumotlar++;임시값=임시값*Fon_VALUE+ko_chirish_joyi_ma_lumotlar;if(소수부)masshtabni_o_zgartirmoq*=Fon_VALUE;
    }임시값/=masshtabni_o_zgartirmoq;
    if((Fon_VALUE==10&&(*satr_ma_lumotlar=='e'||*satr_ma_lumotlar=='E'))||(Fon_VALUE==16&&(*satr_ma_lumotlar=='p'||*satr_ma_lumotlar=='P'))){const char*ko_rsatmoq_VALUE=satr_ma_lumotlar++;int 빼기=0;if(*satr_ma_lumotlar=='-'||*satr_ma_lumotlar=='+')빼기=*satr_ma_lumotlar++=='-';int element_COUNT=0,kiritish_COUNT=0;while(*satr_ma_lumotlar>='0'&&*satr_ma_lumotlar<='9'){kiritish_COUNT++;if(element_COUNT<20000)element_COUNT=element_COUNT*10+*satr_ma_lumotlar-'0';satr_ma_lumotlar++;}if(!kiritish_COUNT)satr_ma_lumotlar=ko_rsatmoq_VALUE;else{long double koʻpaytuvchi=Fon_VALUE==16?2:10;while(element_COUNT-->0&&element_COUNT<200000)임시값=빼기?임시값/koʻpaytuvchi:임시값*koʻpaytuvchi;}}
    if(to_xtatmoq_OFFSET)*to_xtatmoq_OFFSET=(char*)(하나라도?satr_ma_lumotlar:Start_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*satr_ma_lumotlar,char**보조항목){return (double)strtold(satr_ma_lumotlar,보조항목);}float strtof(const char*satr_ma_lumotlar,char**보조항목){return (float)strtold(satr_ma_lumotlar,보조항목);}
void qsort(void*Fon_VALUE,size_t element_COUNT,size_t Hajmi,int(*taqqoslamoq)(const void*,const void*)){
    unsigned char*ma_lumotlar_holat=Fon_VALUE;for(size_t 순번=1;순번<element_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&taqqoslamoq(ma_lumotlar_holat+(안쪽순번-1)*Hajmi,ma_lumotlar_holat+안쪽순번*Hajmi)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Hajmi;셋째순번++){unsigned char belgi_kodi=ma_lumotlar_holat[(안쪽순번-1)*Hajmi+셋째순번];ma_lumotlar_holat[(안쪽순번-1)*Hajmi+셋째순번]=ma_lumotlar_holat[안쪽순번*Hajmi+셋째순번];ma_lumotlar_holat[안쪽순번*Hajmi+셋째순번]=belgi_kodi;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Holati;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *element_COUNT){*element_COUNT=출력크기;return 출력결과;}
int open(const char*Nomi,int tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati,...){
    if(!strcmp(Nomi,"/@cc-output")){if(출력열림){Xato=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Nomi,번역기자원들[순번].Nomi)){
        if(tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&3){Xato=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Holati=0;return 128+안쪽순번;}Xato=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nomi,tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati,0,0,0,0);if(반환값<0){Xato=-반환값;return -1;}return 반환값;
}
int close(int fayl_deskriptor){if(fayl_deskriptor==100){출력열림=0;return 0;}if(fayl_deskriptor>=128&&fayl_deskriptor<152){열림[fayl_deskriptor-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,fayl_deskriptor,0,0,0,0,0);if(반환값<0){Xato=-반환값;return -1;}return 0;}
long read(int fayl_deskriptor,void*ma_lumotlar,size_t element_COUNT){
    if(fayl_deskriptor>=128&&fayl_deskriptor<152&&열림[fayl_deskriptor-128].사용량){int 순번=fayl_deskriptor-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Hajmi-열림[순번].Holati;if(element_COUNT>왼쪽)element_COUNT=왼쪽;memcpy(ma_lumotlar,반환값->ma_lumotlar+열림[순번].Holati,element_COUNT);열림[순번].Holati+=element_COUNT;return element_COUNT;}
    intptr_t 반환값=사용자호출(2,fayl_deskriptor,(uintptr_t)ma_lumotlar,element_COUNT,0,0,0);if(반환값<0){Xato=-반환값;return -1;}return 반환값;
}
long write(int fayl_deskriptor,const void*ma_lumotlar,size_t element_COUNT){
    if(fayl_deskriptor==100){if(element_COUNT>sizeof(출력결과)-출력위치){Xato=28;return -1;}memcpy(출력결과+출력위치,ma_lumotlar,element_COUNT);출력위치+=element_COUNT;if(출력크기<출력위치)출력크기=출력위치;return element_COUNT;}
    intptr_t 반환값=사용자호출(1,fayl_deskriptor,(uintptr_t)ma_lumotlar,element_COUNT,0,0,0);if(반환값<0){Xato=-반환값;return -1;}return 반환값;
}
long lseek(int fayl_deskriptor,long OFFSET_VALUE,int 기준점){
    if(fayl_deskriptor==100){long ma_lumotlar_holat=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(ma_lumotlar_holat<0||(size_t)ma_lumotlar_holat>sizeof(출력결과)){Xato=22;return -1;}출력위치=ma_lumotlar_holat;return ma_lumotlar_holat;}
    if(fayl_deskriptor>=128&&fayl_deskriptor<152&&열림[fayl_deskriptor-128].사용량){int 순번=fayl_deskriptor-128;long ma_lumotlar_holat=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].Holati:번역기자원들[열림[순번].LOOKUP_INDEX].Hajmi);if(ma_lumotlar_holat<0||(size_t)ma_lumotlar_holat>번역기자원들[열림[순번].LOOKUP_INDEX].Hajmi){Xato=22;return -1;}열림[순번].Holati=ma_lumotlar_holat;return ma_lumotlar_holat;}
    intptr_t 반환값=사용자호출(5,fayl_deskriptor,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){Xato=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nomi){intptr_t 반환값=사용자호출(11,(uintptr_t)Nomi,0,0,0,0,0);if(반환값<0){Xato=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nomi,char*o_lchov_ma_lumotlar){if(!o_lchov_ma_lumotlar){o_lchov_ma_lumotlar=malloc(strlen(Nomi)+1);if(!o_lchov_ma_lumotlar)return 0;}return strcpy(o_lchov_ma_lumotlar,Nomi);}
char *getcwd(char*ma_lumotlar_holat,size_t element_COUNT){if(element_COUNT<2){Xato=34;return 0;}ma_lumotlar_holat[0]='/';ma_lumotlar_holat[1]=0;return ma_lumotlar_holat;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_kiritish){time_t 임시값=0;if(Terminal_kiritish)*Terminal_kiritish=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_kiritish){(void)Terminal_kiritish;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int fayl_deskriptor,const char*uslub_MODE){(void)uslub_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Xato=0;흐름목록[순번].fayl_deskriptor=fayl_deskriptor;return &흐름목록[순번];}Xato=24;return 0;}
int fflush(FILE*fayl_kiritish){return fayl_kiritish&&fayl_kiritish->Xato?-1:0;}
int fclose(FILE*fayl_kiritish){int 반환값=close(fayl_kiritish->fayl_deskriptor);if(fayl_kiritish->Xato)반환값=-1;fayl_kiritish->사용량=0;return 반환값;}
size_t fwrite(const void*ma_lumotlar_holat,size_t satr_ma_lumotlar,size_t element_COUNT,FILE*fayl_kiritish){if(!satr_ma_lumotlar)return 0;if(element_COUNT>SIZE_MAX/satr_ma_lumotlar){fayl_kiritish->Xato=1;return 0;}long 반환값=write(fayl_kiritish->fayl_deskriptor,ma_lumotlar_holat,satr_ma_lumotlar*element_COUNT);if(반환값<0){fayl_kiritish->Xato=1;return 0;}return (size_t)반환값/satr_ma_lumotlar;}
int fputc(int belgi_kodi,FILE*fayl_kiritish){unsigned char SECOND_VALUE=belgi_kodi;return fwrite(&SECOND_VALUE,1,1,fayl_kiritish)==1?SECOND_VALUE:EOF;}
int fputs(const char*satr_ma_lumotlar,FILE*fayl_kiritish){return fwrite(satr_ma_lumotlar,1,strlen(satr_ma_lumotlar),fayl_kiritish)==strlen(satr_ma_lumotlar)?0:EOF;}
static void 넣기(char*o_lchov_ma_lumotlar,size_t 용량한도,size_t*현재위치,char belgi_kodi){if(*현재위치+1<용량한도)o_lchov_ma_lumotlar[*현재위치]=belgi_kodi;(*현재위치)++;}
int vsnprintf(char*o_lchov_ma_lumotlar,size_t 용량한도,const char*format,va_list 가변인수){
    size_t 현재위치=0;while(*format){if(*format!='%'){넣기(o_lchov_ma_lumotlar,용량한도,&현재위치,*format++);continue;}format++;
        int 왼쪽=0,영값=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')영값=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,정밀도=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;정밀도=0;if(*format=='*'){정밀도=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')정밀도=정밀도*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char TYPE_toifa=*format?*format++:0,bufer_Xotira[80];const char*satr_ma_lumotlar=bufer_Xotira;size_t element_COUNT=0;
        if(TYPE_toifa=='s'){satr_ma_lumotlar=va_arg(가변인수,const char*);if(!satr_ma_lumotlar)satr_ma_lumotlar="(null)";element_COUNT=strlen(satr_ma_lumotlar);if(정밀도>=0&&element_COUNT>(size_t)정밀도)element_COUNT=정밀도;}
        else if(TYPE_toifa=='c'){bufer_Xotira[0]=va_arg(가변인수,int);element_COUNT=1;}
        else if(TYPE_toifa=='%'){bufer_Xotira[0]='%';element_COUNT=1;}
        else if(TYPE_toifa=='d'||TYPE_toifa=='i'||TYPE_toifa=='u'||TYPE_toifa=='x'||TYPE_toifa=='X'||TYPE_toifa=='o'||TYPE_toifa=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_toifa=='d'||TYPE_toifa=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_toifa=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Fon_VALUE=TYPE_toifa=='x'||TYPE_toifa=='X'||TYPE_toifa=='p'?16:TYPE_toifa=='o'?8:10;char raqam_COUNT[64];unsigned 사용량=0;
            do{raqam_COUNT[사용량++]="0123456789abcdef"[VALUE%Fon_VALUE];VALUE/=Fon_VALUE;}while(VALUE);
            if(음수표시)bufer_Xotira[element_COUNT++]='-';if(TYPE_toifa=='p'||(대체값&&Fon_VALUE==16)){bufer_Xotira[element_COUNT++]='0';bufer_Xotira[element_COUNT++]='x';}
            for(int to_ldirish_VALUE=(int)사용량;정밀도>to_ldirish_VALUE&&element_COUNT<sizeof(bufer_Xotira)-사용량;to_ldirish_VALUE++)bufer_Xotira[element_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(element_COUNT+사용량)&&element_COUNT<sizeof(bufer_Xotira)-사용량)bufer_Xotira[element_COUNT++]='0';
            while(사용량)bufer_Xotira[element_COUNT++]=raqam_COUNT[--사용량];
        }else{bufer_Xotira[0]='?';element_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)element_COUNT){넣기(o_lchov_ma_lumotlar,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<element_COUNT;순번++)넣기(o_lchov_ma_lumotlar,용량한도,&현재위치,satr_ma_lumotlar[순번]);while(왼쪽&&너비>(int)element_COUNT){넣기(o_lchov_ma_lumotlar,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)o_lchov_ma_lumotlar[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*o_lchov_ma_lumotlar,size_t 용량한도,const char*fayl_kiritish,...){va_list 첫째값;va_start(첫째값,fayl_kiritish);int 반환값=vsnprintf(o_lchov_ma_lumotlar,용량한도,fayl_kiritish,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*o_lchov_ma_lumotlar,const char*fayl_kiritish,...){va_list 첫째값;va_start(첫째값,fayl_kiritish);int 반환값=vsnprintf(o_lchov_ma_lumotlar,SIZE_MAX,fayl_kiritish,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*oqim_VALUE,const char*fayl_kiritish,va_list 첫째값){char SECOND_VALUE[2048];int element_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),fayl_kiritish,첫째값);if(element_COUNT>2047)element_COUNT=2047;return fwrite(SECOND_VALUE,1,element_COUNT,oqim_VALUE)==(size_t)element_COUNT?element_COUNT:-1;}
int fprintf(FILE*oqim_VALUE,const char*fayl_kiritish,...){va_list 첫째값;va_start(첫째값,fayl_kiritish);int 반환값=vfprintf(oqim_VALUE,fayl_kiritish,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*fayl_kiritish,...){va_list 첫째값;va_start(첫째값,fayl_kiritish);int 반환값=vfprintf(stdout,fayl_kiritish,첫째값);va_end(첫째값);return 반환값;}
