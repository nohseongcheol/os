/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char SMS[편집용량],fasayi_Tarin_bayani[편집용량],복사자료[편집용량],결과자료[1024];
static int Tsawo_Daraja,Indes_Daraja,맨위,왼쪽,변경됨,Saka,fasayi_Tsawo,위쪽,fasayi_Canje_canje,되돌림있음,Kwafi_Tsawo,사용량,열수=68,행수=19;
static char Fayil_Mashigar_bayanai_Suna[64],Umarni[128],nema_Mashigar_bayanai[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned mai_jira_Makulli;
static int Taimako_ɓangare,Matsayi_Hoto,Matsayi_Jerin_ayyukan_da_za_a_yi;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void bayit_Tarin_bayani(unsigned Lambar_sirrin_harafi){if(Matsayi_Hoto){if((Lambar_sirrin_harafi&192)!=128){Matsayi_Jerin_ayyukan_da_za_a_yi+=Lambar_sirrin_harafi>=196?2:1;}if(Matsayi_Jerin_ayyukan_da_za_a_yi>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=Lambar_sirrin_harafi;}
static void 글내보내기(const char *Zare_Tarin_bayani){while(*Zare_Tarin_bayani)bayit_Tarin_bayani((unsigned char)*Zare_Tarin_bayani++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)bayit_Tarin_bayani(둘째값[--순번]);}
static void Matsar_da_Daraja(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);bayit_Tarin_bayani(';');수치(열위치);bayit_Tarin_bayani('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(SMS[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<Tsawo_Daraja){자료위치++;while(자료위치<Tsawo_Daraja&&(SMS[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int Tafiyar_da(int 자료위치){while(자료위치>0&&SMS[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int Ƙarshe_Sassautawa(int 자료위치){while(자료위치<Tsawo_Daraja&&SMS[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned Lambar_sirrin_harafi){return Lambar_sirrin_harafi>=196?2:1;}
static int ginshiƙi(int 자료위치){int Lambar_sirrin_harafi=0;for(int 순번=Tafiyar_da(자료위치);순번<자료위치;순번=다음(순번))Lambar_sirrin_harafi+=SMS[순번]=='\t'?4-Lambar_sirrin_harafi%4:너비(SMS[순번]);return Lambar_sirrin_harafi;}
static void Tashar_bincike(void){for(int 순번=0;순번<Tsawo_Daraja;순번++)fasayi_Tarin_bayani[순번]=SMS[순번];fasayi_Tsawo=Tsawo_Daraja;위쪽=Indes_Daraja;fasayi_Canje_canje=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){Tashar_bincike();for(int 순번=도착위치;순번<Tsawo_Daraja;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];Tsawo_Daraja-=도착위치-출발위치;Indes_Daraja=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *Zare_Tarin_bayani,int 개수){if(개수>편집용량-Tsawo_Daraja){알림문="File full (16384 bytes)";return 0;}Tashar_bincike();for(int 순번=Tsawo_Daraja-1;순번>=Indes_Daraja;순번--)SMS[순번+개수]=SMS[순번];for(int 순번=0;순번<개수;순번++)SMS[Indes_Daraja+순번]=Zare_Tarin_bayani[순번];Tsawo_Daraja+=개수;Indes_Daraja+=개수;변경됨=1;return 1;}
static void Tsaye(int 차이){int 열위치=ginshiƙi(Indes_Daraja),자료위치=Tafiyar_da(Indes_Daraja);if(차이<0){if(!자료위치)return;자료위치=Tafiyar_da(자료위치-1);}else{자료위치=Ƙarshe_Sassautawa(자료위치);if(자료위치==Tsawo_Daraja)return;자료위치++;}int Lambar_sirrin_harafi=0;while(자료위치<Tsawo_Daraja&&SMS[자료위치]!='\n'&&Lambar_sirrin_harafi<열위치){Lambar_sirrin_harafi+=SMS[자료위치]=='\t'?4-Lambar_sirrin_harafi%4:너비(SMS[자료위치]);자료위치=다음(자료위치);}Indes_Daraja=자료위치;}
static void 화면그리기(void){
    if(Indes_Daraja>Tsawo_Daraja)Indes_Daraja=Tsawo_Daraja;if(맨위>Indes_Daraja)맨위=Tafiyar_da(Indes_Daraja);맨위=Tafiyar_da(맨위);
    int 행위치=0;for(int 순번=맨위;순번<Indes_Daraja;순번++)if(SMS[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=Ƙarshe_Sassautawa(맨위);if(맨위<Tsawo_Daraja)맨위++;행위치--;}
    int 열위치=ginshiƙi(Indes_Daraja);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        Matsar_da_Daraja(반환값+1,1);글내보내기("\033[0m\033[2K");int Lambar_sirrin_harafi=0,그려진상태=0;
        if(자료위치>=Tsawo_Daraja&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<Tsawo_Daraja&&SMS[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=SMS[자료위치]=='\t'?4-Lambar_sirrin_harafi%4:너비(SMS[자료위치]);
            if(Lambar_sirrin_harafi>=왼쪽&&Lambar_sirrin_harafi-왼쪽+너비값<열수){
                if(SMS[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bayit_Tarin_bayani(' ');}else if(SMS[자료위치]<32||SMS[자료위치]==127){bayit_Tarin_bayani('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)bayit_Tarin_bayani(SMS[안쪽순번]);그려진상태+=너비값;
            }Lambar_sirrin_harafi+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<Tsawo_Daraja)자료위치++;
    }
    Matsar_da_Daraja(행수,1);글내보내기("\033[7m\033[2K");Matsayi_Hoto=1;Matsayi_Jerin_ayyukan_da_za_a_yi=0;글내보내기(Saka?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Fayil_Mashigar_bayanai_Suna[이름바이트수]&&이름바이트수<30)bayit_Tarin_bayani(Fayil_Mashigar_bayanai_Suna[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Layi=1;for(int 순번=0;순번<Indes_Daraja;순번++)if(SMS[순번]=='\n')Layi++;수치(Layi);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)bayit_Tarin_bayani(알림문[개수++]);}
    Matsayi_Hoto=0;글내보내기("\033[0m");Matsar_da_Daraja(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(mai_jira_Makulli){int 셋째순번=mai_jira_Makulli;mai_jira_Makulli=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Girma=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(Girma&65535)||행수!=(int)(Girma>>16)){
            열수=Girma&65535;행수=Girma>>16;화면그리기();
            if(Taimako_ɓangare){Matsar_da_Daraja(행수,1);글내보내기("\033[0m\033[2K");bayit_Tarin_bayani(Taimako_ɓangare);글내보내기(Umarni);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){mai_jira_Makulli=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int Ajiye_Daraja(void){
    int Fayil_Mariki=buɗe_Fayil(Fayil_Mashigar_bayanai_Suna,Rubutuwa_karantuwa|없으면만들기|내용비우기,0600);if(Fayil_Mariki<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=Rubuta_Fayil_Tarin_bayani(Fayil_Mariki,SMS,Tsawo_Daraja);Rufe_Fayil(Fayil_Mariki);if(개수!=Tsawo_Daraja){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(nema_Mashigar_bayanai[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=Tsawo_Daraja;순번++){int 자료위치=(Indes_Daraja+순번)%(Tsawo_Daraja?Tsawo_Daraja:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<Tsawo_Daraja&&SMS[자료위치+안쪽순번]==(unsigned char)nema_Mashigar_bayanai[안쪽순번])안쪽순번++;if(안쪽순번==개수){Indes_Daraja=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int promt(int ɓangare_Daraja){
    int 개수=0;Umarni[0]=0;
    for(;;){Matsar_da_Daraja(행수,1);글내보내기("\033[0m\033[2K");bayit_Tarin_bayani(ɓangare_Daraja);글내보내기(Umarni);출력비우기();Taimako_ɓangare=ɓangare_Daraja;int 셋째순번=누름값();Taimako_ɓangare=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)Umarni[개수]&192)==128)개수--;Umarni[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){Umarni[개수++]=셋째순번;Umarni[개수]=0;}
    }
    if(ɓangare_Daraja=='/'){for(int 순번=0;순번<=개수;순번++)nema_Mashigar_bayanai[순번]=Umarni[순번];다음찾기();return 0;}
    if(같은지(Umarni,"q!"))return 1;
    if(같은지(Umarni,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Umarni,"wq")||같은지(Umarni,"x"))return Ajiye_Daraja();
    if(같은지(Umarni,"w")){Ajiye_Daraja();return 0;}
    if(Umarni[0]=='w'&&Umarni[1]==' '){int 순번=2;while(Umarni[순번]==' ')순번++;int Girma=개수-순번;if(Girma<1||Girma>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Girma;안쪽순번++)Fayil_Mashigar_bayanai_Suna[안쪽순번]=Umarni[순번+안쪽순번];Fayil_Mashigar_bayanai_Suna[Girma]=0;Ajiye_Daraja();return 0;}
    int Layi=0;for(int 순번=0;순번<개수;순번++){if(Umarni[순번]<'0'||Umarni[순번]>'9'){Layi=0;break;}Layi=Layi*10+Umarni[순번]-'0';if(Layi>16384){Layi=0;break;}}
    if(Layi){Indes_Daraja=0;while(--Layi&&Indes_Daraja<Tsawo_Daraja){Indes_Daraja=Ƙarshe_Sassautawa(Indes_Daraja);if(Indes_Daraja<Tsawo_Daraja)Indes_Daraja++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Fara_Mai_anfani_da_kwamfuta_Shiri(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||Mai_anfani_da_kwamfuta_Tubalin_aiki(0,Fayil_Mashigar_bayanai_Suna,sizeof(Fayil_Mashigar_bayanai_Suna))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Fayil_Mariki=buɗe_Fayil(Fayil_Mashigar_bayanai_Suna,karanta_kawai_Daraja,0);
    if(Fayil_Mariki>=0){int 개수=Fayil_girma(Fayil_Mariki);if(개수<0||개수>편집용량){Rufe_Fayil(Fayil_Mariki);return 1;}Tsawo_Daraja=파일자료읽기(Fayil_Mariki,SMS,개수);Rufe_Fayil(Fayil_Mariki);if(Tsawo_Daraja!=개수)return 1;for(int 순번=0;순번<Tsawo_Daraja;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Tsaye(-1);continue;}if(셋째순번==1002){Tsaye(1);continue;}if(셋째순번==1003){Indes_Daraja=다음(Indes_Daraja);continue;}if(셋째순번==1004){Indes_Daraja=이전항목(Indes_Daraja);continue;}
        if(셋째순번==1005){Indes_Daraja=Tafiyar_da(Indes_Daraja);continue;}if(셋째순번==1006){Indes_Daraja=Ƙarshe_Sassautawa(Indes_Daraja);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)Tsaye(셋째순번==1008?-1:1);continue;}
        if(Saka){
            if(셋째순번==27||셋째순번==3){Saka=0;continue;}
            if(셋째순번==127||셋째순번==8){if(Indes_Daraja)바이트지우기(이전항목(Indes_Daraja),Indes_Daraja);continue;}
            if(셋째순번==1007){if(Indes_Daraja<Tsawo_Daraja)바이트지우기(Indes_Daraja,다음(Indes_Daraja));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int Lambar_sirrin_harafi=누름값();if(Lambar_sirrin_harafi<128||Lambar_sirrin_harafi>191){mai_jira_Makulli=Lambar_sirrin_harafi;유효함=0;break;}둘째값[순번]=Lambar_sirrin_harafi;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){Indes_Daraja=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=Ajiye_Daraja();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=Tafiyar_da(Indes_Daraja),둘째값=Ƙarshe_Sassautawa(Indes_Daraja);if(둘째값<Tsawo_Daraja)둘째값++;Kwafi_Tsawo=둘째값-첫째값;for(int 순번=0;순번<Kwafi_Tsawo;순번++)복사자료[순번]=SMS[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){Saka=1;continue;}if(셋째순번=='a'){if(Indes_Daraja<Ƙarshe_Sassautawa(Indes_Daraja))Indes_Daraja=다음(Indes_Daraja);Saka=1;continue;}
        if(셋째순번=='I'){Indes_Daraja=Tafiyar_da(Indes_Daraja);Saka=1;continue;}if(셋째순번=='A'){Indes_Daraja=Ƙarshe_Sassautawa(Indes_Daraja);Saka=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char Layi_Ƙarshe='\n';Indes_Daraja=셋째순번=='o'?Ƙarshe_Sassautawa(Indes_Daraja):Tafiyar_da(Indes_Daraja);if(덧붙이기(&Layi_Ƙarshe,1)){if(셋째순번=='O')Indes_Daraja--;Saka=1;}continue;}
        if(셋째순번=='h'){Indes_Daraja=이전항목(Indes_Daraja);continue;}if(셋째순번=='l'){Indes_Daraja=다음(Indes_Daraja);continue;}if(셋째순번=='j'){Tsaye(1);continue;}if(셋째순번=='k'){Tsaye(-1);continue;}
        if(셋째순번=='0'){Indes_Daraja=Tafiyar_da(Indes_Daraja);continue;}if(셋째순번=='$'){Indes_Daraja=Ƙarshe_Sassautawa(Indes_Daraja);continue;}if(셋째순번=='G'){Indes_Daraja=Tafiyar_da(Tsawo_Daraja);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(Indes_Daraja<Tsawo_Daraja)바이트지우기(Indes_Daraja,다음(Indes_Daraja));continue;}
        if(셋째순번=='p'&&Kwafi_Tsawo){Indes_Daraja=Ƙarshe_Sassautawa(Indes_Daraja);if(Indes_Daraja<Tsawo_Daraja)Indes_Daraja++;덧붙이기(복사자료,Kwafi_Tsawo);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=SMS[순번];SMS[순번]=fasayi_Tarin_bayani[순번];fasayi_Tarin_bayani[순번]=둘째값;}int 개수=Tsawo_Daraja;Tsawo_Daraja=fasayi_Tsawo;fasayi_Tsawo=개수;개수=Indes_Daraja;Indes_Daraja=위쪽;위쪽=개수;개수=변경됨;변경됨=fasayi_Canje_canje;fasayi_Canje_canje=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=promt(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
