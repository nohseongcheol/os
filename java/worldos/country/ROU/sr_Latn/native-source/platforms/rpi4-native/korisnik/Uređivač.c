/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Uređivač_kapacitet 16384
static unsigned char SMS[Uređivač_kapacitet],opozvati_radnju_podaci[Uređivač_kapacitet],복사자료[Uređivač_kapacitet],KR_podaci[1024];
static int 길이,INDEX_VALUE,맨위,왼쪽,변경됨,Umetanje,되돌림길이,위쪽,opozvati_radnju_Promene,되돌림있음,복사길이,사용량,COLUMNS=68,ROW_COUNT=19;
static char Datoteka_stavka_ime[64],komanda[128],FIND_stavka[128];
static const char *obaveštavanje_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned na_čekanju_Ključ;
static int pomoć_na_mreži_oblast,Status_IMAGE,Status_red;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_podaci,사용량,0,0,0);사용량=0;}}
static void bajt_podaci(unsigned kôd_znaka){if(Status_IMAGE){if((kôd_znaka&192)!=128){Status_red+=kôd_znaka>=196?2:1;}if(Status_red>=COLUMNS)return;}if(사용량==(int)sizeof(KR_podaci))출력비우기();KR_podaci[사용량++]=kôd_znaka;}
static void 글내보내기(const char *niska_podaci){while(*niska_podaci)bajt_podaci((unsigned char)*niska_podaci++);}
static void 수치(unsigned stavka_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+stavka_COUNT%10;stavka_COUNT/=10;}while(stavka_COUNT);while(순번)bajt_podaci(SECOND_VALUE[--순번]);}
static void premestiti_VALUE(int ROW_pozicija,int COLUMN_pozicija){글내보내기("\033[");수치(ROW_pozicija);bajt_podaci(';');수치(COLUMN_pozicija);bajt_podaci('H');}
static int 이전항목(int podaci_pozicija){if(podaci_pozicija){podaci_pozicija--;while(podaci_pozicija>0&&(SMS[podaci_pozicija]&192)==128)podaci_pozicija--;}return podaci_pozicija;}
static int Dalje_stavka(int podaci_pozicija){if(podaci_pozicija<길이){podaci_pozicija++;while(podaci_pozicija<길이&&(SMS[podaci_pozicija]&192)==128)podaci_pozicija++;}return podaci_pozicija;}
static int koristiti(int podaci_pozicija){while(podaci_pozicija>0&&SMS[podaci_pozicija-1]!='\n')podaci_pozicija--;return podaci_pozicija;}
static int završiti_razgovor_Pomak(int podaci_pozicija){while(podaci_pozicija<길이&&SMS[podaci_pozicija]!='\n')podaci_pozicija++;return podaci_pozicija;}
static int 너비(unsigned kôd_znaka){return kôd_znaka>=196?2:1;}
static int COLUMN(int podaci_pozicija){int kôd_znaka=0;for(int 순번=koristiti(podaci_pozicija);순번<podaci_pozicija;순번=Dalje_stavka(순번))kôd_znaka+=SMS[순번]=='\t'?4-kôd_znaka%4:너비(SMS[순번]);return kôd_znaka;}
static void kontrolna_tačka(void){for(int 순번=0;순번<길이;순번++)opozvati_radnju_podaci[순번]=SMS[순번];되돌림길이=길이;위쪽=INDEX_VALUE;opozvati_radnju_Promene=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrolna_tačka();for(int 순번=도착위치;순번<길이;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];길이-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int dodati_VALUE(const unsigned char *niska_podaci,int stavka_COUNT){if(stavka_COUNT>Uređivač_kapacitet-길이){obaveštavanje_SMS="File full (16384 bytes)";return 0;}kontrolna_tačka();for(int 순번=길이-1;순번>=INDEX_VALUE;순번--)SMS[순번+stavka_COUNT]=SMS[순번];for(int 순번=0;순번<stavka_COUNT;순번++)SMS[INDEX_VALUE+순번]=niska_podaci[순번];길이+=stavka_COUNT;INDEX_VALUE+=stavka_COUNT;변경됨=1;return 1;}
static void vertikala(int 차이){int COLUMN_pozicija=COLUMN(INDEX_VALUE),podaci_pozicija=koristiti(INDEX_VALUE);if(차이<0){if(!podaci_pozicija)return;podaci_pozicija=koristiti(podaci_pozicija-1);}else{podaci_pozicija=završiti_razgovor_Pomak(podaci_pozicija);if(podaci_pozicija==길이)return;podaci_pozicija++;}int kôd_znaka=0;while(podaci_pozicija<길이&&SMS[podaci_pozicija]!='\n'&&kôd_znaka<COLUMN_pozicija){kôd_znaka+=SMS[podaci_pozicija]=='\t'?4-kôd_znaka%4:너비(SMS[podaci_pozicija]);podaci_pozicija=Dalje_stavka(podaci_pozicija);}INDEX_VALUE=podaci_pozicija;}
static void 화면그리기(void){
    if(INDEX_VALUE>길이)INDEX_VALUE=길이;if(맨위>INDEX_VALUE)맨위=koristiti(INDEX_VALUE);맨위=koristiti(맨위);
    int ROW_pozicija=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')ROW_pozicija++;
    while(ROW_pozicija>=ROW_COUNT-1){맨위=završiti_razgovor_Pomak(맨위);if(맨위<길이)맨위++;ROW_pozicija--;}
    int COLUMN_pozicija=COLUMN(INDEX_VALUE);if(COLUMN_pozicija<왼쪽)왼쪽=COLUMN_pozicija;if(COLUMN_pozicija-왼쪽>=COLUMNS-1)왼쪽=COLUMN_pozicija-COLUMNS+2;
    글내보내기("\033[?25l");int podaci_pozicija=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        premestiti_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int kôd_znaka=0,그려진상태=0;
        if(podaci_pozicija>=길이&&반환값>ROW_pozicija){글내보내기("\033[90m~\033[0m");continue;}
        while(podaci_pozicija<길이&&SMS[podaci_pozicija]!='\n'){
            int Dalje_Pomak=Dalje_stavka(podaci_pozicija),너비값=SMS[podaci_pozicija]=='\t'?4-kôd_znaka%4:너비(SMS[podaci_pozicija]);
            if(kôd_znaka>=왼쪽&&kôd_znaka-왼쪽+너비값<COLUMNS){
                if(SMS[podaci_pozicija]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bajt_podaci(' ');}else if(SMS[podaci_pozicija]<32||SMS[podaci_pozicija]==127){bajt_podaci('?');}else for(int 안쪽순번=podaci_pozicija;안쪽순번<Dalje_Pomak;안쪽순번++)bajt_podaci(SMS[안쪽순번]);그려진상태+=너비값;
            }kôd_znaka+=너비값;podaci_pozicija=Dalje_Pomak;
        }
        (void)그려진상태;if(podaci_pozicija<길이)podaci_pozicija++;
    }
    premestiti_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");Status_IMAGE=1;Status_red=0;글내보내기(Umetanje?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Datoteka_stavka_ime[이름바이트수]&&이름바이트수<30)bajt_podaci(Datoteka_stavka_ime[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int red=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')red++;수치(red);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(obaveštavanje_SMS){int stavka_COUNT=0;글내보내기(" | ");while(obaveštavanje_SMS[stavka_COUNT]&&stavka_COUNT<20)bajt_podaci(obaveštavanje_SMS[stavka_COUNT++]);}
    Status_IMAGE=0;글내보내기("\033[0m");premestiti_VALUE(ROW_pozicija+1,COLUMN_pozicija-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(na_čekanju_Ključ){int 셋째순번=na_čekanju_Ključ;na_čekanju_Ključ=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned promeniti_veličinu=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(promeniti_veličinu&65535)||ROW_COUNT!=(int)(promeniti_veličinu>>16)){
            COLUMNS=promeniti_veličinu&65535;ROW_COUNT=promeniti_veličinu>>16;화면그리기();
            if(pomoć_na_mreži_oblast){premestiti_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bajt_podaci(pomoć_na_mreži_oblast);글내보내기(komanda);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned aktuelno_pozicija=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-aktuelno_pozicija<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){na_čekanju_Ključ=셋째순번;return 27;}
    int stavka_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){stavka_COUNT=stavka_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return stavka_COUNT==3?1007:stavka_COUNT==5?1008:stavka_COUNT==6?1009:stavka_COUNT==1?1005:stavka_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int Datoteka_pokazivač=otvoren_Datoteka(Datoteka_stavka_ime,za_čitanje_pisanje|없으면만들기|내용비우기,0600);if(Datoteka_pokazivač<0){obaveštavanje_SMS="Cannot open for save";return 0;}
    intptr_t stavka_COUNT=파일자료쓰기(Datoteka_pokazivač,SMS,길이);Zatvori_Datoteka(Datoteka_pokazivač);if(stavka_COUNT!=길이){obaveštavanje_SMS="Write failed";return 0;}변경됨=0;obaveštavanje_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Dalje(void){int stavka_COUNT=0;while(FIND_stavka[stavka_COUNT])stavka_COUNT++;if(!stavka_COUNT){obaveštavanje_SMS="No search pattern";return;}for(int 순번=1;순번<=길이;순번++){int podaci_pozicija=(INDEX_VALUE+순번)%(길이?길이:1),안쪽순번=0;while(안쪽순번<stavka_COUNT&&podaci_pozicija+안쪽순번<길이&&SMS[podaci_pozicija+안쪽순번]==(unsigned char)FIND_stavka[안쪽순번])안쪽순번++;if(안쪽순번==stavka_COUNT){INDEX_VALUE=podaci_pozicija;obaveštavanje_SMS="Match";return;}}obaveštavanje_SMS="Pattern not found";}
static int odziv(int oblast_VALUE){
    int stavka_COUNT=0;komanda[0]=0;
    for(;;){premestiti_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bajt_podaci(oblast_VALUE);글내보내기(komanda);출력비우기();pomoć_na_mreži_oblast=oblast_VALUE;int 셋째순번=누름값();pomoć_na_mreži_oblast=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(stavka_COUNT){stavka_COUNT--;while(stavka_COUNT>0&&((unsigned char)komanda[stavka_COUNT]&192)==128)stavka_COUNT--;komanda[stavka_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&stavka_COUNT<120){komanda[stavka_COUNT++]=셋째순번;komanda[stavka_COUNT]=0;}
    }
    if(oblast_VALUE=='/'){for(int 순번=0;순번<=stavka_COUNT;순번++)FIND_stavka[순번]=komanda[순번];FIND_Dalje();return 0;}
    if(같은지(komanda,"q!"))return 1;
    if(같은지(komanda,"q")){if(!변경됨)return 1;obaveštavanje_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(komanda,"wq")||같은지(komanda,"x"))return Store_VALUE();
    if(같은지(komanda,"w")){Store_VALUE();return 0;}
    if(komanda[0]=='w'&&komanda[1]==' '){int 순번=2;while(komanda[순번]==' ')순번++;int promeniti_veličinu=stavka_COUNT-순번;if(promeniti_veličinu<1||promeniti_veličinu>63){obaveštavanje_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<promeniti_veličinu;안쪽순번++)Datoteka_stavka_ime[안쪽순번]=komanda[순번+안쪽순번];Datoteka_stavka_ime[promeniti_veličinu]=0;Store_VALUE();return 0;}
    int red=0;for(int 순번=0;순번<stavka_COUNT;순번++){if(komanda[순번]<'0'||komanda[순번]>'9'){red=0;break;}red=red*10+komanda[순번]-'0';if(red>16384){red=0;break;}}
    if(red){INDEX_VALUE=0;while(--red&&INDEX_VALUE<길이){INDEX_VALUE=završiti_razgovor_Pomak(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;}return 0;}
    obaveštavanje_SMS="Unknown vi command";return 0;
}
int START_korisnik_program(int 무시값){
    (void)무시값;if(korisnik_argument_COUNT()!=1||korisnik_argument(0,Datoteka_stavka_ime,sizeof(Datoteka_stavka_ime))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Datoteka_pokazivač=otvoren_Datoteka(Datoteka_stavka_ime,samo_za_čitanje_VALUE,0);
    if(Datoteka_pokazivač>=0){int stavka_COUNT=veličina_datoteke(Datoteka_pokazivač);if(stavka_COUNT<0||stavka_COUNT>Uređivač_kapacitet){Zatvori_Datoteka(Datoteka_pokazivač);return 1;}길이=파일자료읽기(Datoteka_pokazivač,SMS,stavka_COUNT);Zatvori_Datoteka(Datoteka_pokazivač);if(길이!=stavka_COUNT)return 1;for(int 순번=0;순번<길이;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(broj_greške!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,Napusti_program=0;
    while(!Napusti_program){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();obaveštavanje_SMS=0;
        if(셋째순번==1001){vertikala(-1);continue;}if(셋째순번==1002){vertikala(1);continue;}if(셋째순번==1003){INDEX_VALUE=Dalje_stavka(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=koristiti(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=završiti_razgovor_Pomak(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)vertikala(셋째순번==1008?-1:1);continue;}
        if(Umetanje){
            if(셋째순번==27||셋째순번==3){Umetanje=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,Dalje_stavka(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int stavka_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!stavka_COUNT){obaveštavanje_SMS="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<stavka_COUNT;순번++){int kôd_znaka=누름값();if(kôd_znaka<128||kôd_znaka>191){na_čekanju_Ključ=kôd_znaka;유효함=0;break;}SECOND_VALUE[순번]=kôd_znaka;}
                if(유효함)dodati_VALUE(SECOND_VALUE,stavka_COUNT);
            }continue;
        }
        if(앞부분){int podaci_pozicija=앞부분;앞부분=0;if(podaci_pozicija=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(podaci_pozicija=='Z'&&셋째순번=='Z'){Napusti_program=Store_VALUE();continue;}if((podaci_pozicija=='d'&&셋째순번=='d')||(podaci_pozicija=='y'&&셋째순번=='y')){int 첫째값=koristiti(INDEX_VALUE),SECOND_VALUE=završiti_razgovor_Pomak(INDEX_VALUE);if(SECOND_VALUE<길이)SECOND_VALUE++;복사길이=SECOND_VALUE-첫째값;for(int 순번=0;순번<복사길이;순번++)복사자료[순번]=SMS[첫째값+순번];if(podaci_pozicija=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){Umetanje=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<završiti_razgovor_Pomak(INDEX_VALUE))INDEX_VALUE=Dalje_stavka(INDEX_VALUE);Umetanje=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=koristiti(INDEX_VALUE);Umetanje=1;continue;}if(셋째순번=='A'){INDEX_VALUE=završiti_razgovor_Pomak(INDEX_VALUE);Umetanje=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char red_završiti_razgovor='\n';INDEX_VALUE=셋째순번=='o'?završiti_razgovor_Pomak(INDEX_VALUE):koristiti(INDEX_VALUE);if(dodati_VALUE(&red_završiti_razgovor,1)){if(셋째순번=='O')INDEX_VALUE--;Umetanje=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Dalje_stavka(INDEX_VALUE);continue;}if(셋째순번=='j'){vertikala(1);continue;}if(셋째순번=='k'){vertikala(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=koristiti(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=završiti_razgovor_Pomak(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=koristiti(길이);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,Dalje_stavka(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&복사길이){INDEX_VALUE=završiti_razgovor_Pomak(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;dodati_VALUE(복사자료,복사길이);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Uređivač_kapacitet;순번++){unsigned char SECOND_VALUE=SMS[순번];SMS[순번]=opozvati_radnju_podaci[순번];opozvati_radnju_podaci[순번]=SECOND_VALUE;}int stavka_COUNT=길이;길이=되돌림길이;되돌림길이=stavka_COUNT;stavka_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=stavka_COUNT;stavka_COUNT=변경됨;변경됨=opozvati_radnju_Promene;opozvati_radnju_Promene=stavka_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){Napusti_program=odziv(셋째순번);continue;}if(셋째순번=='n'){FIND_Dalje();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
