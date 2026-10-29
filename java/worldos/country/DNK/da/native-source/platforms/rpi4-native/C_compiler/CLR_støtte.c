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
static int fejl;
int *__errno_location(void){return &fejl;}
void exit(int status_VÆRDI){사용자호출(6,status_VÆRDI,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *check_udtryk,const char *Fil,unsigned Linje,const char *metode_post_navn){fprintf(stderr,"cc assertion: %s %s:%u %s\n",check_udtryk,Fil,Linje,metode_post_navn);exit(1);}
size_t strlen(const char*streng_data){const char*data_placere=streng_data;while(*data_placere)data_placere++;return data_placere-streng_data;}
int strcmp(const char*첫째값,const char*SEKUND_VÆRDI){while(*첫째값&&*첫째값==*SEKUND_VÆRDI){첫째값++;SEKUND_VÆRDI++;}return (unsigned char)*첫째값-(unsigned char)*SEKUND_VÆRDI;}
int strncmp(const char*첫째값,const char*SEKUND_VÆRDI,size_t vare_TÆL){while(vare_TÆL--){unsigned char X_koordinat=*첫째값++,Y_koordinat=*SEKUND_VÆRDI++;if(X_koordinat!=Y_koordinat)return X_koordinat-Y_koordinat;if(!X_koordinat)return 0;}return 0;}
char *strcpy(char*destination_data,const char*streng_data){char*반환값=destination_data;while((*destination_data++=*streng_data++)){}return 반환값;}
char *strchr(const char*streng_data,int tegnkode){do{if(*streng_data==(char)tegnkode)return (char*)streng_data;}while(*streng_data++);return 0;}
char *strrchr(const char*streng_data,int tegnkode){const char*반환값=0;do{if(*streng_data==(char)tegnkode)반환값=streng_data;}while(*streng_data++);return (char*)반환값;}
char *strstr(const char*streng_data,const char*Terminal_post){size_t vare_TÆL=strlen(Terminal_post);for(;*streng_data;streng_data++)if(!strncmp(streng_data,Terminal_post,vare_TÆL))return (char*)streng_data;return vare_TÆL?0:(char*)streng_data;}
int memcmp(const void*첫째값,const void*SEKUND_VÆRDI,size_t vare_TÆL){const unsigned char*X_koordinat=첫째값,*Y_koordinat=SEKUND_VÆRDI;while(vare_TÆL--){if(*X_koordinat!=*Y_koordinat)return *X_koordinat-*Y_koordinat;X_koordinat++;Y_koordinat++;}return 0;}
void *memmove(void*destination_data,const void*streng_data,size_t vare_TÆL){unsigned char*X_koordinat=destination_data;const unsigned char*Y_koordinat=streng_data;if(X_koordinat<Y_koordinat){for(size_t 순번=0;순번<vare_TÆL;순번++)X_koordinat[순번]=Y_koordinat[순번];}else while(vare_TÆL){vare_TÆL--;X_koordinat[vare_TÆL]=Y_koordinat[vare_TÆL];}return destination_data;}
static unsigned char fordeling_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct datablok {size_t Størrelse;struct datablok*Næste_vare;int 남은공간;int udfyldning;uint64_t justering_enhed;} datablok;
static datablok *첫항목;
void free(void*data_placere){if(!data_placere)return;datablok*SEKUND_VÆRDI=(datablok*)data_placere-1;SEKUND_VÆRDI->남은공간=1;for(datablok*Næste_FORSKYDNING=첫항목;Næste_FORSKYDNING&&Næste_FORSKYDNING->Næste_vare;){if(Næste_FORSKYDNING->남은공간&&Næste_FORSKYDNING->Næste_vare->남은공간){Næste_FORSKYDNING->Størrelse+=sizeof(datablok)+Næste_FORSKYDNING->Næste_vare->Størrelse;Næste_FORSKYDNING->Næste_vare=Næste_FORSKYDNING->Næste_vare->Næste_vare;}else Næste_FORSKYDNING=Næste_FORSKYDNING->Næste_vare;}}
void *realloc(void*data_placere,size_t vare_TÆL){
    if(!vare_TÆL){free(data_placere);return 0;}if(vare_TÆL>sizeof(fordeling_Arena)-sizeof(datablok))return 0;vare_TÆL=(vare_TÆL+15)&~(size_t)15;
    if(!첫항목){첫항목=(datablok*)fordeling_Arena;첫항목->Størrelse=sizeof(fordeling_Arena)-sizeof(datablok);첫항목->남은공간=1;첫항목->Næste_vare=0;}
    datablok*Forrige_vare=data_placere?(datablok*)data_placere-1:0;if(Forrige_vare&&Forrige_vare->Størrelse>=vare_TÆL)return data_placere;
    for(datablok*SEKUND_VÆRDI=첫항목;SEKUND_VÆRDI;SEKUND_VÆRDI=SEKUND_VÆRDI->Næste_vare)if(SEKUND_VÆRDI->남은공간&&SEKUND_VÆRDI->Størrelse>=vare_TÆL){
        if(SEKUND_VÆRDI->Størrelse>=vare_TÆL+sizeof(datablok)+16){datablok*나머지부분=(datablok*)((unsigned char*)(SEKUND_VÆRDI+1)+vare_TÆL);나머지부분->Størrelse=SEKUND_VÆRDI->Størrelse-vare_TÆL-sizeof(datablok);나머지부분->Næste_vare=SEKUND_VÆRDI->Næste_vare;나머지부분->남은공간=1;SEKUND_VÆRDI->Næste_vare=나머지부분;SEKUND_VÆRDI->Størrelse=vare_TÆL;}
        SEKUND_VÆRDI->남은공간=0;void*반환값=SEKUND_VÆRDI+1;if(Forrige_vare){memcpy(반환값,data_placere,Forrige_vare->Størrelse);free(data_placere);}return 반환값;
    }fejl=12;return 0;
}
void *malloc(size_t vare_TÆL){return realloc(0,vare_TÆL);}
void *calloc(size_t vare_TÆL,size_t streng_data){if(streng_data&&vare_TÆL>SIZE_MAX/streng_data)return 0;void*data_placere=malloc(vare_TÆL*streng_data);if(data_placere)memset(data_placere,0,vare_TÆL*streng_data);return data_placere;}
unsigned long long strtoull(const char*streng_data,char**afslutte_et_opkald_FORSKYDNING,int Baggrund_VÆRDI){
    const char*START_FORSKYDNING=streng_data;while(*streng_data==' '||(*streng_data>=9&&*streng_data<=13))streng_data++;int 음수여부=0;if(*streng_data=='-'||*streng_data=='+')음수여부=*streng_data++=='-';
    if((!Baggrund_VÆRDI||Baggrund_VÆRDI==16)&&streng_data[0]=='0'&&(streng_data[1]=='x'||streng_data[1]=='X')){Baggrund_VÆRDI=16;streng_data+=2;}if(!Baggrund_VÆRDI)Baggrund_VÆRDI=*streng_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned tegnkode=*streng_data,destination_data=tegnkode>='0'&&tegnkode<='9'?tegnkode-'0':tegnkode>='a'&&tegnkode<='z'?tegnkode-'a'+10:tegnkode>='A'&&tegnkode<='Z'?tegnkode-'A'+10:99;if(destination_data>=(unsigned)Baggrund_VÆRDI)break;하나라도=1;streng_data++;if(임시값>(~0ull-destination_data)/(unsigned)Baggrund_VÆRDI){임시값=~0ull;fejl=34;}else 임시값=임시값*Baggrund_VÆRDI+destination_data;}
    if(afslutte_et_opkald_FORSKYDNING)*afslutte_et_opkald_FORSKYDNING=(char*)(하나라도?streng_data:START_FORSKYDNING);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*streng_data,char**보조항목,int SEKUND_VÆRDI){return strtoull(streng_data,보조항목,SEKUND_VÆRDI);}
long strtol(const char*streng_data,char**보조항목,int SEKUND_VÆRDI){return (long)strtoull(streng_data,보조항목,SEKUND_VÆRDI);}
int atoi(const char*streng_data){return (int)strtol(streng_data,0,10);}
long double ldexpl(long double X_koordinat,int vare_TÆL){while(vare_TÆL>0){X_koordinat*=2;vare_TÆL--;}while(vare_TÆL<0){X_koordinat/=2;vare_TÆL++;}return X_koordinat;}
long double strtold(const char*streng_data,char**afslutte_et_opkald_FORSKYDNING){
    const char*START_FORSKYDNING=streng_data;while(*streng_data==' '||(*streng_data>=9&&*streng_data<=13))streng_data++;int 음수여부=0;if(*streng_data=='-'||*streng_data=='+')음수여부=*streng_data++=='-';
    int Baggrund_VÆRDI=10;if(streng_data[0]=='0'&&(streng_data[1]=='x'||streng_data[1]=='X')){Baggrund_VÆRDI=16;streng_data+=2;}long double 임시값=0,skalere=1;int 소수부=0,하나라도=0;
    for(;;){int tegnkode=*streng_data,destination_data=tegnkode>='0'&&tegnkode<='9'?tegnkode-'0':tegnkode>='a'&&tegnkode<='f'?tegnkode-'a'+10:tegnkode>='A'&&tegnkode<='F'?tegnkode-'A'+10:99;
        if(tegnkode=='.'&&!소수부){소수부=1;streng_data++;continue;}if(destination_data>=Baggrund_VÆRDI)break;하나라도=1;streng_data++;임시값=임시값*Baggrund_VÆRDI+destination_data;if(소수부)skalere*=Baggrund_VÆRDI;
    }임시값/=skalere;
    if((Baggrund_VÆRDI==10&&(*streng_data=='e'||*streng_data=='E'))||(Baggrund_VÆRDI==16&&(*streng_data=='p'||*streng_data=='P'))){const char*vise_VÆRDI=streng_data++;int 빼기=0;if(*streng_data=='-'||*streng_data=='+')빼기=*streng_data++=='-';int vare_TÆL=0,post_TÆL_8f7753a1=0;while(*streng_data>='0'&&*streng_data<='9'){post_TÆL_8f7753a1++;if(vare_TÆL<20000)vare_TÆL=vare_TÆL*10+*streng_data-'0';streng_data++;}if(!post_TÆL_8f7753a1)streng_data=vise_VÆRDI;else{long double faktor=Baggrund_VÆRDI==16?2:10;while(vare_TÆL-->0&&vare_TÆL<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(afslutte_et_opkald_FORSKYDNING)*afslutte_et_opkald_FORSKYDNING=(char*)(하나라도?streng_data:START_FORSKYDNING);return 음수여부?-임시값:임시값;
}
double strtod(const char*streng_data,char**보조항목){return (double)strtold(streng_data,보조항목);}float strtof(const char*streng_data,char**보조항목){return (float)strtold(streng_data,보조항목);}
void qsort(void*Baggrund_VÆRDI,size_t vare_TÆL,size_t Størrelse,int(*Sammenlign)(const void*,const void*)){
    unsigned char*data_placere=Baggrund_VÆRDI;for(size_t 순번=1;순번<vare_TÆL;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Sammenlign(data_placere+(안쪽순번-1)*Størrelse,data_placere+안쪽순번*Størrelse)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Størrelse;셋째순번++){unsigned char tegnkode=data_placere[(안쪽순번-1)*Størrelse+셋째순번];data_placere[(안쪽순번-1)*Størrelse+셋째순번]=data_placere[안쪽순번*Størrelse+셋째순번];data_placere[안쪽순번*Størrelse+셋째순번]=tegnkode;}
}
static struct {int 사용량,Opslag_INDEKS;size_t Placering;} 열림[24];
static unsigned char produktoutput[32768];static size_t produktoutput_tilpasse_størrelse,produktoutput_placere;static int produktoutput_åben;
const unsigned char *C_produktoutput(size_t *vare_TÆL){*vare_TÆL=produktoutput_tilpasse_størrelse;return produktoutput;}
int open(const char*Navn,int konfiguration_BITS,...){
    if(!strcmp(Navn,"/@cc-output")){if(produktoutput_åben){fejl=16;return -1;}produktoutput_åben=1;produktoutput_tilpasse_størrelse=produktoutput_placere=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(compiler_Ressourcer)/sizeof(compiler_Ressourcer[0]);순번++)if(!strcmp(Navn,compiler_Ressourcer[순번].Navn)){
        if(konfiguration_BITS&3){fejl=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].Opslag_INDEKS=순번;열림[안쪽순번].Placering=0;return 128+안쪽순번;}fejl=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Navn,konfiguration_BITS,0,0,0,0);if(반환값<0){fejl=-반환값;return -1;}return 반환값;
}
int close(int fil_handle){if(fil_handle==100){produktoutput_åben=0;return 0;}if(fil_handle>=128&&fil_handle<152){열림[fil_handle-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,fil_handle,0,0,0,0,0);if(반환값<0){fejl=-반환값;return -1;}return 0;}
long read(int fil_handle,void*data,size_t vare_TÆL){
    if(fil_handle>=128&&fil_handle<152&&열림[fil_handle-128].사용량){int 순번=fil_handle-128;const compiler_ressource*반환값=&compiler_Ressourcer[열림[순번].Opslag_INDEKS];size_t 왼쪽=반환값->Størrelse-열림[순번].Placering;if(vare_TÆL>왼쪽)vare_TÆL=왼쪽;memcpy(data,반환값->data+열림[순번].Placering,vare_TÆL);열림[순번].Placering+=vare_TÆL;return vare_TÆL;}
    intptr_t 반환값=사용자호출(2,fil_handle,(uintptr_t)data,vare_TÆL,0,0,0);if(반환값<0){fejl=-반환값;return -1;}return 반환값;
}
long write(int fil_handle,const void*data,size_t vare_TÆL){
    if(fil_handle==100){if(vare_TÆL>sizeof(produktoutput)-produktoutput_placere){fejl=28;return -1;}memcpy(produktoutput+produktoutput_placere,data,vare_TÆL);produktoutput_placere+=vare_TÆL;if(produktoutput_tilpasse_størrelse<produktoutput_placere)produktoutput_tilpasse_størrelse=produktoutput_placere;return vare_TÆL;}
    intptr_t 반환값=사용자호출(1,fil_handle,(uintptr_t)data,vare_TÆL,0,0,0);if(반환값<0){fejl=-반환값;return -1;}return 반환값;
}
long lseek(int fil_handle,long FORSKYDNING_VÆRDI,int søge_begyndelsespunkt){
    if(fil_handle==100){long data_placere=FORSKYDNING_VÆRDI+(søge_begyndelsespunkt==0?0:søge_begyndelsespunkt==1?produktoutput_placere:produktoutput_tilpasse_størrelse);if(data_placere<0||(size_t)data_placere>sizeof(produktoutput)){fejl=22;return -1;}produktoutput_placere=data_placere;return data_placere;}
    if(fil_handle>=128&&fil_handle<152&&열림[fil_handle-128].사용량){int 순번=fil_handle-128;long data_placere=FORSKYDNING_VÆRDI+(søge_begyndelsespunkt==0?0:søge_begyndelsespunkt==1?열림[순번].Placering:compiler_Ressourcer[열림[순번].Opslag_INDEKS].Størrelse);if(data_placere<0||(size_t)data_placere>compiler_Ressourcer[열림[순번].Opslag_INDEKS].Størrelse){fejl=22;return -1;}열림[순번].Placering=data_placere;return data_placere;}
    intptr_t 반환값=사용자호출(5,fil_handle,FORSKYDNING_VÆRDI,søge_begyndelsespunkt,0,0,0);if(반환값<0){fejl=-반환값;return -1;}return 반환값;
}
int unlink(const char*Navn){intptr_t 반환값=사용자호출(11,(uintptr_t)Navn,0,0,0,0,0);if(반환값<0){fejl=-반환값;return -1;}return 반환값;}
char *realpath(const char*Navn,char*KR_data){if(!KR_data){KR_data=malloc(strlen(Navn)+1);if(!KR_data)return 0;}return strcpy(KR_data,Navn);}
char *getcwd(char*data_placere,size_t vare_TÆL){if(vare_TÆL<2){fejl=34;return 0;}data_placere[0]='/';data_placere[1]=0;return data_placere;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_post){time_t 임시값=0;if(Terminal_post)*Terminal_post=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_post){(void)Terminal_post;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Strømme[18]={{1,0,1},{2,0,1}};FILE*stdout=&Strømme[0],*stderr=&Strømme[1];
FILE*fdopen(int fil_handle,const char*metode_HYPPIGST){(void)metode_HYPPIGST;for(unsigned 순번=2;순번<18;순번++)if(!Strømme[순번].사용량){Strømme[순번].사용량=1;Strømme[순번].fejl=0;Strømme[순번].fil_handle=fil_handle;return &Strømme[순번];}fejl=24;return 0;}
int fflush(FILE*fil_post){return fil_post&&fil_post->fejl?-1:0;}
int fclose(FILE*fil_post){int 반환값=close(fil_post->fil_handle);if(fil_post->fejl)반환값=-1;fil_post->사용량=0;return 반환값;}
size_t fwrite(const void*data_placere,size_t streng_data,size_t vare_TÆL,FILE*fil_post){if(!streng_data)return 0;if(vare_TÆL>SIZE_MAX/streng_data){fil_post->fejl=1;return 0;}long 반환값=write(fil_post->fil_handle,data_placere,streng_data*vare_TÆL);if(반환값<0){fil_post->fejl=1;return 0;}return (size_t)반환값/streng_data;}
int fputc(int tegnkode,FILE*fil_post){unsigned char SEKUND_VÆRDI=tegnkode;return fwrite(&SEKUND_VÆRDI,1,1,fil_post)==1?SEKUND_VÆRDI:EOF;}
int fputs(const char*streng_data,FILE*fil_post){return fwrite(streng_data,1,strlen(streng_data),fil_post)==strlen(streng_data)?0:EOF;}
static void 넣기(char*KR_data,size_t 용량한도,size_t*aktuel_placere,char tegnkode){if(*aktuel_placere+1<용량한도)KR_data[*aktuel_placere]=tegnkode;(*aktuel_placere)++;}
int vsnprintf(char*KR_data,size_t 용량한도,const char*format,va_list 가변인수){
    size_t aktuel_placere=0;while(*format){if(*format!='%'){넣기(KR_data,용량한도,&aktuel_placere,*format++);continue;}format++;
        int 왼쪽=0,nulværdi=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')nulværdi=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,præcision_VÆRDI=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;præcision_VÆRDI=0;if(*format=='*'){præcision_VÆRDI=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')præcision_VÆRDI=præcision_VÆRDI*10+*format++-'0';}
        int bredt_tegn=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')bredt_tegn=1;format++;}
        char Type_område=*format?*format++:0,bufferlager[80];const char*streng_data=bufferlager;size_t vare_TÆL=0;
        if(Type_område=='s'){streng_data=va_arg(가변인수,const char*);if(!streng_data)streng_data="(null)";vare_TÆL=strlen(streng_data);if(præcision_VÆRDI>=0&&vare_TÆL>(size_t)præcision_VÆRDI)vare_TÆL=præcision_VÆRDI;}
        else if(Type_område=='c'){bufferlager[0]=va_arg(가변인수,int);vare_TÆL=1;}
        else if(Type_område=='%'){bufferlager[0]='%';vare_TÆL=1;}
        else if(Type_område=='d'||Type_område=='i'||Type_område=='u'||Type_område=='x'||Type_område=='X'||Type_område=='o'||Type_område=='p'){
            unsigned long long VÆRDI;int 음수표시=0;
            if(Type_område=='d'||Type_område=='i'){long long 임시값=bredt_tegn?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VÆRDI=음수표시?0-(unsigned long long)임시값:임시값;}
            else VÆRDI=Type_område=='p'?(uintptr_t)va_arg(가변인수,void*):bredt_tegn?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Baggrund_VÆRDI=Type_område=='x'||Type_område=='X'||Type_område=='p'?16:Type_område=='o'?8:10;char ciffer_TÆL[64];unsigned 사용량=0;
            do{ciffer_TÆL[사용량++]="0123456789abcdef"[VÆRDI%Baggrund_VÆRDI];VÆRDI/=Baggrund_VÆRDI;}while(VÆRDI);
            if(음수표시)bufferlager[vare_TÆL++]='-';if(Type_område=='p'||(대체값&&Baggrund_VÆRDI==16)){bufferlager[vare_TÆL++]='0';bufferlager[vare_TÆL++]='x';}
            for(int udfyld_VÆRDI=(int)사용량;præcision_VÆRDI>udfyld_VÆRDI&&vare_TÆL<sizeof(bufferlager)-사용량;udfyld_VÆRDI++)bufferlager[vare_TÆL++]='0';
            if(nulværdi&&!왼쪽&&præcision_VÆRDI<0)while(너비>(int)(vare_TÆL+사용량)&&vare_TÆL<sizeof(bufferlager)-사용량)bufferlager[vare_TÆL++]='0';
            while(사용량)bufferlager[vare_TÆL++]=ciffer_TÆL[--사용량];
        }else{bufferlager[0]='?';vare_TÆL=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)vare_TÆL){넣기(KR_data,용량한도,&aktuel_placere,' ');너비--;}
        for(size_t 순번=0;순번<vare_TÆL;순번++)넣기(KR_data,용량한도,&aktuel_placere,streng_data[순번]);while(왼쪽&&너비>(int)vare_TÆL){넣기(KR_data,용량한도,&aktuel_placere,' ');너비--;}
    }if(용량한도)KR_data[aktuel_placere<용량한도?aktuel_placere:용량한도-1]=0;return aktuel_placere;
}
int snprintf(char*KR_data,size_t 용량한도,const char*fil_post,...){va_list 첫째값;va_start(첫째값,fil_post);int 반환값=vsnprintf(KR_data,용량한도,fil_post,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_data,const char*fil_post,...){va_list 첫째값;va_start(첫째값,fil_post);int 반환값=vsnprintf(KR_data,SIZE_MAX,fil_post,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*strøm_VÆRDI,const char*fil_post,va_list 첫째값){char SEKUND_VÆRDI[2048];int vare_TÆL=vsnprintf(SEKUND_VÆRDI,sizeof(SEKUND_VÆRDI),fil_post,첫째값);if(vare_TÆL>2047)vare_TÆL=2047;return fwrite(SEKUND_VÆRDI,1,vare_TÆL,strøm_VÆRDI)==(size_t)vare_TÆL?vare_TÆL:-1;}
int fprintf(FILE*strøm_VÆRDI,const char*fil_post,...){va_list 첫째값;va_start(첫째값,fil_post);int 반환값=vfprintf(strøm_VÆRDI,fil_post,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*fil_post,...){va_list 첫째값;va_start(첫째값,fil_post);int 반환값=vfprintf(stdout,fil_post,첫째값);va_end(첫째값);return 반환값;}
