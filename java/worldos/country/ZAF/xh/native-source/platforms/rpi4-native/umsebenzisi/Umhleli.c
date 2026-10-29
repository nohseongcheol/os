/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Umbhalo[편집용량],cima_okwenzekileyo_iingcombolo[편집용량],복사자료[편집용량],결과자료[1024];
static int ubude_ixabiso,indeksa_ixabiso,맨위,왼쪽,변경됨,faka,cima_okwenzekileyo_ubude,위쪽,cima_okwenzekileyo_Iinguquko,되돌림있음,kopa_ubude,사용량,열수=68,행수=19;
static char ifayile_ufako_nkcukacha_igama[64],Umyalelo[128],fumana_ufako_nkcukacha[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned ilindile_iqhosha;
static int uncedo_udidi,imo_umfanekiso,imo_ityhu;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void ibhayithi_iingcombolo(unsigned ikhowudi_yekharakhtha){if(imo_umfanekiso){if((ikhowudi_yekharakhtha&192)!=128){imo_ityhu+=ikhowudi_yekharakhtha>=196?2:1;}if(imo_ityhu>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=ikhowudi_yekharakhtha;}
static void 글내보내기(const char *uluhlu_lweekharektha_iingcombolo){while(*uluhlu_lweekharektha_iingcombolo)ibhayithi_iingcombolo((unsigned char)*uluhlu_lweekharektha_iingcombolo++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)ibhayithi_iingcombolo(둘째값[--순번]);}
static void fudusa_ixabiso(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);ibhayithi_iingcombolo(';');수치(열위치);ibhayithi_iingcombolo('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(Umbhalo[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<ubude_ixabiso){자료위치++;while(자료위치<ubude_ixabiso&&(Umbhalo[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int Phumeza(int 자료위치){while(자료위치>0&&Umbhalo[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int phela_Ukulinganisa(int 자료위치){while(자료위치<ubude_ixabiso&&Umbhalo[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned ikhowudi_yekharakhtha){return ikhowudi_yekharakhtha>=196?2:1;}
static int ikholam(int 자료위치){int ikhowudi_yekharakhtha=0;for(int 순번=Phumeza(자료위치);순번<자료위치;순번=다음(순번))ikhowudi_yekharakhtha+=Umbhalo[순번]=='\t'?4-ikhowudi_yekharakhtha%4:너비(Umbhalo[순번]);return ikhowudi_yekharakhtha;}
static void itshekhpoyinti(void){for(int 순번=0;순번<ubude_ixabiso;순번++)cima_okwenzekileyo_iingcombolo[순번]=Umbhalo[순번];cima_okwenzekileyo_ubude=ubude_ixabiso;위쪽=indeksa_ixabiso;cima_okwenzekileyo_Iinguquko=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){itshekhpoyinti();for(int 순번=도착위치;순번<ubude_ixabiso;순번++)Umbhalo[출발위치+순번-도착위치]=Umbhalo[순번];ubude_ixabiso-=도착위치-출발위치;indeksa_ixabiso=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *uluhlu_lweekharektha_iingcombolo,int 개수){if(개수>편집용량-ubude_ixabiso){알림문="File full (16384 bytes)";return 0;}itshekhpoyinti();for(int 순번=ubude_ixabiso-1;순번>=indeksa_ixabiso;순번--)Umbhalo[순번+개수]=Umbhalo[순번];for(int 순번=0;순번<개수;순번++)Umbhalo[indeksa_ixabiso+순번]=uluhlu_lweekharektha_iingcombolo[순번];ubude_ixabiso+=개수;indeksa_ixabiso+=개수;변경됨=1;return 1;}
static void Ethe_nkqo(int 차이){int 열위치=ikholam(indeksa_ixabiso),자료위치=Phumeza(indeksa_ixabiso);if(차이<0){if(!자료위치)return;자료위치=Phumeza(자료위치-1);}else{자료위치=phela_Ukulinganisa(자료위치);if(자료위치==ubude_ixabiso)return;자료위치++;}int ikhowudi_yekharakhtha=0;while(자료위치<ubude_ixabiso&&Umbhalo[자료위치]!='\n'&&ikhowudi_yekharakhtha<열위치){ikhowudi_yekharakhtha+=Umbhalo[자료위치]=='\t'?4-ikhowudi_yekharakhtha%4:너비(Umbhalo[자료위치]);자료위치=다음(자료위치);}indeksa_ixabiso=자료위치;}
static void 화면그리기(void){
    if(indeksa_ixabiso>ubude_ixabiso)indeksa_ixabiso=ubude_ixabiso;if(맨위>indeksa_ixabiso)맨위=Phumeza(indeksa_ixabiso);맨위=Phumeza(맨위);
    int 행위치=0;for(int 순번=맨위;순번<indeksa_ixabiso;순번++)if(Umbhalo[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=phela_Ukulinganisa(맨위);if(맨위<ubude_ixabiso)맨위++;행위치--;}
    int 열위치=ikholam(indeksa_ixabiso);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        fudusa_ixabiso(반환값+1,1);글내보내기("\033[0m\033[2K");int ikhowudi_yekharakhtha=0,그려진상태=0;
        if(자료위치>=ubude_ixabiso&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<ubude_ixabiso&&Umbhalo[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=Umbhalo[자료위치]=='\t'?4-ikhowudi_yekharakhtha%4:너비(Umbhalo[자료위치]);
            if(ikhowudi_yekharakhtha>=왼쪽&&ikhowudi_yekharakhtha-왼쪽+너비값<열수){
                if(Umbhalo[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)ibhayithi_iingcombolo(' ');}else if(Umbhalo[자료위치]<32||Umbhalo[자료위치]==127){ibhayithi_iingcombolo('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)ibhayithi_iingcombolo(Umbhalo[안쪽순번]);그려진상태+=너비값;
            }ikhowudi_yekharakhtha+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<ubude_ixabiso)자료위치++;
    }
    fudusa_ixabiso(행수,1);글내보내기("\033[7m\033[2K");imo_umfanekiso=1;imo_ityhu=0;글내보내기(faka?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(ifayile_ufako_nkcukacha_igama[이름바이트수]&&이름바이트수<30)ibhayithi_iingcombolo(ifayile_ufako_nkcukacha_igama[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int umgca=1;for(int 순번=0;순번<indeksa_ixabiso;순번++)if(Umbhalo[순번]=='\n')umgca++;수치(umgca);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)ibhayithi_iingcombolo(알림문[개수++]);}
    imo_umfanekiso=0;글내보내기("\033[0m");fudusa_ixabiso(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(ilindile_iqhosha){int 셋째순번=ilindile_iqhosha;ilindile_iqhosha=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Ubukhulu=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(Ubukhulu&65535)||행수!=(int)(Ubukhulu>>16)){
            열수=Ubukhulu&65535;행수=Ubukhulu>>16;화면그리기();
            if(uncedo_udidi){fudusa_ixabiso(행수,1);글내보내기("\033[0m\033[2K");ibhayithi_iingcombolo(uncedo_udidi);글내보내기(Umyalelo);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){ilindile_iqhosha=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int Store_ixabiso(void){
    int ifayile_isibambi=vula_ifayile(ifayile_ufako_nkcukacha_igama,funda_bhala|없으면만들기|내용비우기,0600);if(ifayile_isibambi<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=bhala_ifayile_iingcombolo(ifayile_isibambi,Umbhalo,ubude_ixabiso);vala_ifayile(ifayile_isibambi);if(개수!=ubude_ixabiso){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(fumana_ufako_nkcukacha[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=ubude_ixabiso;순번++){int 자료위치=(indeksa_ixabiso+순번)%(ubude_ixabiso?ubude_ixabiso:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<ubude_ixabiso&&Umbhalo[자료위치+안쪽순번]==(unsigned char)fumana_ufako_nkcukacha[안쪽순번])안쪽순번++;if(안쪽순번==개수){indeksa_ixabiso=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int imo_yokulinda(int udidi_ixabiso){
    int 개수=0;Umyalelo[0]=0;
    for(;;){fudusa_ixabiso(행수,1);글내보내기("\033[0m\033[2K");ibhayithi_iingcombolo(udidi_ixabiso);글내보내기(Umyalelo);출력비우기();uncedo_udidi=udidi_ixabiso;int 셋째순번=누름값();uncedo_udidi=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)Umyalelo[개수]&192)==128)개수--;Umyalelo[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){Umyalelo[개수++]=셋째순번;Umyalelo[개수]=0;}
    }
    if(udidi_ixabiso=='/'){for(int 순번=0;순번<=개수;순번++)fumana_ufako_nkcukacha[순번]=Umyalelo[순번];다음찾기();return 0;}
    if(같은지(Umyalelo,"q!"))return 1;
    if(같은지(Umyalelo,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Umyalelo,"wq")||같은지(Umyalelo,"x"))return Store_ixabiso();
    if(같은지(Umyalelo,"w")){Store_ixabiso();return 0;}
    if(Umyalelo[0]=='w'&&Umyalelo[1]==' '){int 순번=2;while(Umyalelo[순번]==' ')순번++;int Ubukhulu=개수-순번;if(Ubukhulu<1||Ubukhulu>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Ubukhulu;안쪽순번++)ifayile_ufako_nkcukacha_igama[안쪽순번]=Umyalelo[순번+안쪽순번];ifayile_ufako_nkcukacha_igama[Ubukhulu]=0;Store_ixabiso();return 0;}
    int umgca=0;for(int 순번=0;순번<개수;순번++){if(Umyalelo[순번]<'0'||Umyalelo[순번]>'9'){umgca=0;break;}umgca=umgca*10+Umyalelo[순번]-'0';if(umgca>16384){umgca=0;break;}}
    if(umgca){indeksa_ixabiso=0;while(--umgca&&indeksa_ixabiso<ubude_ixabiso){indeksa_ixabiso=phela_Ukulinganisa(indeksa_ixabiso);if(indeksa_ixabiso<ubude_ixabiso)indeksa_ixabiso++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int qala_umsebenzisi_inkqubo(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||umsebenzisi_isiniki_myalelo(0,ifayile_ufako_nkcukacha_igama,sizeof(ifayile_ufako_nkcukacha_igama))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int ifayile_isibambi=vula_ifayile(ifayile_ufako_nkcukacha_igama,efundwayo_kuphela_ixabiso,0);
    if(ifayile_isibambi>=0){int 개수=ifayile_isayizi(ifayile_isibambi);if(개수<0||개수>편집용량){vala_ifayile(ifayile_isibambi);return 1;}ubude_ixabiso=파일자료읽기(ifayile_isibambi,Umbhalo,개수);vala_ifayile(ifayile_isibambi);if(ubude_ixabiso!=개수)return 1;for(int 순번=0;순번<ubude_ixabiso;순번++)if(!Umbhalo[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Ethe_nkqo(-1);continue;}if(셋째순번==1002){Ethe_nkqo(1);continue;}if(셋째순번==1003){indeksa_ixabiso=다음(indeksa_ixabiso);continue;}if(셋째순번==1004){indeksa_ixabiso=이전항목(indeksa_ixabiso);continue;}
        if(셋째순번==1005){indeksa_ixabiso=Phumeza(indeksa_ixabiso);continue;}if(셋째순번==1006){indeksa_ixabiso=phela_Ukulinganisa(indeksa_ixabiso);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)Ethe_nkqo(셋째순번==1008?-1:1);continue;}
        if(faka){
            if(셋째순번==27||셋째순번==3){faka=0;continue;}
            if(셋째순번==127||셋째순번==8){if(indeksa_ixabiso)바이트지우기(이전항목(indeksa_ixabiso),indeksa_ixabiso);continue;}
            if(셋째순번==1007){if(indeksa_ixabiso<ubude_ixabiso)바이트지우기(indeksa_ixabiso,다음(indeksa_ixabiso));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int ikhowudi_yekharakhtha=누름값();if(ikhowudi_yekharakhtha<128||ikhowudi_yekharakhtha>191){ilindile_iqhosha=ikhowudi_yekharakhtha;유효함=0;break;}둘째값[순번]=ikhowudi_yekharakhtha;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){indeksa_ixabiso=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=Store_ixabiso();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=Phumeza(indeksa_ixabiso),둘째값=phela_Ukulinganisa(indeksa_ixabiso);if(둘째값<ubude_ixabiso)둘째값++;kopa_ubude=둘째값-첫째값;for(int 순번=0;순번<kopa_ubude;순번++)복사자료[순번]=Umbhalo[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){faka=1;continue;}if(셋째순번=='a'){if(indeksa_ixabiso<phela_Ukulinganisa(indeksa_ixabiso))indeksa_ixabiso=다음(indeksa_ixabiso);faka=1;continue;}
        if(셋째순번=='I'){indeksa_ixabiso=Phumeza(indeksa_ixabiso);faka=1;continue;}if(셋째순번=='A'){indeksa_ixabiso=phela_Ukulinganisa(indeksa_ixabiso);faka=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char umgca_phela='\n';indeksa_ixabiso=셋째순번=='o'?phela_Ukulinganisa(indeksa_ixabiso):Phumeza(indeksa_ixabiso);if(덧붙이기(&umgca_phela,1)){if(셋째순번=='O')indeksa_ixabiso--;faka=1;}continue;}
        if(셋째순번=='h'){indeksa_ixabiso=이전항목(indeksa_ixabiso);continue;}if(셋째순번=='l'){indeksa_ixabiso=다음(indeksa_ixabiso);continue;}if(셋째순번=='j'){Ethe_nkqo(1);continue;}if(셋째순번=='k'){Ethe_nkqo(-1);continue;}
        if(셋째순번=='0'){indeksa_ixabiso=Phumeza(indeksa_ixabiso);continue;}if(셋째순번=='$'){indeksa_ixabiso=phela_Ukulinganisa(indeksa_ixabiso);continue;}if(셋째순번=='G'){indeksa_ixabiso=Phumeza(ubude_ixabiso);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(indeksa_ixabiso<ubude_ixabiso)바이트지우기(indeksa_ixabiso,다음(indeksa_ixabiso));continue;}
        if(셋째순번=='p'&&kopa_ubude){indeksa_ixabiso=phela_Ukulinganisa(indeksa_ixabiso);if(indeksa_ixabiso<ubude_ixabiso)indeksa_ixabiso++;덧붙이기(복사자료,kopa_ubude);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=Umbhalo[순번];Umbhalo[순번]=cima_okwenzekileyo_iingcombolo[순번];cima_okwenzekileyo_iingcombolo[순번]=둘째값;}int 개수=ubude_ixabiso;ubude_ixabiso=cima_okwenzekileyo_ubude;cima_okwenzekileyo_ubude=개수;개수=indeksa_ixabiso;indeksa_ixabiso=위쪽;위쪽=개수;개수=변경됨;변경됨=cima_okwenzekileyo_Iinguquko;cima_okwenzekileyo_Iinguquko=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=imo_yokulinda(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
