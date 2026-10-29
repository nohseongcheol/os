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
static int galat;
int *__errno_location(void){return &galat;}
void exit(int Status_VALUE){사용자호출(6,Status_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *cek_ekspresi,const char *berkas,unsigned baris_masukan,const char *metode_entri_nama){fprintf(stderr,"cc assertion: %s %s:%u %s\n",cek_ekspresi,berkas,baris_masukan,metode_entri_nama);exit(1);}
size_t strlen(const char*string_data){const char*data_posisi=string_data;while(*data_posisi)data_posisi++;return data_posisi-string_data;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t item_COUNT){while(item_COUNT--){unsigned char koordinat_x=*첫째값++,Y_koordinat=*SECOND_VALUE++;if(koordinat_x!=Y_koordinat)return koordinat_x-Y_koordinat;if(!koordinat_x)return 0;}return 0;}
char *strcpy(char*tujuan_data,const char*string_data){char*반환값=tujuan_data;while((*tujuan_data++=*string_data++)){}return 반환값;}
char *strchr(const char*string_data,int kode_karakter){do{if(*string_data==(char)kode_karakter)return (char*)string_data;}while(*string_data++);return 0;}
char *strrchr(const char*string_data,int kode_karakter){const char*반환값=0;do{if(*string_data==(char)kode_karakter)반환값=string_data;}while(*string_data++);return (char*)반환값;}
char *strstr(const char*string_data,const char*Terminal_entri){size_t item_COUNT=strlen(Terminal_entri);for(;*string_data;string_data++)if(!strncmp(string_data,Terminal_entri,item_COUNT))return (char*)string_data;return item_COUNT?0:(char*)string_data;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t item_COUNT){const unsigned char*koordinat_x=첫째값,*Y_koordinat=SECOND_VALUE;while(item_COUNT--){if(*koordinat_x!=*Y_koordinat)return *koordinat_x-*Y_koordinat;koordinat_x++;Y_koordinat++;}return 0;}
void *memmove(void*tujuan_data,const void*string_data,size_t item_COUNT){unsigned char*koordinat_x=tujuan_data;const unsigned char*Y_koordinat=string_data;if(koordinat_x<Y_koordinat){for(size_t 순번=0;순번<item_COUNT;순번++)koordinat_x[순번]=Y_koordinat[순번];}else while(item_COUNT){item_COUNT--;koordinat_x[item_COUNT]=Y_koordinat[item_COUNT];}return tujuan_data;}
static unsigned char alokasi_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct blok_data {size_t Ukuran;struct blok_data*Berikutnya_item;int 남은공간;int 채울크기;uint64_t perataan_unit;} blok_data;
static blok_data *첫항목;
void free(void*data_posisi){if(!data_posisi)return;blok_data*SECOND_VALUE=(blok_data*)data_posisi-1;SECOND_VALUE->남은공간=1;for(blok_data*Berikutnya_OFFSET=첫항목;Berikutnya_OFFSET&&Berikutnya_OFFSET->Berikutnya_item;){if(Berikutnya_OFFSET->남은공간&&Berikutnya_OFFSET->Berikutnya_item->남은공간){Berikutnya_OFFSET->Ukuran+=sizeof(blok_data)+Berikutnya_OFFSET->Berikutnya_item->Ukuran;Berikutnya_OFFSET->Berikutnya_item=Berikutnya_OFFSET->Berikutnya_item->Berikutnya_item;}else Berikutnya_OFFSET=Berikutnya_OFFSET->Berikutnya_item;}}
void *realloc(void*data_posisi,size_t item_COUNT){
    if(!item_COUNT){free(data_posisi);return 0;}if(item_COUNT>sizeof(alokasi_Arena)-sizeof(blok_data))return 0;item_COUNT=(item_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(blok_data*)alokasi_Arena;첫항목->Ukuran=sizeof(alokasi_Arena)-sizeof(blok_data);첫항목->남은공간=1;첫항목->Berikutnya_item=0;}
    blok_data*이전=data_posisi?(blok_data*)data_posisi-1:0;if(이전&&이전->Ukuran>=item_COUNT)return data_posisi;
    for(blok_data*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Berikutnya_item)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Ukuran>=item_COUNT){
        if(SECOND_VALUE->Ukuran>=item_COUNT+sizeof(blok_data)+16){blok_data*나머지부분=(blok_data*)((unsigned char*)(SECOND_VALUE+1)+item_COUNT);나머지부분->Ukuran=SECOND_VALUE->Ukuran-item_COUNT-sizeof(blok_data);나머지부분->Berikutnya_item=SECOND_VALUE->Berikutnya_item;나머지부분->남은공간=1;SECOND_VALUE->Berikutnya_item=나머지부분;SECOND_VALUE->Ukuran=item_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,data_posisi,이전->Ukuran);free(data_posisi);}return 반환값;
    }galat=12;return 0;
}
void *malloc(size_t item_COUNT){return realloc(0,item_COUNT);}
void *calloc(size_t item_COUNT,size_t string_data){if(string_data&&item_COUNT>SIZE_MAX/string_data)return 0;void*data_posisi=malloc(item_COUNT*string_data);if(data_posisi)memset(data_posisi,0,item_COUNT*string_data);return data_posisi;}
unsigned long long strtoull(const char*string_data,char**mengakhiri_OFFSET,int wallpaper_VALUE){
    const char*Mulai_OFFSET=string_data;while(*string_data==' '||(*string_data>=9&&*string_data<=13))string_data++;int 음수여부=0;if(*string_data=='-'||*string_data=='+')음수여부=*string_data++=='-';
    if((!wallpaper_VALUE||wallpaper_VALUE==16)&&string_data[0]=='0'&&(string_data[1]=='x'||string_data[1]=='X')){wallpaper_VALUE=16;string_data+=2;}if(!wallpaper_VALUE)wallpaper_VALUE=*string_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kode_karakter=*string_data,tujuan_data=kode_karakter>='0'&&kode_karakter<='9'?kode_karakter-'0':kode_karakter>='a'&&kode_karakter<='z'?kode_karakter-'a'+10:kode_karakter>='A'&&kode_karakter<='Z'?kode_karakter-'A'+10:99;if(tujuan_data>=(unsigned)wallpaper_VALUE)break;하나라도=1;string_data++;if(임시값>(~0ull-tujuan_data)/(unsigned)wallpaper_VALUE){임시값=~0ull;galat=34;}else 임시값=임시값*wallpaper_VALUE+tujuan_data;}
    if(mengakhiri_OFFSET)*mengakhiri_OFFSET=(char*)(하나라도?string_data:Mulai_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*string_data,char**보조항목,int SECOND_VALUE){return strtoull(string_data,보조항목,SECOND_VALUE);}
long strtol(const char*string_data,char**보조항목,int SECOND_VALUE){return (long)strtoull(string_data,보조항목,SECOND_VALUE);}
int atoi(const char*string_data){return (int)strtol(string_data,0,10);}
long double ldexpl(long double koordinat_x,int item_COUNT){while(item_COUNT>0){koordinat_x*=2;item_COUNT--;}while(item_COUNT<0){koordinat_x/=2;item_COUNT++;}return koordinat_x;}
long double strtold(const char*string_data,char**mengakhiri_OFFSET){
    const char*Mulai_OFFSET=string_data;while(*string_data==' '||(*string_data>=9&&*string_data<=13))string_data++;int 음수여부=0;if(*string_data=='-'||*string_data=='+')음수여부=*string_data++=='-';
    int wallpaper_VALUE=10;if(string_data[0]=='0'&&(string_data[1]=='x'||string_data[1]=='X')){wallpaper_VALUE=16;string_data+=2;}long double 임시값=0,skala=1;int 소수부=0,하나라도=0;
    for(;;){int kode_karakter=*string_data,tujuan_data=kode_karakter>='0'&&kode_karakter<='9'?kode_karakter-'0':kode_karakter>='a'&&kode_karakter<='f'?kode_karakter-'a'+10:kode_karakter>='A'&&kode_karakter<='F'?kode_karakter-'A'+10:99;
        if(kode_karakter=='.'&&!소수부){소수부=1;string_data++;continue;}if(tujuan_data>=wallpaper_VALUE)break;하나라도=1;string_data++;임시값=임시값*wallpaper_VALUE+tujuan_data;if(소수부)skala*=wallpaper_VALUE;
    }임시값/=skala;
    if((wallpaper_VALUE==10&&(*string_data=='e'||*string_data=='E'))||(wallpaper_VALUE==16&&(*string_data=='p'||*string_data=='P'))){const char*show_VALUE=string_data++;int 빼기=0;if(*string_data=='-'||*string_data=='+')빼기=*string_data++=='-';int item_COUNT=0,entri_COUNT=0;while(*string_data>='0'&&*string_data<='9'){entri_COUNT++;if(item_COUNT<20000)item_COUNT=item_COUNT*10+*string_data-'0';string_data++;}if(!entri_COUNT)string_data=show_VALUE;else{long double faktor=wallpaper_VALUE==16?2:10;while(item_COUNT-->0&&item_COUNT<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(mengakhiri_OFFSET)*mengakhiri_OFFSET=(char*)(하나라도?string_data:Mulai_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*string_data,char**보조항목){return (double)strtold(string_data,보조항목);}float strtof(const char*string_data,char**보조항목){return (float)strtold(string_data,보조항목);}
void qsort(void*wallpaper_VALUE,size_t item_COUNT,size_t Ukuran,int(*Bandingkan)(const void*,const void*)){
    unsigned char*data_posisi=wallpaper_VALUE;for(size_t 순번=1;순번<item_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Bandingkan(data_posisi+(안쪽순번-1)*Ukuran,data_posisi+안쪽순번*Ukuran)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Ukuran;셋째순번++){unsigned char kode_karakter=data_posisi[(안쪽순번-1)*Ukuran+셋째순번];data_posisi[(안쪽순번-1)*Ukuran+셋째순번]=data_posisi[안쪽순번*Ukuran+셋째순번];data_posisi[안쪽순번*Ukuran+셋째순번]=kode_karakter;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t posisi;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *item_COUNT){*item_COUNT=출력크기;return 출력결과;}
int open(const char*Nama_2,int konfigurasi_Background_Intelligent_Transfer_Service,...){
    if(!strcmp(Nama_2,"/@cc-output")){if(출력열림){galat=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Nama_2,번역기자원들[순번].Nama_2)){
        if(konfigurasi_Background_Intelligent_Transfer_Service&3){galat=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].posisi=0;return 128+안쪽순번;}galat=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nama_2,konfigurasi_Background_Intelligent_Transfer_Service,0,0,0,0);if(반환값<0){galat=-반환값;return -1;}return 반환값;
}
int close(int file_handel){if(file_handel==100){출력열림=0;return 0;}if(file_handel>=128&&file_handel<152){열림[file_handel-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,file_handel,0,0,0,0,0);if(반환값<0){galat=-반환값;return -1;}return 0;}
long read(int file_handel,void*data,size_t item_COUNT){
    if(file_handel>=128&&file_handel<152&&열림[file_handel-128].사용량){int 순번=file_handel-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Ukuran-열림[순번].posisi;if(item_COUNT>왼쪽)item_COUNT=왼쪽;memcpy(data,반환값->data+열림[순번].posisi,item_COUNT);열림[순번].posisi+=item_COUNT;return item_COUNT;}
    intptr_t 반환값=사용자호출(2,file_handel,(uintptr_t)data,item_COUNT,0,0,0);if(반환값<0){galat=-반환값;return -1;}return 반환값;
}
long write(int file_handel,const void*data,size_t item_COUNT){
    if(file_handel==100){if(item_COUNT>sizeof(출력결과)-출력위치){galat=28;return -1;}memcpy(출력결과+출력위치,data,item_COUNT);출력위치+=item_COUNT;if(출력크기<출력위치)출력크기=출력위치;return item_COUNT;}
    intptr_t 반환값=사용자호출(1,file_handel,(uintptr_t)data,item_COUNT,0,0,0);if(반환값<0){galat=-반환값;return -1;}return 반환값;
}
long lseek(int file_handel,long OFFSET_VALUE,int 기준점){
    if(file_handel==100){long data_posisi=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(data_posisi<0||(size_t)data_posisi>sizeof(출력결과)){galat=22;return -1;}출력위치=data_posisi;return data_posisi;}
    if(file_handel>=128&&file_handel<152&&열림[file_handel-128].사용량){int 순번=file_handel-128;long data_posisi=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].posisi:번역기자원들[열림[순번].LOOKUP_INDEX].Ukuran);if(data_posisi<0||(size_t)data_posisi>번역기자원들[열림[순번].LOOKUP_INDEX].Ukuran){galat=22;return -1;}열림[순번].posisi=data_posisi;return data_posisi;}
    intptr_t 반환값=사용자호출(5,file_handel,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){galat=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nama_2){intptr_t 반환값=사용자호출(11,(uintptr_t)Nama_2,0,0,0,0,0);if(반환값<0){galat=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nama_2,char*KR_data){if(!KR_data){KR_data=malloc(strlen(Nama_2)+1);if(!KR_data)return 0;}return strcpy(KR_data,Nama_2);}
char *getcwd(char*data_posisi,size_t item_COUNT){if(item_COUNT<2){galat=34;return 0;}data_posisi[0]='/';data_posisi[1]=0;return data_posisi;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_entri){time_t 임시값=0;if(Terminal_entri)*Terminal_entri=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_entri){(void)Terminal_entri;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Aliran[18]={{1,0,1},{2,0,1}};FILE*stdout=&Aliran[0],*stderr=&Aliran[1];
FILE*fdopen(int file_handel,const char*metode_MODE){(void)metode_MODE;for(unsigned 순번=2;순번<18;순번++)if(!Aliran[순번].사용량){Aliran[순번].사용량=1;Aliran[순번].galat=0;Aliran[순번].file_handel=file_handel;return &Aliran[순번];}galat=24;return 0;}
int fflush(FILE*file_entri){return file_entri&&file_entri->galat?-1:0;}
int fclose(FILE*file_entri){int 반환값=close(file_entri->file_handel);if(file_entri->galat)반환값=-1;file_entri->사용량=0;return 반환값;}
size_t fwrite(const void*data_posisi,size_t string_data,size_t item_COUNT,FILE*file_entri){if(!string_data)return 0;if(item_COUNT>SIZE_MAX/string_data){file_entri->galat=1;return 0;}long 반환값=write(file_entri->file_handel,data_posisi,string_data*item_COUNT);if(반환값<0){file_entri->galat=1;return 0;}return (size_t)반환값/string_data;}
int fputc(int kode_karakter,FILE*file_entri){unsigned char SECOND_VALUE=kode_karakter;return fwrite(&SECOND_VALUE,1,1,file_entri)==1?SECOND_VALUE:EOF;}
int fputs(const char*string_data,FILE*file_entri){return fwrite(string_data,1,strlen(string_data),file_entri)==strlen(string_data)?0:EOF;}
static void 넣기(char*KR_data,size_t 용량한도,size_t*saat_ini_posisi,char kode_karakter){if(*saat_ini_posisi+1<용량한도)KR_data[*saat_ini_posisi]=kode_karakter;(*saat_ini_posisi)++;}
int vsnprintf(char*KR_data,size_t 용량한도,const char*format,va_list 가변인수){
    size_t saat_ini_posisi=0;while(*format){if(*format!='%'){넣기(KR_data,용량한도,&saat_ini_posisi,*format++);continue;}format++;
        int 왼쪽=0,nilai_nol=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')nilai_nol=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,presisi_VALUE=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;presisi_VALUE=0;if(*format=='*'){presisi_VALUE=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')presisi_VALUE=presisi_VALUE*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char TYPE_area=*format?*format++:0,penyimpanan_buffer[80];const char*string_data=penyimpanan_buffer;size_t item_COUNT=0;
        if(TYPE_area=='s'){string_data=va_arg(가변인수,const char*);if(!string_data)string_data="(null)";item_COUNT=strlen(string_data);if(presisi_VALUE>=0&&item_COUNT>(size_t)presisi_VALUE)item_COUNT=presisi_VALUE;}
        else if(TYPE_area=='c'){penyimpanan_buffer[0]=va_arg(가변인수,int);item_COUNT=1;}
        else if(TYPE_area=='%'){penyimpanan_buffer[0]='%';item_COUNT=1;}
        else if(TYPE_area=='d'||TYPE_area=='i'||TYPE_area=='u'||TYPE_area=='x'||TYPE_area=='X'||TYPE_area=='o'||TYPE_area=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_area=='d'||TYPE_area=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_area=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned wallpaper_VALUE=TYPE_area=='x'||TYPE_area=='X'||TYPE_area=='p'?16:TYPE_area=='o'?8:10;char angka_COUNT[64];unsigned 사용량=0;
            do{angka_COUNT[사용량++]="0123456789abcdef"[VALUE%wallpaper_VALUE];VALUE/=wallpaper_VALUE;}while(VALUE);
            if(음수표시)penyimpanan_buffer[item_COUNT++]='-';if(TYPE_area=='p'||(대체값&&wallpaper_VALUE==16)){penyimpanan_buffer[item_COUNT++]='0';penyimpanan_buffer[item_COUNT++]='x';}
            for(int isi_VALUE=(int)사용량;presisi_VALUE>isi_VALUE&&item_COUNT<sizeof(penyimpanan_buffer)-사용량;isi_VALUE++)penyimpanan_buffer[item_COUNT++]='0';
            if(nilai_nol&&!왼쪽&&presisi_VALUE<0)while(너비>(int)(item_COUNT+사용량)&&item_COUNT<sizeof(penyimpanan_buffer)-사용량)penyimpanan_buffer[item_COUNT++]='0';
            while(사용량)penyimpanan_buffer[item_COUNT++]=angka_COUNT[--사용량];
        }else{penyimpanan_buffer[0]='?';item_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)item_COUNT){넣기(KR_data,용량한도,&saat_ini_posisi,' ');너비--;}
        for(size_t 순번=0;순번<item_COUNT;순번++)넣기(KR_data,용량한도,&saat_ini_posisi,string_data[순번]);while(왼쪽&&너비>(int)item_COUNT){넣기(KR_data,용량한도,&saat_ini_posisi,' ');너비--;}
    }if(용량한도)KR_data[saat_ini_posisi<용량한도?saat_ini_posisi:용량한도-1]=0;return saat_ini_posisi;
}
int snprintf(char*KR_data,size_t 용량한도,const char*file_entri,...){va_list 첫째값;va_start(첫째값,file_entri);int 반환값=vsnprintf(KR_data,용량한도,file_entri,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_data,const char*file_entri,...){va_list 첫째값;va_start(첫째값,file_entri);int 반환값=vsnprintf(KR_data,SIZE_MAX,file_entri,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*file_entri,va_list 첫째값){char SECOND_VALUE[2048];int item_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),file_entri,첫째값);if(item_COUNT>2047)item_COUNT=2047;return fwrite(SECOND_VALUE,1,item_COUNT,Stream_VALUE)==(size_t)item_COUNT?item_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*file_entri,...){va_list 첫째값;va_start(첫째값,file_entri);int 반환값=vfprintf(Stream_VALUE,file_entri,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*file_entri,...){va_list 첫째값;va_start(첫째값,file_entri);int 반환값=vfprintf(stdout,file_entri,첫째값);va_end(첫째값);return 반환값;}
