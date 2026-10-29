/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Itekisi[편집용량],yekisa_imininingwane[편집용량],복사자료[편집용량],결과자료[1024];
static int ubude_inani,thola_inkomba_inani,맨위,왼쪽,변경됨,faka_8e07c86f,yekisa_ubude,위쪽,yekisa_Izinguquko,되돌림있음,kopisha_ubude,사용량,열수=68,행수=19;
static char ifayela_okufakwayo_igama[64],Umlayelo[128],thola_okufakwayo[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned kulindile_inkomba;
static int usizo_umunxa,isimo_isithombe,isimo_ujenge;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void ibhayithi_imininingwane(unsigned ikhodi_yohlamvu){if(isimo_isithombe){if((ikhodi_yohlamvu&192)!=128){isimo_ujenge+=ikhodi_yohlamvu>=196?2:1;}if(isimo_ujenge>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=ikhodi_yohlamvu;}
static void 글내보내기(const char *uchunge_imininingwane){while(*uchunge_imininingwane)ibhayithi_imininingwane((unsigned char)*uchunge_imininingwane++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)ibhayithi_imininingwane(둘째값[--순번]);}
static void susa_inani(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);ibhayithi_imininingwane(';');수치(열위치);ibhayithi_imininingwane('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(Itekisi[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<ubude_inani){자료위치++;while(자료위치<ubude_inani&&(Itekisi[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int Sebenzisa(int 자료위치){while(자료위치>0&&Itekisi[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int yekisa_I_ofisethi(int 자료위치){while(자료위치<ubude_inani&&Itekisi[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned ikhodi_yohlamvu){return ikhodi_yohlamvu>=196?2:1;}
static int ikholomu(int 자료위치){int ikhodi_yohlamvu=0;for(int 순번=Sebenzisa(자료위치);순번<자료위치;순번=다음(순번))ikhodi_yohlamvu+=Itekisi[순번]=='\t'?4-ikhodi_yohlamvu%4:너비(Itekisi[순번]);return ikhodi_yohlamvu;}
static void indawo_yokuhlola(void){for(int 순번=0;순번<ubude_inani;순번++)yekisa_imininingwane[순번]=Itekisi[순번];yekisa_ubude=ubude_inani;위쪽=thola_inkomba_inani;yekisa_Izinguquko=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){indawo_yokuhlola();for(int 순번=도착위치;순번<ubude_inani;순번++)Itekisi[출발위치+순번-도착위치]=Itekisi[순번];ubude_inani-=도착위치-출발위치;thola_inkomba_inani=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *uchunge_imininingwane,int 개수){if(개수>편집용량-ubude_inani){알림문="File full (16384 bytes)";return 0;}indawo_yokuhlola();for(int 순번=ubude_inani-1;순번>=thola_inkomba_inani;순번--)Itekisi[순번+개수]=Itekisi[순번];for(int 순번=0;순번<개수;순번++)Itekisi[thola_inkomba_inani+순번]=uchunge_imininingwane[순번];ubude_inani+=개수;thola_inkomba_inani+=개수;변경됨=1;return 1;}
static void Okuqondile(int 차이){int 열위치=ikholomu(thola_inkomba_inani),자료위치=Sebenzisa(thola_inkomba_inani);if(차이<0){if(!자료위치)return;자료위치=Sebenzisa(자료위치-1);}else{자료위치=yekisa_I_ofisethi(자료위치);if(자료위치==ubude_inani)return;자료위치++;}int ikhodi_yohlamvu=0;while(자료위치<ubude_inani&&Itekisi[자료위치]!='\n'&&ikhodi_yohlamvu<열위치){ikhodi_yohlamvu+=Itekisi[자료위치]=='\t'?4-ikhodi_yohlamvu%4:너비(Itekisi[자료위치]);자료위치=다음(자료위치);}thola_inkomba_inani=자료위치;}
static void 화면그리기(void){
    if(thola_inkomba_inani>ubude_inani)thola_inkomba_inani=ubude_inani;if(맨위>thola_inkomba_inani)맨위=Sebenzisa(thola_inkomba_inani);맨위=Sebenzisa(맨위);
    int 행위치=0;for(int 순번=맨위;순번<thola_inkomba_inani;순번++)if(Itekisi[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=yekisa_I_ofisethi(맨위);if(맨위<ubude_inani)맨위++;행위치--;}
    int 열위치=ikholomu(thola_inkomba_inani);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        susa_inani(반환값+1,1);글내보내기("\033[0m\033[2K");int ikhodi_yohlamvu=0,그려진상태=0;
        if(자료위치>=ubude_inani&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<ubude_inani&&Itekisi[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=Itekisi[자료위치]=='\t'?4-ikhodi_yohlamvu%4:너비(Itekisi[자료위치]);
            if(ikhodi_yohlamvu>=왼쪽&&ikhodi_yohlamvu-왼쪽+너비값<열수){
                if(Itekisi[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)ibhayithi_imininingwane(' ');}else if(Itekisi[자료위치]<32||Itekisi[자료위치]==127){ibhayithi_imininingwane('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)ibhayithi_imininingwane(Itekisi[안쪽순번]);그려진상태+=너비값;
            }ikhodi_yohlamvu+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<ubude_inani)자료위치++;
    }
    susa_inani(행수,1);글내보내기("\033[7m\033[2K");isimo_isithombe=1;isimo_ujenge=0;글내보내기(faka_8e07c86f?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(ifayela_okufakwayo_igama[이름바이트수]&&이름바이트수<30)ibhayithi_imininingwane(ifayela_okufakwayo_igama[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int umugqa=1;for(int 순번=0;순번<thola_inkomba_inani;순번++)if(Itekisi[순번]=='\n')umugqa++;수치(umugqa);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)ibhayithi_imininingwane(알림문[개수++]);}
    isimo_isithombe=0;글내보내기("\033[0m");susa_inani(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(kulindile_inkomba){int 셋째순번=kulindile_inkomba;kulindile_inkomba=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Ubungako=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(Ubungako&65535)||행수!=(int)(Ubungako>>16)){
            열수=Ubungako&65535;행수=Ubungako>>16;화면그리기();
            if(usizo_umunxa){susa_inani(행수,1);글내보내기("\033[0m\033[2K");ibhayithi_imininingwane(usizo_umunxa);글내보내기(Umlayelo);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){kulindile_inkomba=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int Store_inani(void){
    int ifayela_isibambo=vula_ifayela(ifayela_okufakwayo_igama,fundeka_bhaleka|없으면만들기|내용비우기,0600);if(ifayela_isibambo<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=bhala_ifayela_imininingwane(ifayela_isibambo,Itekisi,ubude_inani);vala_ifayela(ifayela_isibambo);if(개수!=ubude_inani){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(thola_okufakwayo[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=ubude_inani;순번++){int 자료위치=(thola_inkomba_inani+순번)%(ubude_inani?ubude_inani:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<ubude_inani&&Itekisi[자료위치+안쪽순번]==(unsigned char)thola_okufakwayo[안쪽순번])안쪽순번++;if(안쪽순번==개수){thola_inkomba_inani=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int ozokusebenzisa(int umunxa_inani){
    int 개수=0;Umlayelo[0]=0;
    for(;;){susa_inani(행수,1);글내보내기("\033[0m\033[2K");ibhayithi_imininingwane(umunxa_inani);글내보내기(Umlayelo);출력비우기();usizo_umunxa=umunxa_inani;int 셋째순번=누름값();usizo_umunxa=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)Umlayelo[개수]&192)==128)개수--;Umlayelo[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){Umlayelo[개수++]=셋째순번;Umlayelo[개수]=0;}
    }
    if(umunxa_inani=='/'){for(int 순번=0;순번<=개수;순번++)thola_okufakwayo[순번]=Umlayelo[순번];다음찾기();return 0;}
    if(같은지(Umlayelo,"q!"))return 1;
    if(같은지(Umlayelo,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Umlayelo,"wq")||같은지(Umlayelo,"x"))return Store_inani();
    if(같은지(Umlayelo,"w")){Store_inani();return 0;}
    if(Umlayelo[0]=='w'&&Umlayelo[1]==' '){int 순번=2;while(Umlayelo[순번]==' ')순번++;int Ubungako=개수-순번;if(Ubungako<1||Ubungako>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Ubungako;안쪽순번++)ifayela_okufakwayo_igama[안쪽순번]=Umlayelo[순번+안쪽순번];ifayela_okufakwayo_igama[Ubungako]=0;Store_inani();return 0;}
    int umugqa=0;for(int 순번=0;순번<개수;순번++){if(Umlayelo[순번]<'0'||Umlayelo[순번]>'9'){umugqa=0;break;}umugqa=umugqa*10+Umlayelo[순번]-'0';if(umugqa>16384){umugqa=0;break;}}
    if(umugqa){thola_inkomba_inani=0;while(--umugqa&&thola_inkomba_inani<ubude_inani){thola_inkomba_inani=yekisa_I_ofisethi(thola_inkomba_inani);if(thola_inkomba_inani<ubude_inani)thola_inkomba_inani++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int qala_umsebenzisi_i_app(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||umsebenzisi_i_agumenti(0,ifayela_okufakwayo_igama,sizeof(ifayela_okufakwayo_igama))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int ifayela_isibambo=vula_ifayela(ifayela_okufakwayo_igama,fundwayo_kuphela_inani,0);
    if(ifayela_isibambo>=0){int 개수=ifayela_linganisa(ifayela_isibambo);if(개수<0||개수>편집용량){vala_ifayela(ifayela_isibambo);return 1;}ubude_inani=파일자료읽기(ifayela_isibambo,Itekisi,개수);vala_ifayela(ifayela_isibambo);if(ubude_inani!=개수)return 1;for(int 순번=0;순번<ubude_inani;순번++)if(!Itekisi[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Okuqondile(-1);continue;}if(셋째순번==1002){Okuqondile(1);continue;}if(셋째순번==1003){thola_inkomba_inani=다음(thola_inkomba_inani);continue;}if(셋째순번==1004){thola_inkomba_inani=이전항목(thola_inkomba_inani);continue;}
        if(셋째순번==1005){thola_inkomba_inani=Sebenzisa(thola_inkomba_inani);continue;}if(셋째순번==1006){thola_inkomba_inani=yekisa_I_ofisethi(thola_inkomba_inani);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)Okuqondile(셋째순번==1008?-1:1);continue;}
        if(faka_8e07c86f){
            if(셋째순번==27||셋째순번==3){faka_8e07c86f=0;continue;}
            if(셋째순번==127||셋째순번==8){if(thola_inkomba_inani)바이트지우기(이전항목(thola_inkomba_inani),thola_inkomba_inani);continue;}
            if(셋째순번==1007){if(thola_inkomba_inani<ubude_inani)바이트지우기(thola_inkomba_inani,다음(thola_inkomba_inani));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int ikhodi_yohlamvu=누름값();if(ikhodi_yohlamvu<128||ikhodi_yohlamvu>191){kulindile_inkomba=ikhodi_yohlamvu;유효함=0;break;}둘째값[순번]=ikhodi_yohlamvu;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){thola_inkomba_inani=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=Store_inani();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=Sebenzisa(thola_inkomba_inani),둘째값=yekisa_I_ofisethi(thola_inkomba_inani);if(둘째값<ubude_inani)둘째값++;kopisha_ubude=둘째값-첫째값;for(int 순번=0;순번<kopisha_ubude;순번++)복사자료[순번]=Itekisi[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){faka_8e07c86f=1;continue;}if(셋째순번=='a'){if(thola_inkomba_inani<yekisa_I_ofisethi(thola_inkomba_inani))thola_inkomba_inani=다음(thola_inkomba_inani);faka_8e07c86f=1;continue;}
        if(셋째순번=='I'){thola_inkomba_inani=Sebenzisa(thola_inkomba_inani);faka_8e07c86f=1;continue;}if(셋째순번=='A'){thola_inkomba_inani=yekisa_I_ofisethi(thola_inkomba_inani);faka_8e07c86f=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char umugqa_yekisa='\n';thola_inkomba_inani=셋째순번=='o'?yekisa_I_ofisethi(thola_inkomba_inani):Sebenzisa(thola_inkomba_inani);if(덧붙이기(&umugqa_yekisa,1)){if(셋째순번=='O')thola_inkomba_inani--;faka_8e07c86f=1;}continue;}
        if(셋째순번=='h'){thola_inkomba_inani=이전항목(thola_inkomba_inani);continue;}if(셋째순번=='l'){thola_inkomba_inani=다음(thola_inkomba_inani);continue;}if(셋째순번=='j'){Okuqondile(1);continue;}if(셋째순번=='k'){Okuqondile(-1);continue;}
        if(셋째순번=='0'){thola_inkomba_inani=Sebenzisa(thola_inkomba_inani);continue;}if(셋째순번=='$'){thola_inkomba_inani=yekisa_I_ofisethi(thola_inkomba_inani);continue;}if(셋째순번=='G'){thola_inkomba_inani=Sebenzisa(ubude_inani);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(thola_inkomba_inani<ubude_inani)바이트지우기(thola_inkomba_inani,다음(thola_inkomba_inani));continue;}
        if(셋째순번=='p'&&kopisha_ubude){thola_inkomba_inani=yekisa_I_ofisethi(thola_inkomba_inani);if(thola_inkomba_inani<ubude_inani)thola_inkomba_inani++;덧붙이기(복사자료,kopisha_ubude);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=Itekisi[순번];Itekisi[순번]=yekisa_imininingwane[순번];yekisa_imininingwane[순번]=둘째값;}int 개수=ubude_inani;ubude_inani=yekisa_ubude;yekisa_ubude=개수;개수=thola_inkomba_inani;thola_inkomba_inani=위쪽;위쪽=개수;개수=변경됨;변경됨=yekisa_Izinguquko;yekisa_Izinguquko=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=ozokusebenzisa(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
