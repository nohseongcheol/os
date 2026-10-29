/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Umwandiko[편집용량],kugaruraho_amakurushingiro[편집용량],복사자료[편집용량],결과자료[1024];
static int uburebure_agaciro,umugerekashakiro_agaciro,맨위,왼쪽,변경됨,kongeramo,kugaruraho_uburebure,위쪽,kugaruraho_Ibyahinduwe,되돌림있음,kopi_uburebure,사용량,열수=68,행수=19;
static char dosiye_icyinjizwa_izina[64],Icyo_wifuza[128],gushaka_icyinjizwa[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned gitegereje_buto;
static int ifashayoboro_icyiciro,imimerere_ishusho,imimerere_umurongo_utegererezwaho;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void bayiti_amakurushingiro(unsigned 문자값){if(imimerere_ishusho){if((문자값&192)!=128){imimerere_umurongo_utegererezwaho+=문자값>=196?2:1;}if(imimerere_umurongo_utegererezwaho>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=문자값;}
static void 글내보내기(const char *igicenteruro_amakurushingiro){while(*igicenteruro_amakurushingiro)bayiti_amakurushingiro((unsigned char)*igicenteruro_amakurushingiro++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)bayiti_amakurushingiro(둘째값[--순번]);}
static void kwimura_agaciro(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);bayiti_amakurushingiro(';');수치(열위치);bayiti_amakurushingiro('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(Umwandiko[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<uburebure_agaciro){자료위치++;while(자료위치<uburebure_agaciro&&(Umwandiko[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int ihuriro(int 자료위치){while(자료위치>0&&Umwandiko[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int kurangiza_Ofuseti(int 자료위치){while(자료위치<uburebure_agaciro&&Umwandiko[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned 문자값){return 문자값>=196?2:1;}
static int inkingi(int 자료위치){int 문자값=0;for(int 순번=ihuriro(자료위치);순번<자료위치;순번=다음(순번))문자값+=Umwandiko[순번]=='\t'?4-문자값%4:너비(Umwandiko[순번]);return 문자값;}
static void ah_igenzura(void){for(int 순번=0;순번<uburebure_agaciro;순번++)kugaruraho_amakurushingiro[순번]=Umwandiko[순번];kugaruraho_uburebure=uburebure_agaciro;위쪽=umugerekashakiro_agaciro;kugaruraho_Ibyahinduwe=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){ah_igenzura();for(int 순번=도착위치;순번<uburebure_agaciro;순번++)Umwandiko[출발위치+순번-도착위치]=Umwandiko[순번];uburebure_agaciro-=도착위치-출발위치;umugerekashakiro_agaciro=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *igicenteruro_amakurushingiro,int 개수){if(개수>편집용량-uburebure_agaciro){알림문="File full (16384 bytes)";return 0;}ah_igenzura();for(int 순번=uburebure_agaciro-1;순번>=umugerekashakiro_agaciro;순번--)Umwandiko[순번+개수]=Umwandiko[순번];for(int 순번=0;순번<개수;순번++)Umwandiko[umugerekashakiro_agaciro+순번]=igicenteruro_amakurushingiro[순번];uburebure_agaciro+=개수;umugerekashakiro_agaciro+=개수;변경됨=1;return 1;}
static void Impagarike(int 차이){int 열위치=inkingi(umugerekashakiro_agaciro),자료위치=ihuriro(umugerekashakiro_agaciro);if(차이<0){if(!자료위치)return;자료위치=ihuriro(자료위치-1);}else{자료위치=kurangiza_Ofuseti(자료위치);if(자료위치==uburebure_agaciro)return;자료위치++;}int 문자값=0;while(자료위치<uburebure_agaciro&&Umwandiko[자료위치]!='\n'&&문자값<열위치){문자값+=Umwandiko[자료위치]=='\t'?4-문자값%4:너비(Umwandiko[자료위치]);자료위치=다음(자료위치);}umugerekashakiro_agaciro=자료위치;}
static void 화면그리기(void){
    if(umugerekashakiro_agaciro>uburebure_agaciro)umugerekashakiro_agaciro=uburebure_agaciro;if(맨위>umugerekashakiro_agaciro)맨위=ihuriro(umugerekashakiro_agaciro);맨위=ihuriro(맨위);
    int 행위치=0;for(int 순번=맨위;순번<umugerekashakiro_agaciro;순번++)if(Umwandiko[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=kurangiza_Ofuseti(맨위);if(맨위<uburebure_agaciro)맨위++;행위치--;}
    int 열위치=inkingi(umugerekashakiro_agaciro);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        kwimura_agaciro(반환값+1,1);글내보내기("\033[0m\033[2K");int 문자값=0,그려진상태=0;
        if(자료위치>=uburebure_agaciro&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<uburebure_agaciro&&Umwandiko[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=Umwandiko[자료위치]=='\t'?4-문자값%4:너비(Umwandiko[자료위치]);
            if(문자값>=왼쪽&&문자값-왼쪽+너비값<열수){
                if(Umwandiko[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bayiti_amakurushingiro(' ');}else if(Umwandiko[자료위치]<32||Umwandiko[자료위치]==127){bayiti_amakurushingiro('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)bayiti_amakurushingiro(Umwandiko[안쪽순번]);그려진상태+=너비값;
            }문자값+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<uburebure_agaciro)자료위치++;
    }
    kwimura_agaciro(행수,1);글내보내기("\033[7m\033[2K");imimerere_ishusho=1;imimerere_umurongo_utegererezwaho=0;글내보내기(kongeramo?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(dosiye_icyinjizwa_izina[이름바이트수]&&이름바이트수<30)bayiti_amakurushingiro(dosiye_icyinjizwa_izina[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int umurongo=1;for(int 순번=0;순번<umugerekashakiro_agaciro;순번++)if(Umwandiko[순번]=='\n')umurongo++;수치(umurongo);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)bayiti_amakurushingiro(알림문[개수++]);}
    imimerere_ishusho=0;글내보내기("\033[0m");kwimura_agaciro(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(gitegereje_buto){int 셋째순번=gitegereje_buto;gitegereje_buto=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Ingano=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(Ingano&65535)||행수!=(int)(Ingano>>16)){
            열수=Ingano&65535;행수=Ingano>>16;화면그리기();
            if(ifashayoboro_icyiciro){kwimura_agaciro(행수,1);글내보내기("\033[0m\033[2K");bayiti_amakurushingiro(ifashayoboro_icyiciro);글내보내기(Icyo_wifuza);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){gitegereje_buto=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int Store_agaciro(void){
    int dosiye_umukondo=kurema_dosiye(dosiye_icyinjizwa_izina,gusoma_kwandika|없으면만들기|내용비우기,0600);if(dosiye_umukondo<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=kwandika_dosiye_amakurushingiro(dosiye_umukondo,Umwandiko,uburebure_agaciro);gufunga_dosiye(dosiye_umukondo);if(개수!=uburebure_agaciro){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(gushaka_icyinjizwa[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=uburebure_agaciro;순번++){int 자료위치=(umugerekashakiro_agaciro+순번)%(uburebure_agaciro?uburebure_agaciro:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<uburebure_agaciro&&Umwandiko[자료위치+안쪽순번]==(unsigned char)gushaka_icyinjizwa[안쪽순번])안쪽순번++;if(안쪽순번==개수){umugerekashakiro_agaciro=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int integuza(int icyiciro_agaciro){
    int 개수=0;Icyo_wifuza[0]=0;
    for(;;){kwimura_agaciro(행수,1);글내보내기("\033[0m\033[2K");bayiti_amakurushingiro(icyiciro_agaciro);글내보내기(Icyo_wifuza);출력비우기();ifashayoboro_icyiciro=icyiciro_agaciro;int 셋째순번=누름값();ifashayoboro_icyiciro=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)Icyo_wifuza[개수]&192)==128)개수--;Icyo_wifuza[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){Icyo_wifuza[개수++]=셋째순번;Icyo_wifuza[개수]=0;}
    }
    if(icyiciro_agaciro=='/'){for(int 순번=0;순번<=개수;순번++)gushaka_icyinjizwa[순번]=Icyo_wifuza[순번];다음찾기();return 0;}
    if(같은지(Icyo_wifuza,"q!"))return 1;
    if(같은지(Icyo_wifuza,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Icyo_wifuza,"wq")||같은지(Icyo_wifuza,"x"))return Store_agaciro();
    if(같은지(Icyo_wifuza,"w")){Store_agaciro();return 0;}
    if(Icyo_wifuza[0]=='w'&&Icyo_wifuza[1]==' '){int 순번=2;while(Icyo_wifuza[순번]==' ')순번++;int Ingano=개수-순번;if(Ingano<1||Ingano>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Ingano;안쪽순번++)dosiye_icyinjizwa_izina[안쪽순번]=Icyo_wifuza[순번+안쪽순번];dosiye_icyinjizwa_izina[Ingano]=0;Store_agaciro();return 0;}
    int umurongo=0;for(int 순번=0;순번<개수;순번++){if(Icyo_wifuza[순번]<'0'||Icyo_wifuza[순번]>'9'){umurongo=0;break;}umurongo=umurongo*10+Icyo_wifuza[순번]-'0';if(umurongo>16384){umurongo=0;break;}}
    if(umurongo){umugerekashakiro_agaciro=0;while(--umurongo&&umugerekashakiro_agaciro<uburebure_agaciro){umugerekashakiro_agaciro=kurangiza_Ofuseti(umugerekashakiro_agaciro);if(umugerekashakiro_agaciro<uburebure_agaciro)umugerekashakiro_agaciro++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Itangira_ukoresha_porogaramu(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||ukoresha_ingingo(0,dosiye_icyinjizwa_izina,sizeof(dosiye_icyinjizwa_izina))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int dosiye_umukondo=kurema_dosiye(dosiye_icyinjizwa_izina,soma_gusa_agaciro,0);
    if(dosiye_umukondo>=0){int 개수=dosiye_ingano(dosiye_umukondo);if(개수<0||개수>편집용량){gufunga_dosiye(dosiye_umukondo);return 1;}uburebure_agaciro=파일자료읽기(dosiye_umukondo,Umwandiko,개수);gufunga_dosiye(dosiye_umukondo);if(uburebure_agaciro!=개수)return 1;for(int 순번=0;순번<uburebure_agaciro;순번++)if(!Umwandiko[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Impagarike(-1);continue;}if(셋째순번==1002){Impagarike(1);continue;}if(셋째순번==1003){umugerekashakiro_agaciro=다음(umugerekashakiro_agaciro);continue;}if(셋째순번==1004){umugerekashakiro_agaciro=이전항목(umugerekashakiro_agaciro);continue;}
        if(셋째순번==1005){umugerekashakiro_agaciro=ihuriro(umugerekashakiro_agaciro);continue;}if(셋째순번==1006){umugerekashakiro_agaciro=kurangiza_Ofuseti(umugerekashakiro_agaciro);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)Impagarike(셋째순번==1008?-1:1);continue;}
        if(kongeramo){
            if(셋째순번==27||셋째순번==3){kongeramo=0;continue;}
            if(셋째순번==127||셋째순번==8){if(umugerekashakiro_agaciro)바이트지우기(이전항목(umugerekashakiro_agaciro),umugerekashakiro_agaciro);continue;}
            if(셋째순번==1007){if(umugerekashakiro_agaciro<uburebure_agaciro)바이트지우기(umugerekashakiro_agaciro,다음(umugerekashakiro_agaciro));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int 문자값=누름값();if(문자값<128||문자값>191){gitegereje_buto=문자값;유효함=0;break;}둘째값[순번]=문자값;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){umugerekashakiro_agaciro=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=Store_agaciro();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=ihuriro(umugerekashakiro_agaciro),둘째값=kurangiza_Ofuseti(umugerekashakiro_agaciro);if(둘째값<uburebure_agaciro)둘째값++;kopi_uburebure=둘째값-첫째값;for(int 순번=0;순번<kopi_uburebure;순번++)복사자료[순번]=Umwandiko[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){kongeramo=1;continue;}if(셋째순번=='a'){if(umugerekashakiro_agaciro<kurangiza_Ofuseti(umugerekashakiro_agaciro))umugerekashakiro_agaciro=다음(umugerekashakiro_agaciro);kongeramo=1;continue;}
        if(셋째순번=='I'){umugerekashakiro_agaciro=ihuriro(umugerekashakiro_agaciro);kongeramo=1;continue;}if(셋째순번=='A'){umugerekashakiro_agaciro=kurangiza_Ofuseti(umugerekashakiro_agaciro);kongeramo=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char umurongo_kurangiza='\n';umugerekashakiro_agaciro=셋째순번=='o'?kurangiza_Ofuseti(umugerekashakiro_agaciro):ihuriro(umugerekashakiro_agaciro);if(덧붙이기(&umurongo_kurangiza,1)){if(셋째순번=='O')umugerekashakiro_agaciro--;kongeramo=1;}continue;}
        if(셋째순번=='h'){umugerekashakiro_agaciro=이전항목(umugerekashakiro_agaciro);continue;}if(셋째순번=='l'){umugerekashakiro_agaciro=다음(umugerekashakiro_agaciro);continue;}if(셋째순번=='j'){Impagarike(1);continue;}if(셋째순번=='k'){Impagarike(-1);continue;}
        if(셋째순번=='0'){umugerekashakiro_agaciro=ihuriro(umugerekashakiro_agaciro);continue;}if(셋째순번=='$'){umugerekashakiro_agaciro=kurangiza_Ofuseti(umugerekashakiro_agaciro);continue;}if(셋째순번=='G'){umugerekashakiro_agaciro=ihuriro(uburebure_agaciro);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(umugerekashakiro_agaciro<uburebure_agaciro)바이트지우기(umugerekashakiro_agaciro,다음(umugerekashakiro_agaciro));continue;}
        if(셋째순번=='p'&&kopi_uburebure){umugerekashakiro_agaciro=kurangiza_Ofuseti(umugerekashakiro_agaciro);if(umugerekashakiro_agaciro<uburebure_agaciro)umugerekashakiro_agaciro++;덧붙이기(복사자료,kopi_uburebure);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=Umwandiko[순번];Umwandiko[순번]=kugaruraho_amakurushingiro[순번];kugaruraho_amakurushingiro[순번]=둘째값;}int 개수=uburebure_agaciro;uburebure_agaciro=kugaruraho_uburebure;kugaruraho_uburebure=개수;개수=umugerekashakiro_agaciro;umugerekashakiro_agaciro=위쪽;위쪽=개수;개수=변경됨;변경됨=kugaruraho_Ibyahinduwe;kugaruraho_Ibyahinduwe=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=integuza(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
