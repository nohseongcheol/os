/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Téacs[편집용량],cealaigh_sonraí[편집용량],복사자료[편집용량],tomhas_sonraí[1024];
static int fad_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,ionsáigh,cealaigh_fad,위쪽,cealaigh_Athruithe,되돌림있음,ásc_fad,사용량,COLUMNS=68,ró_COUNT=19;
static char comhad_iontráil_ainm[64],Ordú[128],FIND_iontráil[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned Ar_feitheamh_eochair;
static int cabhair_catagóir,staid_IMAGE,staid_scuaine;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)tomhas_sonraí,사용량,0,0,0);사용량=0;}}
static void beart_sonraí(unsigned pointe_cóid){if(staid_IMAGE){if((pointe_cóid&192)!=128){staid_scuaine+=pointe_cóid>=196?2:1;}if(staid_scuaine>=COLUMNS)return;}if(사용량==(int)sizeof(tomhas_sonraí))출력비우기();tomhas_sonraí[사용량++]=pointe_cóid;}
static void 글내보내기(const char *teaghrán_sonraí){while(*teaghrán_sonraí)beart_sonraí((unsigned char)*teaghrán_sonraí++);}
static void 수치(unsigned mír_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+mír_COUNT%10;mír_COUNT/=10;}while(mír_COUNT);while(순번)beart_sonraí(SECOND_VALUE[--순번]);}
static void bog_VALUE(int ró_suíomh,int colún_suíomh){글내보내기("\033[");수치(ró_suíomh);beart_sonraí(';');수치(colún_suíomh);beart_sonraí('H');}
static int 이전항목(int sonraí_suíomh){if(sonraí_suíomh){sonraí_suíomh--;while(sonraí_suíomh>0&&(Téacs[sonraí_suíomh]&192)==128)sonraí_suíomh--;}return sonraí_suíomh;}
static int Ar_aghaidh_mír(int sonraí_suíomh){if(sonraí_suíomh<fad_VALUE){sonraí_suíomh++;while(sonraí_suíomh<fad_VALUE&&(Téacs[sonraí_suíomh]&192)==128)sonraí_suíomh++;}return sonraí_suíomh;}
static int Rith_2(int sonraí_suíomh){while(sonraí_suíomh>0&&Téacs[sonraí_suíomh-1]!='\n')sonraí_suíomh--;return sonraí_suíomh;}
static int cuir_deireadh_le_OFFSET(int sonraí_suíomh){while(sonraí_suíomh<fad_VALUE&&Téacs[sonraí_suíomh]!='\n')sonraí_suíomh++;return sonraí_suíomh;}
static int 너비(unsigned pointe_cóid){return pointe_cóid>=196?2:1;}
static int colún(int sonraí_suíomh){int pointe_cóid=0;for(int 순번=Rith_2(sonraí_suíomh);순번<sonraí_suíomh;순번=Ar_aghaidh_mír(순번))pointe_cóid+=Téacs[순번]=='\t'?4-pointe_cóid%4:너비(Téacs[순번]);return pointe_cóid;}
static void seicphointe(void){for(int 순번=0;순번<fad_VALUE;순번++)cealaigh_sonraí[순번]=Téacs[순번];cealaigh_fad=fad_VALUE;위쪽=INDEX_VALUE;cealaigh_Athruithe=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){seicphointe();for(int 순번=도착위치;순번<fad_VALUE;순번++)Téacs[출발위치+순번-도착위치]=Téacs[순번];fad_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *teaghrán_sonraí,int mír_COUNT){if(mír_COUNT>편집용량-fad_VALUE){알림문="File full (16384 bytes)";return 0;}seicphointe();for(int 순번=fad_VALUE-1;순번>=INDEX_VALUE;순번--)Téacs[순번+mír_COUNT]=Téacs[순번];for(int 순번=0;순번<mír_COUNT;순번++)Téacs[INDEX_VALUE+순번]=teaghrán_sonraí[순번];fad_VALUE+=mír_COUNT;INDEX_VALUE+=mír_COUNT;변경됨=1;return 1;}
static void Ingearach(int 차이){int colún_suíomh=colún(INDEX_VALUE),sonraí_suíomh=Rith_2(INDEX_VALUE);if(차이<0){if(!sonraí_suíomh)return;sonraí_suíomh=Rith_2(sonraí_suíomh-1);}else{sonraí_suíomh=cuir_deireadh_le_OFFSET(sonraí_suíomh);if(sonraí_suíomh==fad_VALUE)return;sonraí_suíomh++;}int pointe_cóid=0;while(sonraí_suíomh<fad_VALUE&&Téacs[sonraí_suíomh]!='\n'&&pointe_cóid<colún_suíomh){pointe_cóid+=Téacs[sonraí_suíomh]=='\t'?4-pointe_cóid%4:너비(Téacs[sonraí_suíomh]);sonraí_suíomh=Ar_aghaidh_mír(sonraí_suíomh);}INDEX_VALUE=sonraí_suíomh;}
static void 화면그리기(void){
    if(INDEX_VALUE>fad_VALUE)INDEX_VALUE=fad_VALUE;if(맨위>INDEX_VALUE)맨위=Rith_2(INDEX_VALUE);맨위=Rith_2(맨위);
    int ró_suíomh=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Téacs[순번]=='\n')ró_suíomh++;
    while(ró_suíomh>=ró_COUNT-1){맨위=cuir_deireadh_le_OFFSET(맨위);if(맨위<fad_VALUE)맨위++;ró_suíomh--;}
    int colún_suíomh=colún(INDEX_VALUE);if(colún_suíomh<왼쪽)왼쪽=colún_suíomh;if(colún_suíomh-왼쪽>=COLUMNS-1)왼쪽=colún_suíomh-COLUMNS+2;
    글내보내기("\033[?25l");int sonraí_suíomh=맨위;
    for(int 반환값=0;반환값<ró_COUNT-1;반환값++){
        bog_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int pointe_cóid=0,그려진상태=0;
        if(sonraí_suíomh>=fad_VALUE&&반환값>ró_suíomh){글내보내기("\033[90m~\033[0m");continue;}
        while(sonraí_suíomh<fad_VALUE&&Téacs[sonraí_suíomh]!='\n'){
            int Ar_aghaidh_OFFSET=Ar_aghaidh_mír(sonraí_suíomh),너비값=Téacs[sonraí_suíomh]=='\t'?4-pointe_cóid%4:너비(Téacs[sonraí_suíomh]);
            if(pointe_cóid>=왼쪽&&pointe_cóid-왼쪽+너비값<COLUMNS){
                if(Téacs[sonraí_suíomh]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)beart_sonraí(' ');}else if(Téacs[sonraí_suíomh]<32||Téacs[sonraí_suíomh]==127){beart_sonraí('?');}else for(int 안쪽순번=sonraí_suíomh;안쪽순번<Ar_aghaidh_OFFSET;안쪽순번++)beart_sonraí(Téacs[안쪽순번]);그려진상태+=너비값;
            }pointe_cóid+=너비값;sonraí_suíomh=Ar_aghaidh_OFFSET;
        }
        (void)그려진상태;if(sonraí_suíomh<fad_VALUE)sonraí_suíomh++;
    }
    bog_VALUE(ró_COUNT,1);글내보내기("\033[7m\033[2K");staid_IMAGE=1;staid_scuaine=0;글내보내기(ionsáigh?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(comhad_iontráil_ainm[이름바이트수]&&이름바이트수<30)beart_sonraí(comhad_iontráil_ainm[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Líne=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Téacs[순번]=='\n')Líne++;수치(Líne);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int mír_COUNT=0;글내보내기(" | ");while(알림문[mír_COUNT]&&mír_COUNT<20)beart_sonraí(알림문[mír_COUNT++]);}
    staid_IMAGE=0;글내보내기("\033[0m");bog_VALUE(ró_suíomh+1,colún_suíomh-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(Ar_feitheamh_eochair){int 셋째순번=Ar_feitheamh_eochair;Ar_feitheamh_eochair=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Méid=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Méid&65535)||ró_COUNT!=(int)(Méid>>16)){
            COLUMNS=Méid&65535;ró_COUNT=Méid>>16;화면그리기();
            if(cabhair_catagóir){bog_VALUE(ró_COUNT,1);글내보내기("\033[0m\033[2K");beart_sonraí(cabhair_catagóir);글내보내기(Ordú);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){Ar_feitheamh_eochair=셋째순번;return 27;}
    int mír_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){mír_COUNT=mír_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return mír_COUNT==3?1007:mír_COUNT==5?1008:mír_COUNT==6?1009:mír_COUNT==1?1005:mír_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int comhad_hanla=oscail_comhad(comhad_iontráil_ainm,inléite_inscríofa|없으면만들기|내용비우기,0600);if(comhad_hanla<0){알림문="Cannot open for save";return 0;}
    intptr_t mír_COUNT=scríobh_comhad_sonraí(comhad_hanla,Téacs,fad_VALUE);dún_comhad(comhad_hanla);if(mír_COUNT!=fad_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Ar_aghaidh(void){int mír_COUNT=0;while(FIND_iontráil[mír_COUNT])mír_COUNT++;if(!mír_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=fad_VALUE;순번++){int sonraí_suíomh=(INDEX_VALUE+순번)%(fad_VALUE?fad_VALUE:1),안쪽순번=0;while(안쪽순번<mír_COUNT&&sonraí_suíomh+안쪽순번<fad_VALUE&&Téacs[sonraí_suíomh+안쪽순번]==(unsigned char)FIND_iontráil[안쪽순번])안쪽순번++;if(안쪽순번==mír_COUNT){INDEX_VALUE=sonraí_suíomh;알림문="Match";return;}}알림문="Pattern not found";}
static int leid(int catagóir_VALUE){
    int mír_COUNT=0;Ordú[0]=0;
    for(;;){bog_VALUE(ró_COUNT,1);글내보내기("\033[0m\033[2K");beart_sonraí(catagóir_VALUE);글내보내기(Ordú);출력비우기();cabhair_catagóir=catagóir_VALUE;int 셋째순번=누름값();cabhair_catagóir=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(mír_COUNT){mír_COUNT--;while(mír_COUNT>0&&((unsigned char)Ordú[mír_COUNT]&192)==128)mír_COUNT--;Ordú[mír_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&mír_COUNT<120){Ordú[mír_COUNT++]=셋째순번;Ordú[mír_COUNT]=0;}
    }
    if(catagóir_VALUE=='/'){for(int 순번=0;순번<=mír_COUNT;순번++)FIND_iontráil[순번]=Ordú[순번];FIND_Ar_aghaidh();return 0;}
    if(같은지(Ordú,"q!"))return 1;
    if(같은지(Ordú,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Ordú,"wq")||같은지(Ordú,"x"))return Store_VALUE();
    if(같은지(Ordú,"w")){Store_VALUE();return 0;}
    if(Ordú[0]=='w'&&Ordú[1]==' '){int 순번=2;while(Ordú[순번]==' ')순번++;int Méid=mír_COUNT-순번;if(Méid<1||Méid>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Méid;안쪽순번++)comhad_iontráil_ainm[안쪽순번]=Ordú[순번+안쪽순번];comhad_iontráil_ainm[Méid]=0;Store_VALUE();return 0;}
    int Líne=0;for(int 순번=0;순번<mír_COUNT;순번++){if(Ordú[순번]<'0'||Ordú[순번]>'9'){Líne=0;break;}Líne=Líne*10+Ordú[순번]-'0';if(Líne>16384){Líne=0;break;}}
    if(Líne){INDEX_VALUE=0;while(--Líne&&INDEX_VALUE<fad_VALUE){INDEX_VALUE=cuir_deireadh_le_OFFSET(INDEX_VALUE);if(INDEX_VALUE<fad_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Start_úsáideoir_clár(int 무시값){
    (void)무시값;if(úsáideoir_argóint_COUNT()!=1||úsáideoir_argóint(0,comhad_iontráil_ainm,sizeof(comhad_iontráil_ainm))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int comhad_hanla=oscail_comhad(comhad_iontráil_ainm,inléite_amháin_VALUE,0);
    if(comhad_hanla>=0){int mír_COUNT=comhad_socraigh_méid(comhad_hanla);if(mír_COUNT<0||mír_COUNT>편집용량){dún_comhad(comhad_hanla);return 1;}fad_VALUE=파일자료읽기(comhad_hanla,Téacs,mír_COUNT);dún_comhad(comhad_hanla);if(fad_VALUE!=mír_COUNT)return 1;for(int 순번=0;순번<fad_VALUE;순번++)if(!Téacs[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ró_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,scoir_clár_55b3a1cd=0;
    while(!scoir_clár_55b3a1cd){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Ingearach(-1);continue;}if(셋째순번==1002){Ingearach(1);continue;}if(셋째순번==1003){INDEX_VALUE=Ar_aghaidh_mír(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Rith_2(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=cuir_deireadh_le_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ró_COUNT-2;순번++)Ingearach(셋째순번==1008?-1:1);continue;}
        if(ionsáigh){
            if(셋째순번==27||셋째순번==3){ionsáigh=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<fad_VALUE)바이트지우기(INDEX_VALUE,Ar_aghaidh_mír(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int mír_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!mír_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<mír_COUNT;순번++){int pointe_cóid=누름값();if(pointe_cóid<128||pointe_cóid>191){Ar_feitheamh_eochair=pointe_cóid;유효함=0;break;}SECOND_VALUE[순번]=pointe_cóid;}
                if(유효함)덧붙이기(SECOND_VALUE,mír_COUNT);
            }continue;
        }
        if(앞부분){int sonraí_suíomh=앞부분;앞부분=0;if(sonraí_suíomh=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(sonraí_suíomh=='Z'&&셋째순번=='Z'){scoir_clár_55b3a1cd=Store_VALUE();continue;}if((sonraí_suíomh=='d'&&셋째순번=='d')||(sonraí_suíomh=='y'&&셋째순번=='y')){int 첫째값=Rith_2(INDEX_VALUE),SECOND_VALUE=cuir_deireadh_le_OFFSET(INDEX_VALUE);if(SECOND_VALUE<fad_VALUE)SECOND_VALUE++;ásc_fad=SECOND_VALUE-첫째값;for(int 순번=0;순번<ásc_fad;순번++)복사자료[순번]=Téacs[첫째값+순번];if(sonraí_suíomh=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){ionsáigh=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<cuir_deireadh_le_OFFSET(INDEX_VALUE))INDEX_VALUE=Ar_aghaidh_mír(INDEX_VALUE);ionsáigh=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Rith_2(INDEX_VALUE);ionsáigh=1;continue;}if(셋째순번=='A'){INDEX_VALUE=cuir_deireadh_le_OFFSET(INDEX_VALUE);ionsáigh=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char líne_cuir_deireadh_le='\n';INDEX_VALUE=셋째순번=='o'?cuir_deireadh_le_OFFSET(INDEX_VALUE):Rith_2(INDEX_VALUE);if(덧붙이기(&líne_cuir_deireadh_le,1)){if(셋째순번=='O')INDEX_VALUE--;ionsáigh=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Ar_aghaidh_mír(INDEX_VALUE);continue;}if(셋째순번=='j'){Ingearach(1);continue;}if(셋째순번=='k'){Ingearach(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Rith_2(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=cuir_deireadh_le_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Rith_2(fad_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<fad_VALUE)바이트지우기(INDEX_VALUE,Ar_aghaidh_mír(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&ásc_fad){INDEX_VALUE=cuir_deireadh_le_OFFSET(INDEX_VALUE);if(INDEX_VALUE<fad_VALUE)INDEX_VALUE++;덧붙이기(복사자료,ásc_fad);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=Téacs[순번];Téacs[순번]=cealaigh_sonraí[순번];cealaigh_sonraí[순번]=SECOND_VALUE;}int mír_COUNT=fad_VALUE;fad_VALUE=cealaigh_fad;cealaigh_fad=mír_COUNT;mír_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=mír_COUNT;mír_COUNT=변경됨;변경됨=cealaigh_Athruithe;cealaigh_Athruithe=mír_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){scoir_clár_55b3a1cd=leid(셋째순번);continue;}if(셋째순번=='n'){FIND_Ar_aghaidh();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
