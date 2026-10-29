/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "Soubor_ABI.h"
#define Editor_kapacita 16384
static unsigned char text[Editor_kapacita],vrácení_data[Editor_kapacita],복사자료[Editor_kapacita],KV_data[1024];
static int délka_HODNOTA,INDEX_HODNOTA,맨위,왼쪽,변경됨,Vložit,vrácení_délka,위쪽,vrácení_Změny,되돌림있음,instance_délka,사용량,SLOUPCE=68,ŘÁDEK_POČET=19;
static char Soubor_položka_název[64],příkaz[128],NAJÍT_položka[128];
static const char *povinnost_zvěřejnit_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned probíhá_Klíč;
static int nápověda_oblast,Stav_image,Stav_fronta;
static void vyprázdnit(void){if(사용량){사용자호출(1,1,(uintptr_t)KV_data,사용량,0,0,0);사용량=0;}}
static void bajt_data(unsigned bod_kódu){if(Stav_image){if((bod_kódu&192)!=128){Stav_fronta+=bod_kódu>=196?2:1;}if(Stav_fronta>=SLOUPCE)return;}if(사용량==(int)sizeof(KV_data))vyprázdnit();KV_data[사용량++]=bod_kódu;}
static void 글내보내기(const char *řetězec_data){while(*řetězec_data)bajt_data((unsigned char)*řetězec_data++);}
static void 수치(unsigned zboží_POČET){char SEKUNDA_HODNOTA[12];int 순번=0;do{SEKUNDA_HODNOTA[순번++]='0'+zboží_POČET%10;zboží_POČET/=10;}while(zboží_POČET);while(순번)bajt_data(SEKUNDA_HODNOTA[--순번]);}
static void přesunout_HODNOTA(int ŘÁDEK_pozice,int SLOUPEC_pozice){글내보내기("\033[");수치(ŘÁDEK_pozice);bajt_data(';');수치(SLOUPEC_pozice);bajt_data('H');}
static int Předchozí(int data_pozice){if(data_pozice){data_pozice--;while(data_pozice>0&&(text[data_pozice]&192)==128)data_pozice--;}return data_pozice;}
static int Další_zboží(int data_pozice){if(data_pozice<délka_HODNOTA){data_pozice++;while(data_pozice<délka_HODNOTA&&(text[data_pozice]&192)==128)data_pozice++;}return data_pozice;}
static int Spustit_2(int data_pozice){while(data_pozice>0&&text[data_pozice-1]!='\n')data_pozice--;return data_pozice;}
static int konec_POSUN(int data_pozice){while(data_pozice<délka_HODNOTA&&text[data_pozice]!='\n')data_pozice++;return data_pozice;}
static int 너비(unsigned bod_kódu){return bod_kódu>=196?2:1;}
static int SLOUPEC(int data_pozice){int bod_kódu=0;for(int 순번=Spustit_2(data_pozice);순번<data_pozice;순번=Další_zboží(순번))bod_kódu+=text[순번]=='\t'?4-bod_kódu%4:너비(text[순번]);return bod_kódu;}
static void kontrolní_bod(void){for(int 순번=0;순번<délka_HODNOTA;순번++)vrácení_data[순번]=text[순번];vrácení_délka=délka_HODNOTA;위쪽=INDEX_HODNOTA;vrácení_Změny=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrolní_bod();for(int 순번=도착위치;순번<délka_HODNOTA;순번++)text[출발위치+순번-도착위치]=text[순번];délka_HODNOTA-=도착위치-출발위치;INDEX_HODNOTA=출발위치;변경됨=1;}
static int Připojit_HODNOTA(const unsigned char *řetězec_data,int zboží_POČET){if(zboží_POČET>Editor_kapacita-délka_HODNOTA){povinnost_zvěřejnit_SMS="File full (16384 bytes)";return 0;}kontrolní_bod();for(int 순번=délka_HODNOTA-1;순번>=INDEX_HODNOTA;순번--)text[순번+zboží_POČET]=text[순번];for(int 순번=0;순번<zboží_POČET;순번++)text[INDEX_HODNOTA+순번]=řetězec_data[순번];délka_HODNOTA+=zboží_POČET;INDEX_HODNOTA+=zboží_POČET;변경됨=1;return 1;}
static void Svislá(int 차이){int SLOUPEC_pozice=SLOUPEC(INDEX_HODNOTA),data_pozice=Spustit_2(INDEX_HODNOTA);if(차이<0){if(!data_pozice)return;data_pozice=Spustit_2(data_pozice-1);}else{data_pozice=konec_POSUN(data_pozice);if(data_pozice==délka_HODNOTA)return;data_pozice++;}int bod_kódu=0;while(data_pozice<délka_HODNOTA&&text[data_pozice]!='\n'&&bod_kódu<SLOUPEC_pozice){bod_kódu+=text[data_pozice]=='\t'?4-bod_kódu%4:너비(text[data_pozice]);data_pozice=Další_zboží(data_pozice);}INDEX_HODNOTA=data_pozice;}
static void 화면그리기(void){
    if(INDEX_HODNOTA>délka_HODNOTA)INDEX_HODNOTA=délka_HODNOTA;if(맨위>INDEX_HODNOTA)맨위=Spustit_2(INDEX_HODNOTA);맨위=Spustit_2(맨위);
    int ŘÁDEK_pozice=0;for(int 순번=맨위;순번<INDEX_HODNOTA;순번++)if(text[순번]=='\n')ŘÁDEK_pozice++;
    while(ŘÁDEK_pozice>=ŘÁDEK_POČET-1){맨위=konec_POSUN(맨위);if(맨위<délka_HODNOTA)맨위++;ŘÁDEK_pozice--;}
    int SLOUPEC_pozice=SLOUPEC(INDEX_HODNOTA);if(SLOUPEC_pozice<왼쪽)왼쪽=SLOUPEC_pozice;if(SLOUPEC_pozice-왼쪽>=SLOUPCE-1)왼쪽=SLOUPEC_pozice-SLOUPCE+2;
    글내보내기("\033[?25l");int data_pozice=맨위;
    for(int 반환값=0;반환값<ŘÁDEK_POČET-1;반환값++){
        přesunout_HODNOTA(반환값+1,1);글내보내기("\033[0m\033[2K");int bod_kódu=0,그려진상태=0;
        if(data_pozice>=délka_HODNOTA&&반환값>ŘÁDEK_pozice){글내보내기("\033[90m~\033[0m");continue;}
        while(data_pozice<délka_HODNOTA&&text[data_pozice]!='\n'){
            int Další_POSUN=Další_zboží(data_pozice),너비값=text[data_pozice]=='\t'?4-bod_kódu%4:너비(text[data_pozice]);
            if(bod_kódu>=왼쪽&&bod_kódu-왼쪽+너비값<SLOUPCE){
                if(text[data_pozice]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bajt_data(' ');}else if(text[data_pozice]<32||text[data_pozice]==127){bajt_data('?');}else for(int 안쪽순번=data_pozice;안쪽순번<Další_POSUN;안쪽순번++)bajt_data(text[안쪽순번]);그려진상태+=너비값;
            }bod_kódu+=너비값;data_pozice=Další_POSUN;
        }
        (void)그려진상태;if(data_pozice<délka_HODNOTA)data_pozice++;
    }
    přesunout_HODNOTA(ŘÁDEK_POČET,1);글내보내기("\033[7m\033[2K");Stav_image=1;Stav_fronta=0;글내보내기(Vložit?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Soubor_položka_název[이름바이트수]&&이름바이트수<30)bajt_data(Soubor_položka_název[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int vstupní_řádek=1;for(int 순번=0;순번<INDEX_HODNOTA;순번++)if(text[순번]=='\n')vstupní_řádek++;수치(vstupní_řádek);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(povinnost_zvěřejnit_SMS){int zboží_POČET=0;글내보내기(" | ");while(povinnost_zvěřejnit_SMS[zboží_POČET]&&zboží_POČET<20)bajt_data(povinnost_zvěřejnit_SMS[zboží_POČET++]);}
    Stav_image=0;글내보내기("\033[0m");přesunout_HODNOTA(ŘÁDEK_pozice+1,SLOUPEC_pozice-왼쪽+1);글내보내기("\033[?25h");vyprázdnit();
}
static int 누름값(void){
    if(probíhá_Klíč){int 셋째순번=probíhá_Klíč;probíhá_Klíč=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Velikost=사용자호출(16,3,0,0,0,0,0);
        if(SLOUPCE!=(int)(Velikost&65535)||ŘÁDEK_POČET!=(int)(Velikost>>16)){
            SLOUPCE=Velikost&65535;ŘÁDEK_POČET=Velikost>>16;화면그리기();
            if(nápověda_oblast){přesunout_HODNOTA(ŘÁDEK_POČET,1);글내보내기("\033[0m\033[2K");bajt_data(nápověda_oblast);글내보내기(příkaz);vyprázdnit();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned dobrá_pozice=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-dobrá_pozice<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){probíhá_Klíč=셋째순번;return 27;}
    int zboží_POČET=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){zboží_POČET=zboží_POČET*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return zboží_POČET==3?1007:zboží_POČET==5?1008:zboží_POČET==6?1009:zboží_POČET==1?1005:zboží_POČET==4?1006:27;return 27;}return 27;
}
static int Store_HODNOTA(void){
    int popisovač_souboru=otevřít_Soubor(Soubor_položka_název,pro_čtení_i_zápis|없으면만들기|stříhat_Obsah,0600);if(popisovač_souboru<0){povinnost_zvěřejnit_SMS="Cannot open for save";return 0;}
    intptr_t zboží_POČET=zápis_Soubor_data(popisovač_souboru,text,délka_HODNOTA);Zavřít_Soubor(popisovač_souboru);if(zboží_POČET!=délka_HODNOTA){povinnost_zvěřejnit_SMS="Write failed";return 0;}변경됨=0;povinnost_zvěřejnit_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SEKUNDA_HODNOTA){while(*첫째값&&*첫째값==*SEKUNDA_HODNOTA){첫째값++;SEKUNDA_HODNOTA++;}return *첫째값==*SEKUNDA_HODNOTA;}
static void NAJÍT_Další(void){int zboží_POČET=0;while(NAJÍT_položka[zboží_POČET])zboží_POČET++;if(!zboží_POČET){povinnost_zvěřejnit_SMS="No search pattern";return;}for(int 순번=1;순번<=délka_HODNOTA;순번++){int data_pozice=(INDEX_HODNOTA+순번)%(délka_HODNOTA?délka_HODNOTA:1),안쪽순번=0;while(안쪽순번<zboží_POČET&&data_pozice+안쪽순번<délka_HODNOTA&&text[data_pozice+안쪽순번]==(unsigned char)NAJÍT_položka[안쪽순번])안쪽순번++;if(안쪽순번==zboží_POČET){INDEX_HODNOTA=data_pozice;povinnost_zvěřejnit_SMS="Match";return;}}povinnost_zvěřejnit_SMS="Pattern not found";}
static int výzva(int oblast_HODNOTA){
    int zboží_POČET=0;příkaz[0]=0;
    for(;;){přesunout_HODNOTA(ŘÁDEK_POČET,1);글내보내기("\033[0m\033[2K");bajt_data(oblast_HODNOTA);글내보내기(příkaz);vyprázdnit();nápověda_oblast=oblast_HODNOTA;int 셋째순번=누름값();nápověda_oblast=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(zboží_POČET){zboží_POČET--;while(zboží_POČET>0&&((unsigned char)příkaz[zboží_POČET]&192)==128)zboží_POČET--;příkaz[zboží_POČET]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&zboží_POČET<120){příkaz[zboží_POČET++]=셋째순번;příkaz[zboží_POČET]=0;}
    }
    if(oblast_HODNOTA=='/'){for(int 순번=0;순번<=zboží_POČET;순번++)NAJÍT_položka[순번]=příkaz[순번];NAJÍT_Další();return 0;}
    if(같은지(příkaz,"q!"))return 1;
    if(같은지(příkaz,"q")){if(!변경됨)return 1;povinnost_zvěřejnit_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(příkaz,"wq")||같은지(příkaz,"x"))return Store_HODNOTA();
    if(같은지(příkaz,"w")){Store_HODNOTA();return 0;}
    if(příkaz[0]=='w'&&příkaz[1]==' '){int 순번=2;while(příkaz[순번]==' ')순번++;int Velikost=zboží_POČET-순번;if(Velikost<1||Velikost>63){povinnost_zvěřejnit_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Velikost;안쪽순번++)Soubor_položka_název[안쪽순번]=příkaz[순번+안쪽순번];Soubor_položka_název[Velikost]=0;Store_HODNOTA();return 0;}
    int vstupní_řádek=0;for(int 순번=0;순번<zboží_POČET;순번++){if(příkaz[순번]<'0'||příkaz[순번]>'9'){vstupní_řádek=0;break;}vstupní_řádek=vstupní_řádek*10+příkaz[순번]-'0';if(vstupní_řádek>16384){vstupní_řádek=0;break;}}
    if(vstupní_řádek){INDEX_HODNOTA=0;while(--vstupní_řádek&&INDEX_HODNOTA<délka_HODNOTA){INDEX_HODNOTA=konec_POSUN(INDEX_HODNOTA);if(INDEX_HODNOTA<délka_HODNOTA)INDEX_HODNOTA++;}return 0;}
    povinnost_zvěřejnit_SMS="Unknown vi command";return 0;
}
int START_uživatel_program(int 무시값){
    (void)무시값;if(uživatel_argument_POČET()!=1||uživatel_argument(0,Soubor_položka_název,sizeof(Soubor_položka_název))<0){글내보내기("Usage: vi FILE\n");vyprázdnit();return 2;}
    int popisovač_souboru=otevřít_Soubor(Soubor_položka_název,jen_pro_čtení_HODNOTA,0);
    if(popisovač_souboru>=0){int zboží_POČET=velikost_souboru(popisovač_souboru);if(zboží_POČET<0||zboží_POČET>Editor_kapacita){Zavřít_Soubor(popisovač_souboru);return 1;}délka_HODNOTA=파일자료읽기(popisovač_souboru,text,zboží_POČET);Zavřít_Soubor(popisovač_souboru);if(délka_HODNOTA!=zboží_POČET)return 1;for(int 순번=0;순번<délka_HODNOTA;순번++)if(!text[순번]){글내보내기("vi: NUL byte in text file\n");vyprázdnit();return 1;}}
    else if(číslo_chyby!=2){글내보내기("vi: cannot read file\n");vyprázdnit();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");vyprázdnit();return 1;}SLOUPCE=흐린색&65535;ŘÁDEK_POČET=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");vyprázdnit();
    int řádkování_část=0,ukončit_program=0;
    while(!ukončit_program){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();povinnost_zvěřejnit_SMS=0;
        if(셋째순번==1001){Svislá(-1);continue;}if(셋째순번==1002){Svislá(1);continue;}if(셋째순번==1003){INDEX_HODNOTA=Další_zboží(INDEX_HODNOTA);continue;}if(셋째순번==1004){INDEX_HODNOTA=Předchozí(INDEX_HODNOTA);continue;}
        if(셋째순번==1005){INDEX_HODNOTA=Spustit_2(INDEX_HODNOTA);continue;}if(셋째순번==1006){INDEX_HODNOTA=konec_POSUN(INDEX_HODNOTA);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ŘÁDEK_POČET-2;순번++)Svislá(셋째순번==1008?-1:1);continue;}
        if(Vložit){
            if(셋째순번==27||셋째순번==3){Vložit=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_HODNOTA)바이트지우기(Předchozí(INDEX_HODNOTA),INDEX_HODNOTA);continue;}
            if(셋째순번==1007){if(INDEX_HODNOTA<délka_HODNOTA)바이트지우기(INDEX_HODNOTA,Další_zboží(INDEX_HODNOTA));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SEKUNDA_HODNOTA[4];SEKUNDA_HODNOTA[0]=셋째순번;int zboží_POČET=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!zboží_POČET){povinnost_zvěřejnit_SMS="Invalid UTF-8";continue;}int platný=1;for(int 순번=1;순번<zboží_POČET;순번++){int bod_kódu=누름값();if(bod_kódu<128||bod_kódu>191){probíhá_Klíč=bod_kódu;platný=0;break;}SEKUNDA_HODNOTA[순번]=bod_kódu;}
                if(platný)Připojit_HODNOTA(SEKUNDA_HODNOTA,zboží_POČET);
            }continue;
        }
        if(řádkování_část){int data_pozice=řádkování_část;řádkování_část=0;if(data_pozice=='g'&&셋째순번=='g'){INDEX_HODNOTA=0;continue;}if(data_pozice=='Z'&&셋째순번=='Z'){ukončit_program=Store_HODNOTA();continue;}if((data_pozice=='d'&&셋째순번=='d')||(data_pozice=='y'&&셋째순번=='y')){int 첫째값=Spustit_2(INDEX_HODNOTA),SEKUNDA_HODNOTA=konec_POSUN(INDEX_HODNOTA);if(SEKUNDA_HODNOTA<délka_HODNOTA)SEKUNDA_HODNOTA++;instance_délka=SEKUNDA_HODNOTA-첫째값;for(int 순번=0;순번<instance_délka;순번++)복사자료[순번]=text[첫째값+순번];if(data_pozice=='d')바이트지우기(첫째값,SEKUNDA_HODNOTA);continue;}}
        if(셋째순번=='i'){Vložit=1;continue;}if(셋째순번=='a'){if(INDEX_HODNOTA<konec_POSUN(INDEX_HODNOTA))INDEX_HODNOTA=Další_zboží(INDEX_HODNOTA);Vložit=1;continue;}
        if(셋째순번=='I'){INDEX_HODNOTA=Spustit_2(INDEX_HODNOTA);Vložit=1;continue;}if(셋째순번=='A'){INDEX_HODNOTA=konec_POSUN(INDEX_HODNOTA);Vložit=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char čára_konec='\n';INDEX_HODNOTA=셋째순번=='o'?konec_POSUN(INDEX_HODNOTA):Spustit_2(INDEX_HODNOTA);if(Připojit_HODNOTA(&čára_konec,1)){if(셋째순번=='O')INDEX_HODNOTA--;Vložit=1;}continue;}
        if(셋째순번=='h'){INDEX_HODNOTA=Předchozí(INDEX_HODNOTA);continue;}if(셋째순번=='l'){INDEX_HODNOTA=Další_zboží(INDEX_HODNOTA);continue;}if(셋째순번=='j'){Svislá(1);continue;}if(셋째순번=='k'){Svislá(-1);continue;}
        if(셋째순번=='0'){INDEX_HODNOTA=Spustit_2(INDEX_HODNOTA);continue;}if(셋째순번=='$'){INDEX_HODNOTA=konec_POSUN(INDEX_HODNOTA);continue;}if(셋째순번=='G'){INDEX_HODNOTA=Spustit_2(délka_HODNOTA);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){řádkování_část=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_HODNOTA<délka_HODNOTA)바이트지우기(INDEX_HODNOTA,Další_zboží(INDEX_HODNOTA));continue;}
        if(셋째순번=='p'&&instance_délka){INDEX_HODNOTA=konec_POSUN(INDEX_HODNOTA);if(INDEX_HODNOTA<délka_HODNOTA)INDEX_HODNOTA++;Připojit_HODNOTA(복사자료,instance_délka);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_kapacita;순번++){unsigned char SEKUNDA_HODNOTA=text[순번];text[순번]=vrácení_data[순번];vrácení_data[순번]=SEKUNDA_HODNOTA;}int zboží_POČET=délka_HODNOTA;délka_HODNOTA=vrácení_délka;vrácení_délka=zboží_POČET;zboží_POČET=INDEX_HODNOTA;INDEX_HODNOTA=위쪽;위쪽=zboží_POČET;zboží_POČET=변경됨;변경됨=vrácení_Změny;vrácení_Změny=zboží_POČET;continue;}
        if(셋째순번==':'||셋째순번=='/'){ukončit_program=výzva(셋째순번);continue;}if(셋째순번=='n'){NAJÍT_Další();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");vyprázdnit();사용자호출(16,2,0,0,0,0,0);return 0;
}
