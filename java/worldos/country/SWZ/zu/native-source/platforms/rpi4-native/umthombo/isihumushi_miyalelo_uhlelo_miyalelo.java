// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 ingxoxo_nekhompiyutha isihumushi_miyalelo 문법. 파이프는 순차 yenza_umyalo, 환경은 같은 셸에서 공유한다. */
public final class isihumushi_miyalelo_uhlelo_miyalelo {
    static int[] umthombo = new int[4 * 4096], 종류 = new int[4 * 128], Sebenzisa = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], inani_ubude = new int[16];
    static int[] uhlelosiluleko_inani = new int[4 * 16384];
    static int isimo_inani, 깊이, 쓴수;
    static boolean 연결중, uhlelosiluleko_yekisa, iselulo_iphutha;
    static boolean igama_uhlamvusimo(int ikhodi_yohlamvu) { return ikhodi_yohlamvu >= 'a' && ikhodi_yohlamvu <= 'z' || ikhodi_yohlamvu >= 'A' && ikhodi_yohlamvu <= 'Z' || ikhodi_yohlamvu == '_' || ikhodi_yohlamvu >= 128; }
    static boolean 이름뒤(int ikhodi_yohlamvu) { return igama_uhlamvusimo(ikhodi_yohlamvu) || ikhodi_yohlamvu >= '0' && ikhodi_yohlamvu <= '9'; }
    static void Iphutha(String Itekisi) { 보드.입출력전환(0); 단말.Bhala("Umlayelo zawula_inani: "); 단말.Bhala(Itekisi); 단말.문자(10); isimo_inani = 2; }
    static int Funda(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, uhlamvu_olukhethekile = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (umthombo[기준자리 + 현재자리] == 32 || umthombo[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || umthombo[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { Iphutha("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, ikhodi_yohlamvu = umthombo[기준자리 + 현재자리], 자료종류 = 0;
            if (ikhodi_yohlamvu == ';') { 자료종류 = 1; 현재자리++; }
            else if (ikhodi_yohlamvu == '&') { if (현재자리 + 1 >= 항목수 || umthombo[기준자리 + 현재자리 + 1] != '&') { Iphutha("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (ikhodi_yohlamvu == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && umthombo[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (ikhodi_yohlamvu == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && umthombo[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (ikhodi_yohlamvu == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    ikhodi_yohlamvu = umthombo[기준자리 + 현재자리];
                    if (ikhodi_yohlamvu == '`' && 따옴표 != 39 || ikhodi_yohlamvu == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && umthombo[기준자리 + 현재자리 + 1] == '(') { Iphutha("Umlayelo 결과 치환은 지원하지 않습니다"); return -1; }
                    if (ikhodi_yohlamvu == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { Iphutha("umugqa 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (ikhodi_yohlamvu == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (ikhodi_yohlamvu == 39 || ikhodi_yohlamvu == 34)) { 따옴표 = ikhodi_yohlamvu; 현재자리++; continue; }
                    if (따옴표 == 0 && (ikhodi_yohlamvu == 32 || ikhodi_yohlamvu == 9 || ikhodi_yohlamvu == ';' || ikhodi_yohlamvu == '&' || ikhodi_yohlamvu == '|' || ikhodi_yohlamvu == '<' || ikhodi_yohlamvu == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { Iphutha("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (umthombo[기준자리 + 현재자리] == '>' || umthombo[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int iluphu_thola_inkomba = 시작자리; iluphu_thola_inkomba < 현재자리; iluphu_thola_inkomba++) if (umthombo[기준자리 + iluphu_thola_inkomba] < '0' || umthombo[기준자리 + iluphu_thola_inkomba] > '9') 수치 = false;
                    if (수치) { Iphutha("번호를 지정한 Ihele 서술자 i_I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[uhlamvu_olukhethekile + 총수] = 자료종류; Sebenzisa[uhlamvu_olukhethekile + 총수] = 시작자리; 끝[uhlamvu_olukhethekile + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 총수; iluphu_thola_inkomba++) {
            int 임시값 = 종류[uhlamvu_olukhethekile + iluphu_thola_inkomba];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++iluphu_thola_inkomba == 총수 || 종류[uhlamvu_olukhethekile + iluphu_thola_inkomba] != 0) { Iphutha("i_I_O 전환에 Ihele 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || iluphu_thola_inkomba == 총수 - 1 && 임시값 != 1) { Iphutha("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[uhlamvu_olukhethekile + 총수 - 1] != 1) { Iphutha("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] imininingwane_AMALUNGU_AFANAYO, int endaweni_qala, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) if (imininingwane_AMALUNGU_AFANAYO[endaweni_qala + iluphu_thola_inkomba] != 문자위치.charAt(iluphu_thola_inkomba)) return false; return true;
    }
    static void 넣기(int ibhayithi_imininingwane) {
        if (쓴수 >= 명령해석기.ithokhini_inani.length) { if (!iselulo_iphutha) Iphutha("변수를 펼친 명령이 너무 깁니다"); iselulo_iphutha = true; return; }
        명령해석기.ithokhini_inani[쓴수++] = ibhayithi_imininingwane;
    }
    static void 변수(int[] imininingwane_AMALUNGU_AFANAYO, int 시작자리, int 항목수) {
        if (구간말(imininingwane_AMALUNGU_AFANAYO, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < inkumbulo_Amafayela.현재길이; iluphu_thola_inkomba++) 넣기(inkumbulo_Amafayela.현재[iluphu_thola_inkomba]); return; }
        if (구간말(imininingwane_AMALUNGU_AFANAYO, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(imininingwane_AMALUNGU_AFANAYO, 시작자리, 항목수, "?")) {
            int imininingwane_inani = isimo_inani, idijithi = 100; boolean 시작여부 = false;
            while (idijithi > 0) { int 뒷값 = imininingwane_inani / idijithi; if (뒷값 != 0 || 시작여부 || idijithi == 1) { 넣기('0' + 뒷값); 시작여부 = true; } imininingwane_inani %= idijithi; idijithi /= 10; } return;
        }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 16; iluphu_thola_inkomba++) if (이름길이[iluphu_thola_inkomba] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[iluphu_thola_inkomba * 32 + 안쪽자리] != imininingwane_AMALUNGU_AFANAYO[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < inani_ubude[iluphu_thola_inkomba]; 안쪽자리++) 넣기(변수값[iluphu_thola_inkomba * 256 + 안쪽자리]); return; }
        }
    }
    static boolean Amagama_inani(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Sebenzisa[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && umthombo[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || umthombo[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int ikhodi_yohlamvu = umthombo[기준자리 + 읽는자리++];
            if (ikhodi_yohlamvu == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (ikhodi_yohlamvu == 39 || ikhodi_yohlamvu == 34)) { 따옴표 = ikhodi_yohlamvu; continue; }
            if (ikhodi_yohlamvu == '\\' && 따옴표 != 39) { int 다음자리 = umthombo[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (ikhodi_yohlamvu == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = umthombo[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && umthombo[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(umthombo[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || umthombo[기준자리 + 읽는자리] != '}')) { Iphutha("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(umthombo, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(ikhodi_yohlamvu);
        }
        return !iselulo_iphutha;
    }
    static int 환경설정(int i_agumenti_thola_inkomba, boolean khipha) {
        int endaweni_qala = 명령해석기.시작점[i_agumenti_thola_inkomba], 끝자리 = endaweni_qala + 명령해석기.ubude_inani[i_agumenti_thola_inkomba], 같음자리 = endaweni_qala;
        while (같음자리 < 끝자리 && 명령해석기.ithokhini_inani[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - endaweni_qala;
        if (항목수 < 1 || 항목수 > 31 || !igama_uhlamvusimo(명령해석기.ithokhini_inani[endaweni_qala]) || !khipha && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int iluphu_thola_inkomba = endaweni_qala; iluphu_thola_inkomba < 같음자리; iluphu_thola_inkomba++) if (!이름뒤(명령해석기.ithokhini_inani[iluphu_thola_inkomba])) return 2;
        if (구간말(명령해석기.ithokhini_inani, endaweni_qala, 항목수, "PWD") || 구간말(명령해석기.ithokhini_inani, endaweni_qala, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 16; iluphu_thola_inkomba++) {
            if (이름길이[iluphu_thola_inkomba] == 0) 빈여부 = iluphu_thola_inkomba;
            if (이름길이[iluphu_thola_inkomba] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[iluphu_thola_inkomba * 32 + 안쪽자리] != 명령해석기.ithokhini_inani[endaweni_qala + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = iluphu_thola_inkomba;
        }
        if (khipha) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; inani_ubude[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) 변수이름[찾은여부 * 32 + iluphu_thola_inkomba] = 명령해석기.ithokhini_inani[endaweni_qala + iluphu_thola_inkomba];
        for (int iluphu_thola_inkomba = 같음자리 + 1; iluphu_thola_inkomba < 끝자리; iluphu_thola_inkomba++) 변수값[찾은여부 * 256 + iluphu_thola_inkomba - 같음자리 - 1] = 명령해석기.ithokhini_inani[iluphu_thola_inkomba];
        return 0;
    }
    static void 환경보기() {
        단말.Bhala("HOME=/\nPWD="); inkumbulo_Amafayela.현재쓰기(); 단말.문자(10);
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 16; iluphu_thola_inkomba++) if (이름길이[iluphu_thola_inkomba] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[iluphu_thola_inkomba]; 안쪽자리++) 보드.직렬쓰기(변수이름[iluphu_thola_inkomba * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < inani_ubude[iluphu_thola_inkomba]; 안쪽자리++) 보드.직렬쓰기(변수값[iluphu_thola_inkomba * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void yenza_umyalo(int[] imininingwane_AMALUNGU_AFANAYO, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { Iphutha("Umlayelo 파일의 중첩 또는 umugqa ubude_inani 제한을 넘었습니다"); return; }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) umthombo[중첩깊이 * 4096 + iluphu_thola_inkomba] = imininingwane_AMALUNGU_AFANAYO[시작변위 + iluphu_thola_inkomba];
        int 총수 = Funda(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int iqoqo_yekisa = 읽는자리;
            while (iqoqo_yekisa < 총수 && (종류[중첩깊이 * 128 + iqoqo_yekisa] == 0 || 종류[중첩깊이 * 128 + iqoqo_yekisa] >= 4)) iqoqo_yekisa++;
            boolean yenza = 조건성립 == 1 || 조건성립 == 2 && isimo_inani == 0 || 조건성립 == 3 && isimo_inani != 0;
            if (yenza) {
                boolean 이전자리 = false;
                while (읽는자리 < iqoqo_yekisa) {
                    int 다음자리 = 읽는자리; while (다음자리 < iqoqo_yekisa && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean xhuma_Stream = 다음자리 < iqoqo_yekisa; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; iselulo_iphutha = false;
                    for (int iluphu_thola_inkomba = 읽는자리; iluphu_thola_inkomba < 다음자리; iluphu_thola_inkomba++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + iluphu_thola_inkomba];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Iphutha("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++iluphu_thola_inkomba; } else { if (출력쪽 >= 0) { Iphutha("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++iluphu_thola_inkomba; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { Iphutha("인수가 너무 많습니다"); return; }
                        int i_agumenti_thola_inkomba = 명령해석기.토큰수++; 명령해석기.시작점[i_agumenti_thola_inkomba] = 쓴수;
                        if (!Amagama_inani(iluphu_thola_inkomba, 중첩깊이)) return;
                        명령해석기.ubude_inani[i_agumenti_thola_inkomba] = 쓴수 - 명령해석기.시작점[i_agumenti_thola_inkomba];
                    }
                    연결중 = 이전자리 || xhuma_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Iphutha("ingxoxo_nekhompiyutha 명령과 Umlayelo 파일은 i_I_O 전환이나 Stream_inani 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Sebenzisa(이전자리, xhuma_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!Amagama_inani(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = inkumbulo_Amafayela.umzila_qala(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = inkumbulo_Amafayela.umzila_ibhayithi(안쪽자리 - 시작자리, 명령해석기.ithokhini_inani[안쪽자리]);
                        if (처리값 >= 0) 처리값 = inkumbulo_Amafayela.Vula(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Iphutha(처리값); isimo_inani = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.ifayela_yokukhipha = 처리값;
                    }
                    셸입출력.vumela_ingxoxo_nekhompiyutha = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.Umlayelo();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, Stream_iphutha = 셸입출력.ukwehluleka_inani;
                    셸입출력.끝(); 연결중 = false;
                    isimo_inani = Stream_iphutha < 0 ? 1 : 반환값;
                    if (Stream_iphutha < 0) { 명령해석기.Iphutha(Stream_iphutha); return; }
                    if (uhlelosiluleko_yekisa || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (iqoqo_yekisa < 총수) 조건성립 = 종류[중첩깊이 * 128 + iqoqo_yekisa];
            읽는자리 = iqoqo_yekisa + 1;
        }
    }
    static void yenza_ifayela() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.Bhala("사용법: sh Ihele (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Indlela_2(1); if (처리값 >= 0) 처리값 = inkumbulo_Amafayela.Vula(0);
        if (처리값 < 0) { 명령해석기.Iphutha(처리값); return; }
        int 항목수 = 0, ibhayithi_imininingwane;
        while ((ibhayithi_imininingwane = inkumbulo_Amafayela.Funda(처리값)) != 256 && ibhayithi_imininingwane >= 0 && 항목수 < 16384) uhlelosiluleko_inani[중첩깊이 * 16384 + 항목수++] = ibhayithi_imininingwane;
        inkumbulo_Amafayela.Vala(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !uhlelosiluleko_yekisa;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && uhlelosiluleko_inani[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && uhlelosiluleko_inani[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            yenza_umyalo(uhlelosiluleko_inani, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = isimo_inani; uhlelosiluleko_yekisa = false; 깊이 = 중첩깊이 - 1;
    }
}
