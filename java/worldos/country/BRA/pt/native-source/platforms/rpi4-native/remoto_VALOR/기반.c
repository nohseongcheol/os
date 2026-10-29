/* kernel_VALOR 전용 할당기와 senha_VALOR 난수 공급. espaço_do_utilizador ELF의 libc와 별개이다. */
#include "criptografia_Suporte.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memória_bloco { size_t duração_VALOR; struct Memória_bloco *Avançar_item; int uso_VALOR; } Memória_bloco;
static unsigned char Memória_Arena[2*1024*1024] __attribute__((aligned(16)));
static Memória_bloco *첫조각;
void *alocar_remoto(size_t duração_VALOR) {
    if (!duração_VALOR || duração_VALOR>sizeof(Memória_Arena)-64) return 0;
    duração_VALOR=(duração_VALOR+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memória_Arena;첫조각->duração_VALOR=sizeof(Memória_Arena)-32;}
    for(Memória_bloco *fragmento_VALOR=첫조각;fragmento_VALOR;fragmento_VALOR=fragmento_VALOR->Avançar_item)if(!fragmento_VALOR->uso_VALOR&&fragmento_VALOR->duração_VALOR>=duração_VALOR){
        if(fragmento_VALOR->duração_VALOR>=duração_VALOR+64){Memória_bloco *새조각=(void*)((char*)fragmento_VALOR+32+duração_VALOR);
            새조각->duração_VALOR=fragmento_VALOR->duração_VALOR-duração_VALOR-32;새조각->Avançar_item=fragmento_VALOR->Avançar_item;새조각->uso_VALOR=0;fragmento_VALOR->Avançar_item=새조각;fragmento_VALOR->duração_VALOR=duração_VALOR;}
        fragmento_VALOR->uso_VALOR=1;return(char*)fragmento_VALOR+32;
    }return 0;
}
void lançar_remoto(void *Endereço) {
    if(!Endereço)return;Memória_bloco *fragmento_VALOR=(void*)((char*)Endereço-32);
    volatile unsigned char *지움=Endereço;for(size_t 순번=0;순번<fragmento_VALOR->duração_VALOR;순번++)지움[순번]=0;
    fragmento_VALOR->uso_VALOR=0;
    for(fragmento_VALOR=첫조각;fragmento_VALOR&&fragmento_VALOR->Avançar_item;){if(!fragmento_VALOR->uso_VALOR&&!fragmento_VALOR->Avançar_item->uso_VALOR){fragmento_VALOR->duração_VALOR+=32+fragmento_VALOR->Avançar_item->duração_VALOR;fragmento_VALOR->Avançar_item=fragmento_VALOR->Avançar_item->Avançar_item;}else fragmento_VALOR=fragmento_VALOR->Avançar_item;}
}
void *원격재할당(void *Endereço,size_t duração_VALOR){
    if(!Endereço)return alocar_remoto(duração_VALOR);if(!duração_VALOR){lançar_remoto(Endereço);return 0;}
    Memória_bloco *fragmento_VALOR=(void*)((char*)Endereço-32);void *새주소=alocar_remoto(duração_VALOR);
    if(새주소){memcpy(새주소,Endereço,duração_VALOR<fragmento_VALOR->duração_VALOR?duração_VALOR:fragmento_VALOR->duração_VALOR);lançar_remoto(Endereço);}return 새주소;
}
int strcmp(const char *가,const char *SEGUNDO_operando){while(*가&&*가==*SEGUNDO_operando){가++;SEGUNDO_operando++;}return(unsigned char)*가-(unsigned char)*SEGUNDO_operando;}
char *strchr(const char *Word_SMS,int caractere_VALOR){for(;;Word_SMS++){if(*Word_SMS==(char)caractere_VALOR)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t duração_VALOR=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,duração_VALOR))return(char*)Word_SMS;return duração_VALOR?0:(char*)Word_SMS;}
char *strncpy(char *destino_VALOR,const char *원본,size_t duração_VALOR){size_t 순번=0;for(;순번<duração_VALOR&&원본[순번];순번++)destino_VALOR[순번]=원본[순번];for(;순번<duração_VALOR;순번++)destino_VALOR[순번]=0;return destino_VALOR;}
char *strncat(char *destino_VALOR,const char *원본,size_t duração_VALOR){char *끝=destino_VALOR+strlen(destino_VALOR);while(duração_VALOR--&&*원본)*끝++=*원본++;*끝=0;return destino_VALOR;}
int strncasecmp(const char *가,const char *SEGUNDO_operando,size_t duração_VALOR){while(duração_VALOR--){unsigned 첫글자=*가++,SEGUNDO_caractere=*SEGUNDO_operando++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SEGUNDO_caractere>='A'&&SEGUNDO_caractere<='Z')SEGUNDO_caractere+=32;if(첫글자!=SEGUNDO_caractere)return(int)첫글자-(int)SEGUNDO_caractere;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SEGUNDO_operando){return strncasecmp(가,SEGUNDO_operando,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *delimitador_VALOR,char **Avançar_item){if(!Word_SMS)Word_SMS=*Avançar_item;while(*Word_SMS&&strchr(delimitador_VALOR,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Avançar_item=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(delimitador_VALOR,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Avançar_item=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALOR) {
    const char *códigoFonte=Word_SMS;unsigned long VALOR=0;int negativo_VALOR=0,estouro_VALOR=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')negativo_VALOR=*Word_SMS++=='-';
    if((BASE_VALOR==0||BASE_VALOR==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALOR=16;Word_SMS+=2;}
    if(!BASE_VALOR)BASE_VALOR=*Word_SMS=='0'?8:10;
    if(BASE_VALOR<2||BASE_VALOR>36){if(끝)*끝=(char*)códigoFonte;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned caractere_VALOR=(unsigned char)*Word_SMS;
        unsigned número=caractere_VALOR>='0'&&caractere_VALOR<='9'?caractere_VALOR-'0':caractere_VALOR>='a'&&caractere_VALOR<='z'?caractere_VALOR-'a'+10:caractere_VALOR>='A'&&caractere_VALOR<='Z'?caractere_VALOR-'A'+10:36;
        if(número>=(unsigned)BASE_VALOR)break;
        if(VALOR>(~0ul-número)/(unsigned)BASE_VALOR)estouro_VALOR=1;
        if(!estouro_VALOR)VALOR=VALOR*(unsigned)BASE_VALOR+número;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?códigoFonte:Word_SMS);
    return estouro_VALOR?~0ul:negativo_VALOR?0ul-VALOR:VALOR;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int semente_Estado;
void remoto_resumo(const void *dados, size_t duração_VALOR, unsigned char resultado[32]) {
    br_sha256_context contexto_VALOR;
    br_sha256_init(&contexto_VALOR); br_sha256_update(&contexto_VALOR, dados, duração_VALOR); br_sha256_out(&contexto_VALOR, resultado);
    memset(&contexto_VALOR, 0, sizeof(contexto_VALOR));
}
#define 난수저장기(posição) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(posição)))
int remoto_aleatório(unsigned char *destino_VALOR,unsigned duração_VALOR){
    if(!semente_Estado){volatile unsigned char *dados=(void*)0x01ff0000ul;const char *favorito_VALOR="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=dados[순번]^(unsigned char)favorito_VALOR[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=dados[8+순번];for(unsigned 순번=0;순번<40;순번++)dados[순번]=0;semente_Estado=2;}
        else {semente_Estado=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(semente_Estado==2){while(duração_VALOR){unsigned char Avançar_item[32],entrada_VALOR[33];memcpy(entrada_VALOR,모의씨앗,32);entrada_VALOR[32]=0;remoto_resumo(entrada_VALOR,33,Avançar_item);
        entrada_VALOR[32]=1;remoto_resumo(entrada_VALOR,33,모의씨앗);memset(entrada_VALOR,0,33);
        unsigned número=duração_VALOR<32?duração_VALOR:32;memcpy(destino_VALOR,Avançar_item,número);memset(Avançar_item,0,32);destino_VALOR+=número;duração_VALOR-=número;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(duração_VALOR){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALOR=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&duração_VALOR;순번++,duração_VALOR--){*destino_VALOR++=VALOR&255;VALOR>>=8;}}
    return 0;
}
