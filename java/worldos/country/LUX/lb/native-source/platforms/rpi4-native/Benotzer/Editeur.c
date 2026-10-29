/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char SMS[편집용량],réckgängeg_maachen_Daten[편집용량],복사자료[편집용량],Mooss_Daten[1024];
static int Längt_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,asetzen,réckgängeg_maachen_Längt,위쪽,réckgängeg_maachen_Ännerungen,되돌림있음,Instanz_Längt,사용량,COLUMNS=68,ROW_COUNT=19;
static char Fichier_Agab_Numm[64],Befeel[128],FIND_Agab[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned ausstoend_Tast;
static int Hëllef_Kategorie,Status_Bild,Status_Schlaang;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)Mooss_Daten,사용량,0,0,0);사용량=0;}}
static void Byte_Daten(unsigned Zeechecode){if(Status_Bild){if((Zeechecode&192)!=128){Status_Schlaang+=Zeechecode>=196?2:1;}if(Status_Schlaang>=COLUMNS)return;}if(사용량==(int)sizeof(Mooss_Daten))출력비우기();Mooss_Daten[사용량++]=Zeechecode;}
static void 글내보내기(const char *Zeechefolleg_Daten){while(*Zeechefolleg_Daten)Byte_Daten((unsigned char)*Zeechefolleg_Daten++);}
static void 수치(unsigned Element_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+Element_COUNT%10;Element_COUNT/=10;}while(Element_COUNT);while(순번)Byte_Daten(SECOND_VALUE[--순번]);}
static void verréckelen_VALUE(int ROW_positionéieren,int COLUMN_positionéieren){글내보내기("\033[");수치(ROW_positionéieren);Byte_Daten(';');수치(COLUMN_positionéieren);Byte_Daten('H');}
static int 이전항목(int Daten_positionéieren){if(Daten_positionéieren){Daten_positionéieren--;while(Daten_positionéieren>0&&(SMS[Daten_positionéieren]&192)==128)Daten_positionéieren--;}return Daten_positionéieren;}
static int Weider_Element(int Daten_positionéieren){if(Daten_positionéieren<Längt_VALUE){Daten_positionéieren++;while(Daten_positionéieren<Längt_VALUE&&(SMS[Daten_positionéieren]&192)==128)Daten_positionéieren++;}return Daten_positionéieren;}
static int Laf(int Daten_positionéieren){while(Daten_positionéieren>0&&SMS[Daten_positionéieren-1]!='\n')Daten_positionéieren--;return Daten_positionéieren;}
static int bëennegen_OFFSET(int Daten_positionéieren){while(Daten_positionéieren<Längt_VALUE&&SMS[Daten_positionéieren]!='\n')Daten_positionéieren++;return Daten_positionéieren;}
static int 너비(unsigned Zeechecode){return Zeechecode>=196?2:1;}
static int COLUMN(int Daten_positionéieren){int Zeechecode=0;for(int 순번=Laf(Daten_positionéieren);순번<Daten_positionéieren;순번=Weider_Element(순번))Zeechecode+=SMS[순번]=='\t'?4-Zeechecode%4:너비(SMS[순번]);return Zeechecode;}
static void Kontrollpunkt(void){for(int 순번=0;순번<Längt_VALUE;순번++)réckgängeg_maachen_Daten[순번]=SMS[순번];réckgängeg_maachen_Längt=Längt_VALUE;위쪽=INDEX_VALUE;réckgängeg_maachen_Ännerungen=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){Kontrollpunkt();for(int 순번=도착위치;순번<Längt_VALUE;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];Längt_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *Zeechefolleg_Daten,int Element_COUNT){if(Element_COUNT>편집용량-Längt_VALUE){알림문="File full (16384 bytes)";return 0;}Kontrollpunkt();for(int 순번=Längt_VALUE-1;순번>=INDEX_VALUE;순번--)SMS[순번+Element_COUNT]=SMS[순번];for(int 순번=0;순번<Element_COUNT;순번++)SMS[INDEX_VALUE+순번]=Zeechefolleg_Daten[순번];Längt_VALUE+=Element_COUNT;INDEX_VALUE+=Element_COUNT;변경됨=1;return 1;}
static void Vertikal(int 차이){int COLUMN_positionéieren=COLUMN(INDEX_VALUE),Daten_positionéieren=Laf(INDEX_VALUE);if(차이<0){if(!Daten_positionéieren)return;Daten_positionéieren=Laf(Daten_positionéieren-1);}else{Daten_positionéieren=bëennegen_OFFSET(Daten_positionéieren);if(Daten_positionéieren==Längt_VALUE)return;Daten_positionéieren++;}int Zeechecode=0;while(Daten_positionéieren<Längt_VALUE&&SMS[Daten_positionéieren]!='\n'&&Zeechecode<COLUMN_positionéieren){Zeechecode+=SMS[Daten_positionéieren]=='\t'?4-Zeechecode%4:너비(SMS[Daten_positionéieren]);Daten_positionéieren=Weider_Element(Daten_positionéieren);}INDEX_VALUE=Daten_positionéieren;}
static void 화면그리기(void){
    if(INDEX_VALUE>Längt_VALUE)INDEX_VALUE=Längt_VALUE;if(맨위>INDEX_VALUE)맨위=Laf(INDEX_VALUE);맨위=Laf(맨위);
    int ROW_positionéieren=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')ROW_positionéieren++;
    while(ROW_positionéieren>=ROW_COUNT-1){맨위=bëennegen_OFFSET(맨위);if(맨위<Längt_VALUE)맨위++;ROW_positionéieren--;}
    int COLUMN_positionéieren=COLUMN(INDEX_VALUE);if(COLUMN_positionéieren<왼쪽)왼쪽=COLUMN_positionéieren;if(COLUMN_positionéieren-왼쪽>=COLUMNS-1)왼쪽=COLUMN_positionéieren-COLUMNS+2;
    글내보내기("\033[?25l");int Daten_positionéieren=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        verréckelen_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int Zeechecode=0,그려진상태=0;
        if(Daten_positionéieren>=Längt_VALUE&&반환값>ROW_positionéieren){글내보내기("\033[90m~\033[0m");continue;}
        while(Daten_positionéieren<Längt_VALUE&&SMS[Daten_positionéieren]!='\n'){
            int Weider_OFFSET=Weider_Element(Daten_positionéieren),너비값=SMS[Daten_positionéieren]=='\t'?4-Zeechecode%4:너비(SMS[Daten_positionéieren]);
            if(Zeechecode>=왼쪽&&Zeechecode-왼쪽+너비값<COLUMNS){
                if(SMS[Daten_positionéieren]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)Byte_Daten(' ');}else if(SMS[Daten_positionéieren]<32||SMS[Daten_positionéieren]==127){Byte_Daten('?');}else for(int 안쪽순번=Daten_positionéieren;안쪽순번<Weider_OFFSET;안쪽순번++)Byte_Daten(SMS[안쪽순번]);그려진상태+=너비값;
            }Zeechecode+=너비값;Daten_positionéieren=Weider_OFFSET;
        }
        (void)그려진상태;if(Daten_positionéieren<Längt_VALUE)Daten_positionéieren++;
    }
    verréckelen_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");Status_Bild=1;Status_Schlaang=0;글내보내기(asetzen?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Fichier_Agab_Numm[이름바이트수]&&이름바이트수<30)Byte_Daten(Fichier_Agab_Numm[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Zeil=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')Zeil++;수치(Zeil);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int Element_COUNT=0;글내보내기(" | ");while(알림문[Element_COUNT]&&Element_COUNT<20)Byte_Daten(알림문[Element_COUNT++]);}
    Status_Bild=0;글내보내기("\033[0m");verréckelen_VALUE(ROW_positionéieren+1,COLUMN_positionéieren-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(ausstoend_Tast){int 셋째순번=ausstoend_Tast;ausstoend_Tast=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned d_Gréisst_veränneren=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(d_Gréisst_veränneren&65535)||ROW_COUNT!=(int)(d_Gréisst_veränneren>>16)){
            COLUMNS=d_Gréisst_veränneren&65535;ROW_COUNT=d_Gréisst_veränneren>>16;화면그리기();
            if(Hëllef_Kategorie){verréckelen_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");Byte_Daten(Hëllef_Kategorie);글내보내기(Befeel);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){ausstoend_Tast=셋째순번;return 27;}
    int Element_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){Element_COUNT=Element_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return Element_COUNT==3?1007:Element_COUNT==5?1008:Element_COUNT==6?1009:Element_COUNT==1?1005:Element_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int Fichier_Handle=ariichten_Fichier(Fichier_Agab_Numm,lies_schreiffäeg|없으면만들기|내용비우기,0600);if(Fichier_Handle<0){알림문="Cannot open for save";return 0;}
    intptr_t Element_COUNT=schreiwen_Fichier_Daten(Fichier_Handle,SMS,Längt_VALUE);Clôture_Fichier(Fichier_Handle);if(Element_COUNT!=Längt_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Weider(void){int Element_COUNT=0;while(FIND_Agab[Element_COUNT])Element_COUNT++;if(!Element_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=Längt_VALUE;순번++){int Daten_positionéieren=(INDEX_VALUE+순번)%(Längt_VALUE?Längt_VALUE:1),안쪽순번=0;while(안쪽순번<Element_COUNT&&Daten_positionéieren+안쪽순번<Längt_VALUE&&SMS[Daten_positionéieren+안쪽순번]==(unsigned char)FIND_Agab[안쪽순번])안쪽순번++;if(안쪽순번==Element_COUNT){INDEX_VALUE=Daten_positionéieren;알림문="Match";return;}}알림문="Pattern not found";}
static int Prompt(int Kategorie_VALUE){
    int Element_COUNT=0;Befeel[0]=0;
    for(;;){verréckelen_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");Byte_Daten(Kategorie_VALUE);글내보내기(Befeel);출력비우기();Hëllef_Kategorie=Kategorie_VALUE;int 셋째순번=누름값();Hëllef_Kategorie=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(Element_COUNT){Element_COUNT--;while(Element_COUNT>0&&((unsigned char)Befeel[Element_COUNT]&192)==128)Element_COUNT--;Befeel[Element_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&Element_COUNT<120){Befeel[Element_COUNT++]=셋째순번;Befeel[Element_COUNT]=0;}
    }
    if(Kategorie_VALUE=='/'){for(int 순번=0;순번<=Element_COUNT;순번++)FIND_Agab[순번]=Befeel[순번];FIND_Weider();return 0;}
    if(같은지(Befeel,"q!"))return 1;
    if(같은지(Befeel,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Befeel,"wq")||같은지(Befeel,"x"))return Store_VALUE();
    if(같은지(Befeel,"w")){Store_VALUE();return 0;}
    if(Befeel[0]=='w'&&Befeel[1]==' '){int 순번=2;while(Befeel[순번]==' ')순번++;int d_Gréisst_veränneren=Element_COUNT-순번;if(d_Gréisst_veränneren<1||d_Gréisst_veränneren>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<d_Gréisst_veränneren;안쪽순번++)Fichier_Agab_Numm[안쪽순번]=Befeel[순번+안쪽순번];Fichier_Agab_Numm[d_Gréisst_veränneren]=0;Store_VALUE();return 0;}
    int Zeil=0;for(int 순번=0;순번<Element_COUNT;순번++){if(Befeel[순번]<'0'||Befeel[순번]>'9'){Zeil=0;break;}Zeil=Zeil*10+Befeel[순번]-'0';if(Zeil>16384){Zeil=0;break;}}
    if(Zeil){INDEX_VALUE=0;while(--Zeil&&INDEX_VALUE<Längt_VALUE){INDEX_VALUE=bëennegen_OFFSET(INDEX_VALUE);if(INDEX_VALUE<Längt_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Start_Benotzer_App(int 무시값){
    (void)무시값;if(Benotzer_Argument_COUNT()!=1||Benotzer_Argument(0,Fichier_Agab_Numm,sizeof(Fichier_Agab_Numm))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Fichier_Handle=ariichten_Fichier(Fichier_Agab_Numm,schreifgeschützt_VALUE,0);
    if(Fichier_Handle>=0){int Element_COUNT=Fichier_d_Gréisst_veränneren(Fichier_Handle);if(Element_COUNT<0||Element_COUNT>편집용량){Clôture_Fichier(Fichier_Handle);return 1;}Längt_VALUE=파일자료읽기(Fichier_Handle,SMS,Element_COUNT);Clôture_Fichier(Fichier_Handle);if(Längt_VALUE!=Element_COUNT)return 1;for(int 순번=0;순번<Längt_VALUE;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,verloossen_App=0;
    while(!verloossen_App){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Vertikal(-1);continue;}if(셋째순번==1002){Vertikal(1);continue;}if(셋째순번==1003){INDEX_VALUE=Weider_Element(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Laf(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=bëennegen_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Vertikal(셋째순번==1008?-1:1);continue;}
        if(asetzen){
            if(셋째순번==27||셋째순번==3){asetzen=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<Längt_VALUE)바이트지우기(INDEX_VALUE,Weider_Element(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int Element_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!Element_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<Element_COUNT;순번++){int Zeechecode=누름값();if(Zeechecode<128||Zeechecode>191){ausstoend_Tast=Zeechecode;유효함=0;break;}SECOND_VALUE[순번]=Zeechecode;}
                if(유효함)덧붙이기(SECOND_VALUE,Element_COUNT);
            }continue;
        }
        if(앞부분){int Daten_positionéieren=앞부분;앞부분=0;if(Daten_positionéieren=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(Daten_positionéieren=='Z'&&셋째순번=='Z'){verloossen_App=Store_VALUE();continue;}if((Daten_positionéieren=='d'&&셋째순번=='d')||(Daten_positionéieren=='y'&&셋째순번=='y')){int 첫째값=Laf(INDEX_VALUE),SECOND_VALUE=bëennegen_OFFSET(INDEX_VALUE);if(SECOND_VALUE<Längt_VALUE)SECOND_VALUE++;Instanz_Längt=SECOND_VALUE-첫째값;for(int 순번=0;순번<Instanz_Längt;순번++)복사자료[순번]=SMS[첫째값+순번];if(Daten_positionéieren=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){asetzen=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<bëennegen_OFFSET(INDEX_VALUE))INDEX_VALUE=Weider_Element(INDEX_VALUE);asetzen=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Laf(INDEX_VALUE);asetzen=1;continue;}if(셋째순번=='A'){INDEX_VALUE=bëennegen_OFFSET(INDEX_VALUE);asetzen=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char Zeil_bëennegen='\n';INDEX_VALUE=셋째순번=='o'?bëennegen_OFFSET(INDEX_VALUE):Laf(INDEX_VALUE);if(덧붙이기(&Zeil_bëennegen,1)){if(셋째순번=='O')INDEX_VALUE--;asetzen=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Weider_Element(INDEX_VALUE);continue;}if(셋째순번=='j'){Vertikal(1);continue;}if(셋째순번=='k'){Vertikal(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Laf(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=bëennegen_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Laf(Längt_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<Längt_VALUE)바이트지우기(INDEX_VALUE,Weider_Element(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&Instanz_Längt){INDEX_VALUE=bëennegen_OFFSET(INDEX_VALUE);if(INDEX_VALUE<Längt_VALUE)INDEX_VALUE++;덧붙이기(복사자료,Instanz_Längt);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=SMS[순번];SMS[순번]=réckgängeg_maachen_Daten[순번];réckgängeg_maachen_Daten[순번]=SECOND_VALUE;}int Element_COUNT=Längt_VALUE;Längt_VALUE=réckgängeg_maachen_Längt;réckgängeg_maachen_Längt=Element_COUNT;Element_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=Element_COUNT;Element_COUNT=변경됨;변경됨=réckgängeg_maachen_Ännerungen;réckgängeg_maachen_Ännerungen=Element_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){verloossen_App=Prompt(셋째순번);continue;}if(셋째순번=='n'){FIND_Weider();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
