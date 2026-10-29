#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "paquete.h"
#include "uzlib.h"
static unsigned char Arquivo[16384], 풀린자료[16385];
static unsigned Tamaño, 중앙목록, 항목들;
static char introdución_Clase[256];
static unsigned 두바이트읽기(unsigned ao_corrente_cargo) { return Arquivo[ao_corrente_cargo] | Arquivo[ao_corrente_cargo+1] << 8; }
static uint32_t 네바이트읽기(unsigned ao_corrente_cargo) { return 두바이트읽기(ao_corrente_cargo) | (uint32_t)두바이트읽기(ao_corrente_cargo+2) << 16; }
static int clip(unsigned ao_corrente_cargo, unsigned elemento_CONTAR, unsigned 한도) { return ao_corrente_cargo <= 한도 && elemento_CONTAR <= 한도-ao_corrente_cargo; }
static size_t duración_VALOR(const char *cadea_datos) { size_t elemento_CONTAR=0; while(cadea_datos[elemento_CONTAR]) elemento_CONTAR++; return elemento_CONTAR; }
static int 같음(const unsigned char *첫째값, const unsigned char *SEGUNDO_VALOR, unsigned elemento_CONTAR) { for(unsigned 순번=0;순번<elemento_CONTAR;순번++)if(첫째값[순번]!=SEGUNDO_VALOR[순번])return 0;return 1; }
static int Ficheiro_finalizar(void *미사용값) { (void)미사용값; return -1; }
static int atributo_datos(const char *Liña,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Liña,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Liña,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALOR=사용량-12;if(*진입점있음||!VALOR||VALOR>=sizeof(introdución_Clase))return -8;
        for(unsigned 순번=0;순번<VALOR;순번++){unsigned char código_de_carácter=Liña[12+순번];if(código_de_carácter<=32||código_de_carácter=='/'||código_de_carácter=='\\')return -8;introdución_Clase[순번]=código_de_carácter;}
        introdución_Clase[VALOR]=0;*진입점있음=1;
    }
    return 0;
}
static int membro(unsigned ao_corrente_cargo, unsigned char *medida_datos, unsigned 용량한도) {
    unsigned 메소드=두바이트읽기(ao_corrente_cargo+10), configuración_Servizo_de_transferencia_intelixente_en_segundo_plano=두바이트읽기(ao_corrente_cargo+8), 압축크기=네바이트읽기(ao_corrente_cargo+20), 해제크기=네바이트읽기(ao_corrente_cargo+24), local=네바이트읽기(ao_corrente_cargo+42);
    unsigned Nome=두바이트읽기(ao_corrente_cargo+28);
    if(해제크기>용량한도 || 해제크기>16384 || (메소드!=0 && 메소드!=8) || (configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&~0x80e))return -8;
    if(!clip(local,30,중앙목록) || 네바이트읽기(local)!=0x04034b50 || 두바이트읽기(local+8)!=메소드 || 두바이트읽기(local+6)!=configuración_Servizo_de_transferencia_intelixente_en_segundo_plano || 두바이트읽기(local+26)!=Nome)return -8;
    unsigned START_DESPRAZAMENTO=local+30, 추가영역=두바이트읽기(local+28);
    if(!clip(START_DESPRAZAMENTO,Nome,중앙목록) || !같음(Arquivo+START_DESPRAZAMENTO,Arquivo+ao_corrente_cargo+46,Nome))return -8;
    START_DESPRAZAMENTO+=Nome;if(!clip(START_DESPRAZAMENTO,추가영역,중앙목록))return -8;START_DESPRAZAMENTO+=추가영역;
    if(!clip(START_DESPRAZAMENTO,압축크기,중앙목록))return -8;
    if(!(configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&8) && (네바이트읽기(local+14)!=네바이트읽기(ao_corrente_cargo+16) || 네바이트읽기(local+18)!=압축크기 || 네바이트읽기(local+22)!=해제크기))return -8;
    if(메소드==0) { if(압축크기!=해제크기)return -8; for(unsigned 순번=0;순번<해제크기;순번++)medida_datos[순번]=Arquivo[START_DESPRAZAMENTO+순번]; }
    else {
        uzlib_uncomp_t destino_datos={0};uzlib_uncompress_init(&destino_datos,0,0);
        destino_datos.source=Arquivo+START_DESPRAZAMENTO;destino_datos.source_limit=destino_datos.source+압축크기;destino_datos.source_read_cb=Ficheiro_finalizar;
        /* One extra output byte lets inflate consume/check the end marker. */
        destino_datos.dest_start=destino_datos.dest=풀린자료;destino_datos.dest_limit=풀린자료+해제크기+1;
        int 반환값=uzlib_uncompress(&destino_datos);
        if(반환값!=UZLIB_DONE || destino_datos.eof || destino_datos.dest!=풀린자료+해제크기 || destino_datos.source!=destino_datos.source_limit)return -8;
        for(unsigned 순번=0;순번<해제크기;순번++)medida_datos[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(medida_datos,해제크기,0xffffffffu)^0xffffffffu)!=네바이트읽기(ao_corrente_cargo+16))return -8;
    return 해제크기;
}
int 꾸러미읽기(const char *Nome, unsigned char *medida_datos, unsigned búfer_capacidade) {
    if(!항목들)return -2;unsigned elemento_CONTAR=duración_VALOR(Nome),ao_corrente_cargo=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(ao_corrente_cargo+28);
        if(이름길이==elemento_CONTAR && 같음(Arquivo+ao_corrente_cargo+46,(const unsigned char*)Nome,elemento_CONTAR))return membro(ao_corrente_cargo,medida_datos,búfer_capacidade);
        ao_corrente_cargo+=46+이름길이+두바이트읽기(ao_corrente_cargo+30)+두바이트읽기(ao_corrente_cargo+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return introdución_Clase; }
int 꾸러미열기(const char *Ficheiro_introdución_nome) {
    항목들=0;introdución_Clase[0]=0;
    intptr_t Ficheiro_agarradoira=사용자호출(3,(uintptr_t)Ficheiro_introdución_nome,0,0,0,0,0);if(Ficheiro_agarradoira<0)return Ficheiro_agarradoira;
    intptr_t elemento_CONTAR=사용자호출(9,Ficheiro_agarradoira,0,0,0,0,0);
    if(elemento_CONTAR<22 || elemento_CONTAR>(intptr_t)sizeof(Arquivo)) { 사용자호출(4,Ficheiro_agarradoira,0,0,0,0,0);return -8; }
    intptr_t RECIBIDO_CONTAR=사용자호출(2,Ficheiro_agarradoira,(uintptr_t)Arquivo,elemento_CONTAR,0,0,0);사용자호출(4,Ficheiro_agarradoira,0,0,0,0,0);
    if(RECIBIDO_CONTAR!=elemento_CONTAR)return -5;Tamaño=elemento_CONTAR;
    unsigned finalizar_DESPRAZAMENTO=Tamaño-22;
    for(;;) { if(네바이트읽기(finalizar_DESPRAZAMENTO)==0x06054b50 && finalizar_DESPRAZAMENTO+22+두바이트읽기(finalizar_DESPRAZAMENTO+20)==Tamaño)break; if(!finalizar_DESPRAZAMENTO)return -8;finalizar_DESPRAZAMENTO--; }
    unsigned introdución_CONTAR=두바이트읽기(finalizar_DESPRAZAMENTO+10);중앙목록=네바이트읽기(finalizar_DESPRAZAMENTO+16);
    if(두바이트읽기(finalizar_DESPRAZAMENTO+4)||두바이트읽기(finalizar_DESPRAZAMENTO+6)||두바이트읽기(finalizar_DESPRAZAMENTO+8)!=introdución_CONTAR||!introdución_CONTAR||introdución_CONTAR>256||!clip(중앙목록,네바이트읽기(finalizar_DESPRAZAMENTO+12),finalizar_DESPRAZAMENTO)||중앙목록+네바이트읽기(finalizar_DESPRAZAMENTO+12)!=finalizar_DESPRAZAMENTO)return -8;
    unsigned ao_corrente_cargo=중앙목록;
    for(unsigned 순번=0;순번<introdución_CONTAR;순번++) {
        if(!clip(ao_corrente_cargo,46,finalizar_DESPRAZAMENTO)||네바이트읽기(ao_corrente_cargo)!=0x02014b50||두바이트읽기(ao_corrente_cargo+34))return -8;
        unsigned 이름길이=두바이트읽기(ao_corrente_cargo+28),Seguinte_elemento=46+이름길이+두바이트읽기(ao_corrente_cargo+30)+두바이트읽기(ao_corrente_cargo+32);
        if(!이름길이||이름길이>511||!clip(ao_corrente_cargo,Seguinte_elemento,finalizar_DESPRAZAMENTO)||네바이트읽기(ao_corrente_cargo+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arquivo[ao_corrente_cargo+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned duración_datos=두바이트읽기(다른항목+28);if(duración_datos==이름길이&&같음(Arquivo+다른항목+46,Arquivo+ao_corrente_cargo+46,duración_datos))return -8;다른항목+=46+duración_datos+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        ao_corrente_cargo+=Seguinte_elemento;
    }
    if(ao_corrente_cargo!=finalizar_DESPRAZAMENTO)return -8;항목들=introdución_CONTAR;
    unsigned char 꾸러미명세[4096];int 묶음수=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(묶음수<0){항목들=0;return -8;}
    꾸러미명세[묶음수]=0;
    char 논리크기[512];unsigned 사용량=0,ÍNDICE_VALOR=0;int 진입점있음=0;
    while(ÍNDICE_VALOR<(unsigned)묶음수) {
        unsigned Executar_2=ÍNDICE_VALOR;while(ÍNDICE_VALOR<(unsigned)묶음수 && 꾸러미명세[ÍNDICE_VALOR]!='\n')ÍNDICE_VALOR++;
        unsigned duración_datos=ÍNDICE_VALOR-Executar_2;if(ÍNDICE_VALOR<(unsigned)묶음수)ÍNDICE_VALOR++;if(duración_datos && 꾸러미명세[Executar_2+duración_datos-1]=='\r')duración_datos--;
        if(사용량 && duración_datos && 꾸러미명세[Executar_2]==' ') {Executar_2++;duración_datos--;}
        else {
            int RESULTANTE=atributo_datos(논리크기,사용량,&진입점있음);if(RESULTANTE)return RESULTANTE;
            사용량=0;if(!duración_datos)break;
        }
        if(duración_datos>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<duración_datos;순번++)논리크기[사용량++]=꾸러미명세[Executar_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int RESULTANTE=atributo_datos(논리크기,사용량,&진입점있음);if(RESULTANTE)return RESULTANTE;
    return 진입점있음?0:-8;
}
