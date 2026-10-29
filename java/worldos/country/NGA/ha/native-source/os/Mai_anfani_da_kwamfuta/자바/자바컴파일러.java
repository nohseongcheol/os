// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java tushe_Li_irabin_tarin_bayanai -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] tushe = new int[16384], 출력 = new int[16384], lambar_sirri_Daraja = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], token_Tsawo = new int[2048];
    static int[] Jurarre_Daraja = new int[4096], Jurarre_Sassautawa = new int[512];
    static int[] 문자 = new int[512], Fayil_Suna_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int tushe_girma, 토큰수, 위치, lambar_sirri_girma, Jurarre_girma, 상수수 = 1, 출력크기, Harafi_Tsawo;
    static boolean Kuskure;
    static int Aji_token, Aji_Jurarre, 부모상수, lambar_sirri_Jurarre;
    static int[] tsari_Mashigar_bayanai_Suna = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] tsari_Tubalin_aiki_Suna = new int[512], tsari_Tubalin_aiki_rubuta = new int[512];
    static int[] tsari_jiki = new int[32], tsari_Ƙarshe = new int[32], tsari_lambar_sirri = new int[32];
    static int[] tsari_Tsawo = new int[32], 함수지역 = new int[32], tsari_Suna_Jurarre = new int[32], 함수서술 = new int[32];
    static int[] tsari_isa = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] na_gida_Suna = new int[128], na_gida_rubuta = new int[128], 지역깊이 = new int[128];

    static void Kasa_aiki_Daraja(String 이유) {
        if (!Kuskure) {
            Mai_anfani_da_kwamfuta.Yi_Rubutu("javac error: "); Mai_anfani_da_kwamfuta.Yi_Rubutu(이유);
            Mai_anfani_da_kwamfuta.Yi_Rubutu(" at line ");
            int Layi = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : tushe_girma;
            for (int 수 = 0; 수 < 끝; 수++) if (tushe[수] == 10) Layi++;
            자바도구.수쓰기(Layi); Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja(10);
        }
        Kuskure = true;
    }
    static boolean Harafi_Daraja(int Daraja) { return 문자이름규칙.첫글자(Daraja); }
    static boolean lamba_Daraja(int Daraja) { return Daraja >= '0' && Daraja <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || token_Tsawo[가] != token_Tsawo[나]) return false;
        for (int 수 = 0; 수 < token_Tsawo[가]; 수++) if (tushe[토큰위치[가] + 수] != tushe[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean Microsoft_Word_Daraja(int token_Daraja, String Microsoft_Word_SMS) {
        if (token_Daraja < 0 || token_Daraja >= 토큰수 || token_Tsawo[token_Daraja] != Microsoft_Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Microsoft_Word_SMS.length(); 수++) if (tushe[토큰위치[token_Daraja] + 수] != Microsoft_Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int Daraja) { if (종류() != Daraja) return false; 위치++; return true; }
    static void 요구(int Daraja) { if (!받기(Daraja)) Kasa_aiki_Daraja("unexpected token"); }
    static boolean 말받기(String Microsoft_Word_SMS) { if (!Microsoft_Word_Daraja(위치, Microsoft_Word_SMS)) return false; 위치++; return true; }
    static void 말요구(String Microsoft_Word_SMS) { if (!말받기(Microsoft_Word_SMS)) Kasa_aiki_Daraja(Microsoft_Word_SMS); }
    static int mai_ganewa_Daraja() {
        int 결과 = 위치;
        if (종류() != 256) Kasa_aiki_Daraja("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Tafiyar_da = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Tafiyar_da == token_Tsawo[결과];
                for (int rami_Mashigar_bayanai = Tafiyar_da; 같음 && rami_Mashigar_bayanai < 수; rami_Mashigar_bayanai++) if (예약어.charAt(rami_Mashigar_bayanai) != tushe[토큰위치[결과] + rami_Mashigar_bayanai - Tafiyar_da]) 같음 = false;
                if (같음) Kasa_aiki_Daraja("reserved word cannot be an identifier");
                Tafiyar_da = 수 + 1;
            }
        }
        return 결과;
    }
    static void Yanka_Daraja() {
        int 수 = 0;
        while (수 < tushe_girma && !Kuskure) {
            int Daraja = tushe[수], Tafiyar_da = 수, 종류 = Daraja;
            if (Daraja == 32 || Daraja == 9 || Daraja == 10 || Daraja == 13) { 수++; continue; }
            if (Daraja == '/' && 수 + 1 < tushe_girma && tushe[수 + 1] == '/') {
                while (수 < tushe_girma && tushe[수] != 10) 수++;
                continue;
            }
            if (Daraja == '/' && 수 + 1 < tushe_girma && tushe[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < tushe_girma && !(tushe[수] == '*' && tushe[수 + 1] == '/')) 수++;
                if (수 + 1 >= tushe_girma) { Kasa_aiki_Daraja("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (Harafi_Daraja(Daraja)) { 종류 = 256; while (수 < tushe_girma && 문자이름규칙.이어진글자(tushe[수])) 수++; }
            else if (lamba_Daraja(Daraja)) { 종류 = 257; while (수 < tushe_girma && lamba_Daraja(tushe[수])) 수++; }
            else if (Daraja == '"' || Daraja == '\'') {
                종류 = Daraja == '"' ? 258 : 259; 수++;
                while (수 < tushe_girma && tushe[수] != Daraja && tushe[수] != 10 && tushe[수] != 13) {
                    if (tushe[수] == '\\') 수++;
                    수++;
                }
                if (수 >= tushe_girma || tushe[수] != Daraja) { Kasa_aiki_Daraja("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < tushe_girma) {
                    int 다음 = tushe[수];
                    if (Daraja == '=' && 다음 == '=') 종류 = 300;
                    if (Daraja == '!' && 다음 == '=') 종류 = 301;
                    if (Daraja == '<' && 다음 == '=') 종류 = 302;
                    if (Daraja == '>' && 다음 == '=') 종류 = 303;
                    if (Daraja == '&' && 다음 == '&') 종류 = 304;
                    if (Daraja == '|' && 다음 == '|') 종류 = 305;
                    if (Daraja == '+' && 다음 == '+') 종류 = 306;
                    if (Daraja == '-' && 다음 == '-') 종류 = 307;
                    if (Daraja == '+' && 다음 == '=') 종류 = 308;
                    if (Daraja == '-' && 다음 == '=') 종류 = 309;
                    if (Daraja == '*' && 다음 == '=') 종류 = 310;
                    if (Daraja == '/' && 다음 == '=') 종류 = 311;
                    if (Daraja == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { Kasa_aiki_Daraja("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = Tafiyar_da; token_Tsawo[토큰수++] = 수 - Tafiyar_da;
        }
    }
    static void Rubuta_Jurarre_bayit(int Daraja) {
        if (Jurarre_girma == Jurarre_Daraja.length) { Kasa_aiki_Daraja("constant pool too large"); return; }
        Jurarre_Daraja[Jurarre_girma++] = Daraja & 255;
    }
    static void 상짧(int Daraja) { Rubuta_Jurarre_bayit(Daraja >> 8); Rubuta_Jurarre_bayit(Daraja); }
    static int 상등록(int Tafiyar_da) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int kyamarar_gaba_Daraja = Jurarre_Sassautawa[수], Tsawo_Daraja = (수 + 1 < 상수수 ? Jurarre_Sassautawa[수 + 1] : Tafiyar_da) - kyamarar_gaba_Daraja;
            if (Tsawo_Daraja != Jurarre_girma - Tafiyar_da) continue;
            boolean 같음 = true;
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < Tsawo_Daraja; rami_Mashigar_bayanai++) if (Jurarre_Daraja[kyamarar_gaba_Daraja + rami_Mashigar_bayanai] != Jurarre_Daraja[Tafiyar_da + rami_Mashigar_bayanai]) 같음 = false;
            if (같음) { Jurarre_girma = Tafiyar_da; return 수; }
        }
        if (상수수 == Jurarre_Sassautawa.length) { Kasa_aiki_Daraja("too many constants"); return 0; }
        Jurarre_Sassautawa[상수수] = Tafiyar_da;
        return 상수수++;
    }
    static void 글추가(int Daraja) {
        if (Harafi_Tsawo == 문자.length) { Kasa_aiki_Daraja("text too long"); return; }
        문자[Harafi_Tsawo++] = Daraja;
    }
    static void 말추가(String Microsoft_Word_SMS) { for (int 수 = 0; 수 < Microsoft_Word_SMS.length(); 수++) 글추가(Microsoft_Word_SMS.charAt(수)); }
    static int Harafi_Jurarre() {
        int Tafiyar_da = Jurarre_girma; Rubuta_Jurarre_bayit(1); 상짧(0);
        for (int 수 = 0; 수 < Harafi_Tsawo; 수++) {
            int Daraja = 문자[수];
            if (Daraja > 0 && Daraja < 128) Rubuta_Jurarre_bayit(Daraja);
            else if (Daraja < 2048) { Rubuta_Jurarre_bayit(192 | Daraja >> 6); Rubuta_Jurarre_bayit(128 | Daraja & 63); }
            else { Rubuta_Jurarre_bayit(224 | Daraja >> 12); Rubuta_Jurarre_bayit(128 | Daraja >> 6 & 63); Rubuta_Jurarre_bayit(128 | Daraja & 63); }
        }
        if (Kuskure) return 0;
        int Tsawo_Daraja = Jurarre_girma - Tafiyar_da - 3;
        Jurarre_Daraja[Tafiyar_da + 1] = Tsawo_Daraja >> 8; Jurarre_Daraja[Tafiyar_da + 2] = Tsawo_Daraja & 255;
        return 상등록(Tafiyar_da);
    }
    static int Microsoft_Word_Jurarre(String Microsoft_Word_SMS) { Harafi_Tsawo = 0; 말추가(Microsoft_Word_SMS); return Harafi_Jurarre(); }
    static int token_Jurarre(int token_Daraja) {
        Harafi_Tsawo = 0;
        for (int 수 = 0; 수 < token_Tsawo[token_Daraja]; 수++) 글추가(tushe[토큰위치[token_Daraja] + 수]);
        return Harafi_Jurarre();
    }
    static int Manazarta(int 종류, int 가, int 나) {
        int Tafiyar_da = Jurarre_girma; Rubuta_Jurarre_bayit(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return 상등록(Tafiyar_da);
    }
    static int 외부참조(int 종류, String mamallaki_Daraja, String Suna, String 서술) {
        int mamallaki_mai_ganewa = Manazarta(7, Microsoft_Word_Jurarre(mamallaki_Daraja), 0);
        int 이름수 = Microsoft_Word_Jurarre(Suna), 형식수 = Microsoft_Word_Jurarre(서술);
        return Manazarta(종류, mamallaki_mai_ganewa, Manazarta(12, 이름수, 형식수));
    }
    static void 내보내기(int Daraja) {
        if (lambar_sirri_girma == lambar_sirri_Daraja.length) { Kasa_aiki_Daraja("bytecode too large"); return; }
        lambar_sirri_Daraja[lambar_sirri_girma++] = Daraja & 255;
    }
    static void Umarni(int Daraja, int 인수) { 내보내기(Daraja); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int Daraja) {
        if (Daraja >= -1 && Daraja <= 5) { 내보내기(Daraja + 3); return; }
        int Tafiyar_da = Jurarre_girma; Rubuta_Jurarre_bayit(3); 상짧(Daraja >>> 16); 상짧(Daraja);
        Umarni(19, 상등록(Tafiyar_da));
    }
    static int Reshe(int Umarni) { int 결과 = lambar_sirri_girma; Umarni(Umarni, 0); return 결과; }
    static void Kafa_Daraja(int Reshe, int tageti_abu) {
        if (Kuskure) return;
        int 거리 = tageti_abu - Reshe;
        if (거리 < -32768 || 거리 > 32767 || Reshe < 0 || Reshe + 2 >= lambar_sirri_girma) { Kasa_aiki_Daraja("invalid branch"); return; }
        lambar_sirri_Daraja[Reshe + 1] = 거리 >> 8 & 255; lambar_sirri_Daraja[Reshe + 2] = 거리 & 255;
    }
    static void Kwatantawa_Daraja(int Umarni) {
        int 참 = Reshe(Umarni); 내보내기(3); int 끝 = Reshe(167);
        Kafa_Daraja(참, lambar_sirri_girma); 내보내기(4); Kafa_Daraja(끝, lambar_sirri_girma);
    }
    static int zubi_Daraja() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        Kasa_aiki_Daraja("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void ƙara_zubi(int rubuta_Daraja) {
        if (rubuta_Daraja == 0) 글추가('V');
        if (rubuta_Daraja == 1) 글추가('I');
        if (rubuta_Daraja == 2) 글추가('Z');
        if (rubuta_Daraja == 3) 말추가("Ljava/lang/String;");
        if (rubuta_Daraja == 4) 말추가("[Ljava/lang/String;");
        if (rubuta_Daraja == 5) 글추가('C');
        if (rubuta_Daraja == 6) 말추가("Ljava/io/FileInputStream;");
        if (rubuta_Daraja == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws bayyanarwa. banbanchi haryar_aikin_na_ura_Daraja_Mashigar_bayanai 본문은 sauka javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("banbanchi") || 말받기("실행예외") || 말받기("I_O_banbanchi") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("mara_ƙarfi_Tubalin_aiki_banbanchi") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("Sokakke_Manazarta_banbanchi") || 말받기("산술예외") || 말받기("Matsayi_banbanchi") || 말받기("rubuta_watsa_banbanchi") || 말받기("음수배열크기예외") || 말받기("TSARI_Ajiye_Kasa_aiki") || 말받기("hira_Matsayi_banbanchi") || 말받기("대기중단예외")) return;
        Kasa_aiki_Daraja("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (Microsoft_Word_Daraja(위치, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) Kasa_aiki_Daraja("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); Aji_token = mai_ganewa_Daraja();
        Aji_Jurarre = Manazarta(7, token_Jurarre(Aji_token), 0);
        부모상수 = Manazarta(7, Microsoft_Word_Jurarre("java/lang/Object"), 0); lambar_sirri_Jurarre = Microsoft_Word_Jurarre("Code"); 요구('{');
        while (!Kuskure && 종류() != '}') {
            if (함수수 == 32) { Kasa_aiki_Daraja("too many methods"); break; }
            int isa_Mashigar_bayanai = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int AIKI_Daraja = 함수수++;
            tsari_isa[AIKI_Daraja] = isa_Mashigar_bayanai | 8;
            함수반환[AIKI_Daraja] = zubi_Daraja(); tsari_Mashigar_bayanai_Suna[AIKI_Daraja] = mai_ganewa_Daraja(); 요구('(');
            for (int kyamarar_gaba_Daraja = 0; kyamarar_gaba_Daraja < AIKI_Daraja; kyamarar_gaba_Daraja++) if (이름같음(tsari_Mashigar_bayanai_Suna[kyamarar_gaba_Daraja], tsari_Mashigar_bayanai_Suna[AIKI_Daraja])) Kasa_aiki_Daraja("duplicate method (overloading unsupported)");
            while (!Kuskure && 종류() != ')') {
                int 수 = 함수인수수[AIKI_Daraja];
                if (수 == 16) { Kasa_aiki_Daraja("too many parameters"); break; }
                int rubuta_Daraja = zubi_Daraja(); if (rubuta_Daraja == 0) Kasa_aiki_Daraja("void parameter");
                tsari_Tubalin_aiki_rubuta[AIKI_Daraja * 16 + 수] = rubuta_Daraja; tsari_Tubalin_aiki_Suna[AIKI_Daraja * 16 + 수] = mai_ganewa_Daraja();
                함수인수수[AIKI_Daraja]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!Kuskure && 받기(','));
            }
            tsari_jiki[AIKI_Daraja] = 위치; 요구('{');
            int sarƙaƙewa_Daraja = 1;
            while (위치 < 토큰수 && sarƙaƙewa_Daraja > 0) {
                if (종류() == '{') sarƙaƙewa_Daraja++;
                if (종류() == '}') sarƙaƙewa_Daraja--;
                위치++;
            }
            if (sarƙaƙewa_Daraja != 0) Kasa_aiki_Daraja("unclosed method body");
            tsari_Ƙarshe[AIKI_Daraja] = 위치;
            tsari_Suna_Jurarre[AIKI_Daraja] = token_Jurarre(tsari_Mashigar_bayanai_Suna[AIKI_Daraja]);
            Harafi_Tsawo = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[AIKI_Daraja]; 수++) ƙara_zubi(tsari_Tubalin_aiki_rubuta[AIKI_Daraja * 16 + 수]);
            글추가(')'); ƙara_zubi(함수반환[AIKI_Daraja]); 함수서술[AIKI_Daraja] = Harafi_Jurarre();
        }
        요구('}'); if (위치 != 토큰수) Kasa_aiki_Daraja("extra input after class");
    }
    static int nema_na_gida(int Suna) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(na_gida_Suna[수], Suna)) return 수;
        Kasa_aiki_Daraja("unknown variable"); return 0;
    }
    static int ƙara_na_gida(int Suna, int rubuta_Daraja) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(na_gida_Suna[수], Suna)) Kasa_aiki_Daraja("duplicate local variable");
        if (지역수 == 128) { Kasa_aiki_Daraja("too many locals"); return 0; }
        na_gida_Suna[지역수] = Suna; na_gida_rubuta[지역수] = rubuta_Daraja; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean Lamba_mara_rubuta(int rubuta_Daraja) { return rubuta_Daraja == 1 || rubuta_Daraja == 5; }
    static void 지역읽기(int 수) { 내보내기(na_gida_rubuta[수] <= 2 || na_gida_rubuta[수] == 5 ? 21 : 25); 내보내기(수); }
    static void Rubuta_na_gida(int 수) { 내보내기(na_gida_rubuta[수] <= 2 || na_gida_rubuta[수] == 5 ? 54 : 58); 내보내기(수); }
    static void Tabbatar_da_rubuta(int Na_hakika_Tarin_bayani, int 기대) { if (Na_hakika_Tarin_bayani != 기대 && !(Na_hakika_Tarin_bayani == 5 && 기대 == 1)) Kasa_aiki_Daraja("type mismatch"); }
    static void 문자읽기(int token_Daraja) {
        Harafi_Tsawo = 0; int Tafiyar_da = 토큰위치[token_Daraja] + 1, 끝 = 토큰위치[token_Daraja] + token_Tsawo[token_Daraja] - 1;
        while (Tafiyar_da < 끝 && !Kuskure) {
            int Daraja = tushe[Tafiyar_da++];
            if (Daraja == '\\') {
                if (Tafiyar_da == 끝) { Kasa_aiki_Daraja("invalid escape"); break; }
                Daraja = tushe[Tafiyar_da++];
                if (Daraja == 'n') Daraja = 10;
                else if (Daraja == 'r') Daraja = 13;
                else if (Daraja == 't') Daraja = 9;
                else if (Daraja == 'b') Daraja = 8;
                else if (Daraja == 'f') Daraja = 12;
                else if (Daraja != '\\' && Daraja != '"' && Daraja != '\'') Kasa_aiki_Daraja("unsupported escape");
            }
            글추가(Daraja);
        }
    }
    static int Daddatse_Lamba_mara(int token_Daraja, boolean 음수) {
        if (token_Tsawo[token_Daraja] > 1 && tushe[토큰위치[token_Daraja]] == '0') Kasa_aiki_Daraja("octal literals unsupported");
        int Daraja = 0;
        for (int 수 = 0; 수 < token_Tsawo[token_Daraja]; 수++) {
            int lamba_abu = tushe[토큰위치[token_Daraja] + 수] - '0';
            if (Daraja < -214748364 || Daraja == -214748364 && lamba_abu > (음수 ? 8 : 7)) Kasa_aiki_Daraja("integer literal out of range");
            Daraja = Daraja * 10 - lamba_abu;
        }
        return 음수 ? Daraja : -Daraja;
    }
    static int 기본식() {
        if (말받기("new")) {
            int rubuta_Daraja = zubi_Daraja();
            if (rubuta_Daraja != 6 && rubuta_Daraja != 7) { Kasa_aiki_Daraja("only file streams supported by new in source"); return 0; }
            String mamallaki_Daraja = rubuta_Daraja == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Umarni(187, Manazarta(7, Microsoft_Word_Jurarre(mamallaki_Daraja), 0)); 내보내기(89);
            요구('('); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 3); boolean 이어 = false;
            if (받기(',')) { if (rubuta_Daraja != 7) Kasa_aiki_Daraja("input stream constructor arguments"); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 2); 이어 = true; }
            요구(')');
            Umarni(183, 외부참조(10, mamallaki_Daraja, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return rubuta_Daraja;
        }
        if (받기('(')) { int rubuta_Daraja = Aiyana_alƙaluma_Daraja(); 요구(')'); return rubuta_Daraja; }
        if (종류() == 257) { 수상수(Daddatse_Lamba_mara(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); Umarni(19, Manazarta(8, Harafi_Jurarre(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (Harafi_Tsawo != 1) Kasa_aiki_Daraja("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String mamallaki_Daraja = "", tsari_Daraja = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                mamallaki_Daraja = "한국어/자체/출력"; 요구('.');
                if (말받기("Rubuta_Layi")) { tsari_Daraja = "Rubuta_Layi"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("Yi_Rubutu")) { tsari_Daraja = "Yi_Rubutu"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { tsari_Daraja = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else Kasa_aiki_Daraja("unknown Korean output method");
            } else if (말받기("문자")) {
                mamallaki_Daraja = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("Tsawo_Daraja")) { tsari_Daraja = "Tsawo_Daraja"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { tsari_Daraja = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("Daddatse_Lamba_mara")) { tsari_Daraja = "Daddatse_Lamba_mara"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("Rubuta_Lamba_mara_Daraja")) { tsari_Daraja = "Rubuta_Lamba_mara_Daraja"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { tsari_Daraja = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("manna_SMS")) { tsari_Daraja = "manna_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("Yanka_Daraja")) { tsari_Daraja = "Yanka_Daraja"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else Kasa_aiki_Daraja("unknown Korean text method");
            } else if (말받기("Fayil")) {
                mamallaki_Daraja = "한국어/자체/Fayil"; 요구('.'); 가 = 3;
                if (말받기("Yi_Karatu")) { tsari_Daraja = "Yi_Karatu"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("Yi_Rubutu")) { tsari_Daraja = "Yi_Rubutu"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else Kasa_aiki_Daraja("unknown Korean file method");
            } else if (말받기("화면")) {
                mamallaki_Daraja = "한국어/자체/화면"; 요구('.');
                if (말받기("너비")) { tsari_Daraja = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { tsari_Daraja = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { tsari_Daraja = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("share_Mashigar_bayanai")) { tsari_Daraja = "share_Mashigar_bayanai"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { tsari_Daraja = "기다리기"; 서술 = "()V"; }
                else Kasa_aiki_Daraja("unknown Korean framebuffer method");
            } else Kasa_aiki_Daraja("unsupported Korean library class");
            요구('('); if (가 != 0) Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 가);
            if (나 != 0) { 요구(','); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 나); }
            if (다 != 0) { 요구(','); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 다); }
            if (라 != 0) { 요구(','); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 라); }
            if (마 != 0) { 요구(','); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 마); }
            요구(')'); Umarni(184, 외부참조(10, mamallaki_Daraja, tsari_Daraja, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 3); 요구(')');
            Umarni(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Suna = mai_ganewa_Daraja();
        if (받기('(')) {
            int AIKI_Daraja = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Suna, tsari_Mashigar_bayanai_Suna[수])) AIKI_Daraja = 수;
            if (AIKI_Daraja < 0) { Kasa_aiki_Daraja("unknown static method"); return 0; }
            int 수 = 0;
            while (!Kuskure && 종류() != ')') {
                if (수 >= 함수인수수[AIKI_Daraja]) { Kasa_aiki_Daraja("too many arguments"); break; }
                Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), tsari_Tubalin_aiki_rubuta[AIKI_Daraja * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[AIKI_Daraja]) Kasa_aiki_Daraja("argument count mismatch");
            Umarni(184, Manazarta(10, Aji_Jurarre, Manazarta(12, tsari_Suna_Jurarre[AIKI_Daraja], 함수서술[AIKI_Daraja])));
            return 함수반환[AIKI_Daraja];
        }
        int na_gida_Kima = nema_na_gida(Suna), rubuta_Daraja = na_gida_rubuta[na_gida_Kima]; 지역읽기(na_gida_Kima);
        while (!Kuskure) {
            if (받기('[')) { Tabbatar_da_rubuta(rubuta_Daraja, 4); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 1); 요구(']'); 내보내기(50); rubuta_Daraja = 3; }
            else if (받기('.')) {
                if (rubuta_Daraja == 6 || rubuta_Daraja == 7) {
                    String mamallaki_Daraja = rubuta_Daraja == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); Umarni(182, 외부참조(10, mamallaki_Daraja, "close", "()V")); rubuta_Daraja = 0; }
                    else if (rubuta_Daraja == 6 && 말받기("read")) { 요구('('); 요구(')'); Umarni(182, 외부참조(10, mamallaki_Daraja, "read", "()I")); rubuta_Daraja = 1; }
                    else if (rubuta_Daraja == 7 && 말받기("write")) { 요구('('); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 1); 요구(')'); Umarni(182, 외부참조(10, mamallaki_Daraja, "write", "(I)V")); rubuta_Daraja = 0; }
                    else { Kasa_aiki_Daraja("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (rubuta_Daraja == 4) { 내보내기(190); rubuta_Daraja = 1; }
                else { Tabbatar_da_rubuta(rubuta_Daraja, 3); 요구('('); 요구(')'); Umarni(182, 외부참조(10, "java/lang/String", "length", "()I")); rubuta_Daraja = 1; }
            } else break;
        }
        return rubuta_Daraja;
    }
    static int 단항() {
        if (++식깊이 > 64) { Kasa_aiki_Daraja("expression nesting too deep"); 식깊이--; return 0; }
        int rubuta_Daraja;
        if (받기('!')) { Tabbatar_da_rubuta(단항(), 2); Kwatantawa_Daraja(153); rubuta_Daraja = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(Daddatse_Lamba_mara(위치++, true));
            else { Tabbatar_da_rubuta(단항(), 1); 내보내기(116); }
            rubuta_Daraja = 1;
        } else if (받기('+')) { Tabbatar_da_rubuta(단항(), 1); rubuta_Daraja = 1; }
        else rubuta_Daraja = 기본식();
        식깊이--; return rubuta_Daraja;
    }
    static int 곱식() {
        int rubuta_Daraja = 단항();
        while (!Kuskure && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int Juyar_da_bayanai_zuwa_lamba_Daraja = 종류(); 위치++; Tabbatar_da_rubuta(rubuta_Daraja, 1); Tabbatar_da_rubuta(단항(), 1);
            내보내기(Juyar_da_bayanai_zuwa_lamba_Daraja == '*' ? 104 : Juyar_da_bayanai_zuwa_lamba_Daraja == '/' ? 108 : 112); rubuta_Daraja = 1;
        }
        return rubuta_Daraja;
    }
    static int 합식() {
        int rubuta_Daraja = 곱식();
        while (!Kuskure && (종류() == '+' || 종류() == '-')) {
            int Juyar_da_bayanai_zuwa_lamba_Daraja = 종류(); 위치++; int 경계 = lambar_sirri_girma, Baya_Daraja_rubuta = 곱식();
            if (Juyar_da_bayanai_zuwa_lamba_Daraja == '+' && (rubuta_Daraja == 3 || Baya_Daraja_rubuta == 3)) { 결합(경계, rubuta_Daraja, Baya_Daraja_rubuta); rubuta_Daraja = 3; }
            else { Tabbatar_da_rubuta(rubuta_Daraja, 1); Tabbatar_da_rubuta(Baya_Daraja_rubuta, 1); 내보내기(Juyar_da_bayanai_zuwa_lamba_Daraja == '+' ? 96 : 100); rubuta_Daraja = 1; }
        }
        return rubuta_Daraja;
    }
    static int 붙임참조(int rubuta_Daraja) {
        if (rubuta_Daraja != 1 && rubuta_Daraja != 2 && rubuta_Daraja != 3 && rubuta_Daraja != 5) Kasa_aiki_Daraja("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", rubuta_Daraja == 1 ? "(I)Ljava/lang/StringBuilder;"
            : rubuta_Daraja == 2 ? "(Z)Ljava/lang/StringBuilder;" : rubuta_Daraja == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int kyamarar_gaba_Daraja_rubuta, int Baya_Daraja_rubuta) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 lambar_sirri_Daraja 앞에 생성 코드를 삽입한다.
        // 오른쪽 Aiyana_alƙaluma_Daraja 내부의 Fiya_Daraja Reshe 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = lambar_sirri_girma;
        Umarni(187, Manazarta(7, Microsoft_Word_Jurarre("java/lang/StringBuilder"), 0)); 내보내기(89);
        Umarni(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Umarni(182, 붙임참조(kyamarar_gaba_Daraja_rubuta));
        if (Kuskure) return;
        int Tsawo_Daraja = lambar_sirri_girma - 끝;
        for (int 수 = 0; 수 < Tsawo_Daraja; 수++) 삽입코드[수] = lambar_sirri_Daraja[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) lambar_sirri_Daraja[수 + Tsawo_Daraja] = lambar_sirri_Daraja[수];
        for (int 수 = 0; 수 < Tsawo_Daraja; 수++) lambar_sirri_Daraja[경계 + 수] = 삽입코드[수];
        Umarni(182, 붙임참조(Baya_Daraja_rubuta)); Umarni(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Kwatantawa_Aiyana_alƙaluma() {
        int rubuta_Daraja = 합식();
        while (!Kuskure && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int Juyar_da_bayanai_zuwa_lamba_Daraja = 종류(); 위치++; Tabbatar_da_rubuta(rubuta_Daraja, 1); Tabbatar_da_rubuta(합식(), 1);
            Kwatantawa_Daraja(Juyar_da_bayanai_zuwa_lamba_Daraja == '<' ? 161 : Juyar_da_bayanai_zuwa_lamba_Daraja == '>' ? 163 : Juyar_da_bayanai_zuwa_lamba_Daraja == 302 ? 164 : 162); rubuta_Daraja = 2;
        }
        return rubuta_Daraja;
    }
    static int 동등식() {
        int rubuta_Daraja = Kwatantawa_Aiyana_alƙaluma();
        while (!Kuskure && (종류() == 300 || 종류() == 301)) {
            int Juyar_da_bayanai_zuwa_lamba_Daraja = 종류(); 위치++; int Baya_Daraja_rubuta = Kwatantawa_Aiyana_alƙaluma();
            if (rubuta_Daraja == 0 || Baya_Daraja_rubuta == 0) Kasa_aiki_Daraja("void expression");
            if (!(Lamba_mara_rubuta(rubuta_Daraja) && Lamba_mara_rubuta(Baya_Daraja_rubuta))) Tabbatar_da_rubuta(Baya_Daraja_rubuta, rubuta_Daraja);
            Kwatantawa_Daraja((rubuta_Daraja <= 2 || rubuta_Daraja == 5 ? 159 : 165) + (Juyar_da_bayanai_zuwa_lamba_Daraja == 301 ? 1 : 0)); rubuta_Daraja = 2;
        }
        return rubuta_Daraja;
    }
    static int 논리곱() {
        int rubuta_Daraja = 동등식();
        while (!Kuskure && 받기(304)) {
            Tabbatar_da_rubuta(rubuta_Daraja, 2); int 가 = Reshe(153); Tabbatar_da_rubuta(동등식(), 2); int 나 = Reshe(153);
            내보내기(4); int 끝 = Reshe(167); Kafa_Daraja(가, lambar_sirri_girma); Kafa_Daraja(나, lambar_sirri_girma); 내보내기(3); Kafa_Daraja(끝, lambar_sirri_girma); rubuta_Daraja = 2;
        }
        return rubuta_Daraja;
    }
    static int Aiyana_alƙaluma_Daraja() {
        int rubuta_Daraja = 논리곱();
        while (!Kuskure && 받기(305)) {
            Tabbatar_da_rubuta(rubuta_Daraja, 2); int 가 = Reshe(154); Tabbatar_da_rubuta(논리곱(), 2); int 나 = Reshe(154);
            내보내기(3); int 끝 = Reshe(167); Kafa_Daraja(가, lambar_sirri_girma); Kafa_Daraja(나, lambar_sirri_girma); 내보내기(4); Kafa_Daraja(끝, lambar_sirri_girma); rubuta_Daraja = 2;
        }
        return rubuta_Daraja;
    }
    static void aikin_darasi_Daraja(boolean Bada_izini_bayyanarwa) {
        if (Microsoft_Word_Daraja(위치, "int") || Microsoft_Word_Daraja(위치, "boolean") || Microsoft_Word_Daraja(위치, "String") || Microsoft_Word_Daraja(위치, "char")
            || Microsoft_Word_Daraja(위치, "FileInputStream") || Microsoft_Word_Daraja(위치, "FileOutputStream")) {
            if (!Bada_izini_bayyanarwa) Kasa_aiki_Daraja("declaration not allowed here");
            int rubuta_Daraja = zubi_Daraja(), Suna = mai_ganewa_Daraja(); 요구('='); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), rubuta_Daraja);
            Rubuta_na_gida(ƙara_na_gida(Suna, rubuta_Daraja)); return;
        }
        int Suna = mai_ganewa_Daraja(), na_gida_Kima = nema_na_gida(Suna);
        if (받기('=')) { Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), na_gida_rubuta[na_gida_Kima]); Rubuta_na_gida(na_gida_Kima); }
        else if (종류() >= 308 && 종류() <= 312) {
            int Juyar_da_bayanai_zuwa_lamba_Daraja = 종류(); 위치++; 지역읽기(na_gida_Kima); int 경계 = lambar_sirri_girma, Baya_Daraja_rubuta = Aiyana_alƙaluma_Daraja();
            if (Juyar_da_bayanai_zuwa_lamba_Daraja == 308 && na_gida_rubuta[na_gida_Kima] == 3) 결합(경계, 3, Baya_Daraja_rubuta);
            else {
                Tabbatar_da_rubuta(na_gida_rubuta[na_gida_Kima], 1); Tabbatar_da_rubuta(Baya_Daraja_rubuta, 1);
                내보내기(Juyar_da_bayanai_zuwa_lamba_Daraja == 308 ? 96 : Juyar_da_bayanai_zuwa_lamba_Daraja == 309 ? 100 : Juyar_da_bayanai_zuwa_lamba_Daraja == 310 ? 104 : Juyar_da_bayanai_zuwa_lamba_Daraja == 311 ? 108 : 112);
                if (na_gida_rubuta[na_gida_Kima] == 5) 내보내기(146);
            }
            Rubuta_na_gida(na_gida_Kima);
        }
        else if (종류() == 306 || 종류() == 307) {
            Tabbatar_da_rubuta(na_gida_rubuta[na_gida_Kima], 1); 내보내기(132); 내보내기(na_gida_Kima); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (na_gida_rubuta[na_gida_Kima] == 5) { 지역읽기(na_gida_Kima); 내보내기(146); Rubuta_na_gida(na_gida_Kima); }
        } else Kasa_aiki_Daraja("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Umarni(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean holoko_Tubalin_aiki = 종류() == ')';
        int rubuta_Daraja = holoko_Tubalin_aiki ? 0 : Aiyana_alƙaluma_Daraja(); 요구(')'); 요구(';');
        String 서술 = rubuta_Daraja == 0 ? "()V" : rubuta_Daraja == 1 ? "(I)V" : rubuta_Daraja == 2 ? "(Z)V" : rubuta_Daraja == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (rubuta_Daraja == 4 || rubuta_Daraja >= 6 || rubuta_Daraja == 0 && (!줄바꿈 || !holoko_Tubalin_aiki)) Kasa_aiki_Daraja("unsupported print argument");
        Umarni(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean bayani_Daraja() {
        if (Kuskure) return false;
        if (깊이 > 32) { Kasa_aiki_Daraja("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!Kuskure && 종류() != '}') { if (반환) Kasa_aiki_Daraja("unreachable statement"); 반환 = bayani_Daraja(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int rubuta_Daraja = 종류() == ';' ? 0 : Aiyana_alƙaluma_Daraja(); Tabbatar_da_rubuta(rubuta_Daraja, 함수반환[현재함수]); 요구(';');
            내보내기(rubuta_Daraja == 0 ? 177 : rubuta_Daraja <= 2 || rubuta_Daraja == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 2); 요구(')'); int 거짓 = Reshe(153);
            깊이++; boolean 가 = masarrafa_bayani(); 깊이--;
            if (말받기("else")) { int 끝 = Reshe(167); Kafa_Daraja(거짓, lambar_sirri_girma); 깊이++; boolean 나 = masarrafa_bayani(); 깊이--; Kafa_Daraja(끝, lambar_sirri_girma); return 가 && 나; }
            Kafa_Daraja(거짓, lambar_sirri_girma); return false;
        }
        if (말받기("while")) {
            int Tafiyar_da = lambar_sirri_girma; 요구('('); Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 2); 요구(')'); int 끝 = Reshe(153);
            깊이++; masarrafa_bayani(); 깊이--; Kafa_Daraja(Reshe(167), Tafiyar_da); Kafa_Daraja(끝, lambar_sirri_girma); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') aikin_darasi_Daraja(true); 요구(';');
            int Yanayi = lambar_sirri_girma; if (종류() == ';') 내보내기(4); else Tabbatar_da_rubuta(Aiyana_alƙaluma_Daraja(), 2); 요구(';');
            int 끝 = Reshe(153), Gundarin_zube = Reshe(167), Wartsakewa = lambar_sirri_girma;
            if (종류() != ')') aikin_darasi_Daraja(false); 요구(')'); Kafa_Daraja(Reshe(167), Yanayi); Kafa_Daraja(Gundarin_zube, lambar_sirri_girma);
            masarrafa_bayani(); Kafa_Daraja(Reshe(167), Wartsakewa); Kafa_Daraja(끝, lambar_sirri_girma);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Microsoft_Word_Daraja(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int rubuta_Daraja = Aiyana_alƙaluma_Daraja(); if (rubuta_Daraja != 0) 내보내기(87); 요구(';'); return false;
        }
        aikin_darasi_Daraja(true); 요구(';'); return false;
    }
    static boolean masarrafa_bayani() {
        if (Microsoft_Word_Daraja(위치, "int") || Microsoft_Word_Daraja(위치, "boolean") || Microsoft_Word_Daraja(위치, "char") || Microsoft_Word_Daraja(위치, "String")
            || Microsoft_Word_Daraja(위치, "FileInputStream") || Microsoft_Word_Daraja(위치, "FileOutputStream")) Kasa_aiki_Daraja("local declaration requires braces");
        return bayani_Daraja();
    }
    static void 출바(int Daraja) { if (출력크기 == 출력.length) Kasa_aiki_Daraja("class file too large"); else 출력[출력크기++] = Daraja & 255; }
    static void 출짧(int Daraja) { 출바(Daraja >> 8); 출바(Daraja); }
    static void 출정(int Daraja) { 출짧(Daraja >>> 16); 출짧(Daraja); }
    static void Rubuta_Aji() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < Jurarre_girma; 수++) 출바(Jurarre_Daraja[수]);
        출짧(0x21); 출짧(Aji_Jurarre); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(tsari_isa[수]); 출짧(tsari_Suna_Jurarre[수]); 출짧(함수서술[수]); 출짧(1); 출짧(lambar_sirri_Jurarre);
            출정(12 + tsari_Tsawo[수]); 출짧(128); 출짧(함수지역[수]); 출정(tsari_Tsawo[수]);
            for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < tsari_Tsawo[수]; rami_Mashigar_bayanai++) 출바(lambar_sirri_Daraja[tsari_lambar_sirri[수] + rami_Mashigar_bayanai]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Tafiyar_da() {
        if (Mai_anfani_da_kwamfuta.인수개수() == 1 && 자바도구.같음(Mai_anfani_da_kwamfuta.인수(0), "-version")) {
            Mai_anfani_da_kwamfuta.Yi_Rubutu("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (Mai_anfani_da_kwamfuta.인수개수() != 1) { Mai_anfani_da_kwamfuta.Yi_Rubutu("Usage: javac FILE.java\n"); return 2; }
        int Suna_girma = 자바도구.Suna(Fayil_Suna_SMS, Mai_anfani_da_kwamfuta.인수(0));
        if (Suna_girma < 6 || Suna_girma > 62 || Fayil_Suna_SMS[Suna_girma - 5] != '.' || Fayil_Suna_SMS[Suna_girma - 4] != 'j'
            || Fayil_Suna_SMS[Suna_girma - 3] != 'a' || Fayil_Suna_SMS[Suna_girma - 2] != 'v' || Fayil_Suna_SMS[Suna_girma - 1] != 'a') {
            Mai_anfani_da_kwamfuta.Yi_Rubutu("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        tushe_girma = Mai_anfani_da_kwamfuta.파일읽기(Fayil_Suna_SMS, tushe);
        if (tushe_girma < 0) { Mai_anfani_da_kwamfuta.Yi_Rubutu("javac: cannot read source: "); 자바도구.수쓰기(tushe_girma); Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja(10); return 1; }
        tushe_girma = 자바도구.원문해독(tushe, tushe_girma);
        if (tushe_girma < 0) { Mai_anfani_da_kwamfuta.Yi_Rubutu("javac error: invalid UTF-8 source\n"); return 1; }
        Yanka_Daraja(); if (!Kuskure) 선언읽기();
        if (!Kuskure) {
            if (token_Tsawo[Aji_token] != Suna_girma - 5) Kasa_aiki_Daraja("class name must match file name");
            for (int 수 = 0; 수 < Suna_girma - 5; 수++) if (tushe[토큰위치[Aji_token] + 수] != Fayil_Suna_SMS[수]) Kasa_aiki_Daraja("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !Kuskure; 현재함수++) {
            위치 = tsari_jiki[현재함수]; tsari_lambar_sirri[현재함수] = lambar_sirri_girma; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) ƙara_na_gida(tsari_Tubalin_aiki_Suna[현재함수 * 16 + 수], tsari_Tubalin_aiki_rubuta[현재함수 * 16 + 수]);
            boolean 반환 = bayani_Daraja();
            if (!반환 && 함수반환[현재함수] != 0) Kasa_aiki_Daraja("missing return");
            // Reshe 뒤의 합류 지점은 반드시 Na_hakika_Tarin_bayani 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean Lamba_mara = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(Lamba_mara ? 3 : 1); 내보내기(Lamba_mara ? 172 : 176); }
            if (위치 != tsari_Ƙarshe[현재함수]) Kasa_aiki_Daraja("invalid method body");
            함수지역[현재함수] = 지역수; tsari_Tsawo[현재함수] = lambar_sirri_girma - tsari_lambar_sirri[현재함수];
        }
        if (Kuskure) return 1;
        Rubuta_Aji(); if (Kuskure) return 1;
        Fayil_Suna_SMS[Suna_girma - 4] = 'c'; Fayil_Suna_SMS[Suna_girma - 3] = 'l'; Fayil_Suna_SMS[Suna_girma - 2] = 'a';
        Fayil_Suna_SMS[Suna_girma - 1] = 's'; Fayil_Suna_SMS[Suna_girma] = 's'; Fayil_Suna_SMS[Suna_girma + 1] = 0;
        int 결과 = Mai_anfani_da_kwamfuta.Rubuta_Fayil(Fayil_Suna_SMS, 출력, 출력크기);
        if (결과 < 0) { Mai_anfani_da_kwamfuta.Yi_Rubutu("javac: cannot save class: "); 자바도구.수쓰기(결과); Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja(10); return 1; }
        Mai_anfani_da_kwamfuta.Yi_Rubutu("Compiled: "); for (int 수 = 0; Fayil_Suna_SMS[수] != 0; 수++) Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja(Fayil_Suna_SMS[수]);
        Mai_anfani_da_kwamfuta.Yi_Rubutu(" (JVM class version 49)\n"); return 0;
    }
}
