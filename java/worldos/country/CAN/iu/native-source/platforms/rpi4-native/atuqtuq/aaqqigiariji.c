/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char titiqqaq[편집용량],utiqtilli_titiqqat[편집용량],복사자료[편집용량],결과자료[1024];
static int takininga_atuutilik,nalunaiqsimavik_atuutilik,맨위,왼쪽,변경됨,ilili,utiqtilli_takininga,위쪽,되돌림변경,되돌림있음,ijjuarli_takininga,사용량,열수=68,행수=19;
static char ini_Iliniku_atiq[64],piqujijjut[128],nanili_Iliniku[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned 대기누름;
static int Ikajuqtau_Ataqatigiivvik,qanuilinganiq_ajjinnguaq,qanuilinganiq_utaqqivik;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void byte_titiqqat(unsigned immikkuuqtumut_nalunaikkut){if(qanuilinganiq_ajjinnguaq){if((immikkuuqtumut_nalunaikkut&192)!=128){qanuilinganiq_utaqqivik+=immikkuuqtumut_nalunaikkut>=196?2:1;}if(qanuilinganiq_utaqqivik>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=immikkuuqtumut_nalunaikkut;}
static void 글내보내기(const char *qimiaq_titiqqat){while(*qimiaq_titiqqat)byte_titiqqat((unsigned char)*qimiaq_titiqqat++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)byte_titiqqat(둘째값[--순번]);}
static void nuulli_atuutilik(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);byte_titiqqat(';');수치(열위치);byte_titiqqat('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(titiqqaq[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<takininga_atuutilik){자료위치++;while(자료위치<takininga_atuutilik&&(titiqqaq[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int 시작(int 자료위치){while(자료위치>0&&titiqqaq[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int 끝위치(int 자료위치){while(자료위치<takininga_atuutilik&&titiqqaq[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned immikkuuqtumut_nalunaikkut){return immikkuuqtumut_nalunaikkut>=196?2:1;}
static int ammukutaak(int 자료위치){int immikkuuqtumut_nalunaikkut=0;for(int 순번=시작(자료위치);순번<자료위치;순번=다음(순번))immikkuuqtumut_nalunaikkut+=titiqqaq[순번]=='\t'?4-immikkuuqtumut_nalunaikkut%4:너비(titiqqaq[순번]);return immikkuuqtumut_nalunaikkut;}
static void pigiarvissaq(void){for(int 순번=0;순번<takininga_atuutilik;순번++)utiqtilli_titiqqat[순번]=titiqqaq[순번];utiqtilli_takininga=takininga_atuutilik;위쪽=nalunaiqsimavik_atuutilik;되돌림변경=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){pigiarvissaq();for(int 순번=도착위치;순번<takininga_atuutilik;순번++)titiqqaq[출발위치+순번-도착위치]=titiqqaq[순번];takininga_atuutilik-=도착위치-출발위치;nalunaiqsimavik_atuutilik=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *qimiaq_titiqqat,int 개수){if(개수>편집용량-takininga_atuutilik){알림문="File full (16384 bytes)";return 0;}pigiarvissaq();for(int 순번=takininga_atuutilik-1;순번>=nalunaiqsimavik_atuutilik;순번--)titiqqaq[순번+개수]=titiqqaq[순번];for(int 순번=0;순번<개수;순번++)titiqqaq[nalunaiqsimavik_atuutilik+순번]=qimiaq_titiqqat[순번];takininga_atuutilik+=개수;nalunaiqsimavik_atuutilik+=개수;변경됨=1;return 1;}
static void 세로이동(int 차이){int 열위치=ammukutaak(nalunaiqsimavik_atuutilik),자료위치=시작(nalunaiqsimavik_atuutilik);if(차이<0){if(!자료위치)return;자료위치=시작(자료위치-1);}else{자료위치=끝위치(자료위치);if(자료위치==takininga_atuutilik)return;자료위치++;}int immikkuuqtumut_nalunaikkut=0;while(자료위치<takininga_atuutilik&&titiqqaq[자료위치]!='\n'&&immikkuuqtumut_nalunaikkut<열위치){immikkuuqtumut_nalunaikkut+=titiqqaq[자료위치]=='\t'?4-immikkuuqtumut_nalunaikkut%4:너비(titiqqaq[자료위치]);자료위치=다음(자료위치);}nalunaiqsimavik_atuutilik=자료위치;}
static void 화면그리기(void){
    if(nalunaiqsimavik_atuutilik>takininga_atuutilik)nalunaiqsimavik_atuutilik=takininga_atuutilik;if(맨위>nalunaiqsimavik_atuutilik)맨위=시작(nalunaiqsimavik_atuutilik);맨위=시작(맨위);
    int 행위치=0;for(int 순번=맨위;순번<nalunaiqsimavik_atuutilik;순번++)if(titiqqaq[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=끝위치(맨위);if(맨위<takininga_atuutilik)맨위++;행위치--;}
    int 열위치=ammukutaak(nalunaiqsimavik_atuutilik);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        nuulli_atuutilik(반환값+1,1);글내보내기("\033[0m\033[2K");int immikkuuqtumut_nalunaikkut=0,그려진상태=0;
        if(자료위치>=takininga_atuutilik&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<takininga_atuutilik&&titiqqaq[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=titiqqaq[자료위치]=='\t'?4-immikkuuqtumut_nalunaikkut%4:너비(titiqqaq[자료위치]);
            if(immikkuuqtumut_nalunaikkut>=왼쪽&&immikkuuqtumut_nalunaikkut-왼쪽+너비값<열수){
                if(titiqqaq[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_titiqqat(' ');}else if(titiqqaq[자료위치]<32||titiqqaq[자료위치]==127){byte_titiqqat('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)byte_titiqqat(titiqqaq[안쪽순번]);그려진상태+=너비값;
            }immikkuuqtumut_nalunaikkut+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<takininga_atuutilik)자료위치++;
    }
    nuulli_atuutilik(행수,1);글내보내기("\033[7m\033[2K");qanuilinganiq_ajjinnguaq=1;qanuilinganiq_utaqqivik=0;글내보내기(ilili?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(ini_Iliniku_atiq[이름바이트수]&&이름바이트수<30)byte_titiqqat(ini_Iliniku_atiq[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int titikutaak=1;for(int 순번=0;순번<nalunaiqsimavik_atuutilik;순번++)if(titiqqaq[순번]=='\n')titikutaak++;수치(titikutaak);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)byte_titiqqat(알림문[개수++]);}
    qanuilinganiq_ajjinnguaq=0;글내보내기("\033[0m");nuulli_atuutilik(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(대기누름){int 셋째순번=대기누름;대기누름=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned anininga=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(anininga&65535)||행수!=(int)(anininga>>16)){
            열수=anininga&65535;행수=anininga>>16;화면그리기();
            if(Ikajuqtau_Ataqatigiivvik){nuulli_atuutilik(행수,1);글내보내기("\033[0m\033[2K");byte_titiqqat(Ikajuqtau_Ataqatigiivvik);글내보내기(piqujijjut);출력비우기();}
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
static int tuqqurli_atuutilik(void){
    int ini_nuuttarut=matuirli_ini(ini_Iliniku_atiq,uqalimaarli_titirarli|없으면만들기|내용비우기,0600);if(ini_nuuttarut<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=titiraq_ini_titiqqat(ini_nuuttarut,titiqqaq,takininga_atuutilik);matuli_ini(ini_nuuttarut);if(개수!=takininga_atuutilik){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(nanili_Iliniku[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=takininga_atuutilik;순번++){int 자료위치=(nalunaiqsimavik_atuutilik+순번)%(takininga_atuutilik?takininga_atuutilik:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<takininga_atuutilik&&titiqqaq[자료위치+안쪽순번]==(unsigned char)nanili_Iliniku[안쪽순번])안쪽순번++;if(안쪽순번==개수){nalunaiqsimavik_atuutilik=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int inattijjut(int Ataqatigiivvik_atuutilik){
    int 개수=0;piqujijjut[0]=0;
    for(;;){nuulli_atuutilik(행수,1);글내보내기("\033[0m\033[2K");byte_titiqqat(Ataqatigiivvik_atuutilik);글내보내기(piqujijjut);출력비우기();Ikajuqtau_Ataqatigiivvik=Ataqatigiivvik_atuutilik;int 셋째순번=누름값();Ikajuqtau_Ataqatigiivvik=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)piqujijjut[개수]&192)==128)개수--;piqujijjut[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){piqujijjut[개수++]=셋째순번;piqujijjut[개수]=0;}
    }
    if(Ataqatigiivvik_atuutilik=='/'){for(int 순번=0;순번<=개수;순번++)nanili_Iliniku[순번]=piqujijjut[순번];다음찾기();return 0;}
    if(같은지(piqujijjut,"q!"))return 1;
    if(같은지(piqujijjut,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(piqujijjut,"wq")||같은지(piqujijjut,"x"))return tuqqurli_atuutilik();
    if(같은지(piqujijjut,"w")){tuqqurli_atuutilik();return 0;}
    if(piqujijjut[0]=='w'&&piqujijjut[1]==' '){int 순번=2;while(piqujijjut[순번]==' ')순번++;int anininga=개수-순번;if(anininga<1||anininga>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<anininga;안쪽순번++)ini_Iliniku_atiq[안쪽순번]=piqujijjut[순번+안쪽순번];ini_Iliniku_atiq[anininga]=0;tuqqurli_atuutilik();return 0;}
    int titikutaak=0;for(int 순번=0;순번<개수;순번++){if(piqujijjut[순번]<'0'||piqujijjut[순번]>'9'){titikutaak=0;break;}titikutaak=titikutaak*10+piqujijjut[순번]-'0';if(titikutaak>16384){titikutaak=0;break;}}
    if(titikutaak){nalunaiqsimavik_atuutilik=0;while(--titikutaak&&nalunaiqsimavik_atuutilik<takininga_atuutilik){nalunaiqsimavik_atuutilik=끝위치(nalunaiqsimavik_atuutilik);if(nalunaiqsimavik_atuutilik<takininga_atuutilik)nalunaiqsimavik_atuutilik++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int pigiarli_atuqtuq_pilirijjut(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||atuqtuq_aturniqarnirainiq(0,ini_Iliniku_atiq,sizeof(ini_Iliniku_atiq))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int ini_nuuttarut=matuirli_ini(ini_Iliniku_atiq,takugatuinnaq_atuutilik,0);
    if(ini_nuuttarut>=0){int 개수=ini_anininga(ini_nuuttarut);if(개수<0||개수>편집용량){matuli_ini(ini_nuuttarut);return 1;}takininga_atuutilik=파일자료읽기(ini_nuuttarut,titiqqaq,개수);matuli_ini(ini_nuuttarut);if(takininga_atuutilik!=개수)return 1;for(int 순번=0;순번<takininga_atuutilik;순번++)if(!titiqqaq[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){세로이동(-1);continue;}if(셋째순번==1002){세로이동(1);continue;}if(셋째순번==1003){nalunaiqsimavik_atuutilik=다음(nalunaiqsimavik_atuutilik);continue;}if(셋째순번==1004){nalunaiqsimavik_atuutilik=이전항목(nalunaiqsimavik_atuutilik);continue;}
        if(셋째순번==1005){nalunaiqsimavik_atuutilik=시작(nalunaiqsimavik_atuutilik);continue;}if(셋째순번==1006){nalunaiqsimavik_atuutilik=끝위치(nalunaiqsimavik_atuutilik);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)세로이동(셋째순번==1008?-1:1);continue;}
        if(ilili){
            if(셋째순번==27||셋째순번==3){ilili=0;continue;}
            if(셋째순번==127||셋째순번==8){if(nalunaiqsimavik_atuutilik)바이트지우기(이전항목(nalunaiqsimavik_atuutilik),nalunaiqsimavik_atuutilik);continue;}
            if(셋째순번==1007){if(nalunaiqsimavik_atuutilik<takininga_atuutilik)바이트지우기(nalunaiqsimavik_atuutilik,다음(nalunaiqsimavik_atuutilik));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int immikkuuqtumut_nalunaikkut=누름값();if(immikkuuqtumut_nalunaikkut<128||immikkuuqtumut_nalunaikkut>191){대기누름=immikkuuqtumut_nalunaikkut;유효함=0;break;}둘째값[순번]=immikkuuqtumut_nalunaikkut;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){nalunaiqsimavik_atuutilik=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=tuqqurli_atuutilik();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=시작(nalunaiqsimavik_atuutilik),둘째값=끝위치(nalunaiqsimavik_atuutilik);if(둘째값<takininga_atuutilik)둘째값++;ijjuarli_takininga=둘째값-첫째값;for(int 순번=0;순번<ijjuarli_takininga;순번++)복사자료[순번]=titiqqaq[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){ilili=1;continue;}if(셋째순번=='a'){if(nalunaiqsimavik_atuutilik<끝위치(nalunaiqsimavik_atuutilik))nalunaiqsimavik_atuutilik=다음(nalunaiqsimavik_atuutilik);ilili=1;continue;}
        if(셋째순번=='I'){nalunaiqsimavik_atuutilik=시작(nalunaiqsimavik_atuutilik);ilili=1;continue;}if(셋째순번=='A'){nalunaiqsimavik_atuutilik=끝위치(nalunaiqsimavik_atuutilik);ilili=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char titikutaak_isulittuq='\n';nalunaiqsimavik_atuutilik=셋째순번=='o'?끝위치(nalunaiqsimavik_atuutilik):시작(nalunaiqsimavik_atuutilik);if(덧붙이기(&titikutaak_isulittuq,1)){if(셋째순번=='O')nalunaiqsimavik_atuutilik--;ilili=1;}continue;}
        if(셋째순번=='h'){nalunaiqsimavik_atuutilik=이전항목(nalunaiqsimavik_atuutilik);continue;}if(셋째순번=='l'){nalunaiqsimavik_atuutilik=다음(nalunaiqsimavik_atuutilik);continue;}if(셋째순번=='j'){세로이동(1);continue;}if(셋째순번=='k'){세로이동(-1);continue;}
        if(셋째순번=='0'){nalunaiqsimavik_atuutilik=시작(nalunaiqsimavik_atuutilik);continue;}if(셋째순번=='$'){nalunaiqsimavik_atuutilik=끝위치(nalunaiqsimavik_atuutilik);continue;}if(셋째순번=='G'){nalunaiqsimavik_atuutilik=시작(takininga_atuutilik);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(nalunaiqsimavik_atuutilik<takininga_atuutilik)바이트지우기(nalunaiqsimavik_atuutilik,다음(nalunaiqsimavik_atuutilik));continue;}
        if(셋째순번=='p'&&ijjuarli_takininga){nalunaiqsimavik_atuutilik=끝위치(nalunaiqsimavik_atuutilik);if(nalunaiqsimavik_atuutilik<takininga_atuutilik)nalunaiqsimavik_atuutilik++;덧붙이기(복사자료,ijjuarli_takininga);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=titiqqaq[순번];titiqqaq[순번]=utiqtilli_titiqqat[순번];utiqtilli_titiqqat[순번]=둘째값;}int 개수=takininga_atuutilik;takininga_atuutilik=utiqtilli_takininga;utiqtilli_takininga=개수;개수=nalunaiqsimavik_atuutilik;nalunaiqsimavik_atuutilik=위쪽;위쪽=개수;개수=변경됨;변경됨=되돌림변경;되돌림변경=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=inattijjut(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
