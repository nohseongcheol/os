/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char SMS[편집용량],i_undo_data[편집용량],복사자료[편집용량],sukat_data[1024];
static int haba_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,magsingit_isingit,i_undo_haba,위쪽,i_undo_Mga_Pagbabago,되돌림있음,gumawa_ng_kopya_haba,사용량,COLUMNS=68,ROW_COUNT=19;
static char file_pagpasok_pangalan[64],utos[128],FIND_pagpasok[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned pending_key;
static int tulong_kategorya,katayuan_IMAGE,katayuan_pila;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)sukat_data,사용량,0,0,0);사용량=0;}}
static void byte_data(unsigned character_code){if(katayuan_IMAGE){if((character_code&192)!=128){katayuan_pila+=character_code>=196?2:1;}if(katayuan_pila>=COLUMNS)return;}if(사용량==(int)sizeof(sukat_data))출력비우기();sukat_data[사용량++]=character_code;}
static void 글내보내기(const char *string_data){while(*string_data)byte_data((unsigned char)*string_data++);}
static void 수치(unsigned item_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+item_COUNT%10;item_COUNT/=10;}while(item_COUNT);while(순번)byte_data(SECOND_VALUE[--순번]);}
static void ilipat_VALUE(int ROW_posisyon,int kolum_posisyon){글내보내기("\033[");수치(ROW_posisyon);byte_data(';');수치(kolum_posisyon);byte_data('H');}
static int 이전항목(int data_posisyon){if(data_posisyon){data_posisyon--;while(data_posisyon>0&&(SMS[data_posisyon]&192)==128)data_posisyon--;}return data_posisyon;}
static int Susunod_item(int data_posisyon){if(data_posisyon<haba_VALUE){data_posisyon++;while(data_posisyon<haba_VALUE&&(SMS[data_posisyon]&192)==128)data_posisyon++;}return data_posisyon;}
static int run(int data_posisyon){while(data_posisyon>0&&SMS[data_posisyon-1]!='\n')data_posisyon--;return data_posisyon;}
static int tapusin_OFFSET(int data_posisyon){while(data_posisyon<haba_VALUE&&SMS[data_posisyon]!='\n')data_posisyon++;return data_posisyon;}
static int 너비(unsigned character_code){return character_code>=196?2:1;}
static int kolum(int data_posisyon){int character_code=0;for(int 순번=run(data_posisyon);순번<data_posisyon;순번=Susunod_item(순번))character_code+=SMS[순번]=='\t'?4-character_code%4:너비(SMS[순번]);return character_code;}
static void checkpoint(void){for(int 순번=0;순번<haba_VALUE;순번++)i_undo_data[순번]=SMS[순번];i_undo_haba=haba_VALUE;위쪽=INDEX_VALUE;i_undo_Mga_Pagbabago=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){checkpoint();for(int 순번=도착위치;순번<haba_VALUE;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];haba_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *string_data,int item_COUNT){if(item_COUNT>편집용량-haba_VALUE){알림문="File full (16384 bytes)";return 0;}checkpoint();for(int 순번=haba_VALUE-1;순번>=INDEX_VALUE;순번--)SMS[순번+item_COUNT]=SMS[순번];for(int 순번=0;순번<item_COUNT;순번++)SMS[INDEX_VALUE+순번]=string_data[순번];haba_VALUE+=item_COUNT;INDEX_VALUE+=item_COUNT;변경됨=1;return 1;}
static void archive(int 차이){int kolum_posisyon=kolum(INDEX_VALUE),data_posisyon=run(INDEX_VALUE);if(차이<0){if(!data_posisyon)return;data_posisyon=run(data_posisyon-1);}else{data_posisyon=tapusin_OFFSET(data_posisyon);if(data_posisyon==haba_VALUE)return;data_posisyon++;}int character_code=0;while(data_posisyon<haba_VALUE&&SMS[data_posisyon]!='\n'&&character_code<kolum_posisyon){character_code+=SMS[data_posisyon]=='\t'?4-character_code%4:너비(SMS[data_posisyon]);data_posisyon=Susunod_item(data_posisyon);}INDEX_VALUE=data_posisyon;}
static void 화면그리기(void){
    if(INDEX_VALUE>haba_VALUE)INDEX_VALUE=haba_VALUE;if(맨위>INDEX_VALUE)맨위=run(INDEX_VALUE);맨위=run(맨위);
    int ROW_posisyon=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')ROW_posisyon++;
    while(ROW_posisyon>=ROW_COUNT-1){맨위=tapusin_OFFSET(맨위);if(맨위<haba_VALUE)맨위++;ROW_posisyon--;}
    int kolum_posisyon=kolum(INDEX_VALUE);if(kolum_posisyon<왼쪽)왼쪽=kolum_posisyon;if(kolum_posisyon-왼쪽>=COLUMNS-1)왼쪽=kolum_posisyon-COLUMNS+2;
    글내보내기("\033[?25l");int data_posisyon=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        ilipat_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int character_code=0,그려진상태=0;
        if(data_posisyon>=haba_VALUE&&반환값>ROW_posisyon){글내보내기("\033[90m~\033[0m");continue;}
        while(data_posisyon<haba_VALUE&&SMS[data_posisyon]!='\n'){
            int Susunod_OFFSET=Susunod_item(data_posisyon),너비값=SMS[data_posisyon]=='\t'?4-character_code%4:너비(SMS[data_posisyon]);
            if(character_code>=왼쪽&&character_code-왼쪽+너비값<COLUMNS){
                if(SMS[data_posisyon]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_data(' ');}else if(SMS[data_posisyon]<32||SMS[data_posisyon]==127){byte_data('?');}else for(int 안쪽순번=data_posisyon;안쪽순번<Susunod_OFFSET;안쪽순번++)byte_data(SMS[안쪽순번]);그려진상태+=너비값;
            }character_code+=너비값;data_posisyon=Susunod_OFFSET;
        }
        (void)그려진상태;if(data_posisyon<haba_VALUE)data_posisyon++;
    }
    ilipat_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");katayuan_IMAGE=1;katayuan_pila=0;글내보내기(magsingit_isingit?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(file_pagpasok_pangalan[이름바이트수]&&이름바이트수<30)byte_data(file_pagpasok_pangalan[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int linya=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')linya++;수치(linya);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int item_COUNT=0;글내보내기(" | ");while(알림문[item_COUNT]&&item_COUNT<20)byte_data(알림문[item_COUNT++]);}
    katayuan_IMAGE=0;글내보내기("\033[0m");ilipat_VALUE(ROW_posisyon+1,kolum_posisyon-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(pending_key){int 셋째순번=pending_key;pending_key=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned sukat_82232621=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(sukat_82232621&65535)||ROW_COUNT!=(int)(sukat_82232621>>16)){
            COLUMNS=sukat_82232621&65535;ROW_COUNT=sukat_82232621>>16;화면그리기();
            if(tulong_kategorya){ilipat_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_data(tulong_kategorya);글내보내기(utos);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){pending_key=셋째순번;return 27;}
    int item_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){item_COUNT=item_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return item_COUNT==3?1007:item_COUNT==5?1008:item_COUNT==6?1009:item_COUNT==1?1005:item_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int file_hawakán=buksan_file(file_pagpasok_pangalan,nababasa_nasusulatan|없으면만들기|내용비우기,0600);if(file_hawakán<0){알림문="Cannot open for save";return 0;}
    intptr_t item_COUNT=sumulat_file_data(file_hawakán,SMS,haba_VALUE);isara_file(file_hawakán);if(item_COUNT!=haba_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Susunod(void){int item_COUNT=0;while(FIND_pagpasok[item_COUNT])item_COUNT++;if(!item_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=haba_VALUE;순번++){int data_posisyon=(INDEX_VALUE+순번)%(haba_VALUE?haba_VALUE:1),안쪽순번=0;while(안쪽순번<item_COUNT&&data_posisyon+안쪽순번<haba_VALUE&&SMS[data_posisyon+안쪽순번]==(unsigned char)FIND_pagpasok[안쪽순번])안쪽순번++;if(안쪽순번==item_COUNT){INDEX_VALUE=data_posisyon;알림문="Match";return;}}알림문="Pattern not found";}
static int prompt(int kategorya_VALUE){
    int item_COUNT=0;utos[0]=0;
    for(;;){ilipat_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_data(kategorya_VALUE);글내보내기(utos);출력비우기();tulong_kategorya=kategorya_VALUE;int 셋째순번=누름값();tulong_kategorya=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(item_COUNT){item_COUNT--;while(item_COUNT>0&&((unsigned char)utos[item_COUNT]&192)==128)item_COUNT--;utos[item_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&item_COUNT<120){utos[item_COUNT++]=셋째순번;utos[item_COUNT]=0;}
    }
    if(kategorya_VALUE=='/'){for(int 순번=0;순번<=item_COUNT;순번++)FIND_pagpasok[순번]=utos[순번];FIND_Susunod();return 0;}
    if(같은지(utos,"q!"))return 1;
    if(같은지(utos,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(utos,"wq")||같은지(utos,"x"))return Store_VALUE();
    if(같은지(utos,"w")){Store_VALUE();return 0;}
    if(utos[0]=='w'&&utos[1]==' '){int 순번=2;while(utos[순번]==' ')순번++;int sukat_82232621=item_COUNT-순번;if(sukat_82232621<1||sukat_82232621>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<sukat_82232621;안쪽순번++)file_pagpasok_pangalan[안쪽순번]=utos[순번+안쪽순번];file_pagpasok_pangalan[sukat_82232621]=0;Store_VALUE();return 0;}
    int linya=0;for(int 순번=0;순번<item_COUNT;순번++){if(utos[순번]<'0'||utos[순번]>'9'){linya=0;break;}linya=linya*10+utos[순번]-'0';if(linya>16384){linya=0;break;}}
    if(linya){INDEX_VALUE=0;while(--linya&&INDEX_VALUE<haba_VALUE){INDEX_VALUE=tapusin_OFFSET(INDEX_VALUE);if(INDEX_VALUE<haba_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Start_gumagamit_app(int 무시값){
    (void)무시값;if(gumagamit_argumento_COUNT()!=1||gumagamit_argumento(0,file_pagpasok_pangalan,sizeof(file_pagpasok_pangalan))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int file_hawakán=buksan_file(file_pagpasok_pangalan,mababasa_lamang_VALUE,0);
    if(file_hawakán>=0){int item_COUNT=file_sukat(file_hawakán);if(item_COUNT<0||item_COUNT>편집용량){isara_file(file_hawakán);return 1;}haba_VALUE=파일자료읽기(file_hawakán,SMS,item_COUNT);isara_file(file_hawakán);if(haba_VALUE!=item_COUNT)return 1;for(int 순번=0;순번<haba_VALUE;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,lumabas_app=0;
    while(!lumabas_app){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){archive(-1);continue;}if(셋째순번==1002){archive(1);continue;}if(셋째순번==1003){INDEX_VALUE=Susunod_item(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=run(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=tapusin_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)archive(셋째순번==1008?-1:1);continue;}
        if(magsingit_isingit){
            if(셋째순번==27||셋째순번==3){magsingit_isingit=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<haba_VALUE)바이트지우기(INDEX_VALUE,Susunod_item(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int item_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!item_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<item_COUNT;순번++){int character_code=누름값();if(character_code<128||character_code>191){pending_key=character_code;유효함=0;break;}SECOND_VALUE[순번]=character_code;}
                if(유효함)덧붙이기(SECOND_VALUE,item_COUNT);
            }continue;
        }
        if(앞부분){int data_posisyon=앞부분;앞부분=0;if(data_posisyon=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(data_posisyon=='Z'&&셋째순번=='Z'){lumabas_app=Store_VALUE();continue;}if((data_posisyon=='d'&&셋째순번=='d')||(data_posisyon=='y'&&셋째순번=='y')){int 첫째값=run(INDEX_VALUE),SECOND_VALUE=tapusin_OFFSET(INDEX_VALUE);if(SECOND_VALUE<haba_VALUE)SECOND_VALUE++;gumawa_ng_kopya_haba=SECOND_VALUE-첫째값;for(int 순번=0;순번<gumawa_ng_kopya_haba;순번++)복사자료[순번]=SMS[첫째값+순번];if(data_posisyon=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){magsingit_isingit=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<tapusin_OFFSET(INDEX_VALUE))INDEX_VALUE=Susunod_item(INDEX_VALUE);magsingit_isingit=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=run(INDEX_VALUE);magsingit_isingit=1;continue;}if(셋째순번=='A'){INDEX_VALUE=tapusin_OFFSET(INDEX_VALUE);magsingit_isingit=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char linya_tapusin='\n';INDEX_VALUE=셋째순번=='o'?tapusin_OFFSET(INDEX_VALUE):run(INDEX_VALUE);if(덧붙이기(&linya_tapusin,1)){if(셋째순번=='O')INDEX_VALUE--;magsingit_isingit=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Susunod_item(INDEX_VALUE);continue;}if(셋째순번=='j'){archive(1);continue;}if(셋째순번=='k'){archive(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=run(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=tapusin_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=run(haba_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<haba_VALUE)바이트지우기(INDEX_VALUE,Susunod_item(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&gumawa_ng_kopya_haba){INDEX_VALUE=tapusin_OFFSET(INDEX_VALUE);if(INDEX_VALUE<haba_VALUE)INDEX_VALUE++;덧붙이기(복사자료,gumawa_ng_kopya_haba);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=SMS[순번];SMS[순번]=i_undo_data[순번];i_undo_data[순번]=SECOND_VALUE;}int item_COUNT=haba_VALUE;haba_VALUE=i_undo_haba;i_undo_haba=item_COUNT;item_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=item_COUNT;item_COUNT=변경됨;변경됨=i_undo_Mga_Pagbabago;i_undo_Mga_Pagbabago=item_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){lumabas_app=prompt(셋째순번);continue;}if(셋째순번=='n'){FIND_Susunod();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
