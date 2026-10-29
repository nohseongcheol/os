#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "paquet.h"
#include "uzlib.h"
static unsigned char Arxiu[16384], 풀린자료[16385];
static unsigned Mida, 중앙목록, 항목들;
static char introducció_Classe[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Arxiu[현재위치] | Arxiu[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int clip(unsigned 현재위치, unsigned element_COMPT, unsigned 한도) { return 현재위치 <= 한도 && element_COMPT <= 한도-현재위치; }
static size_t durada_VALOR(const char *cadena_dades) { size_t element_COMPT=0; while(cadena_dades[element_COMPT]) element_COMPT++; return element_COMPT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SEGON_VALOR, unsigned element_COMPT) { for(unsigned 순번=0;순번<element_COMPT;순번++)if(첫째값[순번]!=SEGON_VALOR[순번])return 0;return 1; }
static int arxiu_finalitzar(void *미사용값) { (void)미사용값; return -1; }
static int atribut_dades(const char *línia,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)línia,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)línia,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALOR=사용량-12;if(*진입점있음||!VALOR||VALOR>=sizeof(introducció_Classe))return -8;
        for(unsigned 순번=0;순번<VALOR;순번++){unsigned char codi_de_caràcter=línia[12+순번];if(codi_de_caràcter<=32||codi_de_caràcter=='/'||codi_de_caràcter=='\\')return -8;introducció_Classe[순번]=codi_de_caràcter;}
        introducció_Classe[VALOR]=0;*진입점있음=1;
    }
    return 0;
}
static int membre(unsigned 현재위치, unsigned char *mesura_dades, unsigned 용량한도) {
    unsigned 메소드=두바이트읽기(현재위치+10), configuració_Servei_de_transferència_intel_ligent_en_segon_terme=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), versió_canviar_la_mida=네바이트읽기(현재위치+24), local=네바이트읽기(현재위치+42);
    unsigned Nom=두바이트읽기(현재위치+28);
    if(versió_canviar_la_mida>용량한도 || versió_canviar_la_mida>16384 || (메소드!=0 && 메소드!=8) || (configuració_Servei_de_transferència_intel_ligent_en_segon_terme&~0x80e))return -8;
    if(!clip(local,30,중앙목록) || 네바이트읽기(local)!=0x04034b50 || 두바이트읽기(local+8)!=메소드 || 두바이트읽기(local+6)!=configuració_Servei_de_transferència_intel_ligent_en_segon_terme || 두바이트읽기(local+26)!=Nom)return -8;
    unsigned Inici_DESPLAÇAMENT=local+30, 추가영역=두바이트읽기(local+28);
    if(!clip(Inici_DESPLAÇAMENT,Nom,중앙목록) || !같음(Arxiu+Inici_DESPLAÇAMENT,Arxiu+현재위치+46,Nom))return -8;
    Inici_DESPLAÇAMENT+=Nom;if(!clip(Inici_DESPLAÇAMENT,추가영역,중앙목록))return -8;Inici_DESPLAÇAMENT+=추가영역;
    if(!clip(Inici_DESPLAÇAMENT,압축크기,중앙목록))return -8;
    if(!(configuració_Servei_de_transferència_intel_ligent_en_segon_terme&8) && (네바이트읽기(local+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(local+18)!=압축크기 || 네바이트읽기(local+22)!=versió_canviar_la_mida))return -8;
    if(메소드==0) { if(압축크기!=versió_canviar_la_mida)return -8; for(unsigned 순번=0;순번<versió_canviar_la_mida;순번++)mesura_dades[순번]=Arxiu[Inici_DESPLAÇAMENT+순번]; }
    else {
        uzlib_uncomp_t destinació_dades={0};uzlib_uncompress_init(&destinació_dades,0,0);
        destinació_dades.source=Arxiu+Inici_DESPLAÇAMENT;destinació_dades.source_limit=destinació_dades.source+압축크기;destinació_dades.source_read_cb=arxiu_finalitzar;
        /* One extra output byte lets inflate consume/check the end marker. */
        destinació_dades.dest_start=destinació_dades.dest=풀린자료;destinació_dades.dest_limit=풀린자료+versió_canviar_la_mida+1;
        int 반환값=uzlib_uncompress(&destinació_dades);
        if(반환값!=UZLIB_DONE || destinació_dades.eof || destinació_dades.dest!=풀린자료+versió_canviar_la_mida || destinació_dades.source!=destinació_dades.source_limit)return -8;
        for(unsigned 순번=0;순번<versió_canviar_la_mida;순번++)mesura_dades[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(mesura_dades,versió_canviar_la_mida,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return versió_canviar_la_mida;
}
int 꾸러미읽기(const char *Nom, unsigned char *mesura_dades, unsigned memòria_intermèdia_capacitat) {
    if(!항목들)return -2;unsigned element_COMPT=durada_VALOR(Nom),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==element_COMPT && 같음(Arxiu+현재위치+46,(const unsigned char*)Nom,element_COMPT))return membre(현재위치,mesura_dades,memòria_intermèdia_capacitat);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return introducció_Classe; }
int 꾸러미열기(const char *arxiu_introducció_nom) {
    항목들=0;introducció_Classe[0]=0;
    intptr_t arxiu_control_7f4cdfd5=사용자호출(3,(uintptr_t)arxiu_introducció_nom,0,0,0,0,0);if(arxiu_control_7f4cdfd5<0)return arxiu_control_7f4cdfd5;
    intptr_t element_COMPT=사용자호출(9,arxiu_control_7f4cdfd5,0,0,0,0,0);
    if(element_COMPT<22 || element_COMPT>(intptr_t)sizeof(Arxiu)) { 사용자호출(4,arxiu_control_7f4cdfd5,0,0,0,0,0);return -8; }
    intptr_t CANTIDAD_RECIBIDA_COMPT=사용자호출(2,arxiu_control_7f4cdfd5,(uintptr_t)Arxiu,element_COMPT,0,0,0);사용자호출(4,arxiu_control_7f4cdfd5,0,0,0,0,0);
    if(CANTIDAD_RECIBIDA_COMPT!=element_COMPT)return -5;Mida=element_COMPT;
    unsigned finalitzar_DESPLAÇAMENT=Mida-22;
    for(;;) { if(네바이트읽기(finalitzar_DESPLAÇAMENT)==0x06054b50 && finalitzar_DESPLAÇAMENT+22+두바이트읽기(finalitzar_DESPLAÇAMENT+20)==Mida)break; if(!finalitzar_DESPLAÇAMENT)return -8;finalitzar_DESPLAÇAMENT--; }
    unsigned introducció_COMPT=두바이트읽기(finalitzar_DESPLAÇAMENT+10);중앙목록=네바이트읽기(finalitzar_DESPLAÇAMENT+16);
    if(두바이트읽기(finalitzar_DESPLAÇAMENT+4)||두바이트읽기(finalitzar_DESPLAÇAMENT+6)||두바이트읽기(finalitzar_DESPLAÇAMENT+8)!=introducció_COMPT||!introducció_COMPT||introducció_COMPT>256||!clip(중앙목록,네바이트읽기(finalitzar_DESPLAÇAMENT+12),finalitzar_DESPLAÇAMENT)||중앙목록+네바이트읽기(finalitzar_DESPLAÇAMENT+12)!=finalitzar_DESPLAÇAMENT)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<introducció_COMPT;순번++) {
        if(!clip(현재위치,46,finalitzar_DESPLAÇAMENT)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Següent_element=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!clip(현재위치,Següent_element,finalitzar_DESPLAÇAMENT)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arxiu[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned durada_dades=두바이트읽기(다른항목+28);if(durada_dades==이름길이&&같음(Arxiu+다른항목+46,Arxiu+현재위치+46,durada_dades))return -8;다른항목+=46+durada_dades+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Següent_element;
    }
    if(현재위치!=finalitzar_DESPLAÇAMENT)return -8;항목들=introducció_COMPT;
    unsigned char 꾸러미명세[4096];int Grup_canviar_la_mida=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Grup_canviar_la_mida<0){항목들=0;return -8;}
    꾸러미명세[Grup_canviar_la_mida]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALOR=0;int 진입점있음=0;
    while(INDEX_VALOR<(unsigned)Grup_canviar_la_mida) {
        unsigned Executa_2=INDEX_VALOR;while(INDEX_VALOR<(unsigned)Grup_canviar_la_mida && 꾸러미명세[INDEX_VALOR]!='\n')INDEX_VALOR++;
        unsigned durada_dades=INDEX_VALOR-Executa_2;if(INDEX_VALOR<(unsigned)Grup_canviar_la_mida)INDEX_VALOR++;if(durada_dades && 꾸러미명세[Executa_2+durada_dades-1]=='\r')durada_dades--;
        if(사용량 && durada_dades && 꾸러미명세[Executa_2]==' ') {Executa_2++;durada_dades--;}
        else {
            int RESULTAT=atribut_dades(논리크기,사용량,&진입점있음);if(RESULTAT)return RESULTAT;
            사용량=0;if(!durada_dades)break;
        }
        if(durada_dades>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<durada_dades;순번++)논리크기[사용량++]=꾸러미명세[Executa_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int RESULTAT=atribut_dades(논리크기,사용량,&진입점있음);if(RESULTAT)return RESULTAT;
    return 진입점있음?0:-8;
}
