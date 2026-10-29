/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char SMS[편집용량],dirolola_tshedimosetso[편집용량],복사자료[편집용량],결과자료[1024];
static int boleele_Boleng,tshupane_Boleng,맨위,왼쪽,변경됨,tsenya_8e07c86f,dirolola_boleele,위쪽,dirolola_Diphetogo,되돌림있음,leloko_boleele,사용량,열수=68,행수=19;
static char faele_tsenyo_leina[64],Taelo[128],batla_tsenyo[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned sa_letile_taetsi;
static int thuso_setlhopha,kemo_Setshwantsho,kemo_diletakgatiso;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void baete_tshedimosetso(unsigned khoutuletshwao){if(kemo_Setshwantsho){if((khoutuletshwao&192)!=128){kemo_diletakgatiso+=khoutuletshwao>=196?2:1;}if(kemo_diletakgatiso>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=khoutuletshwao;}
static void 글내보내기(const char *dikwalwa_tshedimosetso){while(*dikwalwa_tshedimosetso)baete_tshedimosetso((unsigned char)*dikwalwa_tshedimosetso++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)baete_tshedimosetso(둘째값[--순번]);}
static void sutisa_Boleng(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);baete_tshedimosetso(';');수치(열위치);baete_tshedimosetso('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(SMS[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<boleele_Boleng){자료위치++;while(자료위치<boleele_Boleng&&(SMS[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int dirisa(int 자료위치){while(자료위치>0&&SMS[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int kgaola_Baya_ka_Tekatekanyo(int 자료위치){while(자료위치<boleele_Boleng&&SMS[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned khoutuletshwao){return khoutuletshwao>=196?2:1;}
static int Kholomo(int 자료위치){int khoutuletshwao=0;for(int 순번=dirisa(자료위치);순번<자료위치;순번=다음(순번))khoutuletshwao+=SMS[순번]=='\t'?4-khoutuletshwao%4:너비(SMS[순번]);return khoutuletshwao;}
static void lefelotlholo(void){for(int 순번=0;순번<boleele_Boleng;순번++)dirolola_tshedimosetso[순번]=SMS[순번];dirolola_boleele=boleele_Boleng;위쪽=tshupane_Boleng;dirolola_Diphetogo=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){lefelotlholo();for(int 순번=도착위치;순번<boleele_Boleng;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];boleele_Boleng-=도착위치-출발위치;tshupane_Boleng=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *dikwalwa_tshedimosetso,int 개수){if(개수>편집용량-boleele_Boleng){알림문="File full (16384 bytes)";return 0;}lefelotlholo();for(int 순번=boleele_Boleng-1;순번>=tshupane_Boleng;순번--)SMS[순번+개수]=SMS[순번];for(int 순번=0;순번<개수;순번++)SMS[tshupane_Boleng+순번]=dikwalwa_tshedimosetso[순번];boleele_Boleng+=개수;tshupane_Boleng+=개수;변경됨=1;return 1;}
static void Tsepamo_3b2f88eb(int 차이){int 열위치=Kholomo(tshupane_Boleng),자료위치=dirisa(tshupane_Boleng);if(차이<0){if(!자료위치)return;자료위치=dirisa(자료위치-1);}else{자료위치=kgaola_Baya_ka_Tekatekanyo(자료위치);if(자료위치==boleele_Boleng)return;자료위치++;}int khoutuletshwao=0;while(자료위치<boleele_Boleng&&SMS[자료위치]!='\n'&&khoutuletshwao<열위치){khoutuletshwao+=SMS[자료위치]=='\t'?4-khoutuletshwao%4:너비(SMS[자료위치]);자료위치=다음(자료위치);}tshupane_Boleng=자료위치;}
static void 화면그리기(void){
    if(tshupane_Boleng>boleele_Boleng)tshupane_Boleng=boleele_Boleng;if(맨위>tshupane_Boleng)맨위=dirisa(tshupane_Boleng);맨위=dirisa(맨위);
    int 행위치=0;for(int 순번=맨위;순번<tshupane_Boleng;순번++)if(SMS[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=kgaola_Baya_ka_Tekatekanyo(맨위);if(맨위<boleele_Boleng)맨위++;행위치--;}
    int 열위치=Kholomo(tshupane_Boleng);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        sutisa_Boleng(반환값+1,1);글내보내기("\033[0m\033[2K");int khoutuletshwao=0,그려진상태=0;
        if(자료위치>=boleele_Boleng&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<boleele_Boleng&&SMS[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=SMS[자료위치]=='\t'?4-khoutuletshwao%4:너비(SMS[자료위치]);
            if(khoutuletshwao>=왼쪽&&khoutuletshwao-왼쪽+너비값<열수){
                if(SMS[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)baete_tshedimosetso(' ');}else if(SMS[자료위치]<32||SMS[자료위치]==127){baete_tshedimosetso('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)baete_tshedimosetso(SMS[안쪽순번]);그려진상태+=너비값;
            }khoutuletshwao+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<boleele_Boleng)자료위치++;
    }
    sutisa_Boleng(행수,1);글내보내기("\033[7m\033[2K");kemo_Setshwantsho=1;kemo_diletakgatiso=0;글내보내기(tsenya_8e07c86f?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(faele_tsenyo_leina[이름바이트수]&&이름바이트수<30)baete_tshedimosetso(faele_tsenyo_leina[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Mola=1;for(int 순번=0;순번<tshupane_Boleng;순번++)if(SMS[순번]=='\n')Mola++;수치(Mola);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)baete_tshedimosetso(알림문[개수++]);}
    kemo_Setshwantsho=0;글내보내기("\033[0m");sutisa_Boleng(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(sa_letile_taetsi){int 셋째순번=sa_letile_taetsi;sa_letile_taetsi=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned lekanya=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(lekanya&65535)||행수!=(int)(lekanya>>16)){
            열수=lekanya&65535;행수=lekanya>>16;화면그리기();
            if(thuso_setlhopha){sutisa_Boleng(행수,1);글내보내기("\033[0m\033[2K");baete_tshedimosetso(thuso_setlhopha);글내보내기(Taelo);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){sa_letile_taetsi=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int Store_Boleng(void){
    int faele_mokgwakamogelo=bula_faele(faele_tsenyo_leina,buisa_kwala|없으면만들기|내용비우기,0600);if(faele_mokgwakamogelo<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=kwala_faele_tshedimosetso(faele_mokgwakamogelo,SMS,boleele_Boleng);tswala_faele(faele_mokgwakamogelo);if(개수!=boleele_Boleng){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(batla_tsenyo[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=boleele_Boleng;순번++){int 자료위치=(tshupane_Boleng+순번)%(boleele_Boleng?boleele_Boleng:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<boleele_Boleng&&SMS[자료위치+안쪽순번]==(unsigned char)batla_tsenyo[안쪽순번])안쪽순번++;if(안쪽순번==개수){tshupane_Boleng=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int kgwetlho(int setlhopha_Boleng_4b6d6445){
    int 개수=0;Taelo[0]=0;
    for(;;){sutisa_Boleng(행수,1);글내보내기("\033[0m\033[2K");baete_tshedimosetso(setlhopha_Boleng_4b6d6445);글내보내기(Taelo);출력비우기();thuso_setlhopha=setlhopha_Boleng_4b6d6445;int 셋째순번=누름값();thuso_setlhopha=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)Taelo[개수]&192)==128)개수--;Taelo[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){Taelo[개수++]=셋째순번;Taelo[개수]=0;}
    }
    if(setlhopha_Boleng_4b6d6445=='/'){for(int 순번=0;순번<=개수;순번++)batla_tsenyo[순번]=Taelo[순번];다음찾기();return 0;}
    if(같은지(Taelo,"q!"))return 1;
    if(같은지(Taelo,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Taelo,"wq")||같은지(Taelo,"x"))return Store_Boleng();
    if(같은지(Taelo,"w")){Store_Boleng();return 0;}
    if(Taelo[0]=='w'&&Taelo[1]==' '){int 순번=2;while(Taelo[순번]==' ')순번++;int lekanya=개수-순번;if(lekanya<1||lekanya>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<lekanya;안쪽순번++)faele_tsenyo_leina[안쪽순번]=Taelo[순번+안쪽순번];faele_tsenyo_leina[lekanya]=0;Store_Boleng();return 0;}
    int Mola=0;for(int 순번=0;순번<개수;순번++){if(Taelo[순번]<'0'||Taelo[순번]>'9'){Mola=0;break;}Mola=Mola*10+Taelo[순번]-'0';if(Mola>16384){Mola=0;break;}}
    if(Mola){tshupane_Boleng=0;while(--Mola&&tshupane_Boleng<boleele_Boleng){tshupane_Boleng=kgaola_Baya_ka_Tekatekanyo(tshupane_Boleng);if(tshupane_Boleng<boleele_Boleng)tshupane_Boleng++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int simolola_modirisi_Tiriso(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||modirisi_Thulaganyo(0,faele_tsenyo_leina,sizeof(faele_tsenyo_leina))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int faele_mokgwakamogelo=bula_faele(faele_tsenyo_leina,puiso_fela_Boleng,0);
    if(faele_mokgwakamogelo>=0){int 개수=faele_lekanya(faele_mokgwakamogelo);if(개수<0||개수>편집용량){tswala_faele(faele_mokgwakamogelo);return 1;}boleele_Boleng=파일자료읽기(faele_mokgwakamogelo,SMS,개수);tswala_faele(faele_mokgwakamogelo);if(boleele_Boleng!=개수)return 1;for(int 순번=0;순번<boleele_Boleng;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Tsepamo_3b2f88eb(-1);continue;}if(셋째순번==1002){Tsepamo_3b2f88eb(1);continue;}if(셋째순번==1003){tshupane_Boleng=다음(tshupane_Boleng);continue;}if(셋째순번==1004){tshupane_Boleng=이전항목(tshupane_Boleng);continue;}
        if(셋째순번==1005){tshupane_Boleng=dirisa(tshupane_Boleng);continue;}if(셋째순번==1006){tshupane_Boleng=kgaola_Baya_ka_Tekatekanyo(tshupane_Boleng);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)Tsepamo_3b2f88eb(셋째순번==1008?-1:1);continue;}
        if(tsenya_8e07c86f){
            if(셋째순번==27||셋째순번==3){tsenya_8e07c86f=0;continue;}
            if(셋째순번==127||셋째순번==8){if(tshupane_Boleng)바이트지우기(이전항목(tshupane_Boleng),tshupane_Boleng);continue;}
            if(셋째순번==1007){if(tshupane_Boleng<boleele_Boleng)바이트지우기(tshupane_Boleng,다음(tshupane_Boleng));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int khoutuletshwao=누름값();if(khoutuletshwao<128||khoutuletshwao>191){sa_letile_taetsi=khoutuletshwao;유효함=0;break;}둘째값[순번]=khoutuletshwao;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){tshupane_Boleng=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=Store_Boleng();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=dirisa(tshupane_Boleng),둘째값=kgaola_Baya_ka_Tekatekanyo(tshupane_Boleng);if(둘째값<boleele_Boleng)둘째값++;leloko_boleele=둘째값-첫째값;for(int 순번=0;순번<leloko_boleele;순번++)복사자료[순번]=SMS[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){tsenya_8e07c86f=1;continue;}if(셋째순번=='a'){if(tshupane_Boleng<kgaola_Baya_ka_Tekatekanyo(tshupane_Boleng))tshupane_Boleng=다음(tshupane_Boleng);tsenya_8e07c86f=1;continue;}
        if(셋째순번=='I'){tshupane_Boleng=dirisa(tshupane_Boleng);tsenya_8e07c86f=1;continue;}if(셋째순번=='A'){tshupane_Boleng=kgaola_Baya_ka_Tekatekanyo(tshupane_Boleng);tsenya_8e07c86f=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char Mola_kgaola='\n';tshupane_Boleng=셋째순번=='o'?kgaola_Baya_ka_Tekatekanyo(tshupane_Boleng):dirisa(tshupane_Boleng);if(덧붙이기(&Mola_kgaola,1)){if(셋째순번=='O')tshupane_Boleng--;tsenya_8e07c86f=1;}continue;}
        if(셋째순번=='h'){tshupane_Boleng=이전항목(tshupane_Boleng);continue;}if(셋째순번=='l'){tshupane_Boleng=다음(tshupane_Boleng);continue;}if(셋째순번=='j'){Tsepamo_3b2f88eb(1);continue;}if(셋째순번=='k'){Tsepamo_3b2f88eb(-1);continue;}
        if(셋째순번=='0'){tshupane_Boleng=dirisa(tshupane_Boleng);continue;}if(셋째순번=='$'){tshupane_Boleng=kgaola_Baya_ka_Tekatekanyo(tshupane_Boleng);continue;}if(셋째순번=='G'){tshupane_Boleng=dirisa(boleele_Boleng);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(tshupane_Boleng<boleele_Boleng)바이트지우기(tshupane_Boleng,다음(tshupane_Boleng));continue;}
        if(셋째순번=='p'&&leloko_boleele){tshupane_Boleng=kgaola_Baya_ka_Tekatekanyo(tshupane_Boleng);if(tshupane_Boleng<boleele_Boleng)tshupane_Boleng++;덧붙이기(복사자료,leloko_boleele);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=SMS[순번];SMS[순번]=dirolola_tshedimosetso[순번];dirolola_tshedimosetso[순번]=둘째값;}int 개수=boleele_Boleng;boleele_Boleng=dirolola_boleele;dirolola_boleele=개수;개수=tshupane_Boleng;tshupane_Boleng=위쪽;위쪽=개수;개수=변경됨;변경됨=dirolola_Diphetogo;dirolola_Diphetogo=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=kgwetlho(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
