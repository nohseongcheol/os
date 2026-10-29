/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char SMS[편집용량],erġa_lura_data[편집용량],복사자료[편집용량],miżura_data[1024];
static int tul_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,daħħal,erġa_lura_tul,위쪽,erġa_lura_Bidliet,되돌림있음,kkopja_tul,사용량,COLUMNS=68,ROW_COUNT=19;
static char fajl_entrata_isem[64],kmand[128],sab_entrata[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned pendenti_tast;
static int għajnuna_kategorija,stat_IMAGE,stat_kju;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)miżura_data,사용량,0,0,0);사용량=0;}}
static void byte_data(unsigned kodiċi_tal_karattru){if(stat_IMAGE){if((kodiċi_tal_karattru&192)!=128){stat_kju+=kodiċi_tal_karattru>=196?2:1;}if(stat_kju>=COLUMNS)return;}if(사용량==(int)sizeof(miżura_data))출력비우기();miżura_data[사용량++]=kodiċi_tal_karattru;}
static void 글내보내기(const char *string_data){while(*string_data)byte_data((unsigned char)*string_data++);}
static void 수치(unsigned element_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+element_COUNT%10;element_COUNT/=10;}while(element_COUNT);while(순번)byte_data(SECOND_VALUE[--순번]);}
static void mexxi_VALUE(int ROW_pożizzjoni,int COLUMN_pożizzjoni){글내보내기("\033[");수치(ROW_pożizzjoni);byte_data(';');수치(COLUMN_pożizzjoni);byte_data('H');}
static int 이전항목(int data_pożizzjoni){if(data_pożizzjoni){data_pożizzjoni--;while(data_pożizzjoni>0&&(SMS[data_pożizzjoni]&192)==128)data_pożizzjoni--;}return data_pożizzjoni;}
static int Li_Jmiss_element(int data_pożizzjoni){if(data_pożizzjoni<tul_VALUE){data_pożizzjoni++;while(data_pożizzjoni<tul_VALUE&&(SMS[data_pożizzjoni]&192)==128)data_pożizzjoni++;}return data_pożizzjoni;}
static int serje(int data_pożizzjoni){while(data_pożizzjoni>0&&SMS[data_pożizzjoni-1]!='\n')data_pożizzjoni--;return data_pożizzjoni;}
static int ttermina_OFFSET(int data_pożizzjoni){while(data_pożizzjoni<tul_VALUE&&SMS[data_pożizzjoni]!='\n')data_pożizzjoni++;return data_pożizzjoni;}
static int 너비(unsigned kodiċi_tal_karattru){return kodiċi_tal_karattru>=196?2:1;}
static int COLUMN(int data_pożizzjoni){int kodiċi_tal_karattru=0;for(int 순번=serje(data_pożizzjoni);순번<data_pożizzjoni;순번=Li_Jmiss_element(순번))kodiċi_tal_karattru+=SMS[순번]=='\t'?4-kodiċi_tal_karattru%4:너비(SMS[순번]);return kodiċi_tal_karattru;}
static void punt_ta_kontroll(void){for(int 순번=0;순번<tul_VALUE;순번++)erġa_lura_data[순번]=SMS[순번];erġa_lura_tul=tul_VALUE;위쪽=INDEX_VALUE;erġa_lura_Bidliet=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){punt_ta_kontroll();for(int 순번=도착위치;순번<tul_VALUE;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];tul_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *string_data,int element_COUNT){if(element_COUNT>편집용량-tul_VALUE){알림문="File full (16384 bytes)";return 0;}punt_ta_kontroll();for(int 순번=tul_VALUE-1;순번>=INDEX_VALUE;순번--)SMS[순번+element_COUNT]=SMS[순번];for(int 순번=0;순번<element_COUNT;순번++)SMS[INDEX_VALUE+순번]=string_data[순번];tul_VALUE+=element_COUNT;INDEX_VALUE+=element_COUNT;변경됨=1;return 1;}
static void Vertikali(int 차이){int COLUMN_pożizzjoni=COLUMN(INDEX_VALUE),data_pożizzjoni=serje(INDEX_VALUE);if(차이<0){if(!data_pożizzjoni)return;data_pożizzjoni=serje(data_pożizzjoni-1);}else{data_pożizzjoni=ttermina_OFFSET(data_pożizzjoni);if(data_pożizzjoni==tul_VALUE)return;data_pożizzjoni++;}int kodiċi_tal_karattru=0;while(data_pożizzjoni<tul_VALUE&&SMS[data_pożizzjoni]!='\n'&&kodiċi_tal_karattru<COLUMN_pożizzjoni){kodiċi_tal_karattru+=SMS[data_pożizzjoni]=='\t'?4-kodiċi_tal_karattru%4:너비(SMS[data_pożizzjoni]);data_pożizzjoni=Li_Jmiss_element(data_pożizzjoni);}INDEX_VALUE=data_pożizzjoni;}
static void 화면그리기(void){
    if(INDEX_VALUE>tul_VALUE)INDEX_VALUE=tul_VALUE;if(맨위>INDEX_VALUE)맨위=serje(INDEX_VALUE);맨위=serje(맨위);
    int ROW_pożizzjoni=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')ROW_pożizzjoni++;
    while(ROW_pożizzjoni>=ROW_COUNT-1){맨위=ttermina_OFFSET(맨위);if(맨위<tul_VALUE)맨위++;ROW_pożizzjoni--;}
    int COLUMN_pożizzjoni=COLUMN(INDEX_VALUE);if(COLUMN_pożizzjoni<왼쪽)왼쪽=COLUMN_pożizzjoni;if(COLUMN_pożizzjoni-왼쪽>=COLUMNS-1)왼쪽=COLUMN_pożizzjoni-COLUMNS+2;
    글내보내기("\033[?25l");int data_pożizzjoni=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        mexxi_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int kodiċi_tal_karattru=0,그려진상태=0;
        if(data_pożizzjoni>=tul_VALUE&&반환값>ROW_pożizzjoni){글내보내기("\033[90m~\033[0m");continue;}
        while(data_pożizzjoni<tul_VALUE&&SMS[data_pożizzjoni]!='\n'){
            int Li_Jmiss_OFFSET=Li_Jmiss_element(data_pożizzjoni),너비값=SMS[data_pożizzjoni]=='\t'?4-kodiċi_tal_karattru%4:너비(SMS[data_pożizzjoni]);
            if(kodiċi_tal_karattru>=왼쪽&&kodiċi_tal_karattru-왼쪽+너비값<COLUMNS){
                if(SMS[data_pożizzjoni]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_data(' ');}else if(SMS[data_pożizzjoni]<32||SMS[data_pożizzjoni]==127){byte_data('?');}else for(int 안쪽순번=data_pożizzjoni;안쪽순번<Li_Jmiss_OFFSET;안쪽순번++)byte_data(SMS[안쪽순번]);그려진상태+=너비값;
            }kodiċi_tal_karattru+=너비값;data_pożizzjoni=Li_Jmiss_OFFSET;
        }
        (void)그려진상태;if(data_pożizzjoni<tul_VALUE)data_pożizzjoni++;
    }
    mexxi_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");stat_IMAGE=1;stat_kju=0;글내보내기(daħħal?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(fajl_entrata_isem[이름바이트수]&&이름바이트수<30)byte_data(fajl_entrata_isem[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int linja=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')linja++;수치(linja);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int element_COUNT=0;글내보내기(" | ");while(알림문[element_COUNT]&&element_COUNT<20)byte_data(알림문[element_COUNT++]);}
    stat_IMAGE=0;글내보내기("\033[0m");mexxi_VALUE(ROW_pożizzjoni+1,COLUMN_pożizzjoni-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(pendenti_tast){int 셋째순번=pendenti_tast;pendenti_tast=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned daqqas=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(daqqas&65535)||ROW_COUNT!=(int)(daqqas>>16)){
            COLUMNS=daqqas&65535;ROW_COUNT=daqqas>>16;화면그리기();
            if(għajnuna_kategorija){mexxi_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_data(għajnuna_kategorija);글내보내기(kmand);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){pendenti_tast=셋째순번;return 27;}
    int element_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){element_COUNT=element_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return element_COUNT==3?1007:element_COUNT==5?1008:element_COUNT==6?1009:element_COUNT==1?1005:element_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int fajl_handle=fetaħ_fajl(fajl_entrata_isem,qari_kitba|없으면만들기|내용비우기,0600);if(fajl_handle<0){알림문="Cannot open for save";return 0;}
    intptr_t element_COUNT=kiteb_fajl_data(fajl_handle,SMS,tul_VALUE);agħlaq_fajl(fajl_handle);if(element_COUNT!=tul_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void sab_Li_Jmiss(void){int element_COUNT=0;while(sab_entrata[element_COUNT])element_COUNT++;if(!element_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=tul_VALUE;순번++){int data_pożizzjoni=(INDEX_VALUE+순번)%(tul_VALUE?tul_VALUE:1),안쪽순번=0;while(안쪽순번<element_COUNT&&data_pożizzjoni+안쪽순번<tul_VALUE&&SMS[data_pożizzjoni+안쪽순번]==(unsigned char)sab_entrata[안쪽순번])안쪽순번++;if(안쪽순번==element_COUNT){INDEX_VALUE=data_pożizzjoni;알림문="Match";return;}}알림문="Pattern not found";}
static int prompt(int kategorija_VALUE){
    int element_COUNT=0;kmand[0]=0;
    for(;;){mexxi_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_data(kategorija_VALUE);글내보내기(kmand);출력비우기();għajnuna_kategorija=kategorija_VALUE;int 셋째순번=누름값();għajnuna_kategorija=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(element_COUNT){element_COUNT--;while(element_COUNT>0&&((unsigned char)kmand[element_COUNT]&192)==128)element_COUNT--;kmand[element_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&element_COUNT<120){kmand[element_COUNT++]=셋째순번;kmand[element_COUNT]=0;}
    }
    if(kategorija_VALUE=='/'){for(int 순번=0;순번<=element_COUNT;순번++)sab_entrata[순번]=kmand[순번];sab_Li_Jmiss();return 0;}
    if(같은지(kmand,"q!"))return 1;
    if(같은지(kmand,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(kmand,"wq")||같은지(kmand,"x"))return Store_VALUE();
    if(같은지(kmand,"w")){Store_VALUE();return 0;}
    if(kmand[0]=='w'&&kmand[1]==' '){int 순번=2;while(kmand[순번]==' ')순번++;int daqqas=element_COUNT-순번;if(daqqas<1||daqqas>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<daqqas;안쪽순번++)fajl_entrata_isem[안쪽순번]=kmand[순번+안쪽순번];fajl_entrata_isem[daqqas]=0;Store_VALUE();return 0;}
    int linja=0;for(int 순번=0;순번<element_COUNT;순번++){if(kmand[순번]<'0'||kmand[순번]>'9'){linja=0;break;}linja=linja*10+kmand[순번]-'0';if(linja>16384){linja=0;break;}}
    if(linja){INDEX_VALUE=0;while(--linja&&INDEX_VALUE<tul_VALUE){INDEX_VALUE=ttermina_OFFSET(INDEX_VALUE);if(INDEX_VALUE<tul_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Bidu_utent_programm(int 무시값){
    (void)무시값;if(utent_argument_COUNT()!=1||utent_argument(0,fajl_entrata_isem,sizeof(fajl_entrata_isem))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int fajl_handle=fetaħ_fajl(fajl_entrata_isem,qari_biss_VALUE,0);
    if(fajl_handle>=0){int element_COUNT=fajl_daqqas(fajl_handle);if(element_COUNT<0||element_COUNT>편집용량){agħlaq_fajl(fajl_handle);return 1;}tul_VALUE=파일자료읽기(fajl_handle,SMS,element_COUNT);agħlaq_fajl(fajl_handle);if(tul_VALUE!=element_COUNT)return 1;for(int 순번=0;순번<tul_VALUE;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,ħruġ_programm=0;
    while(!ħruġ_programm){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Vertikali(-1);continue;}if(셋째순번==1002){Vertikali(1);continue;}if(셋째순번==1003){INDEX_VALUE=Li_Jmiss_element(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=serje(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=ttermina_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Vertikali(셋째순번==1008?-1:1);continue;}
        if(daħħal){
            if(셋째순번==27||셋째순번==3){daħħal=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<tul_VALUE)바이트지우기(INDEX_VALUE,Li_Jmiss_element(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int element_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!element_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<element_COUNT;순번++){int kodiċi_tal_karattru=누름값();if(kodiċi_tal_karattru<128||kodiċi_tal_karattru>191){pendenti_tast=kodiċi_tal_karattru;유효함=0;break;}SECOND_VALUE[순번]=kodiċi_tal_karattru;}
                if(유효함)덧붙이기(SECOND_VALUE,element_COUNT);
            }continue;
        }
        if(앞부분){int data_pożizzjoni=앞부분;앞부분=0;if(data_pożizzjoni=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(data_pożizzjoni=='Z'&&셋째순번=='Z'){ħruġ_programm=Store_VALUE();continue;}if((data_pożizzjoni=='d'&&셋째순번=='d')||(data_pożizzjoni=='y'&&셋째순번=='y')){int 첫째값=serje(INDEX_VALUE),SECOND_VALUE=ttermina_OFFSET(INDEX_VALUE);if(SECOND_VALUE<tul_VALUE)SECOND_VALUE++;kkopja_tul=SECOND_VALUE-첫째값;for(int 순번=0;순번<kkopja_tul;순번++)복사자료[순번]=SMS[첫째값+순번];if(data_pożizzjoni=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){daħħal=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<ttermina_OFFSET(INDEX_VALUE))INDEX_VALUE=Li_Jmiss_element(INDEX_VALUE);daħħal=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=serje(INDEX_VALUE);daħħal=1;continue;}if(셋째순번=='A'){INDEX_VALUE=ttermina_OFFSET(INDEX_VALUE);daħħal=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char linja_ttermina='\n';INDEX_VALUE=셋째순번=='o'?ttermina_OFFSET(INDEX_VALUE):serje(INDEX_VALUE);if(덧붙이기(&linja_ttermina,1)){if(셋째순번=='O')INDEX_VALUE--;daħħal=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Li_Jmiss_element(INDEX_VALUE);continue;}if(셋째순번=='j'){Vertikali(1);continue;}if(셋째순번=='k'){Vertikali(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=serje(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=ttermina_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=serje(tul_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<tul_VALUE)바이트지우기(INDEX_VALUE,Li_Jmiss_element(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&kkopja_tul){INDEX_VALUE=ttermina_OFFSET(INDEX_VALUE);if(INDEX_VALUE<tul_VALUE)INDEX_VALUE++;덧붙이기(복사자료,kkopja_tul);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=SMS[순번];SMS[순번]=erġa_lura_data[순번];erġa_lura_data[순번]=SECOND_VALUE;}int element_COUNT=tul_VALUE;tul_VALUE=erġa_lura_tul;erġa_lura_tul=element_COUNT;element_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=element_COUNT;element_COUNT=변경됨;변경됨=erġa_lura_Bidliet;erġa_lura_Bidliet=element_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){ħruġ_programm=prompt(셋째순번);continue;}if(셋째순번=='n'){sab_Li_Jmiss();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
