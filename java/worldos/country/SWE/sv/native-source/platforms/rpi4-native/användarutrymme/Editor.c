/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Editor_kapacitet 16384
static unsigned char text[Editor_kapacitet],ångra_data[Editor_kapacitet],복사자료[Editor_kapacitet],KR_data[1024];
static int längd_värde,INDEX_värde,맨위,왼쪽,변경됨,Infoga,ångra_längd,위쪽,ångra_Ändringar,되돌림있음,kopia_längd,사용량,KOLUMNER=68,RAD_ANTAL=19;
static char fil_post_namn[64],kommando[128],Sök_post[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned väntar_Nyckel;
static int hjälp_område,status_BILD,status_kö;
static void tömma(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_data,사용량,0,0,0);사용량=0;}}
static void byte_data(unsigned kodpunkt){if(status_BILD){if((kodpunkt&192)!=128){status_kö+=kodpunkt>=196?2:1;}if(status_kö>=KOLUMNER)return;}if(사용량==(int)sizeof(KR_data))tömma();KR_data[사용량++]=kodpunkt;}
static void 글내보내기(const char *sträng_data){while(*sträng_data)byte_data((unsigned char)*sträng_data++);}
static void 수치(unsigned objekt_ANTAL){char SEKUND_värde[12];int 순번=0;do{SEKUND_värde[순번++]='0'+objekt_ANTAL%10;objekt_ANTAL/=10;}while(objekt_ANTAL);while(순번)byte_data(SEKUND_värde[--순번]);}
static void flytta_värde(int RAD_placera,int spalt_placera){글내보내기("\033[");수치(RAD_placera);byte_data(';');수치(spalt_placera);byte_data('H');}
static int Föregående(int data_placera){if(data_placera){data_placera--;while(data_placera>0&&(text[data_placera]&192)==128)data_placera--;}return data_placera;}
static int Nästa_objekt(int data_placera){if(data_placera<längd_värde){data_placera++;while(data_placera<längd_värde&&(text[data_placera]&192)==128)data_placera++;}return data_placera;}
static int Kör(int data_placera){while(data_placera>0&&text[data_placera-1]!='\n')data_placera--;return data_placera;}
static int avsluta_FÖRSKJUTNING(int data_placera){while(data_placera<längd_värde&&text[data_placera]!='\n')data_placera++;return data_placera;}
static int 너비(unsigned kodpunkt){return kodpunkt>=196?2:1;}
static int spalt(int data_placera){int kodpunkt=0;for(int 순번=Kör(data_placera);순번<data_placera;순번=Nästa_objekt(순번))kodpunkt+=text[순번]=='\t'?4-kodpunkt%4:너비(text[순번]);return kodpunkt;}
static void kontrollpunkt(void){for(int 순번=0;순번<längd_värde;순번++)ångra_data[순번]=text[순번];ångra_längd=längd_värde;위쪽=INDEX_värde;ångra_Ändringar=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrollpunkt();for(int 순번=도착위치;순번<längd_värde;순번++)text[출발위치+순번-도착위치]=text[순번];längd_värde-=도착위치-출발위치;INDEX_värde=출발위치;변경됨=1;}
static int Lägga_till_värde(const unsigned char *sträng_data,int objekt_ANTAL){if(objekt_ANTAL>Editor_kapacitet-längd_värde){알림문="File full (16384 bytes)";return 0;}kontrollpunkt();for(int 순번=längd_värde-1;순번>=INDEX_värde;순번--)text[순번+objekt_ANTAL]=text[순번];for(int 순번=0;순번<objekt_ANTAL;순번++)text[INDEX_värde+순번]=sträng_data[순번];längd_värde+=objekt_ANTAL;INDEX_värde+=objekt_ANTAL;변경됨=1;return 1;}
static void bransch(int 차이){int spalt_placera=spalt(INDEX_värde),data_placera=Kör(INDEX_värde);if(차이<0){if(!data_placera)return;data_placera=Kör(data_placera-1);}else{data_placera=avsluta_FÖRSKJUTNING(data_placera);if(data_placera==längd_värde)return;data_placera++;}int kodpunkt=0;while(data_placera<längd_värde&&text[data_placera]!='\n'&&kodpunkt<spalt_placera){kodpunkt+=text[data_placera]=='\t'?4-kodpunkt%4:너비(text[data_placera]);data_placera=Nästa_objekt(data_placera);}INDEX_värde=data_placera;}
static void Rita_skärmbild(void){
    if(INDEX_värde>längd_värde)INDEX_värde=längd_värde;if(맨위>INDEX_värde)맨위=Kör(INDEX_värde);맨위=Kör(맨위);
    int RAD_placera=0;for(int 순번=맨위;순번<INDEX_värde;순번++)if(text[순번]=='\n')RAD_placera++;
    while(RAD_placera>=RAD_ANTAL-1){맨위=avsluta_FÖRSKJUTNING(맨위);if(맨위<längd_värde)맨위++;RAD_placera--;}
    int spalt_placera=spalt(INDEX_värde);if(spalt_placera<왼쪽)왼쪽=spalt_placera;if(spalt_placera-왼쪽>=KOLUMNER-1)왼쪽=spalt_placera-KOLUMNER+2;
    글내보내기("\033[?25l");int data_placera=맨위;
    for(int 반환값=0;반환값<RAD_ANTAL-1;반환값++){
        flytta_värde(반환값+1,1);글내보내기("\033[0m\033[2K");int kodpunkt=0,그려진상태=0;
        if(data_placera>=längd_värde&&반환값>RAD_placera){글내보내기("\033[90m~\033[0m");continue;}
        while(data_placera<längd_värde&&text[data_placera]!='\n'){
            int Nästa_FÖRSKJUTNING=Nästa_objekt(data_placera),너비값=text[data_placera]=='\t'?4-kodpunkt%4:너비(text[data_placera]);
            if(kodpunkt>=왼쪽&&kodpunkt-왼쪽+너비값<KOLUMNER){
                if(text[data_placera]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_data(' ');}else if(text[data_placera]<32||text[data_placera]==127){byte_data('?');}else for(int 안쪽순번=data_placera;안쪽순번<Nästa_FÖRSKJUTNING;안쪽순번++)byte_data(text[안쪽순번]);그려진상태+=너비값;
            }kodpunkt+=너비값;data_placera=Nästa_FÖRSKJUTNING;
        }
        (void)그려진상태;if(data_placera<längd_värde)data_placera++;
    }
    flytta_värde(RAD_ANTAL,1);글내보내기("\033[7m\033[2K");status_BILD=1;status_kö=0;글내보내기(Infoga?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(fil_post_namn[이름바이트수]&&이름바이트수<30)byte_data(fil_post_namn[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int inmatningsrad=1;for(int 순번=0;순번<INDEX_värde;순번++)if(text[순번]=='\n')inmatningsrad++;수치(inmatningsrad);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int objekt_ANTAL=0;글내보내기(" | ");while(알림문[objekt_ANTAL]&&objekt_ANTAL<20)byte_data(알림문[objekt_ANTAL++]);}
    status_BILD=0;글내보내기("\033[0m");flytta_värde(RAD_placera+1,spalt_placera-왼쪽+1);글내보내기("\033[?25h");tömma();
}
static int 누름값(void){
    if(väntar_Nyckel){int 셋째순번=väntar_Nyckel;väntar_Nyckel=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Storlek=사용자호출(16,3,0,0,0,0,0);
        if(KOLUMNER!=(int)(Storlek&65535)||RAD_ANTAL!=(int)(Storlek>>16)){
            KOLUMNER=Storlek&65535;RAD_ANTAL=Storlek>>16;Rita_skärmbild();
            if(hjälp_område){flytta_värde(RAD_ANTAL,1);글내보내기("\033[0m\033[2K");byte_data(hjälp_område);글내보내기(kommando);tömma();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned aktuellt_placera=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-aktuellt_placera<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){väntar_Nyckel=셋째순번;return 27;}
    int objekt_ANTAL=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){objekt_ANTAL=objekt_ANTAL*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return objekt_ANTAL==3?1007:objekt_ANTAL==5?1008:objekt_ANTAL==6?1009:objekt_ANTAL==1?1005:objekt_ANTAL==4?1006:27;return 27;}return 27;
}
static int Store_värde(void){
    int filreferens=skapa_fil(fil_post_namn,läsa_skriva|없으면만들기|trimma_Innehåll,0600);if(filreferens<0){알림문="Cannot open for save";return 0;}
    intptr_t objekt_ANTAL=skriva_fil_data(filreferens,text,längd_värde);Stäng_fil(filreferens);if(objekt_ANTAL!=längd_värde){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SEKUND_värde){while(*첫째값&&*첫째값==*SEKUND_värde){첫째값++;SEKUND_värde++;}return *첫째값==*SEKUND_värde;}
static void Sök_Nästa(void){int objekt_ANTAL=0;while(Sök_post[objekt_ANTAL])objekt_ANTAL++;if(!objekt_ANTAL){알림문="No search pattern";return;}for(int 순번=1;순번<=längd_värde;순번++){int data_placera=(INDEX_värde+순번)%(längd_värde?längd_värde:1),안쪽순번=0;while(안쪽순번<objekt_ANTAL&&data_placera+안쪽순번<längd_värde&&text[data_placera+안쪽순번]==(unsigned char)Sök_post[안쪽순번])안쪽순번++;if(안쪽순번==objekt_ANTAL){INDEX_värde=data_placera;알림문="Match";return;}}알림문="Pattern not found";}
static int fråga(int område_värde){
    int objekt_ANTAL=0;kommando[0]=0;
    for(;;){flytta_värde(RAD_ANTAL,1);글내보내기("\033[0m\033[2K");byte_data(område_värde);글내보내기(kommando);tömma();hjälp_område=område_värde;int 셋째순번=누름값();hjälp_område=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(objekt_ANTAL){objekt_ANTAL--;while(objekt_ANTAL>0&&((unsigned char)kommando[objekt_ANTAL]&192)==128)objekt_ANTAL--;kommando[objekt_ANTAL]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&objekt_ANTAL<120){kommando[objekt_ANTAL++]=셋째순번;kommando[objekt_ANTAL]=0;}
    }
    if(område_värde=='/'){for(int 순번=0;순번<=objekt_ANTAL;순번++)Sök_post[순번]=kommando[순번];Sök_Nästa();return 0;}
    if(같은지(kommando,"q!"))return 1;
    if(같은지(kommando,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(kommando,"wq")||같은지(kommando,"x"))return Store_värde();
    if(같은지(kommando,"w")){Store_värde();return 0;}
    if(kommando[0]=='w'&&kommando[1]==' '){int 순번=2;while(kommando[순번]==' ')순번++;int Storlek=objekt_ANTAL-순번;if(Storlek<1||Storlek>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Storlek;안쪽순번++)fil_post_namn[안쪽순번]=kommando[순번+안쪽순번];fil_post_namn[Storlek]=0;Store_värde();return 0;}
    int inmatningsrad=0;for(int 순번=0;순번<objekt_ANTAL;순번++){if(kommando[순번]<'0'||kommando[순번]>'9'){inmatningsrad=0;break;}inmatningsrad=inmatningsrad*10+kommando[순번]-'0';if(inmatningsrad>16384){inmatningsrad=0;break;}}
    if(inmatningsrad){INDEX_värde=0;while(--inmatningsrad&&INDEX_värde<längd_värde){INDEX_värde=avsluta_FÖRSKJUTNING(INDEX_värde);if(INDEX_värde<längd_värde)INDEX_värde++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int START_användare_app(int 무시값){
    (void)무시값;if(användare_argument_ANTAL()!=1||användare_argument(0,fil_post_namn,sizeof(fil_post_namn))<0){글내보내기("Usage: vi FILE\n");tömma();return 2;}
    int filreferens=skapa_fil(fil_post_namn,skrivskyddad_värde,0);
    if(filreferens>=0){int objekt_ANTAL=filstorlek(filreferens);if(objekt_ANTAL<0||objekt_ANTAL>Editor_kapacitet){Stäng_fil(filreferens);return 1;}längd_värde=läsa_fil_data(filreferens,text,objekt_ANTAL);Stäng_fil(filreferens);if(längd_värde!=objekt_ANTAL)return 1;for(int 순번=0;순번<längd_värde;순번++)if(!text[순번]){글내보내기("vi: NUL byte in text file\n");tömma();return 1;}}
    else if(felnummer!=2){글내보내기("vi: cannot read file\n");tömma();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");tömma();return 1;}KOLUMNER=흐린색&65535;RAD_ANTAL=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");tömma();
    int avstånd_del=0,avsluta_app=0;
    while(!avsluta_app){Rita_skärmbild();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){bransch(-1);continue;}if(셋째순번==1002){bransch(1);continue;}if(셋째순번==1003){INDEX_värde=Nästa_objekt(INDEX_värde);continue;}if(셋째순번==1004){INDEX_värde=Föregående(INDEX_värde);continue;}
        if(셋째순번==1005){INDEX_värde=Kör(INDEX_värde);continue;}if(셋째순번==1006){INDEX_värde=avsluta_FÖRSKJUTNING(INDEX_värde);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<RAD_ANTAL-2;순번++)bransch(셋째순번==1008?-1:1);continue;}
        if(Infoga){
            if(셋째순번==27||셋째순번==3){Infoga=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_värde)바이트지우기(Föregående(INDEX_värde),INDEX_värde);continue;}
            if(셋째순번==1007){if(INDEX_värde<längd_värde)바이트지우기(INDEX_värde,Nästa_objekt(INDEX_värde));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SEKUND_värde[4];SEKUND_värde[0]=셋째순번;int objekt_ANTAL=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!objekt_ANTAL){알림문="Invalid UTF-8";continue;}int giltig=1;for(int 순번=1;순번<objekt_ANTAL;순번++){int kodpunkt=누름값();if(kodpunkt<128||kodpunkt>191){väntar_Nyckel=kodpunkt;giltig=0;break;}SEKUND_värde[순번]=kodpunkt;}
                if(giltig)Lägga_till_värde(SEKUND_värde,objekt_ANTAL);
            }continue;
        }
        if(avstånd_del){int data_placera=avstånd_del;avstånd_del=0;if(data_placera=='g'&&셋째순번=='g'){INDEX_värde=0;continue;}if(data_placera=='Z'&&셋째순번=='Z'){avsluta_app=Store_värde();continue;}if((data_placera=='d'&&셋째순번=='d')||(data_placera=='y'&&셋째순번=='y')){int 첫째값=Kör(INDEX_värde),SEKUND_värde=avsluta_FÖRSKJUTNING(INDEX_värde);if(SEKUND_värde<längd_värde)SEKUND_värde++;kopia_längd=SEKUND_värde-첫째값;for(int 순번=0;순번<kopia_längd;순번++)복사자료[순번]=text[첫째값+순번];if(data_placera=='d')바이트지우기(첫째값,SEKUND_värde);continue;}}
        if(셋째순번=='i'){Infoga=1;continue;}if(셋째순번=='a'){if(INDEX_värde<avsluta_FÖRSKJUTNING(INDEX_värde))INDEX_värde=Nästa_objekt(INDEX_värde);Infoga=1;continue;}
        if(셋째순번=='I'){INDEX_värde=Kör(INDEX_värde);Infoga=1;continue;}if(셋째순번=='A'){INDEX_värde=avsluta_FÖRSKJUTNING(INDEX_värde);Infoga=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char rad_avsluta='\n';INDEX_värde=셋째순번=='o'?avsluta_FÖRSKJUTNING(INDEX_värde):Kör(INDEX_värde);if(Lägga_till_värde(&rad_avsluta,1)){if(셋째순번=='O')INDEX_värde--;Infoga=1;}continue;}
        if(셋째순번=='h'){INDEX_värde=Föregående(INDEX_värde);continue;}if(셋째순번=='l'){INDEX_värde=Nästa_objekt(INDEX_värde);continue;}if(셋째순번=='j'){bransch(1);continue;}if(셋째순번=='k'){bransch(-1);continue;}
        if(셋째순번=='0'){INDEX_värde=Kör(INDEX_värde);continue;}if(셋째순번=='$'){INDEX_värde=avsluta_FÖRSKJUTNING(INDEX_värde);continue;}if(셋째순번=='G'){INDEX_värde=Kör(längd_värde);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){avstånd_del=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_värde<längd_värde)바이트지우기(INDEX_värde,Nästa_objekt(INDEX_värde));continue;}
        if(셋째순번=='p'&&kopia_längd){INDEX_värde=avsluta_FÖRSKJUTNING(INDEX_värde);if(INDEX_värde<längd_värde)INDEX_värde++;Lägga_till_värde(복사자료,kopia_längd);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_kapacitet;순번++){unsigned char SEKUND_värde=text[순번];text[순번]=ångra_data[순번];ångra_data[순번]=SEKUND_värde;}int objekt_ANTAL=längd_värde;längd_värde=ångra_längd;ångra_längd=objekt_ANTAL;objekt_ANTAL=INDEX_värde;INDEX_värde=위쪽;위쪽=objekt_ANTAL;objekt_ANTAL=변경됨;변경됨=ångra_Ändringar;ångra_Ändringar=objekt_ANTAL;continue;}
        if(셋째순번==':'||셋째순번=='/'){avsluta_app=fråga(셋째순번);continue;}if(셋째순번=='n'){Sök_Nästa();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");tömma();사용자호출(16,2,0,0,0,0,0);return 0;
}
