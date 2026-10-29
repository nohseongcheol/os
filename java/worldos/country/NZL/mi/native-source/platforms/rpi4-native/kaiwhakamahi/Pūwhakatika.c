/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Ngā_kupu[편집용량],wete_raraunga[편집용량],복사자료[편집용량],mēhua_raraunga[1024];
static int roa_uara,INDEX_uara,맨위,왼쪽,변경됨,kōkuhu,wete_roa,위쪽,wete_Ngā_Huringa,되돌림있음,tārua_roa,사용량,COLUMNS=68,ROW_COUNT=19;
static char kōnae_tāurunga_ingoa[64],tono[128],FIND_tāurunga[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned tārewa_kī;
static int āwhina_kāwai,tūnga_IMAGE,tūnga_tūtira;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)mēhua_raraunga,사용량,0,0,0);사용량=0;}}
static void paita_raraunga(unsigned waehere_pūāhua){if(tūnga_IMAGE){if((waehere_pūāhua&192)!=128){tūnga_tūtira+=waehere_pūāhua>=196?2:1;}if(tūnga_tūtira>=COLUMNS)return;}if(사용량==(int)sizeof(mēhua_raraunga))출력비우기();mēhua_raraunga[사용량++]=waehere_pūāhua;}
static void 글내보내기(const char *aho_raraunga){while(*aho_raraunga)paita_raraunga((unsigned char)*aho_raraunga++);}
static void 수치(unsigned tuemi_COUNT){char SECOND_uara[12];int 순번=0;do{SECOND_uara[순번++]='0'+tuemi_COUNT%10;tuemi_COUNT/=10;}while(tuemi_COUNT);while(순번)paita_raraunga(SECOND_uara[--순번]);}
static void nuku_uara(int ROW_tūranga,int tīwae_tūranga){글내보내기("\033[");수치(ROW_tūranga);paita_raraunga(';');수치(tīwae_tūranga);paita_raraunga('H');}
static int 이전항목(int raraunga_tūranga){if(raraunga_tūranga){raraunga_tūranga--;while(raraunga_tūranga>0&&(Ngā_kupu[raraunga_tūranga]&192)==128)raraunga_tūranga--;}return raraunga_tūranga;}
static int Panuku_tuemi(int raraunga_tūranga){if(raraunga_tūranga<roa_uara){raraunga_tūranga++;while(raraunga_tūranga<roa_uara&&(Ngā_kupu[raraunga_tūranga]&192)==128)raraunga_tūranga++;}return raraunga_tūranga;}
static int whakahaere(int raraunga_tūranga){while(raraunga_tūranga>0&&Ngā_kupu[raraunga_tūranga-1]!='\n')raraunga_tūranga--;return raraunga_tūranga;}
static int mutu_OFFSET(int raraunga_tūranga){while(raraunga_tūranga<roa_uara&&Ngā_kupu[raraunga_tūranga]!='\n')raraunga_tūranga++;return raraunga_tūranga;}
static int 너비(unsigned waehere_pūāhua){return waehere_pūāhua>=196?2:1;}
static int tīwae(int raraunga_tūranga){int waehere_pūāhua=0;for(int 순번=whakahaere(raraunga_tūranga);순번<raraunga_tūranga;순번=Panuku_tuemi(순번))waehere_pūāhua+=Ngā_kupu[순번]=='\t'?4-waehere_pūāhua%4:너비(Ngā_kupu[순번]);return waehere_pūāhua;}
static void wāhitaki(void){for(int 순번=0;순번<roa_uara;순번++)wete_raraunga[순번]=Ngā_kupu[순번];wete_roa=roa_uara;위쪽=INDEX_uara;wete_Ngā_Huringa=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){wāhitaki();for(int 순번=도착위치;순번<roa_uara;순번++)Ngā_kupu[출발위치+순번-도착위치]=Ngā_kupu[순번];roa_uara-=도착위치-출발위치;INDEX_uara=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *aho_raraunga,int tuemi_COUNT){if(tuemi_COUNT>편집용량-roa_uara){알림문="File full (16384 bytes)";return 0;}wāhitaki();for(int 순번=roa_uara-1;순번>=INDEX_uara;순번--)Ngā_kupu[순번+tuemi_COUNT]=Ngā_kupu[순번];for(int 순번=0;순번<tuemi_COUNT;순번++)Ngā_kupu[INDEX_uara+순번]=aho_raraunga[순번];roa_uara+=tuemi_COUNT;INDEX_uara+=tuemi_COUNT;변경됨=1;return 1;}
static void Poutū(int 차이){int tīwae_tūranga=tīwae(INDEX_uara),raraunga_tūranga=whakahaere(INDEX_uara);if(차이<0){if(!raraunga_tūranga)return;raraunga_tūranga=whakahaere(raraunga_tūranga-1);}else{raraunga_tūranga=mutu_OFFSET(raraunga_tūranga);if(raraunga_tūranga==roa_uara)return;raraunga_tūranga++;}int waehere_pūāhua=0;while(raraunga_tūranga<roa_uara&&Ngā_kupu[raraunga_tūranga]!='\n'&&waehere_pūāhua<tīwae_tūranga){waehere_pūāhua+=Ngā_kupu[raraunga_tūranga]=='\t'?4-waehere_pūāhua%4:너비(Ngā_kupu[raraunga_tūranga]);raraunga_tūranga=Panuku_tuemi(raraunga_tūranga);}INDEX_uara=raraunga_tūranga;}
static void 화면그리기(void){
    if(INDEX_uara>roa_uara)INDEX_uara=roa_uara;if(맨위>INDEX_uara)맨위=whakahaere(INDEX_uara);맨위=whakahaere(맨위);
    int ROW_tūranga=0;for(int 순번=맨위;순번<INDEX_uara;순번++)if(Ngā_kupu[순번]=='\n')ROW_tūranga++;
    while(ROW_tūranga>=ROW_COUNT-1){맨위=mutu_OFFSET(맨위);if(맨위<roa_uara)맨위++;ROW_tūranga--;}
    int tīwae_tūranga=tīwae(INDEX_uara);if(tīwae_tūranga<왼쪽)왼쪽=tīwae_tūranga;if(tīwae_tūranga-왼쪽>=COLUMNS-1)왼쪽=tīwae_tūranga-COLUMNS+2;
    글내보내기("\033[?25l");int raraunga_tūranga=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        nuku_uara(반환값+1,1);글내보내기("\033[0m\033[2K");int waehere_pūāhua=0,그려진상태=0;
        if(raraunga_tūranga>=roa_uara&&반환값>ROW_tūranga){글내보내기("\033[90m~\033[0m");continue;}
        while(raraunga_tūranga<roa_uara&&Ngā_kupu[raraunga_tūranga]!='\n'){
            int Panuku_OFFSET=Panuku_tuemi(raraunga_tūranga),너비값=Ngā_kupu[raraunga_tūranga]=='\t'?4-waehere_pūāhua%4:너비(Ngā_kupu[raraunga_tūranga]);
            if(waehere_pūāhua>=왼쪽&&waehere_pūāhua-왼쪽+너비값<COLUMNS){
                if(Ngā_kupu[raraunga_tūranga]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)paita_raraunga(' ');}else if(Ngā_kupu[raraunga_tūranga]<32||Ngā_kupu[raraunga_tūranga]==127){paita_raraunga('?');}else for(int 안쪽순번=raraunga_tūranga;안쪽순번<Panuku_OFFSET;안쪽순번++)paita_raraunga(Ngā_kupu[안쪽순번]);그려진상태+=너비값;
            }waehere_pūāhua+=너비값;raraunga_tūranga=Panuku_OFFSET;
        }
        (void)그려진상태;if(raraunga_tūranga<roa_uara)raraunga_tūranga++;
    }
    nuku_uara(ROW_COUNT,1);글내보내기("\033[7m\033[2K");tūnga_IMAGE=1;tūnga_tūtira=0;글내보내기(kōkuhu?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(kōnae_tāurunga_ingoa[이름바이트수]&&이름바이트수<30)paita_raraunga(kōnae_tāurunga_ingoa[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int hononga=1;for(int 순번=0;순번<INDEX_uara;순번++)if(Ngā_kupu[순번]=='\n')hononga++;수치(hononga);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int tuemi_COUNT=0;글내보내기(" | ");while(알림문[tuemi_COUNT]&&tuemi_COUNT<20)paita_raraunga(알림문[tuemi_COUNT++]);}
    tūnga_IMAGE=0;글내보내기("\033[0m");nuku_uara(ROW_tūranga+1,tīwae_tūranga-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(tārewa_kī){int 셋째순번=tārewa_kī;tārewa_kī=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned rahi=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(rahi&65535)||ROW_COUNT!=(int)(rahi>>16)){
            COLUMNS=rahi&65535;ROW_COUNT=rahi>>16;화면그리기();
            if(āwhina_kāwai){nuku_uara(ROW_COUNT,1);글내보내기("\033[0m\033[2K");paita_raraunga(āwhina_kāwai);글내보내기(tono);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){tārewa_kī=셋째순번;return 27;}
    int tuemi_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){tuemi_COUNT=tuemi_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return tuemi_COUNT==3?1007:tuemi_COUNT==5?1008:tuemi_COUNT==6?1009:tuemi_COUNT==1?1005:tuemi_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_uara(void){
    int kōnae_raweke=tiwhikete_kōnae(kōnae_tāurunga_ingoa,읽고쓰기|없으면만들기|내용비우기,0600);if(kōnae_raweke<0){알림문="Cannot open for save";return 0;}
    intptr_t tuemi_COUNT=tuhi_kōnae_raraunga(kōnae_raweke,Ngā_kupu,roa_uara);kati_kōnae(kōnae_raweke);if(tuemi_COUNT!=roa_uara){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_uara){while(*첫째값&&*첫째값==*SECOND_uara){첫째값++;SECOND_uara++;}return *첫째값==*SECOND_uara;}
static void FIND_Panuku(void){int tuemi_COUNT=0;while(FIND_tāurunga[tuemi_COUNT])tuemi_COUNT++;if(!tuemi_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=roa_uara;순번++){int raraunga_tūranga=(INDEX_uara+순번)%(roa_uara?roa_uara:1),안쪽순번=0;while(안쪽순번<tuemi_COUNT&&raraunga_tūranga+안쪽순번<roa_uara&&Ngā_kupu[raraunga_tūranga+안쪽순번]==(unsigned char)FIND_tāurunga[안쪽순번])안쪽순번++;if(안쪽순번==tuemi_COUNT){INDEX_uara=raraunga_tūranga;알림문="Match";return;}}알림문="Pattern not found";}
static int tohuaki(int kāwai_uara){
    int tuemi_COUNT=0;tono[0]=0;
    for(;;){nuku_uara(ROW_COUNT,1);글내보내기("\033[0m\033[2K");paita_raraunga(kāwai_uara);글내보내기(tono);출력비우기();āwhina_kāwai=kāwai_uara;int 셋째순번=누름값();āwhina_kāwai=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(tuemi_COUNT){tuemi_COUNT--;while(tuemi_COUNT>0&&((unsigned char)tono[tuemi_COUNT]&192)==128)tuemi_COUNT--;tono[tuemi_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&tuemi_COUNT<120){tono[tuemi_COUNT++]=셋째순번;tono[tuemi_COUNT]=0;}
    }
    if(kāwai_uara=='/'){for(int 순번=0;순번<=tuemi_COUNT;순번++)FIND_tāurunga[순번]=tono[순번];FIND_Panuku();return 0;}
    if(같은지(tono,"q!"))return 1;
    if(같은지(tono,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(tono,"wq")||같은지(tono,"x"))return Store_uara();
    if(같은지(tono,"w")){Store_uara();return 0;}
    if(tono[0]=='w'&&tono[1]==' '){int 순번=2;while(tono[순번]==' ')순번++;int rahi=tuemi_COUNT-순번;if(rahi<1||rahi>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<rahi;안쪽순번++)kōnae_tāurunga_ingoa[안쪽순번]=tono[순번+안쪽순번];kōnae_tāurunga_ingoa[rahi]=0;Store_uara();return 0;}
    int hononga=0;for(int 순번=0;순번<tuemi_COUNT;순번++){if(tono[순번]<'0'||tono[순번]>'9'){hononga=0;break;}hononga=hononga*10+tono[순번]-'0';if(hononga>16384){hononga=0;break;}}
    if(hononga){INDEX_uara=0;while(--hononga&&INDEX_uara<roa_uara){INDEX_uara=mutu_OFFSET(INDEX_uara);if(INDEX_uara<roa_uara)INDEX_uara++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Start_kaiwhakamahi_kaupapa(int 무시값){
    (void)무시값;if(kaiwhakamahi_tohenga_COUNT()!=1||kaiwhakamahi_tohenga(0,kōnae_tāurunga_ingoa,sizeof(kōnae_tāurunga_ingoa))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int kōnae_raweke=tiwhikete_kōnae(kōnae_tāurunga_ingoa,pānui_anake_uara,0);
    if(kōnae_raweke>=0){int tuemi_COUNT=kōnae_rahi(kōnae_raweke);if(tuemi_COUNT<0||tuemi_COUNT>편집용량){kati_kōnae(kōnae_raweke);return 1;}roa_uara=파일자료읽기(kōnae_raweke,Ngā_kupu,tuemi_COUNT);kati_kōnae(kōnae_raweke);if(roa_uara!=tuemi_COUNT)return 1;for(int 순번=0;순번<roa_uara;순번++)if(!Ngā_kupu[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,wehe_kaupapa=0;
    while(!wehe_kaupapa){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Poutū(-1);continue;}if(셋째순번==1002){Poutū(1);continue;}if(셋째순번==1003){INDEX_uara=Panuku_tuemi(INDEX_uara);continue;}if(셋째순번==1004){INDEX_uara=이전항목(INDEX_uara);continue;}
        if(셋째순번==1005){INDEX_uara=whakahaere(INDEX_uara);continue;}if(셋째순번==1006){INDEX_uara=mutu_OFFSET(INDEX_uara);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Poutū(셋째순번==1008?-1:1);continue;}
        if(kōkuhu){
            if(셋째순번==27||셋째순번==3){kōkuhu=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_uara)바이트지우기(이전항목(INDEX_uara),INDEX_uara);continue;}
            if(셋째순번==1007){if(INDEX_uara<roa_uara)바이트지우기(INDEX_uara,Panuku_tuemi(INDEX_uara));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_uara[4];SECOND_uara[0]=셋째순번;int tuemi_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!tuemi_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<tuemi_COUNT;순번++){int waehere_pūāhua=누름값();if(waehere_pūāhua<128||waehere_pūāhua>191){tārewa_kī=waehere_pūāhua;유효함=0;break;}SECOND_uara[순번]=waehere_pūāhua;}
                if(유효함)덧붙이기(SECOND_uara,tuemi_COUNT);
            }continue;
        }
        if(앞부분){int raraunga_tūranga=앞부분;앞부분=0;if(raraunga_tūranga=='g'&&셋째순번=='g'){INDEX_uara=0;continue;}if(raraunga_tūranga=='Z'&&셋째순번=='Z'){wehe_kaupapa=Store_uara();continue;}if((raraunga_tūranga=='d'&&셋째순번=='d')||(raraunga_tūranga=='y'&&셋째순번=='y')){int 첫째값=whakahaere(INDEX_uara),SECOND_uara=mutu_OFFSET(INDEX_uara);if(SECOND_uara<roa_uara)SECOND_uara++;tārua_roa=SECOND_uara-첫째값;for(int 순번=0;순번<tārua_roa;순번++)복사자료[순번]=Ngā_kupu[첫째값+순번];if(raraunga_tūranga=='d')바이트지우기(첫째값,SECOND_uara);continue;}}
        if(셋째순번=='i'){kōkuhu=1;continue;}if(셋째순번=='a'){if(INDEX_uara<mutu_OFFSET(INDEX_uara))INDEX_uara=Panuku_tuemi(INDEX_uara);kōkuhu=1;continue;}
        if(셋째순번=='I'){INDEX_uara=whakahaere(INDEX_uara);kōkuhu=1;continue;}if(셋째순번=='A'){INDEX_uara=mutu_OFFSET(INDEX_uara);kōkuhu=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char hononga_mutu='\n';INDEX_uara=셋째순번=='o'?mutu_OFFSET(INDEX_uara):whakahaere(INDEX_uara);if(덧붙이기(&hononga_mutu,1)){if(셋째순번=='O')INDEX_uara--;kōkuhu=1;}continue;}
        if(셋째순번=='h'){INDEX_uara=이전항목(INDEX_uara);continue;}if(셋째순번=='l'){INDEX_uara=Panuku_tuemi(INDEX_uara);continue;}if(셋째순번=='j'){Poutū(1);continue;}if(셋째순번=='k'){Poutū(-1);continue;}
        if(셋째순번=='0'){INDEX_uara=whakahaere(INDEX_uara);continue;}if(셋째순번=='$'){INDEX_uara=mutu_OFFSET(INDEX_uara);continue;}if(셋째순번=='G'){INDEX_uara=whakahaere(roa_uara);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_uara<roa_uara)바이트지우기(INDEX_uara,Panuku_tuemi(INDEX_uara));continue;}
        if(셋째순번=='p'&&tārua_roa){INDEX_uara=mutu_OFFSET(INDEX_uara);if(INDEX_uara<roa_uara)INDEX_uara++;덧붙이기(복사자료,tārua_roa);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_uara=Ngā_kupu[순번];Ngā_kupu[순번]=wete_raraunga[순번];wete_raraunga[순번]=SECOND_uara;}int tuemi_COUNT=roa_uara;roa_uara=wete_roa;wete_roa=tuemi_COUNT;tuemi_COUNT=INDEX_uara;INDEX_uara=위쪽;위쪽=tuemi_COUNT;tuemi_COUNT=변경됨;변경됨=wete_Ngā_Huringa;wete_Ngā_Huringa=tuemi_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){wehe_kaupapa=tohuaki(셋째순번);continue;}if(셋째순번=='n'){FIND_Panuku();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
