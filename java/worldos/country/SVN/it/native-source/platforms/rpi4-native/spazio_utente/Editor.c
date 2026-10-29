/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "File_ABI.h"
#define Editor_capacità 16384
static unsigned char testo[Editor_capacità],annullare_dati[Editor_capacità],복사자료[Editor_capacità],KR_dati[1024];
static int durata_VALORE,INDICE_VALORE,맨위,왼쪽,변경됨,inserire,annullare_durata,위쪽,annullare_Modifiche,되돌림있음,copiare_durata,사용량,COLONNE=68,riga_CONTA_NUMERI=19;
static char File_voce_nome[64],comando[128],TROVA_voce[128];
static const char *informativa_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned In_sospeso_tasto;
static int Guida_area,Stato_foto,Stato_coda;
static void allineato(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_dati,사용량,0,0,0);사용량=0;}}
static void byte_dati(unsigned punto_di_codice){if(Stato_foto){if((punto_di_codice&192)!=128){Stato_coda+=punto_di_codice>=196?2:1;}if(Stato_coda>=COLONNE)return;}if(사용량==(int)sizeof(KR_dati))allineato();KR_dati[사용량++]=punto_di_codice;}
static void 글내보내기(const char *stringa_dati){while(*stringa_dati)byte_dati((unsigned char)*stringa_dati++);}
static void 수치(unsigned articolo_CONTA_NUMERI){char SECONDO_VALORE[12];int 순번=0;do{SECONDO_VALORE[순번++]='0'+articolo_CONTA_NUMERI%10;articolo_CONTA_NUMERI/=10;}while(articolo_CONTA_NUMERI);while(순번)byte_dati(SECONDO_VALORE[--순번]);}
static void spostare_VALORE(int riga_funzione,int colonna_funzione){글내보내기("\033[");수치(riga_funzione);byte_dati(';');수치(colonna_funzione);byte_dati('H');}
static int Indietro(int dati_funzione){if(dati_funzione){dati_funzione--;while(dati_funzione>0&&(testo[dati_funzione]&192)==128)dati_funzione--;}return dati_funzione;}
static int Avanti_articolo(int dati_funzione){if(dati_funzione<durata_VALORE){dati_funzione++;while(dati_funzione<durata_VALORE&&(testo[dati_funzione]&192)==128)dati_funzione++;}return dati_funzione;}
static int avvia(int dati_funzione){while(dati_funzione>0&&testo[dati_funzione-1]!='\n')dati_funzione--;return dati_funzione;}
static int chiudere_SCARTO(int dati_funzione){while(dati_funzione<durata_VALORE&&testo[dati_funzione]!='\n')dati_funzione++;return dati_funzione;}
static int 너비(unsigned punto_di_codice){return punto_di_codice>=196?2:1;}
static int colonna(int dati_funzione){int punto_di_codice=0;for(int 순번=avvia(dati_funzione);순번<dati_funzione;순번=Avanti_articolo(순번))punto_di_codice+=testo[순번]=='\t'?4-punto_di_codice%4:너비(testo[순번]);return punto_di_codice;}
static void checkpoint(void){for(int 순번=0;순번<durata_VALORE;순번++)annullare_dati[순번]=testo[순번];annullare_durata=durata_VALORE;위쪽=INDICE_VALORE;annullare_Modifiche=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){checkpoint();for(int 순번=도착위치;순번<durata_VALORE;순번++)testo[출발위치+순번-도착위치]=testo[순번];durata_VALORE-=도착위치-출발위치;INDICE_VALORE=출발위치;변경됨=1;}
static int Aggiunta_VALORE(const unsigned char *stringa_dati,int articolo_CONTA_NUMERI){if(articolo_CONTA_NUMERI>Editor_capacità-durata_VALORE){informativa_SMS="File full (16384 bytes)";return 0;}checkpoint();for(int 순번=durata_VALORE-1;순번>=INDICE_VALORE;순번--)testo[순번+articolo_CONTA_NUMERI]=testo[순번];for(int 순번=0;순번<articolo_CONTA_NUMERI;순번++)testo[INDICE_VALORE+순번]=stringa_dati[순번];durata_VALORE+=articolo_CONTA_NUMERI;INDICE_VALORE+=articolo_CONTA_NUMERI;변경됨=1;return 1;}
static void Verticale(int 차이){int colonna_funzione=colonna(INDICE_VALORE),dati_funzione=avvia(INDICE_VALORE);if(차이<0){if(!dati_funzione)return;dati_funzione=avvia(dati_funzione-1);}else{dati_funzione=chiudere_SCARTO(dati_funzione);if(dati_funzione==durata_VALORE)return;dati_funzione++;}int punto_di_codice=0;while(dati_funzione<durata_VALORE&&testo[dati_funzione]!='\n'&&punto_di_codice<colonna_funzione){punto_di_codice+=testo[dati_funzione]=='\t'?4-punto_di_codice%4:너비(testo[dati_funzione]);dati_funzione=Avanti_articolo(dati_funzione);}INDICE_VALORE=dati_funzione;}
static void Disegno_schermata(void){
    if(INDICE_VALORE>durata_VALORE)INDICE_VALORE=durata_VALORE;if(맨위>INDICE_VALORE)맨위=avvia(INDICE_VALORE);맨위=avvia(맨위);
    int riga_funzione=0;for(int 순번=맨위;순번<INDICE_VALORE;순번++)if(testo[순번]=='\n')riga_funzione++;
    while(riga_funzione>=riga_CONTA_NUMERI-1){맨위=chiudere_SCARTO(맨위);if(맨위<durata_VALORE)맨위++;riga_funzione--;}
    int colonna_funzione=colonna(INDICE_VALORE);if(colonna_funzione<왼쪽)왼쪽=colonna_funzione;if(colonna_funzione-왼쪽>=COLONNE-1)왼쪽=colonna_funzione-COLONNE+2;
    글내보내기("\033[?25l");int dati_funzione=맨위;
    for(int 반환값=0;반환값<riga_CONTA_NUMERI-1;반환값++){
        spostare_VALORE(반환값+1,1);글내보내기("\033[0m\033[2K");int punto_di_codice=0,그려진상태=0;
        if(dati_funzione>=durata_VALORE&&반환값>riga_funzione){글내보내기("\033[90m~\033[0m");continue;}
        while(dati_funzione<durata_VALORE&&testo[dati_funzione]!='\n'){
            int Avanti_SCARTO=Avanti_articolo(dati_funzione),너비값=testo[dati_funzione]=='\t'?4-punto_di_codice%4:너비(testo[dati_funzione]);
            if(punto_di_codice>=왼쪽&&punto_di_codice-왼쪽+너비값<COLONNE){
                if(testo[dati_funzione]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_dati(' ');}else if(testo[dati_funzione]<32||testo[dati_funzione]==127){byte_dati('?');}else for(int 안쪽순번=dati_funzione;안쪽순번<Avanti_SCARTO;안쪽순번++)byte_dati(testo[안쪽순번]);그려진상태+=너비값;
            }punto_di_codice+=너비값;dati_funzione=Avanti_SCARTO;
        }
        (void)그려진상태;if(dati_funzione<durata_VALORE)dati_funzione++;
    }
    spostare_VALORE(riga_CONTA_NUMERI,1);글내보내기("\033[7m\033[2K");Stato_foto=1;Stato_coda=0;글내보내기(inserire?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(File_voce_nome[이름바이트수]&&이름바이트수<30)byte_dati(File_voce_nome[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int riga_di_ingresso=1;for(int 순번=0;순번<INDICE_VALORE;순번++)if(testo[순번]=='\n')riga_di_ingresso++;수치(riga_di_ingresso);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(informativa_SMS){int articolo_CONTA_NUMERI=0;글내보내기(" | ");while(informativa_SMS[articolo_CONTA_NUMERI]&&articolo_CONTA_NUMERI<20)byte_dati(informativa_SMS[articolo_CONTA_NUMERI++]);}
    Stato_foto=0;글내보내기("\033[0m");spostare_VALORE(riga_funzione+1,colonna_funzione-왼쪽+1);글내보내기("\033[?25h");allineato();
}
static int 누름값(void){
    if(In_sospeso_tasto){int 셋째순번=In_sospeso_tasto;In_sospeso_tasto=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Dimensione=사용자호출(16,3,0,0,0,0,0);
        if(COLONNE!=(int)(Dimensione&65535)||riga_CONTA_NUMERI!=(int)(Dimensione>>16)){
            COLONNE=Dimensione&65535;riga_CONTA_NUMERI=Dimensione>>16;Disegno_schermata();
            if(Guida_area){spostare_VALORE(riga_CONTA_NUMERI,1);글내보내기("\033[0m\033[2K");byte_dati(Guida_area);글내보내기(comando);allineato();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned Regolari_funzione=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-Regolari_funzione<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){In_sospeso_tasto=셋째순번;return 27;}
    int articolo_CONTA_NUMERI=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){articolo_CONTA_NUMERI=articolo_CONTA_NUMERI*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return articolo_CONTA_NUMERI==3?1007:articolo_CONTA_NUMERI==5?1008:articolo_CONTA_NUMERI==6?1009:articolo_CONTA_NUMERI==1?1005:articolo_CONTA_NUMERI==4?1006:27;return 27;}return 27;
}
static int Store_VALORE(void){
    int handle_di_file=aperto_File(File_voce_nome,in_lettura_scrittura|없으면만들기|tagliare_Sommario,0600);if(handle_di_file<0){informativa_SMS="Cannot open for save";return 0;}
    intptr_t articolo_CONTA_NUMERI=scrivere_File_dati(handle_di_file,testo,durata_VALORE);Chiudi_File(handle_di_file);if(articolo_CONTA_NUMERI!=durata_VALORE){informativa_SMS="Write failed";return 0;}변경됨=0;informativa_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECONDO_VALORE){while(*첫째값&&*첫째값==*SECONDO_VALORE){첫째값++;SECONDO_VALORE++;}return *첫째값==*SECONDO_VALORE;}
static void TROVA_Avanti(void){int articolo_CONTA_NUMERI=0;while(TROVA_voce[articolo_CONTA_NUMERI])articolo_CONTA_NUMERI++;if(!articolo_CONTA_NUMERI){informativa_SMS="No search pattern";return;}for(int 순번=1;순번<=durata_VALORE;순번++){int dati_funzione=(INDICE_VALORE+순번)%(durata_VALORE?durata_VALORE:1),안쪽순번=0;while(안쪽순번<articolo_CONTA_NUMERI&&dati_funzione+안쪽순번<durata_VALORE&&testo[dati_funzione+안쪽순번]==(unsigned char)TROVA_voce[안쪽순번])안쪽순번++;if(안쪽순번==articolo_CONTA_NUMERI){INDICE_VALORE=dati_funzione;informativa_SMS="Match";return;}}informativa_SMS="Pattern not found";}
static int prompt(int Valore_categoria){
    int articolo_CONTA_NUMERI=0;comando[0]=0;
    for(;;){spostare_VALORE(riga_CONTA_NUMERI,1);글내보내기("\033[0m\033[2K");byte_dati(Valore_categoria);글내보내기(comando);allineato();Guida_area=Valore_categoria;int 셋째순번=누름값();Guida_area=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(articolo_CONTA_NUMERI){articolo_CONTA_NUMERI--;while(articolo_CONTA_NUMERI>0&&((unsigned char)comando[articolo_CONTA_NUMERI]&192)==128)articolo_CONTA_NUMERI--;comando[articolo_CONTA_NUMERI]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&articolo_CONTA_NUMERI<120){comando[articolo_CONTA_NUMERI++]=셋째순번;comando[articolo_CONTA_NUMERI]=0;}
    }
    if(Valore_categoria=='/'){for(int 순번=0;순번<=articolo_CONTA_NUMERI;순번++)TROVA_voce[순번]=comando[순번];TROVA_Avanti();return 0;}
    if(같은지(comando,"q!"))return 1;
    if(같은지(comando,"q")){if(!변경됨)return 1;informativa_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(comando,"wq")||같은지(comando,"x"))return Store_VALORE();
    if(같은지(comando,"w")){Store_VALORE();return 0;}
    if(comando[0]=='w'&&comando[1]==' '){int 순번=2;while(comando[순번]==' ')순번++;int Dimensione=articolo_CONTA_NUMERI-순번;if(Dimensione<1||Dimensione>63){informativa_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Dimensione;안쪽순번++)File_voce_nome[안쪽순번]=comando[순번+안쪽순번];File_voce_nome[Dimensione]=0;Store_VALORE();return 0;}
    int riga_di_ingresso=0;for(int 순번=0;순번<articolo_CONTA_NUMERI;순번++){if(comando[순번]<'0'||comando[순번]>'9'){riga_di_ingresso=0;break;}riga_di_ingresso=riga_di_ingresso*10+comando[순번]-'0';if(riga_di_ingresso>16384){riga_di_ingresso=0;break;}}
    if(riga_di_ingresso){INDICE_VALORE=0;while(--riga_di_ingresso&&INDICE_VALORE<durata_VALORE){INDICE_VALORE=chiudere_SCARTO(INDICE_VALORE);if(INDICE_VALORE<durata_VALORE)INDICE_VALORE++;}return 0;}
    informativa_SMS="Unknown vi command";return 0;
}
int START_USER_app(int 무시값){
    (void)무시값;if(USER_argomento_CONTA_NUMERI()!=1||USER_argomento(0,File_voce_nome,sizeof(File_voce_nome))<0){글내보내기("Usage: vi FILE\n");allineato();return 2;}
    int handle_di_file=aperto_File(File_voce_nome,di_sola_lettura_VALORE,0);
    if(handle_di_file>=0){int articolo_CONTA_NUMERI=dimensioni_del_file(handle_di_file);if(articolo_CONTA_NUMERI<0||articolo_CONTA_NUMERI>Editor_capacità){Chiudi_File(handle_di_file);return 1;}durata_VALORE=파일자료읽기(handle_di_file,testo,articolo_CONTA_NUMERI);Chiudi_File(handle_di_file);if(durata_VALORE!=articolo_CONTA_NUMERI)return 1;for(int 순번=0;순번<durata_VALORE;순번++)if(!testo[순번]){글내보내기("vi: NUL byte in text file\n");allineato();return 1;}}
    else if(numero_errore!=2){글내보내기("vi: cannot read file\n");allineato();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");allineato();return 1;}COLONNE=흐린색&65535;riga_CONTA_NUMERI=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");allineato();
    int interlinea_parte=0,esci_app=0;
    while(!esci_app){Disegno_schermata();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();informativa_SMS=0;
        if(셋째순번==1001){Verticale(-1);continue;}if(셋째순번==1002){Verticale(1);continue;}if(셋째순번==1003){INDICE_VALORE=Avanti_articolo(INDICE_VALORE);continue;}if(셋째순번==1004){INDICE_VALORE=Indietro(INDICE_VALORE);continue;}
        if(셋째순번==1005){INDICE_VALORE=avvia(INDICE_VALORE);continue;}if(셋째순번==1006){INDICE_VALORE=chiudere_SCARTO(INDICE_VALORE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<riga_CONTA_NUMERI-2;순번++)Verticale(셋째순번==1008?-1:1);continue;}
        if(inserire){
            if(셋째순번==27||셋째순번==3){inserire=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDICE_VALORE)바이트지우기(Indietro(INDICE_VALORE),INDICE_VALORE);continue;}
            if(셋째순번==1007){if(INDICE_VALORE<durata_VALORE)바이트지우기(INDICE_VALORE,Avanti_articolo(INDICE_VALORE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECONDO_VALORE[4];SECONDO_VALORE[0]=셋째순번;int articolo_CONTA_NUMERI=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!articolo_CONTA_NUMERI){informativa_SMS="Invalid UTF-8";continue;}int valido=1;for(int 순번=1;순번<articolo_CONTA_NUMERI;순번++){int punto_di_codice=누름값();if(punto_di_codice<128||punto_di_codice>191){In_sospeso_tasto=punto_di_codice;valido=0;break;}SECONDO_VALORE[순번]=punto_di_codice;}
                if(valido)Aggiunta_VALORE(SECONDO_VALORE,articolo_CONTA_NUMERI);
            }continue;
        }
        if(interlinea_parte){int dati_funzione=interlinea_parte;interlinea_parte=0;if(dati_funzione=='g'&&셋째순번=='g'){INDICE_VALORE=0;continue;}if(dati_funzione=='Z'&&셋째순번=='Z'){esci_app=Store_VALORE();continue;}if((dati_funzione=='d'&&셋째순번=='d')||(dati_funzione=='y'&&셋째순번=='y')){int 첫째값=avvia(INDICE_VALORE),SECONDO_VALORE=chiudere_SCARTO(INDICE_VALORE);if(SECONDO_VALORE<durata_VALORE)SECONDO_VALORE++;copiare_durata=SECONDO_VALORE-첫째값;for(int 순번=0;순번<copiare_durata;순번++)복사자료[순번]=testo[첫째값+순번];if(dati_funzione=='d')바이트지우기(첫째값,SECONDO_VALORE);continue;}}
        if(셋째순번=='i'){inserire=1;continue;}if(셋째순번=='a'){if(INDICE_VALORE<chiudere_SCARTO(INDICE_VALORE))INDICE_VALORE=Avanti_articolo(INDICE_VALORE);inserire=1;continue;}
        if(셋째순번=='I'){INDICE_VALORE=avvia(INDICE_VALORE);inserire=1;continue;}if(셋째순번=='A'){INDICE_VALORE=chiudere_SCARTO(INDICE_VALORE);inserire=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char riga_chiudere='\n';INDICE_VALORE=셋째순번=='o'?chiudere_SCARTO(INDICE_VALORE):avvia(INDICE_VALORE);if(Aggiunta_VALORE(&riga_chiudere,1)){if(셋째순번=='O')INDICE_VALORE--;inserire=1;}continue;}
        if(셋째순번=='h'){INDICE_VALORE=Indietro(INDICE_VALORE);continue;}if(셋째순번=='l'){INDICE_VALORE=Avanti_articolo(INDICE_VALORE);continue;}if(셋째순번=='j'){Verticale(1);continue;}if(셋째순번=='k'){Verticale(-1);continue;}
        if(셋째순번=='0'){INDICE_VALORE=avvia(INDICE_VALORE);continue;}if(셋째순번=='$'){INDICE_VALORE=chiudere_SCARTO(INDICE_VALORE);continue;}if(셋째순번=='G'){INDICE_VALORE=avvia(durata_VALORE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){interlinea_parte=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDICE_VALORE<durata_VALORE)바이트지우기(INDICE_VALORE,Avanti_articolo(INDICE_VALORE));continue;}
        if(셋째순번=='p'&&copiare_durata){INDICE_VALORE=chiudere_SCARTO(INDICE_VALORE);if(INDICE_VALORE<durata_VALORE)INDICE_VALORE++;Aggiunta_VALORE(복사자료,copiare_durata);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_capacità;순번++){unsigned char SECONDO_VALORE=testo[순번];testo[순번]=annullare_dati[순번];annullare_dati[순번]=SECONDO_VALORE;}int articolo_CONTA_NUMERI=durata_VALORE;durata_VALORE=annullare_durata;annullare_durata=articolo_CONTA_NUMERI;articolo_CONTA_NUMERI=INDICE_VALORE;INDICE_VALORE=위쪽;위쪽=articolo_CONTA_NUMERI;articolo_CONTA_NUMERI=변경됨;변경됨=annullare_Modifiche;annullare_Modifiche=articolo_CONTA_NUMERI;continue;}
        if(셋째순번==':'||셋째순번=='/'){esci_app=prompt(셋째순번);continue;}if(셋째순번=='n'){TROVA_Avanti();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");allineato();사용자호출(16,2,0,0,0,0,0);return 0;
}
