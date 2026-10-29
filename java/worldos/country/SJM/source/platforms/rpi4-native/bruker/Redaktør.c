/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Redaktør_kapasitet 16384
static unsigned char Tekst[Redaktør_kapasitet],angre_data[Redaktør_kapasitet],복사자료[Redaktør_kapasitet],KR_data[1024];
static int lengde_VERDI,INDEKS_VERDI,맨위,왼쪽,변경됨,Sett_inn,angre_lengde,위쪽,angre_Endringer,되돌림있음,kopiere_lengde,사용량,KOLONNER=68,RAD_ANTALL=19;
static char Fil_oppføring_navn[64],Kommando[128],Søk_oppføring[128];
static const char *notice_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned Venter_tast;
static int hjelp_område,status_BILDE,status_kø;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_data,사용량,0,0,0);사용량=0;}}
static void byte_data(unsigned tegnkode){if(status_BILDE){if((tegnkode&192)!=128){status_kø+=tegnkode>=196?2:1;}if(status_kø>=KOLONNER)return;}if(사용량==(int)sizeof(KR_data))출력비우기();KR_data[사용량++]=tegnkode;}
static void 글내보내기(const char *streng_data){while(*streng_data)byte_data((unsigned char)*streng_data++);}
static void 수치(unsigned vare_ANTALL){char SEKUND_VERDI[12];int 순번=0;do{SEKUND_VERDI[순번++]='0'+vare_ANTALL%10;vare_ANTALL/=10;}while(vare_ANTALL);while(순번)byte_data(SEKUND_VERDI[--순번]);}
static void flytte_VERDI_83b651b8(int RAD_plassere,int spalte_plassere){글내보내기("\033[");수치(RAD_plassere);byte_data(';');수치(spalte_plassere);byte_data('H');}
static int Forrige(int data_plassere){if(data_plassere){data_plassere--;while(data_plassere>0&&(Tekst[data_plassere]&192)==128)data_plassere--;}return data_plassere;}
static int Neste_vare(int data_plassere){if(data_plassere<lengde_VERDI){data_plassere++;while(data_plassere<lengde_VERDI&&(Tekst[data_plassere]&192)==128)data_plassere++;}return data_plassere;}
static int Kjør_2(int data_plassere){while(data_plassere>0&&Tekst[data_plassere-1]!='\n')data_plassere--;return data_plassere;}
static int avslutte_en_samtale_FORSKYVNING(int data_plassere){while(data_plassere<lengde_VERDI&&Tekst[data_plassere]!='\n')data_plassere++;return data_plassere;}
static int 너비(unsigned tegnkode){return tegnkode>=196?2:1;}
static int spalte(int data_plassere){int tegnkode=0;for(int 순번=Kjør_2(data_plassere);순번<data_plassere;순번=Neste_vare(순번))tegnkode+=Tekst[순번]=='\t'?4-tegnkode%4:너비(Tekst[순번]);return tegnkode;}
static void kontrollpunkt(void){for(int 순번=0;순번<lengde_VERDI;순번++)angre_data[순번]=Tekst[순번];angre_lengde=lengde_VERDI;위쪽=INDEKS_VERDI;angre_Endringer=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrollpunkt();for(int 순번=도착위치;순번<lengde_VERDI;순번++)Tekst[출발위치+순번-도착위치]=Tekst[순번];lengde_VERDI-=도착위치-출발위치;INDEKS_VERDI=출발위치;변경됨=1;}
static int Tilføye_VERDI(const unsigned char *streng_data,int vare_ANTALL){if(vare_ANTALL>Redaktør_kapasitet-lengde_VERDI){notice_SMS="File full (16384 bytes)";return 0;}kontrollpunkt();for(int 순번=lengde_VERDI-1;순번>=INDEKS_VERDI;순번--)Tekst[순번+vare_ANTALL]=Tekst[순번];for(int 순번=0;순번<vare_ANTALL;순번++)Tekst[INDEKS_VERDI+순번]=streng_data[순번];lengde_VERDI+=vare_ANTALL;INDEKS_VERDI+=vare_ANTALL;변경됨=1;return 1;}
static void vertikal(int 차이){int spalte_plassere=spalte(INDEKS_VERDI),data_plassere=Kjør_2(INDEKS_VERDI);if(차이<0){if(!data_plassere)return;data_plassere=Kjør_2(data_plassere-1);}else{data_plassere=avslutte_en_samtale_FORSKYVNING(data_plassere);if(data_plassere==lengde_VERDI)return;data_plassere++;}int tegnkode=0;while(data_plassere<lengde_VERDI&&Tekst[data_plassere]!='\n'&&tegnkode<spalte_plassere){tegnkode+=Tekst[data_plassere]=='\t'?4-tegnkode%4:너비(Tekst[data_plassere]);data_plassere=Neste_vare(data_plassere);}INDEKS_VERDI=data_plassere;}
static void Tegn_skjermbilde(void){
    if(INDEKS_VERDI>lengde_VERDI)INDEKS_VERDI=lengde_VERDI;if(맨위>INDEKS_VERDI)맨위=Kjør_2(INDEKS_VERDI);맨위=Kjør_2(맨위);
    int RAD_plassere=0;for(int 순번=맨위;순번<INDEKS_VERDI;순번++)if(Tekst[순번]=='\n')RAD_plassere++;
    while(RAD_plassere>=RAD_ANTALL-1){맨위=avslutte_en_samtale_FORSKYVNING(맨위);if(맨위<lengde_VERDI)맨위++;RAD_plassere--;}
    int spalte_plassere=spalte(INDEKS_VERDI);if(spalte_plassere<왼쪽)왼쪽=spalte_plassere;if(spalte_plassere-왼쪽>=KOLONNER-1)왼쪽=spalte_plassere-KOLONNER+2;
    글내보내기("\033[?25l");int data_plassere=맨위;
    for(int 반환값=0;반환값<RAD_ANTALL-1;반환값++){
        flytte_VERDI_83b651b8(반환값+1,1);글내보내기("\033[0m\033[2K");int tegnkode=0,그려진상태=0;
        if(data_plassere>=lengde_VERDI&&반환값>RAD_plassere){글내보내기("\033[90m~\033[0m");continue;}
        while(data_plassere<lengde_VERDI&&Tekst[data_plassere]!='\n'){
            int Neste_FORSKYVNING=Neste_vare(data_plassere),너비값=Tekst[data_plassere]=='\t'?4-tegnkode%4:너비(Tekst[data_plassere]);
            if(tegnkode>=왼쪽&&tegnkode-왼쪽+너비값<KOLONNER){
                if(Tekst[data_plassere]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_data(' ');}else if(Tekst[data_plassere]<32||Tekst[data_plassere]==127){byte_data('?');}else for(int 안쪽순번=data_plassere;안쪽순번<Neste_FORSKYVNING;안쪽순번++)byte_data(Tekst[안쪽순번]);그려진상태+=너비값;
            }tegnkode+=너비값;data_plassere=Neste_FORSKYVNING;
        }
        (void)그려진상태;if(data_plassere<lengde_VERDI)data_plassere++;
    }
    flytte_VERDI_83b651b8(RAD_ANTALL,1);글내보내기("\033[7m\033[2K");status_BILDE=1;status_kø=0;글내보내기(Sett_inn?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Fil_oppføring_navn[이름바이트수]&&이름바이트수<30)byte_data(Fil_oppføring_navn[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Linje=1;for(int 순번=0;순번<INDEKS_VERDI;순번++)if(Tekst[순번]=='\n')Linje++;수치(Linje);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(notice_SMS){int vare_ANTALL=0;글내보내기(" | ");while(notice_SMS[vare_ANTALL]&&vare_ANTALL<20)byte_data(notice_SMS[vare_ANTALL++]);}
    status_BILDE=0;글내보내기("\033[0m");flytte_VERDI_83b651b8(RAD_plassere+1,spalte_plassere-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(Venter_tast){int 셋째순번=Venter_tast;Venter_tast=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Størrelse=사용자호출(16,3,0,0,0,0,0);
        if(KOLONNER!=(int)(Størrelse&65535)||RAD_ANTALL!=(int)(Størrelse>>16)){
            KOLONNER=Størrelse&65535;RAD_ANTALL=Størrelse>>16;Tegn_skjermbilde();
            if(hjelp_område){flytte_VERDI_83b651b8(RAD_ANTALL,1);글내보내기("\033[0m\033[2K");byte_data(hjelp_område);글내보내기(Kommando);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned betalt_plassere=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-betalt_plassere<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){Venter_tast=셋째순번;return 27;}
    int vare_ANTALL=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){vare_ANTALL=vare_ANTALL*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return vare_ANTALL==3?1007:vare_ANTALL==5?1008:vare_ANTALL==6?1009:vare_ANTALL==1?1005:vare_ANTALL==4?1006:27;return 27;}return 27;
}
static int Store_VERDI(void){
    int Fil_håndtak=åpen_Fil(Fil_oppføring_navn,lese_og_skrive|없으면만들기|avkorte_Innhold,0600);if(Fil_håndtak<0){notice_SMS="Cannot open for save";return 0;}
    intptr_t vare_ANTALL=skrive_Fil_data(Fil_håndtak,Tekst,lengde_VERDI);Lukk_Fil(Fil_håndtak);if(vare_ANTALL!=lengde_VERDI){notice_SMS="Write failed";return 0;}변경됨=0;notice_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SEKUND_VERDI){while(*첫째값&&*첫째값==*SEKUND_VERDI){첫째값++;SEKUND_VERDI++;}return *첫째값==*SEKUND_VERDI;}
static void Søk_Neste(void){int vare_ANTALL=0;while(Søk_oppføring[vare_ANTALL])vare_ANTALL++;if(!vare_ANTALL){notice_SMS="No search pattern";return;}for(int 순번=1;순번<=lengde_VERDI;순번++){int data_plassere=(INDEKS_VERDI+순번)%(lengde_VERDI?lengde_VERDI:1),안쪽순번=0;while(안쪽순번<vare_ANTALL&&data_plassere+안쪽순번<lengde_VERDI&&Tekst[data_plassere+안쪽순번]==(unsigned char)Søk_oppføring[안쪽순번])안쪽순번++;if(안쪽순번==vare_ANTALL){INDEKS_VERDI=data_plassere;notice_SMS="Match";return;}}notice_SMS="Pattern not found";}
static int be_om(int område_VERDI){
    int vare_ANTALL=0;Kommando[0]=0;
    for(;;){flytte_VERDI_83b651b8(RAD_ANTALL,1);글내보내기("\033[0m\033[2K");byte_data(område_VERDI);글내보내기(Kommando);출력비우기();hjelp_område=område_VERDI;int 셋째순번=누름값();hjelp_område=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(vare_ANTALL){vare_ANTALL--;while(vare_ANTALL>0&&((unsigned char)Kommando[vare_ANTALL]&192)==128)vare_ANTALL--;Kommando[vare_ANTALL]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&vare_ANTALL<120){Kommando[vare_ANTALL++]=셋째순번;Kommando[vare_ANTALL]=0;}
    }
    if(område_VERDI=='/'){for(int 순번=0;순번<=vare_ANTALL;순번++)Søk_oppføring[순번]=Kommando[순번];Søk_Neste();return 0;}
    if(같은지(Kommando,"q!"))return 1;
    if(같은지(Kommando,"q")){if(!변경됨)return 1;notice_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(Kommando,"wq")||같은지(Kommando,"x"))return Store_VERDI();
    if(같은지(Kommando,"w")){Store_VERDI();return 0;}
    if(Kommando[0]=='w'&&Kommando[1]==' '){int 순번=2;while(Kommando[순번]==' ')순번++;int Størrelse=vare_ANTALL-순번;if(Størrelse<1||Størrelse>63){notice_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Størrelse;안쪽순번++)Fil_oppføring_navn[안쪽순번]=Kommando[순번+안쪽순번];Fil_oppføring_navn[Størrelse]=0;Store_VERDI();return 0;}
    int Linje=0;for(int 순번=0;순번<vare_ANTALL;순번++){if(Kommando[순번]<'0'||Kommando[순번]>'9'){Linje=0;break;}Linje=Linje*10+Kommando[순번]-'0';if(Linje>16384){Linje=0;break;}}
    if(Linje){INDEKS_VERDI=0;while(--Linje&&INDEKS_VERDI<lengde_VERDI){INDEKS_VERDI=avslutte_en_samtale_FORSKYVNING(INDEKS_VERDI);if(INDEKS_VERDI<lengde_VERDI)INDEKS_VERDI++;}return 0;}
    notice_SMS="Unknown vi command";return 0;
}
int START_bruker_app(int 무시값){
    (void)무시값;if(bruker_argument_ANTALL()!=1||bruker_argument(0,Fil_oppføring_navn,sizeof(Fil_oppføring_navn))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Fil_håndtak=åpen_Fil(Fil_oppføring_navn,skrivebeskyttet_VERDI,0);
    if(Fil_håndtak>=0){int vare_ANTALL=filstørrelse(Fil_håndtak);if(vare_ANTALL<0||vare_ANTALL>Redaktør_kapasitet){Lukk_Fil(Fil_håndtak);return 1;}lengde_VERDI=파일자료읽기(Fil_håndtak,Tekst,vare_ANTALL);Lukk_Fil(Fil_håndtak);if(lengde_VERDI!=vare_ANTALL)return 1;for(int 순번=0;순번<lengde_VERDI;순번++)if(!Tekst[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(feilnummer!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}KOLONNER=흐린색&65535;RAD_ANTALL=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,avslutt_app=0;
    while(!avslutt_app){Tegn_skjermbilde();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();notice_SMS=0;
        if(셋째순번==1001){vertikal(-1);continue;}if(셋째순번==1002){vertikal(1);continue;}if(셋째순번==1003){INDEKS_VERDI=Neste_vare(INDEKS_VERDI);continue;}if(셋째순번==1004){INDEKS_VERDI=Forrige(INDEKS_VERDI);continue;}
        if(셋째순번==1005){INDEKS_VERDI=Kjør_2(INDEKS_VERDI);continue;}if(셋째순번==1006){INDEKS_VERDI=avslutte_en_samtale_FORSKYVNING(INDEKS_VERDI);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<RAD_ANTALL-2;순번++)vertikal(셋째순번==1008?-1:1);continue;}
        if(Sett_inn){
            if(셋째순번==27||셋째순번==3){Sett_inn=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEKS_VERDI)바이트지우기(Forrige(INDEKS_VERDI),INDEKS_VERDI);continue;}
            if(셋째순번==1007){if(INDEKS_VERDI<lengde_VERDI)바이트지우기(INDEKS_VERDI,Neste_vare(INDEKS_VERDI));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SEKUND_VERDI[4];SEKUND_VERDI[0]=셋째순번;int vare_ANTALL=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!vare_ANTALL){notice_SMS="Invalid UTF-8";continue;}int gyldig=1;for(int 순번=1;순번<vare_ANTALL;순번++){int tegnkode=누름값();if(tegnkode<128||tegnkode>191){Venter_tast=tegnkode;gyldig=0;break;}SEKUND_VERDI[순번]=tegnkode;}
                if(gyldig)Tilføye_VERDI(SEKUND_VERDI,vare_ANTALL);
            }continue;
        }
        if(앞부분){int data_plassere=앞부분;앞부분=0;if(data_plassere=='g'&&셋째순번=='g'){INDEKS_VERDI=0;continue;}if(data_plassere=='Z'&&셋째순번=='Z'){avslutt_app=Store_VERDI();continue;}if((data_plassere=='d'&&셋째순번=='d')||(data_plassere=='y'&&셋째순번=='y')){int 첫째값=Kjør_2(INDEKS_VERDI),SEKUND_VERDI=avslutte_en_samtale_FORSKYVNING(INDEKS_VERDI);if(SEKUND_VERDI<lengde_VERDI)SEKUND_VERDI++;kopiere_lengde=SEKUND_VERDI-첫째값;for(int 순번=0;순번<kopiere_lengde;순번++)복사자료[순번]=Tekst[첫째값+순번];if(data_plassere=='d')바이트지우기(첫째값,SEKUND_VERDI);continue;}}
        if(셋째순번=='i'){Sett_inn=1;continue;}if(셋째순번=='a'){if(INDEKS_VERDI<avslutte_en_samtale_FORSKYVNING(INDEKS_VERDI))INDEKS_VERDI=Neste_vare(INDEKS_VERDI);Sett_inn=1;continue;}
        if(셋째순번=='I'){INDEKS_VERDI=Kjør_2(INDEKS_VERDI);Sett_inn=1;continue;}if(셋째순번=='A'){INDEKS_VERDI=avslutte_en_samtale_FORSKYVNING(INDEKS_VERDI);Sett_inn=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char linje_avslutte_en_samtale='\n';INDEKS_VERDI=셋째순번=='o'?avslutte_en_samtale_FORSKYVNING(INDEKS_VERDI):Kjør_2(INDEKS_VERDI);if(Tilføye_VERDI(&linje_avslutte_en_samtale,1)){if(셋째순번=='O')INDEKS_VERDI--;Sett_inn=1;}continue;}
        if(셋째순번=='h'){INDEKS_VERDI=Forrige(INDEKS_VERDI);continue;}if(셋째순번=='l'){INDEKS_VERDI=Neste_vare(INDEKS_VERDI);continue;}if(셋째순번=='j'){vertikal(1);continue;}if(셋째순번=='k'){vertikal(-1);continue;}
        if(셋째순번=='0'){INDEKS_VERDI=Kjør_2(INDEKS_VERDI);continue;}if(셋째순번=='$'){INDEKS_VERDI=avslutte_en_samtale_FORSKYVNING(INDEKS_VERDI);continue;}if(셋째순번=='G'){INDEKS_VERDI=Kjør_2(lengde_VERDI);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEKS_VERDI<lengde_VERDI)바이트지우기(INDEKS_VERDI,Neste_vare(INDEKS_VERDI));continue;}
        if(셋째순번=='p'&&kopiere_lengde){INDEKS_VERDI=avslutte_en_samtale_FORSKYVNING(INDEKS_VERDI);if(INDEKS_VERDI<lengde_VERDI)INDEKS_VERDI++;Tilføye_VERDI(복사자료,kopiere_lengde);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Redaktør_kapasitet;순번++){unsigned char SEKUND_VERDI=Tekst[순번];Tekst[순번]=angre_data[순번];angre_data[순번]=SEKUND_VERDI;}int vare_ANTALL=lengde_VERDI;lengde_VERDI=angre_lengde;angre_lengde=vare_ANTALL;vare_ANTALL=INDEKS_VERDI;INDEKS_VERDI=위쪽;위쪽=vare_ANTALL;vare_ANTALL=변경됨;변경됨=angre_Endringer;angre_Endringer=vare_ANTALL;continue;}
        if(셋째순번==':'||셋째순번=='/'){avslutt_app=be_om(셋째순번);continue;}if(셋째순번=='n'){Søk_Neste();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
