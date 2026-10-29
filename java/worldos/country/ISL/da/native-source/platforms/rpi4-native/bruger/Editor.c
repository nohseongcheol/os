/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Editor_kapacitet 16384
static unsigned char Tekst[Editor_kapacitet],fortryde_data[Editor_kapacitet],복사자료[Editor_kapacitet],KR_data[1024];
static int varighed_VÆRDI,INDEKS_VÆRDI,맨위,왼쪽,변경됨,Indsæt,fortryde_varighed,위쪽,fortryde_Ændringer,되돌림있음,kopiere_varighed,사용량,KOLONNER=68,post_TÆL=19;
static char fil_post_navn[64],Kommando[128],Søg_post[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned Afventer_tast;
static int hjælp_område,status_Image,status_kø;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_data,사용량,0,0,0);사용량=0;}}
static void byte_data(unsigned tegnkode){if(status_Image){if((tegnkode&192)!=128){status_kø+=tegnkode>=196?2:1;}if(status_kø>=KOLONNER)return;}if(사용량==(int)sizeof(KR_data))출력비우기();KR_data[사용량++]=tegnkode;}
static void 글내보내기(const char *streng_data){while(*streng_data)byte_data((unsigned char)*streng_data++);}
static void 수치(unsigned vare_TÆL){char SEKUND_VÆRDI[12];int 순번=0;do{SEKUND_VÆRDI[순번++]='0'+vare_TÆL%10;vare_TÆL/=10;}while(vare_TÆL);while(순번)byte_data(SEKUND_VÆRDI[--순번]);}
static void flytte_VÆRDI_83b651b8(int post_placere,int KOLONNE_placere){글내보내기("\033[");수치(post_placere);byte_data(';');수치(KOLONNE_placere);byte_data('H');}
static int Forrige(int data_placere){if(data_placere){data_placere--;while(data_placere>0&&(Tekst[data_placere]&192)==128)data_placere--;}return data_placere;}
static int Næste_vare(int data_placere){if(data_placere<varighed_VÆRDI){data_placere++;while(data_placere<varighed_VÆRDI&&(Tekst[data_placere]&192)==128)data_placere++;}return data_placere;}
static int Kør_2(int data_placere){while(data_placere>0&&Tekst[data_placere-1]!='\n')data_placere--;return data_placere;}
static int afslutte_et_opkald_FORSKYDNING(int data_placere){while(data_placere<varighed_VÆRDI&&Tekst[data_placere]!='\n')data_placere++;return data_placere;}
static int 너비(unsigned tegnkode){return tegnkode>=196?2:1;}
static int KOLONNE(int data_placere){int tegnkode=0;for(int 순번=Kør_2(data_placere);순번<data_placere;순번=Næste_vare(순번))tegnkode+=Tekst[순번]=='\t'?4-tegnkode%4:너비(Tekst[순번]);return tegnkode;}
static void kontrolpunkt(void){for(int 순번=0;순번<varighed_VÆRDI;순번++)fortryde_data[순번]=Tekst[순번];fortryde_varighed=varighed_VÆRDI;위쪽=INDEKS_VÆRDI;fortryde_Ændringer=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrolpunkt();for(int 순번=도착위치;순번<varighed_VÆRDI;순번++)Tekst[출발위치+순번-도착위치]=Tekst[순번];varighed_VÆRDI-=도착위치-출발위치;INDEKS_VÆRDI=출발위치;변경됨=1;}
static int tilføj_VÆRDI(const unsigned char *streng_data,int vare_TÆL){if(vare_TÆL>Editor_kapacitet-varighed_VÆRDI){알림문="File full (16384 bytes)";return 0;}kontrolpunkt();for(int 순번=varighed_VÆRDI-1;순번>=INDEKS_VÆRDI;순번--)Tekst[순번+vare_TÆL]=Tekst[순번];for(int 순번=0;순번<vare_TÆL;순번++)Tekst[INDEKS_VÆRDI+순번]=streng_data[순번];varighed_VÆRDI+=vare_TÆL;INDEKS_VÆRDI+=vare_TÆL;변경됨=1;return 1;}
static void Lodret(int 차이){int KOLONNE_placere=KOLONNE(INDEKS_VÆRDI),data_placere=Kør_2(INDEKS_VÆRDI);if(차이<0){if(!data_placere)return;data_placere=Kør_2(data_placere-1);}else{data_placere=afslutte_et_opkald_FORSKYDNING(data_placere);if(data_placere==varighed_VÆRDI)return;data_placere++;}int tegnkode=0;while(data_placere<varighed_VÆRDI&&Tekst[data_placere]!='\n'&&tegnkode<KOLONNE_placere){tegnkode+=Tekst[data_placere]=='\t'?4-tegnkode%4:너비(Tekst[data_placere]);data_placere=Næste_vare(data_placere);}INDEKS_VÆRDI=data_placere;}
static void tegne_skærmbillede(void){
    if(INDEKS_VÆRDI>varighed_VÆRDI)INDEKS_VÆRDI=varighed_VÆRDI;if(맨위>INDEKS_VÆRDI)맨위=Kør_2(INDEKS_VÆRDI);맨위=Kør_2(맨위);
    int post_placere=0;for(int 순번=맨위;순번<INDEKS_VÆRDI;순번++)if(Tekst[순번]=='\n')post_placere++;
    while(post_placere>=post_TÆL-1){맨위=afslutte_et_opkald_FORSKYDNING(맨위);if(맨위<varighed_VÆRDI)맨위++;post_placere--;}
    int KOLONNE_placere=KOLONNE(INDEKS_VÆRDI);if(KOLONNE_placere<왼쪽)왼쪽=KOLONNE_placere;if(KOLONNE_placere-왼쪽>=KOLONNER-1)왼쪽=KOLONNE_placere-KOLONNER+2;
    글내보내기("\033[?25l");int data_placere=맨위;
    for(int 반환값=0;반환값<post_TÆL-1;반환값++){
        flytte_VÆRDI_83b651b8(반환값+1,1);글내보내기("\033[0m\033[2K");int tegnkode=0,그려진상태=0;
        if(data_placere>=varighed_VÆRDI&&반환값>post_placere){글내보내기("\033[90m~\033[0m");continue;}
        while(data_placere<varighed_VÆRDI&&Tekst[data_placere]!='\n'){
            int Næste_FORSKYDNING=Næste_vare(data_placere),너비값=Tekst[data_placere]=='\t'?4-tegnkode%4:너비(Tekst[data_placere]);
            if(tegnkode>=왼쪽&&tegnkode-왼쪽+너비값<KOLONNER){
                if(Tekst[data_placere]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_data(' ');}else if(Tekst[data_placere]<32||Tekst[data_placere]==127){byte_data('?');}else for(int 안쪽순번=data_placere;안쪽순번<Næste_FORSKYDNING;안쪽순번++)byte_data(Tekst[안쪽순번]);그려진상태+=너비값;
            }tegnkode+=너비값;data_placere=Næste_FORSKYDNING;
        }
        (void)그려진상태;if(data_placere<varighed_VÆRDI)data_placere++;
    }
    flytte_VÆRDI_83b651b8(post_TÆL,1);글내보내기("\033[7m\033[2K");status_Image=1;status_kø=0;글내보내기(Indsæt?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(fil_post_navn[이름바이트수]&&이름바이트수<30)byte_data(fil_post_navn[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Linje=1;for(int 순번=0;순번<INDEKS_VÆRDI;순번++)if(Tekst[순번]=='\n')Linje++;수치(Linje);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int vare_TÆL=0;글내보내기(" | ");while(알림문[vare_TÆL]&&vare_TÆL<20)byte_data(알림문[vare_TÆL++]);}
    status_Image=0;글내보내기("\033[0m");flytte_VÆRDI_83b651b8(post_placere+1,KOLONNE_placere-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(Afventer_tast){int 셋째순번=Afventer_tast;Afventer_tast=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Størrelse=사용자호출(16,3,0,0,0,0,0);
        if(KOLONNER!=(int)(Størrelse&65535)||post_TÆL!=(int)(Størrelse>>16)){
            KOLONNER=Størrelse&65535;post_TÆL=Størrelse>>16;tegne_skærmbillede();
            if(hjælp_område){flytte_VÆRDI_83b651b8(post_TÆL,1);글내보내기("\033[0m\033[2K");byte_data(hjælp_område);글내보내기(Kommando);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned aktuel_placere=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-aktuel_placere<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){Afventer_tast=셋째순번;return 27;}
    int vare_TÆL=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){vare_TÆL=vare_TÆL*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return vare_TÆL==3?1007:vare_TÆL==5?1008:vare_TÆL==6?1009:vare_TÆL==1?1005:vare_TÆL==4?1006:27;return 27;}return 27;
}
static int Store_VÆRDI(void){
    int fil_handle=åben_fil(fil_post_navn,læse_skrive|없으면만들기|afkorte_Indhold,0600);if(fil_handle<0){알림문="Cannot open for save";return 0;}
    intptr_t vare_TÆL=skrive_fil_data(fil_handle,Tekst,varighed_VÆRDI);Luk_fil(fil_handle);if(vare_TÆL!=varighed_VÆRDI){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SEKUND_VÆRDI){while(*첫째값&&*첫째값==*SEKUND_VÆRDI){첫째값++;SEKUND_VÆRDI++;}return *첫째값==*SEKUND_VÆRDI;}
static void Søg_Næste(void){int vare_TÆL=0;while(Søg_post[vare_TÆL])vare_TÆL++;if(!vare_TÆL){알림문="No search pattern";return;}for(int 순번=1;순번<=varighed_VÆRDI;순번++){int data_placere=(INDEKS_VÆRDI+순번)%(varighed_VÆRDI?varighed_VÆRDI:1),안쪽순번=0;while(안쪽순번<vare_TÆL&&data_placere+안쪽순번<varighed_VÆRDI&&Tekst[data_placere+안쪽순번]==(unsigned char)Søg_post[안쪽순번])안쪽순번++;if(안쪽순번==vare_TÆL){INDEKS_VÆRDI=data_placere;알림문="Match";return;}}알림문="Pattern not found";}
static int prompt(int område_VÆRDI){
    int vare_TÆL=0;Kommando[0]=0;
    for(;;){flytte_VÆRDI_83b651b8(post_TÆL,1);글내보내기("\033[0m\033[2K");byte_data(område_VÆRDI);글내보내기(Kommando);출력비우기();hjælp_område=område_VÆRDI;int 셋째순번=누름값();hjælp_område=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(vare_TÆL){vare_TÆL--;while(vare_TÆL>0&&((unsigned char)Kommando[vare_TÆL]&192)==128)vare_TÆL--;Kommando[vare_TÆL]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&vare_TÆL<120){Kommando[vare_TÆL++]=셋째순번;Kommando[vare_TÆL]=0;}
    }
    if(område_VÆRDI=='/'){for(int 순번=0;순번<=vare_TÆL;순번++)Søg_post[순번]=Kommando[순번];Søg_Næste();return 0;}
    if(같은지(Kommando,"q!"))return 1;
    if(같은지(Kommando,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Kommando,"wq")||같은지(Kommando,"x"))return Store_VÆRDI();
    if(같은지(Kommando,"w")){Store_VÆRDI();return 0;}
    if(Kommando[0]=='w'&&Kommando[1]==' '){int 순번=2;while(Kommando[순번]==' ')순번++;int Størrelse=vare_TÆL-순번;if(Størrelse<1||Størrelse>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Størrelse;안쪽순번++)fil_post_navn[안쪽순번]=Kommando[순번+안쪽순번];fil_post_navn[Størrelse]=0;Store_VÆRDI();return 0;}
    int Linje=0;for(int 순번=0;순번<vare_TÆL;순번++){if(Kommando[순번]<'0'||Kommando[순번]>'9'){Linje=0;break;}Linje=Linje*10+Kommando[순번]-'0';if(Linje>16384){Linje=0;break;}}
    if(Linje){INDEKS_VÆRDI=0;while(--Linje&&INDEKS_VÆRDI<varighed_VÆRDI){INDEKS_VÆRDI=afslutte_et_opkald_FORSKYDNING(INDEKS_VÆRDI);if(INDEKS_VÆRDI<varighed_VÆRDI)INDEKS_VÆRDI++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int START_bruger_app(int 무시값){
    (void)무시값;if(bruger_argument_TÆL()!=1||bruger_argument(0,fil_post_navn,sizeof(fil_post_navn))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int fil_handle=åben_fil(fil_post_navn,skrivebeskyttet_VÆRDI,0);
    if(fil_handle>=0){int vare_TÆL=filstørrelse(fil_handle);if(vare_TÆL<0||vare_TÆL>Editor_kapacitet){Luk_fil(fil_handle);return 1;}varighed_VÆRDI=파일자료읽기(fil_handle,Tekst,vare_TÆL);Luk_fil(fil_handle);if(varighed_VÆRDI!=vare_TÆL)return 1;for(int 순번=0;순번<varighed_VÆRDI;순번++)if(!Tekst[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(fejlnummer!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}KOLONNER=흐린색&65535;post_TÆL=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,afslut_app=0;
    while(!afslut_app){tegne_skærmbillede();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Lodret(-1);continue;}if(셋째순번==1002){Lodret(1);continue;}if(셋째순번==1003){INDEKS_VÆRDI=Næste_vare(INDEKS_VÆRDI);continue;}if(셋째순번==1004){INDEKS_VÆRDI=Forrige(INDEKS_VÆRDI);continue;}
        if(셋째순번==1005){INDEKS_VÆRDI=Kør_2(INDEKS_VÆRDI);continue;}if(셋째순번==1006){INDEKS_VÆRDI=afslutte_et_opkald_FORSKYDNING(INDEKS_VÆRDI);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<post_TÆL-2;순번++)Lodret(셋째순번==1008?-1:1);continue;}
        if(Indsæt){
            if(셋째순번==27||셋째순번==3){Indsæt=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEKS_VÆRDI)바이트지우기(Forrige(INDEKS_VÆRDI),INDEKS_VÆRDI);continue;}
            if(셋째순번==1007){if(INDEKS_VÆRDI<varighed_VÆRDI)바이트지우기(INDEKS_VÆRDI,Næste_vare(INDEKS_VÆRDI));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SEKUND_VÆRDI[4];SEKUND_VÆRDI[0]=셋째순번;int vare_TÆL=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!vare_TÆL){알림문="Invalid UTF-8";continue;}int gyldig=1;for(int 순번=1;순번<vare_TÆL;순번++){int tegnkode=누름값();if(tegnkode<128||tegnkode>191){Afventer_tast=tegnkode;gyldig=0;break;}SEKUND_VÆRDI[순번]=tegnkode;}
                if(gyldig)tilføj_VÆRDI(SEKUND_VÆRDI,vare_TÆL);
            }continue;
        }
        if(앞부분){int data_placere=앞부분;앞부분=0;if(data_placere=='g'&&셋째순번=='g'){INDEKS_VÆRDI=0;continue;}if(data_placere=='Z'&&셋째순번=='Z'){afslut_app=Store_VÆRDI();continue;}if((data_placere=='d'&&셋째순번=='d')||(data_placere=='y'&&셋째순번=='y')){int 첫째값=Kør_2(INDEKS_VÆRDI),SEKUND_VÆRDI=afslutte_et_opkald_FORSKYDNING(INDEKS_VÆRDI);if(SEKUND_VÆRDI<varighed_VÆRDI)SEKUND_VÆRDI++;kopiere_varighed=SEKUND_VÆRDI-첫째값;for(int 순번=0;순번<kopiere_varighed;순번++)복사자료[순번]=Tekst[첫째값+순번];if(data_placere=='d')바이트지우기(첫째값,SEKUND_VÆRDI);continue;}}
        if(셋째순번=='i'){Indsæt=1;continue;}if(셋째순번=='a'){if(INDEKS_VÆRDI<afslutte_et_opkald_FORSKYDNING(INDEKS_VÆRDI))INDEKS_VÆRDI=Næste_vare(INDEKS_VÆRDI);Indsæt=1;continue;}
        if(셋째순번=='I'){INDEKS_VÆRDI=Kør_2(INDEKS_VÆRDI);Indsæt=1;continue;}if(셋째순번=='A'){INDEKS_VÆRDI=afslutte_et_opkald_FORSKYDNING(INDEKS_VÆRDI);Indsæt=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char linje_afslutte_et_opkald='\n';INDEKS_VÆRDI=셋째순번=='o'?afslutte_et_opkald_FORSKYDNING(INDEKS_VÆRDI):Kør_2(INDEKS_VÆRDI);if(tilføj_VÆRDI(&linje_afslutte_et_opkald,1)){if(셋째순번=='O')INDEKS_VÆRDI--;Indsæt=1;}continue;}
        if(셋째순번=='h'){INDEKS_VÆRDI=Forrige(INDEKS_VÆRDI);continue;}if(셋째순번=='l'){INDEKS_VÆRDI=Næste_vare(INDEKS_VÆRDI);continue;}if(셋째순번=='j'){Lodret(1);continue;}if(셋째순번=='k'){Lodret(-1);continue;}
        if(셋째순번=='0'){INDEKS_VÆRDI=Kør_2(INDEKS_VÆRDI);continue;}if(셋째순번=='$'){INDEKS_VÆRDI=afslutte_et_opkald_FORSKYDNING(INDEKS_VÆRDI);continue;}if(셋째순번=='G'){INDEKS_VÆRDI=Kør_2(varighed_VÆRDI);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEKS_VÆRDI<varighed_VÆRDI)바이트지우기(INDEKS_VÆRDI,Næste_vare(INDEKS_VÆRDI));continue;}
        if(셋째순번=='p'&&kopiere_varighed){INDEKS_VÆRDI=afslutte_et_opkald_FORSKYDNING(INDEKS_VÆRDI);if(INDEKS_VÆRDI<varighed_VÆRDI)INDEKS_VÆRDI++;tilføj_VÆRDI(복사자료,kopiere_varighed);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_kapacitet;순번++){unsigned char SEKUND_VÆRDI=Tekst[순번];Tekst[순번]=fortryde_data[순번];fortryde_data[순번]=SEKUND_VÆRDI;}int vare_TÆL=varighed_VÆRDI;varighed_VÆRDI=fortryde_varighed;fortryde_varighed=vare_TÆL;vare_TÆL=INDEKS_VÆRDI;INDEKS_VÆRDI=위쪽;위쪽=vare_TÆL;vare_TÆL=변경됨;변경됨=fortryde_Ændringer;fortryde_Ændringer=vare_TÆL;continue;}
        if(셋째순번==':'||셋째순번=='/'){afslut_app=prompt(셋째순번);continue;}if(셋째순번=='n'){Søg_Næste();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
