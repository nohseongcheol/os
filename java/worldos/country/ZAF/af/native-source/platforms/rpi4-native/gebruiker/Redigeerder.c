/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Teks[편집용량],ontdoen_data[편집용량],복사자료[편집용량],maatreël_data[1024];
static int lengte_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,voeg_in,ontdoen_lengte,위쪽,ontdoen_Veranderings,되돌림있음,geval_lengte,사용량,COLUMNS=68,ry_COUNT=19;
static char lêer_inskrywing_naam[64],Opdrag[128],FIND_inskrywing[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned hangend_Sleutel;
static int hulp_kategorie,stand_foto,stand_tou;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)maatreël_data,사용량,0,0,0);사용량=0;}}
static void greep_data(unsigned karakterkode){if(stand_foto){if((karakterkode&192)!=128){stand_tou+=karakterkode>=196?2:1;}if(stand_tou>=COLUMNS)return;}if(사용량==(int)sizeof(maatreël_data))출력비우기();maatreël_data[사용량++]=karakterkode;}
static void 글내보내기(const char *string_data){while(*string_data)greep_data((unsigned char)*string_data++);}
static void 수치(unsigned item_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+item_COUNT%10;item_COUNT/=10;}while(item_COUNT);while(순번)greep_data(SECOND_VALUE[--순번]);}
static void skuif_VALUE(int ry_plaas,int kolom_plaas){글내보내기("\033[");수치(ry_plaas);greep_data(';');수치(kolom_plaas);greep_data('H');}
static int 이전항목(int data_plaas){if(data_plaas){data_plaas--;while(data_plaas>0&&(Teks[data_plaas]&192)==128)data_plaas--;}return data_plaas;}
static int Volgende_item(int data_plaas){if(data_plaas<lengte_VALUE){data_plaas++;while(data_plaas<lengte_VALUE&&(Teks[data_plaas]&192)==128)data_plaas++;}return data_plaas;}
static int Loop(int data_plaas){while(data_plaas>0&&Teks[data_plaas-1]!='\n')data_plaas--;return data_plaas;}
static int beëindig_OFFSET(int data_plaas){while(data_plaas<lengte_VALUE&&Teks[data_plaas]!='\n')data_plaas++;return data_plaas;}
static int 너비(unsigned karakterkode){return karakterkode>=196?2:1;}
static int kolom(int data_plaas){int karakterkode=0;for(int 순번=Loop(data_plaas);순번<data_plaas;순번=Volgende_item(순번))karakterkode+=Teks[순번]=='\t'?4-karakterkode%4:너비(Teks[순번]);return karakterkode;}
static void kontrolepunt(void){for(int 순번=0;순번<lengte_VALUE;순번++)ontdoen_data[순번]=Teks[순번];ontdoen_lengte=lengte_VALUE;위쪽=INDEX_VALUE;ontdoen_Veranderings=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrolepunt();for(int 순번=도착위치;순번<lengte_VALUE;순번++)Teks[출발위치+순번-도착위치]=Teks[순번];lengte_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *string_data,int item_COUNT){if(item_COUNT>편집용량-lengte_VALUE){알림문="File full (16384 bytes)";return 0;}kontrolepunt();for(int 순번=lengte_VALUE-1;순번>=INDEX_VALUE;순번--)Teks[순번+item_COUNT]=Teks[순번];for(int 순번=0;순번<item_COUNT;순번++)Teks[INDEX_VALUE+순번]=string_data[순번];lengte_VALUE+=item_COUNT;INDEX_VALUE+=item_COUNT;변경됨=1;return 1;}
static void Vertikaal(int 차이){int kolom_plaas=kolom(INDEX_VALUE),data_plaas=Loop(INDEX_VALUE);if(차이<0){if(!data_plaas)return;data_plaas=Loop(data_plaas-1);}else{data_plaas=beëindig_OFFSET(data_plaas);if(data_plaas==lengte_VALUE)return;data_plaas++;}int karakterkode=0;while(data_plaas<lengte_VALUE&&Teks[data_plaas]!='\n'&&karakterkode<kolom_plaas){karakterkode+=Teks[data_plaas]=='\t'?4-karakterkode%4:너비(Teks[data_plaas]);data_plaas=Volgende_item(data_plaas);}INDEX_VALUE=data_plaas;}
static void 화면그리기(void){
    if(INDEX_VALUE>lengte_VALUE)INDEX_VALUE=lengte_VALUE;if(맨위>INDEX_VALUE)맨위=Loop(INDEX_VALUE);맨위=Loop(맨위);
    int ry_plaas=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Teks[순번]=='\n')ry_plaas++;
    while(ry_plaas>=ry_COUNT-1){맨위=beëindig_OFFSET(맨위);if(맨위<lengte_VALUE)맨위++;ry_plaas--;}
    int kolom_plaas=kolom(INDEX_VALUE);if(kolom_plaas<왼쪽)왼쪽=kolom_plaas;if(kolom_plaas-왼쪽>=COLUMNS-1)왼쪽=kolom_plaas-COLUMNS+2;
    글내보내기("\033[?25l");int data_plaas=맨위;
    for(int 반환값=0;반환값<ry_COUNT-1;반환값++){
        skuif_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int karakterkode=0,그려진상태=0;
        if(data_plaas>=lengte_VALUE&&반환값>ry_plaas){글내보내기("\033[90m~\033[0m");continue;}
        while(data_plaas<lengte_VALUE&&Teks[data_plaas]!='\n'){
            int Volgende_OFFSET=Volgende_item(data_plaas),너비값=Teks[data_plaas]=='\t'?4-karakterkode%4:너비(Teks[data_plaas]);
            if(karakterkode>=왼쪽&&karakterkode-왼쪽+너비값<COLUMNS){
                if(Teks[data_plaas]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)greep_data(' ');}else if(Teks[data_plaas]<32||Teks[data_plaas]==127){greep_data('?');}else for(int 안쪽순번=data_plaas;안쪽순번<Volgende_OFFSET;안쪽순번++)greep_data(Teks[안쪽순번]);그려진상태+=너비값;
            }karakterkode+=너비값;data_plaas=Volgende_OFFSET;
        }
        (void)그려진상태;if(data_plaas<lengte_VALUE)data_plaas++;
    }
    skuif_VALUE(ry_COUNT,1);글내보내기("\033[7m\033[2K");stand_foto=1;stand_tou=0;글내보내기(voeg_in?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(lêer_inskrywing_naam[이름바이트수]&&이름바이트수<30)greep_data(lêer_inskrywing_naam[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int lyn=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Teks[순번]=='\n')lyn++;수치(lyn);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int item_COUNT=0;글내보내기(" | ");while(알림문[item_COUNT]&&item_COUNT<20)greep_data(알림문[item_COUNT++]);}
    stand_foto=0;글내보내기("\033[0m");skuif_VALUE(ry_plaas+1,kolom_plaas-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(hangend_Sleutel){int 셋째순번=hangend_Sleutel;hangend_Sleutel=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Grootte=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Grootte&65535)||ry_COUNT!=(int)(Grootte>>16)){
            COLUMNS=Grootte&65535;ry_COUNT=Grootte>>16;화면그리기();
            if(hulp_kategorie){skuif_VALUE(ry_COUNT,1);글내보내기("\033[0m\033[2K");greep_data(hulp_kategorie);글내보내기(Opdrag);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){hangend_Sleutel=셋째순번;return 27;}
    int item_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){item_COUNT=item_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return item_COUNT==3?1007:item_COUNT==5?1008:item_COUNT==6?1009:item_COUNT==1?1005:item_COUNT==4?1006:27;return 27;}return 27;
}
static int bêre_VALUE(void){
    int lêer_handvatsel=skep_lêer(lêer_inskrywing_naam,lees_skryf|없으면만들기|내용비우기,0600);if(lêer_handvatsel<0){알림문="Cannot open for save";return 0;}
    intptr_t item_COUNT=skryf_lêer_data(lêer_handvatsel,Teks,lengte_VALUE);sluit_lêer(lêer_handvatsel);if(item_COUNT!=lengte_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Volgende(void){int item_COUNT=0;while(FIND_inskrywing[item_COUNT])item_COUNT++;if(!item_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=lengte_VALUE;순번++){int data_plaas=(INDEX_VALUE+순번)%(lengte_VALUE?lengte_VALUE:1),안쪽순번=0;while(안쪽순번<item_COUNT&&data_plaas+안쪽순번<lengte_VALUE&&Teks[data_plaas+안쪽순번]==(unsigned char)FIND_inskrywing[안쪽순번])안쪽순번++;if(안쪽순번==item_COUNT){INDEX_VALUE=data_plaas;알림문="Match";return;}}알림문="Pattern not found";}
static int por(int kategorie_VALUE){
    int item_COUNT=0;Opdrag[0]=0;
    for(;;){skuif_VALUE(ry_COUNT,1);글내보내기("\033[0m\033[2K");greep_data(kategorie_VALUE);글내보내기(Opdrag);출력비우기();hulp_kategorie=kategorie_VALUE;int 셋째순번=누름값();hulp_kategorie=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(item_COUNT){item_COUNT--;while(item_COUNT>0&&((unsigned char)Opdrag[item_COUNT]&192)==128)item_COUNT--;Opdrag[item_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&item_COUNT<120){Opdrag[item_COUNT++]=셋째순번;Opdrag[item_COUNT]=0;}
    }
    if(kategorie_VALUE=='/'){for(int 순번=0;순번<=item_COUNT;순번++)FIND_inskrywing[순번]=Opdrag[순번];FIND_Volgende();return 0;}
    if(같은지(Opdrag,"q!"))return 1;
    if(같은지(Opdrag,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Opdrag,"wq")||같은지(Opdrag,"x"))return bêre_VALUE();
    if(같은지(Opdrag,"w")){bêre_VALUE();return 0;}
    if(Opdrag[0]=='w'&&Opdrag[1]==' '){int 순번=2;while(Opdrag[순번]==' ')순번++;int Grootte=item_COUNT-순번;if(Grootte<1||Grootte>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Grootte;안쪽순번++)lêer_inskrywing_naam[안쪽순번]=Opdrag[순번+안쪽순번];lêer_inskrywing_naam[Grootte]=0;bêre_VALUE();return 0;}
    int lyn=0;for(int 순번=0;순번<item_COUNT;순번++){if(Opdrag[순번]<'0'||Opdrag[순번]>'9'){lyn=0;break;}lyn=lyn*10+Opdrag[순번]-'0';if(lyn>16384){lyn=0;break;}}
    if(lyn){INDEX_VALUE=0;while(--lyn&&INDEX_VALUE<lengte_VALUE){INDEX_VALUE=beëindig_OFFSET(INDEX_VALUE);if(INDEX_VALUE<lengte_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int BEGIN_gebruiker_program(int 무시값){
    (void)무시값;if(gebruiker_argument_COUNT()!=1||gebruiker_argument(0,lêer_inskrywing_naam,sizeof(lêer_inskrywing_naam))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int lêer_handvatsel=skep_lêer(lêer_inskrywing_naam,leesalleen_VALUE,0);
    if(lêer_handvatsel>=0){int item_COUNT=lêer_verstel(lêer_handvatsel);if(item_COUNT<0||item_COUNT>편집용량){sluit_lêer(lêer_handvatsel);return 1;}lengte_VALUE=파일자료읽기(lêer_handvatsel,Teks,item_COUNT);sluit_lêer(lêer_handvatsel);if(lengte_VALUE!=item_COUNT)return 1;for(int 순번=0;순번<lengte_VALUE;순번++)if(!Teks[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ry_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,gaan_uit_program=0;
    while(!gaan_uit_program){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Vertikaal(-1);continue;}if(셋째순번==1002){Vertikaal(1);continue;}if(셋째순번==1003){INDEX_VALUE=Volgende_item(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Loop(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=beëindig_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ry_COUNT-2;순번++)Vertikaal(셋째순번==1008?-1:1);continue;}
        if(voeg_in){
            if(셋째순번==27||셋째순번==3){voeg_in=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<lengte_VALUE)바이트지우기(INDEX_VALUE,Volgende_item(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int item_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!item_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<item_COUNT;순번++){int karakterkode=누름값();if(karakterkode<128||karakterkode>191){hangend_Sleutel=karakterkode;유효함=0;break;}SECOND_VALUE[순번]=karakterkode;}
                if(유효함)덧붙이기(SECOND_VALUE,item_COUNT);
            }continue;
        }
        if(앞부분){int data_plaas=앞부분;앞부분=0;if(data_plaas=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(data_plaas=='Z'&&셋째순번=='Z'){gaan_uit_program=bêre_VALUE();continue;}if((data_plaas=='d'&&셋째순번=='d')||(data_plaas=='y'&&셋째순번=='y')){int 첫째값=Loop(INDEX_VALUE),SECOND_VALUE=beëindig_OFFSET(INDEX_VALUE);if(SECOND_VALUE<lengte_VALUE)SECOND_VALUE++;geval_lengte=SECOND_VALUE-첫째값;for(int 순번=0;순번<geval_lengte;순번++)복사자료[순번]=Teks[첫째값+순번];if(data_plaas=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){voeg_in=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<beëindig_OFFSET(INDEX_VALUE))INDEX_VALUE=Volgende_item(INDEX_VALUE);voeg_in=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Loop(INDEX_VALUE);voeg_in=1;continue;}if(셋째순번=='A'){INDEX_VALUE=beëindig_OFFSET(INDEX_VALUE);voeg_in=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char lyn_beëindig='\n';INDEX_VALUE=셋째순번=='o'?beëindig_OFFSET(INDEX_VALUE):Loop(INDEX_VALUE);if(덧붙이기(&lyn_beëindig,1)){if(셋째순번=='O')INDEX_VALUE--;voeg_in=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Volgende_item(INDEX_VALUE);continue;}if(셋째순번=='j'){Vertikaal(1);continue;}if(셋째순번=='k'){Vertikaal(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Loop(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=beëindig_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Loop(lengte_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<lengte_VALUE)바이트지우기(INDEX_VALUE,Volgende_item(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&geval_lengte){INDEX_VALUE=beëindig_OFFSET(INDEX_VALUE);if(INDEX_VALUE<lengte_VALUE)INDEX_VALUE++;덧붙이기(복사자료,geval_lengte);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=Teks[순번];Teks[순번]=ontdoen_data[순번];ontdoen_data[순번]=SECOND_VALUE;}int item_COUNT=lengte_VALUE;lengte_VALUE=ontdoen_lengte;ontdoen_lengte=item_COUNT;item_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=item_COUNT;item_COUNT=변경됨;변경됨=ontdoen_Veranderings;ontdoen_Veranderings=item_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){gaan_uit_program=por(셋째순번);continue;}if(셋째순번=='n'){FIND_Volgende();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
