/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char SMS[편집용량],tendua_data[편집용량],복사자료[편집용량],결과자료[1024];
static int urefu_thamani,kielezo_thamani,맨위,왼쪽,변경됨,chomeka,tendua_urefu,위쪽,tendua_Mabadiliko,되돌림있음,mfano_urefu,사용량,열수=68,행수=19;
static char faili_ingizo_jina[64],amri[128],gundua_ingizo[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned inayosubiri_Kitufe;
static int msaada_kategoria,hali_picha,hali_foleni;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void baiti_data(unsigned msimbo_wa_kibambo){if(hali_picha){if((msimbo_wa_kibambo&192)!=128){hali_foleni+=msimbo_wa_kibambo>=196?2:1;}if(hali_foleni>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=msimbo_wa_kibambo;}
static void 글내보내기(const char *tungo_data){while(*tungo_data)baiti_data((unsigned char)*tungo_data++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)baiti_data(둘째값[--순번]);}
static void hamisha_thamani(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);baiti_data(';');수치(열위치);baiti_data('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(SMS[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<urefu_thamani){자료위치++;while(자료위치<urefu_thamani&&(SMS[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int endesha(int 자료위치){while(자료위치>0&&SMS[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int tamatia_Chipua(int 자료위치){while(자료위치<urefu_thamani&&SMS[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned msimbo_wa_kibambo){return msimbo_wa_kibambo>=196?2:1;}
static int safuwima(int 자료위치){int msimbo_wa_kibambo=0;for(int 순번=endesha(자료위치);순번<자료위치;순번=다음(순번))msimbo_wa_kibambo+=SMS[순번]=='\t'?4-msimbo_wa_kibambo%4:너비(SMS[순번]);return msimbo_wa_kibambo;}
static void kituo_cha_ukaguzi(void){for(int 순번=0;순번<urefu_thamani;순번++)tendua_data[순번]=SMS[순번];tendua_urefu=urefu_thamani;위쪽=kielezo_thamani;tendua_Mabadiliko=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kituo_cha_ukaguzi();for(int 순번=도착위치;순번<urefu_thamani;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];urefu_thamani-=도착위치-출발위치;kielezo_thamani=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *tungo_data,int 개수){if(개수>편집용량-urefu_thamani){알림문="File full (16384 bytes)";return 0;}kituo_cha_ukaguzi();for(int 순번=urefu_thamani-1;순번>=kielezo_thamani;순번--)SMS[순번+개수]=SMS[순번];for(int 순번=0;순번<개수;순번++)SMS[kielezo_thamani+순번]=tungo_data[순번];urefu_thamani+=개수;kielezo_thamani+=개수;변경됨=1;return 1;}
static void Wima(int 차이){int 열위치=safuwima(kielezo_thamani),자료위치=endesha(kielezo_thamani);if(차이<0){if(!자료위치)return;자료위치=endesha(자료위치-1);}else{자료위치=tamatia_Chipua(자료위치);if(자료위치==urefu_thamani)return;자료위치++;}int msimbo_wa_kibambo=0;while(자료위치<urefu_thamani&&SMS[자료위치]!='\n'&&msimbo_wa_kibambo<열위치){msimbo_wa_kibambo+=SMS[자료위치]=='\t'?4-msimbo_wa_kibambo%4:너비(SMS[자료위치]);자료위치=다음(자료위치);}kielezo_thamani=자료위치;}
static void 화면그리기(void){
    if(kielezo_thamani>urefu_thamani)kielezo_thamani=urefu_thamani;if(맨위>kielezo_thamani)맨위=endesha(kielezo_thamani);맨위=endesha(맨위);
    int 행위치=0;for(int 순번=맨위;순번<kielezo_thamani;순번++)if(SMS[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=tamatia_Chipua(맨위);if(맨위<urefu_thamani)맨위++;행위치--;}
    int 열위치=safuwima(kielezo_thamani);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        hamisha_thamani(반환값+1,1);글내보내기("\033[0m\033[2K");int msimbo_wa_kibambo=0,그려진상태=0;
        if(자료위치>=urefu_thamani&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<urefu_thamani&&SMS[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=SMS[자료위치]=='\t'?4-msimbo_wa_kibambo%4:너비(SMS[자료위치]);
            if(msimbo_wa_kibambo>=왼쪽&&msimbo_wa_kibambo-왼쪽+너비값<열수){
                if(SMS[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)baiti_data(' ');}else if(SMS[자료위치]<32||SMS[자료위치]==127){baiti_data('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)baiti_data(SMS[안쪽순번]);그려진상태+=너비값;
            }msimbo_wa_kibambo+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<urefu_thamani)자료위치++;
    }
    hamisha_thamani(행수,1);글내보내기("\033[7m\033[2K");hali_picha=1;hali_foleni=0;글내보내기(chomeka?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(faili_ingizo_jina[이름바이트수]&&이름바이트수<30)baiti_data(faili_ingizo_jina[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int laini=1;for(int 순번=0;순번<kielezo_thamani;순번++)if(SMS[순번]=='\n')laini++;수치(laini);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)baiti_data(알림문[개수++]);}
    hali_picha=0;글내보내기("\033[0m");hamisha_thamani(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(inayosubiri_Kitufe){int 셋째순번=inayosubiri_Kitufe;inayosubiri_Kitufe=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned panga_ukubwa=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(panga_ukubwa&65535)||행수!=(int)(panga_ukubwa>>16)){
            열수=panga_ukubwa&65535;행수=panga_ukubwa>>16;화면그리기();
            if(msaada_kategoria){hamisha_thamani(행수,1);글내보내기("\033[0m\033[2K");baiti_data(msaada_kategoria);글내보내기(amri);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){inayosubiri_Kitufe=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int Store_thamani(void){
    int faili_kishiko=unda_faili(faili_ingizo_jina,soma_andika|없으면만들기|내용비우기,0600);if(faili_kishiko<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=andika_faili_data(faili_kishiko,SMS,urefu_thamani);funga_faili(faili_kishiko);if(개수!=urefu_thamani){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(gundua_ingizo[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=urefu_thamani;순번++){int 자료위치=(kielezo_thamani+순번)%(urefu_thamani?urefu_thamani:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<urefu_thamani&&SMS[자료위치+안쪽순번]==(unsigned char)gundua_ingizo[안쪽순번])안쪽순번++;if(안쪽순번==개수){kielezo_thamani=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int kisituo(int kategoria_thamani){
    int 개수=0;amri[0]=0;
    for(;;){hamisha_thamani(행수,1);글내보내기("\033[0m\033[2K");baiti_data(kategoria_thamani);글내보내기(amri);출력비우기();msaada_kategoria=kategoria_thamani;int 셋째순번=누름값();msaada_kategoria=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)amri[개수]&192)==128)개수--;amri[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){amri[개수++]=셋째순번;amri[개수]=0;}
    }
    if(kategoria_thamani=='/'){for(int 순번=0;순번<=개수;순번++)gundua_ingizo[순번]=amri[순번];다음찾기();return 0;}
    if(같은지(amri,"q!"))return 1;
    if(같은지(amri,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(amri,"wq")||같은지(amri,"x"))return Store_thamani();
    if(같은지(amri,"w")){Store_thamani();return 0;}
    if(amri[0]=='w'&&amri[1]==' '){int 순번=2;while(amri[순번]==' ')순번++;int panga_ukubwa=개수-순번;if(panga_ukubwa<1||panga_ukubwa>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<panga_ukubwa;안쪽순번++)faili_ingizo_jina[안쪽순번]=amri[순번+안쪽순번];faili_ingizo_jina[panga_ukubwa]=0;Store_thamani();return 0;}
    int laini=0;for(int 순번=0;순번<개수;순번++){if(amri[순번]<'0'||amri[순번]>'9'){laini=0;break;}laini=laini*10+amri[순번]-'0';if(laini>16384){laini=0;break;}}
    if(laini){kielezo_thamani=0;while(--laini&&kielezo_thamani<urefu_thamani){kielezo_thamani=tamatia_Chipua(kielezo_thamani);if(kielezo_thamani<urefu_thamani)kielezo_thamani++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Anza_mtumiaji_programu(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||mtumiaji_hoja(0,faili_ingizo_jina,sizeof(faili_ingizo_jina))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int faili_kishiko=unda_faili(faili_ingizo_jina,soma_tu_thamani,0);
    if(faili_kishiko>=0){int 개수=faili_panga_ukubwa(faili_kishiko);if(개수<0||개수>편집용량){funga_faili(faili_kishiko);return 1;}urefu_thamani=파일자료읽기(faili_kishiko,SMS,개수);funga_faili(faili_kishiko);if(urefu_thamani!=개수)return 1;for(int 순번=0;순번<urefu_thamani;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Wima(-1);continue;}if(셋째순번==1002){Wima(1);continue;}if(셋째순번==1003){kielezo_thamani=다음(kielezo_thamani);continue;}if(셋째순번==1004){kielezo_thamani=이전항목(kielezo_thamani);continue;}
        if(셋째순번==1005){kielezo_thamani=endesha(kielezo_thamani);continue;}if(셋째순번==1006){kielezo_thamani=tamatia_Chipua(kielezo_thamani);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)Wima(셋째순번==1008?-1:1);continue;}
        if(chomeka){
            if(셋째순번==27||셋째순번==3){chomeka=0;continue;}
            if(셋째순번==127||셋째순번==8){if(kielezo_thamani)바이트지우기(이전항목(kielezo_thamani),kielezo_thamani);continue;}
            if(셋째순번==1007){if(kielezo_thamani<urefu_thamani)바이트지우기(kielezo_thamani,다음(kielezo_thamani));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int msimbo_wa_kibambo=누름값();if(msimbo_wa_kibambo<128||msimbo_wa_kibambo>191){inayosubiri_Kitufe=msimbo_wa_kibambo;유효함=0;break;}둘째값[순번]=msimbo_wa_kibambo;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){kielezo_thamani=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=Store_thamani();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=endesha(kielezo_thamani),둘째값=tamatia_Chipua(kielezo_thamani);if(둘째값<urefu_thamani)둘째값++;mfano_urefu=둘째값-첫째값;for(int 순번=0;순번<mfano_urefu;순번++)복사자료[순번]=SMS[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){chomeka=1;continue;}if(셋째순번=='a'){if(kielezo_thamani<tamatia_Chipua(kielezo_thamani))kielezo_thamani=다음(kielezo_thamani);chomeka=1;continue;}
        if(셋째순번=='I'){kielezo_thamani=endesha(kielezo_thamani);chomeka=1;continue;}if(셋째순번=='A'){kielezo_thamani=tamatia_Chipua(kielezo_thamani);chomeka=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char laini_tamatia='\n';kielezo_thamani=셋째순번=='o'?tamatia_Chipua(kielezo_thamani):endesha(kielezo_thamani);if(덧붙이기(&laini_tamatia,1)){if(셋째순번=='O')kielezo_thamani--;chomeka=1;}continue;}
        if(셋째순번=='h'){kielezo_thamani=이전항목(kielezo_thamani);continue;}if(셋째순번=='l'){kielezo_thamani=다음(kielezo_thamani);continue;}if(셋째순번=='j'){Wima(1);continue;}if(셋째순번=='k'){Wima(-1);continue;}
        if(셋째순번=='0'){kielezo_thamani=endesha(kielezo_thamani);continue;}if(셋째순번=='$'){kielezo_thamani=tamatia_Chipua(kielezo_thamani);continue;}if(셋째순번=='G'){kielezo_thamani=endesha(urefu_thamani);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(kielezo_thamani<urefu_thamani)바이트지우기(kielezo_thamani,다음(kielezo_thamani));continue;}
        if(셋째순번=='p'&&mfano_urefu){kielezo_thamani=tamatia_Chipua(kielezo_thamani);if(kielezo_thamani<urefu_thamani)kielezo_thamani++;덧붙이기(복사자료,mfano_urefu);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=SMS[순번];SMS[순번]=tendua_data[순번];tendua_data[순번]=둘째값;}int 개수=urefu_thamani;urefu_thamani=tendua_urefu;tendua_urefu=개수;개수=kielezo_thamani;kielezo_thamani=위쪽;위쪽=개수;개수=변경됨;변경됨=tendua_Mabadiliko;tendua_Mabadiliko=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=kisituo(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
