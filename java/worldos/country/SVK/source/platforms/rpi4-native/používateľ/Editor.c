/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Editor_kapacita 16384
static unsigned char Spracovanie_textu[Editor_kapacita],zrušiť_akciu_údaje[Editor_kapacita],복사자료[Editor_kapacita],KR_údaje[1024];
static int dĺžka_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,Vložiť,zrušiť_akciu_dĺžka,위쪽,zrušiť_akciu_Zmeny,되돌림있음,inštancia_dĺžka,사용량,COLUMNS=68,ROW_COUNT=19;
static char Súbor_položka_názov[64],Príkaz[128],FIND_položka[128];
static const char *upozornenie_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned čakajúci_Kľúč;
static int Pomocník_oblasť,Stav_IMAGE,Stav_front;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_údaje,사용량,0,0,0);사용량=0;}}
static void Byte_údaje(unsigned bod_kódu){if(Stav_IMAGE){if((bod_kódu&192)!=128){Stav_front+=bod_kódu>=196?2:1;}if(Stav_front>=COLUMNS)return;}if(사용량==(int)sizeof(KR_údaje))출력비우기();KR_údaje[사용량++]=bod_kódu;}
static void 글내보내기(const char *reťazec_údaje){while(*reťazec_údaje)Byte_údaje((unsigned char)*reťazec_údaje++);}
static void 수치(unsigned položka_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+položka_COUNT%10;položka_COUNT/=10;}while(položka_COUNT);while(순번)Byte_údaje(SECOND_VALUE[--순번]);}
static void premiestniť_VALUE(int ROW_pozícia,int COLUMN_pozícia){글내보내기("\033[");수치(ROW_pozícia);Byte_údaje(';');수치(COLUMN_pozícia);Byte_údaje('H');}
static int 이전항목(int údaje_pozícia){if(údaje_pozícia){údaje_pozícia--;while(údaje_pozícia>0&&(Spracovanie_textu[údaje_pozícia]&192)==128)údaje_pozícia--;}return údaje_pozícia;}
static int Ďalej_položka(int údaje_pozícia){if(údaje_pozícia<dĺžka_VALUE){údaje_pozícia++;while(údaje_pozícia<dĺžka_VALUE&&(Spracovanie_textu[údaje_pozícia]&192)==128)údaje_pozícia++;}return údaje_pozícia;}
static int Spustiť_2(int údaje_pozícia){while(údaje_pozícia>0&&Spracovanie_textu[údaje_pozícia-1]!='\n')údaje_pozícia--;return údaje_pozícia;}
static int ukončiť_hovor_Posun(int údaje_pozícia){while(údaje_pozícia<dĺžka_VALUE&&Spracovanie_textu[údaje_pozícia]!='\n')údaje_pozícia++;return údaje_pozícia;}
static int 너비(unsigned bod_kódu){return bod_kódu>=196?2:1;}
static int COLUMN(int údaje_pozícia){int bod_kódu=0;for(int 순번=Spustiť_2(údaje_pozícia);순번<údaje_pozícia;순번=Ďalej_položka(순번))bod_kódu+=Spracovanie_textu[순번]=='\t'?4-bod_kódu%4:너비(Spracovanie_textu[순번]);return bod_kódu;}
static void kontrolný_bod(void){for(int 순번=0;순번<dĺžka_VALUE;순번++)zrušiť_akciu_údaje[순번]=Spracovanie_textu[순번];zrušiť_akciu_dĺžka=dĺžka_VALUE;위쪽=INDEX_VALUE;zrušiť_akciu_Zmeny=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrolný_bod();for(int 순번=도착위치;순번<dĺžka_VALUE;순번++)Spracovanie_textu[출발위치+순번-도착위치]=Spracovanie_textu[순번];dĺžka_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int Pripojiť_VALUE(const unsigned char *reťazec_údaje,int položka_COUNT){if(položka_COUNT>Editor_kapacita-dĺžka_VALUE){upozornenie_SMS="File full (16384 bytes)";return 0;}kontrolný_bod();for(int 순번=dĺžka_VALUE-1;순번>=INDEX_VALUE;순번--)Spracovanie_textu[순번+položka_COUNT]=Spracovanie_textu[순번];for(int 순번=0;순번<položka_COUNT;순번++)Spracovanie_textu[INDEX_VALUE+순번]=reťazec_údaje[순번];dĺžka_VALUE+=položka_COUNT;INDEX_VALUE+=položka_COUNT;변경됨=1;return 1;}
static void vertikála(int 차이){int COLUMN_pozícia=COLUMN(INDEX_VALUE),údaje_pozícia=Spustiť_2(INDEX_VALUE);if(차이<0){if(!údaje_pozícia)return;údaje_pozícia=Spustiť_2(údaje_pozícia-1);}else{údaje_pozícia=ukončiť_hovor_Posun(údaje_pozícia);if(údaje_pozícia==dĺžka_VALUE)return;údaje_pozícia++;}int bod_kódu=0;while(údaje_pozícia<dĺžka_VALUE&&Spracovanie_textu[údaje_pozícia]!='\n'&&bod_kódu<COLUMN_pozícia){bod_kódu+=Spracovanie_textu[údaje_pozícia]=='\t'?4-bod_kódu%4:너비(Spracovanie_textu[údaje_pozícia]);údaje_pozícia=Ďalej_položka(údaje_pozícia);}INDEX_VALUE=údaje_pozícia;}
static void 화면그리기(void){
    if(INDEX_VALUE>dĺžka_VALUE)INDEX_VALUE=dĺžka_VALUE;if(맨위>INDEX_VALUE)맨위=Spustiť_2(INDEX_VALUE);맨위=Spustiť_2(맨위);
    int ROW_pozícia=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Spracovanie_textu[순번]=='\n')ROW_pozícia++;
    while(ROW_pozícia>=ROW_COUNT-1){맨위=ukončiť_hovor_Posun(맨위);if(맨위<dĺžka_VALUE)맨위++;ROW_pozícia--;}
    int COLUMN_pozícia=COLUMN(INDEX_VALUE);if(COLUMN_pozícia<왼쪽)왼쪽=COLUMN_pozícia;if(COLUMN_pozícia-왼쪽>=COLUMNS-1)왼쪽=COLUMN_pozícia-COLUMNS+2;
    글내보내기("\033[?25l");int údaje_pozícia=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        premiestniť_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int bod_kódu=0,그려진상태=0;
        if(údaje_pozícia>=dĺžka_VALUE&&반환값>ROW_pozícia){글내보내기("\033[90m~\033[0m");continue;}
        while(údaje_pozícia<dĺžka_VALUE&&Spracovanie_textu[údaje_pozícia]!='\n'){
            int Ďalej_Posun=Ďalej_položka(údaje_pozícia),너비값=Spracovanie_textu[údaje_pozícia]=='\t'?4-bod_kódu%4:너비(Spracovanie_textu[údaje_pozícia]);
            if(bod_kódu>=왼쪽&&bod_kódu-왼쪽+너비값<COLUMNS){
                if(Spracovanie_textu[údaje_pozícia]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)Byte_údaje(' ');}else if(Spracovanie_textu[údaje_pozícia]<32||Spracovanie_textu[údaje_pozícia]==127){Byte_údaje('?');}else for(int 안쪽순번=údaje_pozícia;안쪽순번<Ďalej_Posun;안쪽순번++)Byte_údaje(Spracovanie_textu[안쪽순번]);그려진상태+=너비값;
            }bod_kódu+=너비값;údaje_pozícia=Ďalej_Posun;
        }
        (void)그려진상태;if(údaje_pozícia<dĺžka_VALUE)údaje_pozícia++;
    }
    premiestniť_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");Stav_IMAGE=1;Stav_front=0;글내보내기(Vložiť?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Súbor_položka_názov[이름바이트수]&&이름바이트수<30)Byte_údaje(Súbor_položka_názov[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int riadok=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Spracovanie_textu[순번]=='\n')riadok++;수치(riadok);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(upozornenie_SMS){int položka_COUNT=0;글내보내기(" | ");while(upozornenie_SMS[položka_COUNT]&&položka_COUNT<20)Byte_údaje(upozornenie_SMS[položka_COUNT++]);}
    Stav_IMAGE=0;글내보내기("\033[0m");premiestniť_VALUE(ROW_pozícia+1,COLUMN_pozícia-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(čakajúci_Kľúč){int 셋째순번=čakajúci_Kľúč;čakajúci_Kľúč=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Veľkosť=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Veľkosť&65535)||ROW_COUNT!=(int)(Veľkosť>>16)){
            COLUMNS=Veľkosť&65535;ROW_COUNT=Veľkosť>>16;화면그리기();
            if(Pomocník_oblasť){premiestniť_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");Byte_údaje(Pomocník_oblasť);글내보내기(Príkaz);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned v_termíne_splatnosti_pozícia=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-v_termíne_splatnosti_pozícia<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){čakajúci_Kľúč=셋째순번;return 27;}
    int položka_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){položka_COUNT=položka_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return položka_COUNT==3?1007:položka_COUNT==5?1008:položka_COUNT==6?1009:položka_COUNT==1?1005:položka_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int Súbor_rukoväť=otvoriť_Súbor(Súbor_položka_názov,na_čítanie_a_zapisovanie|없으면만들기|skrátiť_Obsah,0600);if(Súbor_rukoväť<0){upozornenie_SMS="Cannot open for save";return 0;}
    intptr_t položka_COUNT=zapísať_Súbor_údaje(Súbor_rukoväť,Spracovanie_textu,dĺžka_VALUE);Zavrieť_Súbor(Súbor_rukoväť);if(položka_COUNT!=dĺžka_VALUE){upozornenie_SMS="Write failed";return 0;}변경됨=0;upozornenie_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Ďalej(void){int položka_COUNT=0;while(FIND_položka[položka_COUNT])položka_COUNT++;if(!položka_COUNT){upozornenie_SMS="No search pattern";return;}for(int 순번=1;순번<=dĺžka_VALUE;순번++){int údaje_pozícia=(INDEX_VALUE+순번)%(dĺžka_VALUE?dĺžka_VALUE:1),안쪽순번=0;while(안쪽순번<položka_COUNT&&údaje_pozícia+안쪽순번<dĺžka_VALUE&&Spracovanie_textu[údaje_pozícia+안쪽순번]==(unsigned char)FIND_položka[안쪽순번])안쪽순번++;if(안쪽순번==položka_COUNT){INDEX_VALUE=údaje_pozícia;upozornenie_SMS="Match";return;}}upozornenie_SMS="Pattern not found";}
static int výzva(int oblasť_VALUE){
    int položka_COUNT=0;Príkaz[0]=0;
    for(;;){premiestniť_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");Byte_údaje(oblasť_VALUE);글내보내기(Príkaz);출력비우기();Pomocník_oblasť=oblasť_VALUE;int 셋째순번=누름값();Pomocník_oblasť=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(položka_COUNT){položka_COUNT--;while(položka_COUNT>0&&((unsigned char)Príkaz[položka_COUNT]&192)==128)položka_COUNT--;Príkaz[položka_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&položka_COUNT<120){Príkaz[položka_COUNT++]=셋째순번;Príkaz[položka_COUNT]=0;}
    }
    if(oblasť_VALUE=='/'){for(int 순번=0;순번<=položka_COUNT;순번++)FIND_položka[순번]=Príkaz[순번];FIND_Ďalej();return 0;}
    if(같은지(Príkaz,"q!"))return 1;
    if(같은지(Príkaz,"q")){if(!변경됨)return 1;upozornenie_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(Príkaz,"wq")||같은지(Príkaz,"x"))return Store_VALUE();
    if(같은지(Príkaz,"w")){Store_VALUE();return 0;}
    if(Príkaz[0]=='w'&&Príkaz[1]==' '){int 순번=2;while(Príkaz[순번]==' ')순번++;int Veľkosť=položka_COUNT-순번;if(Veľkosť<1||Veľkosť>63){upozornenie_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Veľkosť;안쪽순번++)Súbor_položka_názov[안쪽순번]=Príkaz[순번+안쪽순번];Súbor_položka_názov[Veľkosť]=0;Store_VALUE();return 0;}
    int riadok=0;for(int 순번=0;순번<položka_COUNT;순번++){if(Príkaz[순번]<'0'||Príkaz[순번]>'9'){riadok=0;break;}riadok=riadok*10+Príkaz[순번]-'0';if(riadok>16384){riadok=0;break;}}
    if(riadok){INDEX_VALUE=0;while(--riadok&&INDEX_VALUE<dĺžka_VALUE){INDEX_VALUE=ukončiť_hovor_Posun(INDEX_VALUE);if(INDEX_VALUE<dĺžka_VALUE)INDEX_VALUE++;}return 0;}
    upozornenie_SMS="Unknown vi command";return 0;
}
int START_používateľ_program(int 무시값){
    (void)무시값;if(používateľ_argument_COUNT()!=1||používateľ_argument(0,Súbor_položka_názov,sizeof(Súbor_položka_názov))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Súbor_rukoväť=otvoriť_Súbor(Súbor_položka_názov,iba_na_čítanie_VALUE,0);
    if(Súbor_rukoväť>=0){int položka_COUNT=veľkosť_súboru(Súbor_rukoväť);if(položka_COUNT<0||položka_COUNT>Editor_kapacita){Zavrieť_Súbor(Súbor_rukoväť);return 1;}dĺžka_VALUE=파일자료읽기(Súbor_rukoväť,Spracovanie_textu,položka_COUNT);Zavrieť_Súbor(Súbor_rukoväť);if(dĺžka_VALUE!=položka_COUNT)return 1;for(int 순번=0;순번<dĺžka_VALUE;순번++)if(!Spracovanie_textu[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(chybové_číslo!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,ukončiť_program=0;
    while(!ukončiť_program){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();upozornenie_SMS=0;
        if(셋째순번==1001){vertikála(-1);continue;}if(셋째순번==1002){vertikála(1);continue;}if(셋째순번==1003){INDEX_VALUE=Ďalej_položka(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Spustiť_2(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=ukončiť_hovor_Posun(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)vertikála(셋째순번==1008?-1:1);continue;}
        if(Vložiť){
            if(셋째순번==27||셋째순번==3){Vložiť=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<dĺžka_VALUE)바이트지우기(INDEX_VALUE,Ďalej_položka(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int položka_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!položka_COUNT){upozornenie_SMS="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<položka_COUNT;순번++){int bod_kódu=누름값();if(bod_kódu<128||bod_kódu>191){čakajúci_Kľúč=bod_kódu;유효함=0;break;}SECOND_VALUE[순번]=bod_kódu;}
                if(유효함)Pripojiť_VALUE(SECOND_VALUE,položka_COUNT);
            }continue;
        }
        if(앞부분){int údaje_pozícia=앞부분;앞부분=0;if(údaje_pozícia=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(údaje_pozícia=='Z'&&셋째순번=='Z'){ukončiť_program=Store_VALUE();continue;}if((údaje_pozícia=='d'&&셋째순번=='d')||(údaje_pozícia=='y'&&셋째순번=='y')){int 첫째값=Spustiť_2(INDEX_VALUE),SECOND_VALUE=ukončiť_hovor_Posun(INDEX_VALUE);if(SECOND_VALUE<dĺžka_VALUE)SECOND_VALUE++;inštancia_dĺžka=SECOND_VALUE-첫째값;for(int 순번=0;순번<inštancia_dĺžka;순번++)복사자료[순번]=Spracovanie_textu[첫째값+순번];if(údaje_pozícia=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){Vložiť=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<ukončiť_hovor_Posun(INDEX_VALUE))INDEX_VALUE=Ďalej_položka(INDEX_VALUE);Vložiť=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Spustiť_2(INDEX_VALUE);Vložiť=1;continue;}if(셋째순번=='A'){INDEX_VALUE=ukončiť_hovor_Posun(INDEX_VALUE);Vložiť=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char linka_ukončiť_hovor='\n';INDEX_VALUE=셋째순번=='o'?ukončiť_hovor_Posun(INDEX_VALUE):Spustiť_2(INDEX_VALUE);if(Pripojiť_VALUE(&linka_ukončiť_hovor,1)){if(셋째순번=='O')INDEX_VALUE--;Vložiť=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Ďalej_položka(INDEX_VALUE);continue;}if(셋째순번=='j'){vertikála(1);continue;}if(셋째순번=='k'){vertikála(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Spustiť_2(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=ukončiť_hovor_Posun(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Spustiť_2(dĺžka_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<dĺžka_VALUE)바이트지우기(INDEX_VALUE,Ďalej_položka(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&inštancia_dĺžka){INDEX_VALUE=ukončiť_hovor_Posun(INDEX_VALUE);if(INDEX_VALUE<dĺžka_VALUE)INDEX_VALUE++;Pripojiť_VALUE(복사자료,inštancia_dĺžka);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_kapacita;순번++){unsigned char SECOND_VALUE=Spracovanie_textu[순번];Spracovanie_textu[순번]=zrušiť_akciu_údaje[순번];zrušiť_akciu_údaje[순번]=SECOND_VALUE;}int položka_COUNT=dĺžka_VALUE;dĺžka_VALUE=zrušiť_akciu_dĺžka;zrušiť_akciu_dĺžka=položka_COUNT;položka_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=položka_COUNT;položka_COUNT=변경됨;변경됨=zrušiť_akciu_Zmeny;zrušiť_akciu_Zmeny=položka_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){ukončiť_program=výzva(셋째순번);continue;}if(셋째순번=='n'){FIND_Ďalej();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
