// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java forrás_fa -> 표준 버전 49 class fordítóprogram. */
public final class 자바컴파일러 {
    static int[] FORRÁS = new int[16384], Kimenet = new int[16384], KÓD_ÉRTÉK = new int[4096];
    static int[] kód_Altípus = new int[2048], kód_pozíció = new int[2048], kód_hossz = new int[2048];
    static int[] állandó_ÉRTÉK = new int[4096], állandó_Ofszet = new int[512];
    static int[] 문자 = new int[512], fájlnév_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int forrás_méretez, kód_DARAB, Pozíció, KÓD_méretez, állandó_méretez, állandó_DARAB = 1, kimenet_méretez, karakter_hossz;
    static boolean HIBA;
    static int tanóra_kód, tanóra_állandó, szülő_állandó, KÓD_állandó;
    static int[] metódus_bejegyzés_név = new int[32], metódus_visszaküld = new int[32], metódus_argumentum_DARAB = new int[32];
    static int[] metódus_argumentum_név = new int[512], metódus_argumentum_beír = new int[512];
    static int[] metódus_törzs = new int[32], metódus_megszüntet = new int[32], metódus_KÓD = new int[32];
    static int[] metódus_hossz = new int[32], 함수지역 = new int[32], metódus_név_állandó = new int[32], 함수서술 = new int[32];
    static int[] metódus_hozzáfér = new int[32];
    static int metódus_DARAB, aktuális_metódus, helyi_DARAB, 깊이, 식깊이;
    static int[] helyi_név = new int[128], helyi_beír = new int[128], 지역깊이 = new int[128];

    static void hiba_ÉRTÉK(String 이유) {
        if (!HIBA) {
            felhasználó.Írás("javac error: "); felhasználó.Írás(이유);
            felhasználó.Írás(" at line ");
            int Vonal = 1, 끝 = Pozíció < kód_DARAB ? kód_pozíció[Pozíció] : forrás_méretez;
            for (int szám = 0; szám < 끝; szám++) if (FORRÁS[szám] == 10) Vonal++;
            자바도구.ír_szám(Vonal); felhasználó.ír_karakter_ÉRTÉK(10);
        }
        HIBA = true;
    }
    static boolean karakter_ÉRTÉK(int ÉRTÉK) { return 문자이름규칙.첫글자(ÉRTÉK); }
    static boolean számjegy_ÉRTÉK(int ÉRTÉK) { return ÉRTÉK >= '0' && ÉRTÉK <= '9'; }
    static boolean 이름같음(int 가, int MPERC_operandus) {
        if (가 < 0 || MPERC_operandus < 0 || 가 >= kód_DARAB || MPERC_operandus >= kód_DARAB || kód_hossz[가] != kód_hossz[MPERC_operandus]) return false;
        for (int szám = 0; szám < kód_hossz[가]; szám++) if (FORRÁS[kód_pozíció[가] + szám] != FORRÁS[kód_pozíció[MPERC_operandus] + szám]) return false;
        return true;
    }
    static boolean szó_ÉRTÉK(int kód_ÉRTÉK, String szó_SMS) {
        if (kód_ÉRTÉK < 0 || kód_ÉRTÉK >= kód_DARAB || kód_hossz[kód_ÉRTÉK] != szó_SMS.length()) return false;
        for (int szám = 0; szám < szó_SMS.length(); szám++) if (FORRÁS[kód_pozíció[kód_ÉRTÉK] + szám] != szó_SMS.charAt(szám)) return false;
        return true;
    }
    static int Altípus_ÉRTÉK() { return Pozíció < kód_DARAB ? kód_Altípus[Pozíció] : 0; }
    static boolean fogad(int ÉRTÉK) { if (Altípus_ÉRTÉK() != ÉRTÉK) return false; Pozíció++; return true; }
    static void követelmény_ÉRTÉK(int ÉRTÉK) { if (!fogad(ÉRTÉK)) hiba_ÉRTÉK("unexpected token"); }
    static boolean ÁTHELYEZ_szó(String szó_SMS) { if (!szó_ÉRTÉK(Pozíció, szó_SMS)) return false; Pozíció++; return true; }
    static void 말요구(String szó_SMS) { if (!ÁTHELYEZ_szó(szó_SMS)) hiba_ÉRTÉK(szó_SMS); }
    static int azonosító_ÉRTÉK() {
        int KR = Pozíció;
        if (Altípus_ÉRTÉK() != 256) hiba_ÉRTÉK("identifier required"); else Pozíció++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Futtatás = 0;
        for (int szám = 0; szám <= 예약어.length(); szám++) {
            if (szám == 예약어.length() || 예약어.charAt(szám) == ' ') {
                boolean 같음 = szám - Futtatás == kód_hossz[KR];
                for (int tárolóhely_bejegyzés = Futtatás; 같음 && tárolóhely_bejegyzés < szám; tárolóhely_bejegyzés++) if (예약어.charAt(tárolóhely_bejegyzés) != FORRÁS[kód_pozíció[KR] + tárolóhely_bejegyzés - Futtatás]) 같음 = false;
                if (같음) hiba_ÉRTÉK("reserved word cannot be an identifier");
                Futtatás = szám + 1;
            }
        }
        return KR;
    }
    static void vágás_ÉRTÉK() {
        int szám = 0;
        while (szám < forrás_méretez && !HIBA) {
            int ÉRTÉK = FORRÁS[szám], Futtatás = szám, Altípus_ÉRTÉK = ÉRTÉK;
            if (ÉRTÉK == 32 || ÉRTÉK == 9 || ÉRTÉK == 10 || ÉRTÉK == 13) { szám++; continue; }
            if (ÉRTÉK == '/' && szám + 1 < forrás_méretez && FORRÁS[szám + 1] == '/') {
                while (szám < forrás_méretez && FORRÁS[szám] != 10) szám++;
                continue;
            }
            if (ÉRTÉK == '/' && szám + 1 < forrás_méretez && FORRÁS[szám + 1] == '*') {
                szám += 2;
                while (szám + 1 < forrás_méretez && !(FORRÁS[szám] == '*' && FORRÁS[szám + 1] == '/')) szám++;
                if (szám + 1 >= forrás_méretez) { hiba_ÉRTÉK("unterminated comment"); break; }
                szám += 2; continue;
            }
            if (karakter_ÉRTÉK(ÉRTÉK)) { Altípus_ÉRTÉK = 256; while (szám < forrás_méretez && 문자이름규칙.이어진글자(FORRÁS[szám])) szám++; }
            else if (számjegy_ÉRTÉK(ÉRTÉK)) { Altípus_ÉRTÉK = 257; while (szám < forrás_méretez && számjegy_ÉRTÉK(FORRÁS[szám])) szám++; }
            else if (ÉRTÉK == '"' || ÉRTÉK == '\'') {
                Altípus_ÉRTÉK = ÉRTÉK == '"' ? 258 : 259; szám++;
                while (szám < forrás_méretez && FORRÁS[szám] != ÉRTÉK && FORRÁS[szám] != 10 && FORRÁS[szám] != 13) {
                    if (FORRÁS[szám] == '\\') szám++;
                    szám++;
                }
                if (szám >= forrás_méretez || FORRÁS[szám] != ÉRTÉK) { hiba_ÉRTÉK("unterminated literal"); break; }
                szám++;
            } else {
                szám++;
                if (szám < forrás_méretez) {
                    int Tovább_cikk = FORRÁS[szám];
                    if (ÉRTÉK == '=' && Tovább_cikk == '=') Altípus_ÉRTÉK = 300;
                    if (ÉRTÉK == '!' && Tovább_cikk == '=') Altípus_ÉRTÉK = 301;
                    if (ÉRTÉK == '<' && Tovább_cikk == '=') Altípus_ÉRTÉK = 302;
                    if (ÉRTÉK == '>' && Tovább_cikk == '=') Altípus_ÉRTÉK = 303;
                    if (ÉRTÉK == '&' && Tovább_cikk == '&') Altípus_ÉRTÉK = 304;
                    if (ÉRTÉK == '|' && Tovább_cikk == '|') Altípus_ÉRTÉK = 305;
                    if (ÉRTÉK == '+' && Tovább_cikk == '+') Altípus_ÉRTÉK = 306;
                    if (ÉRTÉK == '-' && Tovább_cikk == '-') Altípus_ÉRTÉK = 307;
                    if (ÉRTÉK == '+' && Tovább_cikk == '=') Altípus_ÉRTÉK = 308;
                    if (ÉRTÉK == '-' && Tovább_cikk == '=') Altípus_ÉRTÉK = 309;
                    if (ÉRTÉK == '*' && Tovább_cikk == '=') Altípus_ÉRTÉK = 310;
                    if (ÉRTÉK == '/' && Tovább_cikk == '=') Altípus_ÉRTÉK = 311;
                    if (ÉRTÉK == '%' && Tovább_cikk == '=') Altípus_ÉRTÉK = 312;
                    if (Altípus_ÉRTÉK >= 300) szám++;
                }
            }
            if (kód_DARAB == kód_Altípus.length - 1) { hiba_ÉRTÉK("too many tokens (2047 maximum)"); break; }
            kód_Altípus[kód_DARAB] = Altípus_ÉRTÉK; kód_pozíció[kód_DARAB] = Futtatás; kód_hossz[kód_DARAB++] = szám - Futtatás;
        }
    }
    static void ír_állandó_bájt(int ÉRTÉK) {
        if (állandó_méretez == állandó_ÉRTÉK.length) { hiba_ÉRTÉK("constant pool too large"); return; }
        állandó_ÉRTÉK[állandó_méretez++] = ÉRTÉK & 255;
    }
    static void 상짧(int ÉRTÉK) { ír_állandó_bájt(ÉRTÉK >> 8); ír_állandó_bájt(ÉRTÉK); }
    static int jegyzék_állandó(int Futtatás) {
        for (int szám = 1; szám < állandó_DARAB; szám++) {
            int elülső_kamera_ÉRTÉK = állandó_Ofszet[szám], hossz_ÉRTÉK = (szám + 1 < állandó_DARAB ? állandó_Ofszet[szám + 1] : Futtatás) - elülső_kamera_ÉRTÉK;
            if (hossz_ÉRTÉK != állandó_méretez - Futtatás) continue;
            boolean 같음 = true;
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < hossz_ÉRTÉK; tárolóhely_bejegyzés++) if (állandó_ÉRTÉK[elülső_kamera_ÉRTÉK + tárolóhely_bejegyzés] != állandó_ÉRTÉK[Futtatás + tárolóhely_bejegyzés]) 같음 = false;
            if (같음) { állandó_méretez = Futtatás; return szám; }
        }
        if (állandó_DARAB == állandó_Ofszet.length) { hiba_ÉRTÉK("too many constants"); return 0; }
        állandó_Ofszet[állandó_DARAB] = Futtatás;
        return állandó_DARAB++;
    }
    static void hozzáfűz_SMS(int ÉRTÉK) {
        if (karakter_hossz == 문자.length) { hiba_ÉRTÉK("text too long"); return; }
        문자[karakter_hossz++] = ÉRTÉK;
    }
    static void hozzáfűz_szó(String szó_SMS) { for (int szám = 0; szám < szó_SMS.length(); szám++) hozzáfűz_SMS(szó_SMS.charAt(szám)); }
    static int karakter_állandó() {
        int Futtatás = állandó_méretez; ír_állandó_bájt(1); 상짧(0);
        for (int szám = 0; szám < karakter_hossz; szám++) {
            int ÉRTÉK = 문자[szám];
            if (ÉRTÉK > 0 && ÉRTÉK < 128) ír_állandó_bájt(ÉRTÉK);
            else if (ÉRTÉK < 2048) { ír_állandó_bájt(192 | ÉRTÉK >> 6); ír_állandó_bájt(128 | ÉRTÉK & 63); }
            else { ír_állandó_bájt(224 | ÉRTÉK >> 12); ír_állandó_bájt(128 | ÉRTÉK >> 6 & 63); ír_állandó_bájt(128 | ÉRTÉK & 63); }
        }
        if (HIBA) return 0;
        int hossz_ÉRTÉK = állandó_méretez - Futtatás - 3;
        állandó_ÉRTÉK[Futtatás + 1] = hossz_ÉRTÉK >> 8; állandó_ÉRTÉK[Futtatás + 2] = hossz_ÉRTÉK & 255;
        return jegyzék_állandó(Futtatás);
    }
    static int szó_állandó(String szó_SMS) { karakter_hossz = 0; hozzáfűz_szó(szó_SMS); return karakter_állandó(); }
    static int kód_állandó(int kód_ÉRTÉK) {
        karakter_hossz = 0;
        for (int szám = 0; szám < kód_hossz[kód_ÉRTÉK]; szám++) hozzáfűz_SMS(FORRÁS[kód_pozíció[kód_ÉRTÉK] + szám]);
        return karakter_állandó();
    }
    static int hivatkozik(int Altípus_ÉRTÉK, int 가, int MPERC_operandus) {
        int Futtatás = állandó_méretez; ír_állandó_bájt(Altípus_ÉRTÉK); 상짧(가);
        if (Altípus_ÉRTÉK == 9 || Altípus_ÉRTÉK == 10 || Altípus_ÉRTÉK == 12) 상짧(MPERC_operandus);
        return jegyzék_állandó(Futtatás);
    }
    static int külső_hivatkozik(int Altípus_ÉRTÉK, String tulajdonos_ÉRTÉK, String Név, String 서술) {
        int tulajdonos_azonosító = hivatkozik(7, szó_állandó(tulajdonos_ÉRTÉK), 0);
        int név_DARAB = szó_állandó(Név), formáz_DARAB = szó_állandó(서술);
        return hivatkozik(Altípus_ÉRTÉK, tulajdonos_azonosító, hivatkozik(12, név_DARAB, formáz_DARAB));
    }
    static void 내보내기(int ÉRTÉK) {
        if (KÓD_méretez == KÓD_ÉRTÉK.length) { hiba_ÉRTÉK("bytecode too large"); return; }
        KÓD_ÉRTÉK[KÓD_méretez++] = ÉRTÉK & 255;
    }
    static void Parancs(int ÉRTÉK, int Argumentumok) { 내보내기(ÉRTÉK); 내보내기(Argumentumok >> 8); 내보내기(Argumentumok); }
    static void 수상수(int ÉRTÉK) {
        if (ÉRTÉK >= -1 && ÉRTÉK <= 5) { 내보내기(ÉRTÉK + 3); return; }
        int Futtatás = állandó_méretez; ír_állandó_bájt(3); 상짧(ÉRTÉK >>> 16); 상짧(ÉRTÉK);
        Parancs(19, jegyzék_állandó(Futtatás));
    }
    static int ág(int Parancs) { int KR = KÓD_méretez; Parancs(Parancs, 0); return KR; }
    static void csatol_ÉRTÉK(int ág, int cél_objektum) {
        if (HIBA) return;
        int 거리 = cél_objektum - ág;
        if (거리 < -32768 || 거리 > 32767 || ág < 0 || ág + 2 >= KÓD_méretez) { hiba_ÉRTÉK("invalid branch"); return; }
        KÓD_ÉRTÉK[ág + 1] = 거리 >> 8 & 255; KÓD_ÉRTÉK[ág + 2] = 거리 & 255;
    }
    static void Összehasonlítás_ÉRTÉK(int Parancs) {
        int IGAZ_ÉRTÉK = ág(Parancs); 내보내기(3); int 끝 = ág(167);
        csatol_ÉRTÉK(IGAZ_ÉRTÉK, KÓD_méretez); 내보내기(4); csatol_ÉRTÉK(끝, KÓD_méretez);
    }
    static int formáz_ÉRTÉK() {
        if (ÁTHELYEZ_szó("void")) return 0;
        if (ÁTHELYEZ_szó("int")) return 1;
        if (ÁTHELYEZ_szó("boolean")) return 2;
        if (ÁTHELYEZ_szó("char")) return 5;
        if (ÁTHELYEZ_szó("FileInputStream")) return 6;
        if (ÁTHELYEZ_szó("FileOutputStream")) return 7;
        if (ÁTHELYEZ_szó("String")) { if (fogad('[')) { követelmény_ÉRTÉK(']'); return 4; } return 3; }
        hiba_ÉRTÉK("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void hozzáad_formáz(int beír_ÉRTÉK) {
        if (beír_ÉRTÉK == 0) hozzáfűz_SMS('V');
        if (beír_ÉRTÉK == 1) hozzáfűz_SMS('I');
        if (beír_ÉRTÉK == 2) hozzáfűz_SMS('Z');
        if (beír_ÉRTÉK == 3) hozzáfűz_szó("Ljava/lang/String;");
        if (beír_ÉRTÉK == 4) hozzáfűz_szó("[Ljava/lang/String;");
        if (beír_ÉRTÉK == 5) hozzáfűz_SMS('C');
        if (beír_ÉRTÉK == 6) hozzáfűz_szó("Ljava/io/FileInputStream;");
        if (beír_ÉRTÉK == 7) hozzáfűz_szó("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws bevallás. kivétel folyamat_ÉRTÉK_bejegyzés 본문은 gazda javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = ÁTHELYEZ_szó("magyar");
        if (한국어묶음) { követelmény_ÉRTÉK('.'); 말요구("saját"); követelmény_ÉRTÉK('.'); }
        if (!한국어묶음 && (ÁTHELYEZ_szó("Exception") || ÁTHELYEZ_szó("IOException"))) return;
        if (ÁTHELYEZ_szó("kivétel") || ÁTHELYEZ_szó("végrehajtás_kivétel") || ÁTHELYEZ_szó("I_O_kivétel") || ÁTHELYEZ_szó("várj_IDŐTÚLLÉPÉS_kivétel") || ÁTHELYEZ_szó("CÍM_KERES_kivétel") || ÁTHELYEZ_szó("파일없음예외") || ÁTHELYEZ_szó("kommunikáció_kivétel") || ÁTHELYEZ_szó("alaptalan_argumentum_kivétel") || ÁTHELYEZ_szó("szám_formáz_hiba") || ÁTHELYEZ_szó("범위예외") || ÁTHELYEZ_szó("배열범위예외") || ÁTHELYEZ_szó("문자열범위예외") || ÁTHELYEZ_szó("null_hivatkozik_kivétel") || ÁTHELYEZ_szó("산술예외") || ÁTHELYEZ_szó("Állapot_kivétel") || ÁTHELYEZ_szó("beír_Átjátszás_kivétel") || ÁTHELYEZ_szó("음수배열크기예외") || ÁTHELYEZ_szó("TÖMB_tár_hiba") || ÁTHELYEZ_szó("szál_Állapot_kivétel") || ÁTHELYEZ_szó("대기중단예외")) return;
        hiba_ÉRTÉK("unsupported throws type");
    }
    static void 선언읽기() {
        while (ÁTHELYEZ_szó("import")) {
            if (szó_ÉRTÉK(Pozíció, "magyar")) 예외이름읽기();
            else {
                말요구("java"); követelmény_ÉRTÉK('.'); 말요구("io"); követelmény_ÉRTÉK('.');
                if (!(ÁTHELYEZ_szó("FileInputStream") || ÁTHELYEZ_szó("FileOutputStream") || ÁTHELYEZ_szó("IOException"))) hiba_ÉRTÉK("unsupported import");
            }
            követelmény_ÉRTÉK(';');
        }
        ÁTHELYEZ_szó("public"); ÁTHELYEZ_szó("final"); 말요구("class"); tanóra_kód = azonosító_ÉRTÉK();
        tanóra_állandó = hivatkozik(7, kód_állandó(tanóra_kód), 0);
        szülő_állandó = hivatkozik(7, szó_állandó("java/lang/Object"), 0); KÓD_állandó = szó_állandó("Code"); követelmény_ÉRTÉK('{');
        while (!HIBA && Altípus_ÉRTÉK() != '}') {
            if (metódus_DARAB == 32) { hiba_ÉRTÉK("too many methods"); break; }
            int hozzáfér_bejegyzés = ÁTHELYEZ_szó("public") ? 1 : ÁTHELYEZ_szó("private") ? 2 : 0; 말요구("static");
            int FÜGGVÉNY_ÉRTÉK = metódus_DARAB++;
            metódus_hozzáfér[FÜGGVÉNY_ÉRTÉK] = hozzáfér_bejegyzés | 8;
            metódus_visszaküld[FÜGGVÉNY_ÉRTÉK] = formáz_ÉRTÉK(); metódus_bejegyzés_név[FÜGGVÉNY_ÉRTÉK] = azonosító_ÉRTÉK(); követelmény_ÉRTÉK('(');
            for (int elülső_kamera_ÉRTÉK = 0; elülső_kamera_ÉRTÉK < FÜGGVÉNY_ÉRTÉK; elülső_kamera_ÉRTÉK++) if (이름같음(metódus_bejegyzés_név[elülső_kamera_ÉRTÉK], metódus_bejegyzés_név[FÜGGVÉNY_ÉRTÉK])) hiba_ÉRTÉK("duplicate method (overloading unsupported)");
            while (!HIBA && Altípus_ÉRTÉK() != ')') {
                int szám = metódus_argumentum_DARAB[FÜGGVÉNY_ÉRTÉK];
                if (szám == 16) { hiba_ÉRTÉK("too many parameters"); break; }
                int beír_ÉRTÉK = formáz_ÉRTÉK(); if (beír_ÉRTÉK == 0) hiba_ÉRTÉK("void parameter");
                metódus_argumentum_beír[FÜGGVÉNY_ÉRTÉK * 16 + szám] = beír_ÉRTÉK; metódus_argumentum_név[FÜGGVÉNY_ÉRTÉK * 16 + szám] = azonosító_ÉRTÉK();
                metódus_argumentum_DARAB[FÜGGVÉNY_ÉRTÉK]++;
                if (!fogad(',')) break;
            }
            követelmény_ÉRTÉK(')');
            if (ÁTHELYEZ_szó("throws")) {
                do { 예외이름읽기(); } while (!HIBA && fogad(','));
            }
            metódus_törzs[FÜGGVÉNY_ÉRTÉK] = Pozíció; követelmény_ÉRTÉK('{');
            int beágyazás_ÉRTÉK = 1;
            while (Pozíció < kód_DARAB && beágyazás_ÉRTÉK > 0) {
                if (Altípus_ÉRTÉK() == '{') beágyazás_ÉRTÉK++;
                if (Altípus_ÉRTÉK() == '}') beágyazás_ÉRTÉK--;
                Pozíció++;
            }
            if (beágyazás_ÉRTÉK != 0) hiba_ÉRTÉK("unclosed method body");
            metódus_megszüntet[FÜGGVÉNY_ÉRTÉK] = Pozíció;
            metódus_név_állandó[FÜGGVÉNY_ÉRTÉK] = kód_állandó(metódus_bejegyzés_név[FÜGGVÉNY_ÉRTÉK]);
            karakter_hossz = 0; hozzáfűz_SMS('(');
            for (int szám = 0; szám < metódus_argumentum_DARAB[FÜGGVÉNY_ÉRTÉK]; szám++) hozzáad_formáz(metódus_argumentum_beír[FÜGGVÉNY_ÉRTÉK * 16 + szám]);
            hozzáfűz_SMS(')'); hozzáad_formáz(metódus_visszaküld[FÜGGVÉNY_ÉRTÉK]); 함수서술[FÜGGVÉNY_ÉRTÉK] = karakter_állandó();
        }
        követelmény_ÉRTÉK('}'); if (Pozíció != kód_DARAB) hiba_ÉRTÉK("extra input after class");
    }
    static int keres_helyi(int Név) {
        for (int szám = helyi_DARAB - 1; szám >= 0; szám--) if (지역깊이[szám] >= 0 && 이름같음(helyi_név[szám], Név)) return szám;
        hiba_ÉRTÉK("unknown variable"); return 0;
    }
    static int hozzáad_helyi(int Név, int beír_ÉRTÉK) {
        for (int szám = 0; szám < helyi_DARAB; szám++) if (지역깊이[szám] >= 0 && 이름같음(helyi_név[szám], Név)) hiba_ÉRTÉK("duplicate local variable");
        if (helyi_DARAB == 128) { hiba_ÉRTÉK("too many locals"); return 0; }
        helyi_név[helyi_DARAB] = Név; helyi_beír[helyi_DARAB] = beír_ÉRTÉK; 지역깊이[helyi_DARAB] = 깊이;
        return helyi_DARAB++;
    }
    static boolean egész_szám_beír(int beír_ÉRTÉK) { return beír_ÉRTÉK == 1 || beír_ÉRTÉK == 5; }
    static void 지역읽기(int szám) { 내보내기(helyi_beír[szám] <= 2 || helyi_beír[szám] == 5 ? 21 : 25); 내보내기(szám); }
    static void ír_helyi(int szám) { 내보내기(helyi_beír[szám] <= 2 || helyi_beír[szám] == 5 ? 54 : 58); 내보내기(szám); }
    static void igazol_beír(int tényleges_adat, int 기대) { if (tényleges_adat != 기대 && !(tényleges_adat == 5 && 기대 == 1)) hiba_ÉRTÉK("type mismatch"); }
    static void 문자읽기(int kód_ÉRTÉK) {
        karakter_hossz = 0; int Futtatás = kód_pozíció[kód_ÉRTÉK] + 1, 끝 = kód_pozíció[kód_ÉRTÉK] + kód_hossz[kód_ÉRTÉK] - 1;
        while (Futtatás < 끝 && !HIBA) {
            int ÉRTÉK = FORRÁS[Futtatás++];
            if (ÉRTÉK == '\\') {
                if (Futtatás == 끝) { hiba_ÉRTÉK("invalid escape"); break; }
                ÉRTÉK = FORRÁS[Futtatás++];
                if (ÉRTÉK == 'n') ÉRTÉK = 10;
                else if (ÉRTÉK == 'r') ÉRTÉK = 13;
                else if (ÉRTÉK == 't') ÉRTÉK = 9;
                else if (ÉRTÉK == 'b') ÉRTÉK = 8;
                else if (ÉRTÉK == 'f') ÉRTÉK = 12;
                else if (ÉRTÉK != '\\' && ÉRTÉK != '"' && ÉRTÉK != '\'') hiba_ÉRTÉK("unsupported escape");
            }
            hozzáfűz_SMS(ÉRTÉK);
        }
    }
    static int elemez_egész_szám(int kód_ÉRTÉK, boolean 음수) {
        if (kód_hossz[kód_ÉRTÉK] > 1 && FORRÁS[kód_pozíció[kód_ÉRTÉK]] == '0') hiba_ÉRTÉK("octal literals unsupported");
        int ÉRTÉK = 0;
        for (int szám = 0; szám < kód_hossz[kód_ÉRTÉK]; szám++) {
            int számjegy_cikk = FORRÁS[kód_pozíció[kód_ÉRTÉK] + szám] - '0';
            if (ÉRTÉK < -214748364 || ÉRTÉK == -214748364 && számjegy_cikk > (음수 ? 8 : 7)) hiba_ÉRTÉK("integer literal out of range");
            ÉRTÉK = ÉRTÉK * 10 - számjegy_cikk;
        }
        return 음수 ? ÉRTÉK : -ÉRTÉK;
    }
    static int 기본식() {
        if (ÁTHELYEZ_szó("new")) {
            int beír_ÉRTÉK = formáz_ÉRTÉK();
            if (beír_ÉRTÉK != 6 && beír_ÉRTÉK != 7) { hiba_ÉRTÉK("only file streams supported by new in source"); return 0; }
            String tulajdonos_ÉRTÉK = beír_ÉRTÉK == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Parancs(187, hivatkozik(7, szó_állandó(tulajdonos_ÉRTÉK), 0)); 내보내기(89);
            követelmény_ÉRTÉK('('); igazol_beír(kifejezés_ÉRTÉK(), 3); boolean 이어 = false;
            if (fogad(',')) { if (beír_ÉRTÉK != 7) hiba_ÉRTÉK("input stream constructor arguments"); igazol_beír(kifejezés_ÉRTÉK(), 2); 이어 = true; }
            követelmény_ÉRTÉK(')');
            Parancs(183, külső_hivatkozik(10, tulajdonos_ÉRTÉK, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return beír_ÉRTÉK;
        }
        if (fogad('(')) { int beír_ÉRTÉK = kifejezés_ÉRTÉK(); követelmény_ÉRTÉK(')'); return beír_ÉRTÉK; }
        if (Altípus_ÉRTÉK() == 257) { 수상수(elemez_egész_szám(Pozíció++, false)); return 1; }
        if (Altípus_ÉRTÉK() == 258) { 문자읽기(Pozíció++); Parancs(19, hivatkozik(8, karakter_állandó(), 0)); return 3; }
        if (Altípus_ÉRTÉK() == 259) { 문자읽기(Pozíció++); if (karakter_hossz != 1) hiba_ÉRTÉK("character literal length"); 수상수(문자[0]); return 5; }
        if (ÁTHELYEZ_szó("true")) { 내보내기(4); return 2; }
        if (ÁTHELYEZ_szó("false")) { 내보내기(3); return 2; }
        if (ÁTHELYEZ_szó("magyar")) {
            követelmény_ÉRTÉK('.'); 말요구("saját"); követelmény_ÉRTÉK('.');
            String tulajdonos_ÉRTÉK = "", metódus_ÉRTÉK = "", 서술 = ""; int 가 = 0, MPERC_operandus = 0, 다 = 0, 라 = 0, 마 = 0, KR = 0;
            if (ÁTHELYEZ_szó("Kimenet")) {
                tulajdonos_ÉRTÉK = "magyar/saját/Kimenet"; követelmény_ÉRTÉK('.');
                if (ÁTHELYEZ_szó("ír_sor")) { metódus_ÉRTÉK = "ír_sor"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (ÁTHELYEZ_szó("Írás")) { metódus_ÉRTÉK = "Írás"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (ÁTHELYEZ_szó("ír_szám")) { metódus_ÉRTÉK = "ír_szám"; 서술 = "(I)V"; 가 = 1; }
                else hiba_ÉRTÉK("unknown Korean output method");
            } else if (ÁTHELYEZ_szó("문자")) {
                tulajdonos_ÉRTÉK = "magyar/saját/문자"; követelmény_ÉRTÉK('.'); 가 = 3;
                if (ÁTHELYEZ_szó("hossz_ÉRTÉK")) { metódus_ÉRTÉK = "hossz_ÉRTÉK"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (ÁTHELYEZ_szó("kódpont_DARAB")) { metódus_ÉRTÉK = "kódpont_DARAB"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (ÁTHELYEZ_szó("elemez_egész_szám")) { metódus_ÉRTÉK = "elemez_egész_szám"; 서술 = "(Ljava/lang/String;)I"; KR = 1; }
                else if (ÁTHELYEZ_szó("ír_egész_szám_ÉRTÉK")) { metódus_ÉRTÉK = "ír_egész_szám_ÉRTÉK"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; KR = 3; }
                else if (ÁTHELYEZ_szó("같음")) { metódus_ÉRTÉK = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; MPERC_operandus = 3; KR = 2; }
                else if (ÁTHELYEZ_szó("beilleszt_SMS")) { metódus_ÉRTÉK = "beilleszt_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; MPERC_operandus = 3; KR = 3; }
                else if (ÁTHELYEZ_szó("vágás_ÉRTÉK")) { metódus_ÉRTÉK = "vágás_ÉRTÉK"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; MPERC_operandus = 1; 다 = 1; KR = 3; }
                else hiba_ÉRTÉK("unknown Korean text method");
            } else if (ÁTHELYEZ_szó("Fájl")) {
                tulajdonos_ÉRTÉK = "magyar/saját/Fájl"; követelmény_ÉRTÉK('.'); 가 = 3;
                if (ÁTHELYEZ_szó("Olvasás")) { metódus_ÉRTÉK = "Olvasás"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; KR = 3; }
                else if (ÁTHELYEZ_szó("Írás")) { metódus_ÉRTÉK = "Írás"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; MPERC_operandus = 3; }
                else hiba_ÉRTÉK("unknown Korean file method");
            } else if (ÁTHELYEZ_szó("화면")) {
                tulajdonos_ÉRTÉK = "magyar/saját/화면"; követelmény_ÉRTÉK('.');
                if (ÁTHELYEZ_szó("너비")) { metódus_ÉRTÉK = "너비"; 서술 = "()I"; KR = 1; }
                else if (ÁTHELYEZ_szó("높이")) { metódus_ÉRTÉK = "높이"; 서술 = "()I"; KR = 1; }
                else if (ÁTHELYEZ_szó("téglalap")) { metódus_ÉRTÉK = "téglalap"; 서술 = "(IIIII)V"; 가 = 1; MPERC_operandus = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (ÁTHELYEZ_szó("töröl_bejegyzés")) { metódus_ÉRTÉK = "töröl_bejegyzés"; 서술 = "(I)V"; 가 = 1; }
                else if (ÁTHELYEZ_szó("기다리기")) { metódus_ÉRTÉK = "기다리기"; 서술 = "()V"; }
                else hiba_ÉRTÉK("unknown Korean framebuffer method");
            } else hiba_ÉRTÉK("unsupported Korean library class");
            követelmény_ÉRTÉK('('); if (가 != 0) igazol_beír(kifejezés_ÉRTÉK(), 가);
            if (MPERC_operandus != 0) { követelmény_ÉRTÉK(','); igazol_beír(kifejezés_ÉRTÉK(), MPERC_operandus); }
            if (다 != 0) { követelmény_ÉRTÉK(','); igazol_beír(kifejezés_ÉRTÉK(), 다); }
            if (라 != 0) { követelmény_ÉRTÉK(','); igazol_beír(kifejezés_ÉRTÉK(), 라); }
            if (마 != 0) { követelmény_ÉRTÉK(','); igazol_beír(kifejezés_ÉRTÉK(), 마); }
            követelmény_ÉRTÉK(')'); Parancs(184, külső_hivatkozik(10, tulajdonos_ÉRTÉK, metódus_ÉRTÉK, 서술)); return KR;
        }
        if (ÁTHELYEZ_szó("Integer")) {
            követelmény_ÉRTÉK('.'); 말요구("parseInt"); követelmény_ÉRTÉK('('); igazol_beír(kifejezés_ÉRTÉK(), 3); követelmény_ÉRTÉK(')');
            Parancs(184, külső_hivatkozik(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Név = azonosító_ÉRTÉK();
        if (fogad('(')) {
            int FÜGGVÉNY_ÉRTÉK = -1;
            for (int szám = 0; szám < metódus_DARAB; szám++) if (이름같음(Név, metódus_bejegyzés_név[szám])) FÜGGVÉNY_ÉRTÉK = szám;
            if (FÜGGVÉNY_ÉRTÉK < 0) { hiba_ÉRTÉK("unknown static method"); return 0; }
            int szám = 0;
            while (!HIBA && Altípus_ÉRTÉK() != ')') {
                if (szám >= metódus_argumentum_DARAB[FÜGGVÉNY_ÉRTÉK]) { hiba_ÉRTÉK("too many arguments"); break; }
                igazol_beír(kifejezés_ÉRTÉK(), metódus_argumentum_beír[FÜGGVÉNY_ÉRTÉK * 16 + szám++]); if (!fogad(',')) break;
            }
            követelmény_ÉRTÉK(')'); if (szám != metódus_argumentum_DARAB[FÜGGVÉNY_ÉRTÉK]) hiba_ÉRTÉK("argument count mismatch");
            Parancs(184, hivatkozik(10, tanóra_állandó, hivatkozik(12, metódus_név_állandó[FÜGGVÉNY_ÉRTÉK], 함수서술[FÜGGVÉNY_ÉRTÉK])));
            return metódus_visszaküld[FÜGGVÉNY_ÉRTÉK];
        }
        int helyi_hatókör = keres_helyi(Név), beír_ÉRTÉK = helyi_beír[helyi_hatókör]; 지역읽기(helyi_hatókör);
        while (!HIBA) {
            if (fogad('[')) { igazol_beír(beír_ÉRTÉK, 4); igazol_beír(kifejezés_ÉRTÉK(), 1); követelmény_ÉRTÉK(']'); 내보내기(50); beír_ÉRTÉK = 3; }
            else if (fogad('.')) {
                if (beír_ÉRTÉK == 6 || beír_ÉRTÉK == 7) {
                    String tulajdonos_ÉRTÉK = beír_ÉRTÉK == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (ÁTHELYEZ_szó("close")) { követelmény_ÉRTÉK('('); követelmény_ÉRTÉK(')'); Parancs(182, külső_hivatkozik(10, tulajdonos_ÉRTÉK, "close", "()V")); beír_ÉRTÉK = 0; }
                    else if (beír_ÉRTÉK == 6 && ÁTHELYEZ_szó("read")) { követelmény_ÉRTÉK('('); követelmény_ÉRTÉK(')'); Parancs(182, külső_hivatkozik(10, tulajdonos_ÉRTÉK, "read", "()I")); beír_ÉRTÉK = 1; }
                    else if (beír_ÉRTÉK == 7 && ÁTHELYEZ_szó("write")) { követelmény_ÉRTÉK('('); igazol_beír(kifejezés_ÉRTÉK(), 1); követelmény_ÉRTÉK(')'); Parancs(182, külső_hivatkozik(10, tulajdonos_ÉRTÉK, "write", "(I)V")); beír_ÉRTÉK = 0; }
                    else { hiba_ÉRTÉK("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (beír_ÉRTÉK == 4) { 내보내기(190); beír_ÉRTÉK = 1; }
                else { igazol_beír(beír_ÉRTÉK, 3); követelmény_ÉRTÉK('('); követelmény_ÉRTÉK(')'); Parancs(182, külső_hivatkozik(10, "java/lang/String", "length", "()I")); beír_ÉRTÉK = 1; }
            } else break;
        }
        return beír_ÉRTÉK;
    }
    static int 단항() {
        if (++식깊이 > 64) { hiba_ÉRTÉK("expression nesting too deep"); 식깊이--; return 0; }
        int beír_ÉRTÉK;
        if (fogad('!')) { igazol_beír(단항(), 2); Összehasonlítás_ÉRTÉK(153); beír_ÉRTÉK = 2; }
        else if (fogad('-')) {
            if (Altípus_ÉRTÉK() == 257) 수상수(elemez_egész_szám(Pozíció++, true));
            else { igazol_beír(단항(), 1); 내보내기(116); }
            beír_ÉRTÉK = 1;
        } else if (fogad('+')) { igazol_beír(단항(), 1); beír_ÉRTÉK = 1; }
        else beír_ÉRTÉK = 기본식();
        식깊이--; return beír_ÉRTÉK;
    }
    static int 곱식() {
        int beír_ÉRTÉK = 단항();
        while (!HIBA && (Altípus_ÉRTÉK() == '*' || Altípus_ÉRTÉK() == '/' || Altípus_ÉRTÉK() == '%')) {
            int kódolás_ÉRTÉK = Altípus_ÉRTÉK(); Pozíció++; igazol_beír(beír_ÉRTÉK, 1); igazol_beír(단항(), 1);
            내보내기(kódolás_ÉRTÉK == '*' ? 104 : kódolás_ÉRTÉK == '/' ? 108 : 112); beír_ÉRTÉK = 1;
        }
        return beír_ÉRTÉK;
    }
    static int 합식() {
        int beír_ÉRTÉK = 곱식();
        while (!HIBA && (Altípus_ÉRTÉK() == '+' || Altípus_ÉRTÉK() == '-')) {
            int kódolás_ÉRTÉK = Altípus_ÉRTÉK(); Pozíció++; int határ_ÉRTÉK = KÓD_méretez, BACK_értéktípus = 곱식();
            if (kódolás_ÉRTÉK == '+' && (beír_ÉRTÉK == 3 || BACK_értéktípus == 3)) { 결합(határ_ÉRTÉK, beír_ÉRTÉK, BACK_értéktípus); beír_ÉRTÉK = 3; }
            else { igazol_beír(beír_ÉRTÉK, 1); igazol_beír(BACK_értéktípus, 1); 내보내기(kódolás_ÉRTÉK == '+' ? 96 : 100); beír_ÉRTÉK = 1; }
        }
        return beír_ÉRTÉK;
    }
    static int csatlakoztatott_hivatkozik(int beír_ÉRTÉK) {
        if (beír_ÉRTÉK != 1 && beír_ÉRTÉK != 2 && beír_ÉRTÉK != 3 && beír_ÉRTÉK != 5) hiba_ÉRTÉK("unsupported concatenation type");
        return külső_hivatkozik(10, "java/lang/StringBuilder", "append", beír_ÉRTÉK == 1 ? "(I)Ljava/lang/StringBuilder;"
            : beír_ÉRTÉK == 2 ? "(Z)Ljava/lang/StringBuilder;" : beír_ÉRTÉK == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int határ_ÉRTÉK, int elülső_kamera_értéktípus, int BACK_értéktípus) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 jog KÓD_ÉRTÉK 앞에 generálás 코드를 삽입한다.
        // jog kifejezés_ÉRTÉK 내부의 társ_ÉRTÉK ág 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = KÓD_méretez;
        Parancs(187, hivatkozik(7, szó_állandó("java/lang/StringBuilder"), 0)); 내보내기(89);
        Parancs(183, külső_hivatkozik(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Parancs(182, csatlakoztatott_hivatkozik(elülső_kamera_értéktípus));
        if (HIBA) return;
        int hossz_ÉRTÉK = KÓD_méretez - 끝;
        for (int szám = 0; szám < hossz_ÉRTÉK; szám++) 삽입코드[szám] = KÓD_ÉRTÉK[끝 + szám];
        for (int szám = 끝 - 1; szám >= határ_ÉRTÉK; szám--) KÓD_ÉRTÉK[szám + hossz_ÉRTÉK] = KÓD_ÉRTÉK[szám];
        for (int szám = 0; szám < hossz_ÉRTÉK; szám++) KÓD_ÉRTÉK[határ_ÉRTÉK + szám] = 삽입코드[szám];
        Parancs(182, csatlakoztatott_hivatkozik(BACK_értéktípus)); Parancs(182, külső_hivatkozik(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Összehasonlítás_kifejezés() {
        int beír_ÉRTÉK = 합식();
        while (!HIBA && (Altípus_ÉRTÉK() == '<' || Altípus_ÉRTÉK() == '>' || Altípus_ÉRTÉK() == 302 || Altípus_ÉRTÉK() == 303)) {
            int kódolás_ÉRTÉK = Altípus_ÉRTÉK(); Pozíció++; igazol_beír(beír_ÉRTÉK, 1); igazol_beír(합식(), 1);
            Összehasonlítás_ÉRTÉK(kódolás_ÉRTÉK == '<' ? 161 : kódolás_ÉRTÉK == '>' ? 163 : kódolás_ÉRTÉK == 302 ? 164 : 162); beír_ÉRTÉK = 2;
        }
        return beír_ÉRTÉK;
    }
    static int 동등식() {
        int beír_ÉRTÉK = Összehasonlítás_kifejezés();
        while (!HIBA && (Altípus_ÉRTÉK() == 300 || Altípus_ÉRTÉK() == 301)) {
            int kódolás_ÉRTÉK = Altípus_ÉRTÉK(); Pozíció++; int BACK_értéktípus = Összehasonlítás_kifejezés();
            if (beír_ÉRTÉK == 0 || BACK_értéktípus == 0) hiba_ÉRTÉK("void expression");
            if (!(egész_szám_beír(beír_ÉRTÉK) && egész_szám_beír(BACK_értéktípus))) igazol_beír(BACK_értéktípus, beír_ÉRTÉK);
            Összehasonlítás_ÉRTÉK((beír_ÉRTÉK <= 2 || beír_ÉRTÉK == 5 ? 159 : 165) + (kódolás_ÉRTÉK == 301 ? 1 : 0)); beír_ÉRTÉK = 2;
        }
        return beír_ÉRTÉK;
    }
    static int AND() {
        int beír_ÉRTÉK = 동등식();
        while (!HIBA && fogad(304)) {
            igazol_beír(beír_ÉRTÉK, 2); int 가 = ág(153); igazol_beír(동등식(), 2); int MPERC_operandus = ág(153);
            내보내기(4); int 끝 = ág(167); csatol_ÉRTÉK(가, KÓD_méretez); csatol_ÉRTÉK(MPERC_operandus, KÓD_méretez); 내보내기(3); csatol_ÉRTÉK(끝, KÓD_méretez); beír_ÉRTÉK = 2;
        }
        return beír_ÉRTÉK;
    }
    static int kifejezés_ÉRTÉK() {
        int beír_ÉRTÉK = AND();
        while (!HIBA && fogad(305)) {
            igazol_beír(beír_ÉRTÉK, 2); int 가 = ág(154); igazol_beír(AND(), 2); int MPERC_operandus = ág(154);
            내보내기(3); int 끝 = ág(167); csatol_ÉRTÉK(가, KÓD_méretez); csatol_ÉRTÉK(MPERC_operandus, KÓD_méretez); 내보내기(4); csatol_ÉRTÉK(끝, KÓD_méretez); beír_ÉRTÉK = 2;
        }
        return beír_ÉRTÉK;
    }
    static void labor_ÉRTÉK(boolean engedélyez_bevallás) {
        if (szó_ÉRTÉK(Pozíció, "int") || szó_ÉRTÉK(Pozíció, "boolean") || szó_ÉRTÉK(Pozíció, "String") || szó_ÉRTÉK(Pozíció, "char")
            || szó_ÉRTÉK(Pozíció, "FileInputStream") || szó_ÉRTÉK(Pozíció, "FileOutputStream")) {
            if (!engedélyez_bevallás) hiba_ÉRTÉK("declaration not allowed here");
            int beír_ÉRTÉK = formáz_ÉRTÉK(), Név = azonosító_ÉRTÉK(); követelmény_ÉRTÉK('='); igazol_beír(kifejezés_ÉRTÉK(), beír_ÉRTÉK);
            ír_helyi(hozzáad_helyi(Név, beír_ÉRTÉK)); return;
        }
        int Név = azonosító_ÉRTÉK(), helyi_hatókör = keres_helyi(Név);
        if (fogad('=')) { igazol_beír(kifejezés_ÉRTÉK(), helyi_beír[helyi_hatókör]); ír_helyi(helyi_hatókör); }
        else if (Altípus_ÉRTÉK() >= 308 && Altípus_ÉRTÉK() <= 312) {
            int kódolás_ÉRTÉK = Altípus_ÉRTÉK(); Pozíció++; 지역읽기(helyi_hatókör); int határ_ÉRTÉK = KÓD_méretez, BACK_értéktípus = kifejezés_ÉRTÉK();
            if (kódolás_ÉRTÉK == 308 && helyi_beír[helyi_hatókör] == 3) 결합(határ_ÉRTÉK, 3, BACK_értéktípus);
            else {
                igazol_beír(helyi_beír[helyi_hatókör], 1); igazol_beír(BACK_értéktípus, 1);
                내보내기(kódolás_ÉRTÉK == 308 ? 96 : kódolás_ÉRTÉK == 309 ? 100 : kódolás_ÉRTÉK == 310 ? 104 : kódolás_ÉRTÉK == 311 ? 108 : 112);
                if (helyi_beír[helyi_hatókör] == 5) 내보내기(146);
            }
            ír_helyi(helyi_hatókör);
        }
        else if (Altípus_ÉRTÉK() == 306 || Altípus_ÉRTÉK() == 307) {
            igazol_beír(helyi_beír[helyi_hatókör], 1); 내보내기(132); 내보내기(helyi_hatókör); 내보내기(Altípus_ÉRTÉK() == 306 ? 1 : 255); Pozíció++;
            if (helyi_beír[helyi_hatókör] == 5) { 지역읽기(helyi_hatókör); 내보내기(146); ír_helyi(helyi_hatókör); }
        } else hiba_ÉRTÉK("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); követelmény_ÉRTÉK('.'); 말요구("out"); követelmény_ÉRTÉK('.');
        boolean 줄바꿈 = ÁTHELYEZ_szó("println"); if (!줄바꿈) 말요구("print"); követelmény_ÉRTÉK('(');
        Parancs(178, külső_hivatkozik(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean üres_argumentum = Altípus_ÉRTÉK() == ')';
        int beír_ÉRTÉK = üres_argumentum ? 0 : kifejezés_ÉRTÉK(); követelmény_ÉRTÉK(')'); követelmény_ÉRTÉK(';');
        String 서술 = beír_ÉRTÉK == 0 ? "()V" : beír_ÉRTÉK == 1 ? "(I)V" : beír_ÉRTÉK == 2 ? "(Z)V" : beír_ÉRTÉK == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (beír_ÉRTÉK == 4 || beír_ÉRTÉK >= 6 || beír_ÉRTÉK == 0 && (!줄바꿈 || !üres_argumentum)) hiba_ÉRTÉK("unsupported print argument");
        Parancs(182, külső_hivatkozik(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean utasítás_ÉRTÉK() {
        if (HIBA) return false;
        if (깊이 > 32) { hiba_ÉRTÉK("statement nesting too deep"); return false; }
        if (fogad('{')) {
            깊이++; boolean visszaküld_KR = false;
            while (!HIBA && Altípus_ÉRTÉK() != '}') { if (visszaküld_KR) hiba_ÉRTÉK("unreachable statement"); visszaküld_KR = utasítás_ÉRTÉK(); }
            követelmény_ÉRTÉK('}'); for (int szám = 0; szám < helyi_DARAB; szám++) if (지역깊이[szám] == 깊이) 지역깊이[szám] = -1;
            깊이--; return visszaküld_KR;
        }
        if (fogad(';')) return false;
        if (ÁTHELYEZ_szó("return")) {
            int beír_ÉRTÉK = Altípus_ÉRTÉK() == ';' ? 0 : kifejezés_ÉRTÉK(); igazol_beír(beír_ÉRTÉK, metódus_visszaküld[aktuális_metódus]); követelmény_ÉRTÉK(';');
            내보내기(beír_ÉRTÉK == 0 ? 177 : beír_ÉRTÉK <= 2 || beír_ÉRTÉK == 5 ? 172 : 176); return true;
        }
        if (ÁTHELYEZ_szó("if")) {
            követelmény_ÉRTÉK('('); igazol_beír(kifejezés_ÉRTÉK(), 2); követelmény_ÉRTÉK(')'); int HAMIS_ÉRTÉK = ág(153);
            깊이++; boolean 가 = vezérlő_utasítás(); 깊이--;
            if (ÁTHELYEZ_szó("else")) { int 끝 = ág(167); csatol_ÉRTÉK(HAMIS_ÉRTÉK, KÓD_méretez); 깊이++; boolean MPERC_operandus = vezérlő_utasítás(); 깊이--; csatol_ÉRTÉK(끝, KÓD_méretez); return 가 && MPERC_operandus; }
            csatol_ÉRTÉK(HAMIS_ÉRTÉK, KÓD_méretez); return false;
        }
        if (ÁTHELYEZ_szó("while")) {
            int Futtatás = KÓD_méretez; követelmény_ÉRTÉK('('); igazol_beír(kifejezés_ÉRTÉK(), 2); követelmény_ÉRTÉK(')'); int 끝 = ág(153);
            깊이++; vezérlő_utasítás(); 깊이--; csatol_ÉRTÉK(ág(167), Futtatás); csatol_ÉRTÉK(끝, KÓD_méretez); return false;
        }
        if (ÁTHELYEZ_szó("for")) {
            깊이++; követelmény_ÉRTÉK('('); if (Altípus_ÉRTÉK() != ';') labor_ÉRTÉK(true); követelmény_ÉRTÉK(';');
            int állapot = KÓD_méretez; if (Altípus_ÉRTÉK() == ';') 내보내기(4); else igazol_beír(kifejezés_ÉRTÉK(), 2); követelmény_ÉRTÉK(';');
            int 끝 = ág(153), törzsszöveg = ág(167), frissít = KÓD_méretez;
            if (Altípus_ÉRTÉK() != ')') labor_ÉRTÉK(false); követelmény_ÉRTÉK(')'); csatol_ÉRTÉK(ág(167), állapot); csatol_ÉRTÉK(törzsszöveg, KÓD_méretez);
            vezérlő_utasítás(); csatol_ÉRTÉK(ág(167), frissít); csatol_ÉRTÉK(끝, KÓD_méretez);
            for (int szám = 0; szám < helyi_DARAB; szám++) if (지역깊이[szám] == 깊이) 지역깊이[szám] = -1;
            깊이--; return false;
        }
        if (szó_ÉRTÉK(Pozíció, "System")) { 화면출력(); return false; }
        if (Altípus_ÉRTÉK() == 256 && Pozíció + 1 < kód_DARAB && (kód_Altípus[Pozíció + 1] == '(' || kód_Altípus[Pozíció + 1] == '.')) {
            int beír_ÉRTÉK = kifejezés_ÉRTÉK(); if (beír_ÉRTÉK != 0) 내보내기(87); követelmény_ÉRTÉK(';'); return false;
        }
        labor_ÉRTÉK(true); követelmény_ÉRTÉK(';'); return false;
    }
    static boolean vezérlő_utasítás() {
        if (szó_ÉRTÉK(Pozíció, "int") || szó_ÉRTÉK(Pozíció, "boolean") || szó_ÉRTÉK(Pozíció, "char") || szó_ÉRTÉK(Pozíció, "String")
            || szó_ÉRTÉK(Pozíció, "FileInputStream") || szó_ÉRTÉK(Pozíció, "FileOutputStream")) hiba_ÉRTÉK("local declaration requires braces");
        return utasítás_ÉRTÉK();
    }
    static void 출바(int ÉRTÉK) { if (kimenet_méretez == Kimenet.length) hiba_ÉRTÉK("class file too large"); else Kimenet[kimenet_méretez++] = ÉRTÉK & 255; }
    static void 출짧(int ÉRTÉK) { 출바(ÉRTÉK >> 8); 출바(ÉRTÉK); }
    static void 출정(int ÉRTÉK) { 출짧(ÉRTÉK >>> 16); 출짧(ÉRTÉK); }
    static void ír_tanóra() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(állandó_DARAB);
        for (int szám = 0; szám < állandó_méretez; szám++) 출바(állandó_ÉRTÉK[szám]);
        출짧(0x21); 출짧(tanóra_állandó); 출짧(szülő_állandó); 출짧(0); 출짧(0); 출짧(metódus_DARAB);
        for (int szám = 0; szám < metódus_DARAB; szám++) {
            출짧(metódus_hozzáfér[szám]); 출짧(metódus_név_állandó[szám]); 출짧(함수서술[szám]); 출짧(1); 출짧(KÓD_állandó);
            출정(12 + metódus_hossz[szám]); 출짧(128); 출짧(함수지역[szám]); 출정(metódus_hossz[szám]);
            for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < metódus_hossz[szám]; tárolóhely_bejegyzés++) 출바(KÓD_ÉRTÉK[metódus_KÓD[szám] + tárolóhely_bejegyzés]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Futtatás() {
        if (felhasználó.인수개수() == 1 && 자바도구.같음(felhasználó.Argumentumok(0), "-version")) {
            felhasználó.Írás("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (felhasználó.인수개수() != 1) { felhasználó.Írás("Usage: javac FILE.java\n"); return 2; }
        int név_méretez = 자바도구.Név(fájlnév_SMS, felhasználó.Argumentumok(0));
        if (név_méretez < 6 || név_méretez > 62 || fájlnév_SMS[név_méretez - 5] != '.' || fájlnév_SMS[név_méretez - 4] != 'j'
            || fájlnév_SMS[név_méretez - 3] != 'a' || fájlnév_SMS[név_méretez - 2] != 'v' || fájlnév_SMS[név_méretez - 1] != 'a') {
            felhasználó.Írás("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        forrás_méretez = felhasználó.파일읽기(fájlnév_SMS, FORRÁS);
        if (forrás_méretez < 0) { felhasználó.Írás("javac: cannot read source: "); 자바도구.ír_szám(forrás_méretez); felhasználó.ír_karakter_ÉRTÉK(10); return 1; }
        forrás_méretez = 자바도구.원문해독(FORRÁS, forrás_méretez);
        if (forrás_méretez < 0) { felhasználó.Írás("javac error: invalid UTF-8 source\n"); return 1; }
        vágás_ÉRTÉK(); if (!HIBA) 선언읽기();
        if (!HIBA) {
            if (kód_hossz[tanóra_kód] != név_méretez - 5) hiba_ÉRTÉK("class name must match file name");
            for (int szám = 0; szám < név_méretez - 5; szám++) if (FORRÁS[kód_pozíció[tanóra_kód] + szám] != fájlnév_SMS[szám]) hiba_ÉRTÉK("class name must match file name");
        }
        for (aktuális_metódus = 0; aktuális_metódus < metódus_DARAB && !HIBA; aktuális_metódus++) {
            Pozíció = metódus_törzs[aktuális_metódus]; metódus_KÓD[aktuális_metódus] = KÓD_méretez; helyi_DARAB = 0; 깊이 = 0;
            for (int szám = 0; szám < metódus_argumentum_DARAB[aktuális_metódus]; szám++) hozzáad_helyi(metódus_argumentum_név[aktuális_metódus * 16 + szám], metódus_argumentum_beír[aktuális_metódus * 16 + szám]);
            boolean visszaküld_KR = utasítás_ÉRTÉK();
            if (!visszaküld_KR && metódus_visszaküld[aktuális_metódus] != 0) hiba_ÉRTÉK("missing return");
            // ág 뒤의 합류 지점은 반드시 tényleges_adat 명령이어야 한다 (버전 49 검증기).
            if (metódus_visszaküld[aktuális_metódus] == 0) 내보내기(177);
            else { boolean egész_szám = metódus_visszaküld[aktuális_metódus] <= 2 || metódus_visszaküld[aktuális_metódus] == 5; 내보내기(egész_szám ? 3 : 1); 내보내기(egész_szám ? 172 : 176); }
            if (Pozíció != metódus_megszüntet[aktuális_metódus]) hiba_ÉRTÉK("invalid method body");
            함수지역[aktuális_metódus] = helyi_DARAB; metódus_hossz[aktuális_metódus] = KÓD_méretez - metódus_KÓD[aktuális_metódus];
        }
        if (HIBA) return 1;
        ír_tanóra(); if (HIBA) return 1;
        fájlnév_SMS[név_méretez - 4] = 'c'; fájlnév_SMS[név_méretez - 3] = 'l'; fájlnév_SMS[név_méretez - 2] = 'a';
        fájlnév_SMS[név_méretez - 1] = 's'; fájlnév_SMS[név_méretez] = 's'; fájlnév_SMS[név_méretez + 1] = 0;
        int KR = felhasználó.ír_Fájl(fájlnév_SMS, Kimenet, kimenet_méretez);
        if (KR < 0) { felhasználó.Írás("javac: cannot save class: "); 자바도구.ír_szám(KR); felhasználó.ír_karakter_ÉRTÉK(10); return 1; }
        felhasználó.Írás("Compiled: "); for (int szám = 0; fájlnév_SMS[szám] != 0; szám++) felhasználó.ír_karakter_ÉRTÉK(fájlnév_SMS[szám]);
        felhasználó.Írás(" (JVM class version 49)\n"); return 0;
    }
}
