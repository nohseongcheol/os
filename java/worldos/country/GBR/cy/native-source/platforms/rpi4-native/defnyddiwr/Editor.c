/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Testun[편집용량],dad_wneud_data[편집용량],복사자료[편집용량],mesur_data[1024];
static int hyd_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,mewnosod,dad_wneud_hyd,위쪽,dad_wneud_Newidiadau,되돌림있음,copïo_hyd,사용량,COLUMNS=68,ROW_COUNT=19;
static char ffeil_cofnod_enw[64],Gorchymyn[128],FIND_cofnod[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned yn_disgwyl_bysell;
static int help_ardal,cyflwr_llun,cyflwr_ciw;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)mesur_data,사용량,0,0,0);사용량=0;}}
static void beit_data(unsigned cod_nod){if(cyflwr_llun){if((cod_nod&192)!=128){cyflwr_ciw+=cod_nod>=196?2:1;}if(cyflwr_ciw>=COLUMNS)return;}if(사용량==(int)sizeof(mesur_data))출력비우기();mesur_data[사용량++]=cod_nod;}
static void 글내보내기(const char *testun_data){while(*testun_data)beit_data((unsigned char)*testun_data++);}
static void 수치(unsigned eitem_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+eitem_COUNT%10;eitem_COUNT/=10;}while(eitem_COUNT);while(순번)beit_data(SECOND_VALUE[--순번]);}
static void symud_VALUE(int ROW_safle,int COLUMN_safle){글내보내기("\033[");수치(ROW_safle);beit_data(';');수치(COLUMN_safle);beit_data('H');}
static int 이전항목(int data_safle){if(data_safle){data_safle--;while(data_safle>0&&(Testun[data_safle]&192)==128)data_safle--;}return data_safle;}
static int Nesaf_eitem(int data_safle){if(data_safle<hyd_VALUE){data_safle++;while(data_safle<hyd_VALUE&&(Testun[data_safle]&192)==128)data_safle++;}return data_safle;}
static int Gweithredu_2(int data_safle){while(data_safle>0&&Testun[data_safle-1]!='\n')data_safle--;return data_safle;}
static int gorffen_OFFSET(int data_safle){while(data_safle<hyd_VALUE&&Testun[data_safle]!='\n')data_safle++;return data_safle;}
static int 너비(unsigned cod_nod){return cod_nod>=196?2:1;}
static int COLUMN(int data_safle){int cod_nod=0;for(int 순번=Gweithredu_2(data_safle);순번<data_safle;순번=Nesaf_eitem(순번))cod_nod+=Testun[순번]=='\t'?4-cod_nod%4:너비(Testun[순번]);return cod_nod;}
static void pwynt_gwirio(void){for(int 순번=0;순번<hyd_VALUE;순번++)dad_wneud_data[순번]=Testun[순번];dad_wneud_hyd=hyd_VALUE;위쪽=INDEX_VALUE;dad_wneud_Newidiadau=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){pwynt_gwirio();for(int 순번=도착위치;순번<hyd_VALUE;순번++)Testun[출발위치+순번-도착위치]=Testun[순번];hyd_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *testun_data,int eitem_COUNT){if(eitem_COUNT>편집용량-hyd_VALUE){알림문="File full (16384 bytes)";return 0;}pwynt_gwirio();for(int 순번=hyd_VALUE-1;순번>=INDEX_VALUE;순번--)Testun[순번+eitem_COUNT]=Testun[순번];for(int 순번=0;순번<eitem_COUNT;순번++)Testun[INDEX_VALUE+순번]=testun_data[순번];hyd_VALUE+=eitem_COUNT;INDEX_VALUE+=eitem_COUNT;변경됨=1;return 1;}
static void Ar_i_fyny(int 차이){int COLUMN_safle=COLUMN(INDEX_VALUE),data_safle=Gweithredu_2(INDEX_VALUE);if(차이<0){if(!data_safle)return;data_safle=Gweithredu_2(data_safle-1);}else{data_safle=gorffen_OFFSET(data_safle);if(data_safle==hyd_VALUE)return;data_safle++;}int cod_nod=0;while(data_safle<hyd_VALUE&&Testun[data_safle]!='\n'&&cod_nod<COLUMN_safle){cod_nod+=Testun[data_safle]=='\t'?4-cod_nod%4:너비(Testun[data_safle]);data_safle=Nesaf_eitem(data_safle);}INDEX_VALUE=data_safle;}
static void 화면그리기(void){
    if(INDEX_VALUE>hyd_VALUE)INDEX_VALUE=hyd_VALUE;if(맨위>INDEX_VALUE)맨위=Gweithredu_2(INDEX_VALUE);맨위=Gweithredu_2(맨위);
    int ROW_safle=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Testun[순번]=='\n')ROW_safle++;
    while(ROW_safle>=ROW_COUNT-1){맨위=gorffen_OFFSET(맨위);if(맨위<hyd_VALUE)맨위++;ROW_safle--;}
    int COLUMN_safle=COLUMN(INDEX_VALUE);if(COLUMN_safle<왼쪽)왼쪽=COLUMN_safle;if(COLUMN_safle-왼쪽>=COLUMNS-1)왼쪽=COLUMN_safle-COLUMNS+2;
    글내보내기("\033[?25l");int data_safle=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        symud_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int cod_nod=0,그려진상태=0;
        if(data_safle>=hyd_VALUE&&반환값>ROW_safle){글내보내기("\033[90m~\033[0m");continue;}
        while(data_safle<hyd_VALUE&&Testun[data_safle]!='\n'){
            int Nesaf_OFFSET=Nesaf_eitem(data_safle),너비값=Testun[data_safle]=='\t'?4-cod_nod%4:너비(Testun[data_safle]);
            if(cod_nod>=왼쪽&&cod_nod-왼쪽+너비값<COLUMNS){
                if(Testun[data_safle]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)beit_data(' ');}else if(Testun[data_safle]<32||Testun[data_safle]==127){beit_data('?');}else for(int 안쪽순번=data_safle;안쪽순번<Nesaf_OFFSET;안쪽순번++)beit_data(Testun[안쪽순번]);그려진상태+=너비값;
            }cod_nod+=너비값;data_safle=Nesaf_OFFSET;
        }
        (void)그려진상태;if(data_safle<hyd_VALUE)data_safle++;
    }
    symud_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");cyflwr_llun=1;cyflwr_ciw=0;글내보내기(mewnosod?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(ffeil_cofnod_enw[이름바이트수]&&이름바이트수<30)beit_data(ffeil_cofnod_enw[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int llinell=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Testun[순번]=='\n')llinell++;수치(llinell);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int eitem_COUNT=0;글내보내기(" | ");while(알림문[eitem_COUNT]&&eitem_COUNT<20)beit_data(알림문[eitem_COUNT++]);}
    cyflwr_llun=0;글내보내기("\033[0m");symud_VALUE(ROW_safle+1,COLUMN_safle-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(yn_disgwyl_bysell){int 셋째순번=yn_disgwyl_bysell;yn_disgwyl_bysell=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Maint=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Maint&65535)||ROW_COUNT!=(int)(Maint>>16)){
            COLUMNS=Maint&65535;ROW_COUNT=Maint>>16;화면그리기();
            if(help_ardal){symud_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");beit_data(help_ardal);글내보내기(Gorchymyn);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){yn_disgwyl_bysell=셋째순번;return 27;}
    int eitem_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){eitem_COUNT=eitem_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return eitem_COUNT==3?1007:eitem_COUNT==5?1008:eitem_COUNT==6?1009:eitem_COUNT==1?1005:eitem_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int ffeil_dolen=agor_ffeil(ffeil_cofnod_enw,darllen_ysgrifennu|없으면만들기|내용비우기,0600);if(ffeil_dolen<0){알림문="Cannot open for save";return 0;}
    intptr_t eitem_COUNT=ysgrifennu_ffeil_data(ffeil_dolen,Testun,hyd_VALUE);cau_ffeil(ffeil_dolen);if(eitem_COUNT!=hyd_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Nesaf(void){int eitem_COUNT=0;while(FIND_cofnod[eitem_COUNT])eitem_COUNT++;if(!eitem_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=hyd_VALUE;순번++){int data_safle=(INDEX_VALUE+순번)%(hyd_VALUE?hyd_VALUE:1),안쪽순번=0;while(안쪽순번<eitem_COUNT&&data_safle+안쪽순번<hyd_VALUE&&Testun[data_safle+안쪽순번]==(unsigned char)FIND_cofnod[안쪽순번])안쪽순번++;if(안쪽순번==eitem_COUNT){INDEX_VALUE=data_safle;알림문="Match";return;}}알림문="Pattern not found";}
static int neges_1dd14da4(int ardal_VALUE){
    int eitem_COUNT=0;Gorchymyn[0]=0;
    for(;;){symud_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");beit_data(ardal_VALUE);글내보내기(Gorchymyn);출력비우기();help_ardal=ardal_VALUE;int 셋째순번=누름값();help_ardal=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(eitem_COUNT){eitem_COUNT--;while(eitem_COUNT>0&&((unsigned char)Gorchymyn[eitem_COUNT]&192)==128)eitem_COUNT--;Gorchymyn[eitem_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&eitem_COUNT<120){Gorchymyn[eitem_COUNT++]=셋째순번;Gorchymyn[eitem_COUNT]=0;}
    }
    if(ardal_VALUE=='/'){for(int 순번=0;순번<=eitem_COUNT;순번++)FIND_cofnod[순번]=Gorchymyn[순번];FIND_Nesaf();return 0;}
    if(같은지(Gorchymyn,"q!"))return 1;
    if(같은지(Gorchymyn,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Gorchymyn,"wq")||같은지(Gorchymyn,"x"))return Store_VALUE();
    if(같은지(Gorchymyn,"w")){Store_VALUE();return 0;}
    if(Gorchymyn[0]=='w'&&Gorchymyn[1]==' '){int 순번=2;while(Gorchymyn[순번]==' ')순번++;int Maint=eitem_COUNT-순번;if(Maint<1||Maint>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Maint;안쪽순번++)ffeil_cofnod_enw[안쪽순번]=Gorchymyn[순번+안쪽순번];ffeil_cofnod_enw[Maint]=0;Store_VALUE();return 0;}
    int llinell=0;for(int 순번=0;순번<eitem_COUNT;순번++){if(Gorchymyn[순번]<'0'||Gorchymyn[순번]>'9'){llinell=0;break;}llinell=llinell*10+Gorchymyn[순번]-'0';if(llinell>16384){llinell=0;break;}}
    if(llinell){INDEX_VALUE=0;while(--llinell&&INDEX_VALUE<hyd_VALUE){INDEX_VALUE=gorffen_OFFSET(INDEX_VALUE);if(INDEX_VALUE<hyd_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int START_defnyddiwr_Rhaglen(int 무시값){
    (void)무시값;if(defnyddiwr_arg_COUNT()!=1||defnyddiwr_arg(0,ffeil_cofnod_enw,sizeof(ffeil_cofnod_enw))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int ffeil_dolen=agor_ffeil(ffeil_cofnod_enw,darllen_yn_unig_VALUE,0);
    if(ffeil_dolen>=0){int eitem_COUNT=ffeil_newid_maint(ffeil_dolen);if(eitem_COUNT<0||eitem_COUNT>편집용량){cau_ffeil(ffeil_dolen);return 1;}hyd_VALUE=파일자료읽기(ffeil_dolen,Testun,eitem_COUNT);cau_ffeil(ffeil_dolen);if(hyd_VALUE!=eitem_COUNT)return 1;for(int 순번=0;순번<hyd_VALUE;순번++)if(!Testun[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,gadael_Rhaglen_55b3a1cd=0;
    while(!gadael_Rhaglen_55b3a1cd){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Ar_i_fyny(-1);continue;}if(셋째순번==1002){Ar_i_fyny(1);continue;}if(셋째순번==1003){INDEX_VALUE=Nesaf_eitem(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Gweithredu_2(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=gorffen_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Ar_i_fyny(셋째순번==1008?-1:1);continue;}
        if(mewnosod){
            if(셋째순번==27||셋째순번==3){mewnosod=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<hyd_VALUE)바이트지우기(INDEX_VALUE,Nesaf_eitem(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int eitem_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!eitem_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<eitem_COUNT;순번++){int cod_nod=누름값();if(cod_nod<128||cod_nod>191){yn_disgwyl_bysell=cod_nod;유효함=0;break;}SECOND_VALUE[순번]=cod_nod;}
                if(유효함)덧붙이기(SECOND_VALUE,eitem_COUNT);
            }continue;
        }
        if(앞부분){int data_safle=앞부분;앞부분=0;if(data_safle=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(data_safle=='Z'&&셋째순번=='Z'){gadael_Rhaglen_55b3a1cd=Store_VALUE();continue;}if((data_safle=='d'&&셋째순번=='d')||(data_safle=='y'&&셋째순번=='y')){int 첫째값=Gweithredu_2(INDEX_VALUE),SECOND_VALUE=gorffen_OFFSET(INDEX_VALUE);if(SECOND_VALUE<hyd_VALUE)SECOND_VALUE++;copïo_hyd=SECOND_VALUE-첫째값;for(int 순번=0;순번<copïo_hyd;순번++)복사자료[순번]=Testun[첫째값+순번];if(data_safle=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){mewnosod=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<gorffen_OFFSET(INDEX_VALUE))INDEX_VALUE=Nesaf_eitem(INDEX_VALUE);mewnosod=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Gweithredu_2(INDEX_VALUE);mewnosod=1;continue;}if(셋째순번=='A'){INDEX_VALUE=gorffen_OFFSET(INDEX_VALUE);mewnosod=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char llinell_gorffen='\n';INDEX_VALUE=셋째순번=='o'?gorffen_OFFSET(INDEX_VALUE):Gweithredu_2(INDEX_VALUE);if(덧붙이기(&llinell_gorffen,1)){if(셋째순번=='O')INDEX_VALUE--;mewnosod=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Nesaf_eitem(INDEX_VALUE);continue;}if(셋째순번=='j'){Ar_i_fyny(1);continue;}if(셋째순번=='k'){Ar_i_fyny(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Gweithredu_2(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=gorffen_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Gweithredu_2(hyd_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<hyd_VALUE)바이트지우기(INDEX_VALUE,Nesaf_eitem(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&copïo_hyd){INDEX_VALUE=gorffen_OFFSET(INDEX_VALUE);if(INDEX_VALUE<hyd_VALUE)INDEX_VALUE++;덧붙이기(복사자료,copïo_hyd);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=Testun[순번];Testun[순번]=dad_wneud_data[순번];dad_wneud_data[순번]=SECOND_VALUE;}int eitem_COUNT=hyd_VALUE;hyd_VALUE=dad_wneud_hyd;dad_wneud_hyd=eitem_COUNT;eitem_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=eitem_COUNT;eitem_COUNT=변경됨;변경됨=dad_wneud_Newidiadau;dad_wneud_Newidiadau=eitem_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){gadael_Rhaglen_55b3a1cd=neges_1dd14da4(셋째순번);continue;}if(셋째순번=='n'){FIND_Nesaf();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
