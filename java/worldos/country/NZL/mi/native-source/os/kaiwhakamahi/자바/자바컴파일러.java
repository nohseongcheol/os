// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java pūtake_rākau -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] pūtake = new int[16384], 출력 = new int[16384], CODE_uara = new int[4096];
    static int[] 토큰종류 = new int[2048], tohu_tūranga = new int[2048], tohu_roa = new int[2048];
    static int[] taimau_uara = new int[4096], taimau_OFFSET = new int[512];
    static int[] 문자 = new int[512], kōnae_ingoa_TEXT = new int[64];
    static int[] 삽입코드 = new int[16];
    static int pūtake_rahi, tohu_COUNT, tūranga, CODE_rahi, taimau_rahi, taimau_COUNT = 1, 출력크기, pūāhua_roa;
    static boolean Pōhēhē;
    static int tauaha_tohu, tauaha_taimau, 부모상수, CODE_taimau;
    static int[] aratuka_tāurunga_ingoa = new int[32], 함수반환 = new int[32], aratuka_tohenga_COUNT = new int[32];
    static int[] aratuka_tohenga_ingoa = new int[512], aratuka_tohenga_TYPE = new int[512];
    static int[] 함수본문 = new int[32], aratuka_mutu = new int[32], aratuka_CODE = new int[32];
    static int[] aratuka_roa = new int[32], 함수지역 = new int[32], aratuka_ingoa_taimau = new int[32], 함수서술 = new int[32];
    static int[] aratuka_uru = new int[32];
    static int aratuka_COUNT, 현재함수, paetata_COUNT, 깊이, 식깊이;
    static int[] paetata_ingoa = new int[128], paetata_TYPE = new int[128], 지역깊이 = new int[128];

    static void rahunga_uara(String 이유) {
        if (!Pōhēhē) {
            kaiwhakamahi.Tuhia("javac error: "); kaiwhakamahi.Tuhia(이유);
            kaiwhakamahi.Tuhia(" at line ");
            int hononga = 1, 끝 = tūranga < tohu_COUNT ? tohu_tūranga[tūranga] : pūtake_rahi;
            for (int 수 = 0; 수 < 끝; 수++) if (pūtake[수] == 10) hononga++;
            자바도구.수쓰기(hononga); kaiwhakamahi.tuhi_pūāhua_uara(10);
        }
        Pōhēhē = true;
    }
    static boolean pūāhua_uara(int uara) { return 문자이름규칙.첫글자(uara); }
    static boolean mati_uara(int uara) { return uara >= '0' && uara <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= tohu_COUNT || 나 >= tohu_COUNT || tohu_roa[가] != tohu_roa[나]) return false;
        for (int 수 = 0; 수 < tohu_roa[가]; 수++) if (pūtake[tohu_tūranga[가] + 수] != pūtake[tohu_tūranga[나] + 수]) return false;
        return true;
    }
    static boolean Word_uara(int tohu_uara_eb540501, String Word_TEXT) {
        if (tohu_uara_eb540501 < 0 || tohu_uara_eb540501 >= tohu_COUNT || tohu_roa[tohu_uara_eb540501] != Word_TEXT.length()) return false;
        for (int 수 = 0; 수 < Word_TEXT.length(); 수++) if (pūtake[tohu_tūranga[tohu_uara_eb540501] + 수] != Word_TEXT.charAt(수)) return false;
        return true;
    }
    static int 종류() { return tūranga < tohu_COUNT ? 토큰종류[tūranga] : 0; }
    static boolean 받기(int uara) { if (종류() != uara) return false; tūranga++; return true; }
    static void 요구(int uara) { if (!받기(uara)) rahunga_uara("unexpected token"); }
    static boolean TAKE_Word(String Word_TEXT) { if (!Word_uara(tūranga, Word_TEXT)) return false; tūranga++; return true; }
    static void 말요구(String Word_TEXT) { if (!TAKE_Word(Word_TEXT)) rahunga_uara(Word_TEXT); }
    static int pūtāutu_uara() {
        int mēhua = tūranga;
        if (종류() != 256) rahunga_uara("identifier required"); else tūranga++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int whakahaere = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - whakahaere == tohu_roa[mēhua];
                for (int kāniwha_tāurunga = whakahaere; 같음 && kāniwha_tāurunga < 수; kāniwha_tāurunga++) if (예약어.charAt(kāniwha_tāurunga) != pūtake[tohu_tūranga[mēhua] + kāniwha_tāurunga - whakahaere]) 같음 = false;
                if (같음) rahunga_uara("reserved word cannot be an identifier");
                whakahaere = 수 + 1;
            }
        }
        return mēhua;
    }
    static void tapahi_uara() {
        int 수 = 0;
        while (수 < pūtake_rahi && !Pōhēhē) {
            int uara = pūtake[수], whakahaere = 수, 종류 = uara;
            if (uara == 32 || uara == 9 || uara == 10 || uara == 13) { 수++; continue; }
            if (uara == '/' && 수 + 1 < pūtake_rahi && pūtake[수 + 1] == '/') {
                while (수 < pūtake_rahi && pūtake[수] != 10) 수++;
                continue;
            }
            if (uara == '/' && 수 + 1 < pūtake_rahi && pūtake[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < pūtake_rahi && !(pūtake[수] == '*' && pūtake[수 + 1] == '/')) 수++;
                if (수 + 1 >= pūtake_rahi) { rahunga_uara("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (pūāhua_uara(uara)) { 종류 = 256; while (수 < pūtake_rahi && 문자이름규칙.이어진글자(pūtake[수])) 수++; }
            else if (mati_uara(uara)) { 종류 = 257; while (수 < pūtake_rahi && mati_uara(pūtake[수])) 수++; }
            else if (uara == '"' || uara == '\'') {
                종류 = uara == '"' ? 258 : 259; 수++;
                while (수 < pūtake_rahi && pūtake[수] != uara && pūtake[수] != 10 && pūtake[수] != 13) {
                    if (pūtake[수] == '\\') 수++;
                    수++;
                }
                if (수 >= pūtake_rahi || pūtake[수] != uara) { rahunga_uara("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < pūtake_rahi) {
                    int Panuku_tuemi = pūtake[수];
                    if (uara == '=' && Panuku_tuemi == '=') 종류 = 300;
                    if (uara == '!' && Panuku_tuemi == '=') 종류 = 301;
                    if (uara == '<' && Panuku_tuemi == '=') 종류 = 302;
                    if (uara == '>' && Panuku_tuemi == '=') 종류 = 303;
                    if (uara == '&' && Panuku_tuemi == '&') 종류 = 304;
                    if (uara == '|' && Panuku_tuemi == '|') 종류 = 305;
                    if (uara == '+' && Panuku_tuemi == '+') 종류 = 306;
                    if (uara == '-' && Panuku_tuemi == '-') 종류 = 307;
                    if (uara == '+' && Panuku_tuemi == '=') 종류 = 308;
                    if (uara == '-' && Panuku_tuemi == '=') 종류 = 309;
                    if (uara == '*' && Panuku_tuemi == '=') 종류 = 310;
                    if (uara == '/' && Panuku_tuemi == '=') 종류 = 311;
                    if (uara == '%' && Panuku_tuemi == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (tohu_COUNT == 토큰종류.length - 1) { rahunga_uara("too many tokens (2047 maximum)"); break; }
            토큰종류[tohu_COUNT] = 종류; tohu_tūranga[tohu_COUNT] = whakahaere; tohu_roa[tohu_COUNT++] = 수 - whakahaere;
        }
    }
    static void tuhi_taimau_paita(int uara) {
        if (taimau_rahi == taimau_uara.length) { rahunga_uara("constant pool too large"); return; }
        taimau_uara[taimau_rahi++] = uara & 255;
    }
    static void 상짧(int uara) { tuhi_taimau_paita(uara >> 8); tuhi_taimau_paita(uara); }
    static int rēhita_taimau(int whakahaere) {
        for (int 수 = 1; 수 < taimau_COUNT; 수++) {
            int 앞 = taimau_OFFSET[수], roa_uara = (수 + 1 < taimau_COUNT ? taimau_OFFSET[수 + 1] : whakahaere) - 앞;
            if (roa_uara != taimau_rahi - whakahaere) continue;
            boolean 같음 = true;
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < roa_uara; kāniwha_tāurunga++) if (taimau_uara[앞 + kāniwha_tāurunga] != taimau_uara[whakahaere + kāniwha_tāurunga]) 같음 = false;
            if (같음) { taimau_rahi = whakahaere; return 수; }
        }
        if (taimau_COUNT == taimau_OFFSET.length) { rahunga_uara("too many constants"); return 0; }
        taimau_OFFSET[taimau_COUNT] = whakahaere;
        return taimau_COUNT++;
    }
    static void 글추가(int uara) {
        if (pūāhua_roa == 문자.length) { rahunga_uara("text too long"); return; }
        문자[pūāhua_roa++] = uara;
    }
    static void 말추가(String Word_TEXT) { for (int 수 = 0; 수 < Word_TEXT.length(); 수++) 글추가(Word_TEXT.charAt(수)); }
    static int pūāhua_taimau() {
        int whakahaere = taimau_rahi; tuhi_taimau_paita(1); 상짧(0);
        for (int 수 = 0; 수 < pūāhua_roa; 수++) {
            int uara = 문자[수];
            if (uara > 0 && uara < 128) tuhi_taimau_paita(uara);
            else if (uara < 2048) { tuhi_taimau_paita(192 | uara >> 6); tuhi_taimau_paita(128 | uara & 63); }
            else { tuhi_taimau_paita(224 | uara >> 12); tuhi_taimau_paita(128 | uara >> 6 & 63); tuhi_taimau_paita(128 | uara & 63); }
        }
        if (Pōhēhē) return 0;
        int roa_uara = taimau_rahi - whakahaere - 3;
        taimau_uara[whakahaere + 1] = roa_uara >> 8; taimau_uara[whakahaere + 2] = roa_uara & 255;
        return rēhita_taimau(whakahaere);
    }
    static int Word_taimau(String Word_TEXT) { pūāhua_roa = 0; 말추가(Word_TEXT); return pūāhua_taimau(); }
    static int tohu_taimau(int tohu_uara_eb540501) {
        pūāhua_roa = 0;
        for (int 수 = 0; 수 < tohu_roa[tohu_uara_eb540501]; 수++) 글추가(pūtake[tohu_tūranga[tohu_uara_eb540501] + 수]);
        return pūāhua_taimau();
    }
    static int Pūranga_kōrero(int 종류, int 가, int 나) {
        int whakahaere = taimau_rahi; tuhi_taimau_paita(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return rēhita_taimau(whakahaere);
    }
    static int 외부참조(int 종류, String kaipupuri_uara, String Ingoa, String 서술) {
        int kaipupuri_pūtāutu = Pūranga_kōrero(7, Word_taimau(kaipupuri_uara), 0);
        int ingoa_COUNT = Word_taimau(Ingoa), hōputu_COUNT = Word_taimau(서술);
        return Pūranga_kōrero(종류, kaipupuri_pūtāutu, Pūranga_kōrero(12, ingoa_COUNT, hōputu_COUNT));
    }
    static void 내보내기(int uara) {
        if (CODE_rahi == CODE_uara.length) { rahunga_uara("bytecode too large"); return; }
        CODE_uara[CODE_rahi++] = uara & 255;
    }
    static void tono(int uara, int 인수) { 내보내기(uara); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int uara) {
        if (uara >= -1 && uara <= 5) { 내보내기(uara + 3); return; }
        int whakahaere = taimau_rahi; tuhi_taimau_paita(3); 상짧(uara >>> 16); 상짧(uara);
        tono(19, rēhita_taimau(whakahaere));
    }
    static int peka(int tono) { int mēhua = CODE_rahi; tono(tono, 0); return mēhua; }
    static void Hono_uara(int peka, int ūnga_ahanoa) {
        if (Pōhēhē) return;
        int 거리 = ūnga_ahanoa - peka;
        if (거리 < -32768 || 거리 > 32767 || peka < 0 || peka + 2 >= CODE_rahi) { rahunga_uara("invalid branch"); return; }
        CODE_uara[peka + 1] = 거리 >> 8 & 255; CODE_uara[peka + 2] = 거리 & 255;
    }
    static void 비교값(int tono) {
        int TRUE_uara = peka(tono); 내보내기(3); int 끝 = peka(167);
        Hono_uara(TRUE_uara, CODE_rahi); 내보내기(4); Hono_uara(끝, CODE_rahi);
    }
    static int hōputu_uara() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        rahunga_uara("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void tāpiri_hōputu(int TYPE_uara) {
        if (TYPE_uara == 0) 글추가('V');
        if (TYPE_uara == 1) 글추가('I');
        if (TYPE_uara == 2) 글추가('Z');
        if (TYPE_uara == 3) 말추가("Ljava/lang/String;");
        if (TYPE_uara == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_uara == 5) 글추가('C');
        if (TYPE_uara == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_uara == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Hātepe_uara_tāurunga 본문은 taurima javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("Reo_Māori");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("예외") || TAKE_Word("실행예외") || TAKE_Word("입출력예외") || TAKE_Word("대기시간초과예외") || TAKE_Word("주소확인예외") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("잘못된인수예외") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("빈참조예외") || TAKE_Word("산술예외") || TAKE_Word("상태예외") || TAKE_Word("형변환예외") || TAKE_Word("음수배열크기예외") || TAKE_Word("HUĀNGA_Store_rahunga") || TAKE_Word("가닥상태예외") || TAKE_Word("대기중단예외")) return;
        rahunga_uara("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_uara(tūranga, "Reo_Māori")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) rahunga_uara("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); tauaha_tohu = pūtāutu_uara();
        tauaha_taimau = Pūranga_kōrero(7, tohu_taimau(tauaha_tohu), 0);
        부모상수 = Pūranga_kōrero(7, Word_taimau("java/lang/Object"), 0); CODE_taimau = Word_taimau("Code"); 요구('{');
        while (!Pōhēhē && 종류() != '}') {
            if (aratuka_COUNT == 32) { rahunga_uara("too many methods"); break; }
            int uru_tāurunga = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int TAUMAHI_uara = aratuka_COUNT++;
            aratuka_uru[TAUMAHI_uara] = uru_tāurunga | 8;
            함수반환[TAUMAHI_uara] = hōputu_uara(); aratuka_tāurunga_ingoa[TAUMAHI_uara] = pūtāutu_uara(); 요구('(');
            for (int 앞 = 0; 앞 < TAUMAHI_uara; 앞++) if (이름같음(aratuka_tāurunga_ingoa[앞], aratuka_tāurunga_ingoa[TAUMAHI_uara])) rahunga_uara("duplicate method (overloading unsupported)");
            while (!Pōhēhē && 종류() != ')') {
                int 수 = aratuka_tohenga_COUNT[TAUMAHI_uara];
                if (수 == 16) { rahunga_uara("too many parameters"); break; }
                int TYPE_uara = hōputu_uara(); if (TYPE_uara == 0) rahunga_uara("void parameter");
                aratuka_tohenga_TYPE[TAUMAHI_uara * 16 + 수] = TYPE_uara; aratuka_tohenga_ingoa[TAUMAHI_uara * 16 + 수] = pūtāutu_uara();
                aratuka_tohenga_COUNT[TAUMAHI_uara]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!Pōhēhē && 받기(','));
            }
            함수본문[TAUMAHI_uara] = tūranga; 요구('{');
            int 중첩 = 1;
            while (tūranga < tohu_COUNT && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                tūranga++;
            }
            if (중첩 != 0) rahunga_uara("unclosed method body");
            aratuka_mutu[TAUMAHI_uara] = tūranga;
            aratuka_ingoa_taimau[TAUMAHI_uara] = tohu_taimau(aratuka_tāurunga_ingoa[TAUMAHI_uara]);
            pūāhua_roa = 0; 글추가('(');
            for (int 수 = 0; 수 < aratuka_tohenga_COUNT[TAUMAHI_uara]; 수++) tāpiri_hōputu(aratuka_tohenga_TYPE[TAUMAHI_uara * 16 + 수]);
            글추가(')'); tāpiri_hōputu(함수반환[TAUMAHI_uara]); 함수서술[TAUMAHI_uara] = pūāhua_taimau();
        }
        요구('}'); if (tūranga != tohu_COUNT) rahunga_uara("extra input after class");
    }
    static int FIND_paetata(int Ingoa) {
        for (int 수 = paetata_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(paetata_ingoa[수], Ingoa)) return 수;
        rahunga_uara("unknown variable"); return 0;
    }
    static int tāpiri_paetata(int Ingoa, int TYPE_uara) {
        for (int 수 = 0; 수 < paetata_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(paetata_ingoa[수], Ingoa)) rahunga_uara("duplicate local variable");
        if (paetata_COUNT == 128) { rahunga_uara("too many locals"); return 0; }
        paetata_ingoa[paetata_COUNT] = Ingoa; paetata_TYPE[paetata_COUNT] = TYPE_uara; 지역깊이[paetata_COUNT] = 깊이;
        return paetata_COUNT++;
    }
    static boolean tau_tōpū_TYPE(int TYPE_uara) { return TYPE_uara == 1 || TYPE_uara == 5; }
    static void 지역읽기(int 수) { 내보내기(paetata_TYPE[수] <= 2 || paetata_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void tuhi_paetata(int 수) { 내보내기(paetata_TYPE[수] <= 2 || paetata_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void manatoko_TYPE(int tūturu_raraunga, int 기대) { if (tūturu_raraunga != 기대 && !(tūturu_raraunga == 5 && 기대 == 1)) rahunga_uara("type mismatch"); }
    static void 문자읽기(int tohu_uara_eb540501) {
        pūāhua_roa = 0; int whakahaere = tohu_tūranga[tohu_uara_eb540501] + 1, 끝 = tohu_tūranga[tohu_uara_eb540501] + tohu_roa[tohu_uara_eb540501] - 1;
        while (whakahaere < 끝 && !Pōhēhē) {
            int uara = pūtake[whakahaere++];
            if (uara == '\\') {
                if (whakahaere == 끝) { rahunga_uara("invalid escape"); break; }
                uara = pūtake[whakahaere++];
                if (uara == 'n') uara = 10;
                else if (uara == 'r') uara = 13;
                else if (uara == 't') uara = 9;
                else if (uara == 'b') uara = 8;
                else if (uara == 'f') uara = 12;
                else if (uara != '\\' && uara != '"' && uara != '\'') rahunga_uara("unsupported escape");
            }
            글추가(uara);
        }
    }
    static int poroporo_tau_tōpū(int tohu_uara_eb540501, boolean 음수) {
        if (tohu_roa[tohu_uara_eb540501] > 1 && pūtake[tohu_tūranga[tohu_uara_eb540501]] == '0') rahunga_uara("octal literals unsupported");
        int uara = 0;
        for (int 수 = 0; 수 < tohu_roa[tohu_uara_eb540501]; 수++) {
            int mati_tuemi = pūtake[tohu_tūranga[tohu_uara_eb540501] + 수] - '0';
            if (uara < -214748364 || uara == -214748364 && mati_tuemi > (음수 ? 8 : 7)) rahunga_uara("integer literal out of range");
            uara = uara * 10 - mati_tuemi;
        }
        return 음수 ? uara : -uara;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_uara = hōputu_uara();
            if (TYPE_uara != 6 && TYPE_uara != 7) { rahunga_uara("only file streams supported by new in source"); return 0; }
            String kaipupuri_uara = TYPE_uara == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            tono(187, Pūranga_kōrero(7, Word_taimau(kaipupuri_uara), 0)); 내보내기(89);
            요구('('); manatoko_TYPE(kīanga_uara(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_uara != 7) rahunga_uara("input stream constructor arguments"); manatoko_TYPE(kīanga_uara(), 2); 이어 = true; }
            요구(')');
            tono(183, 외부참조(10, kaipupuri_uara, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_uara;
        }
        if (받기('(')) { int TYPE_uara = kīanga_uara(); 요구(')'); return TYPE_uara; }
        if (종류() == 257) { 수상수(poroporo_tau_tōpū(tūranga++, false)); return 1; }
        if (종류() == 258) { 문자읽기(tūranga++); tono(19, Pūranga_kōrero(8, pūāhua_taimau(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(tūranga++); if (pūāhua_roa != 1) rahunga_uara("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("Reo_Māori")) {
            요구('.'); 말요구("자체"); 요구('.');
            String kaipupuri_uara = "", aratuka_uara = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, mēhua = 0;
            if (TAKE_Word("출력")) {
                kaipupuri_uara = "Reo_Māori/자체/출력"; 요구('.');
                if (TAKE_Word("tuhi_hononga")) { aratuka_uara = "tuhi_hononga"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Tuhia")) { aratuka_uara = "Tuhia"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { aratuka_uara = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else rahunga_uara("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                kaipupuri_uara = "Reo_Māori/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("roa_uara")) { aratuka_uara = "roa_uara"; 서술 = "(Ljava/lang/String;)I"; mēhua = 1; }
                else if (TAKE_Word("waehere_pūāhua_COUNT")) { aratuka_uara = "waehere_pūāhua_COUNT"; 서술 = "(Ljava/lang/String;)I"; mēhua = 1; }
                else if (TAKE_Word("poroporo_tau_tōpū")) { aratuka_uara = "poroporo_tau_tōpū"; 서술 = "(Ljava/lang/String;)I"; mēhua = 1; }
                else if (TAKE_Word("tuhi_tau_tōpū_uara")) { aratuka_uara = "tuhi_tau_tōpū_uara"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; mēhua = 3; }
                else if (TAKE_Word("같음")) { aratuka_uara = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; mēhua = 2; }
                else if (TAKE_Word("whakapiri_TEXT")) { aratuka_uara = "whakapiri_TEXT"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; mēhua = 3; }
                else if (TAKE_Word("tapahi_uara")) { aratuka_uara = "tapahi_uara"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; mēhua = 3; }
                else rahunga_uara("unknown Korean text method");
            } else if (TAKE_Word("Kōnae")) {
                kaipupuri_uara = "Reo_Māori/자체/Kōnae"; 요구('.'); 가 = 3;
                if (TAKE_Word("Pānuitia")) { aratuka_uara = "Pānuitia"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; mēhua = 3; }
                else if (TAKE_Word("Tuhia")) { aratuka_uara = "Tuhia"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else rahunga_uara("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                kaipupuri_uara = "Reo_Māori/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { aratuka_uara = "너비"; 서술 = "()I"; mēhua = 1; }
                else if (TAKE_Word("높이")) { aratuka_uara = "높이"; 서술 = "()I"; mēhua = 1; }
                else if (TAKE_Word("사각형")) { aratuka_uara = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("지우기")) { aratuka_uara = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { aratuka_uara = "기다리기"; 서술 = "()V"; }
                else rahunga_uara("unknown Korean framebuffer method");
            } else rahunga_uara("unsupported Korean library class");
            요구('('); if (가 != 0) manatoko_TYPE(kīanga_uara(), 가);
            if (나 != 0) { 요구(','); manatoko_TYPE(kīanga_uara(), 나); }
            if (다 != 0) { 요구(','); manatoko_TYPE(kīanga_uara(), 다); }
            if (라 != 0) { 요구(','); manatoko_TYPE(kīanga_uara(), 라); }
            if (마 != 0) { 요구(','); manatoko_TYPE(kīanga_uara(), 마); }
            요구(')'); tono(184, 외부참조(10, kaipupuri_uara, aratuka_uara, 서술)); return mēhua;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); manatoko_TYPE(kīanga_uara(), 3); 요구(')');
            tono(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Ingoa = pūtāutu_uara();
        if (받기('(')) {
            int TAUMAHI_uara = -1;
            for (int 수 = 0; 수 < aratuka_COUNT; 수++) if (이름같음(Ingoa, aratuka_tāurunga_ingoa[수])) TAUMAHI_uara = 수;
            if (TAUMAHI_uara < 0) { rahunga_uara("unknown static method"); return 0; }
            int 수 = 0;
            while (!Pōhēhē && 종류() != ')') {
                if (수 >= aratuka_tohenga_COUNT[TAUMAHI_uara]) { rahunga_uara("too many arguments"); break; }
                manatoko_TYPE(kīanga_uara(), aratuka_tohenga_TYPE[TAUMAHI_uara * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != aratuka_tohenga_COUNT[TAUMAHI_uara]) rahunga_uara("argument count mismatch");
            tono(184, Pūranga_kōrero(10, tauaha_taimau, Pūranga_kōrero(12, aratuka_ingoa_taimau[TAUMAHI_uara], 함수서술[TAUMAHI_uara])));
            return 함수반환[TAUMAHI_uara];
        }
        int paetata_whānuitanga = FIND_paetata(Ingoa), TYPE_uara = paetata_TYPE[paetata_whānuitanga]; 지역읽기(paetata_whānuitanga);
        while (!Pōhēhē) {
            if (받기('[')) { manatoko_TYPE(TYPE_uara, 4); manatoko_TYPE(kīanga_uara(), 1); 요구(']'); 내보내기(50); TYPE_uara = 3; }
            else if (받기('.')) {
                if (TYPE_uara == 6 || TYPE_uara == 7) {
                    String kaipupuri_uara = TYPE_uara == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); tono(182, 외부참조(10, kaipupuri_uara, "close", "()V")); TYPE_uara = 0; }
                    else if (TYPE_uara == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); tono(182, 외부참조(10, kaipupuri_uara, "read", "()I")); TYPE_uara = 1; }
                    else if (TYPE_uara == 7 && TAKE_Word("write")) { 요구('('); manatoko_TYPE(kīanga_uara(), 1); 요구(')'); tono(182, 외부참조(10, kaipupuri_uara, "write", "(I)V")); TYPE_uara = 0; }
                    else { rahunga_uara("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_uara == 4) { 내보내기(190); TYPE_uara = 1; }
                else { manatoko_TYPE(TYPE_uara, 3); 요구('('); 요구(')'); tono(182, 외부참조(10, "java/lang/String", "length", "()I")); TYPE_uara = 1; }
            } else break;
        }
        return TYPE_uara;
    }
    static int 단항() {
        if (++식깊이 > 64) { rahunga_uara("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_uara;
        if (받기('!')) { manatoko_TYPE(단항(), 2); 비교값(153); TYPE_uara = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(poroporo_tau_tōpū(tūranga++, true));
            else { manatoko_TYPE(단항(), 1); 내보내기(116); }
            TYPE_uara = 1;
        } else if (받기('+')) { manatoko_TYPE(단항(), 1); TYPE_uara = 1; }
        else TYPE_uara = 기본식();
        식깊이--; return TYPE_uara;
    }
    static int 곱식() {
        int TYPE_uara = 단항();
        while (!Pōhēhē && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int whakawaehere_uara = 종류(); tūranga++; manatoko_TYPE(TYPE_uara, 1); manatoko_TYPE(단항(), 1);
            내보내기(whakawaehere_uara == '*' ? 104 : whakawaehere_uara == '/' ? 108 : 112); TYPE_uara = 1;
        }
        return TYPE_uara;
    }
    static int 합식() {
        int TYPE_uara = 곱식();
        while (!Pōhēhē && (종류() == '+' || 종류() == '-')) {
            int whakawaehere_uara = 종류(); tūranga++; int 경계 = CODE_rahi, Hoki_uara_TYPE = 곱식();
            if (whakawaehere_uara == '+' && (TYPE_uara == 3 || Hoki_uara_TYPE == 3)) { 결합(경계, TYPE_uara, Hoki_uara_TYPE); TYPE_uara = 3; }
            else { manatoko_TYPE(TYPE_uara, 1); manatoko_TYPE(Hoki_uara_TYPE, 1); 내보내기(whakawaehere_uara == '+' ? 96 : 100); TYPE_uara = 1; }
        }
        return TYPE_uara;
    }
    static int 붙임참조(int TYPE_uara) {
        if (TYPE_uara != 1 && TYPE_uara != 2 && TYPE_uara != 3 && TYPE_uara != 5) rahunga_uara("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", TYPE_uara == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_uara == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_uara == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Hoki_uara_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_uara 앞에 waihanga 코드를 삽입한다.
        // RIGHT kīanga_uara 내부의 hoa_uara peka 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_rahi;
        tono(187, Pūranga_kōrero(7, Word_taimau("java/lang/StringBuilder"), 0)); 내보내기(89);
        tono(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); tono(182, 붙임참조(앞형));
        if (Pōhēhē) return;
        int roa_uara = CODE_rahi - 끝;
        for (int 수 = 0; 수 < roa_uara; 수++) 삽입코드[수] = CODE_uara[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_uara[수 + roa_uara] = CODE_uara[수];
        for (int 수 = 0; 수 < roa_uara; 수++) CODE_uara[경계 + 수] = 삽입코드[수];
        tono(182, 붙임참조(Hoki_uara_TYPE)); tono(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int TYPE_uara = 합식();
        while (!Pōhēhē && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int whakawaehere_uara = 종류(); tūranga++; manatoko_TYPE(TYPE_uara, 1); manatoko_TYPE(합식(), 1);
            비교값(whakawaehere_uara == '<' ? 161 : whakawaehere_uara == '>' ? 163 : whakawaehere_uara == 302 ? 164 : 162); TYPE_uara = 2;
        }
        return TYPE_uara;
    }
    static int 동등식() {
        int TYPE_uara = 비교식();
        while (!Pōhēhē && (종류() == 300 || 종류() == 301)) {
            int whakawaehere_uara = 종류(); tūranga++; int Hoki_uara_TYPE = 비교식();
            if (TYPE_uara == 0 || Hoki_uara_TYPE == 0) rahunga_uara("void expression");
            if (!(tau_tōpū_TYPE(TYPE_uara) && tau_tōpū_TYPE(Hoki_uara_TYPE))) manatoko_TYPE(Hoki_uara_TYPE, TYPE_uara);
            비교값((TYPE_uara <= 2 || TYPE_uara == 5 ? 159 : 165) + (whakawaehere_uara == 301 ? 1 : 0)); TYPE_uara = 2;
        }
        return TYPE_uara;
    }
    static int 논리곱() {
        int TYPE_uara = 동등식();
        while (!Pōhēhē && 받기(304)) {
            manatoko_TYPE(TYPE_uara, 2); int 가 = peka(153); manatoko_TYPE(동등식(), 2); int 나 = peka(153);
            내보내기(4); int 끝 = peka(167); Hono_uara(가, CODE_rahi); Hono_uara(나, CODE_rahi); 내보내기(3); Hono_uara(끝, CODE_rahi); TYPE_uara = 2;
        }
        return TYPE_uara;
    }
    static int kīanga_uara() {
        int TYPE_uara = 논리곱();
        while (!Pōhēhē && 받기(305)) {
            manatoko_TYPE(TYPE_uara, 2); int 가 = peka(154); manatoko_TYPE(논리곱(), 2); int 나 = peka(154);
            내보내기(3); int 끝 = peka(167); Hono_uara(가, CODE_rahi); Hono_uara(나, CODE_rahi); 내보내기(4); Hono_uara(끝, CODE_rahi); TYPE_uara = 2;
        }
        return TYPE_uara;
    }
    static void wehenga_mahi_uara(boolean 선언허용) {
        if (Word_uara(tūranga, "int") || Word_uara(tūranga, "boolean") || Word_uara(tūranga, "String") || Word_uara(tūranga, "char")
            || Word_uara(tūranga, "FileInputStream") || Word_uara(tūranga, "FileOutputStream")) {
            if (!선언허용) rahunga_uara("declaration not allowed here");
            int TYPE_uara = hōputu_uara(), Ingoa = pūtāutu_uara(); 요구('='); manatoko_TYPE(kīanga_uara(), TYPE_uara);
            tuhi_paetata(tāpiri_paetata(Ingoa, TYPE_uara)); return;
        }
        int Ingoa = pūtāutu_uara(), paetata_whānuitanga = FIND_paetata(Ingoa);
        if (받기('=')) { manatoko_TYPE(kīanga_uara(), paetata_TYPE[paetata_whānuitanga]); tuhi_paetata(paetata_whānuitanga); }
        else if (종류() >= 308 && 종류() <= 312) {
            int whakawaehere_uara = 종류(); tūranga++; 지역읽기(paetata_whānuitanga); int 경계 = CODE_rahi, Hoki_uara_TYPE = kīanga_uara();
            if (whakawaehere_uara == 308 && paetata_TYPE[paetata_whānuitanga] == 3) 결합(경계, 3, Hoki_uara_TYPE);
            else {
                manatoko_TYPE(paetata_TYPE[paetata_whānuitanga], 1); manatoko_TYPE(Hoki_uara_TYPE, 1);
                내보내기(whakawaehere_uara == 308 ? 96 : whakawaehere_uara == 309 ? 100 : whakawaehere_uara == 310 ? 104 : whakawaehere_uara == 311 ? 108 : 112);
                if (paetata_TYPE[paetata_whānuitanga] == 5) 내보내기(146);
            }
            tuhi_paetata(paetata_whānuitanga);
        }
        else if (종류() == 306 || 종류() == 307) {
            manatoko_TYPE(paetata_TYPE[paetata_whānuitanga], 1); 내보내기(132); 내보내기(paetata_whānuitanga); 내보내기(종류() == 306 ? 1 : 255); tūranga++;
            if (paetata_TYPE[paetata_whānuitanga] == 5) { 지역읽기(paetata_whānuitanga); 내보내기(146); tuhi_paetata(paetata_whānuitanga); }
        } else rahunga_uara("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        tono(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean putua_tohenga = 종류() == ')';
        int TYPE_uara = putua_tohenga ? 0 : kīanga_uara(); 요구(')'); 요구(';');
        String 서술 = TYPE_uara == 0 ? "()V" : TYPE_uara == 1 ? "(I)V" : TYPE_uara == 2 ? "(Z)V" : TYPE_uara == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_uara == 4 || TYPE_uara >= 6 || TYPE_uara == 0 && (!줄바꿈 || !putua_tohenga)) rahunga_uara("unsupported print argument");
        tono(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean tauākī_uara() {
        if (Pōhēhē) return false;
        if (깊이 > 32) { rahunga_uara("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!Pōhēhē && 종류() != '}') { if (반환) rahunga_uara("unreachable statement"); 반환 = tauākī_uara(); }
            요구('}'); for (int 수 = 0; 수 < paetata_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_uara = 종류() == ';' ? 0 : kīanga_uara(); manatoko_TYPE(TYPE_uara, 함수반환[현재함수]); 요구(';');
            내보내기(TYPE_uara == 0 ? 177 : TYPE_uara <= 2 || TYPE_uara == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); manatoko_TYPE(kīanga_uara(), 2); 요구(')'); int FALSE_uara = peka(153);
            깊이++; boolean 가 = mana_tauākī(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = peka(167); Hono_uara(FALSE_uara, CODE_rahi); 깊이++; boolean 나 = mana_tauākī(); 깊이--; Hono_uara(끝, CODE_rahi); return 가 && 나; }
            Hono_uara(FALSE_uara, CODE_rahi); return false;
        }
        if (TAKE_Word("while")) {
            int whakahaere = CODE_rahi; 요구('('); manatoko_TYPE(kīanga_uara(), 2); 요구(')'); int 끝 = peka(153);
            깊이++; mana_tauākī(); 깊이--; Hono_uara(peka(167), whakahaere); Hono_uara(끝, CODE_rahi); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') wehenga_mahi_uara(true); 요구(';');
            int here = CODE_rahi; if (종류() == ';') 내보내기(4); else manatoko_TYPE(kīanga_uara(), 2); 요구(';');
            int 끝 = peka(153), kuputuhi_tinana = peka(167), tāmata = CODE_rahi;
            if (종류() != ')') wehenga_mahi_uara(false); 요구(')'); Hono_uara(peka(167), here); Hono_uara(kuputuhi_tinana, CODE_rahi);
            mana_tauākī(); Hono_uara(peka(167), tāmata); Hono_uara(끝, CODE_rahi);
            for (int 수 = 0; 수 < paetata_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_uara(tūranga, "System")) { 화면출력(); return false; }
        if (종류() == 256 && tūranga + 1 < tohu_COUNT && (토큰종류[tūranga + 1] == '(' || 토큰종류[tūranga + 1] == '.')) {
            int TYPE_uara = kīanga_uara(); if (TYPE_uara != 0) 내보내기(87); 요구(';'); return false;
        }
        wehenga_mahi_uara(true); 요구(';'); return false;
    }
    static boolean mana_tauākī() {
        if (Word_uara(tūranga, "int") || Word_uara(tūranga, "boolean") || Word_uara(tūranga, "char") || Word_uara(tūranga, "String")
            || Word_uara(tūranga, "FileInputStream") || Word_uara(tūranga, "FileOutputStream")) rahunga_uara("local declaration requires braces");
        return tauākī_uara();
    }
    static void 출바(int uara) { if (출력크기 == 출력.length) rahunga_uara("class file too large"); else 출력[출력크기++] = uara & 255; }
    static void 출짧(int uara) { 출바(uara >> 8); 출바(uara); }
    static void 출정(int uara) { 출짧(uara >>> 16); 출짧(uara); }
    static void tuhi_tauaha() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(taimau_COUNT);
        for (int 수 = 0; 수 < taimau_rahi; 수++) 출바(taimau_uara[수]);
        출짧(0x21); 출짧(tauaha_taimau); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(aratuka_COUNT);
        for (int 수 = 0; 수 < aratuka_COUNT; 수++) {
            출짧(aratuka_uru[수]); 출짧(aratuka_ingoa_taimau[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_taimau);
            출정(12 + aratuka_roa[수]); 출짧(128); 출짧(함수지역[수]); 출정(aratuka_roa[수]);
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < aratuka_roa[수]; kāniwha_tāurunga++) 출바(CODE_uara[aratuka_CODE[수] + kāniwha_tāurunga]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int whakahaere() {
        if (kaiwhakamahi.인수개수() == 1 && 자바도구.같음(kaiwhakamahi.인수(0), "-version")) {
            kaiwhakamahi.Tuhia("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (kaiwhakamahi.인수개수() != 1) { kaiwhakamahi.Tuhia("Usage: javac FILE.java\n"); return 2; }
        int ingoa_rahi = 자바도구.Ingoa(kōnae_ingoa_TEXT, kaiwhakamahi.인수(0));
        if (ingoa_rahi < 6 || ingoa_rahi > 62 || kōnae_ingoa_TEXT[ingoa_rahi - 5] != '.' || kōnae_ingoa_TEXT[ingoa_rahi - 4] != 'j'
            || kōnae_ingoa_TEXT[ingoa_rahi - 3] != 'a' || kōnae_ingoa_TEXT[ingoa_rahi - 2] != 'v' || kōnae_ingoa_TEXT[ingoa_rahi - 1] != 'a') {
            kaiwhakamahi.Tuhia("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        pūtake_rahi = kaiwhakamahi.파일읽기(kōnae_ingoa_TEXT, pūtake);
        if (pūtake_rahi < 0) { kaiwhakamahi.Tuhia("javac: cannot read source: "); 자바도구.수쓰기(pūtake_rahi); kaiwhakamahi.tuhi_pūāhua_uara(10); return 1; }
        pūtake_rahi = 자바도구.원문해독(pūtake, pūtake_rahi);
        if (pūtake_rahi < 0) { kaiwhakamahi.Tuhia("javac error: invalid UTF-8 source\n"); return 1; }
        tapahi_uara(); if (!Pōhēhē) 선언읽기();
        if (!Pōhēhē) {
            if (tohu_roa[tauaha_tohu] != ingoa_rahi - 5) rahunga_uara("class name must match file name");
            for (int 수 = 0; 수 < ingoa_rahi - 5; 수++) if (pūtake[tohu_tūranga[tauaha_tohu] + 수] != kōnae_ingoa_TEXT[수]) rahunga_uara("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < aratuka_COUNT && !Pōhēhē; 현재함수++) {
            tūranga = 함수본문[현재함수]; aratuka_CODE[현재함수] = CODE_rahi; paetata_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < aratuka_tohenga_COUNT[현재함수]; 수++) tāpiri_paetata(aratuka_tohenga_ingoa[현재함수 * 16 + 수], aratuka_tohenga_TYPE[현재함수 * 16 + 수]);
            boolean 반환 = tauākī_uara();
            if (!반환 && 함수반환[현재함수] != 0) rahunga_uara("missing return");
            // peka 뒤의 합류 지점은 반드시 tūturu_raraunga 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean tau_tōpū = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(tau_tōpū ? 3 : 1); 내보내기(tau_tōpū ? 172 : 176); }
            if (tūranga != aratuka_mutu[현재함수]) rahunga_uara("invalid method body");
            함수지역[현재함수] = paetata_COUNT; aratuka_roa[현재함수] = CODE_rahi - aratuka_CODE[현재함수];
        }
        if (Pōhēhē) return 1;
        tuhi_tauaha(); if (Pōhēhē) return 1;
        kōnae_ingoa_TEXT[ingoa_rahi - 4] = 'c'; kōnae_ingoa_TEXT[ingoa_rahi - 3] = 'l'; kōnae_ingoa_TEXT[ingoa_rahi - 2] = 'a';
        kōnae_ingoa_TEXT[ingoa_rahi - 1] = 's'; kōnae_ingoa_TEXT[ingoa_rahi] = 's'; kōnae_ingoa_TEXT[ingoa_rahi + 1] = 0;
        int mēhua = kaiwhakamahi.tuhi_kōnae(kōnae_ingoa_TEXT, 출력, 출력크기);
        if (mēhua < 0) { kaiwhakamahi.Tuhia("javac: cannot save class: "); 자바도구.수쓰기(mēhua); kaiwhakamahi.tuhi_pūāhua_uara(10); return 1; }
        kaiwhakamahi.Tuhia("Compiled: "); for (int 수 = 0; kōnae_ingoa_TEXT[수] != 0; 수++) kaiwhakamahi.tuhi_pūāhua_uara(kōnae_ingoa_TEXT[수]);
        kaiwhakamahi.Tuhia(" (JVM class version 49)\n"); return 0;
    }
}
