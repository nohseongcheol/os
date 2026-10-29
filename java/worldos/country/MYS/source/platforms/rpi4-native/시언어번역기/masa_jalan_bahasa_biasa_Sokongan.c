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
static int RALAT;
int *__errno_location(void){return &RALAT;}
void exit(int status_VALUE){사용자호출(6,status_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *cek_ungkapan,const char *Fail,unsigned baris,const char *kaedah_pemasukan_nama){fprintf(stderr,"cc assertion: %s %s:%u %s\n",cek_ungkapan,Fail,baris,kaedah_pemasukan_nama);exit(1);}
size_t strlen(const char*rentetan_data){const char*data_jawatan=rentetan_data;while(*data_jawatan)data_jawatan++;return data_jawatan-rentetan_data;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t item_COUNT){while(item_COUNT--){unsigned char koordinat_x=*첫째값++,Y_koordinat=*SECOND_VALUE++;if(koordinat_x!=Y_koordinat)return koordinat_x-Y_koordinat;if(!koordinat_x)return 0;}return 0;}
char *strcpy(char*destinasi_data,const char*rentetan_data){char*반환값=destinasi_data;while((*destinasi_data++=*rentetan_data++)){}return 반환값;}
char *strchr(const char*rentetan_data,int titik_kod){do{if(*rentetan_data==(char)titik_kod)return (char*)rentetan_data;}while(*rentetan_data++);return 0;}
char *strrchr(const char*rentetan_data,int titik_kod){const char*반환값=0;do{if(*rentetan_data==(char)titik_kod)반환값=rentetan_data;}while(*rentetan_data++);return (char*)반환값;}
char *strstr(const char*rentetan_data,const char*Terminal_pemasukan){size_t item_COUNT=strlen(Terminal_pemasukan);for(;*rentetan_data;rentetan_data++)if(!strncmp(rentetan_data,Terminal_pemasukan,item_COUNT))return (char*)rentetan_data;return item_COUNT?0:(char*)rentetan_data;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t item_COUNT){const unsigned char*koordinat_x=첫째값,*Y_koordinat=SECOND_VALUE;while(item_COUNT--){if(*koordinat_x!=*Y_koordinat)return *koordinat_x-*Y_koordinat;koordinat_x++;Y_koordinat++;}return 0;}
void *memmove(void*destinasi_data,const void*rentetan_data,size_t item_COUNT){unsigned char*koordinat_x=destinasi_data;const unsigned char*Y_koordinat=rentetan_data;if(koordinat_x<Y_koordinat){for(size_t 순번=0;순번<item_COUNT;순번++)koordinat_x[순번]=Y_koordinat[순번];}else while(item_COUNT){item_COUNT--;koordinat_x[item_COUNT]=Y_koordinat[item_COUNT];}return destinasi_data;}
static unsigned char peruntukan_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct blok_data {size_t Saiz;struct blok_data*Seterusnya_item;int 남은공간;int pelapik;uint64_t jajaran_unit;} blok_data;
static blok_data *첫항목;
void free(void*data_jawatan){if(!data_jawatan)return;blok_data*SECOND_VALUE=(blok_data*)data_jawatan-1;SECOND_VALUE->남은공간=1;for(blok_data*Seterusnya_Ofset=첫항목;Seterusnya_Ofset&&Seterusnya_Ofset->Seterusnya_item;){if(Seterusnya_Ofset->남은공간&&Seterusnya_Ofset->Seterusnya_item->남은공간){Seterusnya_Ofset->Saiz+=sizeof(blok_data)+Seterusnya_Ofset->Seterusnya_item->Saiz;Seterusnya_Ofset->Seterusnya_item=Seterusnya_Ofset->Seterusnya_item->Seterusnya_item;}else Seterusnya_Ofset=Seterusnya_Ofset->Seterusnya_item;}}
void *realloc(void*data_jawatan,size_t item_COUNT){
    if(!item_COUNT){free(data_jawatan);return 0;}if(item_COUNT>sizeof(peruntukan_Arena)-sizeof(blok_data))return 0;item_COUNT=(item_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(blok_data*)peruntukan_Arena;첫항목->Saiz=sizeof(peruntukan_Arena)-sizeof(blok_data);첫항목->남은공간=1;첫항목->Seterusnya_item=0;}
    blok_data*이전=data_jawatan?(blok_data*)data_jawatan-1:0;if(이전&&이전->Saiz>=item_COUNT)return data_jawatan;
    for(blok_data*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Seterusnya_item)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Saiz>=item_COUNT){
        if(SECOND_VALUE->Saiz>=item_COUNT+sizeof(blok_data)+16){blok_data*나머지부분=(blok_data*)((unsigned char*)(SECOND_VALUE+1)+item_COUNT);나머지부분->Saiz=SECOND_VALUE->Saiz-item_COUNT-sizeof(blok_data);나머지부분->Seterusnya_item=SECOND_VALUE->Seterusnya_item;나머지부분->남은공간=1;SECOND_VALUE->Seterusnya_item=나머지부분;SECOND_VALUE->Saiz=item_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,data_jawatan,이전->Saiz);free(data_jawatan);}return 반환값;
    }RALAT=12;return 0;
}
void *malloc(size_t item_COUNT){return realloc(0,item_COUNT);}
void *calloc(size_t item_COUNT,size_t rentetan_data){if(rentetan_data&&item_COUNT>SIZE_MAX/rentetan_data)return 0;void*data_jawatan=malloc(item_COUNT*rentetan_data);if(data_jawatan)memset(data_jawatan,0,item_COUNT*rentetan_data);return data_jawatan;}
unsigned long long strtoull(const char*rentetan_data,char**tamat_Ofset,int latar_VALUE){
    const char*Mula_Ofset=rentetan_data;while(*rentetan_data==' '||(*rentetan_data>=9&&*rentetan_data<=13))rentetan_data++;int 음수여부=0;if(*rentetan_data=='-'||*rentetan_data=='+')음수여부=*rentetan_data++=='-';
    if((!latar_VALUE||latar_VALUE==16)&&rentetan_data[0]=='0'&&(rentetan_data[1]=='x'||rentetan_data[1]=='X')){latar_VALUE=16;rentetan_data+=2;}if(!latar_VALUE)latar_VALUE=*rentetan_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned titik_kod=*rentetan_data,destinasi_data=titik_kod>='0'&&titik_kod<='9'?titik_kod-'0':titik_kod>='a'&&titik_kod<='z'?titik_kod-'a'+10:titik_kod>='A'&&titik_kod<='Z'?titik_kod-'A'+10:99;if(destinasi_data>=(unsigned)latar_VALUE)break;하나라도=1;rentetan_data++;if(임시값>(~0ull-destinasi_data)/(unsigned)latar_VALUE){임시값=~0ull;RALAT=34;}else 임시값=임시값*latar_VALUE+destinasi_data;}
    if(tamat_Ofset)*tamat_Ofset=(char*)(하나라도?rentetan_data:Mula_Ofset);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*rentetan_data,char**보조항목,int SECOND_VALUE){return strtoull(rentetan_data,보조항목,SECOND_VALUE);}
long strtol(const char*rentetan_data,char**보조항목,int SECOND_VALUE){return (long)strtoull(rentetan_data,보조항목,SECOND_VALUE);}
int atoi(const char*rentetan_data){return (int)strtol(rentetan_data,0,10);}
long double ldexpl(long double koordinat_x,int item_COUNT){while(item_COUNT>0){koordinat_x*=2;item_COUNT--;}while(item_COUNT<0){koordinat_x/=2;item_COUNT++;}return koordinat_x;}
long double strtold(const char*rentetan_data,char**tamat_Ofset){
    const char*Mula_Ofset=rentetan_data;while(*rentetan_data==' '||(*rentetan_data>=9&&*rentetan_data<=13))rentetan_data++;int 음수여부=0;if(*rentetan_data=='-'||*rentetan_data=='+')음수여부=*rentetan_data++=='-';
    int latar_VALUE=10;if(rentetan_data[0]=='0'&&(rentetan_data[1]=='x'||rentetan_data[1]=='X')){latar_VALUE=16;rentetan_data+=2;}long double 임시값=0,skala=1;int 소수부=0,하나라도=0;
    for(;;){int titik_kod=*rentetan_data,destinasi_data=titik_kod>='0'&&titik_kod<='9'?titik_kod-'0':titik_kod>='a'&&titik_kod<='f'?titik_kod-'a'+10:titik_kod>='A'&&titik_kod<='F'?titik_kod-'A'+10:99;
        if(titik_kod=='.'&&!소수부){소수부=1;rentetan_data++;continue;}if(destinasi_data>=latar_VALUE)break;하나라도=1;rentetan_data++;임시값=임시값*latar_VALUE+destinasi_data;if(소수부)skala*=latar_VALUE;
    }임시값/=skala;
    if((latar_VALUE==10&&(*rentetan_data=='e'||*rentetan_data=='E'))||(latar_VALUE==16&&(*rentetan_data=='p'||*rentetan_data=='P'))){const char*tayang_VALUE=rentetan_data++;int 빼기=0;if(*rentetan_data=='-'||*rentetan_data=='+')빼기=*rentetan_data++=='-';int item_COUNT=0,pemasukan_COUNT=0;while(*rentetan_data>='0'&&*rentetan_data<='9'){pemasukan_COUNT++;if(item_COUNT<20000)item_COUNT=item_COUNT*10+*rentetan_data-'0';rentetan_data++;}if(!pemasukan_COUNT)rentetan_data=tayang_VALUE;else{long double faktor=latar_VALUE==16?2:10;while(item_COUNT-->0&&item_COUNT<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(tamat_Ofset)*tamat_Ofset=(char*)(하나라도?rentetan_data:Mula_Ofset);return 음수여부?-임시값:임시값;
}
double strtod(const char*rentetan_data,char**보조항목){return (double)strtold(rentetan_data,보조항목);}float strtof(const char*rentetan_data,char**보조항목){return (float)strtold(rentetan_data,보조항목);}
void qsort(void*latar_VALUE,size_t item_COUNT,size_t Saiz,int(*Banding)(const void*,const void*)){
    unsigned char*data_jawatan=latar_VALUE;for(size_t 순번=1;순번<item_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Banding(data_jawatan+(안쪽순번-1)*Saiz,data_jawatan+안쪽순번*Saiz)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Saiz;셋째순번++){unsigned char titik_kod=data_jawatan[(안쪽순번-1)*Saiz+셋째순번];data_jawatan[(안쪽순번-1)*Saiz+셋째순번]=data_jawatan[안쪽순번*Saiz+셋째순번];data_jawatan[안쪽순번*Saiz+셋째순번]=titik_kod;}
}
static struct {int 사용량,Carian_INDEX;size_t Kedudukan;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *item_COUNT){*item_COUNT=출력크기;return 출력결과;}
int open(const char*Nama,int konfigurasi_Background_Intelligent_Transfer_Service,...){
    if(!strcmp(Nama,"/@cc-output")){if(출력열림){RALAT=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Nama,번역기자원들[순번].Nama)){
        if(konfigurasi_Background_Intelligent_Transfer_Service&3){RALAT=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].Carian_INDEX=순번;열림[안쪽순번].Kedudukan=0;return 128+안쪽순번;}RALAT=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nama,konfigurasi_Background_Intelligent_Transfer_Service,0,0,0,0);if(반환값<0){RALAT=-반환값;return -1;}return 반환값;
}
int close(int fail_pemegang){if(fail_pemegang==100){출력열림=0;return 0;}if(fail_pemegang>=128&&fail_pemegang<152){열림[fail_pemegang-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,fail_pemegang,0,0,0,0,0);if(반환값<0){RALAT=-반환값;return -1;}return 0;}
long read(int fail_pemegang,void*data,size_t item_COUNT){
    if(fail_pemegang>=128&&fail_pemegang<152&&열림[fail_pemegang-128].사용량){int 순번=fail_pemegang-128;const 번역기자원*반환값=&번역기자원들[열림[순번].Carian_INDEX];size_t 왼쪽=반환값->Saiz-열림[순번].Kedudukan;if(item_COUNT>왼쪽)item_COUNT=왼쪽;memcpy(data,반환값->data+열림[순번].Kedudukan,item_COUNT);열림[순번].Kedudukan+=item_COUNT;return item_COUNT;}
    intptr_t 반환값=사용자호출(2,fail_pemegang,(uintptr_t)data,item_COUNT,0,0,0);if(반환값<0){RALAT=-반환값;return -1;}return 반환값;
}
long write(int fail_pemegang,const void*data,size_t item_COUNT){
    if(fail_pemegang==100){if(item_COUNT>sizeof(출력결과)-출력위치){RALAT=28;return -1;}memcpy(출력결과+출력위치,data,item_COUNT);출력위치+=item_COUNT;if(출력크기<출력위치)출력크기=출력위치;return item_COUNT;}
    intptr_t 반환값=사용자호출(1,fail_pemegang,(uintptr_t)data,item_COUNT,0,0,0);if(반환값<0){RALAT=-반환값;return -1;}return 반환값;
}
long lseek(int fail_pemegang,long Ofset_VALUE,int 기준점){
    if(fail_pemegang==100){long data_jawatan=Ofset_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(data_jawatan<0||(size_t)data_jawatan>sizeof(출력결과)){RALAT=22;return -1;}출력위치=data_jawatan;return data_jawatan;}
    if(fail_pemegang>=128&&fail_pemegang<152&&열림[fail_pemegang-128].사용량){int 순번=fail_pemegang-128;long data_jawatan=Ofset_VALUE+(기준점==0?0:기준점==1?열림[순번].Kedudukan:번역기자원들[열림[순번].Carian_INDEX].Saiz);if(data_jawatan<0||(size_t)data_jawatan>번역기자원들[열림[순번].Carian_INDEX].Saiz){RALAT=22;return -1;}열림[순번].Kedudukan=data_jawatan;return data_jawatan;}
    intptr_t 반환값=사용자호출(5,fail_pemegang,Ofset_VALUE,기준점,0,0,0);if(반환값<0){RALAT=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nama){intptr_t 반환값=사용자호출(11,(uintptr_t)Nama,0,0,0,0,0);if(반환값<0){RALAT=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nama,char*ukuran_data){if(!ukuran_data){ukuran_data=malloc(strlen(Nama)+1);if(!ukuran_data)return 0;}return strcpy(ukuran_data,Nama);}
char *getcwd(char*data_jawatan,size_t item_COUNT){if(item_COUNT<2){RALAT=34;return 0;}data_jawatan[0]='/';data_jawatan[1]=0;return data_jawatan;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_pemasukan){time_t 임시값=0;if(Terminal_pemasukan)*Terminal_pemasukan=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_pemasukan){(void)Terminal_pemasukan;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Strim[18]={{1,0,1},{2,0,1}};FILE*stdout=&Strim[0],*stderr=&Strim[1];
FILE*fdopen(int fail_pemegang,const char*kaedah_mod){(void)kaedah_mod;for(unsigned 순번=2;순번<18;순번++)if(!Strim[순번].사용량){Strim[순번].사용량=1;Strim[순번].RALAT=0;Strim[순번].fail_pemegang=fail_pemegang;return &Strim[순번];}RALAT=24;return 0;}
int fflush(FILE*fail_pemasukan){return fail_pemasukan&&fail_pemasukan->RALAT?-1:0;}
int fclose(FILE*fail_pemasukan){int 반환값=close(fail_pemasukan->fail_pemegang);if(fail_pemasukan->RALAT)반환값=-1;fail_pemasukan->사용량=0;return 반환값;}
size_t fwrite(const void*data_jawatan,size_t rentetan_data,size_t item_COUNT,FILE*fail_pemasukan){if(!rentetan_data)return 0;if(item_COUNT>SIZE_MAX/rentetan_data){fail_pemasukan->RALAT=1;return 0;}long 반환값=write(fail_pemasukan->fail_pemegang,data_jawatan,rentetan_data*item_COUNT);if(반환값<0){fail_pemasukan->RALAT=1;return 0;}return (size_t)반환값/rentetan_data;}
int fputc(int titik_kod,FILE*fail_pemasukan){unsigned char SECOND_VALUE=titik_kod;return fwrite(&SECOND_VALUE,1,1,fail_pemasukan)==1?SECOND_VALUE:EOF;}
int fputs(const char*rentetan_data,FILE*fail_pemasukan){return fwrite(rentetan_data,1,strlen(rentetan_data),fail_pemasukan)==strlen(rentetan_data)?0:EOF;}
static void 넣기(char*ukuran_data,size_t 용량한도,size_t*현재위치,char titik_kod){if(*현재위치+1<용량한도)ukuran_data[*현재위치]=titik_kod;(*현재위치)++;}
int vsnprintf(char*ukuran_data,size_t 용량한도,const char*format,va_list 가변인수){
    size_t 현재위치=0;while(*format){if(*format!='%'){넣기(ukuran_data,용량한도,&현재위치,*format++);continue;}format++;
        int 왼쪽=0,영값=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')영값=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,kepersisan_VALUE=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;kepersisan_VALUE=0;if(*format=='*'){kepersisan_VALUE=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')kepersisan_VALUE=kepersisan_VALUE*10+*format++-'0';}
        int aksara_lebar=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')aksara_lebar=1;format++;}
        char TYPE_bidang=*format?*format++:0,storan_penimbal[80];const char*rentetan_data=storan_penimbal;size_t item_COUNT=0;
        if(TYPE_bidang=='s'){rentetan_data=va_arg(가변인수,const char*);if(!rentetan_data)rentetan_data="(null)";item_COUNT=strlen(rentetan_data);if(kepersisan_VALUE>=0&&item_COUNT>(size_t)kepersisan_VALUE)item_COUNT=kepersisan_VALUE;}
        else if(TYPE_bidang=='c'){storan_penimbal[0]=va_arg(가변인수,int);item_COUNT=1;}
        else if(TYPE_bidang=='%'){storan_penimbal[0]='%';item_COUNT=1;}
        else if(TYPE_bidang=='d'||TYPE_bidang=='i'||TYPE_bidang=='u'||TYPE_bidang=='x'||TYPE_bidang=='X'||TYPE_bidang=='o'||TYPE_bidang=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_bidang=='d'||TYPE_bidang=='i'){long long 임시값=aksara_lebar?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_bidang=='p'?(uintptr_t)va_arg(가변인수,void*):aksara_lebar?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned latar_VALUE=TYPE_bidang=='x'||TYPE_bidang=='X'||TYPE_bidang=='p'?16:TYPE_bidang=='o'?8:10;char digit_COUNT[64];unsigned 사용량=0;
            do{digit_COUNT[사용량++]="0123456789abcdef"[VALUE%latar_VALUE];VALUE/=latar_VALUE;}while(VALUE);
            if(음수표시)storan_penimbal[item_COUNT++]='-';if(TYPE_bidang=='p'||(대체값&&latar_VALUE==16)){storan_penimbal[item_COUNT++]='0';storan_penimbal[item_COUNT++]='x';}
            for(int isi_VALUE=(int)사용량;kepersisan_VALUE>isi_VALUE&&item_COUNT<sizeof(storan_penimbal)-사용량;isi_VALUE++)storan_penimbal[item_COUNT++]='0';
            if(영값&&!왼쪽&&kepersisan_VALUE<0)while(너비>(int)(item_COUNT+사용량)&&item_COUNT<sizeof(storan_penimbal)-사용량)storan_penimbal[item_COUNT++]='0';
            while(사용량)storan_penimbal[item_COUNT++]=digit_COUNT[--사용량];
        }else{storan_penimbal[0]='?';item_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)item_COUNT){넣기(ukuran_data,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<item_COUNT;순번++)넣기(ukuran_data,용량한도,&현재위치,rentetan_data[순번]);while(왼쪽&&너비>(int)item_COUNT){넣기(ukuran_data,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)ukuran_data[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*ukuran_data,size_t 용량한도,const char*fail_pemasukan,...){va_list 첫째값;va_start(첫째값,fail_pemasukan);int 반환값=vsnprintf(ukuran_data,용량한도,fail_pemasukan,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*ukuran_data,const char*fail_pemasukan,...){va_list 첫째값;va_start(첫째값,fail_pemasukan);int 반환값=vsnprintf(ukuran_data,SIZE_MAX,fail_pemasukan,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*strim_VALUE,const char*fail_pemasukan,va_list 첫째값){char SECOND_VALUE[2048];int item_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),fail_pemasukan,첫째값);if(item_COUNT>2047)item_COUNT=2047;return fwrite(SECOND_VALUE,1,item_COUNT,strim_VALUE)==(size_t)item_COUNT?item_COUNT:-1;}
int fprintf(FILE*strim_VALUE,const char*fail_pemasukan,...){va_list 첫째값;va_start(첫째값,fail_pemasukan);int 반환값=vfprintf(strim_VALUE,fail_pemasukan,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*fail_pemasukan,...){va_list 첫째값;va_start(첫째값,fail_pemasukan);int 반환값=vfprintf(stdout,fail_pemasukan,첫째값);va_end(첫째값);return 반환값;}
