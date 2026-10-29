#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "grupo.h"
#include "uzlib.h"
static unsigned char arquivo[16384], 풀린자료[16385];
static unsigned Tamanho, 중앙목록, 항목들;
static char entrada_aula[256];
static unsigned 두바이트읽기(unsigned em_dia_cargo) { return arquivo[em_dia_cargo] | arquivo[em_dia_cargo+1] << 8; }
static uint32_t 네바이트읽기(unsigned em_dia_cargo) { return 두바이트읽기(em_dia_cargo) | (uint32_t)두바이트읽기(em_dia_cargo+2) << 16; }
static int recortar(unsigned em_dia_cargo, unsigned item_CONT_NÚM, unsigned 한도) { return em_dia_cargo <= 한도 && item_CONT_NÚM <= 한도-em_dia_cargo; }
static size_t duração_VALOR(const char *cadeia_dados) { size_t item_CONT_NÚM=0; while(cadeia_dados[item_CONT_NÚM]) item_CONT_NÚM++; return item_CONT_NÚM; }
static int 같음(const unsigned char *첫째값, const unsigned char *SEGUNDO_VALOR, unsigned item_CONT_NÚM) { for(unsigned 순번=0;순번<item_CONT_NÚM;순번++)if(첫째값[순번]!=SEGUNDO_VALOR[순번])return 0;return 1; }
static int Arquivo_encerrar(void *미사용값) { (void)미사용값; return -1; }
static int atributo_dados(const char *linha_de_entrada,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)linha_de_entrada,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)linha_de_entrada,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALOR=사용량-12;if(*진입점있음||!VALOR||VALOR>=sizeof(entrada_aula))return -8;
        for(unsigned 순번=0;순번<VALOR;순번++){unsigned char ponto_de_código=linha_de_entrada[12+순번];if(ponto_de_código<=32||ponto_de_código=='/'||ponto_de_código=='\\')return -8;entrada_aula[순번]=ponto_de_código;}
        entrada_aula[VALOR]=0;*진입점있음=1;
    }
    return 0;
}
static int membro(unsigned em_dia_cargo, unsigned char *RC_dados, unsigned 용량한도) {
    unsigned método_entrada=두바이트읽기(em_dia_cargo+10), Configuração_BITS=두바이트읽기(em_dia_cargo+8), 압축크기=네바이트읽기(em_dia_cargo+20), lançar_dimensionar=네바이트읽기(em_dia_cargo+24), local=네바이트읽기(em_dia_cargo+42);
    unsigned Nome=두바이트읽기(em_dia_cargo+28);
    if(lançar_dimensionar>용량한도 || lançar_dimensionar>16384 || (método_entrada!=0 && método_entrada!=8) || (Configuração_BITS&~0x80e))return -8;
    if(!recortar(local,30,중앙목록) || 네바이트읽기(local)!=0x04034b50 || 두바이트읽기(local+8)!=método_entrada || 두바이트읽기(local+6)!=Configuração_BITS || 두바이트읽기(local+26)!=Nome)return -8;
    unsigned START_DESLOC=local+30, 추가영역=두바이트읽기(local+28);
    if(!recortar(START_DESLOC,Nome,중앙목록) || !같음(arquivo+START_DESLOC,arquivo+em_dia_cargo+46,Nome))return -8;
    START_DESLOC+=Nome;if(!recortar(START_DESLOC,추가영역,중앙목록))return -8;START_DESLOC+=추가영역;
    if(!recortar(START_DESLOC,압축크기,중앙목록))return -8;
    if(!(Configuração_BITS&8) && (네바이트읽기(local+14)!=네바이트읽기(em_dia_cargo+16) || 네바이트읽기(local+18)!=압축크기 || 네바이트읽기(local+22)!=lançar_dimensionar))return -8;
    if(método_entrada==0) { if(압축크기!=lançar_dimensionar)return -8; for(unsigned 순번=0;순번<lançar_dimensionar;순번++)RC_dados[순번]=arquivo[START_DESLOC+순번]; }
    else {
        uzlib_uncomp_t destino_dados={0};uzlib_uncompress_init(&destino_dados,0,0);
        destino_dados.source=arquivo+START_DESLOC;destino_dados.source_limit=destino_dados.source+압축크기;destino_dados.source_read_cb=Arquivo_encerrar;
        /* One extra output byte lets inflate consume/check the end marker. */
        destino_dados.dest_start=destino_dados.dest=풀린자료;destino_dados.dest_limit=풀린자료+lançar_dimensionar+1;
        int 반환값=uzlib_uncompress(&destino_dados);
        if(반환값!=UZLIB_DONE || destino_dados.eof || destino_dados.dest!=풀린자료+lançar_dimensionar || destino_dados.source!=destino_dados.source_limit)return -8;
        for(unsigned 순번=0;순번<lançar_dimensionar;순번++)RC_dados[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(RC_dados,lançar_dimensionar,0xffffffffu)^0xffffffffu)!=네바이트읽기(em_dia_cargo+16))return -8;
    return lançar_dimensionar;
}
int 꾸러미읽기(const char *Nome, unsigned char *RC_dados, unsigned buffer_capacidade) {
    if(!항목들)return -2;unsigned item_CONT_NÚM=duração_VALOR(Nome),em_dia_cargo=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(em_dia_cargo+28);
        if(이름길이==item_CONT_NÚM && 같음(arquivo+em_dia_cargo+46,(const unsigned char*)Nome,item_CONT_NÚM))return membro(em_dia_cargo,RC_dados,buffer_capacidade);
        em_dia_cargo+=46+이름길이+두바이트읽기(em_dia_cargo+30)+두바이트읽기(em_dia_cargo+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return entrada_aula; }
int 꾸러미열기(const char *Arquivo_entrada_nome) {
    항목들=0;entrada_aula[0]=0;
    intptr_t identificador_de_arquivo=사용자호출(3,(uintptr_t)Arquivo_entrada_nome,0,0,0,0,0);if(identificador_de_arquivo<0)return identificador_de_arquivo;
    intptr_t item_CONT_NÚM=사용자호출(9,identificador_de_arquivo,0,0,0,0,0);
    if(item_CONT_NÚM<22 || item_CONT_NÚM>(intptr_t)sizeof(arquivo)) { 사용자호출(4,identificador_de_arquivo,0,0,0,0,0);return -8; }
    intptr_t RECEBER_CONT_NÚM=사용자호출(2,identificador_de_arquivo,(uintptr_t)arquivo,item_CONT_NÚM,0,0,0);사용자호출(4,identificador_de_arquivo,0,0,0,0,0);
    if(RECEBER_CONT_NÚM!=item_CONT_NÚM)return -5;Tamanho=item_CONT_NÚM;
    unsigned encerrar_DESLOC=Tamanho-22;
    for(;;) { if(네바이트읽기(encerrar_DESLOC)==0x06054b50 && encerrar_DESLOC+22+두바이트읽기(encerrar_DESLOC+20)==Tamanho)break; if(!encerrar_DESLOC)return -8;encerrar_DESLOC--; }
    unsigned entrada_CONT_NÚM_8f7753a1=두바이트읽기(encerrar_DESLOC+10);중앙목록=네바이트읽기(encerrar_DESLOC+16);
    if(두바이트읽기(encerrar_DESLOC+4)||두바이트읽기(encerrar_DESLOC+6)||두바이트읽기(encerrar_DESLOC+8)!=entrada_CONT_NÚM_8f7753a1||!entrada_CONT_NÚM_8f7753a1||entrada_CONT_NÚM_8f7753a1>256||!recortar(중앙목록,네바이트읽기(encerrar_DESLOC+12),encerrar_DESLOC)||중앙목록+네바이트읽기(encerrar_DESLOC+12)!=encerrar_DESLOC)return -8;
    unsigned em_dia_cargo=중앙목록;
    for(unsigned 순번=0;순번<entrada_CONT_NÚM_8f7753a1;순번++) {
        if(!recortar(em_dia_cargo,46,encerrar_DESLOC)||네바이트읽기(em_dia_cargo)!=0x02014b50||두바이트읽기(em_dia_cargo+34))return -8;
        unsigned 이름길이=두바이트읽기(em_dia_cargo+28),Avançar_item=46+이름길이+두바이트읽기(em_dia_cargo+30)+두바이트읽기(em_dia_cargo+32);
        if(!이름길이||이름길이>511||!recortar(em_dia_cargo,Avançar_item,encerrar_DESLOC)||네바이트읽기(em_dia_cargo+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!arquivo[em_dia_cargo+46+안쪽순번])return -8;
        unsigned Outros_entrada=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned duração_dados=두바이트읽기(Outros_entrada+28);if(duração_dados==이름길이&&같음(arquivo+Outros_entrada+46,arquivo+em_dia_cargo+46,duração_dados))return -8;Outros_entrada+=46+duração_dados+두바이트읽기(Outros_entrada+30)+두바이트읽기(Outros_entrada+32);}
        em_dia_cargo+=Avançar_item;
    }
    if(em_dia_cargo!=encerrar_DESLOC)return -8;항목들=entrada_CONT_NÚM_8f7753a1;
    unsigned char grupo_manifesto[4096];int Grupo_dimensionar=꾸러미읽기("META-INF/MANIFEST.MF",grupo_manifesto,sizeof(grupo_manifesto)-1);if(Grupo_dimensionar<0){항목들=0;return -8;}
    grupo_manifesto[Grupo_dimensionar]=0;
    char 논리크기[512];unsigned 사용량=0,ÍNDICE_VALOR=0;int 진입점있음=0;
    while(ÍNDICE_VALOR<(unsigned)Grupo_dimensionar) {
        unsigned iniciar=ÍNDICE_VALOR;while(ÍNDICE_VALOR<(unsigned)Grupo_dimensionar && grupo_manifesto[ÍNDICE_VALOR]!='\n')ÍNDICE_VALOR++;
        unsigned duração_dados=ÍNDICE_VALOR-iniciar;if(ÍNDICE_VALOR<(unsigned)Grupo_dimensionar)ÍNDICE_VALOR++;if(duração_dados && grupo_manifesto[iniciar+duração_dados-1]=='\r')duração_dados--;
        if(사용량 && duração_dados && grupo_manifesto[iniciar]==' ') {iniciar++;duração_dados--;}
        else {
            int resultado=atributo_dados(논리크기,사용량,&진입점있음);if(resultado)return resultado;
            사용량=0;if(!duração_dados)break;
        }
        if(duração_dados>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<duração_dados;순번++)논리크기[사용량++]=grupo_manifesto[iniciar+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int resultado=atributo_dados(논리크기,사용량,&진입점있음);if(resultado)return resultado;
    return 진입점있음?0:-8;
}
