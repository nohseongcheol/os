/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define ritill_afkastageta 16384
static unsigned char Texti[ritill_afkastageta],afturkalla_gögn[ritill_afkastageta],복사자료[ritill_afkastageta],mæld_stærð_gögn[1024];
static int lengd_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,setja_inn,afturkalla_lengd,위쪽,afturkalla_Breytingar,되돌림있음,afrita_lengd,사용량,COLUMNS=68,ROW_COUNT=19;
static char skrá_færsla_heiti[64],Skipun[128],FIND_færsla[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned Í_bið_Lykill;
static int hjálp_tegund,staða_mynd,staða_biðröð;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)mæld_stærð_gögn,사용량,0,0,0);사용량=0;}}
static void bæti_gögn(unsigned stafkóði){if(staða_mynd){if((stafkóði&192)!=128){staða_biðröð+=stafkóði>=196?2:1;}if(staða_biðröð>=COLUMNS)return;}if(사용량==(int)sizeof(mæld_stærð_gögn))출력비우기();mæld_stærð_gögn[사용량++]=stafkóði;}
static void 글내보내기(const char *strengur_gögn){while(*strengur_gögn)bæti_gögn((unsigned char)*strengur_gögn++);}
static void 수치(unsigned vara_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+vara_COUNT%10;vara_COUNT/=10;}while(vara_COUNT);while(순번)bæti_gögn(SECOND_VALUE[--순번]);}
static void færa_VALUE(int ROW_staða,int COLUMN_staða){글내보내기("\033[");수치(ROW_staða);bæti_gögn(';');수치(COLUMN_staða);bæti_gögn('H');}
static int 이전항목(int gögn_staða){if(gögn_staða){gögn_staða--;while(gögn_staða>0&&(Texti[gögn_staða]&192)==128)gögn_staða--;}return gögn_staða;}
static int Áfram_vara(int gögn_staða){if(gögn_staða<lengd_VALUE){gögn_staða++;while(gögn_staða<lengd_VALUE&&(Texti[gögn_staða]&192)==128)gögn_staða++;}return gögn_staða;}
static int Keyra_2(int gögn_staða){while(gögn_staða>0&&Texti[gögn_staða-1]!='\n')gögn_staða--;return gögn_staða;}
static int ljúka_OFFSET(int gögn_staða){while(gögn_staða<lengd_VALUE&&Texti[gögn_staða]!='\n')gögn_staða++;return gögn_staða;}
static int 너비(unsigned stafkóði){return stafkóði>=196?2:1;}
static int COLUMN(int gögn_staða){int stafkóði=0;for(int 순번=Keyra_2(gögn_staða);순번<gögn_staða;순번=Áfram_vara(순번))stafkóði+=Texti[순번]=='\t'?4-stafkóði%4:너비(Texti[순번]);return stafkóði;}
static void gátstaður(void){for(int 순번=0;순번<lengd_VALUE;순번++)afturkalla_gögn[순번]=Texti[순번];afturkalla_lengd=lengd_VALUE;위쪽=INDEX_VALUE;afturkalla_Breytingar=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){gátstaður();for(int 순번=도착위치;순번<lengd_VALUE;순번++)Texti[출발위치+순번-도착위치]=Texti[순번];lengd_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *strengur_gögn,int vara_COUNT){if(vara_COUNT>ritill_afkastageta-lengd_VALUE){알림문="File full (16384 bytes)";return 0;}gátstaður();for(int 순번=lengd_VALUE-1;순번>=INDEX_VALUE;순번--)Texti[순번+vara_COUNT]=Texti[순번];for(int 순번=0;순번<vara_COUNT;순번++)Texti[INDEX_VALUE+순번]=strengur_gögn[순번];lengd_VALUE+=vara_COUNT;INDEX_VALUE+=vara_COUNT;변경됨=1;return 1;}
static void Lóðrétt(int 차이){int COLUMN_staða=COLUMN(INDEX_VALUE),gögn_staða=Keyra_2(INDEX_VALUE);if(차이<0){if(!gögn_staða)return;gögn_staða=Keyra_2(gögn_staða-1);}else{gögn_staða=ljúka_OFFSET(gögn_staða);if(gögn_staða==lengd_VALUE)return;gögn_staða++;}int stafkóði=0;while(gögn_staða<lengd_VALUE&&Texti[gögn_staða]!='\n'&&stafkóði<COLUMN_staða){stafkóði+=Texti[gögn_staða]=='\t'?4-stafkóði%4:너비(Texti[gögn_staða]);gögn_staða=Áfram_vara(gögn_staða);}INDEX_VALUE=gögn_staða;}
static void 화면그리기(void){
    if(INDEX_VALUE>lengd_VALUE)INDEX_VALUE=lengd_VALUE;if(맨위>INDEX_VALUE)맨위=Keyra_2(INDEX_VALUE);맨위=Keyra_2(맨위);
    int ROW_staða=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Texti[순번]=='\n')ROW_staða++;
    while(ROW_staða>=ROW_COUNT-1){맨위=ljúka_OFFSET(맨위);if(맨위<lengd_VALUE)맨위++;ROW_staða--;}
    int COLUMN_staða=COLUMN(INDEX_VALUE);if(COLUMN_staða<왼쪽)왼쪽=COLUMN_staða;if(COLUMN_staða-왼쪽>=COLUMNS-1)왼쪽=COLUMN_staða-COLUMNS+2;
    글내보내기("\033[?25l");int gögn_staða=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        færa_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int stafkóði=0,그려진상태=0;
        if(gögn_staða>=lengd_VALUE&&반환값>ROW_staða){글내보내기("\033[90m~\033[0m");continue;}
        while(gögn_staða<lengd_VALUE&&Texti[gögn_staða]!='\n'){
            int Áfram_OFFSET=Áfram_vara(gögn_staða),너비값=Texti[gögn_staða]=='\t'?4-stafkóði%4:너비(Texti[gögn_staða]);
            if(stafkóði>=왼쪽&&stafkóði-왼쪽+너비값<COLUMNS){
                if(Texti[gögn_staða]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bæti_gögn(' ');}else if(Texti[gögn_staða]<32||Texti[gögn_staða]==127){bæti_gögn('?');}else for(int 안쪽순번=gögn_staða;안쪽순번<Áfram_OFFSET;안쪽순번++)bæti_gögn(Texti[안쪽순번]);그려진상태+=너비값;
            }stafkóði+=너비값;gögn_staða=Áfram_OFFSET;
        }
        (void)그려진상태;if(gögn_staða<lengd_VALUE)gögn_staða++;
    }
    færa_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");staða_mynd=1;staða_biðröð=0;글내보내기(setja_inn?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(skrá_færsla_heiti[이름바이트수]&&이름바이트수<30)bæti_gögn(skrá_færsla_heiti[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Lína=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Texti[순번]=='\n')Lína++;수치(Lína);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int vara_COUNT=0;글내보내기(" | ");while(알림문[vara_COUNT]&&vara_COUNT<20)bæti_gögn(알림문[vara_COUNT++]);}
    staða_mynd=0;글내보내기("\033[0m");færa_VALUE(ROW_staða+1,COLUMN_staða-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(Í_bið_Lykill){int 셋째순번=Í_bið_Lykill;Í_bið_Lykill=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Stærð=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Stærð&65535)||ROW_COUNT!=(int)(Stærð>>16)){
            COLUMNS=Stærð&65535;ROW_COUNT=Stærð>>16;화면그리기();
            if(hjálp_tegund){færa_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bæti_gögn(hjálp_tegund);글내보내기(Skipun);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){Í_bið_Lykill=셋째순번;return 27;}
    int vara_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){vara_COUNT=vara_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return vara_COUNT==3?1007:vara_COUNT==5?1008:vara_COUNT==6?1009:vara_COUNT==1?1005:vara_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int skrá_hald=opið_skrá(skrá_færsla_heiti,les_skrifheimild|없으면만들기|내용비우기,0600);if(skrá_hald<0){알림문="Cannot open for save";return 0;}
    intptr_t vara_COUNT=skrifa_skrá_gögn(skrá_hald,Texti,lengd_VALUE);loka_skrá(skrá_hald);if(vara_COUNT!=lengd_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Áfram(void){int vara_COUNT=0;while(FIND_færsla[vara_COUNT])vara_COUNT++;if(!vara_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=lengd_VALUE;순번++){int gögn_staða=(INDEX_VALUE+순번)%(lengd_VALUE?lengd_VALUE:1),안쪽순번=0;while(안쪽순번<vara_COUNT&&gögn_staða+안쪽순번<lengd_VALUE&&Texti[gögn_staða+안쪽순번]==(unsigned char)FIND_færsla[안쪽순번])안쪽순번++;if(안쪽순번==vara_COUNT){INDEX_VALUE=gögn_staða;알림문="Match";return;}}알림문="Pattern not found";}
static int biðja(int tegund_VALUE){
    int vara_COUNT=0;Skipun[0]=0;
    for(;;){færa_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bæti_gögn(tegund_VALUE);글내보내기(Skipun);출력비우기();hjálp_tegund=tegund_VALUE;int 셋째순번=누름값();hjálp_tegund=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(vara_COUNT){vara_COUNT--;while(vara_COUNT>0&&((unsigned char)Skipun[vara_COUNT]&192)==128)vara_COUNT--;Skipun[vara_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&vara_COUNT<120){Skipun[vara_COUNT++]=셋째순번;Skipun[vara_COUNT]=0;}
    }
    if(tegund_VALUE=='/'){for(int 순번=0;순번<=vara_COUNT;순번++)FIND_færsla[순번]=Skipun[순번];FIND_Áfram();return 0;}
    if(같은지(Skipun,"q!"))return 1;
    if(같은지(Skipun,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Skipun,"wq")||같은지(Skipun,"x"))return Store_VALUE();
    if(같은지(Skipun,"w")){Store_VALUE();return 0;}
    if(Skipun[0]=='w'&&Skipun[1]==' '){int 순번=2;while(Skipun[순번]==' ')순번++;int Stærð=vara_COUNT-순번;if(Stærð<1||Stærð>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Stærð;안쪽순번++)skrá_færsla_heiti[안쪽순번]=Skipun[순번+안쪽순번];skrá_færsla_heiti[Stærð]=0;Store_VALUE();return 0;}
    int Lína=0;for(int 순번=0;순번<vara_COUNT;순번++){if(Skipun[순번]<'0'||Skipun[순번]>'9'){Lína=0;break;}Lína=Lína*10+Skipun[순번]-'0';if(Lína>16384){Lína=0;break;}}
    if(Lína){INDEX_VALUE=0;while(--Lína&&INDEX_VALUE<lengd_VALUE){INDEX_VALUE=ljúka_OFFSET(INDEX_VALUE);if(INDEX_VALUE<lengd_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Opna_notandi_forrit(int 무시값){
    (void)무시값;if(notandi_frumbreyta_COUNT()!=1||notandi_frumbreyta(0,skrá_færsla_heiti,sizeof(skrá_færsla_heiti))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int skrá_hald=opið_skrá(skrá_færsla_heiti,skrifvarið_VALUE,0);
    if(skrá_hald>=0){int vara_COUNT=skrá_breyta_stærð(skrá_hald);if(vara_COUNT<0||vara_COUNT>ritill_afkastageta){loka_skrá(skrá_hald);return 1;}lengd_VALUE=파일자료읽기(skrá_hald,Texti,vara_COUNT);loka_skrá(skrá_hald);if(lengd_VALUE!=vara_COUNT)return 1;for(int 순번=0;순번<lengd_VALUE;순번++)if(!Texti[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(villa_númer!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,hætta_forrit=0;
    while(!hætta_forrit){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Lóðrétt(-1);continue;}if(셋째순번==1002){Lóðrétt(1);continue;}if(셋째순번==1003){INDEX_VALUE=Áfram_vara(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Keyra_2(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=ljúka_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Lóðrétt(셋째순번==1008?-1:1);continue;}
        if(setja_inn){
            if(셋째순번==27||셋째순번==3){setja_inn=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<lengd_VALUE)바이트지우기(INDEX_VALUE,Áfram_vara(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int vara_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!vara_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<vara_COUNT;순번++){int stafkóði=누름값();if(stafkóði<128||stafkóði>191){Í_bið_Lykill=stafkóði;유효함=0;break;}SECOND_VALUE[순번]=stafkóði;}
                if(유효함)덧붙이기(SECOND_VALUE,vara_COUNT);
            }continue;
        }
        if(앞부분){int gögn_staða=앞부분;앞부분=0;if(gögn_staða=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(gögn_staða=='Z'&&셋째순번=='Z'){hætta_forrit=Store_VALUE();continue;}if((gögn_staða=='d'&&셋째순번=='d')||(gögn_staða=='y'&&셋째순번=='y')){int 첫째값=Keyra_2(INDEX_VALUE),SECOND_VALUE=ljúka_OFFSET(INDEX_VALUE);if(SECOND_VALUE<lengd_VALUE)SECOND_VALUE++;afrita_lengd=SECOND_VALUE-첫째값;for(int 순번=0;순번<afrita_lengd;순번++)복사자료[순번]=Texti[첫째값+순번];if(gögn_staða=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){setja_inn=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<ljúka_OFFSET(INDEX_VALUE))INDEX_VALUE=Áfram_vara(INDEX_VALUE);setja_inn=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Keyra_2(INDEX_VALUE);setja_inn=1;continue;}if(셋째순번=='A'){INDEX_VALUE=ljúka_OFFSET(INDEX_VALUE);setja_inn=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char lína_ljúka='\n';INDEX_VALUE=셋째순번=='o'?ljúka_OFFSET(INDEX_VALUE):Keyra_2(INDEX_VALUE);if(덧붙이기(&lína_ljúka,1)){if(셋째순번=='O')INDEX_VALUE--;setja_inn=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Áfram_vara(INDEX_VALUE);continue;}if(셋째순번=='j'){Lóðrétt(1);continue;}if(셋째순번=='k'){Lóðrétt(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Keyra_2(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=ljúka_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Keyra_2(lengd_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<lengd_VALUE)바이트지우기(INDEX_VALUE,Áfram_vara(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&afrita_lengd){INDEX_VALUE=ljúka_OFFSET(INDEX_VALUE);if(INDEX_VALUE<lengd_VALUE)INDEX_VALUE++;덧붙이기(복사자료,afrita_lengd);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<ritill_afkastageta;순번++){unsigned char SECOND_VALUE=Texti[순번];Texti[순번]=afturkalla_gögn[순번];afturkalla_gögn[순번]=SECOND_VALUE;}int vara_COUNT=lengd_VALUE;lengd_VALUE=afturkalla_lengd;afturkalla_lengd=vara_COUNT;vara_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=vara_COUNT;vara_COUNT=변경됨;변경됨=afturkalla_Breytingar;afturkalla_Breytingar=vara_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){hætta_forrit=biðja(셋째순번);continue;}if(셋째순번=='n'){FIND_Áfram();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
