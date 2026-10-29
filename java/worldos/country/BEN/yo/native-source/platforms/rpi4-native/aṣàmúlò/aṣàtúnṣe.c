/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char SMS[편집용량],padàsẹ́yìn_détà[편집용량],복사자료[편집용량],결과자료[1024];
static int gígùn_iye,wá_atọ̀ka_àkóónú_iye,맨위,왼쪽,변경됨,ṣèfibọ̀,padàsẹ́yìn_gígùn,위쪽,padàsẹ́yìn_Àwọn_àyípadà,되돌림있음,ṣẹ̀dà_gígùn,사용량,열수=68,행수=19;
static char fáìlì_ìgbéwọlé_orúkọ[64],Àṣẹ[128],wá_ìgbéwọlé[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned Wànídúró_ráńpẹ́_bọ́tìnnì;
static int ìrànwọ́_ìsọ̀rí,ipò_àwòrán,ipò_ìtòléra;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void báìtì_détà(unsigned kóòdù_ẹyọ_ọ̀rọ̀){if(ipò_àwòrán){if((kóòdù_ẹyọ_ọ̀rọ̀&192)!=128){ipò_ìtòléra+=kóòdù_ẹyọ_ọ̀rọ̀>=196?2:1;}if(ipò_ìtòléra>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=kóòdù_ẹyọ_ọ̀rọ̀;}
static void 글내보내기(const char *fọ́nrán_détà){while(*fọ́nrán_détà)báìtì_détà((unsigned char)*fọ́nrán_détà++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)báìtì_détà(둘째값[--순번]);}
static void gbé_iye(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);báìtì_détà(';');수치(열위치);báìtì_détà('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(SMS[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<gígùn_iye){자료위치++;while(자료위치<gígùn_iye&&(SMS[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int Rọ́ọ̀nù(int 자료위치){while(자료위치>0&&SMS[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int parí_Ìtayọ(int 자료위치){while(자료위치<gígùn_iye&&SMS[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned kóòdù_ẹyọ_ọ̀rọ̀){return kóòdù_ẹyọ_ọ̀rọ̀>=196?2:1;}
static int ìlà_òró(int 자료위치){int kóòdù_ẹyọ_ọ̀rọ̀=0;for(int 순번=Rọ́ọ̀nù(자료위치);순번<자료위치;순번=다음(순번))kóòdù_ẹyọ_ọ̀rọ̀+=SMS[순번]=='\t'?4-kóòdù_ẹyọ_ọ̀rọ̀%4:너비(SMS[순번]);return kóòdù_ẹyọ_ọ̀rọ̀;}
static void ibodè(void){for(int 순번=0;순번<gígùn_iye;순번++)padàsẹ́yìn_détà[순번]=SMS[순번];padàsẹ́yìn_gígùn=gígùn_iye;위쪽=wá_atọ̀ka_àkóónú_iye;padàsẹ́yìn_Àwọn_àyípadà=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){ibodè();for(int 순번=도착위치;순번<gígùn_iye;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];gígùn_iye-=도착위치-출발위치;wá_atọ̀ka_àkóónú_iye=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *fọ́nrán_détà,int 개수){if(개수>편집용량-gígùn_iye){알림문="File full (16384 bytes)";return 0;}ibodè();for(int 순번=gígùn_iye-1;순번>=wá_atọ̀ka_àkóónú_iye;순번--)SMS[순번+개수]=SMS[순번];for(int 순번=0;순번<개수;순번++)SMS[wá_atọ̀ka_àkóónú_iye+순번]=fọ́nrán_détà[순번];gígùn_iye+=개수;wá_atọ̀ka_àkóónú_iye+=개수;변경됨=1;return 1;}
static void Atòlóòró(int 차이){int 열위치=ìlà_òró(wá_atọ̀ka_àkóónú_iye),자료위치=Rọ́ọ̀nù(wá_atọ̀ka_àkóónú_iye);if(차이<0){if(!자료위치)return;자료위치=Rọ́ọ̀nù(자료위치-1);}else{자료위치=parí_Ìtayọ(자료위치);if(자료위치==gígùn_iye)return;자료위치++;}int kóòdù_ẹyọ_ọ̀rọ̀=0;while(자료위치<gígùn_iye&&SMS[자료위치]!='\n'&&kóòdù_ẹyọ_ọ̀rọ̀<열위치){kóòdù_ẹyọ_ọ̀rọ̀+=SMS[자료위치]=='\t'?4-kóòdù_ẹyọ_ọ̀rọ̀%4:너비(SMS[자료위치]);자료위치=다음(자료위치);}wá_atọ̀ka_àkóónú_iye=자료위치;}
static void 화면그리기(void){
    if(wá_atọ̀ka_àkóónú_iye>gígùn_iye)wá_atọ̀ka_àkóónú_iye=gígùn_iye;if(맨위>wá_atọ̀ka_àkóónú_iye)맨위=Rọ́ọ̀nù(wá_atọ̀ka_àkóónú_iye);맨위=Rọ́ọ̀nù(맨위);
    int 행위치=0;for(int 순번=맨위;순번<wá_atọ̀ka_àkóónú_iye;순번++)if(SMS[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=parí_Ìtayọ(맨위);if(맨위<gígùn_iye)맨위++;행위치--;}
    int 열위치=ìlà_òró(wá_atọ̀ka_àkóónú_iye);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        gbé_iye(반환값+1,1);글내보내기("\033[0m\033[2K");int kóòdù_ẹyọ_ọ̀rọ̀=0,그려진상태=0;
        if(자료위치>=gígùn_iye&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<gígùn_iye&&SMS[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=SMS[자료위치]=='\t'?4-kóòdù_ẹyọ_ọ̀rọ̀%4:너비(SMS[자료위치]);
            if(kóòdù_ẹyọ_ọ̀rọ̀>=왼쪽&&kóòdù_ẹyọ_ọ̀rọ̀-왼쪽+너비값<열수){
                if(SMS[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)báìtì_détà(' ');}else if(SMS[자료위치]<32||SMS[자료위치]==127){báìtì_détà('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)báìtì_détà(SMS[안쪽순번]);그려진상태+=너비값;
            }kóòdù_ẹyọ_ọ̀rọ̀+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<gígùn_iye)자료위치++;
    }
    gbé_iye(행수,1);글내보내기("\033[7m\033[2K");ipò_àwòrán=1;ipò_ìtòléra=0;글내보내기(ṣèfibọ̀?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(fáìlì_ìgbéwọlé_orúkọ[이름바이트수]&&이름바이트수<30)báìtì_détà(fáìlì_ìgbéwọlé_orúkọ[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int ìlà=1;for(int 순번=0;순번<wá_atọ̀ka_àkóónú_iye;순번++)if(SMS[순번]=='\n')ìlà++;수치(ìlà);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)báìtì_détà(알림문[개수++]);}
    ipò_àwòrán=0;글내보내기("\033[0m");gbé_iye(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(Wànídúró_ráńpẹ́_bọ́tìnnì){int 셋째순번=Wànídúró_ráńpẹ́_bọ́tìnnì;Wànídúró_ráńpẹ́_bọ́tìnnì=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Ìwọ̀n=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(Ìwọ̀n&65535)||행수!=(int)(Ìwọ̀n>>16)){
            열수=Ìwọ̀n&65535;행수=Ìwọ̀n>>16;화면그리기();
            if(ìrànwọ́_ìsọ̀rí){gbé_iye(행수,1);글내보내기("\033[0m\033[2K");báìtì_détà(ìrànwọ́_ìsọ̀rí);글내보내기(Àṣẹ);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){Wànídúró_ráńpẹ́_bọ́tìnnì=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int Store_iye(void){
    int fáìlì_èkù=ṣí_fáìlì(fáìlì_ìgbéwọlé_orúkọ,tí_a_lè_kà_tí_a_lè_kọ|없으면만들기|내용비우기,0600);if(fáìlì_èkù<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=kọ_fáìlì_détà(fáìlì_èkù,SMS,gígùn_iye);pa_dé_fáìlì(fáìlì_èkù);if(개수!=gígùn_iye){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(wá_ìgbéwọlé[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=gígùn_iye;순번++){int 자료위치=(wá_atọ̀ka_àkóónú_iye+순번)%(gígùn_iye?gígùn_iye:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<gígùn_iye&&SMS[자료위치+안쪽순번]==(unsigned char)wá_ìgbéwọlé[안쪽순번])안쪽순번++;if(안쪽순번==개수){wá_atọ̀ka_àkóónú_iye=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int ìgún_ní_kẹ́ṣẹ́(int ìsọ̀rí_iye){
    int 개수=0;Àṣẹ[0]=0;
    for(;;){gbé_iye(행수,1);글내보내기("\033[0m\033[2K");báìtì_détà(ìsọ̀rí_iye);글내보내기(Àṣẹ);출력비우기();ìrànwọ́_ìsọ̀rí=ìsọ̀rí_iye;int 셋째순번=누름값();ìrànwọ́_ìsọ̀rí=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)Àṣẹ[개수]&192)==128)개수--;Àṣẹ[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){Àṣẹ[개수++]=셋째순번;Àṣẹ[개수]=0;}
    }
    if(ìsọ̀rí_iye=='/'){for(int 순번=0;순번<=개수;순번++)wá_ìgbéwọlé[순번]=Àṣẹ[순번];다음찾기();return 0;}
    if(같은지(Àṣẹ,"q!"))return 1;
    if(같은지(Àṣẹ,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Àṣẹ,"wq")||같은지(Àṣẹ,"x"))return Store_iye();
    if(같은지(Àṣẹ,"w")){Store_iye();return 0;}
    if(Àṣẹ[0]=='w'&&Àṣẹ[1]==' '){int 순번=2;while(Àṣẹ[순번]==' ')순번++;int Ìwọ̀n=개수-순번;if(Ìwọ̀n<1||Ìwọ̀n>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Ìwọ̀n;안쪽순번++)fáìlì_ìgbéwọlé_orúkọ[안쪽순번]=Àṣẹ[순번+안쪽순번];fáìlì_ìgbéwọlé_orúkọ[Ìwọ̀n]=0;Store_iye();return 0;}
    int ìlà=0;for(int 순번=0;순번<개수;순번++){if(Àṣẹ[순번]<'0'||Àṣẹ[순번]>'9'){ìlà=0;break;}ìlà=ìlà*10+Àṣẹ[순번]-'0';if(ìlà>16384){ìlà=0;break;}}
    if(ìlà){wá_atọ̀ka_àkóónú_iye=0;while(--ìlà&&wá_atọ̀ka_àkóónú_iye<gígùn_iye){wá_atọ̀ka_àkóónú_iye=parí_Ìtayọ(wá_atọ̀ka_àkóónú_iye);if(wá_atọ̀ka_àkóónú_iye<gígùn_iye)wá_atọ̀ka_àkóónú_iye++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||aṣàmúlò_ágúmẹ́ntì(0,fáìlì_ìgbéwọlé_orúkọ,sizeof(fáìlì_ìgbéwọlé_orúkọ))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int fáìlì_èkù=ṣí_fáìlì(fáìlì_ìgbéwọlé_orúkọ,kàn_kàá_iye,0);
    if(fáìlì_èkù>=0){int 개수=fáìlì_ìwọn(fáìlì_èkù);if(개수<0||개수>편집용량){pa_dé_fáìlì(fáìlì_èkù);return 1;}gígùn_iye=파일자료읽기(fáìlì_èkù,SMS,개수);pa_dé_fáìlì(fáìlì_èkù);if(gígùn_iye!=개수)return 1;for(int 순번=0;순번<gígùn_iye;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Atòlóòró(-1);continue;}if(셋째순번==1002){Atòlóòró(1);continue;}if(셋째순번==1003){wá_atọ̀ka_àkóónú_iye=다음(wá_atọ̀ka_àkóónú_iye);continue;}if(셋째순번==1004){wá_atọ̀ka_àkóónú_iye=이전항목(wá_atọ̀ka_àkóónú_iye);continue;}
        if(셋째순번==1005){wá_atọ̀ka_àkóónú_iye=Rọ́ọ̀nù(wá_atọ̀ka_àkóónú_iye);continue;}if(셋째순번==1006){wá_atọ̀ka_àkóónú_iye=parí_Ìtayọ(wá_atọ̀ka_àkóónú_iye);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)Atòlóòró(셋째순번==1008?-1:1);continue;}
        if(ṣèfibọ̀){
            if(셋째순번==27||셋째순번==3){ṣèfibọ̀=0;continue;}
            if(셋째순번==127||셋째순번==8){if(wá_atọ̀ka_àkóónú_iye)바이트지우기(이전항목(wá_atọ̀ka_àkóónú_iye),wá_atọ̀ka_àkóónú_iye);continue;}
            if(셋째순번==1007){if(wá_atọ̀ka_àkóónú_iye<gígùn_iye)바이트지우기(wá_atọ̀ka_àkóónú_iye,다음(wá_atọ̀ka_àkóónú_iye));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int kóòdù_ẹyọ_ọ̀rọ̀=누름값();if(kóòdù_ẹyọ_ọ̀rọ̀<128||kóòdù_ẹyọ_ọ̀rọ̀>191){Wànídúró_ráńpẹ́_bọ́tìnnì=kóòdù_ẹyọ_ọ̀rọ̀;유효함=0;break;}둘째값[순번]=kóòdù_ẹyọ_ọ̀rọ̀;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){wá_atọ̀ka_àkóónú_iye=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=Store_iye();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=Rọ́ọ̀nù(wá_atọ̀ka_àkóónú_iye),둘째값=parí_Ìtayọ(wá_atọ̀ka_àkóónú_iye);if(둘째값<gígùn_iye)둘째값++;ṣẹ̀dà_gígùn=둘째값-첫째값;for(int 순번=0;순번<ṣẹ̀dà_gígùn;순번++)복사자료[순번]=SMS[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){ṣèfibọ̀=1;continue;}if(셋째순번=='a'){if(wá_atọ̀ka_àkóónú_iye<parí_Ìtayọ(wá_atọ̀ka_àkóónú_iye))wá_atọ̀ka_àkóónú_iye=다음(wá_atọ̀ka_àkóónú_iye);ṣèfibọ̀=1;continue;}
        if(셋째순번=='I'){wá_atọ̀ka_àkóónú_iye=Rọ́ọ̀nù(wá_atọ̀ka_àkóónú_iye);ṣèfibọ̀=1;continue;}if(셋째순번=='A'){wá_atọ̀ka_àkóónú_iye=parí_Ìtayọ(wá_atọ̀ka_àkóónú_iye);ṣèfibọ̀=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char ìlà_parí='\n';wá_atọ̀ka_àkóónú_iye=셋째순번=='o'?parí_Ìtayọ(wá_atọ̀ka_àkóónú_iye):Rọ́ọ̀nù(wá_atọ̀ka_àkóónú_iye);if(덧붙이기(&ìlà_parí,1)){if(셋째순번=='O')wá_atọ̀ka_àkóónú_iye--;ṣèfibọ̀=1;}continue;}
        if(셋째순번=='h'){wá_atọ̀ka_àkóónú_iye=이전항목(wá_atọ̀ka_àkóónú_iye);continue;}if(셋째순번=='l'){wá_atọ̀ka_àkóónú_iye=다음(wá_atọ̀ka_àkóónú_iye);continue;}if(셋째순번=='j'){Atòlóòró(1);continue;}if(셋째순번=='k'){Atòlóòró(-1);continue;}
        if(셋째순번=='0'){wá_atọ̀ka_àkóónú_iye=Rọ́ọ̀nù(wá_atọ̀ka_àkóónú_iye);continue;}if(셋째순번=='$'){wá_atọ̀ka_àkóónú_iye=parí_Ìtayọ(wá_atọ̀ka_àkóónú_iye);continue;}if(셋째순번=='G'){wá_atọ̀ka_àkóónú_iye=Rọ́ọ̀nù(gígùn_iye);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(wá_atọ̀ka_àkóónú_iye<gígùn_iye)바이트지우기(wá_atọ̀ka_àkóónú_iye,다음(wá_atọ̀ka_àkóónú_iye));continue;}
        if(셋째순번=='p'&&ṣẹ̀dà_gígùn){wá_atọ̀ka_àkóónú_iye=parí_Ìtayọ(wá_atọ̀ka_àkóónú_iye);if(wá_atọ̀ka_àkóónú_iye<gígùn_iye)wá_atọ̀ka_àkóónú_iye++;덧붙이기(복사자료,ṣẹ̀dà_gígùn);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=SMS[순번];SMS[순번]=padàsẹ́yìn_détà[순번];padàsẹ́yìn_détà[순번]=둘째값;}int 개수=gígùn_iye;gígùn_iye=padàsẹ́yìn_gígùn;padàsẹ́yìn_gígùn=개수;개수=wá_atọ̀ka_àkóónú_iye;wá_atọ̀ka_àkóónú_iye=위쪽;위쪽=개수;개수=변경됨;변경됨=padàsẹ́yìn_Àwọn_àyípadà;padàsẹ́yìn_Àwọn_àyípadà=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=ìgún_ní_kẹ́ṣẹ́(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
