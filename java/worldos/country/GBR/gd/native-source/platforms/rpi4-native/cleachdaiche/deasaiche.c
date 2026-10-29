/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char SMS[편집용량],neo_dhèan_dàta[편집용량],복사자료[편집용량],tomhas_dàta[1024];
static int faid_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,cuir_a_steach,neo_dhèan_faid,위쪽,neo_dhèan_atharraichean,되돌림있음,ionstans_faid,사용량,COLUMNS=68,ROW_COUNT=19;
static char faidhle_cur_a_steach_ainm[64],àithne[128],FIND_cur_a_steach[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned ri_dhèiligeadh_Iuchair;
static int cuideachadh_roinn_seòrsa,cor_IMAGE,cor_ciutha;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)tomhas_dàta,사용량,0,0,0);사용량=0;}}
static void baidht_dàta(unsigned còd_a_charactair){if(cor_IMAGE){if((còd_a_charactair&192)!=128){cor_ciutha+=còd_a_charactair>=196?2:1;}if(cor_ciutha>=COLUMNS)return;}if(사용량==(int)sizeof(tomhas_dàta))출력비우기();tomhas_dàta[사용량++]=còd_a_charactair;}
static void 글내보내기(const char *sreang_dàta){while(*sreang_dàta)baidht_dàta((unsigned char)*sreang_dàta++);}
static void 수치(unsigned nì_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+nì_COUNT%10;nì_COUNT/=10;}while(nì_COUNT);while(순번)baidht_dàta(SECOND_VALUE[--순번]);}
static void gluais_VALUE(int ROW_suidhich,int colbh_suidhich){글내보내기("\033[");수치(ROW_suidhich);baidht_dàta(';');수치(colbh_suidhich);baidht_dàta('H');}
static int 이전항목(int dàta_suidhich){if(dàta_suidhich){dàta_suidhich--;while(dàta_suidhich>0&&(SMS[dàta_suidhich]&192)==128)dàta_suidhich--;}return dàta_suidhich;}
static int air_adhart_nì(int dàta_suidhich){if(dàta_suidhich<faid_VALUE){dàta_suidhich++;while(dàta_suidhich<faid_VALUE&&(SMS[dàta_suidhich]&192)==128)dàta_suidhich++;}return dàta_suidhich;}
static int ruith(int dàta_suidhich){while(dàta_suidhich>0&&SMS[dàta_suidhich-1]!='\n')dàta_suidhich--;return dàta_suidhich;}
static int crìochnaich_OFFSET(int dàta_suidhich){while(dàta_suidhich<faid_VALUE&&SMS[dàta_suidhich]!='\n')dàta_suidhich++;return dàta_suidhich;}
static int 너비(unsigned còd_a_charactair){return còd_a_charactair>=196?2:1;}
static int colbh(int dàta_suidhich){int còd_a_charactair=0;for(int 순번=ruith(dàta_suidhich);순번<dàta_suidhich;순번=air_adhart_nì(순번))còd_a_charactair+=SMS[순번]=='\t'?4-còd_a_charactair%4:너비(SMS[순번]);return còd_a_charactair;}
static void àite_dearbhaidh(void){for(int 순번=0;순번<faid_VALUE;순번++)neo_dhèan_dàta[순번]=SMS[순번];neo_dhèan_faid=faid_VALUE;위쪽=INDEX_VALUE;neo_dhèan_atharraichean=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){àite_dearbhaidh();for(int 순번=도착위치;순번<faid_VALUE;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];faid_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *sreang_dàta,int nì_COUNT){if(nì_COUNT>편집용량-faid_VALUE){알림문="File full (16384 bytes)";return 0;}àite_dearbhaidh();for(int 순번=faid_VALUE-1;순번>=INDEX_VALUE;순번--)SMS[순번+nì_COUNT]=SMS[순번];for(int 순번=0;순번<nì_COUNT;순번++)SMS[INDEX_VALUE+순번]=sreang_dàta[순번];faid_VALUE+=nì_COUNT;INDEX_VALUE+=nì_COUNT;변경됨=1;return 1;}
static void inghearach(int 차이){int colbh_suidhich=colbh(INDEX_VALUE),dàta_suidhich=ruith(INDEX_VALUE);if(차이<0){if(!dàta_suidhich)return;dàta_suidhich=ruith(dàta_suidhich-1);}else{dàta_suidhich=crìochnaich_OFFSET(dàta_suidhich);if(dàta_suidhich==faid_VALUE)return;dàta_suidhich++;}int còd_a_charactair=0;while(dàta_suidhich<faid_VALUE&&SMS[dàta_suidhich]!='\n'&&còd_a_charactair<colbh_suidhich){còd_a_charactair+=SMS[dàta_suidhich]=='\t'?4-còd_a_charactair%4:너비(SMS[dàta_suidhich]);dàta_suidhich=air_adhart_nì(dàta_suidhich);}INDEX_VALUE=dàta_suidhich;}
static void 화면그리기(void){
    if(INDEX_VALUE>faid_VALUE)INDEX_VALUE=faid_VALUE;if(맨위>INDEX_VALUE)맨위=ruith(INDEX_VALUE);맨위=ruith(맨위);
    int ROW_suidhich=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')ROW_suidhich++;
    while(ROW_suidhich>=ROW_COUNT-1){맨위=crìochnaich_OFFSET(맨위);if(맨위<faid_VALUE)맨위++;ROW_suidhich--;}
    int colbh_suidhich=colbh(INDEX_VALUE);if(colbh_suidhich<왼쪽)왼쪽=colbh_suidhich;if(colbh_suidhich-왼쪽>=COLUMNS-1)왼쪽=colbh_suidhich-COLUMNS+2;
    글내보내기("\033[?25l");int dàta_suidhich=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        gluais_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int còd_a_charactair=0,그려진상태=0;
        if(dàta_suidhich>=faid_VALUE&&반환값>ROW_suidhich){글내보내기("\033[90m~\033[0m");continue;}
        while(dàta_suidhich<faid_VALUE&&SMS[dàta_suidhich]!='\n'){
            int air_adhart_OFFSET=air_adhart_nì(dàta_suidhich),너비값=SMS[dàta_suidhich]=='\t'?4-còd_a_charactair%4:너비(SMS[dàta_suidhich]);
            if(còd_a_charactair>=왼쪽&&còd_a_charactair-왼쪽+너비값<COLUMNS){
                if(SMS[dàta_suidhich]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)baidht_dàta(' ');}else if(SMS[dàta_suidhich]<32||SMS[dàta_suidhich]==127){baidht_dàta('?');}else for(int 안쪽순번=dàta_suidhich;안쪽순번<air_adhart_OFFSET;안쪽순번++)baidht_dàta(SMS[안쪽순번]);그려진상태+=너비값;
            }còd_a_charactair+=너비값;dàta_suidhich=air_adhart_OFFSET;
        }
        (void)그려진상태;if(dàta_suidhich<faid_VALUE)dàta_suidhich++;
    }
    gluais_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");cor_IMAGE=1;cor_ciutha=0;글내보내기(cuir_a_steach?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(faidhle_cur_a_steach_ainm[이름바이트수]&&이름바이트수<30)baidht_dàta(faidhle_cur_a_steach_ainm[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int loidhne=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')loidhne++;수치(loidhne);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int nì_COUNT=0;글내보내기(" | ");while(알림문[nì_COUNT]&&nì_COUNT<20)baidht_dàta(알림문[nì_COUNT++]);}
    cor_IMAGE=0;글내보내기("\033[0m");gluais_VALUE(ROW_suidhich+1,colbh_suidhich-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(ri_dhèiligeadh_Iuchair){int 셋째순번=ri_dhèiligeadh_Iuchair;ri_dhèiligeadh_Iuchair=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned atharraich_am_meud=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(atharraich_am_meud&65535)||ROW_COUNT!=(int)(atharraich_am_meud>>16)){
            COLUMNS=atharraich_am_meud&65535;ROW_COUNT=atharraich_am_meud>>16;화면그리기();
            if(cuideachadh_roinn_seòrsa){gluais_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");baidht_dàta(cuideachadh_roinn_seòrsa);글내보내기(àithne);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){ri_dhèiligeadh_Iuchair=셋째순번;return 27;}
    int nì_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){nì_COUNT=nì_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return nì_COUNT==3?1007:nì_COUNT==5?1008:nì_COUNT==6?1009:nì_COUNT==1?1005:nì_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int faidhle_làmhrachan=fosgail_faidhle(faidhle_cur_a_steach_ainm,so_leughte_so_sgrìobhte|없으면만들기|내용비우기,0600);if(faidhle_làmhrachan<0){알림문="Cannot open for save";return 0;}
    intptr_t nì_COUNT=sgrìobh_faidhle_dàta(faidhle_làmhrachan,SMS,faid_VALUE);dùin_faidhle(faidhle_làmhrachan);if(nì_COUNT!=faid_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_air_adhart(void){int nì_COUNT=0;while(FIND_cur_a_steach[nì_COUNT])nì_COUNT++;if(!nì_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=faid_VALUE;순번++){int dàta_suidhich=(INDEX_VALUE+순번)%(faid_VALUE?faid_VALUE:1),안쪽순번=0;while(안쪽순번<nì_COUNT&&dàta_suidhich+안쪽순번<faid_VALUE&&SMS[dàta_suidhich+안쪽순번]==(unsigned char)FIND_cur_a_steach[안쪽순번])안쪽순번++;if(안쪽순번==nì_COUNT){INDEX_VALUE=dàta_suidhich;알림문="Match";return;}}알림문="Pattern not found";}
static int brodadh(int roinn_seòrsa_VALUE){
    int nì_COUNT=0;àithne[0]=0;
    for(;;){gluais_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");baidht_dàta(roinn_seòrsa_VALUE);글내보내기(àithne);출력비우기();cuideachadh_roinn_seòrsa=roinn_seòrsa_VALUE;int 셋째순번=누름값();cuideachadh_roinn_seòrsa=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(nì_COUNT){nì_COUNT--;while(nì_COUNT>0&&((unsigned char)àithne[nì_COUNT]&192)==128)nì_COUNT--;àithne[nì_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&nì_COUNT<120){àithne[nì_COUNT++]=셋째순번;àithne[nì_COUNT]=0;}
    }
    if(roinn_seòrsa_VALUE=='/'){for(int 순번=0;순번<=nì_COUNT;순번++)FIND_cur_a_steach[순번]=àithne[순번];FIND_air_adhart();return 0;}
    if(같은지(àithne,"q!"))return 1;
    if(같은지(àithne,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(àithne,"wq")||같은지(àithne,"x"))return Store_VALUE();
    if(같은지(àithne,"w")){Store_VALUE();return 0;}
    if(àithne[0]=='w'&&àithne[1]==' '){int 순번=2;while(àithne[순번]==' ')순번++;int atharraich_am_meud=nì_COUNT-순번;if(atharraich_am_meud<1||atharraich_am_meud>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<atharraich_am_meud;안쪽순번++)faidhle_cur_a_steach_ainm[안쪽순번]=àithne[순번+안쪽순번];faidhle_cur_a_steach_ainm[atharraich_am_meud]=0;Store_VALUE();return 0;}
    int loidhne=0;for(int 순번=0;순번<nì_COUNT;순번++){if(àithne[순번]<'0'||àithne[순번]>'9'){loidhne=0;break;}loidhne=loidhne*10+àithne[순번]-'0';if(loidhne>16384){loidhne=0;break;}}
    if(loidhne){INDEX_VALUE=0;while(--loidhne&&INDEX_VALUE<faid_VALUE){INDEX_VALUE=crìochnaich_OFFSET(INDEX_VALUE);if(INDEX_VALUE<faid_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Start_cleachdaiche_ap(int 무시값){
    (void)무시값;if(cleachdaiche_argamaid_COUNT()!=1||cleachdaiche_argamaid(0,faidhle_cur_a_steach_ainm,sizeof(faidhle_cur_a_steach_ainm))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int faidhle_làmhrachan=fosgail_faidhle(faidhle_cur_a_steach_ainm,ri_leughadh_a_mhàin_VALUE,0);
    if(faidhle_làmhrachan>=0){int nì_COUNT=faidhle_atharraich_am_meud(faidhle_làmhrachan);if(nì_COUNT<0||nì_COUNT>편집용량){dùin_faidhle(faidhle_làmhrachan);return 1;}faid_VALUE=파일자료읽기(faidhle_làmhrachan,SMS,nì_COUNT);dùin_faidhle(faidhle_làmhrachan);if(faid_VALUE!=nì_COUNT)return 1;for(int 순번=0;순번<faid_VALUE;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,fàg_an_seo_ap=0;
    while(!fàg_an_seo_ap){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){inghearach(-1);continue;}if(셋째순번==1002){inghearach(1);continue;}if(셋째순번==1003){INDEX_VALUE=air_adhart_nì(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=ruith(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=crìochnaich_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)inghearach(셋째순번==1008?-1:1);continue;}
        if(cuir_a_steach){
            if(셋째순번==27||셋째순번==3){cuir_a_steach=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<faid_VALUE)바이트지우기(INDEX_VALUE,air_adhart_nì(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int nì_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!nì_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<nì_COUNT;순번++){int còd_a_charactair=누름값();if(còd_a_charactair<128||còd_a_charactair>191){ri_dhèiligeadh_Iuchair=còd_a_charactair;유효함=0;break;}SECOND_VALUE[순번]=còd_a_charactair;}
                if(유효함)덧붙이기(SECOND_VALUE,nì_COUNT);
            }continue;
        }
        if(앞부분){int dàta_suidhich=앞부분;앞부분=0;if(dàta_suidhich=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(dàta_suidhich=='Z'&&셋째순번=='Z'){fàg_an_seo_ap=Store_VALUE();continue;}if((dàta_suidhich=='d'&&셋째순번=='d')||(dàta_suidhich=='y'&&셋째순번=='y')){int 첫째값=ruith(INDEX_VALUE),SECOND_VALUE=crìochnaich_OFFSET(INDEX_VALUE);if(SECOND_VALUE<faid_VALUE)SECOND_VALUE++;ionstans_faid=SECOND_VALUE-첫째값;for(int 순번=0;순번<ionstans_faid;순번++)복사자료[순번]=SMS[첫째값+순번];if(dàta_suidhich=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){cuir_a_steach=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<crìochnaich_OFFSET(INDEX_VALUE))INDEX_VALUE=air_adhart_nì(INDEX_VALUE);cuir_a_steach=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=ruith(INDEX_VALUE);cuir_a_steach=1;continue;}if(셋째순번=='A'){INDEX_VALUE=crìochnaich_OFFSET(INDEX_VALUE);cuir_a_steach=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char loidhne_crìochnaich='\n';INDEX_VALUE=셋째순번=='o'?crìochnaich_OFFSET(INDEX_VALUE):ruith(INDEX_VALUE);if(덧붙이기(&loidhne_crìochnaich,1)){if(셋째순번=='O')INDEX_VALUE--;cuir_a_steach=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=air_adhart_nì(INDEX_VALUE);continue;}if(셋째순번=='j'){inghearach(1);continue;}if(셋째순번=='k'){inghearach(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=ruith(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=crìochnaich_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=ruith(faid_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<faid_VALUE)바이트지우기(INDEX_VALUE,air_adhart_nì(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&ionstans_faid){INDEX_VALUE=crìochnaich_OFFSET(INDEX_VALUE);if(INDEX_VALUE<faid_VALUE)INDEX_VALUE++;덧붙이기(복사자료,ionstans_faid);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=SMS[순번];SMS[순번]=neo_dhèan_dàta[순번];neo_dhèan_dàta[순번]=SECOND_VALUE;}int nì_COUNT=faid_VALUE;faid_VALUE=neo_dhèan_faid;neo_dhèan_faid=nì_COUNT;nì_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=nì_COUNT;nì_COUNT=변경됨;변경됨=neo_dhèan_atharraichean;neo_dhèan_atharraichean=nì_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){fàg_an_seo_ap=brodadh(셋째순번);continue;}if(셋째순번=='n'){FIND_air_adhart();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
