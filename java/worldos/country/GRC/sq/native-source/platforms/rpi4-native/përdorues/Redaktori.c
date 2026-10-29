/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Teksti[편집용량],zhbëj_të_dhëna[편집용량],복사자료[편집용량],llogaritje_të_dhëna[1024];
static int gjatësi_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,ndërfut,zhbëj_gjatësi,위쪽,zhbëj_Ndryshime,되돌림있음,kopjoj_gjatësi,사용량,COLUMNS=68,ROW_COUNT=19;
static char skedar_futje_emër[64],Komanda[128],FIND_futje[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned në_pritje_tast;
static int ndihmë_kategori,status_IMAGE,status_radhë;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)llogaritje_të_dhëna,사용량,0,0,0);사용량=0;}}
static void bajt_të_dhëna(unsigned kodi_i_karakterit){if(status_IMAGE){if((kodi_i_karakterit&192)!=128){status_radhë+=kodi_i_karakterit>=196?2:1;}if(status_radhë>=COLUMNS)return;}if(사용량==(int)sizeof(llogaritje_të_dhëna))출력비우기();llogaritje_të_dhëna[사용량++]=kodi_i_karakterit;}
static void 글내보내기(const char *varg_të_dhëna){while(*varg_të_dhëna)bajt_të_dhëna((unsigned char)*varg_të_dhëna++);}
static void 수치(unsigned njësi_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+njësi_COUNT%10;njësi_COUNT/=10;}while(njësi_COUNT);while(순번)bajt_të_dhëna(SECOND_VALUE[--순번]);}
static void lëviz_VALUE(int ROW_pozicioni,int COLUMN_pozicioni){글내보내기("\033[");수치(ROW_pozicioni);bajt_të_dhëna(';');수치(COLUMN_pozicioni);bajt_të_dhëna('H');}
static int 이전항목(int të_dhëna_pozicioni){if(të_dhëna_pozicioni){të_dhëna_pozicioni--;while(të_dhëna_pozicioni>0&&(Teksti[të_dhëna_pozicioni]&192)==128)të_dhëna_pozicioni--;}return të_dhëna_pozicioni;}
static int Tjetër_njësi(int të_dhëna_pozicioni){if(të_dhëna_pozicioni<gjatësi_VALUE){të_dhëna_pozicioni++;while(të_dhëna_pozicioni<gjatësi_VALUE&&(Teksti[të_dhëna_pozicioni]&192)==128)të_dhëna_pozicioni++;}return të_dhëna_pozicioni;}
static int Ekzekuto(int të_dhëna_pozicioni){while(të_dhëna_pozicioni>0&&Teksti[të_dhëna_pozicioni-1]!='\n')të_dhëna_pozicioni--;return të_dhëna_pozicioni;}
static int mbaroj_OFFSET(int të_dhëna_pozicioni){while(të_dhëna_pozicioni<gjatësi_VALUE&&Teksti[të_dhëna_pozicioni]!='\n')të_dhëna_pozicioni++;return të_dhëna_pozicioni;}
static int 너비(unsigned kodi_i_karakterit){return kodi_i_karakterit>=196?2:1;}
static int COLUMN(int të_dhëna_pozicioni){int kodi_i_karakterit=0;for(int 순번=Ekzekuto(të_dhëna_pozicioni);순번<të_dhëna_pozicioni;순번=Tjetër_njësi(순번))kodi_i_karakterit+=Teksti[순번]=='\t'?4-kodi_i_karakterit%4:너비(Teksti[순번]);return kodi_i_karakterit;}
static void pikë_kontrolli(void){for(int 순번=0;순번<gjatësi_VALUE;순번++)zhbëj_të_dhëna[순번]=Teksti[순번];zhbëj_gjatësi=gjatësi_VALUE;위쪽=INDEX_VALUE;zhbëj_Ndryshime=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){pikë_kontrolli();for(int 순번=도착위치;순번<gjatësi_VALUE;순번++)Teksti[출발위치+순번-도착위치]=Teksti[순번];gjatësi_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *varg_të_dhëna,int njësi_COUNT){if(njësi_COUNT>편집용량-gjatësi_VALUE){알림문="File full (16384 bytes)";return 0;}pikë_kontrolli();for(int 순번=gjatësi_VALUE-1;순번>=INDEX_VALUE;순번--)Teksti[순번+njësi_COUNT]=Teksti[순번];for(int 순번=0;순번<njësi_COUNT;순번++)Teksti[INDEX_VALUE+순번]=varg_të_dhëna[순번];gjatësi_VALUE+=njësi_COUNT;INDEX_VALUE+=njësi_COUNT;변경됨=1;return 1;}
static void Vertikal(int 차이){int COLUMN_pozicioni=COLUMN(INDEX_VALUE),të_dhëna_pozicioni=Ekzekuto(INDEX_VALUE);if(차이<0){if(!të_dhëna_pozicioni)return;të_dhëna_pozicioni=Ekzekuto(të_dhëna_pozicioni-1);}else{të_dhëna_pozicioni=mbaroj_OFFSET(të_dhëna_pozicioni);if(të_dhëna_pozicioni==gjatësi_VALUE)return;të_dhëna_pozicioni++;}int kodi_i_karakterit=0;while(të_dhëna_pozicioni<gjatësi_VALUE&&Teksti[të_dhëna_pozicioni]!='\n'&&kodi_i_karakterit<COLUMN_pozicioni){kodi_i_karakterit+=Teksti[të_dhëna_pozicioni]=='\t'?4-kodi_i_karakterit%4:너비(Teksti[të_dhëna_pozicioni]);të_dhëna_pozicioni=Tjetër_njësi(të_dhëna_pozicioni);}INDEX_VALUE=të_dhëna_pozicioni;}
static void 화면그리기(void){
    if(INDEX_VALUE>gjatësi_VALUE)INDEX_VALUE=gjatësi_VALUE;if(맨위>INDEX_VALUE)맨위=Ekzekuto(INDEX_VALUE);맨위=Ekzekuto(맨위);
    int ROW_pozicioni=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Teksti[순번]=='\n')ROW_pozicioni++;
    while(ROW_pozicioni>=ROW_COUNT-1){맨위=mbaroj_OFFSET(맨위);if(맨위<gjatësi_VALUE)맨위++;ROW_pozicioni--;}
    int COLUMN_pozicioni=COLUMN(INDEX_VALUE);if(COLUMN_pozicioni<왼쪽)왼쪽=COLUMN_pozicioni;if(COLUMN_pozicioni-왼쪽>=COLUMNS-1)왼쪽=COLUMN_pozicioni-COLUMNS+2;
    글내보내기("\033[?25l");int të_dhëna_pozicioni=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        lëviz_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int kodi_i_karakterit=0,그려진상태=0;
        if(të_dhëna_pozicioni>=gjatësi_VALUE&&반환값>ROW_pozicioni){글내보내기("\033[90m~\033[0m");continue;}
        while(të_dhëna_pozicioni<gjatësi_VALUE&&Teksti[të_dhëna_pozicioni]!='\n'){
            int Tjetër_OFFSET=Tjetër_njësi(të_dhëna_pozicioni),너비값=Teksti[të_dhëna_pozicioni]=='\t'?4-kodi_i_karakterit%4:너비(Teksti[të_dhëna_pozicioni]);
            if(kodi_i_karakterit>=왼쪽&&kodi_i_karakterit-왼쪽+너비값<COLUMNS){
                if(Teksti[të_dhëna_pozicioni]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bajt_të_dhëna(' ');}else if(Teksti[të_dhëna_pozicioni]<32||Teksti[të_dhëna_pozicioni]==127){bajt_të_dhëna('?');}else for(int 안쪽순번=të_dhëna_pozicioni;안쪽순번<Tjetër_OFFSET;안쪽순번++)bajt_të_dhëna(Teksti[안쪽순번]);그려진상태+=너비값;
            }kodi_i_karakterit+=너비값;të_dhëna_pozicioni=Tjetër_OFFSET;
        }
        (void)그려진상태;if(të_dhëna_pozicioni<gjatësi_VALUE)të_dhëna_pozicioni++;
    }
    lëviz_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");status_IMAGE=1;status_radhë=0;글내보내기(ndërfut?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(skedar_futje_emër[이름바이트수]&&이름바이트수<30)bajt_të_dhëna(skedar_futje_emër[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int linjë=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Teksti[순번]=='\n')linjë++;수치(linjë);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int njësi_COUNT=0;글내보내기(" | ");while(알림문[njësi_COUNT]&&njësi_COUNT<20)bajt_të_dhëna(알림문[njësi_COUNT++]);}
    status_IMAGE=0;글내보내기("\033[0m");lëviz_VALUE(ROW_pozicioni+1,COLUMN_pozicioni-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(në_pritje_tast){int 셋째순번=në_pritje_tast;në_pritje_tast=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Madhësi=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Madhësi&65535)||ROW_COUNT!=(int)(Madhësi>>16)){
            COLUMNS=Madhësi&65535;ROW_COUNT=Madhësi>>16;화면그리기();
            if(ndihmë_kategori){lëviz_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bajt_të_dhëna(ndihmë_kategori);글내보내기(Komanda);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){në_pritje_tast=셋째순번;return 27;}
    int njësi_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){njësi_COUNT=njësi_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return njësi_COUNT==3?1007:njësi_COUNT==5?1008:njësi_COUNT==6?1009:njësi_COUNT==1?1005:njësi_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int skedar_dorezë=hap_skedar(skedar_futje_emër,lexoj_shkruaj|없으면만들기|내용비우기,0600);if(skedar_dorezë<0){알림문="Cannot open for save";return 0;}
    intptr_t njësi_COUNT=shkruaj_skedar_të_dhëna(skedar_dorezë,Teksti,gjatësi_VALUE);mbyll_skedar(skedar_dorezë);if(njësi_COUNT!=gjatësi_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Tjetër(void){int njësi_COUNT=0;while(FIND_futje[njësi_COUNT])njësi_COUNT++;if(!njësi_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=gjatësi_VALUE;순번++){int të_dhëna_pozicioni=(INDEX_VALUE+순번)%(gjatësi_VALUE?gjatësi_VALUE:1),안쪽순번=0;while(안쪽순번<njësi_COUNT&&të_dhëna_pozicioni+안쪽순번<gjatësi_VALUE&&Teksti[të_dhëna_pozicioni+안쪽순번]==(unsigned char)FIND_futje[안쪽순번])안쪽순번++;if(안쪽순번==njësi_COUNT){INDEX_VALUE=të_dhëna_pozicioni;알림문="Match";return;}}알림문="Pattern not found";}
static int kërkoj(int kategori_VALUE){
    int njësi_COUNT=0;Komanda[0]=0;
    for(;;){lëviz_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bajt_të_dhëna(kategori_VALUE);글내보내기(Komanda);출력비우기();ndihmë_kategori=kategori_VALUE;int 셋째순번=누름값();ndihmë_kategori=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(njësi_COUNT){njësi_COUNT--;while(njësi_COUNT>0&&((unsigned char)Komanda[njësi_COUNT]&192)==128)njësi_COUNT--;Komanda[njësi_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&njësi_COUNT<120){Komanda[njësi_COUNT++]=셋째순번;Komanda[njësi_COUNT]=0;}
    }
    if(kategori_VALUE=='/'){for(int 순번=0;순번<=njësi_COUNT;순번++)FIND_futje[순번]=Komanda[순번];FIND_Tjetër();return 0;}
    if(같은지(Komanda,"q!"))return 1;
    if(같은지(Komanda,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Komanda,"wq")||같은지(Komanda,"x"))return Store_VALUE();
    if(같은지(Komanda,"w")){Store_VALUE();return 0;}
    if(Komanda[0]=='w'&&Komanda[1]==' '){int 순번=2;while(Komanda[순번]==' ')순번++;int Madhësi=njësi_COUNT-순번;if(Madhësi<1||Madhësi>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Madhësi;안쪽순번++)skedar_futje_emër[안쪽순번]=Komanda[순번+안쪽순번];skedar_futje_emër[Madhësi]=0;Store_VALUE();return 0;}
    int linjë=0;for(int 순번=0;순번<njësi_COUNT;순번++){if(Komanda[순번]<'0'||Komanda[순번]>'9'){linjë=0;break;}linjë=linjë*10+Komanda[순번]-'0';if(linjë>16384){linjë=0;break;}}
    if(linjë){INDEX_VALUE=0;while(--linjë&&INDEX_VALUE<gjatësi_VALUE){INDEX_VALUE=mbaroj_OFFSET(INDEX_VALUE);if(INDEX_VALUE<gjatësi_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int nis_përdorues_program(int 무시값){
    (void)무시값;if(përdorues_argument_COUNT()!=1||përdorues_argument(0,skedar_futje_emër,sizeof(skedar_futje_emër))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int skedar_dorezë=hap_skedar(skedar_futje_emër,vetëm_për_lexim_VALUE,0);
    if(skedar_dorezë>=0){int njësi_COUNT=skedar_ndryshoj_përmasat(skedar_dorezë);if(njësi_COUNT<0||njësi_COUNT>편집용량){mbyll_skedar(skedar_dorezë);return 1;}gjatësi_VALUE=파일자료읽기(skedar_dorezë,Teksti,njësi_COUNT);mbyll_skedar(skedar_dorezë);if(gjatësi_VALUE!=njësi_COUNT)return 1;for(int 순번=0;순번<gjatësi_VALUE;순번++)if(!Teksti[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,mbyll_program=0;
    while(!mbyll_program){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Vertikal(-1);continue;}if(셋째순번==1002){Vertikal(1);continue;}if(셋째순번==1003){INDEX_VALUE=Tjetër_njësi(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Ekzekuto(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=mbaroj_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Vertikal(셋째순번==1008?-1:1);continue;}
        if(ndërfut){
            if(셋째순번==27||셋째순번==3){ndërfut=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<gjatësi_VALUE)바이트지우기(INDEX_VALUE,Tjetër_njësi(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int njësi_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!njësi_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<njësi_COUNT;순번++){int kodi_i_karakterit=누름값();if(kodi_i_karakterit<128||kodi_i_karakterit>191){në_pritje_tast=kodi_i_karakterit;유효함=0;break;}SECOND_VALUE[순번]=kodi_i_karakterit;}
                if(유효함)덧붙이기(SECOND_VALUE,njësi_COUNT);
            }continue;
        }
        if(앞부분){int të_dhëna_pozicioni=앞부분;앞부분=0;if(të_dhëna_pozicioni=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(të_dhëna_pozicioni=='Z'&&셋째순번=='Z'){mbyll_program=Store_VALUE();continue;}if((të_dhëna_pozicioni=='d'&&셋째순번=='d')||(të_dhëna_pozicioni=='y'&&셋째순번=='y')){int 첫째값=Ekzekuto(INDEX_VALUE),SECOND_VALUE=mbaroj_OFFSET(INDEX_VALUE);if(SECOND_VALUE<gjatësi_VALUE)SECOND_VALUE++;kopjoj_gjatësi=SECOND_VALUE-첫째값;for(int 순번=0;순번<kopjoj_gjatësi;순번++)복사자료[순번]=Teksti[첫째값+순번];if(të_dhëna_pozicioni=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){ndërfut=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<mbaroj_OFFSET(INDEX_VALUE))INDEX_VALUE=Tjetër_njësi(INDEX_VALUE);ndërfut=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Ekzekuto(INDEX_VALUE);ndërfut=1;continue;}if(셋째순번=='A'){INDEX_VALUE=mbaroj_OFFSET(INDEX_VALUE);ndërfut=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char linjë_mbaroj='\n';INDEX_VALUE=셋째순번=='o'?mbaroj_OFFSET(INDEX_VALUE):Ekzekuto(INDEX_VALUE);if(덧붙이기(&linjë_mbaroj,1)){if(셋째순번=='O')INDEX_VALUE--;ndërfut=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Tjetër_njësi(INDEX_VALUE);continue;}if(셋째순번=='j'){Vertikal(1);continue;}if(셋째순번=='k'){Vertikal(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Ekzekuto(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=mbaroj_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Ekzekuto(gjatësi_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<gjatësi_VALUE)바이트지우기(INDEX_VALUE,Tjetër_njësi(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&kopjoj_gjatësi){INDEX_VALUE=mbaroj_OFFSET(INDEX_VALUE);if(INDEX_VALUE<gjatësi_VALUE)INDEX_VALUE++;덧붙이기(복사자료,kopjoj_gjatësi);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=Teksti[순번];Teksti[순번]=zhbëj_të_dhëna[순번];zhbëj_të_dhëna[순번]=SECOND_VALUE;}int njësi_COUNT=gjatësi_VALUE;gjatësi_VALUE=zhbëj_gjatësi;zhbëj_gjatësi=njësi_COUNT;njësi_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=njësi_COUNT;njësi_COUNT=변경됨;변경됨=zhbëj_Ndryshime;zhbëj_Ndryshime=njësi_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){mbyll_program=kërkoj(셋째순번);continue;}if(셋째순번=='n'){FIND_Tjetër();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
