// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 esebenzisana_nomsebenzi isiniki_myalelo 문법. 파이프는 순차 ukwenza_umyalelo, 환경은 같은 셸에서 공유한다. */
public final class isiniki_myalelo_ukuma_kwezivakalisi {
    static int[] UMTHOMBO = new int[4 * 4096], 종류 = new int[4 * 128], Phumeza = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], ixabiso_ubude = new int[16];
    static int[] iskripthi_ixabiso = new int[4 * 16384];
    static int imo_ixabiso, 깊이, 쓴수;
    static boolean 연결중, iskripthi_phela, isongezelelo_impazamo;
    static boolean igama_ikharakhtha(int ikhowudi_yekharakhtha) { return ikhowudi_yekharakhtha >= 'a' && ikhowudi_yekharakhtha <= 'z' || ikhowudi_yekharakhtha >= 'A' && ikhowudi_yekharakhtha <= 'Z' || ikhowudi_yekharakhtha == '_' || ikhowudi_yekharakhtha >= 128; }
    static boolean 이름뒤(int ikhowudi_yekharakhtha) { return igama_ikharakhtha(ikhowudi_yekharakhtha) || ikhowudi_yekharakhtha >= '0' && ikhowudi_yekharakhtha <= '9'; }
    static void Impazamo(String Umbhalo) { 보드.입출력전환(0); 단말.Bhala("Umyalelo ingcaciso_yegama_ixabiso: "); 단말.Bhala(Umbhalo); 단말.문자(10); imo_ixabiso = 2; }
    static int Funda(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, ikharakhtha_ekhethekileyo = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (UMTHOMBO[기준자리 + 현재자리] == 32 || UMTHOMBO[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || UMTHOMBO[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { Impazamo("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, ikhowudi_yekharakhtha = UMTHOMBO[기준자리 + 현재자리], 자료종류 = 0;
            if (ikhowudi_yekharakhtha == ';') { 자료종류 = 1; 현재자리++; }
            else if (ikhowudi_yekharakhtha == '&') { if (현재자리 + 1 >= 항목수 || UMTHOMBO[기준자리 + 현재자리 + 1] != '&') { Impazamo("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (ikhowudi_yekharakhtha == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && UMTHOMBO[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (ikhowudi_yekharakhtha == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && UMTHOMBO[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (ikhowudi_yekharakhtha == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    ikhowudi_yekharakhtha = UMTHOMBO[기준자리 + 현재자리];
                    if (ikhowudi_yekharakhtha == '`' && 따옴표 != 39 || ikhowudi_yekharakhtha == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && UMTHOMBO[기준자리 + 현재자리 + 1] == '(') { Impazamo("Umyalelo 결과 치환은 지원하지 않습니다"); return -1; }
                    if (ikhowudi_yekharakhtha == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { Impazamo("umgca 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (ikhowudi_yekharakhtha == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (ikhowudi_yekharakhtha == 39 || ikhowudi_yekharakhtha == 34)) { 따옴표 = ikhowudi_yekharakhtha; 현재자리++; continue; }
                    if (따옴표 == 0 && (ikhowudi_yekharakhtha == 32 || ikhowudi_yekharakhtha == 9 || ikhowudi_yekharakhtha == ';' || ikhowudi_yekharakhtha == '&' || ikhowudi_yekharakhtha == '|' || ikhowudi_yekharakhtha == '<' || ikhowudi_yekharakhtha == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { Impazamo("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (UMTHOMBO[기준자리 + 현재자리] == '>' || UMTHOMBO[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int iluphu_indeksa = 시작자리; iluphu_indeksa < 현재자리; iluphu_indeksa++) if (UMTHOMBO[기준자리 + iluphu_indeksa] < '0' || UMTHOMBO[기준자리 + iluphu_indeksa] > '9') 수치 = false;
                    if (수치) { Impazamo("번호를 지정한 iFayili 서술자 i_I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[ikharakhtha_ekhethekileyo + 총수] = 자료종류; Phumeza[ikharakhtha_ekhethekileyo + 총수] = 시작자리; 끝[ikharakhtha_ekhethekileyo + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 총수; iluphu_indeksa++) {
            int 임시값 = 종류[ikharakhtha_ekhethekileyo + iluphu_indeksa];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++iluphu_indeksa == 총수 || 종류[ikharakhtha_ekhethekileyo + iluphu_indeksa] != 0) { Impazamo("i_I_O 전환에 iFayili 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || iluphu_indeksa == 총수 - 1 && 임시값 != 1) { Impazamo("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[ikharakhtha_ekhethekileyo + 총수 - 1] != 1) { Impazamo("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] iingcombolo_ULUHLU, int eyale_ndawo_qala, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) if (iingcombolo_ULUHLU[eyale_ndawo_qala + iluphu_indeksa] != 문자위치.charAt(iluphu_indeksa)) return false; return true;
    }
    static void 넣기(int ibhayithi_iingcombolo) {
        if (쓴수 >= 명령해석기.ithokeni_ixabiso.length) { if (!isongezelelo_impazamo) Impazamo("변수를 펼친 명령이 너무 깁니다"); isongezelelo_impazamo = true; return; }
        명령해석기.ithokeni_ixabiso[쓴수++] = ibhayithi_iingcombolo;
    }
    static void 변수(int[] iingcombolo_ULUHLU, int 시작자리, int 항목수) {
        if (구간말(iingcombolo_ULUHLU, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int iluphu_indeksa = 0; iluphu_indeksa < imemori_Iifayile.현재길이; iluphu_indeksa++) 넣기(imemori_Iifayile.현재[iluphu_indeksa]); return; }
        if (구간말(iingcombolo_ULUHLU, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(iingcombolo_ULUHLU, 시작자리, 항목수, "?")) {
            int iingcombolo_ixabiso = imo_ixabiso, inani = 100; boolean 시작여부 = false;
            while (inani > 0) { int 뒷값 = iingcombolo_ixabiso / inani; if (뒷값 != 0 || 시작여부 || inani == 1) { 넣기('0' + 뒷값); 시작여부 = true; } iingcombolo_ixabiso %= inani; inani /= 10; } return;
        }
        for (int iluphu_indeksa = 0; iluphu_indeksa < 16; iluphu_indeksa++) if (이름길이[iluphu_indeksa] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[iluphu_indeksa * 32 + 안쪽자리] != iingcombolo_ULUHLU[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < ixabiso_ubude[iluphu_indeksa]; 안쪽자리++) 넣기(변수값[iluphu_indeksa * 256 + 안쪽자리]); return; }
        }
    }
    static boolean Igama_ixabiso(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Phumeza[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && UMTHOMBO[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || UMTHOMBO[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int ikhowudi_yekharakhtha = UMTHOMBO[기준자리 + 읽는자리++];
            if (ikhowudi_yekharakhtha == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (ikhowudi_yekharakhtha == 39 || ikhowudi_yekharakhtha == 34)) { 따옴표 = ikhowudi_yekharakhtha; continue; }
            if (ikhowudi_yekharakhtha == '\\' && 따옴표 != 39) { int 다음자리 = UMTHOMBO[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (ikhowudi_yekharakhtha == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = UMTHOMBO[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && UMTHOMBO[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(UMTHOMBO[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || UMTHOMBO[기준자리 + 읽는자리] != '}')) { Impazamo("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(UMTHOMBO, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(ikhowudi_yekharakhtha);
        }
        return !isongezelelo_impazamo;
    }
    static int 환경설정(int isiniki_myalelo_indeksa, boolean shenxisa) {
        int eyale_ndawo_qala = 명령해석기.시작점[isiniki_myalelo_indeksa], 끝자리 = eyale_ndawo_qala + 명령해석기.ubude_ixabiso[isiniki_myalelo_indeksa], 같음자리 = eyale_ndawo_qala;
        while (같음자리 < 끝자리 && 명령해석기.ithokeni_ixabiso[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - eyale_ndawo_qala;
        if (항목수 < 1 || 항목수 > 31 || !igama_ikharakhtha(명령해석기.ithokeni_ixabiso[eyale_ndawo_qala]) || !shenxisa && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int iluphu_indeksa = eyale_ndawo_qala; iluphu_indeksa < 같음자리; iluphu_indeksa++) if (!이름뒤(명령해석기.ithokeni_ixabiso[iluphu_indeksa])) return 2;
        if (구간말(명령해석기.ithokeni_ixabiso, eyale_ndawo_qala, 항목수, "PWD") || 구간말(명령해석기.ithokeni_ixabiso, eyale_ndawo_qala, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 16; iluphu_indeksa++) {
            if (이름길이[iluphu_indeksa] == 0) 빈여부 = iluphu_indeksa;
            if (이름길이[iluphu_indeksa] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[iluphu_indeksa * 32 + 안쪽자리] != 명령해석기.ithokeni_ixabiso[eyale_ndawo_qala + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = iluphu_indeksa;
        }
        if (shenxisa) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; ixabiso_ubude[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) 변수이름[찾은여부 * 32 + iluphu_indeksa] = 명령해석기.ithokeni_ixabiso[eyale_ndawo_qala + iluphu_indeksa];
        for (int iluphu_indeksa = 같음자리 + 1; iluphu_indeksa < 끝자리; iluphu_indeksa++) 변수값[찾은여부 * 256 + iluphu_indeksa - 같음자리 - 1] = 명령해석기.ithokeni_ixabiso[iluphu_indeksa];
        return 0;
    }
    static void 환경보기() {
        단말.Bhala("HOME=/\nPWD="); imemori_Iifayile.현재쓰기(); 단말.문자(10);
        for (int iluphu_indeksa = 0; iluphu_indeksa < 16; iluphu_indeksa++) if (이름길이[iluphu_indeksa] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[iluphu_indeksa]; 안쪽자리++) 보드.직렬쓰기(변수이름[iluphu_indeksa * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < ixabiso_ubude[iluphu_indeksa]; 안쪽자리++) 보드.직렬쓰기(변수값[iluphu_indeksa * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void ukwenza_umyalelo(int[] iingcombolo_ULUHLU, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { Impazamo("Umyalelo 파일의 중첩 또는 umgca ubude_ixabiso 제한을 넘었습니다"); return; }
        for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) UMTHOMBO[중첩깊이 * 4096 + iluphu_indeksa] = iingcombolo_ULUHLU[시작변위 + iluphu_indeksa];
        int 총수 = Funda(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int iqela_phela = 읽는자리;
            while (iqela_phela < 총수 && (종류[중첩깊이 * 128 + iqela_phela] == 0 || 종류[중첩깊이 * 128 + iqela_phela] >= 4)) iqela_phela++;
            boolean ukwenza = 조건성립 == 1 || 조건성립 == 2 && imo_ixabiso == 0 || 조건성립 == 3 && imo_ixabiso != 0;
            if (ukwenza) {
                boolean 이전자리 = false;
                while (읽는자리 < iqela_phela) {
                    int 다음자리 = 읽는자리; while (다음자리 < iqela_phela && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean I_Connect_Stream = 다음자리 < iqela_phela; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; isongezelelo_impazamo = false;
                    for (int iluphu_indeksa = 읽는자리; iluphu_indeksa < 다음자리; iluphu_indeksa++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + iluphu_indeksa];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Impazamo("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++iluphu_indeksa; } else { if (출력쪽 >= 0) { Impazamo("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++iluphu_indeksa; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { Impazamo("인수가 너무 많습니다"); return; }
                        int isiniki_myalelo_indeksa = 명령해석기.토큰수++; 명령해석기.시작점[isiniki_myalelo_indeksa] = 쓴수;
                        if (!Igama_ixabiso(iluphu_indeksa, 중첩깊이)) return;
                        명령해석기.ubude_ixabiso[isiniki_myalelo_indeksa] = 쓴수 - 명령해석기.시작점[isiniki_myalelo_indeksa];
                    }
                    연결중 = 이전자리 || I_Connect_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Impazamo("esebenzisana_nomsebenzi 명령과 Umyalelo 파일은 i_I_O 전환이나 Stream_ixabiso 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Phumeza(이전자리, I_Connect_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!Igama_ixabiso(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = imemori_Iifayile.indlela_qala(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = imemori_Iifayile.indlela_ibhayithi(안쪽자리 - 시작자리, 명령해석기.ithokeni_ixabiso[안쪽자리]);
                        if (처리값 >= 0) 처리값 = imemori_Iifayile.Vula(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Impazamo(처리값); imo_ixabiso = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.ifayile_yemveliso = 처리값;
                    }
                    셸입출력.vumela_esebenzisana_nomsebenzi = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.Umyalelo();
                    보드.i_Terminal(3);
                    int 반환값 = 명령해석기.결과, Stream_impazamo = 셸입출력.ukungaphumeleli_ixabiso;
                    셸입출력.끝(); 연결중 = false;
                    imo_ixabiso = Stream_impazamo < 0 ? 1 : 반환값;
                    if (Stream_impazamo < 0) { 명령해석기.Impazamo(Stream_impazamo); return; }
                    if (iskripthi_phela || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (iqela_phela < 총수) 조건성립 = 종류[중첩깊이 * 128 + iqela_phela];
            읽는자리 = iqela_phela + 1;
        }
    }
    static void ukwenza_ifayile() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.Bhala("사용법: sh iFayili (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.INDLELA(1); if (처리값 >= 0) 처리값 = imemori_Iifayile.Vula(0);
        if (처리값 < 0) { 명령해석기.Impazamo(처리값); return; }
        int 항목수 = 0, ibhayithi_iingcombolo;
        while ((ibhayithi_iingcombolo = imemori_Iifayile.Funda(처리값)) != 256 && ibhayithi_iingcombolo >= 0 && 항목수 < 16384) iskripthi_ixabiso[중첩깊이 * 16384 + 항목수++] = ibhayithi_iingcombolo;
        imemori_Iifayile.Vala(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !iskripthi_phela;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && iskripthi_ixabiso[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && iskripthi_ixabiso[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            ukwenza_umyalelo(iskripthi_ixabiso, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = imo_ixabiso; iskripthi_phela = false; 깊이 = 중첩깊이 - 1;
    }
}
