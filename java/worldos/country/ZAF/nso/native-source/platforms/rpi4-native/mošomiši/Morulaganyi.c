/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Sengwalwa[편집용량],dirolla_data[편집용량],복사자료[편집용량],결과자료[1024];
static int botelele_boleng,lokela_boleng,맨위,왼쪽,변경됨,tsenya,dirolla_botelele,위쪽,dirolla_Diphetogo,되돌림있음,kopiša_botelele,사용량,열수=68,행수=19;
static char faele_go_tsenya_tshedimošo_leina[64],Taelo[128],hwetša_go_tsenya_tshedimošo[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned e_sa_šoma_khii;
static int thušo_legoro,boemo_seswantšho,boemo_lenaneotetelo;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void paete_data(unsigned khouto_ya_tlhaka){if(boemo_seswantšho){if((khouto_ya_tlhaka&192)!=128){boemo_lenaneotetelo+=khouto_ya_tlhaka>=196?2:1;}if(boemo_lenaneotetelo>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=khouto_ya_tlhaka;}
static void 글내보내기(const char *molokoloko_data){while(*molokoloko_data)paete_data((unsigned char)*molokoloko_data++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)paete_data(둘째값[--순번]);}
static void šuthiša_boleng(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);paete_data(';');수치(열위치);paete_data('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(Sengwalwa[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<botelele_boleng){자료위치++;while(자료위치<botelele_boleng&&(Sengwalwa[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int Diriša(int 자료위치){while(자료위치>0&&Sengwalwa[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int fetša_E_Šetšego(int 자료위치){while(자료위치<botelele_boleng&&Sengwalwa[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned khouto_ya_tlhaka){return khouto_ya_tlhaka>=196?2:1;}
static int kholomo(int 자료위치){int khouto_ya_tlhaka=0;for(int 순번=Diriša(자료위치);순번<자료위치;순번=다음(순번))khouto_ya_tlhaka+=Sengwalwa[순번]=='\t'?4-khouto_ya_tlhaka%4:너비(Sengwalwa[순번]);return khouto_ya_tlhaka;}
static void lefelwanatekolo(void){for(int 순번=0;순번<botelele_boleng;순번++)dirolla_data[순번]=Sengwalwa[순번];dirolla_botelele=botelele_boleng;위쪽=lokela_boleng;dirolla_Diphetogo=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){lefelwanatekolo();for(int 순번=도착위치;순번<botelele_boleng;순번++)Sengwalwa[출발위치+순번-도착위치]=Sengwalwa[순번];botelele_boleng-=도착위치-출발위치;lokela_boleng=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *molokoloko_data,int 개수){if(개수>편집용량-botelele_boleng){알림문="File full (16384 bytes)";return 0;}lefelwanatekolo();for(int 순번=botelele_boleng-1;순번>=lokela_boleng;순번--)Sengwalwa[순번+개수]=Sengwalwa[순번];for(int 순번=0;순번<개수;순번++)Sengwalwa[lokela_boleng+순번]=molokoloko_data[순번];botelele_boleng+=개수;lokela_boleng+=개수;변경됨=1;return 1;}
static void Tsepamo(int 차이){int 열위치=kholomo(lokela_boleng),자료위치=Diriša(lokela_boleng);if(차이<0){if(!자료위치)return;자료위치=Diriša(자료위치-1);}else{자료위치=fetša_E_Šetšego(자료위치);if(자료위치==botelele_boleng)return;자료위치++;}int khouto_ya_tlhaka=0;while(자료위치<botelele_boleng&&Sengwalwa[자료위치]!='\n'&&khouto_ya_tlhaka<열위치){khouto_ya_tlhaka+=Sengwalwa[자료위치]=='\t'?4-khouto_ya_tlhaka%4:너비(Sengwalwa[자료위치]);자료위치=다음(자료위치);}lokela_boleng=자료위치;}
static void 화면그리기(void){
    if(lokela_boleng>botelele_boleng)lokela_boleng=botelele_boleng;if(맨위>lokela_boleng)맨위=Diriša(lokela_boleng);맨위=Diriša(맨위);
    int 행위치=0;for(int 순번=맨위;순번<lokela_boleng;순번++)if(Sengwalwa[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=fetša_E_Šetšego(맨위);if(맨위<botelele_boleng)맨위++;행위치--;}
    int 열위치=kholomo(lokela_boleng);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        šuthiša_boleng(반환값+1,1);글내보내기("\033[0m\033[2K");int khouto_ya_tlhaka=0,그려진상태=0;
        if(자료위치>=botelele_boleng&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<botelele_boleng&&Sengwalwa[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=Sengwalwa[자료위치]=='\t'?4-khouto_ya_tlhaka%4:너비(Sengwalwa[자료위치]);
            if(khouto_ya_tlhaka>=왼쪽&&khouto_ya_tlhaka-왼쪽+너비값<열수){
                if(Sengwalwa[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)paete_data(' ');}else if(Sengwalwa[자료위치]<32||Sengwalwa[자료위치]==127){paete_data('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)paete_data(Sengwalwa[안쪽순번]);그려진상태+=너비값;
            }khouto_ya_tlhaka+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<botelele_boleng)자료위치++;
    }
    šuthiša_boleng(행수,1);글내보내기("\033[7m\033[2K");boemo_seswantšho=1;boemo_lenaneotetelo=0;글내보내기(tsenya?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(faele_go_tsenya_tshedimošo_leina[이름바이트수]&&이름바이트수<30)paete_data(faele_go_tsenya_tshedimošo_leina[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int mothaladi=1;for(int 순번=0;순번<lokela_boleng;순번++)if(Sengwalwa[순번]=='\n')mothaladi++;수치(mothaladi);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)paete_data(알림문[개수++]);}
    boemo_seswantšho=0;글내보내기("\033[0m");šuthiša_boleng(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(e_sa_šoma_khii){int 셋째순번=e_sa_šoma_khii;e_sa_šoma_khii=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Bogolo=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(Bogolo&65535)||행수!=(int)(Bogolo>>16)){
            열수=Bogolo&65535;행수=Bogolo>>16;화면그리기();
            if(thušo_legoro){šuthiša_boleng(행수,1);글내보내기("\033[0m\033[2K");paete_data(thušo_legoro);글내보내기(Taelo);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){e_sa_šoma_khii=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int lota_boleng(void){
    int faele_tshwaro=bula_faele(faele_go_tsenya_tshedimošo_leina,bala_ngwala|없으면만들기|내용비우기,0600);if(faele_tshwaro<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=ngwala_faele_data(faele_tshwaro,Sengwalwa,botelele_boleng);tswalela_faele(faele_tshwaro);if(개수!=botelele_boleng){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(hwetša_go_tsenya_tshedimošo[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=botelele_boleng;순번++){int 자료위치=(lokela_boleng+순번)%(botelele_boleng?botelele_boleng:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<botelele_boleng&&Sengwalwa[자료위치+안쪽순번]==(unsigned char)hwetša_go_tsenya_tshedimošo[안쪽순번])안쪽순번++;if(안쪽순번==개수){lokela_boleng=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int temoši(int legoro_boleng){
    int 개수=0;Taelo[0]=0;
    for(;;){šuthiša_boleng(행수,1);글내보내기("\033[0m\033[2K");paete_data(legoro_boleng);글내보내기(Taelo);출력비우기();thušo_legoro=legoro_boleng;int 셋째순번=누름값();thušo_legoro=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)Taelo[개수]&192)==128)개수--;Taelo[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){Taelo[개수++]=셋째순번;Taelo[개수]=0;}
    }
    if(legoro_boleng=='/'){for(int 순번=0;순번<=개수;순번++)hwetša_go_tsenya_tshedimošo[순번]=Taelo[순번];다음찾기();return 0;}
    if(같은지(Taelo,"q!"))return 1;
    if(같은지(Taelo,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Taelo,"wq")||같은지(Taelo,"x"))return lota_boleng();
    if(같은지(Taelo,"w")){lota_boleng();return 0;}
    if(Taelo[0]=='w'&&Taelo[1]==' '){int 순번=2;while(Taelo[순번]==' ')순번++;int Bogolo=개수-순번;if(Bogolo<1||Bogolo>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Bogolo;안쪽순번++)faele_go_tsenya_tshedimošo_leina[안쪽순번]=Taelo[순번+안쪽순번];faele_go_tsenya_tshedimošo_leina[Bogolo]=0;lota_boleng();return 0;}
    int mothaladi=0;for(int 순번=0;순번<개수;순번++){if(Taelo[순번]<'0'||Taelo[순번]>'9'){mothaladi=0;break;}mothaladi=mothaladi*10+Taelo[순번]-'0';if(mothaladi>16384){mothaladi=0;break;}}
    if(mothaladi){lokela_boleng=0;while(--mothaladi&&lokela_boleng<botelele_boleng){lokela_boleng=fetša_E_Šetšego(lokela_boleng);if(lokela_boleng<botelele_boleng)lokela_boleng++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Thomišo_mošomiši_tirišo(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||mošomiši_akumente(0,faele_go_tsenya_tshedimošo_leina,sizeof(faele_go_tsenya_tshedimošo_leina))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int faele_tshwaro=bula_faele(faele_go_tsenya_tshedimošo_leina,balwago_fela_boleng,0);
    if(faele_tshwaro>=0){int 개수=faele_bogolo(faele_tshwaro);if(개수<0||개수>편집용량){tswalela_faele(faele_tshwaro);return 1;}botelele_boleng=파일자료읽기(faele_tshwaro,Sengwalwa,개수);tswalela_faele(faele_tshwaro);if(botelele_boleng!=개수)return 1;for(int 순번=0;순번<botelele_boleng;순번++)if(!Sengwalwa[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Tsepamo(-1);continue;}if(셋째순번==1002){Tsepamo(1);continue;}if(셋째순번==1003){lokela_boleng=다음(lokela_boleng);continue;}if(셋째순번==1004){lokela_boleng=이전항목(lokela_boleng);continue;}
        if(셋째순번==1005){lokela_boleng=Diriša(lokela_boleng);continue;}if(셋째순번==1006){lokela_boleng=fetša_E_Šetšego(lokela_boleng);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)Tsepamo(셋째순번==1008?-1:1);continue;}
        if(tsenya){
            if(셋째순번==27||셋째순번==3){tsenya=0;continue;}
            if(셋째순번==127||셋째순번==8){if(lokela_boleng)바이트지우기(이전항목(lokela_boleng),lokela_boleng);continue;}
            if(셋째순번==1007){if(lokela_boleng<botelele_boleng)바이트지우기(lokela_boleng,다음(lokela_boleng));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int khouto_ya_tlhaka=누름값();if(khouto_ya_tlhaka<128||khouto_ya_tlhaka>191){e_sa_šoma_khii=khouto_ya_tlhaka;유효함=0;break;}둘째값[순번]=khouto_ya_tlhaka;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){lokela_boleng=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=lota_boleng();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=Diriša(lokela_boleng),둘째값=fetša_E_Šetšego(lokela_boleng);if(둘째값<botelele_boleng)둘째값++;kopiša_botelele=둘째값-첫째값;for(int 순번=0;순번<kopiša_botelele;순번++)복사자료[순번]=Sengwalwa[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){tsenya=1;continue;}if(셋째순번=='a'){if(lokela_boleng<fetša_E_Šetšego(lokela_boleng))lokela_boleng=다음(lokela_boleng);tsenya=1;continue;}
        if(셋째순번=='I'){lokela_boleng=Diriša(lokela_boleng);tsenya=1;continue;}if(셋째순번=='A'){lokela_boleng=fetša_E_Šetšego(lokela_boleng);tsenya=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char mothaladi_fetša='\n';lokela_boleng=셋째순번=='o'?fetša_E_Šetšego(lokela_boleng):Diriša(lokela_boleng);if(덧붙이기(&mothaladi_fetša,1)){if(셋째순번=='O')lokela_boleng--;tsenya=1;}continue;}
        if(셋째순번=='h'){lokela_boleng=이전항목(lokela_boleng);continue;}if(셋째순번=='l'){lokela_boleng=다음(lokela_boleng);continue;}if(셋째순번=='j'){Tsepamo(1);continue;}if(셋째순번=='k'){Tsepamo(-1);continue;}
        if(셋째순번=='0'){lokela_boleng=Diriša(lokela_boleng);continue;}if(셋째순번=='$'){lokela_boleng=fetša_E_Šetšego(lokela_boleng);continue;}if(셋째순번=='G'){lokela_boleng=Diriša(botelele_boleng);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(lokela_boleng<botelele_boleng)바이트지우기(lokela_boleng,다음(lokela_boleng));continue;}
        if(셋째순번=='p'&&kopiša_botelele){lokela_boleng=fetša_E_Šetšego(lokela_boleng);if(lokela_boleng<botelele_boleng)lokela_boleng++;덧붙이기(복사자료,kopiša_botelele);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=Sengwalwa[순번];Sengwalwa[순번]=dirolla_data[순번];dirolla_data[순번]=둘째값;}int 개수=botelele_boleng;botelele_boleng=dirolla_botelele;dirolla_botelele=개수;개수=lokela_boleng;lokela_boleng=위쪽;위쪽=개수;개수=변경됨;변경됨=dirolla_Diphetogo;dirolla_Diphetogo=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=temoši(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
