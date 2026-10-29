/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char 글[편집용량],atsataa_atijaaya[편집용량],복사자료[편집용량],결과자료[1024];
static int akaliaa_ajutuu,ee_iyatialujuna_ajutuu,맨위,왼쪽,변경됨,e_itawaa,atsataa_akaliaa,위쪽,되돌림변경,되돌림있음,ashataa_akaliaa,사용량,열수=68,행수=19;
static char 파일이름[64],aluwataaya[128],찾기[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned 대기누름;
static int akaaliijiaa_akotchiraayanüliee,jamakua_iparülein_ayaakuaa,jamakua_iparülein_a_atapajüsüirua;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void waai_atijaaya(unsigned 문자값){if(jamakua_iparülein_ayaakuaa){if((문자값&192)!=128){jamakua_iparülein_a_atapajüsüirua+=문자값>=196?2:1;}if(jamakua_iparülein_a_atapajüsüirua>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=문자값;}
static void 글내보내기(const char *kaleena_atijaaya){while(*kaleena_atijaaya)waai_atijaaya((unsigned char)*kaleena_atijaaya++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)waai_atijaaya(둘째값[--순번]);}
static void 이동(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);waai_atijaaya(';');수치(열위치);waai_atijaaya('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(글[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<akaliaa_ajutuu){자료위치++;while(자료위치<akaliaa_ajutuu&&(글[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int 시작(int 자료위치){while(자료위치>0&&글[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int 끝위치(int 자료위치){while(자료위치<akaliaa_ajutuu&&글[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned 문자값){return 문자값>=196?2:1;}
static int sha_washa_watüsü(int 자료위치){int 문자값=0;for(int 순번=시작(자료위치);순번<자료위치;순번=다음(순번))문자값+=글[순번]=='\t'?4-문자값%4:너비(글[순번]);return 문자값;}
static void aa_inmajio_u(void){for(int 순번=0;순번<akaliaa_ajutuu;순번++)atsataa_atijaaya[순번]=글[순번];atsataa_akaliaa=akaliaa_ajutuu;위쪽=ee_iyatialujuna_ajutuu;되돌림변경=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){aa_inmajio_u();for(int 순번=도착위치;순번<akaliaa_ajutuu;순번++)글[출발위치+순번-도착위치]=글[순번];akaliaa_ajutuu-=도착위치-출발위치;ee_iyatialujuna_ajutuu=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *kaleena_atijaaya,int 개수){if(개수>편집용량-akaliaa_ajutuu){알림문="File full (16384 bytes)";return 0;}aa_inmajio_u();for(int 순번=akaliaa_ajutuu-1;순번>=ee_iyatialujuna_ajutuu;순번--)글[순번+개수]=글[순번];for(int 순번=0;순번<개수;순번++)글[ee_iyatialujuna_ajutuu+순번]=kaleena_atijaaya[순번];akaliaa_ajutuu+=개수;ee_iyatialujuna_ajutuu+=개수;변경됨=1;return 1;}
static void 세로이동(int 차이){int 열위치=sha_washa_watüsü(ee_iyatialujuna_ajutuu),자료위치=시작(ee_iyatialujuna_ajutuu);if(차이<0){if(!자료위치)return;자료위치=시작(자료위치-1);}else{자료위치=끝위치(자료위치);if(자료위치==akaliaa_ajutuu)return;자료위치++;}int 문자값=0;while(자료위치<akaliaa_ajutuu&&글[자료위치]!='\n'&&문자값<열위치){문자값+=글[자료위치]=='\t'?4-문자값%4:너비(글[자료위치]);자료위치=다음(자료위치);}ee_iyatialujuna_ajutuu=자료위치;}
static void 화면그리기(void){
    if(ee_iyatialujuna_ajutuu>akaliaa_ajutuu)ee_iyatialujuna_ajutuu=akaliaa_ajutuu;if(맨위>ee_iyatialujuna_ajutuu)맨위=시작(ee_iyatialujuna_ajutuu);맨위=시작(맨위);
    int 행위치=0;for(int 순번=맨위;순번<ee_iyatialujuna_ajutuu;순번++)if(글[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=끝위치(맨위);if(맨위<akaliaa_ajutuu)맨위++;행위치--;}
    int 열위치=sha_washa_watüsü(ee_iyatialujuna_ajutuu);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        이동(반환값+1,1);글내보내기("\033[0m\033[2K");int 문자값=0,그려진상태=0;
        if(자료위치>=akaliaa_ajutuu&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<akaliaa_ajutuu&&글[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=글[자료위치]=='\t'?4-문자값%4:너비(글[자료위치]);
            if(문자값>=왼쪽&&문자값-왼쪽+너비값<열수){
                if(글[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)waai_atijaaya(' ');}else if(글[자료위치]<32||글[자료위치]==127){waai_atijaaya('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)waai_atijaaya(글[안쪽순번]);그려진상태+=너비값;
            }문자값+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<akaliaa_ajutuu)자료위치++;
    }
    이동(행수,1);글내보내기("\033[7m\033[2K");jamakua_iparülein_ayaakuaa=1;jamakua_iparülein_a_atapajüsüirua=0;글내보내기(e_itawaa?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(파일이름[이름바이트수]&&이름바이트수<30)waai_atijaaya(파일이름[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int liinia=1;for(int 순번=0;순번<ee_iyatialujuna_ajutuu;순번++)if(글[순번]=='\n')liinia++;수치(liinia);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)waai_atijaaya(알림문[개수++]);}
    jamakua_iparülein_ayaakuaa=0;글내보내기("\033[0m");이동(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(대기누름){int 셋째순번=대기누름;대기누름=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned 크기=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(크기&65535)||행수!=(int)(크기>>16)){
            열수=크기&65535;행수=크기>>16;화면그리기();
            if(akaaliijiaa_akotchiraayanüliee){이동(행수,1);글내보내기("\033[0m\033[2K");waai_atijaaya(akaaliijiaa_akotchiraayanüliee);글내보내기(aluwataaya);출력비우기();}
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
static int 저장(void){
    int anaajaalaa_aapaaya=파일열기(파일이름,읽고쓰기|없으면만들기|내용비우기,0600);if(anaajaalaa_aapaaya<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=ashajaa_anaajaalaa_atijaaya(anaajaalaa_aapaaya,글,akaliaa_ajutuu);asürülaa_anaajaalaa(anaajaalaa_aapaaya);if(개수!=akaliaa_ajutuu){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(찾기[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=akaliaa_ajutuu;순번++){int 자료위치=(ee_iyatialujuna_ajutuu+순번)%(akaliaa_ajutuu?akaliaa_ajutuu:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<akaliaa_ajutuu&&글[자료위치+안쪽순번]==(unsigned char)찾기[안쪽순번])안쪽순번++;if(안쪽순번==개수){ee_iyatialujuna_ajutuu=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int a_atapajülü(int akotchiraayanüliee_ajutuu){
    int 개수=0;aluwataaya[0]=0;
    for(;;){이동(행수,1);글내보내기("\033[0m\033[2K");waai_atijaaya(akotchiraayanüliee_ajutuu);글내보내기(aluwataaya);출력비우기();akaaliijiaa_akotchiraayanüliee=akotchiraayanüliee_ajutuu;int 셋째순번=누름값();akaaliijiaa_akotchiraayanüliee=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)aluwataaya[개수]&192)==128)개수--;aluwataaya[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){aluwataaya[개수++]=셋째순번;aluwataaya[개수]=0;}
    }
    if(akotchiraayanüliee_ajutuu=='/'){for(int 순번=0;순번<=개수;순번++)찾기[순번]=aluwataaya[순번];다음찾기();return 0;}
    if(같은지(aluwataaya,"q!"))return 1;
    if(같은지(aluwataaya,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(aluwataaya,"wq")||같은지(aluwataaya,"x"))return 저장();
    if(같은지(aluwataaya,"w")){저장();return 0;}
    if(aluwataaya[0]=='w'&&aluwataaya[1]==' '){int 순번=2;while(aluwataaya[순번]==' ')순번++;int 크기=개수-순번;if(크기<1||크기>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<크기;안쪽순번++)파일이름[안쪽순번]=aluwataaya[순번+안쪽순번];파일이름[크기]=0;저장();return 0;}
    int liinia=0;for(int 순번=0;순번<개수;순번++){if(aluwataaya[순번]<'0'||aluwataaya[순번]>'9'){liinia=0;break;}liinia=liinia*10+aluwataaya[순번]-'0';if(liinia>16384){liinia=0;break;}}
    if(liinia){ee_iyatialujuna_ajutuu=0;while(--liinia&&ee_iyatialujuna_ajutuu<akaliaa_ajutuu){ee_iyatialujuna_ajutuu=끝위치(ee_iyatialujuna_ajutuu);if(ee_iyatialujuna_ajutuu<akaliaa_ajutuu)ee_iyatialujuna_ajutuu++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int achuwalaa_ka_yataayakalü_akumajiaa(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||ka_yataayakalü_ajutuu(0,파일이름,sizeof(파일이름))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int anaajaalaa_aapaaya=파일열기(파일이름,읽기전용,0);
    if(anaajaalaa_aapaaya>=0){int 개수=파일크기(anaajaalaa_aapaaya);if(개수<0||개수>편집용량){asürülaa_anaajaalaa(anaajaalaa_aapaaya);return 1;}akaliaa_ajutuu=파일자료읽기(anaajaalaa_aapaaya,글,개수);asürülaa_anaajaalaa(anaajaalaa_aapaaya);if(akaliaa_ajutuu!=개수)return 1;for(int 순번=0;순번<akaliaa_ajutuu;순번++)if(!글[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){세로이동(-1);continue;}if(셋째순번==1002){세로이동(1);continue;}if(셋째순번==1003){ee_iyatialujuna_ajutuu=다음(ee_iyatialujuna_ajutuu);continue;}if(셋째순번==1004){ee_iyatialujuna_ajutuu=이전항목(ee_iyatialujuna_ajutuu);continue;}
        if(셋째순번==1005){ee_iyatialujuna_ajutuu=시작(ee_iyatialujuna_ajutuu);continue;}if(셋째순번==1006){ee_iyatialujuna_ajutuu=끝위치(ee_iyatialujuna_ajutuu);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)세로이동(셋째순번==1008?-1:1);continue;}
        if(e_itawaa){
            if(셋째순번==27||셋째순번==3){e_itawaa=0;continue;}
            if(셋째순번==127||셋째순번==8){if(ee_iyatialujuna_ajutuu)바이트지우기(이전항목(ee_iyatialujuna_ajutuu),ee_iyatialujuna_ajutuu);continue;}
            if(셋째순번==1007){if(ee_iyatialujuna_ajutuu<akaliaa_ajutuu)바이트지우기(ee_iyatialujuna_ajutuu,다음(ee_iyatialujuna_ajutuu));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int 문자값=누름값();if(문자값<128||문자값>191){대기누름=문자값;유효함=0;break;}둘째값[순번]=문자값;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){ee_iyatialujuna_ajutuu=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=저장();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=시작(ee_iyatialujuna_ajutuu),둘째값=끝위치(ee_iyatialujuna_ajutuu);if(둘째값<akaliaa_ajutuu)둘째값++;ashataa_akaliaa=둘째값-첫째값;for(int 순번=0;순번<ashataa_akaliaa;순번++)복사자료[순번]=글[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){e_itawaa=1;continue;}if(셋째순번=='a'){if(ee_iyatialujuna_ajutuu<끝위치(ee_iyatialujuna_ajutuu))ee_iyatialujuna_ajutuu=다음(ee_iyatialujuna_ajutuu);e_itawaa=1;continue;}
        if(셋째순번=='I'){ee_iyatialujuna_ajutuu=시작(ee_iyatialujuna_ajutuu);e_itawaa=1;continue;}if(셋째순번=='A'){ee_iyatialujuna_ajutuu=끝위치(ee_iyatialujuna_ajutuu);e_itawaa=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char liinia_ajattiraa='\n';ee_iyatialujuna_ajutuu=셋째순번=='o'?끝위치(ee_iyatialujuna_ajutuu):시작(ee_iyatialujuna_ajutuu);if(덧붙이기(&liinia_ajattiraa,1)){if(셋째순번=='O')ee_iyatialujuna_ajutuu--;e_itawaa=1;}continue;}
        if(셋째순번=='h'){ee_iyatialujuna_ajutuu=이전항목(ee_iyatialujuna_ajutuu);continue;}if(셋째순번=='l'){ee_iyatialujuna_ajutuu=다음(ee_iyatialujuna_ajutuu);continue;}if(셋째순번=='j'){세로이동(1);continue;}if(셋째순번=='k'){세로이동(-1);continue;}
        if(셋째순번=='0'){ee_iyatialujuna_ajutuu=시작(ee_iyatialujuna_ajutuu);continue;}if(셋째순번=='$'){ee_iyatialujuna_ajutuu=끝위치(ee_iyatialujuna_ajutuu);continue;}if(셋째순번=='G'){ee_iyatialujuna_ajutuu=시작(akaliaa_ajutuu);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(ee_iyatialujuna_ajutuu<akaliaa_ajutuu)바이트지우기(ee_iyatialujuna_ajutuu,다음(ee_iyatialujuna_ajutuu));continue;}
        if(셋째순번=='p'&&ashataa_akaliaa){ee_iyatialujuna_ajutuu=끝위치(ee_iyatialujuna_ajutuu);if(ee_iyatialujuna_ajutuu<akaliaa_ajutuu)ee_iyatialujuna_ajutuu++;덧붙이기(복사자료,ashataa_akaliaa);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=글[순번];글[순번]=atsataa_atijaaya[순번];atsataa_atijaaya[순번]=둘째값;}int 개수=akaliaa_ajutuu;akaliaa_ajutuu=atsataa_akaliaa;atsataa_akaliaa=개수;개수=ee_iyatialujuna_ajutuu;ee_iyatialujuna_ajutuu=위쪽;위쪽=개수;개수=변경됨;변경됨=되돌림변경;되돌림변경=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=a_atapajülü(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
