#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "aggregare.h"
#include "uzlib.h"
static unsigned char Archivio[16384], 풀린자료[16385];
static unsigned Dimensione, 중앙목록, 항목들;
static char voce_Corso[256];
static unsigned 두바이트읽기(unsigned Regolari_funzione) { return Archivio[Regolari_funzione] | Archivio[Regolari_funzione+1] << 8; }
static uint32_t 네바이트읽기(unsigned Regolari_funzione) { return 두바이트읽기(Regolari_funzione) | (uint32_t)두바이트읽기(Regolari_funzione+2) << 16; }
static int ritagliare(unsigned Regolari_funzione, unsigned articolo_CONTA_NUMERI, unsigned 한도) { return Regolari_funzione <= 한도 && articolo_CONTA_NUMERI <= 한도-Regolari_funzione; }
static size_t durata_VALORE(const char *stringa_dati) { size_t articolo_CONTA_NUMERI=0; while(stringa_dati[articolo_CONTA_NUMERI]) articolo_CONTA_NUMERI++; return articolo_CONTA_NUMERI; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECONDO_VALORE, unsigned articolo_CONTA_NUMERI) { for(unsigned 순번=0;순번<articolo_CONTA_NUMERI;순번++)if(첫째값[순번]!=SECONDO_VALORE[순번])return 0;return 1; }
static int File_chiudere(void *미사용값) { (void)미사용값; return -1; }
static int attributo_dati(const char *riga_di_ingresso,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)riga_di_ingresso,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)riga_di_ingresso,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALORE=사용량-12;if(*진입점있음||!VALORE||VALORE>=sizeof(voce_Corso))return -8;
        for(unsigned 순번=0;순번<VALORE;순번++){unsigned char punto_di_codice=riga_di_ingresso[12+순번];if(punto_di_codice<=32||punto_di_codice=='/'||punto_di_codice=='\\')return -8;voce_Corso[순번]=punto_di_codice;}
        voce_Corso[VALORE]=0;*진입점있음=1;
    }
    return 0;
}
static int membro(unsigned Regolari_funzione, unsigned char *KR_dati, unsigned 용량한도) {
    unsigned metodo_voce=두바이트읽기(Regolari_funzione+10), configurazione_BITS=두바이트읽기(Regolari_funzione+8), 압축크기=네바이트읽기(Regolari_funzione+20), release_ridimensionare=네바이트읽기(Regolari_funzione+24), locale=네바이트읽기(Regolari_funzione+42);
    unsigned Nome=두바이트읽기(Regolari_funzione+28);
    if(release_ridimensionare>용량한도 || release_ridimensionare>16384 || (metodo_voce!=0 && metodo_voce!=8) || (configurazione_BITS&~0x80e))return -8;
    if(!ritagliare(locale,30,중앙목록) || 네바이트읽기(locale)!=0x04034b50 || 두바이트읽기(locale+8)!=metodo_voce || 두바이트읽기(locale+6)!=configurazione_BITS || 두바이트읽기(locale+26)!=Nome)return -8;
    unsigned START_SCARTO=locale+30, 추가영역=두바이트읽기(locale+28);
    if(!ritagliare(START_SCARTO,Nome,중앙목록) || !같음(Archivio+START_SCARTO,Archivio+Regolari_funzione+46,Nome))return -8;
    START_SCARTO+=Nome;if(!ritagliare(START_SCARTO,추가영역,중앙목록))return -8;START_SCARTO+=추가영역;
    if(!ritagliare(START_SCARTO,압축크기,중앙목록))return -8;
    if(!(configurazione_BITS&8) && (네바이트읽기(locale+14)!=네바이트읽기(Regolari_funzione+16) || 네바이트읽기(locale+18)!=압축크기 || 네바이트읽기(locale+22)!=release_ridimensionare))return -8;
    if(metodo_voce==0) { if(압축크기!=release_ridimensionare)return -8; for(unsigned 순번=0;순번<release_ridimensionare;순번++)KR_dati[순번]=Archivio[START_SCARTO+순번]; }
    else {
        uzlib_uncomp_t meta_dati={0};uzlib_uncompress_init(&meta_dati,0,0);
        meta_dati.source=Archivio+START_SCARTO;meta_dati.source_limit=meta_dati.source+압축크기;meta_dati.source_read_cb=File_chiudere;
        /* One extra output byte lets inflate consume/check the end marker. */
        meta_dati.dest_start=meta_dati.dest=풀린자료;meta_dati.dest_limit=풀린자료+release_ridimensionare+1;
        int 반환값=uzlib_uncompress(&meta_dati);
        if(반환값!=UZLIB_DONE || meta_dati.eof || meta_dati.dest!=풀린자료+release_ridimensionare || meta_dati.source!=meta_dati.source_limit)return -8;
        for(unsigned 순번=0;순번<release_ridimensionare;순번++)KR_dati[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_dati,release_ridimensionare,0xffffffffu)^0xffffffffu)!=네바이트읽기(Regolari_funzione+16))return -8;
    return release_ridimensionare;
}
int 꾸러미읽기(const char *Nome, unsigned char *KR_dati, unsigned buffer_capacità) {
    if(!항목들)return -2;unsigned articolo_CONTA_NUMERI=durata_VALORE(Nome),Regolari_funzione=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(Regolari_funzione+28);
        if(이름길이==articolo_CONTA_NUMERI && 같음(Archivio+Regolari_funzione+46,(const unsigned char*)Nome,articolo_CONTA_NUMERI))return membro(Regolari_funzione,KR_dati,buffer_capacità);
        Regolari_funzione+=46+이름길이+두바이트읽기(Regolari_funzione+30)+두바이트읽기(Regolari_funzione+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return voce_Corso; }
int 꾸러미열기(const char *File_voce_nome) {
    항목들=0;voce_Corso[0]=0;
    intptr_t handle_di_file=사용자호출(3,(uintptr_t)File_voce_nome,0,0,0,0,0);if(handle_di_file<0)return handle_di_file;
    intptr_t articolo_CONTA_NUMERI=사용자호출(9,handle_di_file,0,0,0,0,0);
    if(articolo_CONTA_NUMERI<22 || articolo_CONTA_NUMERI>(intptr_t)sizeof(Archivio)) { 사용자호출(4,handle_di_file,0,0,0,0,0);return -8; }
    intptr_t RICEV_SCAD_CONTA_NUMERI=사용자호출(2,handle_di_file,(uintptr_t)Archivio,articolo_CONTA_NUMERI,0,0,0);사용자호출(4,handle_di_file,0,0,0,0,0);
    if(RICEV_SCAD_CONTA_NUMERI!=articolo_CONTA_NUMERI)return -5;Dimensione=articolo_CONTA_NUMERI;
    unsigned chiudere_SCARTO=Dimensione-22;
    for(;;) { if(네바이트읽기(chiudere_SCARTO)==0x06054b50 && chiudere_SCARTO+22+두바이트읽기(chiudere_SCARTO+20)==Dimensione)break; if(!chiudere_SCARTO)return -8;chiudere_SCARTO--; }
    unsigned voce_CONTA_NUMERI=두바이트읽기(chiudere_SCARTO+10);중앙목록=네바이트읽기(chiudere_SCARTO+16);
    if(두바이트읽기(chiudere_SCARTO+4)||두바이트읽기(chiudere_SCARTO+6)||두바이트읽기(chiudere_SCARTO+8)!=voce_CONTA_NUMERI||!voce_CONTA_NUMERI||voce_CONTA_NUMERI>256||!ritagliare(중앙목록,네바이트읽기(chiudere_SCARTO+12),chiudere_SCARTO)||중앙목록+네바이트읽기(chiudere_SCARTO+12)!=chiudere_SCARTO)return -8;
    unsigned Regolari_funzione=중앙목록;
    for(unsigned 순번=0;순번<voce_CONTA_NUMERI;순번++) {
        if(!ritagliare(Regolari_funzione,46,chiudere_SCARTO)||네바이트읽기(Regolari_funzione)!=0x02014b50||두바이트읽기(Regolari_funzione+34))return -8;
        unsigned 이름길이=두바이트읽기(Regolari_funzione+28),Avanti_articolo=46+이름길이+두바이트읽기(Regolari_funzione+30)+두바이트읽기(Regolari_funzione+32);
        if(!이름길이||이름길이>511||!ritagliare(Regolari_funzione,Avanti_articolo,chiudere_SCARTO)||네바이트읽기(Regolari_funzione+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Archivio[Regolari_funzione+46+안쪽순번])return -8;
        unsigned Altro_voce=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned durata_dati=두바이트읽기(Altro_voce+28);if(durata_dati==이름길이&&같음(Archivio+Altro_voce+46,Archivio+Regolari_funzione+46,durata_dati))return -8;Altro_voce+=46+durata_dati+두바이트읽기(Altro_voce+30)+두바이트읽기(Altro_voce+32);}
        Regolari_funzione+=Avanti_articolo;
    }
    if(Regolari_funzione!=chiudere_SCARTO)return -8;항목들=voce_CONTA_NUMERI;
    unsigned char aggregare_manifesto[4096];int gruppo_ridimensionare=꾸러미읽기("META-INF/MANIFEST.MF",aggregare_manifesto,sizeof(aggregare_manifesto)-1);if(gruppo_ridimensionare<0){항목들=0;return -8;}
    aggregare_manifesto[gruppo_ridimensionare]=0;
    char logico[512];unsigned 사용량=0,INDICE_VALORE=0;int 진입점있음=0;
    while(INDICE_VALORE<(unsigned)gruppo_ridimensionare) {
        unsigned avvia=INDICE_VALORE;while(INDICE_VALORE<(unsigned)gruppo_ridimensionare && aggregare_manifesto[INDICE_VALORE]!='\n')INDICE_VALORE++;
        unsigned durata_dati=INDICE_VALORE-avvia;if(INDICE_VALORE<(unsigned)gruppo_ridimensionare)INDICE_VALORE++;if(durata_dati && aggregare_manifesto[avvia+durata_dati-1]=='\r')durata_dati--;
        if(사용량 && durata_dati && aggregare_manifesto[avvia]==' ') {avvia++;durata_dati--;}
        else {
            int risultato=attributo_dati(logico,사용량,&진입점있음);if(risultato)return risultato;
            사용량=0;if(!durata_dati)break;
        }
        if(durata_dati>sizeof(logico)-사용량)return -8;
        for(unsigned 순번=0;순번<durata_dati;순번++)logico[사용량++]=aggregare_manifesto[avvia+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int risultato=attributo_dati(logico,사용량,&진입점있음);if(risultato)return risultato;
    return 진입점있음?0:-8;
}
