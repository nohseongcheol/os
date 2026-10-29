/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Tekst[편집용량],jamonoy_dekkal_mbir[편집용량],복사자료[편집용량],결과자료[1024];
static int diir_xëyma,àlluwa_tur_xëyma,맨위,왼쪽,변경됨,dugal,jamonoy_dekkal_diir,위쪽,jamonoy_dekkal_Coppite_yi,되돌림있음,mbokk_diir,사용량,열수=68,행수=19;
static char bara_denc_dugal_xabaar_tur[64],ndigel[128],seet_dugal_xabaar[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned xaarandi_kër;
static int ndimbal_ngiir,nekkin_nataal,nekkin_Topplante_xaarandi;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)결과자료,사용량,0,0,0);사용량=0;}}
static void okte_mbir(unsigned kotu_araf){if(nekkin_nataal){if((kotu_araf&192)!=128){nekkin_Topplante_xaarandi+=kotu_araf>=196?2:1;}if(nekkin_Topplante_xaarandi>=열수)return;}if(사용량==(int)sizeof(결과자료))출력비우기();결과자료[사용량++]=kotu_araf;}
static void 글내보내기(const char *araf_yu_bennoo_mbir){while(*araf_yu_bennoo_mbir)okte_mbir((unsigned char)*araf_yu_bennoo_mbir++);}
static void 수치(unsigned 개수){char 둘째값[12];int 순번=0;do{둘째값[순번++]='0'+개수%10;개수/=10;}while(개수);while(순번)okte_mbir(둘째값[--순번]);}
static void toxal_xëyma(int 행위치,int 열위치){글내보내기("\033[");수치(행위치);okte_mbir(';');수치(열위치);okte_mbir('H');}
static int 이전항목(int 자료위치){if(자료위치){자료위치--;while(자료위치>0&&(Tekst[자료위치]&192)==128)자료위치--;}return 자료위치;}
static int 다음(int 자료위치){if(자료위치<diir_xëyma){자료위치++;while(자료위치<diir_xëyma&&(Tekst[자료위치]&192)==128)자료위치++;}return 자료위치;}
static int daw(int 자료위치){while(자료위치>0&&Tekst[자료위치-1]!='\n')자료위치--;return 자료위치;}
static int jeexal_Randal(int 자료위치){while(자료위치<diir_xëyma&&Tekst[자료위치]!='\n')자료위치++;return 자료위치;}
static int 너비(unsigned kotu_araf){return kotu_araf>=196?2:1;}
static int Jen(int 자료위치){int kotu_araf=0;for(int 순번=daw(자료위치);순번<자료위치;순번=다음(순번))kotu_araf+=Tekst[순번]=='\t'?4-kotu_araf%4:너비(Tekst[순번]);return kotu_araf;}
static void barabu_caytu(void){for(int 순번=0;순번<diir_xëyma;순번++)jamonoy_dekkal_mbir[순번]=Tekst[순번];jamonoy_dekkal_diir=diir_xëyma;위쪽=àlluwa_tur_xëyma;jamonoy_dekkal_Coppite_yi=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){barabu_caytu();for(int 순번=도착위치;순번<diir_xëyma;순번++)Tekst[출발위치+순번-도착위치]=Tekst[순번];diir_xëyma-=도착위치-출발위치;àlluwa_tur_xëyma=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *araf_yu_bennoo_mbir,int 개수){if(개수>편집용량-diir_xëyma){알림문="File full (16384 bytes)";return 0;}barabu_caytu();for(int 순번=diir_xëyma-1;순번>=àlluwa_tur_xëyma;순번--)Tekst[순번+개수]=Tekst[순번];for(int 순번=0;순번<개수;순번++)Tekst[àlluwa_tur_xëyma+순번]=araf_yu_bennoo_mbir[순번];diir_xëyma+=개수;àlluwa_tur_xëyma+=개수;변경됨=1;return 1;}
static void Taxaw(int 차이){int 열위치=Jen(àlluwa_tur_xëyma),자료위치=daw(àlluwa_tur_xëyma);if(차이<0){if(!자료위치)return;자료위치=daw(자료위치-1);}else{자료위치=jeexal_Randal(자료위치);if(자료위치==diir_xëyma)return;자료위치++;}int kotu_araf=0;while(자료위치<diir_xëyma&&Tekst[자료위치]!='\n'&&kotu_araf<열위치){kotu_araf+=Tekst[자료위치]=='\t'?4-kotu_araf%4:너비(Tekst[자료위치]);자료위치=다음(자료위치);}àlluwa_tur_xëyma=자료위치;}
static void 화면그리기(void){
    if(àlluwa_tur_xëyma>diir_xëyma)àlluwa_tur_xëyma=diir_xëyma;if(맨위>àlluwa_tur_xëyma)맨위=daw(àlluwa_tur_xëyma);맨위=daw(맨위);
    int 행위치=0;for(int 순번=맨위;순번<àlluwa_tur_xëyma;순번++)if(Tekst[순번]=='\n')행위치++;
    while(행위치>=행수-1){맨위=jeexal_Randal(맨위);if(맨위<diir_xëyma)맨위++;행위치--;}
    int 열위치=Jen(àlluwa_tur_xëyma);if(열위치<왼쪽)왼쪽=열위치;if(열위치-왼쪽>=열수-1)왼쪽=열위치-열수+2;
    글내보내기("\033[?25l");int 자료위치=맨위;
    for(int 반환값=0;반환값<행수-1;반환값++){
        toxal_xëyma(반환값+1,1);글내보내기("\033[0m\033[2K");int kotu_araf=0,그려진상태=0;
        if(자료위치>=diir_xëyma&&반환값>행위치){글내보내기("\033[90m~\033[0m");continue;}
        while(자료위치<diir_xëyma&&Tekst[자료위치]!='\n'){
            int 다음위치=다음(자료위치),너비값=Tekst[자료위치]=='\t'?4-kotu_araf%4:너비(Tekst[자료위치]);
            if(kotu_araf>=왼쪽&&kotu_araf-왼쪽+너비값<열수){
                if(Tekst[자료위치]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)okte_mbir(' ');}else if(Tekst[자료위치]<32||Tekst[자료위치]==127){okte_mbir('?');}else for(int 안쪽순번=자료위치;안쪽순번<다음위치;안쪽순번++)okte_mbir(Tekst[안쪽순번]);그려진상태+=너비값;
            }kotu_araf+=너비값;자료위치=다음위치;
        }
        (void)그려진상태;if(자료위치<diir_xëyma)자료위치++;
    }
    toxal_xëyma(행수,1);글내보내기("\033[7m\033[2K");nekkin_nataal=1;nekkin_Topplante_xaarandi=0;글내보내기(dugal?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(bara_denc_dugal_xabaar_tur[이름바이트수]&&이름바이트수<30)okte_mbir(bara_denc_dugal_xabaar_tur[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int buum=1;for(int 순번=0;순번<àlluwa_tur_xëyma;순번++)if(Tekst[순번]=='\n')buum++;수치(buum);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int 개수=0;글내보내기(" | ");while(알림문[개수]&&개수<20)okte_mbir(알림문[개수++]);}
    nekkin_nataal=0;글내보내기("\033[0m");toxal_xëyma(행위치+1,열위치-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(xaarandi_kër){int 셋째순번=xaarandi_kër;xaarandi_kër=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned tolluwaay=사용자호출(16,3,0,0,0,0,0);
        if(열수!=(int)(tolluwaay&65535)||행수!=(int)(tolluwaay>>16)){
            열수=tolluwaay&65535;행수=tolluwaay>>16;화면그리기();
            if(ndimbal_ngiir){toxal_xëyma(행수,1);글내보내기("\033[0m\033[2K");okte_mbir(ndimbal_ngiir);글내보내기(ndigel);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){xaarandi_kër=셋째순번;return 27;}
    int 개수=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){개수=개수*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return 개수==3?1007:개수==5?1008:개수==6?1009:개수==1?1005:개수==4?1006:27;return 27;}return 27;
}
static int Store_xëyma(void){
    int bara_denc_yombal=sos_bara_denc(bara_denc_dugal_xabaar_tur,jàng_bind|없으면만들기|내용비우기,0600);if(bara_denc_yombal<0){알림문="Cannot open for save";return 0;}
    intptr_t 개수=biir_bara_denc_mbir(bara_denc_yombal,Tekst,diir_xëyma);Tej_bara_denc(bara_denc_yombal);if(개수!=diir_xëyma){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return *첫째값==*둘째값;}
static void 다음찾기(void){int 개수=0;while(seet_dugal_xabaar[개수])개수++;if(!개수){알림문="No search pattern";return;}for(int 순번=1;순번<=diir_xëyma;순번++){int 자료위치=(àlluwa_tur_xëyma+순번)%(diir_xëyma?diir_xëyma:1),안쪽순번=0;while(안쪽순번<개수&&자료위치+안쪽순번<diir_xëyma&&Tekst[자료위치+안쪽순번]==(unsigned char)seet_dugal_xabaar[안쪽순번])안쪽순번++;if(안쪽순번==개수){àlluwa_tur_xëyma=자료위치;알림문="Match";return;}}알림문="Pattern not found";}
static int xaar_jëf(int ngiir_xëyma){
    int 개수=0;ndigel[0]=0;
    for(;;){toxal_xëyma(행수,1);글내보내기("\033[0m\033[2K");okte_mbir(ngiir_xëyma);글내보내기(ndigel);출력비우기();ndimbal_ngiir=ngiir_xëyma;int 셋째순번=누름값();ndimbal_ngiir=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(개수){개수--;while(개수>0&&((unsigned char)ndigel[개수]&192)==128)개수--;ndigel[개수]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&개수<120){ndigel[개수++]=셋째순번;ndigel[개수]=0;}
    }
    if(ngiir_xëyma=='/'){for(int 순번=0;순번<=개수;순번++)seet_dugal_xabaar[순번]=ndigel[순번];다음찾기();return 0;}
    if(같은지(ndigel,"q!"))return 1;
    if(같은지(ndigel,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(ndigel,"wq")||같은지(ndigel,"x"))return Store_xëyma();
    if(같은지(ndigel,"w")){Store_xëyma();return 0;}
    if(ndigel[0]=='w'&&ndigel[1]==' '){int 순번=2;while(ndigel[순번]==' ')순번++;int tolluwaay=개수-순번;if(tolluwaay<1||tolluwaay>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<tolluwaay;안쪽순번++)bara_denc_dugal_xabaar_tur[안쪽순번]=ndigel[순번+안쪽순번];bara_denc_dugal_xabaar_tur[tolluwaay]=0;Store_xëyma();return 0;}
    int buum=0;for(int 순번=0;순번<개수;순번++){if(ndigel[순번]<'0'||ndigel[순번]>'9'){buum=0;break;}buum=buum*10+ndigel[순번]-'0';if(buum>16384){buum=0;break;}}
    if(buum){àlluwa_tur_xëyma=0;while(--buum&&àlluwa_tur_xëyma<diir_xëyma){àlluwa_tur_xëyma=jeexal_Randal(àlluwa_tur_xëyma);if(àlluwa_tur_xëyma<diir_xëyma)àlluwa_tur_xëyma++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Door_kiy_jariñoo_internet_jëfekaay(int 무시값){
    (void)무시값;if(사용자인수개수()!=1||kiy_jariñoo_internet_Tegtal(0,bara_denc_dugal_xabaar_tur,sizeof(bara_denc_dugal_xabaar_tur))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int bara_denc_yombal=sos_bara_denc(bara_denc_dugal_xabaar_tur,ngir_jaŋarek_la_xëyma,0);
    if(bara_denc_yombal>=0){int 개수=bara_denc_tolluwaay(bara_denc_yombal);if(개수<0||개수>편집용량){Tej_bara_denc(bara_denc_yombal);return 1;}diir_xëyma=파일자료읽기(bara_denc_yombal,Tekst,개수);Tej_bara_denc(bara_denc_yombal);if(diir_xëyma!=개수)return 1;for(int 순번=0;순번<diir_xëyma;순번++)if(!Tekst[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}열수=흐린색&65535;행수=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,끝내기=0;
    while(!끝내기){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Taxaw(-1);continue;}if(셋째순번==1002){Taxaw(1);continue;}if(셋째순번==1003){àlluwa_tur_xëyma=다음(àlluwa_tur_xëyma);continue;}if(셋째순번==1004){àlluwa_tur_xëyma=이전항목(àlluwa_tur_xëyma);continue;}
        if(셋째순번==1005){àlluwa_tur_xëyma=daw(àlluwa_tur_xëyma);continue;}if(셋째순번==1006){àlluwa_tur_xëyma=jeexal_Randal(àlluwa_tur_xëyma);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<행수-2;순번++)Taxaw(셋째순번==1008?-1:1);continue;}
        if(dugal){
            if(셋째순번==27||셋째순번==3){dugal=0;continue;}
            if(셋째순번==127||셋째순번==8){if(àlluwa_tur_xëyma)바이트지우기(이전항목(àlluwa_tur_xëyma),àlluwa_tur_xëyma);continue;}
            if(셋째순번==1007){if(àlluwa_tur_xëyma<diir_xëyma)바이트지우기(àlluwa_tur_xëyma,다음(àlluwa_tur_xëyma));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char 둘째값[4];둘째값[0]=셋째순번;int 개수=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!개수){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<개수;순번++){int kotu_araf=누름값();if(kotu_araf<128||kotu_araf>191){xaarandi_kër=kotu_araf;유효함=0;break;}둘째값[순번]=kotu_araf;}
                if(유효함)덧붙이기(둘째값,개수);
            }continue;
        }
        if(앞부분){int 자료위치=앞부분;앞부분=0;if(자료위치=='g'&&셋째순번=='g'){àlluwa_tur_xëyma=0;continue;}if(자료위치=='Z'&&셋째순번=='Z'){끝내기=Store_xëyma();continue;}if((자료위치=='d'&&셋째순번=='d')||(자료위치=='y'&&셋째순번=='y')){int 첫째값=daw(àlluwa_tur_xëyma),둘째값=jeexal_Randal(àlluwa_tur_xëyma);if(둘째값<diir_xëyma)둘째값++;mbokk_diir=둘째값-첫째값;for(int 순번=0;순번<mbokk_diir;순번++)복사자료[순번]=Tekst[첫째값+순번];if(자료위치=='d')바이트지우기(첫째값,둘째값);continue;}}
        if(셋째순번=='i'){dugal=1;continue;}if(셋째순번=='a'){if(àlluwa_tur_xëyma<jeexal_Randal(àlluwa_tur_xëyma))àlluwa_tur_xëyma=다음(àlluwa_tur_xëyma);dugal=1;continue;}
        if(셋째순번=='I'){àlluwa_tur_xëyma=daw(àlluwa_tur_xëyma);dugal=1;continue;}if(셋째순번=='A'){àlluwa_tur_xëyma=jeexal_Randal(àlluwa_tur_xëyma);dugal=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char buum_jeexal='\n';àlluwa_tur_xëyma=셋째순번=='o'?jeexal_Randal(àlluwa_tur_xëyma):daw(àlluwa_tur_xëyma);if(덧붙이기(&buum_jeexal,1)){if(셋째순번=='O')àlluwa_tur_xëyma--;dugal=1;}continue;}
        if(셋째순번=='h'){àlluwa_tur_xëyma=이전항목(àlluwa_tur_xëyma);continue;}if(셋째순번=='l'){àlluwa_tur_xëyma=다음(àlluwa_tur_xëyma);continue;}if(셋째순번=='j'){Taxaw(1);continue;}if(셋째순번=='k'){Taxaw(-1);continue;}
        if(셋째순번=='0'){àlluwa_tur_xëyma=daw(àlluwa_tur_xëyma);continue;}if(셋째순번=='$'){àlluwa_tur_xëyma=jeexal_Randal(àlluwa_tur_xëyma);continue;}if(셋째순번=='G'){àlluwa_tur_xëyma=daw(diir_xëyma);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(àlluwa_tur_xëyma<diir_xëyma)바이트지우기(àlluwa_tur_xëyma,다음(àlluwa_tur_xëyma));continue;}
        if(셋째순번=='p'&&mbokk_diir){àlluwa_tur_xëyma=jeexal_Randal(àlluwa_tur_xëyma);if(àlluwa_tur_xëyma<diir_xëyma)àlluwa_tur_xëyma++;덧붙이기(복사자료,mbokk_diir);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char 둘째값=Tekst[순번];Tekst[순번]=jamonoy_dekkal_mbir[순번];jamonoy_dekkal_mbir[순번]=둘째값;}int 개수=diir_xëyma;diir_xëyma=jamonoy_dekkal_diir;jamonoy_dekkal_diir=개수;개수=àlluwa_tur_xëyma;àlluwa_tur_xëyma=위쪽;위쪽=개수;개수=변경됨;변경됨=jamonoy_dekkal_Coppite_yi;jamonoy_dekkal_Coppite_yi=개수;continue;}
        if(셋째순번==':'||셋째순번=='/'){끝내기=xaar_jëf(셋째순번);continue;}if(셋째순번=='n'){다음찾기();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
