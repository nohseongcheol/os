/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Editor_kapacitet 16384
static unsigned char Tekst[Editor_kapacitet],poništiti_podaci[Editor_kapacitet],복사자료[Editor_kapacitet],KR_podaci[1024];
static int 길이,INDEX_VALUE,맨위,왼쪽,변경됨,Umetanje,되돌림길이,위쪽,poništiti_Promjene,되돌림있음,복사길이,사용량,COLUMNS=68,ROW_COUNT=19;
static char Datoteka_unos_naziv[64],Naredba[128],FIND_unos[128];
static const char *obavijest_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned na_čekanju_Ključ;
static int pomoć_područje,Stanje_IMAGE,Stanje_red_čekanja;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_podaci,사용량,0,0,0);사용량=0;}}
static void bajt_podaci(unsigned kodna_točka){if(Stanje_IMAGE){if((kodna_točka&192)!=128){Stanje_red_čekanja+=kodna_točka>=196?2:1;}if(Stanje_red_čekanja>=COLUMNS)return;}if(사용량==(int)sizeof(KR_podaci))출력비우기();KR_podaci[사용량++]=kodna_točka;}
static void 글내보내기(const char *niz_podaci){while(*niz_podaci)bajt_podaci((unsigned char)*niz_podaci++);}
static void 수치(unsigned artikl_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+artikl_COUNT%10;artikl_COUNT/=10;}while(artikl_COUNT);while(순번)bajt_podaci(SECOND_VALUE[--순번]);}
static void pomicati_se_VALUE(int ROW_položaj,int COLUMN_položaj){글내보내기("\033[");수치(ROW_položaj);bajt_podaci(';');수치(COLUMN_položaj);bajt_podaci('H');}
static int 이전항목(int podaci_položaj){if(podaci_položaj){podaci_položaj--;while(podaci_položaj>0&&(Tekst[podaci_položaj]&192)==128)podaci_položaj--;}return podaci_položaj;}
static int Dalje_artikl(int podaci_položaj){if(podaci_položaj<길이){podaci_položaj++;while(podaci_položaj<길이&&(Tekst[podaci_položaj]&192)==128)podaci_položaj++;}return podaci_položaj;}
static int Pokreni(int podaci_položaj){while(podaci_položaj>0&&Tekst[podaci_položaj-1]!='\n')podaci_položaj--;return podaci_položaj;}
static int završiti_razgovor_pomak(int podaci_položaj){while(podaci_položaj<길이&&Tekst[podaci_položaj]!='\n')podaci_položaj++;return podaci_položaj;}
static int 너비(unsigned kodna_točka){return kodna_točka>=196?2:1;}
static int COLUMN(int podaci_položaj){int kodna_točka=0;for(int 순번=Pokreni(podaci_položaj);순번<podaci_položaj;순번=Dalje_artikl(순번))kodna_točka+=Tekst[순번]=='\t'?4-kodna_točka%4:너비(Tekst[순번]);return kodna_točka;}
static void kontrolna_točka(void){for(int 순번=0;순번<길이;순번++)poništiti_podaci[순번]=Tekst[순번];되돌림길이=길이;위쪽=INDEX_VALUE;poništiti_Promjene=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrolna_točka();for(int 순번=도착위치;순번<길이;순번++)Tekst[출발위치+순번-도착위치]=Tekst[순번];길이-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int dodati_VALUE(const unsigned char *niz_podaci,int artikl_COUNT){if(artikl_COUNT>Editor_kapacitet-길이){obavijest_SMS="File full (16384 bytes)";return 0;}kontrolna_točka();for(int 순번=길이-1;순번>=INDEX_VALUE;순번--)Tekst[순번+artikl_COUNT]=Tekst[순번];for(int 순번=0;순번<artikl_COUNT;순번++)Tekst[INDEX_VALUE+순번]=niz_podaci[순번];길이+=artikl_COUNT;INDEX_VALUE+=artikl_COUNT;변경됨=1;return 1;}
static void Okomito(int 차이){int COLUMN_položaj=COLUMN(INDEX_VALUE),podaci_položaj=Pokreni(INDEX_VALUE);if(차이<0){if(!podaci_položaj)return;podaci_položaj=Pokreni(podaci_položaj-1);}else{podaci_položaj=završiti_razgovor_pomak(podaci_položaj);if(podaci_položaj==길이)return;podaci_položaj++;}int kodna_točka=0;while(podaci_položaj<길이&&Tekst[podaci_položaj]!='\n'&&kodna_točka<COLUMN_položaj){kodna_točka+=Tekst[podaci_položaj]=='\t'?4-kodna_točka%4:너비(Tekst[podaci_položaj]);podaci_položaj=Dalje_artikl(podaci_položaj);}INDEX_VALUE=podaci_položaj;}
static void 화면그리기(void){
    if(INDEX_VALUE>길이)INDEX_VALUE=길이;if(맨위>INDEX_VALUE)맨위=Pokreni(INDEX_VALUE);맨위=Pokreni(맨위);
    int ROW_položaj=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Tekst[순번]=='\n')ROW_položaj++;
    while(ROW_položaj>=ROW_COUNT-1){맨위=završiti_razgovor_pomak(맨위);if(맨위<길이)맨위++;ROW_položaj--;}
    int COLUMN_položaj=COLUMN(INDEX_VALUE);if(COLUMN_položaj<왼쪽)왼쪽=COLUMN_položaj;if(COLUMN_položaj-왼쪽>=COLUMNS-1)왼쪽=COLUMN_položaj-COLUMNS+2;
    글내보내기("\033[?25l");int podaci_položaj=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        pomicati_se_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int kodna_točka=0,그려진상태=0;
        if(podaci_položaj>=길이&&반환값>ROW_položaj){글내보내기("\033[90m~\033[0m");continue;}
        while(podaci_položaj<길이&&Tekst[podaci_položaj]!='\n'){
            int Dalje_pomak=Dalje_artikl(podaci_položaj),너비값=Tekst[podaci_položaj]=='\t'?4-kodna_točka%4:너비(Tekst[podaci_položaj]);
            if(kodna_točka>=왼쪽&&kodna_točka-왼쪽+너비값<COLUMNS){
                if(Tekst[podaci_položaj]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bajt_podaci(' ');}else if(Tekst[podaci_položaj]<32||Tekst[podaci_položaj]==127){bajt_podaci('?');}else for(int 안쪽순번=podaci_položaj;안쪽순번<Dalje_pomak;안쪽순번++)bajt_podaci(Tekst[안쪽순번]);그려진상태+=너비값;
            }kodna_točka+=너비값;podaci_položaj=Dalje_pomak;
        }
        (void)그려진상태;if(podaci_položaj<길이)podaci_položaj++;
    }
    pomicati_se_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");Stanje_IMAGE=1;Stanje_red_čekanja=0;글내보내기(Umetanje?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Datoteka_unos_naziv[이름바이트수]&&이름바이트수<30)bajt_podaci(Datoteka_unos_naziv[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int red=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Tekst[순번]=='\n')red++;수치(red);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(obavijest_SMS){int artikl_COUNT=0;글내보내기(" | ");while(obavijest_SMS[artikl_COUNT]&&artikl_COUNT<20)bajt_podaci(obavijest_SMS[artikl_COUNT++]);}
    Stanje_IMAGE=0;글내보내기("\033[0m");pomicati_se_VALUE(ROW_položaj+1,COLUMN_položaj-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(na_čekanju_Ključ){int 셋째순번=na_čekanju_Ključ;na_čekanju_Ključ=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Veličina=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Veličina&65535)||ROW_COUNT!=(int)(Veličina>>16)){
            COLUMNS=Veličina&65535;ROW_COUNT=Veličina>>16;화면그리기();
            if(pomoć_područje){pomicati_se_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bajt_podaci(pomoć_područje);글내보내기(Naredba);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned redovno_položaj=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-redovno_položaj<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){na_čekanju_Ključ=셋째순번;return 27;}
    int artikl_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){artikl_COUNT=artikl_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return artikl_COUNT==3?1007:artikl_COUNT==5?1008:artikl_COUNT==6?1009:artikl_COUNT==1?1005:artikl_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int Datoteka_ustroj=otvoreno_Datoteka(Datoteka_unos_naziv,읽고쓰기|없으면만들기|skratiti_Sadržaj,0600);if(Datoteka_ustroj<0){obavijest_SMS="Cannot open for save";return 0;}
    intptr_t artikl_COUNT=zapisivanje_Datoteka_podaci(Datoteka_ustroj,Tekst,길이);Zatvori_Datoteka(Datoteka_ustroj);if(artikl_COUNT!=길이){obavijest_SMS="Write failed";return 0;}변경됨=0;obavijest_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Dalje(void){int artikl_COUNT=0;while(FIND_unos[artikl_COUNT])artikl_COUNT++;if(!artikl_COUNT){obavijest_SMS="No search pattern";return;}for(int 순번=1;순번<=길이;순번++){int podaci_položaj=(INDEX_VALUE+순번)%(길이?길이:1),안쪽순번=0;while(안쪽순번<artikl_COUNT&&podaci_položaj+안쪽순번<길이&&Tekst[podaci_položaj+안쪽순번]==(unsigned char)FIND_unos[안쪽순번])안쪽순번++;if(안쪽순번==artikl_COUNT){INDEX_VALUE=podaci_položaj;obavijest_SMS="Match";return;}}obavijest_SMS="Pattern not found";}
static int upit(int područje_VALUE){
    int artikl_COUNT=0;Naredba[0]=0;
    for(;;){pomicati_se_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bajt_podaci(područje_VALUE);글내보내기(Naredba);출력비우기();pomoć_područje=područje_VALUE;int 셋째순번=누름값();pomoć_područje=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(artikl_COUNT){artikl_COUNT--;while(artikl_COUNT>0&&((unsigned char)Naredba[artikl_COUNT]&192)==128)artikl_COUNT--;Naredba[artikl_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&artikl_COUNT<120){Naredba[artikl_COUNT++]=셋째순번;Naredba[artikl_COUNT]=0;}
    }
    if(područje_VALUE=='/'){for(int 순번=0;순번<=artikl_COUNT;순번++)FIND_unos[순번]=Naredba[순번];FIND_Dalje();return 0;}
    if(같은지(Naredba,"q!"))return 1;
    if(같은지(Naredba,"q")){if(!변경됨)return 1;obavijest_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(Naredba,"wq")||같은지(Naredba,"x"))return Store_VALUE();
    if(같은지(Naredba,"w")){Store_VALUE();return 0;}
    if(Naredba[0]=='w'&&Naredba[1]==' '){int 순번=2;while(Naredba[순번]==' ')순번++;int Veličina=artikl_COUNT-순번;if(Veličina<1||Veličina>63){obavijest_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Veličina;안쪽순번++)Datoteka_unos_naziv[안쪽순번]=Naredba[순번+안쪽순번];Datoteka_unos_naziv[Veličina]=0;Store_VALUE();return 0;}
    int red=0;for(int 순번=0;순번<artikl_COUNT;순번++){if(Naredba[순번]<'0'||Naredba[순번]>'9'){red=0;break;}red=red*10+Naredba[순번]-'0';if(red>16384){red=0;break;}}
    if(red){INDEX_VALUE=0;while(--red&&INDEX_VALUE<길이){INDEX_VALUE=završiti_razgovor_pomak(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;}return 0;}
    obavijest_SMS="Unknown vi command";return 0;
}
int START_korisnik_program(int 무시값){
    (void)무시값;if(korisnik_argument_COUNT()!=1||korisnik_argument(0,Datoteka_unos_naziv,sizeof(Datoteka_unos_naziv))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Datoteka_ustroj=otvoreno_Datoteka(Datoteka_unos_naziv,samo_za_čitanje_VALUE,0);
    if(Datoteka_ustroj>=0){int artikl_COUNT=veličina_datoteke(Datoteka_ustroj);if(artikl_COUNT<0||artikl_COUNT>Editor_kapacitet){Zatvori_Datoteka(Datoteka_ustroj);return 1;}길이=파일자료읽기(Datoteka_ustroj,Tekst,artikl_COUNT);Zatvori_Datoteka(Datoteka_ustroj);if(길이!=artikl_COUNT)return 1;for(int 순번=0;순번<길이;순번++)if(!Tekst[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(broj_pogreške!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,izlaz_program=0;
    while(!izlaz_program){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();obavijest_SMS=0;
        if(셋째순번==1001){Okomito(-1);continue;}if(셋째순번==1002){Okomito(1);continue;}if(셋째순번==1003){INDEX_VALUE=Dalje_artikl(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Pokreni(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=završiti_razgovor_pomak(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Okomito(셋째순번==1008?-1:1);continue;}
        if(Umetanje){
            if(셋째순번==27||셋째순번==3){Umetanje=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,Dalje_artikl(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int artikl_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!artikl_COUNT){obavijest_SMS="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<artikl_COUNT;순번++){int kodna_točka=누름값();if(kodna_točka<128||kodna_točka>191){na_čekanju_Ključ=kodna_točka;유효함=0;break;}SECOND_VALUE[순번]=kodna_točka;}
                if(유효함)dodati_VALUE(SECOND_VALUE,artikl_COUNT);
            }continue;
        }
        if(앞부분){int podaci_položaj=앞부분;앞부분=0;if(podaci_položaj=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(podaci_položaj=='Z'&&셋째순번=='Z'){izlaz_program=Store_VALUE();continue;}if((podaci_položaj=='d'&&셋째순번=='d')||(podaci_položaj=='y'&&셋째순번=='y')){int 첫째값=Pokreni(INDEX_VALUE),SECOND_VALUE=završiti_razgovor_pomak(INDEX_VALUE);if(SECOND_VALUE<길이)SECOND_VALUE++;복사길이=SECOND_VALUE-첫째값;for(int 순번=0;순번<복사길이;순번++)복사자료[순번]=Tekst[첫째값+순번];if(podaci_položaj=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){Umetanje=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<završiti_razgovor_pomak(INDEX_VALUE))INDEX_VALUE=Dalje_artikl(INDEX_VALUE);Umetanje=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Pokreni(INDEX_VALUE);Umetanje=1;continue;}if(셋째순번=='A'){INDEX_VALUE=završiti_razgovor_pomak(INDEX_VALUE);Umetanje=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char red_završiti_razgovor='\n';INDEX_VALUE=셋째순번=='o'?završiti_razgovor_pomak(INDEX_VALUE):Pokreni(INDEX_VALUE);if(dodati_VALUE(&red_završiti_razgovor,1)){if(셋째순번=='O')INDEX_VALUE--;Umetanje=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Dalje_artikl(INDEX_VALUE);continue;}if(셋째순번=='j'){Okomito(1);continue;}if(셋째순번=='k'){Okomito(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Pokreni(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=završiti_razgovor_pomak(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Pokreni(길이);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,Dalje_artikl(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&복사길이){INDEX_VALUE=završiti_razgovor_pomak(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;dodati_VALUE(복사자료,복사길이);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_kapacitet;순번++){unsigned char SECOND_VALUE=Tekst[순번];Tekst[순번]=poništiti_podaci[순번];poništiti_podaci[순번]=SECOND_VALUE;}int artikl_COUNT=길이;길이=되돌림길이;되돌림길이=artikl_COUNT;artikl_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=artikl_COUNT;artikl_COUNT=변경됨;변경됨=poništiti_Promjene;poništiti_Promjene=artikl_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){izlaz_program=upit(셋째순번);continue;}if(셋째순번=='n'){FIND_Dalje();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
