// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java Cosaan_tëralinuy_pàcc -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] Cosaan = new int[16384], 출력 = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], jeton_diir = new int[2048];
    static int[] Lees_dul_soppi_xëyma = new int[4096], Lees_dul_soppi_Randal = new int[512];
    static int[] 문자 = new int[512], bara_denc_tur_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int Cosaan_tolluwaay, 토큰수, 위치, 코드크기, Lees_dul_soppi_tolluwaay, 상수수 = 1, 출력크기, Araf_diir;
    static boolean njumte;
    static int maas_jeton, maas_Lees_dul_soppi, 부모상수, 코드상수;
    static int[] doxalin_dugal_xabaar_tur = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] doxalin_Tegtal_tur = new int[512], doxalin_Tegtal_xeet = new int[512];
    static int[] 함수본문 = new int[32], doxalin_jeexal = new int[32], 함수코드 = new int[32];
    static int[] doxalin_diir = new int[32], 함수지역 = new int[32], doxalin_tur_Lees_dul_soppi = new int[32], 함수서술 = new int[32];
    static int[] doxalin_jot = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] dënnd_tur = new int[128], dënnd_xeet = new int[128], 지역깊이 = new int[128];

    static void foo_xëyma(String 이유) {
        if (!njumte) {
            kiy_jariñoo_internet.biir("javac error: "); kiy_jariñoo_internet.biir(이유);
            kiy_jariñoo_internet.biir(" at line ");
            int buum = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : Cosaan_tolluwaay;
            for (int 수 = 0; 수 < 끝; 수++) if (Cosaan[수] == 10) buum++;
            자바도구.수쓰기(buum); kiy_jariñoo_internet.biir_Araf_xëyma(10);
        }
        njumte = true;
    }
    static boolean Araf_xëyma(int xëyma) { return 문자이름규칙.첫글자(xëyma); }
    static boolean siifar_xëyma(int xëyma) { return xëyma >= '0' && xëyma <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || jeton_diir[가] != jeton_diir[나]) return false;
        for (int 수 = 0; 수 < jeton_diir[가]; 수++) if (Cosaan[토큰위치[가] + 수] != Cosaan[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean Word_xëyma(int jeton_xëyma, String Word_SMS) {
        if (jeton_xëyma < 0 || jeton_xëyma >= 토큰수 || jeton_diir[jeton_xëyma] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (Cosaan[토큰위치[jeton_xëyma] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int xëyma) { if (종류() != xëyma) return false; 위치++; return true; }
    static void 요구(int xëyma) { if (!받기(xëyma)) foo_xëyma("unexpected token"); }
    static boolean 말받기(String Word_SMS) { if (!Word_xëyma(위치, Word_SMS)) return false; 위치++; return true; }
    static void 말요구(String Word_SMS) { if (!말받기(Word_SMS)) foo_xëyma(Word_SMS); }
    static int raññeekaay_xëyma() {
        int 결과 = 위치;
        if (종류() != 256) foo_xëyma("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int daw = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - daw == jeton_diir[결과];
                for (int xar_xar_dugal_xabaar = daw; 같음 && xar_xar_dugal_xabaar < 수; xar_xar_dugal_xabaar++) if (예약어.charAt(xar_xar_dugal_xabaar) != Cosaan[토큰위치[결과] + xar_xar_dugal_xabaar - daw]) 같음 = false;
                if (같음) foo_xëyma("reserved word cannot be an identifier");
                daw = 수 + 1;
            }
        }
        return 결과;
    }
    static void dogandi_xëyma() {
        int 수 = 0;
        while (수 < Cosaan_tolluwaay && !njumte) {
            int xëyma = Cosaan[수], daw = 수, 종류 = xëyma;
            if (xëyma == 32 || xëyma == 9 || xëyma == 10 || xëyma == 13) { 수++; continue; }
            if (xëyma == '/' && 수 + 1 < Cosaan_tolluwaay && Cosaan[수 + 1] == '/') {
                while (수 < Cosaan_tolluwaay && Cosaan[수] != 10) 수++;
                continue;
            }
            if (xëyma == '/' && 수 + 1 < Cosaan_tolluwaay && Cosaan[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < Cosaan_tolluwaay && !(Cosaan[수] == '*' && Cosaan[수 + 1] == '/')) 수++;
                if (수 + 1 >= Cosaan_tolluwaay) { foo_xëyma("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (Araf_xëyma(xëyma)) { 종류 = 256; while (수 < Cosaan_tolluwaay && 문자이름규칙.이어진글자(Cosaan[수])) 수++; }
            else if (siifar_xëyma(xëyma)) { 종류 = 257; while (수 < Cosaan_tolluwaay && siifar_xëyma(Cosaan[수])) 수++; }
            else if (xëyma == '"' || xëyma == '\'') {
                종류 = xëyma == '"' ? 258 : 259; 수++;
                while (수 < Cosaan_tolluwaay && Cosaan[수] != xëyma && Cosaan[수] != 10 && Cosaan[수] != 13) {
                    if (Cosaan[수] == '\\') 수++;
                    수++;
                }
                if (수 >= Cosaan_tolluwaay || Cosaan[수] != xëyma) { foo_xëyma("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < Cosaan_tolluwaay) {
                    int 다음 = Cosaan[수];
                    if (xëyma == '=' && 다음 == '=') 종류 = 300;
                    if (xëyma == '!' && 다음 == '=') 종류 = 301;
                    if (xëyma == '<' && 다음 == '=') 종류 = 302;
                    if (xëyma == '>' && 다음 == '=') 종류 = 303;
                    if (xëyma == '&' && 다음 == '&') 종류 = 304;
                    if (xëyma == '|' && 다음 == '|') 종류 = 305;
                    if (xëyma == '+' && 다음 == '+') 종류 = 306;
                    if (xëyma == '-' && 다음 == '-') 종류 = 307;
                    if (xëyma == '+' && 다음 == '=') 종류 = 308;
                    if (xëyma == '-' && 다음 == '=') 종류 = 309;
                    if (xëyma == '*' && 다음 == '=') 종류 = 310;
                    if (xëyma == '/' && 다음 == '=') 종류 = 311;
                    if (xëyma == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { foo_xëyma("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = daw; jeton_diir[토큰수++] = 수 - daw;
        }
    }
    static void biir_Lees_dul_soppi_okte(int xëyma) {
        if (Lees_dul_soppi_tolluwaay == Lees_dul_soppi_xëyma.length) { foo_xëyma("constant pool too large"); return; }
        Lees_dul_soppi_xëyma[Lees_dul_soppi_tolluwaay++] = xëyma & 255;
    }
    static void 상짧(int xëyma) { biir_Lees_dul_soppi_okte(xëyma >> 8); biir_Lees_dul_soppi_okte(xëyma); }
    static int bindu_Lees_dul_soppi(int daw) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = Lees_dul_soppi_Randal[수], diir_xëyma = (수 + 1 < 상수수 ? Lees_dul_soppi_Randal[수 + 1] : daw) - 앞;
            if (diir_xëyma != Lees_dul_soppi_tolluwaay - daw) continue;
            boolean 같음 = true;
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < diir_xëyma; xar_xar_dugal_xabaar++) if (Lees_dul_soppi_xëyma[앞 + xar_xar_dugal_xabaar] != Lees_dul_soppi_xëyma[daw + xar_xar_dugal_xabaar]) 같음 = false;
            if (같음) { Lees_dul_soppi_tolluwaay = daw; return 수; }
        }
        if (상수수 == Lees_dul_soppi_Randal.length) { foo_xëyma("too many constants"); return 0; }
        Lees_dul_soppi_Randal[상수수] = daw;
        return 상수수++;
    }
    static void 글추가(int xëyma) {
        if (Araf_diir == 문자.length) { foo_xëyma("text too long"); return; }
        문자[Araf_diir++] = xëyma;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int Araf_Lees_dul_soppi() {
        int daw = Lees_dul_soppi_tolluwaay; biir_Lees_dul_soppi_okte(1); 상짧(0);
        for (int 수 = 0; 수 < Araf_diir; 수++) {
            int xëyma = 문자[수];
            if (xëyma > 0 && xëyma < 128) biir_Lees_dul_soppi_okte(xëyma);
            else if (xëyma < 2048) { biir_Lees_dul_soppi_okte(192 | xëyma >> 6); biir_Lees_dul_soppi_okte(128 | xëyma & 63); }
            else { biir_Lees_dul_soppi_okte(224 | xëyma >> 12); biir_Lees_dul_soppi_okte(128 | xëyma >> 6 & 63); biir_Lees_dul_soppi_okte(128 | xëyma & 63); }
        }
        if (njumte) return 0;
        int diir_xëyma = Lees_dul_soppi_tolluwaay - daw - 3;
        Lees_dul_soppi_xëyma[daw + 1] = diir_xëyma >> 8; Lees_dul_soppi_xëyma[daw + 2] = diir_xëyma & 255;
        return bindu_Lees_dul_soppi(daw);
    }
    static int Word_Lees_dul_soppi(String Word_SMS) { Araf_diir = 0; 말추가(Word_SMS); return Araf_Lees_dul_soppi(); }
    static int jeton_Lees_dul_soppi(int jeton_xëyma) {
        Araf_diir = 0;
        for (int 수 = 0; 수 < jeton_diir[jeton_xëyma]; 수++) 글추가(Cosaan[토큰위치[jeton_xëyma] + 수]);
        return Araf_Lees_dul_soppi();
    }
    static int Royukaay(int 종류, int 가, int 나) {
        int daw = Lees_dul_soppi_tolluwaay; biir_Lees_dul_soppi_okte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return bindu_Lees_dul_soppi(daw);
    }
    static int 외부참조(int 종류, String boroom_xëyma, String tur_253d1510, String 서술) {
        int boroom_raññeekaay = Royukaay(7, Word_Lees_dul_soppi(boroom_xëyma), 0);
        int 이름수 = Word_Lees_dul_soppi(tur_253d1510), 형식수 = Word_Lees_dul_soppi(서술);
        return Royukaay(종류, boroom_raññeekaay, Royukaay(12, 이름수, 형식수));
    }
    static void 내보내기(int xëyma) {
        if (코드크기 == 코드.length) { foo_xëyma("bytecode too large"); return; }
        코드[코드크기++] = xëyma & 255;
    }
    static void ndigel(int xëyma, int 인수) { 내보내기(xëyma); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int xëyma) {
        if (xëyma >= -1 && xëyma <= 5) { 내보내기(xëyma + 3); return; }
        int daw = Lees_dul_soppi_tolluwaay; biir_Lees_dul_soppi_okte(3); 상짧(xëyma >>> 16); 상짧(xëyma);
        ndigel(19, bindu_Lees_dul_soppi(daw));
    }
    static int car(int ndigel) { int 결과 = 코드크기; ndigel(ndigel, 0); return 결과; }
    static void lëkkale_xëyma(int car, int luñu_name_yëf) {
        if (njumte) return;
        int 거리 = luñu_name_yëf - car;
        if (거리 < -32768 || 거리 > 32767 || car < 0 || car + 2 >= 코드크기) { foo_xëyma("invalid branch"); return; }
        코드[car + 1] = 거리 >> 8 & 255; 코드[car + 2] = 거리 & 255;
    }
    static void 비교값(int ndigel) {
        int 참 = car(ndigel); 내보내기(3); int 끝 = car(167);
        lëkkale_xëyma(참, 코드크기); 내보내기(4); lëkkale_xëyma(끝, 코드크기);
    }
    static int dayo_xëyma() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        foo_xëyma("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void mottal_dayo(int xeet_xëyma) {
        if (xeet_xëyma == 0) 글추가('V');
        if (xeet_xëyma == 1) 글추가('I');
        if (xeet_xëyma == 2) 글추가('Z');
        if (xeet_xëyma == 3) 말추가("Ljava/lang/String;");
        if (xeet_xëyma == 4) 말추가("[Ljava/lang/String;");
        if (xeet_xëyma == 5) 글추가('C');
        if (xeet_xëyma == 6) 말추가("Ljava/io/FileInputStream;");
        if (xeet_xëyma == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 yokkute_xëyma_dugal_xabaar 본문은 dalal javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("TABLO_Store_foo") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        foo_xëyma("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (Word_xëyma(위치, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) foo_xëyma("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); maas_jeton = raññeekaay_xëyma();
        maas_Lees_dul_soppi = Royukaay(7, jeton_Lees_dul_soppi(maas_jeton), 0);
        부모상수 = Royukaay(7, Word_Lees_dul_soppi("java/lang/Object"), 0); 코드상수 = Word_Lees_dul_soppi("Code"); 요구('{');
        while (!njumte && 종류() != '}') {
            if (함수수 == 32) { foo_xëyma("too many methods"); break; }
            int jot_dugal_xabaar = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int liëey_xëyma = 함수수++;
            doxalin_jot[liëey_xëyma] = jot_dugal_xabaar | 8;
            함수반환[liëey_xëyma] = dayo_xëyma(); doxalin_dugal_xabaar_tur[liëey_xëyma] = raññeekaay_xëyma(); 요구('(');
            for (int 앞 = 0; 앞 < liëey_xëyma; 앞++) if (이름같음(doxalin_dugal_xabaar_tur[앞], doxalin_dugal_xabaar_tur[liëey_xëyma])) foo_xëyma("duplicate method (overloading unsupported)");
            while (!njumte && 종류() != ')') {
                int 수 = 함수인수수[liëey_xëyma];
                if (수 == 16) { foo_xëyma("too many parameters"); break; }
                int xeet_xëyma = dayo_xëyma(); if (xeet_xëyma == 0) foo_xëyma("void parameter");
                doxalin_Tegtal_xeet[liëey_xëyma * 16 + 수] = xeet_xëyma; doxalin_Tegtal_tur[liëey_xëyma * 16 + 수] = raññeekaay_xëyma();
                함수인수수[liëey_xëyma]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!njumte && 받기(','));
            }
            함수본문[liëey_xëyma] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) foo_xëyma("unclosed method body");
            doxalin_jeexal[liëey_xëyma] = 위치;
            doxalin_tur_Lees_dul_soppi[liëey_xëyma] = jeton_Lees_dul_soppi(doxalin_dugal_xabaar_tur[liëey_xëyma]);
            Araf_diir = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[liëey_xëyma]; 수++) mottal_dayo(doxalin_Tegtal_xeet[liëey_xëyma * 16 + 수]);
            글추가(')'); mottal_dayo(함수반환[liëey_xëyma]); 함수서술[liëey_xëyma] = Araf_Lees_dul_soppi();
        }
        요구('}'); if (위치 != 토큰수) foo_xëyma("extra input after class");
    }
    static int seet_dënnd(int tur_253d1510) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(dënnd_tur[수], tur_253d1510)) return 수;
        foo_xëyma("unknown variable"); return 0;
    }
    static int mottal_dënnd(int tur_253d1510, int xeet_xëyma) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(dënnd_tur[수], tur_253d1510)) foo_xëyma("duplicate local variable");
        if (지역수 == 128) { foo_xëyma("too many locals"); return 0; }
        dënnd_tur[지역수] = tur_253d1510; dënnd_xeet[지역수] = xeet_xëyma; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean lëmm_xeet(int xeet_xëyma) { return xeet_xëyma == 1 || xeet_xëyma == 5; }
    static void 지역읽기(int 수) { 내보내기(dënnd_xeet[수] <= 2 || dënnd_xeet[수] == 5 ? 21 : 25); 내보내기(수); }
    static void biir_dënnd(int 수) { 내보내기(dënnd_xeet[수] <= 2 || dënnd_xeet[수] == 5 ? 54 : 58); 내보내기(수); }
    static void luñutu_xeet(int liteew_mbir, int 기대) { if (liteew_mbir != 기대 && !(liteew_mbir == 5 && 기대 == 1)) foo_xëyma("type mismatch"); }
    static void 문자읽기(int jeton_xëyma) {
        Araf_diir = 0; int daw = 토큰위치[jeton_xëyma] + 1, 끝 = 토큰위치[jeton_xëyma] + jeton_diir[jeton_xëyma] - 1;
        while (daw < 끝 && !njumte) {
            int xëyma = Cosaan[daw++];
            if (xëyma == '\\') {
                if (daw == 끝) { foo_xëyma("invalid escape"); break; }
                xëyma = Cosaan[daw++];
                if (xëyma == 'n') xëyma = 10;
                else if (xëyma == 'r') xëyma = 13;
                else if (xëyma == 't') xëyma = 9;
                else if (xëyma == 'b') xëyma = 8;
                else if (xëyma == 'f') xëyma = 12;
                else if (xëyma != '\\' && xëyma != '"' && xëyma != '\'') foo_xëyma("unsupported escape");
            }
            글추가(xëyma);
        }
    }
    static int Segg_lëmm(int jeton_xëyma, boolean 음수) {
        if (jeton_diir[jeton_xëyma] > 1 && Cosaan[토큰위치[jeton_xëyma]] == '0') foo_xëyma("octal literals unsupported");
        int xëyma = 0;
        for (int 수 = 0; 수 < jeton_diir[jeton_xëyma]; 수++) {
            int siifar_ëmbeef = Cosaan[토큰위치[jeton_xëyma] + 수] - '0';
            if (xëyma < -214748364 || xëyma == -214748364 && siifar_ëmbeef > (음수 ? 8 : 7)) foo_xëyma("integer literal out of range");
            xëyma = xëyma * 10 - siifar_ëmbeef;
        }
        return 음수 ? xëyma : -xëyma;
    }
    static int 기본식() {
        if (말받기("new")) {
            int xeet_xëyma = dayo_xëyma();
            if (xeet_xëyma != 6 && xeet_xëyma != 7) { foo_xëyma("only file streams supported by new in source"); return 0; }
            String boroom_xëyma = xeet_xëyma == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            ndigel(187, Royukaay(7, Word_Lees_dul_soppi(boroom_xëyma), 0)); 내보내기(89);
            요구('('); luñutu_xeet(guddalinu_méngale_xëyma(), 3); boolean 이어 = false;
            if (받기(',')) { if (xeet_xëyma != 7) foo_xëyma("input stream constructor arguments"); luñutu_xeet(guddalinu_méngale_xëyma(), 2); 이어 = true; }
            요구(')');
            ndigel(183, 외부참조(10, boroom_xëyma, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return xeet_xëyma;
        }
        if (받기('(')) { int xeet_xëyma = guddalinu_méngale_xëyma(); 요구(')'); return xeet_xëyma; }
        if (종류() == 257) { 수상수(Segg_lëmm(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); ndigel(19, Royukaay(8, Araf_Lees_dul_soppi(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (Araf_diir != 1) foo_xëyma("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String boroom_xëyma = "", doxalin_xëyma = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                boroom_xëyma = "한국어/자체/출력"; 요구('.');
                if (말받기("biir_buum")) { doxalin_xëyma = "biir_buum"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("biir")) { doxalin_xëyma = "biir"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { doxalin_xëyma = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else foo_xëyma("unknown Korean output method");
            } else if (말받기("문자")) {
                boroom_xëyma = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("diir_xëyma")) { doxalin_xëyma = "diir_xëyma"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { doxalin_xëyma = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("Segg_lëmm")) { doxalin_xëyma = "Segg_lëmm"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("biir_lëmm_xëyma")) { doxalin_xëyma = "biir_lëmm_xëyma"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { doxalin_xëyma = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("Taf_SMS")) { doxalin_xëyma = "Taf_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("dogandi_xëyma")) { doxalin_xëyma = "dogandi_xëyma"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else foo_xëyma("unknown Korean text method");
            } else if (말받기("bara_denc")) {
                boroom_xëyma = "한국어/자체/bara_denc"; 요구('.'); 가 = 3;
                if (말받기("읽기")) { doxalin_xëyma = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("biir")) { doxalin_xëyma = "biir"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else foo_xëyma("unknown Korean file method");
            } else if (말받기("화면")) {
                boroom_xëyma = "한국어/자체/화면"; 요구('.');
                if (말받기("너비")) { doxalin_xëyma = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { doxalin_xëyma = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { doxalin_xëyma = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { doxalin_xëyma = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { doxalin_xëyma = "기다리기"; 서술 = "()V"; }
                else foo_xëyma("unknown Korean framebuffer method");
            } else foo_xëyma("unsupported Korean library class");
            요구('('); if (가 != 0) luñutu_xeet(guddalinu_méngale_xëyma(), 가);
            if (나 != 0) { 요구(','); luñutu_xeet(guddalinu_méngale_xëyma(), 나); }
            if (다 != 0) { 요구(','); luñutu_xeet(guddalinu_méngale_xëyma(), 다); }
            if (라 != 0) { 요구(','); luñutu_xeet(guddalinu_méngale_xëyma(), 라); }
            if (마 != 0) { 요구(','); luñutu_xeet(guddalinu_méngale_xëyma(), 마); }
            요구(')'); ndigel(184, 외부참조(10, boroom_xëyma, doxalin_xëyma, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); luñutu_xeet(guddalinu_méngale_xëyma(), 3); 요구(')');
            ndigel(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int tur_253d1510 = raññeekaay_xëyma();
        if (받기('(')) {
            int liëey_xëyma = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(tur_253d1510, doxalin_dugal_xabaar_tur[수])) liëey_xëyma = 수;
            if (liëey_xëyma < 0) { foo_xëyma("unknown static method"); return 0; }
            int 수 = 0;
            while (!njumte && 종류() != ')') {
                if (수 >= 함수인수수[liëey_xëyma]) { foo_xëyma("too many arguments"); break; }
                luñutu_xeet(guddalinu_méngale_xëyma(), doxalin_Tegtal_xeet[liëey_xëyma * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[liëey_xëyma]) foo_xëyma("argument count mismatch");
            ndigel(184, Royukaay(10, maas_Lees_dul_soppi, Royukaay(12, doxalin_tur_Lees_dul_soppi[liëey_xëyma], 함수서술[liëey_xëyma])));
            return 함수반환[liëey_xëyma];
        }
        int dënnd_nameef = seet_dënnd(tur_253d1510), xeet_xëyma = dënnd_xeet[dënnd_nameef]; 지역읽기(dënnd_nameef);
        while (!njumte) {
            if (받기('[')) { luñutu_xeet(xeet_xëyma, 4); luñutu_xeet(guddalinu_méngale_xëyma(), 1); 요구(']'); 내보내기(50); xeet_xëyma = 3; }
            else if (받기('.')) {
                if (xeet_xëyma == 6 || xeet_xëyma == 7) {
                    String boroom_xëyma = xeet_xëyma == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); ndigel(182, 외부참조(10, boroom_xëyma, "close", "()V")); xeet_xëyma = 0; }
                    else if (xeet_xëyma == 6 && 말받기("read")) { 요구('('); 요구(')'); ndigel(182, 외부참조(10, boroom_xëyma, "read", "()I")); xeet_xëyma = 1; }
                    else if (xeet_xëyma == 7 && 말받기("write")) { 요구('('); luñutu_xeet(guddalinu_méngale_xëyma(), 1); 요구(')'); ndigel(182, 외부참조(10, boroom_xëyma, "write", "(I)V")); xeet_xëyma = 0; }
                    else { foo_xëyma("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (xeet_xëyma == 4) { 내보내기(190); xeet_xëyma = 1; }
                else { luñutu_xeet(xeet_xëyma, 3); 요구('('); 요구(')'); ndigel(182, 외부참조(10, "java/lang/String", "length", "()I")); xeet_xëyma = 1; }
            } else break;
        }
        return xeet_xëyma;
    }
    static int 단항() {
        if (++식깊이 > 64) { foo_xëyma("expression nesting too deep"); 식깊이--; return 0; }
        int xeet_xëyma;
        if (받기('!')) { luñutu_xeet(단항(), 2); 비교값(153); xeet_xëyma = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(Segg_lëmm(위치++, true));
            else { luñutu_xeet(단항(), 1); 내보내기(116); }
            xeet_xëyma = 1;
        } else if (받기('+')) { luñutu_xeet(단항(), 1); xeet_xëyma = 1; }
        else xeet_xëyma = 기본식();
        식깊이--; return xeet_xëyma;
    }
    static int 곱식() {
        int xeet_xëyma = 단항();
        while (!njumte && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int nëbbin_ci_lim_xëyma = 종류(); 위치++; luñutu_xeet(xeet_xëyma, 1); luñutu_xeet(단항(), 1);
            내보내기(nëbbin_ci_lim_xëyma == '*' ? 104 : nëbbin_ci_lim_xëyma == '/' ? 108 : 112); xeet_xëyma = 1;
        }
        return xeet_xëyma;
    }
    static int 합식() {
        int xeet_xëyma = 곱식();
        while (!njumte && (종류() == '+' || 종류() == '-')) {
            int nëbbin_ci_lim_xëyma = 종류(); 위치++; int 경계 = 코드크기, woñeeku_xëyma_xeet = 곱식();
            if (nëbbin_ci_lim_xëyma == '+' && (xeet_xëyma == 3 || woñeeku_xëyma_xeet == 3)) { 결합(경계, xeet_xëyma, woñeeku_xëyma_xeet); xeet_xëyma = 3; }
            else { luñutu_xeet(xeet_xëyma, 1); luñutu_xeet(woñeeku_xëyma_xeet, 1); 내보내기(nëbbin_ci_lim_xëyma == '+' ? 96 : 100); xeet_xëyma = 1; }
        }
        return xeet_xëyma;
    }
    static int 붙임참조(int xeet_xëyma) {
        if (xeet_xëyma != 1 && xeet_xëyma != 2 && xeet_xëyma != 3 && xeet_xëyma != 5) foo_xëyma("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", xeet_xëyma == 1 ? "(I)Ljava/lang/StringBuilder;"
            : xeet_xëyma == 2 ? "(Z)Ljava/lang/StringBuilder;" : xeet_xëyma == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int woñeeku_xëyma_xeet) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 guddalinu_méngale_xëyma 내부의 Nàttangoo_xëyma car 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        ndigel(187, Royukaay(7, Word_Lees_dul_soppi("java/lang/StringBuilder"), 0)); 내보내기(89);
        ndigel(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); ndigel(182, 붙임참조(앞형));
        if (njumte) return;
        int diir_xëyma = 코드크기 - 끝;
        for (int 수 = 0; 수 < diir_xëyma; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + diir_xëyma] = 코드[수];
        for (int 수 = 0; 수 < diir_xëyma; 수++) 코드[경계 + 수] = 삽입코드[수];
        ndigel(182, 붙임참조(woñeeku_xëyma_xeet)); ndigel(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int xeet_xëyma = 합식();
        while (!njumte && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int nëbbin_ci_lim_xëyma = 종류(); 위치++; luñutu_xeet(xeet_xëyma, 1); luñutu_xeet(합식(), 1);
            비교값(nëbbin_ci_lim_xëyma == '<' ? 161 : nëbbin_ci_lim_xëyma == '>' ? 163 : nëbbin_ci_lim_xëyma == 302 ? 164 : 162); xeet_xëyma = 2;
        }
        return xeet_xëyma;
    }
    static int 동등식() {
        int xeet_xëyma = 비교식();
        while (!njumte && (종류() == 300 || 종류() == 301)) {
            int nëbbin_ci_lim_xëyma = 종류(); 위치++; int woñeeku_xëyma_xeet = 비교식();
            if (xeet_xëyma == 0 || woñeeku_xëyma_xeet == 0) foo_xëyma("void expression");
            if (!(lëmm_xeet(xeet_xëyma) && lëmm_xeet(woñeeku_xëyma_xeet))) luñutu_xeet(woñeeku_xëyma_xeet, xeet_xëyma);
            비교값((xeet_xëyma <= 2 || xeet_xëyma == 5 ? 159 : 165) + (nëbbin_ci_lim_xëyma == 301 ? 1 : 0)); xeet_xëyma = 2;
        }
        return xeet_xëyma;
    }
    static int 논리곱() {
        int xeet_xëyma = 동등식();
        while (!njumte && 받기(304)) {
            luñutu_xeet(xeet_xëyma, 2); int 가 = car(153); luñutu_xeet(동등식(), 2); int 나 = car(153);
            내보내기(4); int 끝 = car(167); lëkkale_xëyma(가, 코드크기); lëkkale_xëyma(나, 코드크기); 내보내기(3); lëkkale_xëyma(끝, 코드크기); xeet_xëyma = 2;
        }
        return xeet_xëyma;
    }
    static int guddalinu_méngale_xëyma() {
        int xeet_xëyma = 논리곱();
        while (!njumte && 받기(305)) {
            luñutu_xeet(xeet_xëyma, 2); int 가 = car(154); luñutu_xeet(논리곱(), 2); int 나 = car(154);
            내보내기(3); int 끝 = car(167); lëkkale_xëyma(가, 코드크기); lëkkale_xëyma(나, 코드크기); 내보내기(4); lëkkale_xëyma(끝, 코드크기); xeet_xëyma = 2;
        }
        return xeet_xëyma;
    }
    static void santaane_bi_xëyma(boolean 선언허용) {
        if (Word_xëyma(위치, "int") || Word_xëyma(위치, "boolean") || Word_xëyma(위치, "String") || Word_xëyma(위치, "char")
            || Word_xëyma(위치, "FileInputStream") || Word_xëyma(위치, "FileOutputStream")) {
            if (!선언허용) foo_xëyma("declaration not allowed here");
            int xeet_xëyma = dayo_xëyma(), tur_253d1510 = raññeekaay_xëyma(); 요구('='); luñutu_xeet(guddalinu_méngale_xëyma(), xeet_xëyma);
            biir_dënnd(mottal_dënnd(tur_253d1510, xeet_xëyma)); return;
        }
        int tur_253d1510 = raññeekaay_xëyma(), dënnd_nameef = seet_dënnd(tur_253d1510);
        if (받기('=')) { luñutu_xeet(guddalinu_méngale_xëyma(), dënnd_xeet[dënnd_nameef]); biir_dënnd(dënnd_nameef); }
        else if (종류() >= 308 && 종류() <= 312) {
            int nëbbin_ci_lim_xëyma = 종류(); 위치++; 지역읽기(dënnd_nameef); int 경계 = 코드크기, woñeeku_xëyma_xeet = guddalinu_méngale_xëyma();
            if (nëbbin_ci_lim_xëyma == 308 && dënnd_xeet[dënnd_nameef] == 3) 결합(경계, 3, woñeeku_xëyma_xeet);
            else {
                luñutu_xeet(dënnd_xeet[dënnd_nameef], 1); luñutu_xeet(woñeeku_xëyma_xeet, 1);
                내보내기(nëbbin_ci_lim_xëyma == 308 ? 96 : nëbbin_ci_lim_xëyma == 309 ? 100 : nëbbin_ci_lim_xëyma == 310 ? 104 : nëbbin_ci_lim_xëyma == 311 ? 108 : 112);
                if (dënnd_xeet[dënnd_nameef] == 5) 내보내기(146);
            }
            biir_dënnd(dënnd_nameef);
        }
        else if (종류() == 306 || 종류() == 307) {
            luñutu_xeet(dënnd_xeet[dënnd_nameef], 1); 내보내기(132); 내보내기(dënnd_nameef); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (dënnd_xeet[dënnd_nameef] == 5) { 지역읽기(dënnd_nameef); 내보내기(146); biir_dënnd(dënnd_nameef); }
        } else foo_xëyma("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        ndigel(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean neen_Tegtal = 종류() == ')';
        int xeet_xëyma = neen_Tegtal ? 0 : guddalinu_méngale_xëyma(); 요구(')'); 요구(';');
        String 서술 = xeet_xëyma == 0 ? "()V" : xeet_xëyma == 1 ? "(I)V" : xeet_xëyma == 2 ? "(Z)V" : xeet_xëyma == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (xeet_xëyma == 4 || xeet_xëyma >= 6 || xeet_xëyma == 0 && (!줄바꿈 || !neen_Tegtal)) foo_xëyma("unsupported print argument");
        ndigel(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean nétali_xëyma() {
        if (njumte) return false;
        if (깊이 > 32) { foo_xëyma("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!njumte && 종류() != '}') { if (반환) foo_xëyma("unreachable statement"); 반환 = nétali_xëyma(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int xeet_xëyma = 종류() == ';' ? 0 : guddalinu_méngale_xëyma(); luñutu_xeet(xeet_xëyma, 함수반환[현재함수]); 요구(';');
            내보내기(xeet_xëyma == 0 ? 177 : xeet_xëyma <= 2 || xeet_xëyma == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); luñutu_xeet(guddalinu_méngale_xëyma(), 2); 요구(')'); int 거짓 = car(153);
            깊이++; boolean 가 = Saytu_doxinu_ordinateur_nétali(); 깊이--;
            if (말받기("else")) { int 끝 = car(167); lëkkale_xëyma(거짓, 코드크기); 깊이++; boolean 나 = Saytu_doxinu_ordinateur_nétali(); 깊이--; lëkkale_xëyma(끝, 코드크기); return 가 && 나; }
            lëkkale_xëyma(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int daw = 코드크기; 요구('('); luñutu_xeet(guddalinu_méngale_xëyma(), 2); 요구(')'); int 끝 = car(153);
            깊이++; Saytu_doxinu_ordinateur_nétali(); 깊이--; lëkkale_xëyma(car(167), daw); lëkkale_xëyma(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') santaane_bi_xëyma(true); 요구(';');
            int anam = 코드크기; if (종류() == ';') 내보내기(4); else luñutu_xeet(guddalinu_méngale_xëyma(), 2); 요구(';');
            int 끝 = car(153), yaxub_mool = car(167), Yeesal = 코드크기;
            if (종류() != ')') santaane_bi_xëyma(false); 요구(')'); lëkkale_xëyma(car(167), anam); lëkkale_xëyma(yaxub_mool, 코드크기);
            Saytu_doxinu_ordinateur_nétali(); lëkkale_xëyma(car(167), Yeesal); lëkkale_xëyma(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_xëyma(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int xeet_xëyma = guddalinu_méngale_xëyma(); if (xeet_xëyma != 0) 내보내기(87); 요구(';'); return false;
        }
        santaane_bi_xëyma(true); 요구(';'); return false;
    }
    static boolean Saytu_doxinu_ordinateur_nétali() {
        if (Word_xëyma(위치, "int") || Word_xëyma(위치, "boolean") || Word_xëyma(위치, "char") || Word_xëyma(위치, "String")
            || Word_xëyma(위치, "FileInputStream") || Word_xëyma(위치, "FileOutputStream")) foo_xëyma("local declaration requires braces");
        return nétali_xëyma();
    }
    static void 출바(int xëyma) { if (출력크기 == 출력.length) foo_xëyma("class file too large"); else 출력[출력크기++] = xëyma & 255; }
    static void 출짧(int xëyma) { 출바(xëyma >> 8); 출바(xëyma); }
    static void 출정(int xëyma) { 출짧(xëyma >>> 16); 출짧(xëyma); }
    static void biir_maas() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < Lees_dul_soppi_tolluwaay; 수++) 출바(Lees_dul_soppi_xëyma[수]);
        출짧(0x21); 출짧(maas_Lees_dul_soppi); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(doxalin_jot[수]); 출짧(doxalin_tur_Lees_dul_soppi[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + doxalin_diir[수]); 출짧(128); 출짧(함수지역[수]); 출정(doxalin_diir[수]);
            for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < doxalin_diir[수]; xar_xar_dugal_xabaar++) 출바(코드[함수코드[수] + xar_xar_dugal_xabaar]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int daw() {
        if (kiy_jariñoo_internet.인수개수() == 1 && 자바도구.같음(kiy_jariñoo_internet.인수(0), "-version")) {
            kiy_jariñoo_internet.biir("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (kiy_jariñoo_internet.인수개수() != 1) { kiy_jariñoo_internet.biir("Usage: javac FILE.java\n"); return 2; }
        int tur_tolluwaay = 자바도구.tur_253d1510(bara_denc_tur_SMS, kiy_jariñoo_internet.인수(0));
        if (tur_tolluwaay < 6 || tur_tolluwaay > 62 || bara_denc_tur_SMS[tur_tolluwaay - 5] != '.' || bara_denc_tur_SMS[tur_tolluwaay - 4] != 'j'
            || bara_denc_tur_SMS[tur_tolluwaay - 3] != 'a' || bara_denc_tur_SMS[tur_tolluwaay - 2] != 'v' || bara_denc_tur_SMS[tur_tolluwaay - 1] != 'a') {
            kiy_jariñoo_internet.biir("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        Cosaan_tolluwaay = kiy_jariñoo_internet.파일읽기(bara_denc_tur_SMS, Cosaan);
        if (Cosaan_tolluwaay < 0) { kiy_jariñoo_internet.biir("javac: cannot read source: "); 자바도구.수쓰기(Cosaan_tolluwaay); kiy_jariñoo_internet.biir_Araf_xëyma(10); return 1; }
        Cosaan_tolluwaay = 자바도구.원문해독(Cosaan, Cosaan_tolluwaay);
        if (Cosaan_tolluwaay < 0) { kiy_jariñoo_internet.biir("javac error: invalid UTF-8 source\n"); return 1; }
        dogandi_xëyma(); if (!njumte) 선언읽기();
        if (!njumte) {
            if (jeton_diir[maas_jeton] != tur_tolluwaay - 5) foo_xëyma("class name must match file name");
            for (int 수 = 0; 수 < tur_tolluwaay - 5; 수++) if (Cosaan[토큰위치[maas_jeton] + 수] != bara_denc_tur_SMS[수]) foo_xëyma("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !njumte; 현재함수++) {
            위치 = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) mottal_dënnd(doxalin_Tegtal_tur[현재함수 * 16 + 수], doxalin_Tegtal_xeet[현재함수 * 16 + 수]);
            boolean 반환 = nétali_xëyma();
            if (!반환 && 함수반환[현재함수] != 0) foo_xëyma("missing return");
            // car 뒤의 합류 지점은 반드시 liteew_mbir 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean lëmm = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(lëmm ? 3 : 1); 내보내기(lëmm ? 172 : 176); }
            if (위치 != doxalin_jeexal[현재함수]) foo_xëyma("invalid method body");
            함수지역[현재함수] = 지역수; doxalin_diir[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (njumte) return 1;
        biir_maas(); if (njumte) return 1;
        bara_denc_tur_SMS[tur_tolluwaay - 4] = 'c'; bara_denc_tur_SMS[tur_tolluwaay - 3] = 'l'; bara_denc_tur_SMS[tur_tolluwaay - 2] = 'a';
        bara_denc_tur_SMS[tur_tolluwaay - 1] = 's'; bara_denc_tur_SMS[tur_tolluwaay] = 's'; bara_denc_tur_SMS[tur_tolluwaay + 1] = 0;
        int 결과 = kiy_jariñoo_internet.biir_bara_denc(bara_denc_tur_SMS, 출력, 출력크기);
        if (결과 < 0) { kiy_jariñoo_internet.biir("javac: cannot save class: "); 자바도구.수쓰기(결과); kiy_jariñoo_internet.biir_Araf_xëyma(10); return 1; }
        kiy_jariñoo_internet.biir("Compiled: "); for (int 수 = 0; bara_denc_tur_SMS[수] != 0; 수++) kiy_jariñoo_internet.biir_Araf_xëyma(bara_denc_tur_SMS[수]);
        kiy_jariñoo_internet.biir(" (JVM class version 49)\n"); return 0;
    }
}
