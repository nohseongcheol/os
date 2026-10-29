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
static int Impazamo;
int *__errno_location(void){return &Impazamo;}
void exit(int imo_ixabiso){사용자호출(6,imo_ixabiso,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *jonga_usetyenziso_oluxubileyo,const char *iFayili,unsigned umgca,const char *imethodi_ufako_nkcukacha_igama){fprintf(stderr,"cc assertion: %s %s:%u %s\n",jonga_usetyenziso_oluxubileyo,iFayili,umgca,imethodi_ufako_nkcukacha_igama);exit(1);}
size_t strlen(const char*uluhlu_lweekharektha_iingcombolo){const char*자료위치=uluhlu_lweekharektha_iingcombolo;while(*자료위치)자료위치++;return 자료위치-uluhlu_lweekharektha_iingcombolo;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char isilungelelanisi_x=*첫째값++,세로좌표=*둘째값++;if(isilungelelanisi_x!=세로좌표)return isilungelelanisi_x-세로좌표;if(!isilungelelanisi_x)return 0;}return 0;}
char *strcpy(char*indawo_ekuyiwa_kuyo_iingcombolo,const char*uluhlu_lweekharektha_iingcombolo){char*반환값=indawo_ekuyiwa_kuyo_iingcombolo;while((*indawo_ekuyiwa_kuyo_iingcombolo++=*uluhlu_lweekharektha_iingcombolo++)){}return 반환값;}
char *strchr(const char*uluhlu_lweekharektha_iingcombolo,int ikhowudi_yekharakhtha){do{if(*uluhlu_lweekharektha_iingcombolo==(char)ikhowudi_yekharakhtha)return (char*)uluhlu_lweekharektha_iingcombolo;}while(*uluhlu_lweekharektha_iingcombolo++);return 0;}
char *strrchr(const char*uluhlu_lweekharektha_iingcombolo,int ikhowudi_yekharakhtha){const char*반환값=0;do{if(*uluhlu_lweekharektha_iingcombolo==(char)ikhowudi_yekharakhtha)반환값=uluhlu_lweekharektha_iingcombolo;}while(*uluhlu_lweekharektha_iingcombolo++);return (char*)반환값;}
char *strstr(const char*uluhlu_lweekharektha_iingcombolo,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*uluhlu_lweekharektha_iingcombolo;uluhlu_lweekharektha_iingcombolo++)if(!strncmp(uluhlu_lweekharektha_iingcombolo,터미널항목,개수))return (char*)uluhlu_lweekharektha_iingcombolo;return 개수?0:(char*)uluhlu_lweekharektha_iingcombolo;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*isilungelelanisi_x=첫째값,*세로좌표=둘째값;while(개수--){if(*isilungelelanisi_x!=*세로좌표)return *isilungelelanisi_x-*세로좌표;isilungelelanisi_x++;세로좌표++;}return 0;}
void *memmove(void*indawo_ekuyiwa_kuyo_iingcombolo,const void*uluhlu_lweekharektha_iingcombolo,size_t 개수){unsigned char*isilungelelanisi_x=indawo_ekuyiwa_kuyo_iingcombolo;const unsigned char*세로좌표=uluhlu_lweekharektha_iingcombolo;if(isilungelelanisi_x<세로좌표){for(size_t 순번=0;순번<개수;순번++)isilungelelanisi_x[순번]=세로좌표[순번];}else while(개수){개수--;isilungelelanisi_x[개수]=세로좌표[개수];}return indawo_ekuyiwa_kuyo_iingcombolo;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct iingcombolo_thintela {size_t Ubukhulu;struct iingcombolo_thintela*다음;int 남은공간;int 채울크기;uint64_t ulungelelwaniso_isifundo;} iingcombolo_thintela;
static iingcombolo_thintela *첫항목;
void free(void*자료위치){if(!자료위치)return;iingcombolo_thintela*둘째값=(iingcombolo_thintela*)자료위치-1;둘째값->남은공간=1;for(iingcombolo_thintela*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->Ubukhulu+=sizeof(iingcombolo_thintela)+다음위치->다음->Ubukhulu;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(iingcombolo_thintela))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(iingcombolo_thintela*)할당마당;첫항목->Ubukhulu=sizeof(할당마당)-sizeof(iingcombolo_thintela);첫항목->남은공간=1;첫항목->다음=0;}
    iingcombolo_thintela*이전=자료위치?(iingcombolo_thintela*)자료위치-1:0;if(이전&&이전->Ubukhulu>=개수)return 자료위치;
    for(iingcombolo_thintela*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->Ubukhulu>=개수){
        if(둘째값->Ubukhulu>=개수+sizeof(iingcombolo_thintela)+16){iingcombolo_thintela*나머지부분=(iingcombolo_thintela*)((unsigned char*)(둘째값+1)+개수);나머지부분->Ubukhulu=둘째값->Ubukhulu-개수-sizeof(iingcombolo_thintela);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->Ubukhulu=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->Ubukhulu);free(자료위치);}return 반환값;
    }Impazamo=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t uluhlu_lweekharektha_iingcombolo){if(uluhlu_lweekharektha_iingcombolo&&개수>SIZE_MAX/uluhlu_lweekharektha_iingcombolo)return 0;void*자료위치=malloc(개수*uluhlu_lweekharektha_iingcombolo);if(자료위치)memset(자료위치,0,개수*uluhlu_lweekharektha_iingcombolo);return 자료위치;}
unsigned long long strtoull(const char*uluhlu_lweekharektha_iingcombolo,char**phela_Ukulinganisa,int Ngasemva_ixabiso){
    const char*qala_Ukulinganisa=uluhlu_lweekharektha_iingcombolo;while(*uluhlu_lweekharektha_iingcombolo==' '||(*uluhlu_lweekharektha_iingcombolo>=9&&*uluhlu_lweekharektha_iingcombolo<=13))uluhlu_lweekharektha_iingcombolo++;int 음수여부=0;if(*uluhlu_lweekharektha_iingcombolo=='-'||*uluhlu_lweekharektha_iingcombolo=='+')음수여부=*uluhlu_lweekharektha_iingcombolo++=='-';
    if((!Ngasemva_ixabiso||Ngasemva_ixabiso==16)&&uluhlu_lweekharektha_iingcombolo[0]=='0'&&(uluhlu_lweekharektha_iingcombolo[1]=='x'||uluhlu_lweekharektha_iingcombolo[1]=='X')){Ngasemva_ixabiso=16;uluhlu_lweekharektha_iingcombolo+=2;}if(!Ngasemva_ixabiso)Ngasemva_ixabiso=*uluhlu_lweekharektha_iingcombolo=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned ikhowudi_yekharakhtha=*uluhlu_lweekharektha_iingcombolo,indawo_ekuyiwa_kuyo_iingcombolo=ikhowudi_yekharakhtha>='0'&&ikhowudi_yekharakhtha<='9'?ikhowudi_yekharakhtha-'0':ikhowudi_yekharakhtha>='a'&&ikhowudi_yekharakhtha<='z'?ikhowudi_yekharakhtha-'a'+10:ikhowudi_yekharakhtha>='A'&&ikhowudi_yekharakhtha<='Z'?ikhowudi_yekharakhtha-'A'+10:99;if(indawo_ekuyiwa_kuyo_iingcombolo>=(unsigned)Ngasemva_ixabiso)break;하나라도=1;uluhlu_lweekharektha_iingcombolo++;if(임시값>(~0ull-indawo_ekuyiwa_kuyo_iingcombolo)/(unsigned)Ngasemva_ixabiso){임시값=~0ull;Impazamo=34;}else 임시값=임시값*Ngasemva_ixabiso+indawo_ekuyiwa_kuyo_iingcombolo;}
    if(phela_Ukulinganisa)*phela_Ukulinganisa=(char*)(하나라도?uluhlu_lweekharektha_iingcombolo:qala_Ukulinganisa);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*uluhlu_lweekharektha_iingcombolo,char**보조항목,int 둘째값){return strtoull(uluhlu_lweekharektha_iingcombolo,보조항목,둘째값);}
long strtol(const char*uluhlu_lweekharektha_iingcombolo,char**보조항목,int 둘째값){return (long)strtoull(uluhlu_lweekharektha_iingcombolo,보조항목,둘째값);}
int atoi(const char*uluhlu_lweekharektha_iingcombolo){return (int)strtol(uluhlu_lweekharektha_iingcombolo,0,10);}
long double ldexpl(long double isilungelelanisi_x,int 개수){while(개수>0){isilungelelanisi_x*=2;개수--;}while(개수<0){isilungelelanisi_x/=2;개수++;}return isilungelelanisi_x;}
long double strtold(const char*uluhlu_lweekharektha_iingcombolo,char**phela_Ukulinganisa){
    const char*qala_Ukulinganisa=uluhlu_lweekharektha_iingcombolo;while(*uluhlu_lweekharektha_iingcombolo==' '||(*uluhlu_lweekharektha_iingcombolo>=9&&*uluhlu_lweekharektha_iingcombolo<=13))uluhlu_lweekharektha_iingcombolo++;int 음수여부=0;if(*uluhlu_lweekharektha_iingcombolo=='-'||*uluhlu_lweekharektha_iingcombolo=='+')음수여부=*uluhlu_lweekharektha_iingcombolo++=='-';
    int Ngasemva_ixabiso=10;if(uluhlu_lweekharektha_iingcombolo[0]=='0'&&(uluhlu_lweekharektha_iingcombolo[1]=='x'||uluhlu_lweekharektha_iingcombolo[1]=='X')){Ngasemva_ixabiso=16;uluhlu_lweekharektha_iingcombolo+=2;}long double 임시값=0,linganisela=1;int 소수부=0,하나라도=0;
    for(;;){int ikhowudi_yekharakhtha=*uluhlu_lweekharektha_iingcombolo,indawo_ekuyiwa_kuyo_iingcombolo=ikhowudi_yekharakhtha>='0'&&ikhowudi_yekharakhtha<='9'?ikhowudi_yekharakhtha-'0':ikhowudi_yekharakhtha>='a'&&ikhowudi_yekharakhtha<='f'?ikhowudi_yekharakhtha-'a'+10:ikhowudi_yekharakhtha>='A'&&ikhowudi_yekharakhtha<='F'?ikhowudi_yekharakhtha-'A'+10:99;
        if(ikhowudi_yekharakhtha=='.'&&!소수부){소수부=1;uluhlu_lweekharektha_iingcombolo++;continue;}if(indawo_ekuyiwa_kuyo_iingcombolo>=Ngasemva_ixabiso)break;하나라도=1;uluhlu_lweekharektha_iingcombolo++;임시값=임시값*Ngasemva_ixabiso+indawo_ekuyiwa_kuyo_iingcombolo;if(소수부)linganisela*=Ngasemva_ixabiso;
    }임시값/=linganisela;
    if((Ngasemva_ixabiso==10&&(*uluhlu_lweekharektha_iingcombolo=='e'||*uluhlu_lweekharektha_iingcombolo=='E'))||(Ngasemva_ixabiso==16&&(*uluhlu_lweekharektha_iingcombolo=='p'||*uluhlu_lweekharektha_iingcombolo=='P'))){const char*bonisa_ixabiso=uluhlu_lweekharektha_iingcombolo++;int 빼기=0;if(*uluhlu_lweekharektha_iingcombolo=='-'||*uluhlu_lweekharektha_iingcombolo=='+')빼기=*uluhlu_lweekharektha_iingcombolo++=='-';int 개수=0,항목수=0;while(*uluhlu_lweekharektha_iingcombolo>='0'&&*uluhlu_lweekharektha_iingcombolo<='9'){항목수++;if(개수<20000)개수=개수*10+*uluhlu_lweekharektha_iingcombolo-'0';uluhlu_lweekharektha_iingcombolo++;}if(!항목수)uluhlu_lweekharektha_iingcombolo=bonisa_ixabiso;else{long double ifekta=Ngasemva_ixabiso==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/ifekta:임시값*ifekta;}}
    if(phela_Ukulinganisa)*phela_Ukulinganisa=(char*)(하나라도?uluhlu_lweekharektha_iingcombolo:qala_Ukulinganisa);return 음수여부?-임시값:임시값;
}
double strtod(const char*uluhlu_lweekharektha_iingcombolo,char**보조항목){return (double)strtold(uluhlu_lweekharektha_iingcombolo,보조항목);}float strtof(const char*uluhlu_lweekharektha_iingcombolo,char**보조항목){return (float)strtold(uluhlu_lweekharektha_iingcombolo,보조항목);}
void qsort(void*Ngasemva_ixabiso,size_t 개수,size_t Ubukhulu,int(*Thelekisa)(const void*,const void*)){
    unsigned char*자료위치=Ngasemva_ixabiso;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Thelekisa(자료위치+(안쪽순번-1)*Ubukhulu,자료위치+안쪽순번*Ubukhulu)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Ubukhulu;셋째순번++){unsigned char ikhowudi_yekharakhtha=자료위치[(안쪽순번-1)*Ubukhulu+셋째순번];자료위치[(안쪽순번-1)*Ubukhulu+셋째순번]=자료위치[안쪽순번*Ubukhulu+셋째순번];자료위치[안쪽순번*Ubukhulu+셋째순번]=ikhowudi_yekharakhtha;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*Igama,int 설정비트,...){
    if(!strcmp(Igama,"/@cc-output")){if(출력열림){Impazamo=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Igama,번역기자원들[순번].Igama)){
        if(설정비트&3){Impazamo=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}Impazamo=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Igama,설정비트,0,0,0,0);if(반환값<0){Impazamo=-반환값;return -1;}return 반환값;
}
int close(int ifayile_isibambi){if(ifayile_isibambi==100){출력열림=0;return 0;}if(ifayile_isibambi>=128&&ifayile_isibambi<152){열림[ifayile_isibambi-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,ifayile_isibambi,0,0,0,0,0);if(반환값<0){Impazamo=-반환값;return -1;}return 0;}
long read(int ifayile_isibambi,void*iingcombolo,size_t 개수){
    if(ifayile_isibambi>=128&&ifayile_isibambi<152&&열림[ifayile_isibambi-128].사용량){int 순번=ifayile_isibambi-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->Ubukhulu-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(iingcombolo,반환값->iingcombolo+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,ifayile_isibambi,(uintptr_t)iingcombolo,개수,0,0,0);if(반환값<0){Impazamo=-반환값;return -1;}return 반환값;
}
long write(int ifayile_isibambi,const void*iingcombolo,size_t 개수){
    if(ifayile_isibambi==100){if(개수>sizeof(출력결과)-출력위치){Impazamo=28;return -1;}memcpy(출력결과+출력위치,iingcombolo,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,ifayile_isibambi,(uintptr_t)iingcombolo,개수,0,0,0);if(반환값<0){Impazamo=-반환값;return -1;}return 반환값;
}
long lseek(int ifayile_isibambi,long Ukulinganisa_ixabiso,int 기준점){
    if(ifayile_isibambi==100){long 자료위치=Ukulinganisa_ixabiso+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){Impazamo=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(ifayile_isibambi>=128&&ifayile_isibambi<152&&열림[ifayile_isibambi-128].사용량){int 순번=ifayile_isibambi-128;long 자료위치=Ukulinganisa_ixabiso+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].Ubukhulu);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].Ubukhulu){Impazamo=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,ifayile_isibambi,Ukulinganisa_ixabiso,기준점,0,0,0);if(반환값<0){Impazamo=-반환값;return -1;}return 반환값;
}
int unlink(const char*Igama){intptr_t 반환값=사용자호출(11,(uintptr_t)Igama,0,0,0,0,0);if(반환값<0){Impazamo=-반환값;return -1;}return 반환값;}
char *realpath(const char*Igama,char*결과자료){if(!결과자료){결과자료=malloc(strlen(Igama)+1);if(!결과자료)return 0;}return strcpy(결과자료,Igama);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){Impazamo=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int ifayile_isibambi,const char*imethodi_imo){(void)imethodi_imo;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Impazamo=0;흐름목록[순번].ifayile_isibambi=ifayile_isibambi;return &흐름목록[순번];}Impazamo=24;return 0;}
int fflush(FILE*ifayile_ufako_nkcukacha){return ifayile_ufako_nkcukacha&&ifayile_ufako_nkcukacha->Impazamo?-1:0;}
int fclose(FILE*ifayile_ufako_nkcukacha){int 반환값=close(ifayile_ufako_nkcukacha->ifayile_isibambi);if(ifayile_ufako_nkcukacha->Impazamo)반환값=-1;ifayile_ufako_nkcukacha->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t uluhlu_lweekharektha_iingcombolo,size_t 개수,FILE*ifayile_ufako_nkcukacha){if(!uluhlu_lweekharektha_iingcombolo)return 0;if(개수>SIZE_MAX/uluhlu_lweekharektha_iingcombolo){ifayile_ufako_nkcukacha->Impazamo=1;return 0;}long 반환값=write(ifayile_ufako_nkcukacha->ifayile_isibambi,자료위치,uluhlu_lweekharektha_iingcombolo*개수);if(반환값<0){ifayile_ufako_nkcukacha->Impazamo=1;return 0;}return (size_t)반환값/uluhlu_lweekharektha_iingcombolo;}
int fputc(int ikhowudi_yekharakhtha,FILE*ifayile_ufako_nkcukacha){unsigned char 둘째값=ikhowudi_yekharakhtha;return fwrite(&둘째값,1,1,ifayile_ufako_nkcukacha)==1?둘째값:EOF;}
int fputs(const char*uluhlu_lweekharektha_iingcombolo,FILE*ifayile_ufako_nkcukacha){return fwrite(uluhlu_lweekharektha_iingcombolo,1,strlen(uluhlu_lweekharektha_iingcombolo),ifayile_ufako_nkcukacha)==strlen(uluhlu_lweekharektha_iingcombolo)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char ikhowudi_yekharakhtha){if(*현재위치+1<용량한도)결과자료[*현재위치]=ikhowudi_yekharakhtha;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*fomatha,va_list 가변인수){
    size_t 현재위치=0;while(*fomatha){if(*fomatha!='%'){넣기(결과자료,용량한도,&현재위치,*fomatha++);continue;}fomatha++;
        int 왼쪽=0,영값=0,대체값=0;while(*fomatha=='-'||*fomatha=='0'||*fomatha=='#'||*fomatha=='+'||*fomatha==' '){if(*fomatha=='-')왼쪽=1;if(*fomatha=='0')영값=1;if(*fomatha=='#')대체값=1;fomatha++;}
        int 너비=0,정밀도=-1;if(*fomatha=='*'){너비=va_arg(가변인수,int);fomatha++;}else while(*fomatha>='0'&&*fomatha<='9')너비=너비*10+*fomatha++-'0';
        if(*fomatha=='.'){fomatha++;정밀도=0;if(*fomatha=='*'){정밀도=va_arg(가변인수,int);fomatha++;}else while(*fomatha>='0'&&*fomatha<='9')정밀도=정밀도*10+*fomatha++-'0';}
        int 넓은글자=0;while(*fomatha=='l'||*fomatha=='z'||*fomatha=='t'||*fomatha=='j'||*fomatha=='h'){if(*fomatha!='h')넓은글자=1;fomatha++;}
        char uhlobo_udidi=*fomatha?*fomatha++:0,isigcini_lwazi_sethutyana_Ugcino[80];const char*uluhlu_lweekharektha_iingcombolo=isigcini_lwazi_sethutyana_Ugcino;size_t 개수=0;
        if(uhlobo_udidi=='s'){uluhlu_lweekharektha_iingcombolo=va_arg(가변인수,const char*);if(!uluhlu_lweekharektha_iingcombolo)uluhlu_lweekharektha_iingcombolo="(null)";개수=strlen(uluhlu_lweekharektha_iingcombolo);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(uhlobo_udidi=='c'){isigcini_lwazi_sethutyana_Ugcino[0]=va_arg(가변인수,int);개수=1;}
        else if(uhlobo_udidi=='%'){isigcini_lwazi_sethutyana_Ugcino[0]='%';개수=1;}
        else if(uhlobo_udidi=='d'||uhlobo_udidi=='i'||uhlobo_udidi=='u'||uhlobo_udidi=='x'||uhlobo_udidi=='X'||uhlobo_udidi=='o'||uhlobo_udidi=='p'){
            unsigned long long ixabiso;int 음수표시=0;
            if(uhlobo_udidi=='d'||uhlobo_udidi=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;ixabiso=음수표시?0-(unsigned long long)임시값:임시값;}
            else ixabiso=uhlobo_udidi=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Ngasemva_ixabiso=uhlobo_udidi=='x'||uhlobo_udidi=='X'||uhlobo_udidi=='p'?16:uhlobo_udidi=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[ixabiso%Ngasemva_ixabiso];ixabiso/=Ngasemva_ixabiso;}while(ixabiso);
            if(음수표시)isigcini_lwazi_sethutyana_Ugcino[개수++]='-';if(uhlobo_udidi=='p'||(대체값&&Ngasemva_ixabiso==16)){isigcini_lwazi_sethutyana_Ugcino[개수++]='0';isigcini_lwazi_sethutyana_Ugcino[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(isigcini_lwazi_sethutyana_Ugcino)-사용량;채움++)isigcini_lwazi_sethutyana_Ugcino[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(isigcini_lwazi_sethutyana_Ugcino)-사용량)isigcini_lwazi_sethutyana_Ugcino[개수++]='0';
            while(사용량)isigcini_lwazi_sethutyana_Ugcino[개수++]=숫자수[--사용량];
        }else{isigcini_lwazi_sethutyana_Ugcino[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,uluhlu_lweekharektha_iingcombolo[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*ifayile_ufako_nkcukacha,...){va_list 첫째값;va_start(첫째값,ifayile_ufako_nkcukacha);int 반환값=vsnprintf(결과자료,용량한도,ifayile_ufako_nkcukacha,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*ifayile_ufako_nkcukacha,...){va_list 첫째값;va_start(첫째값,ifayile_ufako_nkcukacha);int 반환값=vsnprintf(결과자료,SIZE_MAX,ifayile_ufako_nkcukacha,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_ixabiso,const char*ifayile_ufako_nkcukacha,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),ifayile_ufako_nkcukacha,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,Stream_ixabiso)==(size_t)개수?개수:-1;}
int fprintf(FILE*Stream_ixabiso,const char*ifayile_ufako_nkcukacha,...){va_list 첫째값;va_start(첫째값,ifayile_ufako_nkcukacha);int 반환값=vfprintf(Stream_ixabiso,ifayile_ufako_nkcukacha,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*ifayile_ufako_nkcukacha,...){va_list 첫째값;va_start(첫째값,ifayile_ufako_nkcukacha);int 반환값=vfprintf(stdout,ifayile_ufako_nkcukacha,첫째값);va_end(첫째값);return 반환값;}
