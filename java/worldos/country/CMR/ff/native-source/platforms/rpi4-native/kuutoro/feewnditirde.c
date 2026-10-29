/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char binndi[편집용량],firtude_keɓe[편집용량],복사자료[편집용량],결과자료[1024];
static int njuuteendi_njaru,joopirdu_njaru,맨위,왼쪽,변경됨,tummbude,firtude_njuuteendi,위쪽,되돌림변경,되돌림있음,waanjitaade_njuuteendi,사용량,열수=68,행수=19;
static char fiilde_naatnugol_innde[64],ginol[128],yiylaade_naatnugol[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned 대기누름;
static int ballal_kategorii,ngonka_natal,ngonka_lappol;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void oktee_keɓe(unsigned 문자값){if(ngonka_natal){if((문자값&192)!=128){ngonka_lappol+=문자값>=196?2:1;}if(ngonka_lappol>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=문자값;}
static void 글내보내기(const char *ɓoggol_keɓe){while(*ɓoggol_keɓe)oktee_keɓe((unsigned char)*ɓoggol_keɓe++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)oktee_keɓe(둘째값[--순번]);}
static void dirtinde_njaru(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);oktee_keɓe(';');수치(열위치);oktee_keɓe('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(binndi[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<njuuteendi_njaru){자료위치++;while(자료위치<njuuteendi_njaru&&(binndi[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int huutoraade(int 자료위치){while(자료위치>0&&binndi[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int 끝위치(int 자료위치){while(자료위치<njuuteendi_njaru&&binndi[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned 문자값){return 문자값>=196?2:1;}
static int darol(int 자료위치){int 문자값=0;for(int 순번=huutoraade(자료위치);순번<자료위치;순번=다음(순번))문자값+=binndi[순번]=='\t'?4-문자값%4:너비(binndi[순번]);return 문자값;}
static void aynirde(void){for(int 순번=0;순번<njuuteendi_njaru;순번++)firtude_keɓe[순번]=binndi[순번];firtude_njuuteendi=njuuteendi_njaru;위쪽=joopirdu_njaru;되돌림변경=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){aynirde();for(int 순번=도착위치;순번<njuuteendi_njaru;순번++)binndi[출발위치+순번-도착위치]=binndi[순번];njuuteendi_njaru-=도착위치-출발위치;joopirdu_njaru=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *ɓoggol_keɓe,int 개수){if(개수>편집용량-njuuteendi_njaru){알림문="File full (16384 bytes)";return 0;}aynirde();for(int 순번=njuuteendi_njaru-1;순번>=joopirdu_njaru;순번--)binndi[순번+개수]=binndi[순번];for(int 순번=0;순번<개수;순번++)binndi[joopirdu_njaru+순번]=ɓoggol_keɓe[순번];njuuteendi_njaru+=개수;joopirdu_njaru+=개수;변경됨=1;return 1;}
static void 세로이동(int 차이){int 열위치=darol(joopirdu_njaru),자료위치=huutoraade(joopirdu_njaru);if(차이<0){if(!자료위치)return;자료위치=huutoraade(자료위치-1);}else{자료위치=끝위치(자료위치);if(자료위치==njuuteendi_njaru)return;자료위치++;}int 문자값=0;while(자료위치<njuuteendi_njaru&&binndi[자료위치]!='\n'&&문자값<열위치){문자값+=binndi[자료위치]=='\t'?4-문자값%4:너비(binndi[자료위치]);자료위치=다음(자료위치);}joopirdu_njaru=자료위치;}
static void 화면그리기(void){
    if(joopirdu_njaru>njuuteendi_njaru)joopirdu_njaru=njuuteendi_njaru;if(맨위>joopirdu_njaru)맨위=huutoraade(joopirdu_njaru);맨위=huutoraade(맨위);
    int 행위치=0;for(int 순번=맨위;순번<joopirdu_njaru;순번++)if(binndi[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=끝위치(맨위);if(맨위<njuuteendi_njaru)맨위++;행위치--;}
    int 열위치=darol(joopirdu_njaru);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        dirtinde_njaru(반환값+1,1);글내보내기("\033[0m\033[2K");int 문자값=0,그려진상태=0;
        if(자료위치>=njuuteendi_njaru&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<njuuteendi_njaru&&binndi[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=binndi[자료위치]=='\t'?4-문자값%4:너비(binndi[자료위치]);
            if(문자값>=왼쪽&&문자값-왼쪽+너비값<열수){
                if(binndi[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)oktee_keɓe(' ');}else if(binndi[자료위치]<32||binndi[자료위치]==127){oktee_keɓe('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)oktee_keɓe(binndi[안쪽순번]);그려진상태+=너비값;
            }문자값+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<njuuteendi_njaru)자료위치++;
    }
    dirtinde_njaru(행수,1);글내보내기("\033[7m\033[2K");ngonka_natal=1;ngonka_lappol=0;글내보내기(tummbude?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(fiilde_naatnugol_innde[이름바이트수]&&이름바이트수<30)oktee_keɓe(fiilde_naatnugol_innde[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int diidol=1;for(int 순번=0;순번<joopirdu_njaru;순번++)if(binndi[순번]=='\n')diidol++;수치(diidol);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)oktee_keɓe(알림문[개수++]);}
    ngonka_natal=0;글내보내기("\033[0m");dirtinde_njaru(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(대기누름){int 셋째순번=대기누름;대기누름=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned waylude_etannde=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(waylude_etannde&65535)||행수!=(int)(waylude_etannde>>16)){
            열수=waylude_etannde&65535;행수=waylude_etannde>>16;화면그리기();
            if(ballal_kategorii){dirtinde_njaru(행수,1);글내보내기("\033[0m\033[2K");oktee_keɓe(ballal_kategorii);글내보내기(ginol);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){대기누름=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int resde_njaru(void){
    int fiilde_jaggoode=udditde_fiilde(fiilde_naatnugol_innde,tar_winndu|없으면만들기|내용비우기,0600);if(fiilde_jaggoode<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=winndude_fiilde_keɓe(fiilde_jaggoode,binndi,njuuteendi_njaru);uddude_fiilde(fiilde_jaggoode);if(개수!=njuuteendi_njaru){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(yiylaade_naatnugol[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=njuuteendi_njaru;순번++){int 자료위치=(joopirdu_njaru+순번)%(njuuteendi_njaru?njuuteendi_njaru:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<njuuteendi_njaru&&binndi[자료위치+안쪽순번]==(unsigned char)yiylaade_naatnugol[안쪽순번])안쪽순번++;if(안쪽순번==개수){joopirdu_njaru=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int hirjinaango(int kategorii_njaru){
    int 개수=0;ginol[0]=0;
    for(;;){dirtinde_njaru(행수,1);글내보내기("\033[0m\033[2K");oktee_keɓe(kategorii_njaru);글내보내기(ginol);출력비우기();ballal_kategorii=kategorii_njaru;int 셋째순번=누름값();ballal_kategorii=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)ginol[개수]&192)==128)개수--;ginol[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){ginol[개수++]=셋째순번;ginol[개수]=0;}
    }
    if(kategorii_njaru=='/'){for(int 순번=0;순번<=개수;순번++)yiylaade_naatnugol[순번]=ginol[순번];다음찾기();return 0;}
    if(같은지(ginol,"q!"))return 1;
    if(같은지(ginol,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(ginol,"wq")||같은지(ginol,"x"))return resde_njaru();
    if(같은지(ginol,"w")){resde_njaru();return 0;}
    if(ginol[0]=='w'&&ginol[1]==' '){int 순번=2;while(ginol[순번]==' ')순번++;int waylude_etannde=개수-순번;if(waylude_etannde<1||waylude_etannde>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<waylude_etannde;안쪽순번++)fiilde_naatnugol_innde[안쪽순번]=ginol[순번+안쪽순번];fiilde_naatnugol_innde[waylude_etannde]=0;resde_njaru();return 0;}
    int diidol=0;for(int 순번=0;순번<개수;순번++){if(ginol[순번]<'0'||ginol[순번]>'9'){diidol=0;break;}diidol=diidol*10+ginol[순번]-'0';if(diidol>16384){diidol=0;break;}}
    if(diidol){joopirdu_njaru=0;while(--diidol&&joopirdu_njaru<njuuteendi_njaru){joopirdu_njaru=끝위치(joopirdu_njaru);if(joopirdu_njaru<njuuteendi_njaru)joopirdu_njaru++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int huɓɓude_kuutoro_tafirde(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||kuutoro_hujja(0,fiilde_naatnugol_innde,sizeof(fiilde_naatnugol_innde))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int fiilde_jaggoode=udditde_fiilde(fiilde_naatnugol_innde,janngotooɗo_tan_njaru,0);
    if(fiilde_jaggoode>=0){int 개수=fiilde_waylude_etannde(fiilde_jaggoode);if(개수<0||개수>편집용량){uddude_fiilde(fiilde_jaggoode);return 1;}njuuteendi_njaru=파일자료읽기(fiilde_jaggoode,binndi,개수);uddude_fiilde(fiilde_jaggoode);if(njuuteendi_njaru!=개수)return 1;for(int 순번=0;순번<njuuteendi_njaru;순번++)if(!binndi[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){세로이동(-1);continue;}if(셋째순번==1002){세로이동(1);continue;}if(셋째순번==1003){joopirdu_njaru=다음(joopirdu_njaru);continue;}if(셋째순번==1004){joopirdu_njaru=이전항목(joopirdu_njaru);continue;}
        if(셋째순번==1005){joopirdu_njaru=huutoraade(joopirdu_njaru);continue;}if(셋째순번==1006){joopirdu_njaru=끝위치(joopirdu_njaru);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)세로이동(셋째순번==1008?-1:1);continue;}
        if(tummbude){
            if(셋째순번==27||셋째순번==3){tummbude=0;continue;}
            if(셋째순번==127||셋째순번==8){if(joopirdu_njaru)바이트지우기(이전항목(joopirdu_njaru),joopirdu_njaru);continue;}
            if(셋째순번==1007){if(joopirdu_njaru<njuuteendi_njaru)바이트지우기(joopirdu_njaru,다음(joopirdu_njaru));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int 문자값=누름값();if(문자값<128||문자값>191){대기누름=문자값;유효함=0;break;}둘째값[순번]=문자값;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){joopirdu_njaru=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=resde_njaru();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=huutoraade(joopirdu_njaru),둘째값=끝위치(joopirdu_njaru);if(둘째값<njuuteendi_njaru)둘째값++;waanjitaade_njuuteendi=둘째값-첫째값;for(int 순번=0;순번<waanjitaade_njuuteendi;순번++)복사자료[순번]=binndi[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){tummbude=1;continue;}if(셋째순번=='a'){if(joopirdu_njaru<끝위치(joopirdu_njaru))joopirdu_njaru=다음(joopirdu_njaru);tummbude=1;continue;}
        if(셋째순번=='I'){joopirdu_njaru=huutoraade(joopirdu_njaru);tummbude=1;continue;}if(셋째순번=='A'){joopirdu_njaru=끝위치(joopirdu_njaru);tummbude=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char diidol_taƴde='\n';joopirdu_njaru=셋째순번=='o'?끝위치(joopirdu_njaru):huutoraade(joopirdu_njaru);if(덧붙이기(&diidol_taƴde,1)){if(셋째순번=='O')joopirdu_njaru--;tummbude=1;}continue;}
        if(셋째순번=='h'){joopirdu_njaru=이전항목(joopirdu_njaru);continue;}if(셋째순번=='l'){joopirdu_njaru=다음(joopirdu_njaru);continue;}if(셋째순번=='j'){세로이동(1);continue;}if(셋째순번=='k'){세로이동(-1);continue;}
        if(셋째순번=='0'){joopirdu_njaru=huutoraade(joopirdu_njaru);continue;}if(셋째순번=='$'){joopirdu_njaru=끝위치(joopirdu_njaru);continue;}if(셋째순번=='G'){joopirdu_njaru=huutoraade(njuuteendi_njaru);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(joopirdu_njaru<njuuteendi_njaru)바이트지우기(joopirdu_njaru,다음(joopirdu_njaru));continue;}
        if(셋째순번=='p'&&waanjitaade_njuuteendi){joopirdu_njaru=끝위치(joopirdu_njaru);if(joopirdu_njaru<njuuteendi_njaru)joopirdu_njaru++;덧붙이기(복사자료,waanjitaade_njuuteendi);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=binndi[순번];binndi[순번]=firtude_keɓe[순번];firtude_keɓe[순번]=둘째값;}int 개수=njuuteendi_njaru;njuuteendi_njaru=firtude_njuuteendi;firtude_njuuteendi=개수;개수=joopirdu_njaru;joopirdu_njaru=위쪽;위쪽=개수;개수=변경됨;변경됨=되돌림변경;되돌림변경=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=hirjinaango(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
