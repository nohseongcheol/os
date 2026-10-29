/* kernel_VALOR 전용 할당기와 contrasinal_VALOR 난수 공급. usuario ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memoria_bloquear { size_t duración_VALOR; struct Memoria_bloquear *Seguinte_elemento; int 사용; } Memoria_bloquear;
static unsigned char Memoria_Arena[2*1024*1024] __attribute__((aligned(16)));
static Memoria_bloquear *첫조각;
void *atribuír_remoto(size_t duración_VALOR) {
    if (!duración_VALOR || duración_VALOR>sizeof(Memoria_Arena)-64) return 0;
    duración_VALOR=(duración_VALOR+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memoria_Arena;첫조각->duración_VALOR=sizeof(Memoria_Arena)-32;}
    for(Memoria_bloquear *조각=첫조각;조각;조각=조각->Seguinte_elemento)if(!조각->사용&&조각->duración_VALOR>=duración_VALOR){
        if(조각->duración_VALOR>=duración_VALOR+64){Memoria_bloquear *새조각=(void*)((char*)조각+32+duración_VALOR);
            새조각->duración_VALOR=조각->duración_VALOR-duración_VALOR-32;새조각->Seguinte_elemento=조각->Seguinte_elemento;새조각->사용=0;조각->Seguinte_elemento=새조각;조각->duración_VALOR=duración_VALOR;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void liberar_remoto(void *ENDEREZO) {
    if(!ENDEREZO)return;Memoria_bloquear *조각=(void*)((char*)ENDEREZO-32);
    volatile unsigned char *지움=ENDEREZO;for(size_t 순번=0;순번<조각->duración_VALOR;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Seguinte_elemento;){if(!조각->사용&&!조각->Seguinte_elemento->사용){조각->duración_VALOR+=32+조각->Seguinte_elemento->duración_VALOR;조각->Seguinte_elemento=조각->Seguinte_elemento->Seguinte_elemento;}else 조각=조각->Seguinte_elemento;}
}
void *원격재할당(void *ENDEREZO,size_t duración_VALOR){
    if(!ENDEREZO)return atribuír_remoto(duración_VALOR);if(!duración_VALOR){liberar_remoto(ENDEREZO);return 0;}
    Memoria_bloquear *조각=(void*)((char*)ENDEREZO-32);void *새주소=atribuír_remoto(duración_VALOR);
    if(새주소){memcpy(새주소,ENDEREZO,duración_VALOR<조각->duración_VALOR?duración_VALOR:조각->duración_VALOR);liberar_remoto(ENDEREZO);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int carácter_VALOR){for(;;Word_SMS++){if(*Word_SMS==(char)carácter_VALOR)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t duración_VALOR=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,duración_VALOR))return(char*)Word_SMS;return duración_VALOR?0:(char*)Word_SMS;}
char *strncpy(char *destino_VALOR,const char *원본,size_t duración_VALOR){size_t 순번=0;for(;순번<duración_VALOR&&원본[순번];순번++)destino_VALOR[순번]=원본[순번];for(;순번<duración_VALOR;순번++)destino_VALOR[순번]=0;return destino_VALOR;}
char *strncat(char *destino_VALOR,const char *원본,size_t duración_VALOR){char *끝=destino_VALOR+strlen(destino_VALOR);while(duración_VALOR--&&*원본)*끝++=*원본++;*끝=0;return destino_VALOR;}
int strncasecmp(const char *가,const char *나,size_t duración_VALOR){while(duración_VALOR--){unsigned 첫글자=*가++,SEGUNDO_carácter=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SEGUNDO_carácter>='A'&&SEGUNDO_carácter<='Z')SEGUNDO_carácter+=32;if(첫글자!=SEGUNDO_carácter)return(int)첫글자-(int)SEGUNDO_carácter;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *delimitador_VALOR,char **Seguinte_elemento){if(!Word_SMS)Word_SMS=*Seguinte_elemento;while(*Word_SMS&&strchr(delimitador_VALOR,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Seguinte_elemento=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(delimitador_VALOR,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Seguinte_elemento=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALOR) {
    const char *FONTE=Word_SMS;unsigned long VALOR=0;int 음수=0,넘침=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALOR==0||BASE_VALOR==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALOR=16;Word_SMS+=2;}
    if(!BASE_VALOR)BASE_VALOR=*Word_SMS=='0'?8:10;
    if(BASE_VALOR<2||BASE_VALOR>36){if(끝)*끝=(char*)FONTE;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned carácter_VALOR=(unsigned char)*Word_SMS;
        unsigned 수=carácter_VALOR>='0'&&carácter_VALOR<='9'?carácter_VALOR-'0':carácter_VALOR>='a'&&carácter_VALOR<='z'?carácter_VALOR-'a'+10:carácter_VALOR>='A'&&carácter_VALOR<='Z'?carácter_VALOR-'A'+10:36;
        if(수>=(unsigned)BASE_VALOR)break;
        if(VALOR>(~0ul-수)/(unsigned)BASE_VALOR)넘침=1;
        if(!넘침)VALOR=VALOR*(unsigned)BASE_VALOR+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?FONTE:Word_SMS);
    return 넘침?~0ul:음수?0ul-VALOR:VALOR;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int fornecer_Estado;
void remoto_resumo(const void *datos, size_t duración_VALOR, unsigned char RESULTANTE[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, datos, duración_VALOR); br_sha256_out(&문맥, RESULTANTE);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(Posición) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Posición)))
int 원격난수(unsigned char *destino_VALOR,unsigned duración_VALOR){
    if(!fornecer_Estado){volatile unsigned char *datos=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=datos[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=datos[8+순번];for(unsigned 순번=0;순번<40;순번++)datos[순번]=0;fornecer_Estado=2;}
        else {fornecer_Estado=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(fornecer_Estado==2){while(duración_VALOR){unsigned char Seguinte_elemento[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;remoto_resumo(입력,33,Seguinte_elemento);
        입력[32]=1;remoto_resumo(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=duración_VALOR<32?duración_VALOR:32;memcpy(destino_VALOR,Seguinte_elemento,수);memset(Seguinte_elemento,0,32);destino_VALOR+=수;duración_VALOR-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(duración_VALOR){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALOR=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&duración_VALOR;순번++,duración_VALOR--){*destino_VALOR++=VALOR&255;VALOR>>=8;}}
    return 0;
}
