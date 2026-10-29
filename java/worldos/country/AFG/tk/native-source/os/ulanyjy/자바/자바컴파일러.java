// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java gor_agaç -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] Çeşme = new int[16384], 출력 = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], token_dowamlylyk = new int[2048];
    static int[] hemişelik_baha = new int[4096], hemişelik_Süýşüriş = new int[512];
    static int[] 문자 = new int[512], faýl_at_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int gor_ölçegi_üýtget, 토큰수, 위치, 코드크기, hemişelik_ölçegi_üýtget, 상수수 = 1, 출력크기, nyşan_dowamlylyk;
    static boolean Hata;
    static int klas_token, klas_hemişelik, 부모상수, 코드상수;
    static int[] usul_girizmeklik_at = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] usul_argument_at = new int[512], usul_argument_ýaz = new int[512];
    static int[] 함수본문 = new int[32], usul_tamamla = new int[32], 함수코드 = new int[32];
    static int[] usul_dowamlylyk = new int[32], 함수지역 = new int[32], usul_at_hemişelik = new int[32], 함수서술 = new int[32];
    static int[] usul_ygtyýarlylyk = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] ýerli_at = new int[128], ýerli_ýaz = new int[128], 지역깊이 = new int[128];

    static void näsazlyk_baha(String 이유) {
        if (!Hata) {
            ulanyjy.Ýaz("javac error: "); ulanyjy.Ýaz(이유);
            ulanyjy.Ýaz(" at line ");
            int setir = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : gor_ölçegi_üýtget;
            for (int 수 = 0; 수 < 끝; 수++) if (Çeşme[수] == 10) setir++;
            자바도구.수쓰기(setir); ulanyjy.ýaz_nyşan_baha(10);
        }
        Hata = true;
    }
    static boolean nyşan_baha_068c2631(int baha) { return 문자이름규칙.첫글자(baha); }
    static boolean san_baha(int baha) { return baha >= '0' && baha <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || token_dowamlylyk[가] != token_dowamlylyk[나]) return false;
        for (int 수 = 0; 수 < token_dowamlylyk[가]; 수++) if (Çeşme[토큰위치[가] + 수] != Çeşme[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean Söz_baha(int token_baha, String Söz_SMS) {
        if (token_baha < 0 || token_baha >= 토큰수 || token_dowamlylyk[token_baha] != Söz_SMS.length()) return false;
        for (int 수 = 0; 수 < Söz_SMS.length(); 수++) if (Çeşme[토큰위치[token_baha] + 수] != Söz_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int baha) { if (종류() != baha) return false; 위치++; return true; }
    static void 요구(int baha) { if (!받기(baha)) näsazlyk_baha("unexpected token"); }
    static boolean 말받기(String Söz_SMS) { if (!Söz_baha(위치, Söz_SMS)) return false; 위치++; return true; }
    static void 말요구(String Söz_SMS) { if (!말받기(Söz_SMS)) näsazlyk_baha(Söz_SMS); }
    static int tanaýjy_baha() {
        int 결과 = 위치;
        if (종류() != 256) näsazlyk_baha("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Bitir = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Bitir == token_dowamlylyk[결과];
                for (int ýer_girizmeklik = Bitir; 같음 && ýer_girizmeklik < 수; ýer_girizmeklik++) if (예약어.charAt(ýer_girizmeklik) != Çeşme[토큰위치[결과] + ýer_girizmeklik - Bitir]) 같음 = false;
                if (같음) näsazlyk_baha("reserved word cannot be an identifier");
                Bitir = 수 + 1;
            }
        }
        return 결과;
    }
    static void kes_baha() {
        int 수 = 0;
        while (수 < gor_ölçegi_üýtget && !Hata) {
            int baha = Çeşme[수], Bitir = 수, 종류 = baha;
            if (baha == 32 || baha == 9 || baha == 10 || baha == 13) { 수++; continue; }
            if (baha == '/' && 수 + 1 < gor_ölçegi_üýtget && Çeşme[수 + 1] == '/') {
                while (수 < gor_ölçegi_üýtget && Çeşme[수] != 10) 수++;
                continue;
            }
            if (baha == '/' && 수 + 1 < gor_ölçegi_üýtget && Çeşme[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < gor_ölçegi_üýtget && !(Çeşme[수] == '*' && Çeşme[수 + 1] == '/')) 수++;
                if (수 + 1 >= gor_ölçegi_üýtget) { näsazlyk_baha("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (nyşan_baha_068c2631(baha)) { 종류 = 256; while (수 < gor_ölçegi_üýtget && 문자이름규칙.이어진글자(Çeşme[수])) 수++; }
            else if (san_baha(baha)) { 종류 = 257; while (수 < gor_ölçegi_üýtget && san_baha(Çeşme[수])) 수++; }
            else if (baha == '"' || baha == '\'') {
                종류 = baha == '"' ? 258 : 259; 수++;
                while (수 < gor_ölçegi_üýtget && Çeşme[수] != baha && Çeşme[수] != 10 && Çeşme[수] != 13) {
                    if (Çeşme[수] == '\\') 수++;
                    수++;
                }
                if (수 >= gor_ölçegi_üýtget || Çeşme[수] != baha) { näsazlyk_baha("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < gor_ölçegi_üýtget) {
                    int 다음 = Çeşme[수];
                    if (baha == '=' && 다음 == '=') 종류 = 300;
                    if (baha == '!' && 다음 == '=') 종류 = 301;
                    if (baha == '<' && 다음 == '=') 종류 = 302;
                    if (baha == '>' && 다음 == '=') 종류 = 303;
                    if (baha == '&' && 다음 == '&') 종류 = 304;
                    if (baha == '|' && 다음 == '|') 종류 = 305;
                    if (baha == '+' && 다음 == '+') 종류 = 306;
                    if (baha == '-' && 다음 == '-') 종류 = 307;
                    if (baha == '+' && 다음 == '=') 종류 = 308;
                    if (baha == '-' && 다음 == '=') 종류 = 309;
                    if (baha == '*' && 다음 == '=') 종류 = 310;
                    if (baha == '/' && 다음 == '=') 종류 = 311;
                    if (baha == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { näsazlyk_baha("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = Bitir; token_dowamlylyk[토큰수++] = 수 - Bitir;
        }
    }
    static void ýaz_hemişelik_baýt(int baha) {
        if (hemişelik_ölçegi_üýtget == hemişelik_baha.length) { näsazlyk_baha("constant pool too large"); return; }
        hemişelik_baha[hemişelik_ölçegi_üýtget++] = baha & 255;
    }
    static void 상짧(int baha) { ýaz_hemişelik_baýt(baha >> 8); ýaz_hemişelik_baýt(baha); }
    static int 상등록(int Bitir) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = hemişelik_Süýşüriş[수], dowamlylyk_baha = (수 + 1 < 상수수 ? hemişelik_Süýşüriş[수 + 1] : Bitir) - 앞;
            if (dowamlylyk_baha != hemişelik_ölçegi_üýtget - Bitir) continue;
            boolean 같음 = true;
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < dowamlylyk_baha; ýer_girizmeklik++) if (hemişelik_baha[앞 + ýer_girizmeklik] != hemişelik_baha[Bitir + ýer_girizmeklik]) 같음 = false;
            if (같음) { hemişelik_ölçegi_üýtget = Bitir; return 수; }
        }
        if (상수수 == hemişelik_Süýşüriş.length) { näsazlyk_baha("too many constants"); return 0; }
        hemişelik_Süýşüriş[상수수] = Bitir;
        return 상수수++;
    }
    static void 글추가(int baha) {
        if (nyşan_dowamlylyk == 문자.length) { näsazlyk_baha("text too long"); return; }
        문자[nyşan_dowamlylyk++] = baha;
    }
    static void 말추가(String Söz_SMS) { for (int 수 = 0; 수 < Söz_SMS.length(); 수++) 글추가(Söz_SMS.charAt(수)); }
    static int nyşan_hemişelik() {
        int Bitir = hemişelik_ölçegi_üýtget; ýaz_hemişelik_baýt(1); 상짧(0);
        for (int 수 = 0; 수 < nyşan_dowamlylyk; 수++) {
            int baha = 문자[수];
            if (baha > 0 && baha < 128) ýaz_hemişelik_baýt(baha);
            else if (baha < 2048) { ýaz_hemişelik_baýt(192 | baha >> 6); ýaz_hemişelik_baýt(128 | baha & 63); }
            else { ýaz_hemişelik_baýt(224 | baha >> 12); ýaz_hemişelik_baýt(128 | baha >> 6 & 63); ýaz_hemişelik_baýt(128 | baha & 63); }
        }
        if (Hata) return 0;
        int dowamlylyk_baha = hemişelik_ölçegi_üýtget - Bitir - 3;
        hemişelik_baha[Bitir + 1] = dowamlylyk_baha >> 8; hemişelik_baha[Bitir + 2] = dowamlylyk_baha & 255;
        return 상등록(Bitir);
    }
    static int Söz_hemişelik(String Söz_SMS) { nyşan_dowamlylyk = 0; 말추가(Söz_SMS); return nyşan_hemişelik(); }
    static int token_hemişelik(int token_baha) {
        nyşan_dowamlylyk = 0;
        for (int 수 = 0; 수 < token_dowamlylyk[token_baha]; 수++) 글추가(Çeşme[토큰위치[token_baha] + 수]);
        return nyşan_hemişelik();
    }
    static int Salgylanma(int 종류, int 가, int 나) {
        int Bitir = hemişelik_ölçegi_üýtget; ýaz_hemişelik_baýt(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return 상등록(Bitir);
    }
    static int 외부참조(int 종류, String eýe_baha, String Ad, String 서술) {
        int eýe_tanaýjy = Salgylanma(7, Söz_hemişelik(eýe_baha), 0);
        int 이름수 = Söz_hemişelik(Ad), 형식수 = Söz_hemişelik(서술);
        return Salgylanma(종류, eýe_tanaýjy, Salgylanma(12, 이름수, 형식수));
    }
    static void 내보내기(int baha) {
        if (코드크기 == 코드.length) { näsazlyk_baha("bytecode too large"); return; }
        코드[코드크기++] = baha & 255;
    }
    static void buýruk(int baha, int 인수) { 내보내기(baha); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int baha) {
        if (baha >= -1 && baha <= 5) { 내보내기(baha + 3); return; }
        int Bitir = hemişelik_ölçegi_üýtget; ýaz_hemişelik_baýt(3); 상짧(baha >>> 16); 상짧(baha);
        buýruk(19, 상등록(Bitir));
    }
    static int şahalanma(int buýruk) { int 결과 = 코드크기; buýruk(buýruk, 0); return 결과; }
    static void Bag_baha(int şahalanma, int niýet_obýekt) {
        if (Hata) return;
        int 거리 = niýet_obýekt - şahalanma;
        if (거리 < -32768 || 거리 > 32767 || şahalanma < 0 || şahalanma + 2 >= 코드크기) { näsazlyk_baha("invalid branch"); return; }
        코드[şahalanma + 1] = 거리 >> 8 & 255; 코드[şahalanma + 2] = 거리 & 255;
    }
    static void 비교값(int buýruk) {
        int 참 = şahalanma(buýruk); 내보내기(3); int 끝 = şahalanma(167);
        Bag_baha(참, 코드크기); 내보내기(4); Bag_baha(끝, 코드크기);
    }
    static int format_baha() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        näsazlyk_baha("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void goş_format(int ýaz_baha) {
        if (ýaz_baha == 0) 글추가('V');
        if (ýaz_baha == 1) 글추가('I');
        if (ýaz_baha == 2) 글추가('Z');
        if (ýaz_baha == 3) 말추가("Ljava/lang/String;");
        if (ýaz_baha == 4) 말추가("[Ljava/lang/String;");
        if (ýaz_baha == 5) 글추가('C');
        if (ýaz_baha == 6) 말추가("Ljava/io/FileInputStream;");
        if (ýaz_baha == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Proses_baha_girizmeklik 본문은 esasy javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("ARRAY_Store_näsazlyk") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        näsazlyk_baha("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (Söz_baha(위치, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) näsazlyk_baha("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); klas_token = tanaýjy_baha();
        klas_hemişelik = Salgylanma(7, token_hemişelik(klas_token), 0);
        부모상수 = Salgylanma(7, Söz_hemişelik("java/lang/Object"), 0); 코드상수 = Söz_hemişelik("Code"); 요구('{');
        while (!Hata && 종류() != '}') {
            if (함수수 == 32) { näsazlyk_baha("too many methods"); break; }
            int ygtyýarlylyk_girizmeklik = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int FUNCTION_baha = 함수수++;
            usul_ygtyýarlylyk[FUNCTION_baha] = ygtyýarlylyk_girizmeklik | 8;
            함수반환[FUNCTION_baha] = format_baha(); usul_girizmeklik_at[FUNCTION_baha] = tanaýjy_baha(); 요구('(');
            for (int 앞 = 0; 앞 < FUNCTION_baha; 앞++) if (이름같음(usul_girizmeklik_at[앞], usul_girizmeklik_at[FUNCTION_baha])) näsazlyk_baha("duplicate method (overloading unsupported)");
            while (!Hata && 종류() != ')') {
                int 수 = 함수인수수[FUNCTION_baha];
                if (수 == 16) { näsazlyk_baha("too many parameters"); break; }
                int ýaz_baha = format_baha(); if (ýaz_baha == 0) näsazlyk_baha("void parameter");
                usul_argument_ýaz[FUNCTION_baha * 16 + 수] = ýaz_baha; usul_argument_at[FUNCTION_baha * 16 + 수] = tanaýjy_baha();
                함수인수수[FUNCTION_baha]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!Hata && 받기(','));
            }
            함수본문[FUNCTION_baha] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) näsazlyk_baha("unclosed method body");
            usul_tamamla[FUNCTION_baha] = 위치;
            usul_at_hemişelik[FUNCTION_baha] = token_hemişelik(usul_girizmeklik_at[FUNCTION_baha]);
            nyşan_dowamlylyk = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[FUNCTION_baha]; 수++) goş_format(usul_argument_ýaz[FUNCTION_baha * 16 + 수]);
            글추가(')'); goş_format(함수반환[FUNCTION_baha]); 함수서술[FUNCTION_baha] = nyşan_hemişelik();
        }
        요구('}'); if (위치 != 토큰수) näsazlyk_baha("extra input after class");
    }
    static int tap_ýerli(int Ad) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(ýerli_at[수], Ad)) return 수;
        näsazlyk_baha("unknown variable"); return 0;
    }
    static int goş_ýerli(int Ad, int ýaz_baha) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(ýerli_at[수], Ad)) näsazlyk_baha("duplicate local variable");
        if (지역수 == 128) { näsazlyk_baha("too many locals"); return 0; }
        ýerli_at[지역수] = Ad; ýerli_ýaz[지역수] = ýaz_baha; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean bitin_ýaz(int ýaz_baha) { return ýaz_baha == 1 || ýaz_baha == 5; }
    static void 지역읽기(int 수) { 내보내기(ýerli_ýaz[수] <= 2 || ýerli_ýaz[수] == 5 ? 21 : 25); 내보내기(수); }
    static void ýaz_ýerli(int 수) { 내보내기(ýerli_ýaz[수] <= 2 || ýerli_ýaz[수] == 5 ? 54 : 58); 내보내기(수); }
    static void barla_ýaz(int hakyky_maglumat, int 기대) { if (hakyky_maglumat != 기대 && !(hakyky_maglumat == 5 && 기대 == 1)) näsazlyk_baha("type mismatch"); }
    static void 문자읽기(int token_baha) {
        nyşan_dowamlylyk = 0; int Bitir = 토큰위치[token_baha] + 1, 끝 = 토큰위치[token_baha] + token_dowamlylyk[token_baha] - 1;
        while (Bitir < 끝 && !Hata) {
            int baha = Çeşme[Bitir++];
            if (baha == '\\') {
                if (Bitir == 끝) { näsazlyk_baha("invalid escape"); break; }
                baha = Çeşme[Bitir++];
                if (baha == 'n') baha = 10;
                else if (baha == 'r') baha = 13;
                else if (baha == 't') baha = 9;
                else if (baha == 'b') baha = 8;
                else if (baha == 'f') baha = 12;
                else if (baha != '\\' && baha != '"' && baha != '\'') näsazlyk_baha("unsupported escape");
            }
            글추가(baha);
        }
    }
    static int seljer_bitin(int token_baha, boolean 음수) {
        if (token_dowamlylyk[token_baha] > 1 && Çeşme[토큰위치[token_baha]] == '0') näsazlyk_baha("octal literals unsupported");
        int baha = 0;
        for (int 수 = 0; 수 < token_dowamlylyk[token_baha]; 수++) {
            int san_element = Çeşme[토큰위치[token_baha] + 수] - '0';
            if (baha < -214748364 || baha == -214748364 && san_element > (음수 ? 8 : 7)) näsazlyk_baha("integer literal out of range");
            baha = baha * 10 - san_element;
        }
        return 음수 ? baha : -baha;
    }
    static int 기본식() {
        if (말받기("new")) {
            int ýaz_baha = format_baha();
            if (ýaz_baha != 6 && ýaz_baha != 7) { näsazlyk_baha("only file streams supported by new in source"); return 0; }
            String eýe_baha = ýaz_baha == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            buýruk(187, Salgylanma(7, Söz_hemişelik(eýe_baha), 0)); 내보내기(89);
            요구('('); barla_ýaz(aňlatma_baha(), 3); boolean 이어 = false;
            if (받기(',')) { if (ýaz_baha != 7) näsazlyk_baha("input stream constructor arguments"); barla_ýaz(aňlatma_baha(), 2); 이어 = true; }
            요구(')');
            buýruk(183, 외부참조(10, eýe_baha, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return ýaz_baha;
        }
        if (받기('(')) { int ýaz_baha = aňlatma_baha(); 요구(')'); return ýaz_baha; }
        if (종류() == 257) { 수상수(seljer_bitin(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); buýruk(19, Salgylanma(8, nyşan_hemişelik(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (nyşan_dowamlylyk != 1) näsazlyk_baha("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String eýe_baha = "", usul_baha = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                eýe_baha = "한국어/자체/출력"; 요구('.');
                if (말받기("ýaz_setir")) { usul_baha = "ýaz_setir"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("Ýaz")) { usul_baha = "Ýaz"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { usul_baha = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else näsazlyk_baha("unknown Korean output method");
            } else if (말받기("문자")) {
                eýe_baha = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("dowamlylyk_baha")) { usul_baha = "dowamlylyk_baha"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { usul_baha = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("seljer_bitin")) { usul_baha = "seljer_bitin"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("ýaz_bitin_baha")) { usul_baha = "ýaz_bitin_baha"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { usul_baha = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("ýelme_SMS")) { usul_baha = "ýelme_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("kes_baha")) { usul_baha = "kes_baha"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else näsazlyk_baha("unknown Korean text method");
            } else if (말받기("Faýl")) {
                eýe_baha = "한국어/자체/Faýl"; 요구('.'); 가 = 3;
                if (말받기("Oka")) { usul_baha = "Oka"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("Ýaz")) { usul_baha = "Ýaz"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else näsazlyk_baha("unknown Korean file method");
            } else if (말받기("화면")) {
                eýe_baha = "한국어/자체/화면"; 요구('.');
                if (말받기("너비")) { usul_baha = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { usul_baha = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { usul_baha = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { usul_baha = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { usul_baha = "기다리기"; 서술 = "()V"; }
                else näsazlyk_baha("unknown Korean framebuffer method");
            } else näsazlyk_baha("unsupported Korean library class");
            요구('('); if (가 != 0) barla_ýaz(aňlatma_baha(), 가);
            if (나 != 0) { 요구(','); barla_ýaz(aňlatma_baha(), 나); }
            if (다 != 0) { 요구(','); barla_ýaz(aňlatma_baha(), 다); }
            if (라 != 0) { 요구(','); barla_ýaz(aňlatma_baha(), 라); }
            if (마 != 0) { 요구(','); barla_ýaz(aňlatma_baha(), 마); }
            요구(')'); buýruk(184, 외부참조(10, eýe_baha, usul_baha, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); barla_ýaz(aňlatma_baha(), 3); 요구(')');
            buýruk(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Ad = tanaýjy_baha();
        if (받기('(')) {
            int FUNCTION_baha = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Ad, usul_girizmeklik_at[수])) FUNCTION_baha = 수;
            if (FUNCTION_baha < 0) { näsazlyk_baha("unknown static method"); return 0; }
            int 수 = 0;
            while (!Hata && 종류() != ')') {
                if (수 >= 함수인수수[FUNCTION_baha]) { näsazlyk_baha("too many arguments"); break; }
                barla_ýaz(aňlatma_baha(), usul_argument_ýaz[FUNCTION_baha * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[FUNCTION_baha]) näsazlyk_baha("argument count mismatch");
            buýruk(184, Salgylanma(10, klas_hemişelik, Salgylanma(12, usul_at_hemişelik[FUNCTION_baha], 함수서술[FUNCTION_baha])));
            return 함수반환[FUNCTION_baha];
        }
        int ýerli_elýeterli_gor = tap_ýerli(Ad), ýaz_baha = ýerli_ýaz[ýerli_elýeterli_gor]; 지역읽기(ýerli_elýeterli_gor);
        while (!Hata) {
            if (받기('[')) { barla_ýaz(ýaz_baha, 4); barla_ýaz(aňlatma_baha(), 1); 요구(']'); 내보내기(50); ýaz_baha = 3; }
            else if (받기('.')) {
                if (ýaz_baha == 6 || ýaz_baha == 7) {
                    String eýe_baha = ýaz_baha == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); buýruk(182, 외부참조(10, eýe_baha, "close", "()V")); ýaz_baha = 0; }
                    else if (ýaz_baha == 6 && 말받기("read")) { 요구('('); 요구(')'); buýruk(182, 외부참조(10, eýe_baha, "read", "()I")); ýaz_baha = 1; }
                    else if (ýaz_baha == 7 && 말받기("write")) { 요구('('); barla_ýaz(aňlatma_baha(), 1); 요구(')'); buýruk(182, 외부참조(10, eýe_baha, "write", "(I)V")); ýaz_baha = 0; }
                    else { näsazlyk_baha("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (ýaz_baha == 4) { 내보내기(190); ýaz_baha = 1; }
                else { barla_ýaz(ýaz_baha, 3); 요구('('); 요구(')'); buýruk(182, 외부참조(10, "java/lang/String", "length", "()I")); ýaz_baha = 1; }
            } else break;
        }
        return ýaz_baha;
    }
    static int 단항() {
        if (++식깊이 > 64) { näsazlyk_baha("expression nesting too deep"); 식깊이--; return 0; }
        int ýaz_baha;
        if (받기('!')) { barla_ýaz(단항(), 2); 비교값(153); ýaz_baha = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(seljer_bitin(위치++, true));
            else { barla_ýaz(단항(), 1); 내보내기(116); }
            ýaz_baha = 1;
        } else if (받기('+')) { barla_ýaz(단항(), 1); ýaz_baha = 1; }
        else ýaz_baha = 기본식();
        식깊이--; return ýaz_baha;
    }
    static int 곱식() {
        int ýaz_baha = 단항();
        while (!Hata && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int kodlaşdyrma_baha = 종류(); 위치++; barla_ýaz(ýaz_baha, 1); barla_ýaz(단항(), 1);
            내보내기(kodlaşdyrma_baha == '*' ? 104 : kodlaşdyrma_baha == '/' ? 108 : 112); ýaz_baha = 1;
        }
        return ýaz_baha;
    }
    static int 합식() {
        int ýaz_baha = 곱식();
        while (!Hata && (종류() == '+' || 종류() == '-')) {
            int kodlaşdyrma_baha = 종류(); 위치++; int 경계 = 코드크기, Yza_baha_ýaz = 곱식();
            if (kodlaşdyrma_baha == '+' && (ýaz_baha == 3 || Yza_baha_ýaz == 3)) { 결합(경계, ýaz_baha, Yza_baha_ýaz); ýaz_baha = 3; }
            else { barla_ýaz(ýaz_baha, 1); barla_ýaz(Yza_baha_ýaz, 1); 내보내기(kodlaşdyrma_baha == '+' ? 96 : 100); ýaz_baha = 1; }
        }
        return ýaz_baha;
    }
    static int 붙임참조(int ýaz_baha) {
        if (ýaz_baha != 1 && ýaz_baha != 2 && ýaz_baha != 3 && ýaz_baha != 5) näsazlyk_baha("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", ýaz_baha == 1 ? "(I)Ljava/lang/StringBuilder;"
            : ýaz_baha == 2 ? "(Z)Ljava/lang/StringBuilder;" : ýaz_baha == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Yza_baha_ýaz) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 aňlatma_baha 내부의 deň_derejeli_düwün_baha şahalanma 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        buýruk(187, Salgylanma(7, Söz_hemişelik("java/lang/StringBuilder"), 0)); 내보내기(89);
        buýruk(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); buýruk(182, 붙임참조(앞형));
        if (Hata) return;
        int dowamlylyk_baha = 코드크기 - 끝;
        for (int 수 = 0; 수 < dowamlylyk_baha; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + dowamlylyk_baha] = 코드[수];
        for (int 수 = 0; 수 < dowamlylyk_baha; 수++) 코드[경계 + 수] = 삽입코드[수];
        buýruk(182, 붙임참조(Yza_baha_ýaz)); buýruk(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int ýaz_baha = 합식();
        while (!Hata && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int kodlaşdyrma_baha = 종류(); 위치++; barla_ýaz(ýaz_baha, 1); barla_ýaz(합식(), 1);
            비교값(kodlaşdyrma_baha == '<' ? 161 : kodlaşdyrma_baha == '>' ? 163 : kodlaşdyrma_baha == 302 ? 164 : 162); ýaz_baha = 2;
        }
        return ýaz_baha;
    }
    static int 동등식() {
        int ýaz_baha = 비교식();
        while (!Hata && (종류() == 300 || 종류() == 301)) {
            int kodlaşdyrma_baha = 종류(); 위치++; int Yza_baha_ýaz = 비교식();
            if (ýaz_baha == 0 || Yza_baha_ýaz == 0) näsazlyk_baha("void expression");
            if (!(bitin_ýaz(ýaz_baha) && bitin_ýaz(Yza_baha_ýaz))) barla_ýaz(Yza_baha_ýaz, ýaz_baha);
            비교값((ýaz_baha <= 2 || ýaz_baha == 5 ? 159 : 165) + (kodlaşdyrma_baha == 301 ? 1 : 0)); ýaz_baha = 2;
        }
        return ýaz_baha;
    }
    static int 논리곱() {
        int ýaz_baha = 동등식();
        while (!Hata && 받기(304)) {
            barla_ýaz(ýaz_baha, 2); int 가 = şahalanma(153); barla_ýaz(동등식(), 2); int 나 = şahalanma(153);
            내보내기(4); int 끝 = şahalanma(167); Bag_baha(가, 코드크기); Bag_baha(나, 코드크기); 내보내기(3); Bag_baha(끝, 코드크기); ýaz_baha = 2;
        }
        return ýaz_baha;
    }
    static int aňlatma_baha() {
        int ýaz_baha = 논리곱();
        while (!Hata && 받기(305)) {
            barla_ýaz(ýaz_baha, 2); int 가 = şahalanma(154); barla_ýaz(논리곱(), 2); int 나 = şahalanma(154);
            내보내기(3); int 끝 = şahalanma(167); Bag_baha(가, 코드크기); Bag_baha(나, 코드크기); 내보내기(4); Bag_baha(끝, 코드크기); ýaz_baha = 2;
        }
        return ýaz_baha;
    }
    static void ýumuş_baha(boolean 선언허용) {
        if (Söz_baha(위치, "int") || Söz_baha(위치, "boolean") || Söz_baha(위치, "String") || Söz_baha(위치, "char")
            || Söz_baha(위치, "FileInputStream") || Söz_baha(위치, "FileOutputStream")) {
            if (!선언허용) näsazlyk_baha("declaration not allowed here");
            int ýaz_baha = format_baha(), Ad = tanaýjy_baha(); 요구('='); barla_ýaz(aňlatma_baha(), ýaz_baha);
            ýaz_ýerli(goş_ýerli(Ad, ýaz_baha)); return;
        }
        int Ad = tanaýjy_baha(), ýerli_elýeterli_gor = tap_ýerli(Ad);
        if (받기('=')) { barla_ýaz(aňlatma_baha(), ýerli_ýaz[ýerli_elýeterli_gor]); ýaz_ýerli(ýerli_elýeterli_gor); }
        else if (종류() >= 308 && 종류() <= 312) {
            int kodlaşdyrma_baha = 종류(); 위치++; 지역읽기(ýerli_elýeterli_gor); int 경계 = 코드크기, Yza_baha_ýaz = aňlatma_baha();
            if (kodlaşdyrma_baha == 308 && ýerli_ýaz[ýerli_elýeterli_gor] == 3) 결합(경계, 3, Yza_baha_ýaz);
            else {
                barla_ýaz(ýerli_ýaz[ýerli_elýeterli_gor], 1); barla_ýaz(Yza_baha_ýaz, 1);
                내보내기(kodlaşdyrma_baha == 308 ? 96 : kodlaşdyrma_baha == 309 ? 100 : kodlaşdyrma_baha == 310 ? 104 : kodlaşdyrma_baha == 311 ? 108 : 112);
                if (ýerli_ýaz[ýerli_elýeterli_gor] == 5) 내보내기(146);
            }
            ýaz_ýerli(ýerli_elýeterli_gor);
        }
        else if (종류() == 306 || 종류() == 307) {
            barla_ýaz(ýerli_ýaz[ýerli_elýeterli_gor], 1); 내보내기(132); 내보내기(ýerli_elýeterli_gor); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (ýerli_ýaz[ýerli_elýeterli_gor] == 5) { 지역읽기(ýerli_elýeterli_gor); 내보내기(146); ýaz_ýerli(ýerli_elýeterli_gor); }
        } else näsazlyk_baha("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        buýruk(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean boş_argument = 종류() == ')';
        int ýaz_baha = boş_argument ? 0 : aňlatma_baha(); 요구(')'); 요구(';');
        String 서술 = ýaz_baha == 0 ? "()V" : ýaz_baha == 1 ? "(I)V" : ýaz_baha == 2 ? "(Z)V" : ýaz_baha == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (ýaz_baha == 4 || ýaz_baha >= 6 || ýaz_baha == 0 && (!줄바꿈 || !boş_argument)) näsazlyk_baha("unsupported print argument");
        buýruk(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean beýannama_baha() {
        if (Hata) return false;
        if (깊이 > 32) { näsazlyk_baha("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!Hata && 종류() != '}') { if (반환) näsazlyk_baha("unreachable statement"); 반환 = beýannama_baha(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int ýaz_baha = 종류() == ';' ? 0 : aňlatma_baha(); barla_ýaz(ýaz_baha, 함수반환[현재함수]); 요구(';');
            내보내기(ýaz_baha == 0 ? 177 : ýaz_baha <= 2 || ýaz_baha == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); barla_ýaz(aňlatma_baha(), 2); 요구(')'); int 거짓 = şahalanma(153);
            깊이++; boolean 가 = dolandyryş_beýannama(); 깊이--;
            if (말받기("else")) { int 끝 = şahalanma(167); Bag_baha(거짓, 코드크기); 깊이++; boolean 나 = dolandyryş_beýannama(); 깊이--; Bag_baha(끝, 코드크기); return 가 && 나; }
            Bag_baha(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int Bitir = 코드크기; 요구('('); barla_ýaz(aňlatma_baha(), 2); 요구(')'); int 끝 = şahalanma(153);
            깊이++; dolandyryş_beýannama(); 깊이--; Bag_baha(şahalanma(167), Bitir); Bag_baha(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') ýumuş_baha(true); 요구(';');
            int şert = 코드크기; if (종류() == ';') 내보내기(4); else barla_ýaz(aňlatma_baha(), 2); 요구(';');
            int 끝 = şahalanma(153), göwre_teksti = şahalanma(167), täzelendir = 코드크기;
            if (종류() != ')') ýumuş_baha(false); 요구(')'); Bag_baha(şahalanma(167), şert); Bag_baha(göwre_teksti, 코드크기);
            dolandyryş_beýannama(); Bag_baha(şahalanma(167), täzelendir); Bag_baha(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Söz_baha(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int ýaz_baha = aňlatma_baha(); if (ýaz_baha != 0) 내보내기(87); 요구(';'); return false;
        }
        ýumuş_baha(true); 요구(';'); return false;
    }
    static boolean dolandyryş_beýannama() {
        if (Söz_baha(위치, "int") || Söz_baha(위치, "boolean") || Söz_baha(위치, "char") || Söz_baha(위치, "String")
            || Söz_baha(위치, "FileInputStream") || Söz_baha(위치, "FileOutputStream")) näsazlyk_baha("local declaration requires braces");
        return beýannama_baha();
    }
    static void 출바(int baha) { if (출력크기 == 출력.length) näsazlyk_baha("class file too large"); else 출력[출력크기++] = baha & 255; }
    static void 출짧(int baha) { 출바(baha >> 8); 출바(baha); }
    static void 출정(int baha) { 출짧(baha >>> 16); 출짧(baha); }
    static void ýaz_klas() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < hemişelik_ölçegi_üýtget; 수++) 출바(hemişelik_baha[수]);
        출짧(0x21); 출짧(klas_hemişelik); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(usul_ygtyýarlylyk[수]); 출짧(usul_at_hemişelik[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + usul_dowamlylyk[수]); 출짧(128); 출짧(함수지역[수]); 출정(usul_dowamlylyk[수]);
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < usul_dowamlylyk[수]; ýer_girizmeklik++) 출바(코드[함수코드[수] + ýer_girizmeklik]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Bitir() {
        if (ulanyjy.인수개수() == 1 && 자바도구.같음(ulanyjy.인수(0), "-version")) {
            ulanyjy.Ýaz("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (ulanyjy.인수개수() != 1) { ulanyjy.Ýaz("Usage: javac FILE.java\n"); return 2; }
        int at_ölçegi_üýtget = 자바도구.Ad(faýl_at_SMS, ulanyjy.인수(0));
        if (at_ölçegi_üýtget < 6 || at_ölçegi_üýtget > 62 || faýl_at_SMS[at_ölçegi_üýtget - 5] != '.' || faýl_at_SMS[at_ölçegi_üýtget - 4] != 'j'
            || faýl_at_SMS[at_ölçegi_üýtget - 3] != 'a' || faýl_at_SMS[at_ölçegi_üýtget - 2] != 'v' || faýl_at_SMS[at_ölçegi_üýtget - 1] != 'a') {
            ulanyjy.Ýaz("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        gor_ölçegi_üýtget = ulanyjy.파일읽기(faýl_at_SMS, Çeşme);
        if (gor_ölçegi_üýtget < 0) { ulanyjy.Ýaz("javac: cannot read source: "); 자바도구.수쓰기(gor_ölçegi_üýtget); ulanyjy.ýaz_nyşan_baha(10); return 1; }
        gor_ölçegi_üýtget = 자바도구.원문해독(Çeşme, gor_ölçegi_üýtget);
        if (gor_ölçegi_üýtget < 0) { ulanyjy.Ýaz("javac error: invalid UTF-8 source\n"); return 1; }
        kes_baha(); if (!Hata) 선언읽기();
        if (!Hata) {
            if (token_dowamlylyk[klas_token] != at_ölçegi_üýtget - 5) näsazlyk_baha("class name must match file name");
            for (int 수 = 0; 수 < at_ölçegi_üýtget - 5; 수++) if (Çeşme[토큰위치[klas_token] + 수] != faýl_at_SMS[수]) näsazlyk_baha("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !Hata; 현재함수++) {
            위치 = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) goş_ýerli(usul_argument_at[현재함수 * 16 + 수], usul_argument_ýaz[현재함수 * 16 + 수]);
            boolean 반환 = beýannama_baha();
            if (!반환 && 함수반환[현재함수] != 0) näsazlyk_baha("missing return");
            // şahalanma 뒤의 합류 지점은 반드시 hakyky_maglumat 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean bitin = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(bitin ? 3 : 1); 내보내기(bitin ? 172 : 176); }
            if (위치 != usul_tamamla[현재함수]) näsazlyk_baha("invalid method body");
            함수지역[현재함수] = 지역수; usul_dowamlylyk[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (Hata) return 1;
        ýaz_klas(); if (Hata) return 1;
        faýl_at_SMS[at_ölçegi_üýtget - 4] = 'c'; faýl_at_SMS[at_ölçegi_üýtget - 3] = 'l'; faýl_at_SMS[at_ölçegi_üýtget - 2] = 'a';
        faýl_at_SMS[at_ölçegi_üýtget - 1] = 's'; faýl_at_SMS[at_ölçegi_üýtget] = 's'; faýl_at_SMS[at_ölçegi_üýtget + 1] = 0;
        int 결과 = ulanyjy.ýaz_faýl(faýl_at_SMS, 출력, 출력크기);
        if (결과 < 0) { ulanyjy.Ýaz("javac: cannot save class: "); 자바도구.수쓰기(결과); ulanyjy.ýaz_nyşan_baha(10); return 1; }
        ulanyjy.Ýaz("Compiled: "); for (int 수 = 0; faýl_at_SMS[수] != 0; 수++) ulanyjy.ýaz_nyşan_baha(faýl_at_SMS[수]);
        ulanyjy.Ýaz(" (JVM class version 49)\n"); return 0;
    }
}
