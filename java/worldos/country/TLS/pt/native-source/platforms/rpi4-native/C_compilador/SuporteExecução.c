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
static int erro;
int *__errno_location(void){return &erro;}
void exit(int Estado_VALOR){사용자호출(6,Estado_VALOR,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *cheque_expressão,const char *ficheiro,unsigned linha_de_entrada,const char *método_entrada_nome){fprintf(stderr,"cc assertion: %s %s:%u %s\n",cheque_expressão,ficheiro,linha_de_entrada,método_entrada_nome);exit(1);}
size_t strlen(const char*cadeia_dados){const char*dados_cargo=cadeia_dados;while(*dados_cargo)dados_cargo++;return dados_cargo-cadeia_dados;}
int strcmp(const char*첫째값,const char*SEGUNDO_VALOR){while(*첫째값&&*첫째값==*SEGUNDO_VALOR){첫째값++;SEGUNDO_VALOR++;}return (unsigned char)*첫째값-(unsigned char)*SEGUNDO_VALOR;}
int strncmp(const char*첫째값,const char*SEGUNDO_VALOR,size_t item_CONT_NÚM){while(item_CONT_NÚM--){unsigned char coordenada_X=*첫째값++,Y_coordenada=*SEGUNDO_VALOR++;if(coordenada_X!=Y_coordenada)return coordenada_X-Y_coordenada;if(!coordenada_X)return 0;}return 0;}
char *strcpy(char*destino_dados,const char*cadeia_dados){char*반환값=destino_dados;while((*destino_dados++=*cadeia_dados++)){}return 반환값;}
char *strchr(const char*cadeia_dados,int ponto_de_código){do{if(*cadeia_dados==(char)ponto_de_código)return (char*)cadeia_dados;}while(*cadeia_dados++);return 0;}
char *strrchr(const char*cadeia_dados,int ponto_de_código){const char*반환값=0;do{if(*cadeia_dados==(char)ponto_de_código)반환값=cadeia_dados;}while(*cadeia_dados++);return (char*)반환값;}
char *strstr(const char*cadeia_dados,const char*Terminal_entrada){size_t item_CONT_NÚM=strlen(Terminal_entrada);for(;*cadeia_dados;cadeia_dados++)if(!strncmp(cadeia_dados,Terminal_entrada,item_CONT_NÚM))return (char*)cadeia_dados;return item_CONT_NÚM?0:(char*)cadeia_dados;}
int memcmp(const void*첫째값,const void*SEGUNDO_VALOR,size_t item_CONT_NÚM){const unsigned char*coordenada_X=첫째값,*Y_coordenada=SEGUNDO_VALOR;while(item_CONT_NÚM--){if(*coordenada_X!=*Y_coordenada)return *coordenada_X-*Y_coordenada;coordenada_X++;Y_coordenada++;}return 0;}
void *memmove(void*destino_dados,const void*cadeia_dados,size_t item_CONT_NÚM){unsigned char*coordenada_X=destino_dados;const unsigned char*Y_coordenada=cadeia_dados;if(coordenada_X<Y_coordenada){for(size_t 순번=0;순번<item_CONT_NÚM;순번++)coordenada_X[순번]=Y_coordenada[순번];}else while(item_CONT_NÚM){item_CONT_NÚM--;coordenada_X[item_CONT_NÚM]=Y_coordenada[item_CONT_NÚM];}return destino_dados;}
static unsigned char alocação_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct bloco_de_dados {size_t Tamanho;struct bloco_de_dados*Avançar_item;int 남은공간;int preenchimento;uint64_t alinhamento_lição;} bloco_de_dados;
static bloco_de_dados *첫항목;
void free(void*dados_cargo){if(!dados_cargo)return;bloco_de_dados*SEGUNDO_VALOR=(bloco_de_dados*)dados_cargo-1;SEGUNDO_VALOR->남은공간=1;for(bloco_de_dados*Avançar_DESLOC=첫항목;Avançar_DESLOC&&Avançar_DESLOC->Avançar_item;){if(Avançar_DESLOC->남은공간&&Avançar_DESLOC->Avançar_item->남은공간){Avançar_DESLOC->Tamanho+=sizeof(bloco_de_dados)+Avançar_DESLOC->Avançar_item->Tamanho;Avançar_DESLOC->Avançar_item=Avançar_DESLOC->Avançar_item->Avançar_item;}else Avançar_DESLOC=Avançar_DESLOC->Avançar_item;}}
void *realloc(void*dados_cargo,size_t item_CONT_NÚM){
    if(!item_CONT_NÚM){free(dados_cargo);return 0;}if(item_CONT_NÚM>sizeof(alocação_Arena)-sizeof(bloco_de_dados))return 0;item_CONT_NÚM=(item_CONT_NÚM+15)&~(size_t)15;
    if(!첫항목){첫항목=(bloco_de_dados*)alocação_Arena;첫항목->Tamanho=sizeof(alocação_Arena)-sizeof(bloco_de_dados);첫항목->남은공간=1;첫항목->Avançar_item=0;}
    bloco_de_dados*Anterior_item=dados_cargo?(bloco_de_dados*)dados_cargo-1:0;if(Anterior_item&&Anterior_item->Tamanho>=item_CONT_NÚM)return dados_cargo;
    for(bloco_de_dados*SEGUNDO_VALOR=첫항목;SEGUNDO_VALOR;SEGUNDO_VALOR=SEGUNDO_VALOR->Avançar_item)if(SEGUNDO_VALOR->남은공간&&SEGUNDO_VALOR->Tamanho>=item_CONT_NÚM){
        if(SEGUNDO_VALOR->Tamanho>=item_CONT_NÚM+sizeof(bloco_de_dados)+16){bloco_de_dados*나머지부분=(bloco_de_dados*)((unsigned char*)(SEGUNDO_VALOR+1)+item_CONT_NÚM);나머지부분->Tamanho=SEGUNDO_VALOR->Tamanho-item_CONT_NÚM-sizeof(bloco_de_dados);나머지부분->Avançar_item=SEGUNDO_VALOR->Avançar_item;나머지부분->남은공간=1;SEGUNDO_VALOR->Avançar_item=나머지부분;SEGUNDO_VALOR->Tamanho=item_CONT_NÚM;}
        SEGUNDO_VALOR->남은공간=0;void*반환값=SEGUNDO_VALOR+1;if(Anterior_item){memcpy(반환값,dados_cargo,Anterior_item->Tamanho);free(dados_cargo);}return 반환값;
    }erro=12;return 0;
}
void *malloc(size_t item_CONT_NÚM){return realloc(0,item_CONT_NÚM);}
void *calloc(size_t item_CONT_NÚM,size_t cadeia_dados){if(cadeia_dados&&item_CONT_NÚM>SIZE_MAX/cadeia_dados)return 0;void*dados_cargo=malloc(item_CONT_NÚM*cadeia_dados);if(dados_cargo)memset(dados_cargo,0,item_CONT_NÚM*cadeia_dados);return dados_cargo;}
unsigned long long strtoull(const char*cadeia_dados,char**encerrar_DESLOC,int Tela_de_fundo_VALOR){
    const char*START_DESLOC=cadeia_dados;while(*cadeia_dados==' '||(*cadeia_dados>=9&&*cadeia_dados<=13))cadeia_dados++;int TI_negativo=0;if(*cadeia_dados=='-'||*cadeia_dados=='+')TI_negativo=*cadeia_dados++=='-';
    if((!Tela_de_fundo_VALOR||Tela_de_fundo_VALOR==16)&&cadeia_dados[0]=='0'&&(cadeia_dados[1]=='x'||cadeia_dados[1]=='X')){Tela_de_fundo_VALOR=16;cadeia_dados+=2;}if(!Tela_de_fundo_VALOR)Tela_de_fundo_VALOR=*cadeia_dados=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned ponto_de_código=*cadeia_dados,destino_dados=ponto_de_código>='0'&&ponto_de_código<='9'?ponto_de_código-'0':ponto_de_código>='a'&&ponto_de_código<='z'?ponto_de_código-'a'+10:ponto_de_código>='A'&&ponto_de_código<='Z'?ponto_de_código-'A'+10:99;if(destino_dados>=(unsigned)Tela_de_fundo_VALOR)break;하나라도=1;cadeia_dados++;if(임시값>(~0ull-destino_dados)/(unsigned)Tela_de_fundo_VALOR){임시값=~0ull;erro=34;}else 임시값=임시값*Tela_de_fundo_VALOR+destino_dados;}
    if(encerrar_DESLOC)*encerrar_DESLOC=(char*)(하나라도?cadeia_dados:START_DESLOC);return TI_negativo?0-임시값:임시값;
}
unsigned long strtoul(const char*cadeia_dados,char**보조항목,int SEGUNDO_VALOR){return strtoull(cadeia_dados,보조항목,SEGUNDO_VALOR);}
long strtol(const char*cadeia_dados,char**보조항목,int SEGUNDO_VALOR){return (long)strtoull(cadeia_dados,보조항목,SEGUNDO_VALOR);}
int atoi(const char*cadeia_dados){return (int)strtol(cadeia_dados,0,10);}
long double ldexpl(long double coordenada_X,int item_CONT_NÚM){while(item_CONT_NÚM>0){coordenada_X*=2;item_CONT_NÚM--;}while(item_CONT_NÚM<0){coordenada_X/=2;item_CONT_NÚM++;}return coordenada_X;}
long double strtold(const char*cadeia_dados,char**encerrar_DESLOC){
    const char*START_DESLOC=cadeia_dados;while(*cadeia_dados==' '||(*cadeia_dados>=9&&*cadeia_dados<=13))cadeia_dados++;int TI_negativo=0;if(*cadeia_dados=='-'||*cadeia_dados=='+')TI_negativo=*cadeia_dados++=='-';
    int Tela_de_fundo_VALOR=10;if(cadeia_dados[0]=='0'&&(cadeia_dados[1]=='x'||cadeia_dados[1]=='X')){Tela_de_fundo_VALOR=16;cadeia_dados+=2;}long double 임시값=0,escala=1;int 소수부=0,하나라도=0;
    for(;;){int ponto_de_código=*cadeia_dados,destino_dados=ponto_de_código>='0'&&ponto_de_código<='9'?ponto_de_código-'0':ponto_de_código>='a'&&ponto_de_código<='f'?ponto_de_código-'a'+10:ponto_de_código>='A'&&ponto_de_código<='F'?ponto_de_código-'A'+10:99;
        if(ponto_de_código=='.'&&!소수부){소수부=1;cadeia_dados++;continue;}if(destino_dados>=Tela_de_fundo_VALOR)break;하나라도=1;cadeia_dados++;임시값=임시값*Tela_de_fundo_VALOR+destino_dados;if(소수부)escala*=Tela_de_fundo_VALOR;
    }임시값/=escala;
    if((Tela_de_fundo_VALOR==10&&(*cadeia_dados=='e'||*cadeia_dados=='E'))||(Tela_de_fundo_VALOR==16&&(*cadeia_dados=='p'||*cadeia_dados=='P'))){const char*mostrar_VALOR=cadeia_dados++;int 빼기=0;if(*cadeia_dados=='-'||*cadeia_dados=='+')빼기=*cadeia_dados++=='-';int item_CONT_NÚM=0,entrada_CONT_NÚM_8f7753a1=0;while(*cadeia_dados>='0'&&*cadeia_dados<='9'){entrada_CONT_NÚM_8f7753a1++;if(item_CONT_NÚM<20000)item_CONT_NÚM=item_CONT_NÚM*10+*cadeia_dados-'0';cadeia_dados++;}if(!entrada_CONT_NÚM_8f7753a1)cadeia_dados=mostrar_VALOR;else{long double fator=Tela_de_fundo_VALOR==16?2:10;while(item_CONT_NÚM-->0&&item_CONT_NÚM<200000)임시값=빼기?임시값/fator:임시값*fator;}}
    if(encerrar_DESLOC)*encerrar_DESLOC=(char*)(하나라도?cadeia_dados:START_DESLOC);return TI_negativo?-임시값:임시값;
}
double strtod(const char*cadeia_dados,char**보조항목){return (double)strtold(cadeia_dados,보조항목);}float strtof(const char*cadeia_dados,char**보조항목){return (float)strtold(cadeia_dados,보조항목);}
void qsort(void*Tela_de_fundo_VALOR,size_t item_CONT_NÚM,size_t Tamanho,int(*Comparar)(const void*,const void*)){
    unsigned char*dados_cargo=Tela_de_fundo_VALOR;for(size_t 순번=1;순번<item_CONT_NÚM;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Comparar(dados_cargo+(안쪽순번-1)*Tamanho,dados_cargo+안쪽순번*Tamanho)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Tamanho;셋째순번++){unsigned char ponto_de_código=dados_cargo[(안쪽순번-1)*Tamanho+셋째순번];dados_cargo[(안쪽순번-1)*Tamanho+셋째순번]=dados_cargo[안쪽순번*Tamanho+셋째순번];dados_cargo[안쪽순번*Tamanho+셋째순번]=ponto_de_código;}
}
static struct {int 사용량,PROC_ÍNDICE;size_t posição;} 열림[24];
static unsigned char saída[32768];static size_t saída_dimensionar,saída_cargo;static int saída_abrir;
const unsigned char *C_saída(size_t *item_CONT_NÚM){*item_CONT_NÚM=saída_dimensionar;return saída;}
int open(const char*Nome,int Configuração_BITS,...){
    if(!strcmp(Nome,"/@cc-output")){if(saída_abrir){erro=16;return -1;}saída_abrir=1;saída_dimensionar=saída_cargo=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(compilador_Recursos)/sizeof(compilador_Recursos[0]);순번++)if(!strcmp(Nome,compilador_Recursos[순번].Nome)){
        if(Configuração_BITS&3){erro=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].PROC_ÍNDICE=순번;열림[안쪽순번].posição=0;return 128+안쪽순번;}erro=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nome,Configuração_BITS,0,0,0,0);if(반환값<0){erro=-반환값;return -1;}return 반환값;
}
int close(int identificador_de_arquivo){if(identificador_de_arquivo==100){saída_abrir=0;return 0;}if(identificador_de_arquivo>=128&&identificador_de_arquivo<152){열림[identificador_de_arquivo-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,identificador_de_arquivo,0,0,0,0,0);if(반환값<0){erro=-반환값;return -1;}return 0;}
long read(int identificador_de_arquivo,void*dados,size_t item_CONT_NÚM){
    if(identificador_de_arquivo>=128&&identificador_de_arquivo<152&&열림[identificador_de_arquivo-128].사용량){int 순번=identificador_de_arquivo-128;const compilador_recurso*반환값=&compilador_Recursos[열림[순번].PROC_ÍNDICE];size_t 왼쪽=반환값->Tamanho-열림[순번].posição;if(item_CONT_NÚM>왼쪽)item_CONT_NÚM=왼쪽;memcpy(dados,반환값->dados+열림[순번].posição,item_CONT_NÚM);열림[순번].posição+=item_CONT_NÚM;return item_CONT_NÚM;}
    intptr_t 반환값=사용자호출(2,identificador_de_arquivo,(uintptr_t)dados,item_CONT_NÚM,0,0,0);if(반환값<0){erro=-반환값;return -1;}return 반환값;
}
long write(int identificador_de_arquivo,const void*dados,size_t item_CONT_NÚM){
    if(identificador_de_arquivo==100){if(item_CONT_NÚM>sizeof(saída)-saída_cargo){erro=28;return -1;}memcpy(saída+saída_cargo,dados,item_CONT_NÚM);saída_cargo+=item_CONT_NÚM;if(saída_dimensionar<saída_cargo)saída_dimensionar=saída_cargo;return item_CONT_NÚM;}
    intptr_t 반환값=사용자호출(1,identificador_de_arquivo,(uintptr_t)dados,item_CONT_NÚM,0,0,0);if(반환값<0){erro=-반환값;return -1;}return 반환값;
}
long lseek(int identificador_de_arquivo,long DESLOC_VALOR,int busca_origem){
    if(identificador_de_arquivo==100){long dados_cargo=DESLOC_VALOR+(busca_origem==0?0:busca_origem==1?saída_cargo:saída_dimensionar);if(dados_cargo<0||(size_t)dados_cargo>sizeof(saída)){erro=22;return -1;}saída_cargo=dados_cargo;return dados_cargo;}
    if(identificador_de_arquivo>=128&&identificador_de_arquivo<152&&열림[identificador_de_arquivo-128].사용량){int 순번=identificador_de_arquivo-128;long dados_cargo=DESLOC_VALOR+(busca_origem==0?0:busca_origem==1?열림[순번].posição:compilador_Recursos[열림[순번].PROC_ÍNDICE].Tamanho);if(dados_cargo<0||(size_t)dados_cargo>compilador_Recursos[열림[순번].PROC_ÍNDICE].Tamanho){erro=22;return -1;}열림[순번].posição=dados_cargo;return dados_cargo;}
    intptr_t 반환값=사용자호출(5,identificador_de_arquivo,DESLOC_VALOR,busca_origem,0,0,0);if(반환값<0){erro=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nome){intptr_t 반환값=사용자호출(11,(uintptr_t)Nome,0,0,0,0,0);if(반환값<0){erro=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nome,char*RC_dados){if(!RC_dados){RC_dados=malloc(strlen(Nome)+1);if(!RC_dados)return 0;}return strcpy(RC_dados,Nome);}
char *getcwd(char*dados_cargo,size_t item_CONT_NÚM){if(item_CONT_NÚM<2){erro=34;return 0;}dados_cargo[0]='/';dados_cargo[1]=0;return dados_cargo;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_entrada){time_t 임시값=0;if(Terminal_entrada)*Terminal_entrada=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_entrada){(void)Terminal_entrada;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Fluxos[18]={{1,0,1},{2,0,1}};FILE*stdout=&Fluxos[0],*stderr=&Fluxos[1];
FILE*fdopen(int identificador_de_arquivo,const char*método_MODO){(void)método_MODO;for(unsigned 순번=2;순번<18;순번++)if(!Fluxos[순번].사용량){Fluxos[순번].사용량=1;Fluxos[순번].erro=0;Fluxos[순번].identificador_de_arquivo=identificador_de_arquivo;return &Fluxos[순번];}erro=24;return 0;}
int fflush(FILE*Arquivo_entrada){return Arquivo_entrada&&Arquivo_entrada->erro?-1:0;}
int fclose(FILE*Arquivo_entrada){int 반환값=close(Arquivo_entrada->identificador_de_arquivo);if(Arquivo_entrada->erro)반환값=-1;Arquivo_entrada->사용량=0;return 반환값;}
size_t fwrite(const void*dados_cargo,size_t cadeia_dados,size_t item_CONT_NÚM,FILE*Arquivo_entrada){if(!cadeia_dados)return 0;if(item_CONT_NÚM>SIZE_MAX/cadeia_dados){Arquivo_entrada->erro=1;return 0;}long 반환값=write(Arquivo_entrada->identificador_de_arquivo,dados_cargo,cadeia_dados*item_CONT_NÚM);if(반환값<0){Arquivo_entrada->erro=1;return 0;}return (size_t)반환값/cadeia_dados;}
int fputc(int ponto_de_código,FILE*Arquivo_entrada){unsigned char SEGUNDO_VALOR=ponto_de_código;return fwrite(&SEGUNDO_VALOR,1,1,Arquivo_entrada)==1?SEGUNDO_VALOR:EOF;}
int fputs(const char*cadeia_dados,FILE*Arquivo_entrada){return fwrite(cadeia_dados,1,strlen(cadeia_dados),Arquivo_entrada)==strlen(cadeia_dados)?0:EOF;}
static void 넣기(char*RC_dados,size_t 용량한도,size_t*em_dia_cargo,char ponto_de_código){if(*em_dia_cargo+1<용량한도)RC_dados[*em_dia_cargo]=ponto_de_código;(*em_dia_cargo)++;}
int vsnprintf(char*RC_dados,size_t 용량한도,const char*formato,va_list 가변인수){
    size_t em_dia_cargo=0;while(*formato){if(*formato!='%'){넣기(RC_dados,용량한도,&em_dia_cargo,*formato++);continue;}formato++;
        int 왼쪽=0,valor_zero=0,대체값=0;while(*formato=='-'||*formato=='0'||*formato=='#'||*formato=='+'||*formato==' '){if(*formato=='-')왼쪽=1;if(*formato=='0')valor_zero=1;if(*formato=='#')대체값=1;formato++;}
        int 너비=0,precisão_VALOR=-1;if(*formato=='*'){너비=va_arg(가변인수,int);formato++;}else while(*formato>='0'&&*formato<='9')너비=너비*10+*formato++-'0';
        if(*formato=='.'){formato++;precisão_VALOR=0;if(*formato=='*'){precisão_VALOR=va_arg(가변인수,int);formato++;}else while(*formato>='0'&&*formato<='9')precisão_VALOR=precisão_VALOR*10+*formato++-'0';}
        int caractere_largo=0;while(*formato=='l'||*formato=='z'||*formato=='t'||*formato=='j'||*formato=='h'){if(*formato!='h')caractere_largo=1;formato++;}
        char TIPO_área=*formato?*formato++:0,armazenamento_em_buffer[80];const char*cadeia_dados=armazenamento_em_buffer;size_t item_CONT_NÚM=0;
        if(TIPO_área=='s'){cadeia_dados=va_arg(가변인수,const char*);if(!cadeia_dados)cadeia_dados="(null)";item_CONT_NÚM=strlen(cadeia_dados);if(precisão_VALOR>=0&&item_CONT_NÚM>(size_t)precisão_VALOR)item_CONT_NÚM=precisão_VALOR;}
        else if(TIPO_área=='c'){armazenamento_em_buffer[0]=va_arg(가변인수,int);item_CONT_NÚM=1;}
        else if(TIPO_área=='%'){armazenamento_em_buffer[0]='%';item_CONT_NÚM=1;}
        else if(TIPO_área=='d'||TIPO_área=='i'||TIPO_área=='u'||TIPO_área=='x'||TIPO_área=='X'||TIPO_área=='o'||TIPO_área=='p'){
            unsigned long long VALOR;int negativo=0;
            if(TIPO_área=='d'||TIPO_área=='i'){long long 임시값=caractere_largo?va_arg(가변인수,long long):va_arg(가변인수,int);negativo=임시값<0;VALOR=negativo?0-(unsigned long long)임시값:임시값;}
            else VALOR=TIPO_área=='p'?(uintptr_t)va_arg(가변인수,void*):caractere_largo?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Tela_de_fundo_VALOR=TIPO_área=='x'||TIPO_área=='X'||TIPO_área=='p'?16:TIPO_área=='o'?8:10;char dígito_CONT_NÚM[64];unsigned 사용량=0;
            do{dígito_CONT_NÚM[사용량++]="0123456789abcdef"[VALOR%Tela_de_fundo_VALOR];VALOR/=Tela_de_fundo_VALOR;}while(VALOR);
            if(negativo)armazenamento_em_buffer[item_CONT_NÚM++]='-';if(TIPO_área=='p'||(대체값&&Tela_de_fundo_VALOR==16)){armazenamento_em_buffer[item_CONT_NÚM++]='0';armazenamento_em_buffer[item_CONT_NÚM++]='x';}
            for(int preencher_VALOR=(int)사용량;precisão_VALOR>preencher_VALOR&&item_CONT_NÚM<sizeof(armazenamento_em_buffer)-사용량;preencher_VALOR++)armazenamento_em_buffer[item_CONT_NÚM++]='0';
            if(valor_zero&&!왼쪽&&precisão_VALOR<0)while(너비>(int)(item_CONT_NÚM+사용량)&&item_CONT_NÚM<sizeof(armazenamento_em_buffer)-사용량)armazenamento_em_buffer[item_CONT_NÚM++]='0';
            while(사용량)armazenamento_em_buffer[item_CONT_NÚM++]=dígito_CONT_NÚM[--사용량];
        }else{armazenamento_em_buffer[0]='?';item_CONT_NÚM=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)item_CONT_NÚM){넣기(RC_dados,용량한도,&em_dia_cargo,' ');너비--;}
        for(size_t 순번=0;순번<item_CONT_NÚM;순번++)넣기(RC_dados,용량한도,&em_dia_cargo,cadeia_dados[순번]);while(왼쪽&&너비>(int)item_CONT_NÚM){넣기(RC_dados,용량한도,&em_dia_cargo,' ');너비--;}
    }if(용량한도)RC_dados[em_dia_cargo<용량한도?em_dia_cargo:용량한도-1]=0;return em_dia_cargo;
}
int snprintf(char*RC_dados,size_t 용량한도,const char*Arquivo_entrada,...){va_list 첫째값;va_start(첫째값,Arquivo_entrada);int 반환값=vsnprintf(RC_dados,용량한도,Arquivo_entrada,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*RC_dados,const char*Arquivo_entrada,...){va_list 첫째값;va_start(첫째값,Arquivo_entrada);int 반환값=vsnprintf(RC_dados,SIZE_MAX,Arquivo_entrada,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*fluxo_VALOR,const char*Arquivo_entrada,va_list 첫째값){char SEGUNDO_VALOR[2048];int item_CONT_NÚM=vsnprintf(SEGUNDO_VALOR,sizeof(SEGUNDO_VALOR),Arquivo_entrada,첫째값);if(item_CONT_NÚM>2047)item_CONT_NÚM=2047;return fwrite(SEGUNDO_VALOR,1,item_CONT_NÚM,fluxo_VALOR)==(size_t)item_CONT_NÚM?item_CONT_NÚM:-1;}
int fprintf(FILE*fluxo_VALOR,const char*Arquivo_entrada,...){va_list 첫째값;va_start(첫째값,Arquivo_entrada);int 반환값=vfprintf(fluxo_VALOR,Arquivo_entrada,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Arquivo_entrada,...){va_list 첫째값;va_start(첫째값,Arquivo_entrada);int 반환값=vfprintf(stdout,Arquivo_entrada,첫째값);va_end(첫째값);return 반환값;}
