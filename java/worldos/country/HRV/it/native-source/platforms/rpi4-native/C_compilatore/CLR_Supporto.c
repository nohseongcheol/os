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
static int errore;
int *__errno_location(void){return &errore;}
void exit(int Stato_VALORE){사용자호출(6,Stato_VALORE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *assegno_espressione,const char *file,unsigned riga_di_ingresso,const char *metodo_voce_nome){fprintf(stderr,"cc assertion: %s %s:%u %s\n",assegno_espressione,file,riga_di_ingresso,metodo_voce_nome);exit(1);}
size_t strlen(const char*stringa_dati){const char*dati_funzione=stringa_dati;while(*dati_funzione)dati_funzione++;return dati_funzione-stringa_dati;}
int strcmp(const char*첫째값,const char*SECONDO_VALORE){while(*첫째값&&*첫째값==*SECONDO_VALORE){첫째값++;SECONDO_VALORE++;}return (unsigned char)*첫째값-(unsigned char)*SECONDO_VALORE;}
int strncmp(const char*첫째값,const char*SECONDO_VALORE,size_t articolo_CONTA_NUMERI){while(articolo_CONTA_NUMERI--){unsigned char coordinata_x=*첫째값++,Y_coordinata=*SECONDO_VALORE++;if(coordinata_x!=Y_coordinata)return coordinata_x-Y_coordinata;if(!coordinata_x)return 0;}return 0;}
char *strcpy(char*meta_dati,const char*stringa_dati){char*반환값=meta_dati;while((*meta_dati++=*stringa_dati++)){}return 반환값;}
char *strchr(const char*stringa_dati,int punto_di_codice){do{if(*stringa_dati==(char)punto_di_codice)return (char*)stringa_dati;}while(*stringa_dati++);return 0;}
char *strrchr(const char*stringa_dati,int punto_di_codice){const char*반환값=0;do{if(*stringa_dati==(char)punto_di_codice)반환값=stringa_dati;}while(*stringa_dati++);return (char*)반환값;}
char *strstr(const char*stringa_dati,const char*Terminale_voce){size_t articolo_CONTA_NUMERI=strlen(Terminale_voce);for(;*stringa_dati;stringa_dati++)if(!strncmp(stringa_dati,Terminale_voce,articolo_CONTA_NUMERI))return (char*)stringa_dati;return articolo_CONTA_NUMERI?0:(char*)stringa_dati;}
int memcmp(const void*첫째값,const void*SECONDO_VALORE,size_t articolo_CONTA_NUMERI){const unsigned char*coordinata_x=첫째값,*Y_coordinata=SECONDO_VALORE;while(articolo_CONTA_NUMERI--){if(*coordinata_x!=*Y_coordinata)return *coordinata_x-*Y_coordinata;coordinata_x++;Y_coordinata++;}return 0;}
void *memmove(void*meta_dati,const void*stringa_dati,size_t articolo_CONTA_NUMERI){unsigned char*coordinata_x=meta_dati;const unsigned char*Y_coordinata=stringa_dati;if(coordinata_x<Y_coordinata){for(size_t 순번=0;순번<articolo_CONTA_NUMERI;순번++)coordinata_x[순번]=Y_coordinata[순번];}else while(articolo_CONTA_NUMERI){articolo_CONTA_NUMERI--;coordinata_x[articolo_CONTA_NUMERI]=Y_coordinata[articolo_CONTA_NUMERI];}return meta_dati;}
static unsigned char allocazione_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct blocco_di_dati {size_t Dimensione;struct blocco_di_dati*Avanti_articolo;int 남은공간;int riempimento;uint64_t ancoraggio_unità;} blocco_di_dati;
static blocco_di_dati *첫항목;
void free(void*dati_funzione){if(!dati_funzione)return;blocco_di_dati*SECONDO_VALORE=(blocco_di_dati*)dati_funzione-1;SECONDO_VALORE->남은공간=1;for(blocco_di_dati*Avanti_SCARTO=첫항목;Avanti_SCARTO&&Avanti_SCARTO->Avanti_articolo;){if(Avanti_SCARTO->남은공간&&Avanti_SCARTO->Avanti_articolo->남은공간){Avanti_SCARTO->Dimensione+=sizeof(blocco_di_dati)+Avanti_SCARTO->Avanti_articolo->Dimensione;Avanti_SCARTO->Avanti_articolo=Avanti_SCARTO->Avanti_articolo->Avanti_articolo;}else Avanti_SCARTO=Avanti_SCARTO->Avanti_articolo;}}
void *realloc(void*dati_funzione,size_t articolo_CONTA_NUMERI){
    if(!articolo_CONTA_NUMERI){free(dati_funzione);return 0;}if(articolo_CONTA_NUMERI>sizeof(allocazione_Arena)-sizeof(blocco_di_dati))return 0;articolo_CONTA_NUMERI=(articolo_CONTA_NUMERI+15)&~(size_t)15;
    if(!첫항목){첫항목=(blocco_di_dati*)allocazione_Arena;첫항목->Dimensione=sizeof(allocazione_Arena)-sizeof(blocco_di_dati);첫항목->남은공간=1;첫항목->Avanti_articolo=0;}
    blocco_di_dati*Indietro_articolo=dati_funzione?(blocco_di_dati*)dati_funzione-1:0;if(Indietro_articolo&&Indietro_articolo->Dimensione>=articolo_CONTA_NUMERI)return dati_funzione;
    for(blocco_di_dati*SECONDO_VALORE=첫항목;SECONDO_VALORE;SECONDO_VALORE=SECONDO_VALORE->Avanti_articolo)if(SECONDO_VALORE->남은공간&&SECONDO_VALORE->Dimensione>=articolo_CONTA_NUMERI){
        if(SECONDO_VALORE->Dimensione>=articolo_CONTA_NUMERI+sizeof(blocco_di_dati)+16){blocco_di_dati*나머지부분=(blocco_di_dati*)((unsigned char*)(SECONDO_VALORE+1)+articolo_CONTA_NUMERI);나머지부분->Dimensione=SECONDO_VALORE->Dimensione-articolo_CONTA_NUMERI-sizeof(blocco_di_dati);나머지부분->Avanti_articolo=SECONDO_VALORE->Avanti_articolo;나머지부분->남은공간=1;SECONDO_VALORE->Avanti_articolo=나머지부분;SECONDO_VALORE->Dimensione=articolo_CONTA_NUMERI;}
        SECONDO_VALORE->남은공간=0;void*반환값=SECONDO_VALORE+1;if(Indietro_articolo){memcpy(반환값,dati_funzione,Indietro_articolo->Dimensione);free(dati_funzione);}return 반환값;
    }errore=12;return 0;
}
void *malloc(size_t articolo_CONTA_NUMERI){return realloc(0,articolo_CONTA_NUMERI);}
void *calloc(size_t articolo_CONTA_NUMERI,size_t stringa_dati){if(stringa_dati&&articolo_CONTA_NUMERI>SIZE_MAX/stringa_dati)return 0;void*dati_funzione=malloc(articolo_CONTA_NUMERI*stringa_dati);if(dati_funzione)memset(dati_funzione,0,articolo_CONTA_NUMERI*stringa_dati);return dati_funzione;}
unsigned long long strtoull(const char*stringa_dati,char**chiudere_SCARTO,int sfondo_VALORE){
    const char*START_SCARTO=stringa_dati;while(*stringa_dati==' '||(*stringa_dati>=9&&*stringa_dati<=13))stringa_dati++;int reparto_IT_negativo=0;if(*stringa_dati=='-'||*stringa_dati=='+')reparto_IT_negativo=*stringa_dati++=='-';
    if((!sfondo_VALORE||sfondo_VALORE==16)&&stringa_dati[0]=='0'&&(stringa_dati[1]=='x'||stringa_dati[1]=='X')){sfondo_VALORE=16;stringa_dati+=2;}if(!sfondo_VALORE)sfondo_VALORE=*stringa_dati=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned punto_di_codice=*stringa_dati,meta_dati=punto_di_codice>='0'&&punto_di_codice<='9'?punto_di_codice-'0':punto_di_codice>='a'&&punto_di_codice<='z'?punto_di_codice-'a'+10:punto_di_codice>='A'&&punto_di_codice<='Z'?punto_di_codice-'A'+10:99;if(meta_dati>=(unsigned)sfondo_VALORE)break;하나라도=1;stringa_dati++;if(임시값>(~0ull-meta_dati)/(unsigned)sfondo_VALORE){임시값=~0ull;errore=34;}else 임시값=임시값*sfondo_VALORE+meta_dati;}
    if(chiudere_SCARTO)*chiudere_SCARTO=(char*)(하나라도?stringa_dati:START_SCARTO);return reparto_IT_negativo?0-임시값:임시값;
}
unsigned long strtoul(const char*stringa_dati,char**보조항목,int SECONDO_VALORE){return strtoull(stringa_dati,보조항목,SECONDO_VALORE);}
long strtol(const char*stringa_dati,char**보조항목,int SECONDO_VALORE){return (long)strtoull(stringa_dati,보조항목,SECONDO_VALORE);}
int atoi(const char*stringa_dati){return (int)strtol(stringa_dati,0,10);}
long double ldexpl(long double coordinata_x,int articolo_CONTA_NUMERI){while(articolo_CONTA_NUMERI>0){coordinata_x*=2;articolo_CONTA_NUMERI--;}while(articolo_CONTA_NUMERI<0){coordinata_x/=2;articolo_CONTA_NUMERI++;}return coordinata_x;}
long double strtold(const char*stringa_dati,char**chiudere_SCARTO){
    const char*START_SCARTO=stringa_dati;while(*stringa_dati==' '||(*stringa_dati>=9&&*stringa_dati<=13))stringa_dati++;int reparto_IT_negativo=0;if(*stringa_dati=='-'||*stringa_dati=='+')reparto_IT_negativo=*stringa_dati++=='-';
    int sfondo_VALORE=10;if(stringa_dati[0]=='0'&&(stringa_dati[1]=='x'||stringa_dati[1]=='X')){sfondo_VALORE=16;stringa_dati+=2;}long double 임시값=0,scala=1;int 소수부=0,하나라도=0;
    for(;;){int punto_di_codice=*stringa_dati,meta_dati=punto_di_codice>='0'&&punto_di_codice<='9'?punto_di_codice-'0':punto_di_codice>='a'&&punto_di_codice<='f'?punto_di_codice-'a'+10:punto_di_codice>='A'&&punto_di_codice<='F'?punto_di_codice-'A'+10:99;
        if(punto_di_codice=='.'&&!소수부){소수부=1;stringa_dati++;continue;}if(meta_dati>=sfondo_VALORE)break;하나라도=1;stringa_dati++;임시값=임시값*sfondo_VALORE+meta_dati;if(소수부)scala*=sfondo_VALORE;
    }임시값/=scala;
    if((sfondo_VALORE==10&&(*stringa_dati=='e'||*stringa_dati=='E'))||(sfondo_VALORE==16&&(*stringa_dati=='p'||*stringa_dati=='P'))){const char*mostrare_VALORE=stringa_dati++;int 빼기=0;if(*stringa_dati=='-'||*stringa_dati=='+')빼기=*stringa_dati++=='-';int articolo_CONTA_NUMERI=0,voce_CONTA_NUMERI=0;while(*stringa_dati>='0'&&*stringa_dati<='9'){voce_CONTA_NUMERI++;if(articolo_CONTA_NUMERI<20000)articolo_CONTA_NUMERI=articolo_CONTA_NUMERI*10+*stringa_dati-'0';stringa_dati++;}if(!voce_CONTA_NUMERI)stringa_dati=mostrare_VALORE;else{long double fattore=sfondo_VALORE==16?2:10;while(articolo_CONTA_NUMERI-->0&&articolo_CONTA_NUMERI<200000)임시값=빼기?임시값/fattore:임시값*fattore;}}
    if(chiudere_SCARTO)*chiudere_SCARTO=(char*)(하나라도?stringa_dati:START_SCARTO);return reparto_IT_negativo?-임시값:임시값;
}
double strtod(const char*stringa_dati,char**보조항목){return (double)strtold(stringa_dati,보조항목);}float strtof(const char*stringa_dati,char**보조항목){return (float)strtold(stringa_dati,보조항목);}
void qsort(void*sfondo_VALORE,size_t articolo_CONTA_NUMERI,size_t Dimensione,int(*Confronta)(const void*,const void*)){
    unsigned char*dati_funzione=sfondo_VALORE;for(size_t 순번=1;순번<articolo_CONTA_NUMERI;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Confronta(dati_funzione+(안쪽순번-1)*Dimensione,dati_funzione+안쪽순번*Dimensione)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Dimensione;셋째순번++){unsigned char punto_di_codice=dati_funzione[(안쪽순번-1)*Dimensione+셋째순번];dati_funzione[(안쪽순번-1)*Dimensione+셋째순번]=dati_funzione[안쪽순번*Dimensione+셋째순번];dati_funzione[안쪽순번*Dimensione+셋째순번]=punto_di_codice;}
}
static struct {int 사용량,CERCA_INDICE;size_t posizione;} 열림[24];
static unsigned char output[32768];static size_t output_ridimensionare,output_funzione;static int output_aperto;
const unsigned char *C_output(size_t *articolo_CONTA_NUMERI){*articolo_CONTA_NUMERI=output_ridimensionare;return output;}
int open(const char*Nome,int configurazione_BITS,...){
    if(!strcmp(Nome,"/@cc-output")){if(output_aperto){errore=16;return -1;}output_aperto=1;output_ridimensionare=output_funzione=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(compilatore_Risorse)/sizeof(compilatore_Risorse[0]);순번++)if(!strcmp(Nome,compilatore_Risorse[순번].Nome)){
        if(configurazione_BITS&3){errore=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].CERCA_INDICE=순번;열림[안쪽순번].posizione=0;return 128+안쪽순번;}errore=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nome,configurazione_BITS,0,0,0,0);if(반환값<0){errore=-반환값;return -1;}return 반환값;
}
int close(int handle_di_file){if(handle_di_file==100){output_aperto=0;return 0;}if(handle_di_file>=128&&handle_di_file<152){열림[handle_di_file-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,handle_di_file,0,0,0,0,0);if(반환값<0){errore=-반환값;return -1;}return 0;}
long read(int handle_di_file,void*dati,size_t articolo_CONTA_NUMERI){
    if(handle_di_file>=128&&handle_di_file<152&&열림[handle_di_file-128].사용량){int 순번=handle_di_file-128;const compilatore_risorsa*반환값=&compilatore_Risorse[열림[순번].CERCA_INDICE];size_t 왼쪽=반환값->Dimensione-열림[순번].posizione;if(articolo_CONTA_NUMERI>왼쪽)articolo_CONTA_NUMERI=왼쪽;memcpy(dati,반환값->dati+열림[순번].posizione,articolo_CONTA_NUMERI);열림[순번].posizione+=articolo_CONTA_NUMERI;return articolo_CONTA_NUMERI;}
    intptr_t 반환값=사용자호출(2,handle_di_file,(uintptr_t)dati,articolo_CONTA_NUMERI,0,0,0);if(반환값<0){errore=-반환값;return -1;}return 반환값;
}
long write(int handle_di_file,const void*dati,size_t articolo_CONTA_NUMERI){
    if(handle_di_file==100){if(articolo_CONTA_NUMERI>sizeof(output)-output_funzione){errore=28;return -1;}memcpy(output+output_funzione,dati,articolo_CONTA_NUMERI);output_funzione+=articolo_CONTA_NUMERI;if(output_ridimensionare<output_funzione)output_ridimensionare=output_funzione;return articolo_CONTA_NUMERI;}
    intptr_t 반환값=사용자호출(1,handle_di_file,(uintptr_t)dati,articolo_CONTA_NUMERI,0,0,0);if(반환값<0){errore=-반환값;return -1;}return 반환값;
}
long lseek(int handle_di_file,long SCARTO_VALORE,int cercare_origine){
    if(handle_di_file==100){long dati_funzione=SCARTO_VALORE+(cercare_origine==0?0:cercare_origine==1?output_funzione:output_ridimensionare);if(dati_funzione<0||(size_t)dati_funzione>sizeof(output)){errore=22;return -1;}output_funzione=dati_funzione;return dati_funzione;}
    if(handle_di_file>=128&&handle_di_file<152&&열림[handle_di_file-128].사용량){int 순번=handle_di_file-128;long dati_funzione=SCARTO_VALORE+(cercare_origine==0?0:cercare_origine==1?열림[순번].posizione:compilatore_Risorse[열림[순번].CERCA_INDICE].Dimensione);if(dati_funzione<0||(size_t)dati_funzione>compilatore_Risorse[열림[순번].CERCA_INDICE].Dimensione){errore=22;return -1;}열림[순번].posizione=dati_funzione;return dati_funzione;}
    intptr_t 반환값=사용자호출(5,handle_di_file,SCARTO_VALORE,cercare_origine,0,0,0);if(반환값<0){errore=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nome){intptr_t 반환값=사용자호출(11,(uintptr_t)Nome,0,0,0,0,0);if(반환값<0){errore=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nome,char*KR_dati){if(!KR_dati){KR_dati=malloc(strlen(Nome)+1);if(!KR_dati)return 0;}return strcpy(KR_dati,Nome);}
char *getcwd(char*dati_funzione,size_t articolo_CONTA_NUMERI){if(articolo_CONTA_NUMERI<2){errore=34;return 0;}dati_funzione[0]='/';dati_funzione[1]=0;return dati_funzione;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminale_voce){time_t 임시값=0;if(Terminale_voce)*Terminale_voce=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminale_voce){(void)Terminale_voce;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Flussi[18]={{1,0,1},{2,0,1}};FILE*stdout=&Flussi[0],*stderr=&Flussi[1];
FILE*fdopen(int handle_di_file,const char*metodo_MODA){(void)metodo_MODA;for(unsigned 순번=2;순번<18;순번++)if(!Flussi[순번].사용량){Flussi[순번].사용량=1;Flussi[순번].errore=0;Flussi[순번].handle_di_file=handle_di_file;return &Flussi[순번];}errore=24;return 0;}
int fflush(FILE*File_voce){return File_voce&&File_voce->errore?-1:0;}
int fclose(FILE*File_voce){int 반환값=close(File_voce->handle_di_file);if(File_voce->errore)반환값=-1;File_voce->사용량=0;return 반환값;}
size_t fwrite(const void*dati_funzione,size_t stringa_dati,size_t articolo_CONTA_NUMERI,FILE*File_voce){if(!stringa_dati)return 0;if(articolo_CONTA_NUMERI>SIZE_MAX/stringa_dati){File_voce->errore=1;return 0;}long 반환값=write(File_voce->handle_di_file,dati_funzione,stringa_dati*articolo_CONTA_NUMERI);if(반환값<0){File_voce->errore=1;return 0;}return (size_t)반환값/stringa_dati;}
int fputc(int punto_di_codice,FILE*File_voce){unsigned char SECONDO_VALORE=punto_di_codice;return fwrite(&SECONDO_VALORE,1,1,File_voce)==1?SECONDO_VALORE:EOF;}
int fputs(const char*stringa_dati,FILE*File_voce){return fwrite(stringa_dati,1,strlen(stringa_dati),File_voce)==strlen(stringa_dati)?0:EOF;}
static void 넣기(char*KR_dati,size_t 용량한도,size_t*Regolari_funzione,char punto_di_codice){if(*Regolari_funzione+1<용량한도)KR_dati[*Regolari_funzione]=punto_di_codice;(*Regolari_funzione)++;}
int vsnprintf(char*KR_dati,size_t 용량한도,const char*formato,va_list 가변인수){
    size_t Regolari_funzione=0;while(*formato){if(*formato!='%'){넣기(KR_dati,용량한도,&Regolari_funzione,*formato++);continue;}formato++;
        int 왼쪽=0,valore_uguale_a_zero=0,대체값=0;while(*formato=='-'||*formato=='0'||*formato=='#'||*formato=='+'||*formato==' '){if(*formato=='-')왼쪽=1;if(*formato=='0')valore_uguale_a_zero=1;if(*formato=='#')대체값=1;formato++;}
        int 너비=0,precisione_VALORE=-1;if(*formato=='*'){너비=va_arg(가변인수,int);formato++;}else while(*formato>='0'&&*formato<='9')너비=너비*10+*formato++-'0';
        if(*formato=='.'){formato++;precisione_VALORE=0;if(*formato=='*'){precisione_VALORE=va_arg(가변인수,int);formato++;}else while(*formato>='0'&&*formato<='9')precisione_VALORE=precisione_VALORE*10+*formato++-'0';}
        int carattere_wide=0;while(*formato=='l'||*formato=='z'||*formato=='t'||*formato=='j'||*formato=='h'){if(*formato!='h')carattere_wide=1;formato++;}
        char TIPO_area=*formato?*formato++:0,buffer_Memoria[80];const char*stringa_dati=buffer_Memoria;size_t articolo_CONTA_NUMERI=0;
        if(TIPO_area=='s'){stringa_dati=va_arg(가변인수,const char*);if(!stringa_dati)stringa_dati="(null)";articolo_CONTA_NUMERI=strlen(stringa_dati);if(precisione_VALORE>=0&&articolo_CONTA_NUMERI>(size_t)precisione_VALORE)articolo_CONTA_NUMERI=precisione_VALORE;}
        else if(TIPO_area=='c'){buffer_Memoria[0]=va_arg(가변인수,int);articolo_CONTA_NUMERI=1;}
        else if(TIPO_area=='%'){buffer_Memoria[0]='%';articolo_CONTA_NUMERI=1;}
        else if(TIPO_area=='d'||TIPO_area=='i'||TIPO_area=='u'||TIPO_area=='x'||TIPO_area=='X'||TIPO_area=='o'||TIPO_area=='p'){
            unsigned long long VALORE;int negativo=0;
            if(TIPO_area=='d'||TIPO_area=='i'){long long 임시값=carattere_wide?va_arg(가변인수,long long):va_arg(가변인수,int);negativo=임시값<0;VALORE=negativo?0-(unsigned long long)임시값:임시값;}
            else VALORE=TIPO_area=='p'?(uintptr_t)va_arg(가변인수,void*):carattere_wide?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned sfondo_VALORE=TIPO_area=='x'||TIPO_area=='X'||TIPO_area=='p'?16:TIPO_area=='o'?8:10;char cifra_CONTA_NUMERI[64];unsigned 사용량=0;
            do{cifra_CONTA_NUMERI[사용량++]="0123456789abcdef"[VALORE%sfondo_VALORE];VALORE/=sfondo_VALORE;}while(VALORE);
            if(negativo)buffer_Memoria[articolo_CONTA_NUMERI++]='-';if(TIPO_area=='p'||(대체값&&sfondo_VALORE==16)){buffer_Memoria[articolo_CONTA_NUMERI++]='0';buffer_Memoria[articolo_CONTA_NUMERI++]='x';}
            for(int Riempi_VALORE=(int)사용량;precisione_VALORE>Riempi_VALORE&&articolo_CONTA_NUMERI<sizeof(buffer_Memoria)-사용량;Riempi_VALORE++)buffer_Memoria[articolo_CONTA_NUMERI++]='0';
            if(valore_uguale_a_zero&&!왼쪽&&precisione_VALORE<0)while(너비>(int)(articolo_CONTA_NUMERI+사용량)&&articolo_CONTA_NUMERI<sizeof(buffer_Memoria)-사용량)buffer_Memoria[articolo_CONTA_NUMERI++]='0';
            while(사용량)buffer_Memoria[articolo_CONTA_NUMERI++]=cifra_CONTA_NUMERI[--사용량];
        }else{buffer_Memoria[0]='?';articolo_CONTA_NUMERI=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)articolo_CONTA_NUMERI){넣기(KR_dati,용량한도,&Regolari_funzione,' ');너비--;}
        for(size_t 순번=0;순번<articolo_CONTA_NUMERI;순번++)넣기(KR_dati,용량한도,&Regolari_funzione,stringa_dati[순번]);while(왼쪽&&너비>(int)articolo_CONTA_NUMERI){넣기(KR_dati,용량한도,&Regolari_funzione,' ');너비--;}
    }if(용량한도)KR_dati[Regolari_funzione<용량한도?Regolari_funzione:용량한도-1]=0;return Regolari_funzione;
}
int snprintf(char*KR_dati,size_t 용량한도,const char*File_voce,...){va_list 첫째값;va_start(첫째값,File_voce);int 반환값=vsnprintf(KR_dati,용량한도,File_voce,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_dati,const char*File_voce,...){va_list 첫째값;va_start(첫째값,File_voce);int 반환값=vsnprintf(KR_dati,SIZE_MAX,File_voce,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALORE,const char*File_voce,va_list 첫째값){char SECONDO_VALORE[2048];int articolo_CONTA_NUMERI=vsnprintf(SECONDO_VALORE,sizeof(SECONDO_VALORE),File_voce,첫째값);if(articolo_CONTA_NUMERI>2047)articolo_CONTA_NUMERI=2047;return fwrite(SECONDO_VALORE,1,articolo_CONTA_NUMERI,Stream_VALORE)==(size_t)articolo_CONTA_NUMERI?articolo_CONTA_NUMERI:-1;}
int fprintf(FILE*Stream_VALORE,const char*File_voce,...){va_list 첫째값;va_start(첫째값,File_voce);int 반환값=vfprintf(Stream_VALORE,File_voce,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*File_voce,...){va_list 첫째값;va_start(첫째값,File_voce);int 반환값=vfprintf(stdout,File_voce,첫째값);va_end(첫째값);return 반환값;}
