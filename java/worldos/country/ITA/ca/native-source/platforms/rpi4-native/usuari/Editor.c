/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Editor_capacitat 16384
static unsigned char SMS[Editor_capacitat],desfer_dades[Editor_capacitat],복사자료[Editor_capacitat],mesura_dades[1024];
static int durada_VALOR,INDEX_VALOR,맨위,왼쪽,변경됨,inserir,desfer_durada,위쪽,desfer_Canvis,되돌림있음,copiar_durada,사용량,COLUMNES=68,FILA_COMPT=19;
static char arxiu_introducció_nom[64],Ordre[128],BUSCA_introducció[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned pendent_Clau;
static int ajuda_Categoria,Estat_IMATGE,Estat_cua;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)mesura_dades,사용량,0,0,0);사용량=0;}}
static void byte_dades(unsigned codi_de_caràcter){if(Estat_IMATGE){if((codi_de_caràcter&192)!=128){Estat_cua+=codi_de_caràcter>=196?2:1;}if(Estat_cua>=COLUMNES)return;}if(사용량==(int)sizeof(mesura_dades))출력비우기();mesura_dades[사용량++]=codi_de_caràcter;}
static void 글내보내기(const char *cadena_dades){while(*cadena_dades)byte_dades((unsigned char)*cadena_dades++);}
static void 수치(unsigned element_COMPT){char SEGON_VALOR[12];int 순번=0;do{SEGON_VALOR[순번++]='0'+element_COMPT%10;element_COMPT/=10;}while(element_COMPT);while(순번)byte_dades(SEGON_VALOR[--순번]);}
static void moure_VALOR(int FILA_càrrec,int COLUMNA_càrrec){글내보내기("\033[");수치(FILA_càrrec);byte_dades(';');수치(COLUMNA_càrrec);byte_dades('H');}
static int 이전항목(int dades_càrrec){if(dades_càrrec){dades_càrrec--;while(dades_càrrec>0&&(SMS[dades_càrrec]&192)==128)dades_càrrec--;}return dades_càrrec;}
static int Següent_element(int dades_càrrec){if(dades_càrrec<durada_VALOR){dades_càrrec++;while(dades_càrrec<durada_VALOR&&(SMS[dades_càrrec]&192)==128)dades_càrrec++;}return dades_càrrec;}
static int Executa_2(int dades_càrrec){while(dades_càrrec>0&&SMS[dades_càrrec-1]!='\n')dades_càrrec--;return dades_càrrec;}
static int finalitzar_DESPLAÇAMENT(int dades_càrrec){while(dades_càrrec<durada_VALOR&&SMS[dades_càrrec]!='\n')dades_càrrec++;return dades_càrrec;}
static int 너비(unsigned codi_de_caràcter){return codi_de_caràcter>=196?2:1;}
static int COLUMNA(int dades_càrrec){int codi_de_caràcter=0;for(int 순번=Executa_2(dades_càrrec);순번<dades_càrrec;순번=Següent_element(순번))codi_de_caràcter+=SMS[순번]=='\t'?4-codi_de_caràcter%4:너비(SMS[순번]);return codi_de_caràcter;}
static void punt_de_control(void){for(int 순번=0;순번<durada_VALOR;순번++)desfer_dades[순번]=SMS[순번];desfer_durada=durada_VALOR;위쪽=INDEX_VALOR;desfer_Canvis=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){punt_de_control();for(int 순번=도착위치;순번<durada_VALOR;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];durada_VALOR-=도착위치-출발위치;INDEX_VALOR=출발위치;변경됨=1;}
static int Annexa_VALOR(const unsigned char *cadena_dades,int element_COMPT){if(element_COMPT>Editor_capacitat-durada_VALOR){알림문="File full (16384 bytes)";return 0;}punt_de_control();for(int 순번=durada_VALOR-1;순번>=INDEX_VALOR;순번--)SMS[순번+element_COMPT]=SMS[순번];for(int 순번=0;순번<element_COMPT;순번++)SMS[INDEX_VALOR+순번]=cadena_dades[순번];durada_VALOR+=element_COMPT;INDEX_VALOR+=element_COMPT;변경됨=1;return 1;}
static void Vertical(int 차이){int COLUMNA_càrrec=COLUMNA(INDEX_VALOR),dades_càrrec=Executa_2(INDEX_VALOR);if(차이<0){if(!dades_càrrec)return;dades_càrrec=Executa_2(dades_càrrec-1);}else{dades_càrrec=finalitzar_DESPLAÇAMENT(dades_càrrec);if(dades_càrrec==durada_VALOR)return;dades_càrrec++;}int codi_de_caràcter=0;while(dades_càrrec<durada_VALOR&&SMS[dades_càrrec]!='\n'&&codi_de_caràcter<COLUMNA_càrrec){codi_de_caràcter+=SMS[dades_càrrec]=='\t'?4-codi_de_caràcter%4:너비(SMS[dades_càrrec]);dades_càrrec=Següent_element(dades_càrrec);}INDEX_VALOR=dades_càrrec;}
static void 화면그리기(void){
    if(INDEX_VALOR>durada_VALOR)INDEX_VALOR=durada_VALOR;if(맨위>INDEX_VALOR)맨위=Executa_2(INDEX_VALOR);맨위=Executa_2(맨위);
    int FILA_càrrec=0;for(int 순번=맨위;순번<INDEX_VALOR;순번++)if(SMS[순번]=='\n')FILA_càrrec++;
    while(FILA_càrrec>=FILA_COMPT-1){맨위=finalitzar_DESPLAÇAMENT(맨위);if(맨위<durada_VALOR)맨위++;FILA_càrrec--;}
    int COLUMNA_càrrec=COLUMNA(INDEX_VALOR);if(COLUMNA_càrrec<왼쪽)왼쪽=COLUMNA_càrrec;if(COLUMNA_càrrec-왼쪽>=COLUMNES-1)왼쪽=COLUMNA_càrrec-COLUMNES+2;
    글내보내기("\033[?25l");int dades_càrrec=맨위;
    for(int 반환값=0;반환값<FILA_COMPT-1;반환값++){
        moure_VALOR(반환값+1,1);글내보내기("\033[0m\033[2K");int codi_de_caràcter=0,그려진상태=0;
        if(dades_càrrec>=durada_VALOR&&반환값>FILA_càrrec){글내보내기("\033[90m~\033[0m");continue;}
        while(dades_càrrec<durada_VALOR&&SMS[dades_càrrec]!='\n'){
            int Següent_DESPLAÇAMENT=Següent_element(dades_càrrec),너비값=SMS[dades_càrrec]=='\t'?4-codi_de_caràcter%4:너비(SMS[dades_càrrec]);
            if(codi_de_caràcter>=왼쪽&&codi_de_caràcter-왼쪽+너비값<COLUMNES){
                if(SMS[dades_càrrec]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_dades(' ');}else if(SMS[dades_càrrec]<32||SMS[dades_càrrec]==127){byte_dades('?');}else for(int 안쪽순번=dades_càrrec;안쪽순번<Següent_DESPLAÇAMENT;안쪽순번++)byte_dades(SMS[안쪽순번]);그려진상태+=너비값;
            }codi_de_caràcter+=너비값;dades_càrrec=Següent_DESPLAÇAMENT;
        }
        (void)그려진상태;if(dades_càrrec<durada_VALOR)dades_càrrec++;
    }
    moure_VALOR(FILA_COMPT,1);글내보내기("\033[7m\033[2K");Estat_IMATGE=1;Estat_cua=0;글내보내기(inserir?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(arxiu_introducció_nom[이름바이트수]&&이름바이트수<30)byte_dades(arxiu_introducció_nom[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int línia=1;for(int 순번=0;순번<INDEX_VALOR;순번++)if(SMS[순번]=='\n')línia++;수치(línia);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int element_COMPT=0;글내보내기(" | ");while(알림문[element_COMPT]&&element_COMPT<20)byte_dades(알림문[element_COMPT++]);}
    Estat_IMATGE=0;글내보내기("\033[0m");moure_VALOR(FILA_càrrec+1,COLUMNA_càrrec-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(pendent_Clau){int 셋째순번=pendent_Clau;pendent_Clau=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Mida=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNES!=(int)(Mida&65535)||FILA_COMPT!=(int)(Mida>>16)){
            COLUMNES=Mida&65535;FILA_COMPT=Mida>>16;화면그리기();
            if(ajuda_Categoria){moure_VALOR(FILA_COMPT,1);글내보내기("\033[0m\033[2K");byte_dades(ajuda_Categoria);글내보내기(Ordre);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){pendent_Clau=셋째순번;return 27;}
    int element_COMPT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){element_COMPT=element_COMPT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return element_COMPT==3?1007:element_COMPT==5?1008:element_COMPT==6?1009:element_COMPT==1?1005:element_COMPT==4?1006:27;return 27;}return 27;
}
static int Store_VALOR(void){
    int arxiu_control_7f4cdfd5=crear_arxiu(arxiu_introducció_nom,lectura_escriptura|없으면만들기|내용비우기,0600);if(arxiu_control_7f4cdfd5<0){알림문="Cannot open for save";return 0;}
    intptr_t element_COMPT=escriure_arxiu_dades(arxiu_control_7f4cdfd5,SMS,durada_VALOR);Tanca_arxiu(arxiu_control_7f4cdfd5);if(element_COMPT!=durada_VALOR){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SEGON_VALOR){while(*첫째값&&*첫째값==*SEGON_VALOR){첫째값++;SEGON_VALOR++;}return *첫째값==*SEGON_VALOR;}
static void BUSCA_Següent(void){int element_COMPT=0;while(BUSCA_introducció[element_COMPT])element_COMPT++;if(!element_COMPT){알림문="No search pattern";return;}for(int 순번=1;순번<=durada_VALOR;순번++){int dades_càrrec=(INDEX_VALOR+순번)%(durada_VALOR?durada_VALOR:1),안쪽순번=0;while(안쪽순번<element_COMPT&&dades_càrrec+안쪽순번<durada_VALOR&&SMS[dades_càrrec+안쪽순번]==(unsigned char)BUSCA_introducció[안쪽순번])안쪽순번++;if(안쪽순번==element_COMPT){INDEX_VALOR=dades_càrrec;알림문="Match";return;}}알림문="Pattern not found";}
static int sol_licitar(int Categoria_VALOR){
    int element_COMPT=0;Ordre[0]=0;
    for(;;){moure_VALOR(FILA_COMPT,1);글내보내기("\033[0m\033[2K");byte_dades(Categoria_VALOR);글내보내기(Ordre);출력비우기();ajuda_Categoria=Categoria_VALOR;int 셋째순번=누름값();ajuda_Categoria=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(element_COMPT){element_COMPT--;while(element_COMPT>0&&((unsigned char)Ordre[element_COMPT]&192)==128)element_COMPT--;Ordre[element_COMPT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&element_COMPT<120){Ordre[element_COMPT++]=셋째순번;Ordre[element_COMPT]=0;}
    }
    if(Categoria_VALOR=='/'){for(int 순번=0;순번<=element_COMPT;순번++)BUSCA_introducció[순번]=Ordre[순번];BUSCA_Següent();return 0;}
    if(같은지(Ordre,"q!"))return 1;
    if(같은지(Ordre,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Ordre,"wq")||같은지(Ordre,"x"))return Store_VALOR();
    if(같은지(Ordre,"w")){Store_VALOR();return 0;}
    if(Ordre[0]=='w'&&Ordre[1]==' '){int 순번=2;while(Ordre[순번]==' ')순번++;int Mida=element_COMPT-순번;if(Mida<1||Mida>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Mida;안쪽순번++)arxiu_introducció_nom[안쪽순번]=Ordre[순번+안쪽순번];arxiu_introducció_nom[Mida]=0;Store_VALOR();return 0;}
    int línia=0;for(int 순번=0;순번<element_COMPT;순번++){if(Ordre[순번]<'0'||Ordre[순번]>'9'){línia=0;break;}línia=línia*10+Ordre[순번]-'0';if(línia>16384){línia=0;break;}}
    if(línia){INDEX_VALOR=0;while(--línia&&INDEX_VALOR<durada_VALOR){INDEX_VALOR=finalitzar_DESPLAÇAMENT(INDEX_VALOR);if(INDEX_VALOR<durada_VALOR)INDEX_VALOR++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Inici_usuari_programa(int 무시값){
    (void)무시값;if(usuari_arg_COMPT()!=1||usuari_arg(0,arxiu_introducció_nom,sizeof(arxiu_introducció_nom))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int arxiu_control_7f4cdfd5=crear_arxiu(arxiu_introducció_nom,només_de_lectura_VALOR,0);
    if(arxiu_control_7f4cdfd5>=0){int element_COMPT=arxiu_canviar_la_mida(arxiu_control_7f4cdfd5);if(element_COMPT<0||element_COMPT>Editor_capacitat){Tanca_arxiu(arxiu_control_7f4cdfd5);return 1;}durada_VALOR=tancar_arxiu_dades(arxiu_control_7f4cdfd5,SMS,element_COMPT);Tanca_arxiu(arxiu_control_7f4cdfd5);if(durada_VALOR!=element_COMPT)return 1;for(int 순번=0;순번<durada_VALOR;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(número_d_error!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNES=흐린색&65535;FILA_COMPT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,sortir_programa=0;
    while(!sortir_programa){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Vertical(-1);continue;}if(셋째순번==1002){Vertical(1);continue;}if(셋째순번==1003){INDEX_VALOR=Següent_element(INDEX_VALOR);continue;}if(셋째순번==1004){INDEX_VALOR=이전항목(INDEX_VALOR);continue;}
        if(셋째순번==1005){INDEX_VALOR=Executa_2(INDEX_VALOR);continue;}if(셋째순번==1006){INDEX_VALOR=finalitzar_DESPLAÇAMENT(INDEX_VALOR);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<FILA_COMPT-2;순번++)Vertical(셋째순번==1008?-1:1);continue;}
        if(inserir){
            if(셋째순번==27||셋째순번==3){inserir=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALOR)바이트지우기(이전항목(INDEX_VALOR),INDEX_VALOR);continue;}
            if(셋째순번==1007){if(INDEX_VALOR<durada_VALOR)바이트지우기(INDEX_VALOR,Següent_element(INDEX_VALOR));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SEGON_VALOR[4];SEGON_VALOR[0]=셋째순번;int element_COMPT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!element_COMPT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<element_COMPT;순번++){int codi_de_caràcter=누름값();if(codi_de_caràcter<128||codi_de_caràcter>191){pendent_Clau=codi_de_caràcter;유효함=0;break;}SEGON_VALOR[순번]=codi_de_caràcter;}
                if(유효함)Annexa_VALOR(SEGON_VALOR,element_COMPT);
            }continue;
        }
        if(앞부분){int dades_càrrec=앞부분;앞부분=0;if(dades_càrrec=='g'&&셋째순번=='g'){INDEX_VALOR=0;continue;}if(dades_càrrec=='Z'&&셋째순번=='Z'){sortir_programa=Store_VALOR();continue;}if((dades_càrrec=='d'&&셋째순번=='d')||(dades_càrrec=='y'&&셋째순번=='y')){int 첫째값=Executa_2(INDEX_VALOR),SEGON_VALOR=finalitzar_DESPLAÇAMENT(INDEX_VALOR);if(SEGON_VALOR<durada_VALOR)SEGON_VALOR++;copiar_durada=SEGON_VALOR-첫째값;for(int 순번=0;순번<copiar_durada;순번++)복사자료[순번]=SMS[첫째값+순번];if(dades_càrrec=='d')바이트지우기(첫째값,SEGON_VALOR);continue;}}
        if(셋째순번=='i'){inserir=1;continue;}if(셋째순번=='a'){if(INDEX_VALOR<finalitzar_DESPLAÇAMENT(INDEX_VALOR))INDEX_VALOR=Següent_element(INDEX_VALOR);inserir=1;continue;}
        if(셋째순번=='I'){INDEX_VALOR=Executa_2(INDEX_VALOR);inserir=1;continue;}if(셋째순번=='A'){INDEX_VALOR=finalitzar_DESPLAÇAMENT(INDEX_VALOR);inserir=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char línia_finalitzar='\n';INDEX_VALOR=셋째순번=='o'?finalitzar_DESPLAÇAMENT(INDEX_VALOR):Executa_2(INDEX_VALOR);if(Annexa_VALOR(&línia_finalitzar,1)){if(셋째순번=='O')INDEX_VALOR--;inserir=1;}continue;}
        if(셋째순번=='h'){INDEX_VALOR=이전항목(INDEX_VALOR);continue;}if(셋째순번=='l'){INDEX_VALOR=Següent_element(INDEX_VALOR);continue;}if(셋째순번=='j'){Vertical(1);continue;}if(셋째순번=='k'){Vertical(-1);continue;}
        if(셋째순번=='0'){INDEX_VALOR=Executa_2(INDEX_VALOR);continue;}if(셋째순번=='$'){INDEX_VALOR=finalitzar_DESPLAÇAMENT(INDEX_VALOR);continue;}if(셋째순번=='G'){INDEX_VALOR=Executa_2(durada_VALOR);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALOR<durada_VALOR)바이트지우기(INDEX_VALOR,Següent_element(INDEX_VALOR));continue;}
        if(셋째순번=='p'&&copiar_durada){INDEX_VALOR=finalitzar_DESPLAÇAMENT(INDEX_VALOR);if(INDEX_VALOR<durada_VALOR)INDEX_VALOR++;Annexa_VALOR(복사자료,copiar_durada);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_capacitat;순번++){unsigned char SEGON_VALOR=SMS[순번];SMS[순번]=desfer_dades[순번];desfer_dades[순번]=SEGON_VALOR;}int element_COMPT=durada_VALOR;durada_VALOR=desfer_durada;desfer_durada=element_COMPT;element_COMPT=INDEX_VALOR;INDEX_VALOR=위쪽;위쪽=element_COMPT;element_COMPT=변경됨;변경됨=desfer_Canvis;desfer_Canvis=element_COMPT;continue;}
        if(셋째순번==':'||셋째순번=='/'){sortir_programa=sol_licitar(셋째순번);continue;}if(셋째순번=='n'){BUSCA_Següent();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
