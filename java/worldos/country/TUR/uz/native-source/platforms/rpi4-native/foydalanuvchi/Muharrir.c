/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Matn[편집용량],되돌림자료[편집용량],복사자료[편집용량],o_lchov_ma_lumotlar[1024];
static int uzunlik_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,qo_shib_qo_ymoq,되돌림길이,위쪽,되돌림변경,되돌림있음,namuna_uzunlik,사용량,COLUMNS=68,ROW_COUNT=19;
static char fayl_kiritish_nom[64],Buyruq[128],FIND_kiritish[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned 대기누름;
static int yordam_toifa,holat_rasm,holat_navbat;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)o_lchov_ma_lumotlar,사용량,0,0,0);사용량=0;}}
static void bayt_ma_lumotlar(unsigned belgi_kodi){if(holat_rasm){if((belgi_kodi&192)!=128){holat_navbat+=belgi_kodi>=196?2:1;}if(holat_navbat>=COLUMNS)return;}if(사용량==(int)sizeof(o_lchov_ma_lumotlar))출력비우기();o_lchov_ma_lumotlar[사용량++]=belgi_kodi;}
static void 글내보내기(const char *satr_ma_lumotlar){while(*satr_ma_lumotlar)bayt_ma_lumotlar((unsigned char)*satr_ma_lumotlar++);}
static void 수치(unsigned element_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+element_COUNT%10;element_COUNT/=10;}while(element_COUNT);while(순번)bayt_ma_lumotlar(SECOND_VALUE[--순번]);}
static void ko_chirmoq_VALUE(int ROW_holat,int ustun_holat){글내보내기("\033[");수치(ROW_holat);bayt_ma_lumotlar(';');수치(ustun_holat);bayt_ma_lumotlar('H');}
static int 이전항목(int ma_lumotlar_holat){if(ma_lumotlar_holat){ma_lumotlar_holat--;while(ma_lumotlar_holat>0&&(Matn[ma_lumotlar_holat]&192)==128)ma_lumotlar_holat--;}return ma_lumotlar_holat;}
static int Keyingi_element(int ma_lumotlar_holat){if(ma_lumotlar_holat<uzunlik_VALUE){ma_lumotlar_holat++;while(ma_lumotlar_holat<uzunlik_VALUE&&(Matn[ma_lumotlar_holat]&192)==128)ma_lumotlar_holat++;}return ma_lumotlar_holat;}
static int Bajarish(int ma_lumotlar_holat){while(ma_lumotlar_holat>0&&Matn[ma_lumotlar_holat-1]!='\n')ma_lumotlar_holat--;return ma_lumotlar_holat;}
static int to_xtatmoq_OFFSET(int ma_lumotlar_holat){while(ma_lumotlar_holat<uzunlik_VALUE&&Matn[ma_lumotlar_holat]!='\n')ma_lumotlar_holat++;return ma_lumotlar_holat;}
static int 너비(unsigned belgi_kodi){return belgi_kodi>=196?2:1;}
static int ustun(int ma_lumotlar_holat){int belgi_kodi=0;for(int 순번=Bajarish(ma_lumotlar_holat);순번<ma_lumotlar_holat;순번=Keyingi_element(순번))belgi_kodi+=Matn[순번]=='\t'?4-belgi_kodi%4:너비(Matn[순번]);return belgi_kodi;}
static void nazorat_nuqtasi(void){for(int 순번=0;순번<uzunlik_VALUE;순번++)되돌림자료[순번]=Matn[순번];되돌림길이=uzunlik_VALUE;위쪽=INDEX_VALUE;되돌림변경=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){nazorat_nuqtasi();for(int 순번=도착위치;순번<uzunlik_VALUE;순번++)Matn[출발위치+순번-도착위치]=Matn[순번];uzunlik_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *satr_ma_lumotlar,int element_COUNT){if(element_COUNT>편집용량-uzunlik_VALUE){알림문="File full (16384 bytes)";return 0;}nazorat_nuqtasi();for(int 순번=uzunlik_VALUE-1;순번>=INDEX_VALUE;순번--)Matn[순번+element_COUNT]=Matn[순번];for(int 순번=0;순번<element_COUNT;순번++)Matn[INDEX_VALUE+순번]=satr_ma_lumotlar[순번];uzunlik_VALUE+=element_COUNT;INDEX_VALUE+=element_COUNT;변경됨=1;return 1;}
static void Vertikal(int 차이){int ustun_holat=ustun(INDEX_VALUE),ma_lumotlar_holat=Bajarish(INDEX_VALUE);if(차이<0){if(!ma_lumotlar_holat)return;ma_lumotlar_holat=Bajarish(ma_lumotlar_holat-1);}else{ma_lumotlar_holat=to_xtatmoq_OFFSET(ma_lumotlar_holat);if(ma_lumotlar_holat==uzunlik_VALUE)return;ma_lumotlar_holat++;}int belgi_kodi=0;while(ma_lumotlar_holat<uzunlik_VALUE&&Matn[ma_lumotlar_holat]!='\n'&&belgi_kodi<ustun_holat){belgi_kodi+=Matn[ma_lumotlar_holat]=='\t'?4-belgi_kodi%4:너비(Matn[ma_lumotlar_holat]);ma_lumotlar_holat=Keyingi_element(ma_lumotlar_holat);}INDEX_VALUE=ma_lumotlar_holat;}
static void 화면그리기(void){
    if(INDEX_VALUE>uzunlik_VALUE)INDEX_VALUE=uzunlik_VALUE;if(맨위>INDEX_VALUE)맨위=Bajarish(INDEX_VALUE);맨위=Bajarish(맨위);
    int ROW_holat=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Matn[순번]=='\n')ROW_holat++;
    while(ROW_holat>=ROW_COUNT-1){맨위=to_xtatmoq_OFFSET(맨위);if(맨위<uzunlik_VALUE)맨위++;ROW_holat--;}
    int ustun_holat=ustun(INDEX_VALUE);if(ustun_holat<왼쪽)왼쪽=ustun_holat;if(ustun_holat-왼쪽>=COLUMNS-1)왼쪽=ustun_holat-COLUMNS+2;
    글내보내기("\033[?25l");int ma_lumotlar_holat=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        ko_chirmoq_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int belgi_kodi=0,그려진상태=0;
        if(ma_lumotlar_holat>=uzunlik_VALUE&&반환값>ROW_holat){글내보내기("\033[90m~\033[0m");continue;}
        while(ma_lumotlar_holat<uzunlik_VALUE&&Matn[ma_lumotlar_holat]!='\n'){
            int Keyingi_OFFSET=Keyingi_element(ma_lumotlar_holat),너비값=Matn[ma_lumotlar_holat]=='\t'?4-belgi_kodi%4:너비(Matn[ma_lumotlar_holat]);
            if(belgi_kodi>=왼쪽&&belgi_kodi-왼쪽+너비값<COLUMNS){
                if(Matn[ma_lumotlar_holat]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bayt_ma_lumotlar(' ');}else if(Matn[ma_lumotlar_holat]<32||Matn[ma_lumotlar_holat]==127){bayt_ma_lumotlar('?');}else for(int 안쪽순번=ma_lumotlar_holat;안쪽순번<Keyingi_OFFSET;안쪽순번++)bayt_ma_lumotlar(Matn[안쪽순번]);그려진상태+=너비값;
            }belgi_kodi+=너비값;ma_lumotlar_holat=Keyingi_OFFSET;
        }
        (void)그려진상태;if(ma_lumotlar_holat<uzunlik_VALUE)ma_lumotlar_holat++;
    }
    ko_chirmoq_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");holat_rasm=1;holat_navbat=0;글내보내기(qo_shib_qo_ymoq?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(fayl_kiritish_nom[이름바이트수]&&이름바이트수<30)bayt_ma_lumotlar(fayl_kiritish_nom[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int satr=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Matn[순번]=='\n')satr++;수치(satr);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int element_COUNT=0;글내보내기(" | ");while(알림문[element_COUNT]&&element_COUNT<20)bayt_ma_lumotlar(알림문[element_COUNT++]);}
    holat_rasm=0;글내보내기("\033[0m");ko_chirmoq_VALUE(ROW_holat+1,ustun_holat-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(대기누름){int 셋째순번=대기누름;대기누름=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Hajmi=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Hajmi&65535)||ROW_COUNT!=(int)(Hajmi>>16)){
            COLUMNS=Hajmi&65535;ROW_COUNT=Hajmi>>16;화면그리기();
            if(yordam_toifa){ko_chirmoq_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bayt_ma_lumotlar(yordam_toifa);글내보내기(Buyruq);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){대기누름=셋째순번;return 27;}
    int element_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){element_COUNT=element_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return element_COUNT==3?1007:element_COUNT==5?1008:element_COUNT==6?1009:element_COUNT==1?1005:element_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int fayl_deskriptor=ochmoq_fayl(fayl_kiritish_nom,o_qish_yozish_mumkin|없으면만들기|내용비우기,0600);if(fayl_deskriptor<0){알림문="Cannot open for save";return 0;}
    intptr_t element_COUNT=yozmoq_fayl_ma_lumotlar(fayl_deskriptor,Matn,uzunlik_VALUE);yopmoq_fayl(fayl_deskriptor);if(element_COUNT!=uzunlik_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Keyingi(void){int element_COUNT=0;while(FIND_kiritish[element_COUNT])element_COUNT++;if(!element_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=uzunlik_VALUE;순번++){int ma_lumotlar_holat=(INDEX_VALUE+순번)%(uzunlik_VALUE?uzunlik_VALUE:1),안쪽순번=0;while(안쪽순번<element_COUNT&&ma_lumotlar_holat+안쪽순번<uzunlik_VALUE&&Matn[ma_lumotlar_holat+안쪽순번]==(unsigned char)FIND_kiritish[안쪽순번])안쪽순번++;if(안쪽순번==element_COUNT){INDEX_VALUE=ma_lumotlar_holat;알림문="Match";return;}}알림문="Pattern not found";}
static int so_rov(int toifa_VALUE){
    int element_COUNT=0;Buyruq[0]=0;
    for(;;){ko_chirmoq_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bayt_ma_lumotlar(toifa_VALUE);글내보내기(Buyruq);출력비우기();yordam_toifa=toifa_VALUE;int 셋째순번=누름값();yordam_toifa=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(element_COUNT){element_COUNT--;while(element_COUNT>0&&((unsigned char)Buyruq[element_COUNT]&192)==128)element_COUNT--;Buyruq[element_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&element_COUNT<120){Buyruq[element_COUNT++]=셋째순번;Buyruq[element_COUNT]=0;}
    }
    if(toifa_VALUE=='/'){for(int 순번=0;순번<=element_COUNT;순번++)FIND_kiritish[순번]=Buyruq[순번];FIND_Keyingi();return 0;}
    if(같은지(Buyruq,"q!"))return 1;
    if(같은지(Buyruq,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Buyruq,"wq")||같은지(Buyruq,"x"))return Store_VALUE();
    if(같은지(Buyruq,"w")){Store_VALUE();return 0;}
    if(Buyruq[0]=='w'&&Buyruq[1]==' '){int 순번=2;while(Buyruq[순번]==' ')순번++;int Hajmi=element_COUNT-순번;if(Hajmi<1||Hajmi>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Hajmi;안쪽순번++)fayl_kiritish_nom[안쪽순번]=Buyruq[순번+안쪽순번];fayl_kiritish_nom[Hajmi]=0;Store_VALUE();return 0;}
    int satr=0;for(int 순번=0;순번<element_COUNT;순번++){if(Buyruq[순번]<'0'||Buyruq[순번]>'9'){satr=0;break;}satr=satr*10+Buyruq[순번]-'0';if(satr>16384){satr=0;break;}}
    if(satr){INDEX_VALUE=0;while(--satr&&INDEX_VALUE<uzunlik_VALUE){INDEX_VALUE=to_xtatmoq_OFFSET(INDEX_VALUE);if(INDEX_VALUE<uzunlik_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Start_foydalanuvchi_ilova(int 무시값){
    (void)무시값;if(foydalanuvchi_dalil_COUNT()!=1||foydalanuvchi_dalil(0,fayl_kiritish_nom,sizeof(fayl_kiritish_nom))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int fayl_deskriptor=ochmoq_fayl(fayl_kiritish_nom,faqat_o_qish_uchun_VALUE,0);
    if(fayl_deskriptor>=0){int element_COUNT=fayl_o_lcham(fayl_deskriptor);if(element_COUNT<0||element_COUNT>편집용량){yopmoq_fayl(fayl_deskriptor);return 1;}uzunlik_VALUE=파일자료읽기(fayl_deskriptor,Matn,element_COUNT);yopmoq_fayl(fayl_deskriptor);if(uzunlik_VALUE!=element_COUNT)return 1;for(int 순번=0;순번<uzunlik_VALUE;순번++)if(!Matn[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,tugatish_ilova=0;
    while(!tugatish_ilova){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Vertikal(-1);continue;}if(셋째순번==1002){Vertikal(1);continue;}if(셋째순번==1003){INDEX_VALUE=Keyingi_element(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Bajarish(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=to_xtatmoq_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Vertikal(셋째순번==1008?-1:1);continue;}
        if(qo_shib_qo_ymoq){
            if(셋째순번==27||셋째순번==3){qo_shib_qo_ymoq=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<uzunlik_VALUE)바이트지우기(INDEX_VALUE,Keyingi_element(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int element_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!element_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<element_COUNT;순번++){int belgi_kodi=누름값();if(belgi_kodi<128||belgi_kodi>191){대기누름=belgi_kodi;유효함=0;break;}SECOND_VALUE[순번]=belgi_kodi;}
                if(유효함)덧붙이기(SECOND_VALUE,element_COUNT);
            }continue;
        }
        if(앞부분){int ma_lumotlar_holat=앞부분;앞부분=0;if(ma_lumotlar_holat=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(ma_lumotlar_holat=='Z'&&셋째순번=='Z'){tugatish_ilova=Store_VALUE();continue;}if((ma_lumotlar_holat=='d'&&셋째순번=='d')||(ma_lumotlar_holat=='y'&&셋째순번=='y')){int 첫째값=Bajarish(INDEX_VALUE),SECOND_VALUE=to_xtatmoq_OFFSET(INDEX_VALUE);if(SECOND_VALUE<uzunlik_VALUE)SECOND_VALUE++;namuna_uzunlik=SECOND_VALUE-첫째값;for(int 순번=0;순번<namuna_uzunlik;순번++)복사자료[순번]=Matn[첫째값+순번];if(ma_lumotlar_holat=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){qo_shib_qo_ymoq=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<to_xtatmoq_OFFSET(INDEX_VALUE))INDEX_VALUE=Keyingi_element(INDEX_VALUE);qo_shib_qo_ymoq=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Bajarish(INDEX_VALUE);qo_shib_qo_ymoq=1;continue;}if(셋째순번=='A'){INDEX_VALUE=to_xtatmoq_OFFSET(INDEX_VALUE);qo_shib_qo_ymoq=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char satr_to_xtatmoq='\n';INDEX_VALUE=셋째순번=='o'?to_xtatmoq_OFFSET(INDEX_VALUE):Bajarish(INDEX_VALUE);if(덧붙이기(&satr_to_xtatmoq,1)){if(셋째순번=='O')INDEX_VALUE--;qo_shib_qo_ymoq=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Keyingi_element(INDEX_VALUE);continue;}if(셋째순번=='j'){Vertikal(1);continue;}if(셋째순번=='k'){Vertikal(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Bajarish(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=to_xtatmoq_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Bajarish(uzunlik_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<uzunlik_VALUE)바이트지우기(INDEX_VALUE,Keyingi_element(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&namuna_uzunlik){INDEX_VALUE=to_xtatmoq_OFFSET(INDEX_VALUE);if(INDEX_VALUE<uzunlik_VALUE)INDEX_VALUE++;덧붙이기(복사자료,namuna_uzunlik);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=Matn[순번];Matn[순번]=되돌림자료[순번];되돌림자료[순번]=SECOND_VALUE;}int element_COUNT=uzunlik_VALUE;uzunlik_VALUE=되돌림길이;되돌림길이=element_COUNT;element_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=element_COUNT;element_COUNT=변경됨;변경됨=되돌림변경;되돌림변경=element_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){tugatish_ilova=so_rov(셋째순번);continue;}if(셋째순번=='n'){FIND_Keyingi();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
