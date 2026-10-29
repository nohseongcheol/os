/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Editor_capaciteit 16384
static unsigned char tekst[Editor_capaciteit],ongedaan_maken_gegevens[Editor_capaciteit],복사자료[Editor_capaciteit],HR_gegevens[1024];
static int tijdsduur_WAARDE,INDEX_WAARDE,맨위,왼쪽,변경됨,Invoegen,ongedaan_maken_tijdsduur,위쪽,ongedaan_maken_Wijzigingen,되돌림있음,kopiëren_tijdsduur,사용량,KOLOMMEN=68,RIJ_AANTAL=19;
static char Bestand_invoer_naam[64],opdracht[128],Zoeken_invoer[128];
static const char *kennisgeving_sms="NORMAL  i:insert  :w:save  :q:quit";
static unsigned In_behandeling_toets;
static int help_gebied,Status_kopie,Status_wachtrij;
static void leegmaken(void){if(사용량){사용자호출(1,1,(uintptr_t)HR_gegevens,사용량,0,0,0);사용량=0;}}
static void byte_gegevens(unsigned codepoint){if(Status_kopie){if((codepoint&192)!=128){Status_wachtrij+=codepoint>=196?2:1;}if(Status_wachtrij>=KOLOMMEN)return;}if(사용량==(int)sizeof(HR_gegevens))leegmaken();HR_gegevens[사용량++]=codepoint;}
static void 글내보내기(const char *tekenreeks_gegevens){while(*tekenreeks_gegevens)byte_gegevens((unsigned char)*tekenreeks_gegevens++);}
static void 수치(unsigned item_AANTAL){char SECONDE_WAARDE[12];int 순번=0;do{SECONDE_WAARDE[순번++]='0'+item_AANTAL%10;item_AANTAL/=10;}while(item_AANTAL);while(순번)byte_gegevens(SECONDE_WAARDE[--순번]);}
static void verplaatsen_WAARDE_83b651b8(int RIJ_functie,int KOLOM_functie){글내보내기("\033[");수치(RIJ_functie);byte_gegevens(';');수치(KOLOM_functie);byte_gegevens('H');}
static int Vorige(int gegevens_functie){if(gegevens_functie){gegevens_functie--;while(gegevens_functie>0&&(tekst[gegevens_functie]&192)==128)gegevens_functie--;}return gegevens_functie;}
static int Volgende_item(int gegevens_functie){if(gegevens_functie<tijdsduur_WAARDE){gegevens_functie++;while(gegevens_functie<tijdsduur_WAARDE&&(tekst[gegevens_functie]&192)==128)gegevens_functie++;}return gegevens_functie;}
static int starten(int gegevens_functie){while(gegevens_functie>0&&tekst[gegevens_functie-1]!='\n')gegevens_functie--;return gegevens_functie;}
static int beëindigen_VERSCHUIVING(int gegevens_functie){while(gegevens_functie<tijdsduur_WAARDE&&tekst[gegevens_functie]!='\n')gegevens_functie++;return gegevens_functie;}
static int 너비(unsigned codepoint){return codepoint>=196?2:1;}
static int KOLOM(int gegevens_functie){int codepoint=0;for(int 순번=starten(gegevens_functie);순번<gegevens_functie;순번=Volgende_item(순번))codepoint+=tekst[순번]=='\t'?4-codepoint%4:너비(tekst[순번]);return codepoint;}
static void controlepunt(void){for(int 순번=0;순번<tijdsduur_WAARDE;순번++)ongedaan_maken_gegevens[순번]=tekst[순번];ongedaan_maken_tijdsduur=tijdsduur_WAARDE;위쪽=INDEX_WAARDE;ongedaan_maken_Wijzigingen=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){controlepunt();for(int 순번=도착위치;순번<tijdsduur_WAARDE;순번++)tekst[출발위치+순번-도착위치]=tekst[순번];tijdsduur_WAARDE-=도착위치-출발위치;INDEX_WAARDE=출발위치;변경됨=1;}
static int toevoegen_WAARDE(const unsigned char *tekenreeks_gegevens,int item_AANTAL){if(item_AANTAL>Editor_capaciteit-tijdsduur_WAARDE){kennisgeving_sms="File full (16384 bytes)";return 0;}controlepunt();for(int 순번=tijdsduur_WAARDE-1;순번>=INDEX_WAARDE;순번--)tekst[순번+item_AANTAL]=tekst[순번];for(int 순번=0;순번<item_AANTAL;순번++)tekst[INDEX_WAARDE+순번]=tekenreeks_gegevens[순번];tijdsduur_WAARDE+=item_AANTAL;INDEX_WAARDE+=item_AANTAL;변경됨=1;return 1;}
static void Verticaal(int 차이){int KOLOM_functie=KOLOM(INDEX_WAARDE),gegevens_functie=starten(INDEX_WAARDE);if(차이<0){if(!gegevens_functie)return;gegevens_functie=starten(gegevens_functie-1);}else{gegevens_functie=beëindigen_VERSCHUIVING(gegevens_functie);if(gegevens_functie==tijdsduur_WAARDE)return;gegevens_functie++;}int codepoint=0;while(gegevens_functie<tijdsduur_WAARDE&&tekst[gegevens_functie]!='\n'&&codepoint<KOLOM_functie){codepoint+=tekst[gegevens_functie]=='\t'?4-codepoint%4:너비(tekst[gegevens_functie]);gegevens_functie=Volgende_item(gegevens_functie);}INDEX_WAARDE=gegevens_functie;}
static void Tekenen_scherm(void){
    if(INDEX_WAARDE>tijdsduur_WAARDE)INDEX_WAARDE=tijdsduur_WAARDE;if(맨위>INDEX_WAARDE)맨위=starten(INDEX_WAARDE);맨위=starten(맨위);
    int RIJ_functie=0;for(int 순번=맨위;순번<INDEX_WAARDE;순번++)if(tekst[순번]=='\n')RIJ_functie++;
    while(RIJ_functie>=RIJ_AANTAL-1){맨위=beëindigen_VERSCHUIVING(맨위);if(맨위<tijdsduur_WAARDE)맨위++;RIJ_functie--;}
    int KOLOM_functie=KOLOM(INDEX_WAARDE);if(KOLOM_functie<왼쪽)왼쪽=KOLOM_functie;if(KOLOM_functie-왼쪽>=KOLOMMEN-1)왼쪽=KOLOM_functie-KOLOMMEN+2;
    글내보내기("\033[?25l");int gegevens_functie=맨위;
    for(int 반환값=0;반환값<RIJ_AANTAL-1;반환값++){
        verplaatsen_WAARDE_83b651b8(반환값+1,1);글내보내기("\033[0m\033[2K");int codepoint=0,그려진상태=0;
        if(gegevens_functie>=tijdsduur_WAARDE&&반환값>RIJ_functie){글내보내기("\033[90m~\033[0m");continue;}
        while(gegevens_functie<tijdsduur_WAARDE&&tekst[gegevens_functie]!='\n'){
            int Volgende_VERSCHUIVING=Volgende_item(gegevens_functie),너비값=tekst[gegevens_functie]=='\t'?4-codepoint%4:너비(tekst[gegevens_functie]);
            if(codepoint>=왼쪽&&codepoint-왼쪽+너비값<KOLOMMEN){
                if(tekst[gegevens_functie]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_gegevens(' ');}else if(tekst[gegevens_functie]<32||tekst[gegevens_functie]==127){byte_gegevens('?');}else for(int 안쪽순번=gegevens_functie;안쪽순번<Volgende_VERSCHUIVING;안쪽순번++)byte_gegevens(tekst[안쪽순번]);그려진상태+=너비값;
            }codepoint+=너비값;gegevens_functie=Volgende_VERSCHUIVING;
        }
        (void)그려진상태;if(gegevens_functie<tijdsduur_WAARDE)gegevens_functie++;
    }
    verplaatsen_WAARDE_83b651b8(RIJ_AANTAL,1);글내보내기("\033[7m\033[2K");Status_kopie=1;Status_wachtrij=0;글내보내기(Invoegen?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Bestand_invoer_naam[이름바이트수]&&이름바이트수<30)byte_gegevens(Bestand_invoer_naam[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int invoerregel=1;for(int 순번=0;순번<INDEX_WAARDE;순번++)if(tekst[순번]=='\n')invoerregel++;수치(invoerregel);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(kennisgeving_sms){int item_AANTAL=0;글내보내기(" | ");while(kennisgeving_sms[item_AANTAL]&&item_AANTAL<20)byte_gegevens(kennisgeving_sms[item_AANTAL++]);}
    Status_kopie=0;글내보내기("\033[0m");verplaatsen_WAARDE_83b651b8(RIJ_functie+1,KOLOM_functie-왼쪽+1);글내보내기("\033[?25h");leegmaken();
}
static int 누름값(void){
    if(In_behandeling_toets){int 셋째순번=In_behandeling_toets;In_behandeling_toets=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Grootte=사용자호출(16,3,0,0,0,0,0);
        if(KOLOMMEN!=(int)(Grootte&65535)||RIJ_AANTAL!=(int)(Grootte>>16)){
            KOLOMMEN=Grootte&65535;RIJ_AANTAL=Grootte>>16;Tekenen_scherm();
            if(help_gebied){verplaatsen_WAARDE_83b651b8(RIJ_AANTAL,1);글내보내기("\033[0m\033[2K");byte_gegevens(help_gebied);글내보내기(opdracht);leegmaken();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned actueel_functie=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-actueel_functie<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){In_behandeling_toets=셋째순번;return 27;}
    int item_AANTAL=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){item_AANTAL=item_AANTAL*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return item_AANTAL==3?1007:item_AANTAL==5?1008:item_AANTAL==6?1009:item_AANTAL==1?1005:item_AANTAL==4?1006:27;return 27;}return 27;
}
static int Store_WAARDE(void){
    int bestandsingang=open_Bestand(Bestand_invoer_naam,lezen_schrijven|없으면만들기|afkappen_Inhoud,0600);if(bestandsingang<0){kennisgeving_sms="Cannot open for save";return 0;}
    intptr_t item_AANTAL=schrijven_Bestand_gegevens(bestandsingang,tekst,tijdsduur_WAARDE);Sluiten_Bestand(bestandsingang);if(item_AANTAL!=tijdsduur_WAARDE){kennisgeving_sms="Write failed";return 0;}변경됨=0;kennisgeving_sms="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECONDE_WAARDE){while(*첫째값&&*첫째값==*SECONDE_WAARDE){첫째값++;SECONDE_WAARDE++;}return *첫째값==*SECONDE_WAARDE;}
static void Zoeken_Volgende(void){int item_AANTAL=0;while(Zoeken_invoer[item_AANTAL])item_AANTAL++;if(!item_AANTAL){kennisgeving_sms="No search pattern";return;}for(int 순번=1;순번<=tijdsduur_WAARDE;순번++){int gegevens_functie=(INDEX_WAARDE+순번)%(tijdsduur_WAARDE?tijdsduur_WAARDE:1),안쪽순번=0;while(안쪽순번<item_AANTAL&&gegevens_functie+안쪽순번<tijdsduur_WAARDE&&tekst[gegevens_functie+안쪽순번]==(unsigned char)Zoeken_invoer[안쪽순번])안쪽순번++;if(안쪽순번==item_AANTAL){INDEX_WAARDE=gegevens_functie;kennisgeving_sms="Match";return;}}kennisgeving_sms="Pattern not found";}
static int prompt(int gebied_WAARDE){
    int item_AANTAL=0;opdracht[0]=0;
    for(;;){verplaatsen_WAARDE_83b651b8(RIJ_AANTAL,1);글내보내기("\033[0m\033[2K");byte_gegevens(gebied_WAARDE);글내보내기(opdracht);leegmaken();help_gebied=gebied_WAARDE;int 셋째순번=누름값();help_gebied=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(item_AANTAL){item_AANTAL--;while(item_AANTAL>0&&((unsigned char)opdracht[item_AANTAL]&192)==128)item_AANTAL--;opdracht[item_AANTAL]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&item_AANTAL<120){opdracht[item_AANTAL++]=셋째순번;opdracht[item_AANTAL]=0;}
    }
    if(gebied_WAARDE=='/'){for(int 순번=0;순번<=item_AANTAL;순번++)Zoeken_invoer[순번]=opdracht[순번];Zoeken_Volgende();return 0;}
    if(같은지(opdracht,"q!"))return 1;
    if(같은지(opdracht,"q")){if(!변경됨)return 1;kennisgeving_sms="Unsaved: :w or :q!";return 0;}
    if(같은지(opdracht,"wq")||같은지(opdracht,"x"))return Store_WAARDE();
    if(같은지(opdracht,"w")){Store_WAARDE();return 0;}
    if(opdracht[0]=='w'&&opdracht[1]==' '){int 순번=2;while(opdracht[순번]==' ')순번++;int Grootte=item_AANTAL-순번;if(Grootte<1||Grootte>63){kennisgeving_sms="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Grootte;안쪽순번++)Bestand_invoer_naam[안쪽순번]=opdracht[순번+안쪽순번];Bestand_invoer_naam[Grootte]=0;Store_WAARDE();return 0;}
    int invoerregel=0;for(int 순번=0;순번<item_AANTAL;순번++){if(opdracht[순번]<'0'||opdracht[순번]>'9'){invoerregel=0;break;}invoerregel=invoerregel*10+opdracht[순번]-'0';if(invoerregel>16384){invoerregel=0;break;}}
    if(invoerregel){INDEX_WAARDE=0;while(--invoerregel&&INDEX_WAARDE<tijdsduur_WAARDE){INDEX_WAARDE=beëindigen_VERSCHUIVING(INDEX_WAARDE);if(INDEX_WAARDE<tijdsduur_WAARDE)INDEX_WAARDE++;}return 0;}
    kennisgeving_sms="Unknown vi command";return 0;
}
int START_gebruiker_app(int 무시값){
    (void)무시값;if(gebruiker_argument_AANTAL()!=1||gebruiker_argument(0,Bestand_invoer_naam,sizeof(Bestand_invoer_naam))<0){글내보내기("Usage: vi FILE\n");leegmaken();return 2;}
    int bestandsingang=open_Bestand(Bestand_invoer_naam,alleen_lezen_WAARDE,0);
    if(bestandsingang>=0){int item_AANTAL=bestandsgrootte(bestandsingang);if(item_AANTAL<0||item_AANTAL>Editor_capaciteit){Sluiten_Bestand(bestandsingang);return 1;}tijdsduur_WAARDE=파일자료읽기(bestandsingang,tekst,item_AANTAL);Sluiten_Bestand(bestandsingang);if(tijdsduur_WAARDE!=item_AANTAL)return 1;for(int 순번=0;순번<tijdsduur_WAARDE;순번++)if(!tekst[순번]){글내보내기("vi: NUL byte in text file\n");leegmaken();return 1;}}
    else if(foutnummer!=2){글내보내기("vi: cannot read file\n");leegmaken();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");leegmaken();return 1;}KOLOMMEN=흐린색&65535;RIJ_AANTAL=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");leegmaken();
    int interlinie_tegel=0,sluiten_app=0;
    while(!sluiten_app){Tekenen_scherm();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();kennisgeving_sms=0;
        if(셋째순번==1001){Verticaal(-1);continue;}if(셋째순번==1002){Verticaal(1);continue;}if(셋째순번==1003){INDEX_WAARDE=Volgende_item(INDEX_WAARDE);continue;}if(셋째순번==1004){INDEX_WAARDE=Vorige(INDEX_WAARDE);continue;}
        if(셋째순번==1005){INDEX_WAARDE=starten(INDEX_WAARDE);continue;}if(셋째순번==1006){INDEX_WAARDE=beëindigen_VERSCHUIVING(INDEX_WAARDE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<RIJ_AANTAL-2;순번++)Verticaal(셋째순번==1008?-1:1);continue;}
        if(Invoegen){
            if(셋째순번==27||셋째순번==3){Invoegen=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_WAARDE)바이트지우기(Vorige(INDEX_WAARDE),INDEX_WAARDE);continue;}
            if(셋째순번==1007){if(INDEX_WAARDE<tijdsduur_WAARDE)바이트지우기(INDEX_WAARDE,Volgende_item(INDEX_WAARDE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECONDE_WAARDE[4];SECONDE_WAARDE[0]=셋째순번;int item_AANTAL=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!item_AANTAL){kennisgeving_sms="Invalid UTF-8";continue;}int geldig=1;for(int 순번=1;순번<item_AANTAL;순번++){int codepoint=누름값();if(codepoint<128||codepoint>191){In_behandeling_toets=codepoint;geldig=0;break;}SECONDE_WAARDE[순번]=codepoint;}
                if(geldig)toevoegen_WAARDE(SECONDE_WAARDE,item_AANTAL);
            }continue;
        }
        if(interlinie_tegel){int gegevens_functie=interlinie_tegel;interlinie_tegel=0;if(gegevens_functie=='g'&&셋째순번=='g'){INDEX_WAARDE=0;continue;}if(gegevens_functie=='Z'&&셋째순번=='Z'){sluiten_app=Store_WAARDE();continue;}if((gegevens_functie=='d'&&셋째순번=='d')||(gegevens_functie=='y'&&셋째순번=='y')){int 첫째값=starten(INDEX_WAARDE),SECONDE_WAARDE=beëindigen_VERSCHUIVING(INDEX_WAARDE);if(SECONDE_WAARDE<tijdsduur_WAARDE)SECONDE_WAARDE++;kopiëren_tijdsduur=SECONDE_WAARDE-첫째값;for(int 순번=0;순번<kopiëren_tijdsduur;순번++)복사자료[순번]=tekst[첫째값+순번];if(gegevens_functie=='d')바이트지우기(첫째값,SECONDE_WAARDE);continue;}}
        if(셋째순번=='i'){Invoegen=1;continue;}if(셋째순번=='a'){if(INDEX_WAARDE<beëindigen_VERSCHUIVING(INDEX_WAARDE))INDEX_WAARDE=Volgende_item(INDEX_WAARDE);Invoegen=1;continue;}
        if(셋째순번=='I'){INDEX_WAARDE=starten(INDEX_WAARDE);Invoegen=1;continue;}if(셋째순번=='A'){INDEX_WAARDE=beëindigen_VERSCHUIVING(INDEX_WAARDE);Invoegen=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char lijn_beëindigen='\n';INDEX_WAARDE=셋째순번=='o'?beëindigen_VERSCHUIVING(INDEX_WAARDE):starten(INDEX_WAARDE);if(toevoegen_WAARDE(&lijn_beëindigen,1)){if(셋째순번=='O')INDEX_WAARDE--;Invoegen=1;}continue;}
        if(셋째순번=='h'){INDEX_WAARDE=Vorige(INDEX_WAARDE);continue;}if(셋째순번=='l'){INDEX_WAARDE=Volgende_item(INDEX_WAARDE);continue;}if(셋째순번=='j'){Verticaal(1);continue;}if(셋째순번=='k'){Verticaal(-1);continue;}
        if(셋째순번=='0'){INDEX_WAARDE=starten(INDEX_WAARDE);continue;}if(셋째순번=='$'){INDEX_WAARDE=beëindigen_VERSCHUIVING(INDEX_WAARDE);continue;}if(셋째순번=='G'){INDEX_WAARDE=starten(tijdsduur_WAARDE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){interlinie_tegel=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_WAARDE<tijdsduur_WAARDE)바이트지우기(INDEX_WAARDE,Volgende_item(INDEX_WAARDE));continue;}
        if(셋째순번=='p'&&kopiëren_tijdsduur){INDEX_WAARDE=beëindigen_VERSCHUIVING(INDEX_WAARDE);if(INDEX_WAARDE<tijdsduur_WAARDE)INDEX_WAARDE++;toevoegen_WAARDE(복사자료,kopiëren_tijdsduur);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_capaciteit;순번++){unsigned char SECONDE_WAARDE=tekst[순번];tekst[순번]=ongedaan_maken_gegevens[순번];ongedaan_maken_gegevens[순번]=SECONDE_WAARDE;}int item_AANTAL=tijdsduur_WAARDE;tijdsduur_WAARDE=ongedaan_maken_tijdsduur;ongedaan_maken_tijdsduur=item_AANTAL;item_AANTAL=INDEX_WAARDE;INDEX_WAARDE=위쪽;위쪽=item_AANTAL;item_AANTAL=변경됨;변경됨=ongedaan_maken_Wijzigingen;ongedaan_maken_Wijzigingen=item_AANTAL;continue;}
        if(셋째순번==':'||셋째순번=='/'){sluiten_app=prompt(셋째순번);continue;}if(셋째순번=='n'){Zoeken_Volgende();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");leegmaken();사용자호출(16,2,0,0,0,0,0);return 0;
}
