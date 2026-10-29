// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java lähde_puu -> 표준 버전 49 class kääntäjä. */
public final class 자바컴파일러 {
    static int[] lähdetiedosto = new int[16384], tulostuspaikka = new int[16384], KOODI_ARVO = new int[4096];
    static int[] 토큰종류 = new int[2048], tunnus_toimi = new int[2048], tunnus_kesto = new int[2048];
    static int[] vakio_ARVO = new int[4096], vakio_SIIRTYMÄ = new int[512];
    static int[] 문자 = new int[512], tiedostonimi_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int lähde_muuttaa_kokoa, tunnus_LASKE, paikka, KOODI_muuttaa_kokoa, vakio_muuttaa_kokoa, vakio_LASKE = 1, tulos_muuttaa_kokoa, merkki_kesto;
    static boolean VIRHE;
    static int Luokka_tunnus, Luokka_vakio, pää_vakio, KOODI_vakio;
    static int[] menetelmä_merkintä_nimi = new int[32], menetelmä_palauttaa = new int[32], menetelmä_argumentti_LASKE = new int[32];
    static int[] menetelmä_argumentti_nimi = new int[512], menetelmä_argumentti_TYYPPI = new int[512];
    static int[] menetelmä_teksti = new int[32], menetelmä_lopettaa_puhelu = new int[32], menetelmä_KOODI = new int[32];
    static int[] menetelmä_kesto = new int[32], 함수지역 = new int[32], menetelmä_nimi_vakio = new int[32], 함수서술 = new int[32];
    static int[] menetelmä_pääsy = new int[32];
    static int menetelmä_LASKE, nykyinen_menetelmä, paikallinen_LASKE, 깊이, 식깊이;
    static int[] paikallinen_nimi = new int[128], paikallinen_TYYPPI = new int[128], 지역깊이 = new int[128];

    static void virhe_ARVO(String 이유) {
        if (!VIRHE) {
            käyttäjätila.Kirjoitus("javac error: "); käyttäjätila.Kirjoitus(이유);
            käyttäjätila.Kirjoitus(" at line ");
            int syöterivi = 1, 끝 = paikka < tunnus_LASKE ? tunnus_toimi[paikka] : lähde_muuttaa_kokoa;
            for (int numero = 0; numero < 끝; numero++) if (lähdetiedosto[numero] == 10) syöterivi++;
            자바도구.kirjoitus_numero(syöterivi); käyttäjätila.kirjoitus_merkki_ARVO(10);
        }
        VIRHE = true;
    }
    static boolean merkki_ARVO(int ARVO) { return 문자이름규칙.첫글자(ARVO); }
    static boolean numero_ARVO(int ARVO) { return ARVO >= '0' && ARVO <= '9'; }
    static boolean 이름같음(int 가, int SEKUNNIT_operandi) {
        if (가 < 0 || SEKUNNIT_operandi < 0 || 가 >= tunnus_LASKE || SEKUNNIT_operandi >= tunnus_LASKE || tunnus_kesto[가] != tunnus_kesto[SEKUNNIT_operandi]) return false;
        for (int numero = 0; numero < tunnus_kesto[가]; numero++) if (lähdetiedosto[tunnus_toimi[가] + numero] != lähdetiedosto[tunnus_toimi[SEKUNNIT_operandi] + numero]) return false;
        return true;
    }
    static boolean Word_ARVO(int tunnus_ARVO_eb540501, String Word_SMS) {
        if (tunnus_ARVO_eb540501 < 0 || tunnus_ARVO_eb540501 >= tunnus_LASKE || tunnus_kesto[tunnus_ARVO_eb540501] != Word_SMS.length()) return false;
        for (int numero = 0; numero < Word_SMS.length(); numero++) if (lähdetiedosto[tunnus_toimi[tunnus_ARVO_eb540501] + numero] != Word_SMS.charAt(numero)) return false;
        return true;
    }
    static int 종류() { return paikka < tunnus_LASKE ? 토큰종류[paikka] : 0; }
    static boolean saada(int ARVO) { if (종류() != ARVO) return false; paikka++; return true; }
    static void vaatimus_ARVO(int ARVO) { if (!saada(ARVO)) virhe_ARVO("unexpected token"); }
    static boolean OTA_Word(String Word_SMS) { if (!Word_ARVO(paikka, Word_SMS)) return false; paikka++; return true; }
    static void 말요구(String Word_SMS) { if (!OTA_Word(Word_SMS)) virhe_ARVO(Word_SMS); }
    static int tunniste_ARVO() {
        int TULOS = paikka;
        if (종류() != 256) virhe_ARVO("identifier required"); else paikka++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Suorita_2 = 0;
        for (int numero = 0; numero <= 예약어.length(); numero++) {
            if (numero == 예약어.length() || 예약어.charAt(numero) == ' ') {
                boolean 같음 = numero - Suorita_2 == tunnus_kesto[TULOS];
                for (int paikka_merkintä = Suorita_2; 같음 && paikka_merkintä < numero; paikka_merkintä++) if (예약어.charAt(paikka_merkintä) != lähdetiedosto[tunnus_toimi[TULOS] + paikka_merkintä - Suorita_2]) 같음 = false;
                if (같음) virhe_ARVO("reserved word cannot be an identifier");
                Suorita_2 = numero + 1;
            }
        }
        return TULOS;
    }
    static void leikata_ARVO_4601577b() {
        int numero = 0;
        while (numero < lähde_muuttaa_kokoa && !VIRHE) {
            int ARVO = lähdetiedosto[numero], Suorita_2 = numero, 종류 = ARVO;
            if (ARVO == 32 || ARVO == 9 || ARVO == 10 || ARVO == 13) { numero++; continue; }
            if (ARVO == '/' && numero + 1 < lähde_muuttaa_kokoa && lähdetiedosto[numero + 1] == '/') {
                while (numero < lähde_muuttaa_kokoa && lähdetiedosto[numero] != 10) numero++;
                continue;
            }
            if (ARVO == '/' && numero + 1 < lähde_muuttaa_kokoa && lähdetiedosto[numero + 1] == '*') {
                numero += 2;
                while (numero + 1 < lähde_muuttaa_kokoa && !(lähdetiedosto[numero] == '*' && lähdetiedosto[numero + 1] == '/')) numero++;
                if (numero + 1 >= lähde_muuttaa_kokoa) { virhe_ARVO("unterminated comment"); break; }
                numero += 2; continue;
            }
            if (merkki_ARVO(ARVO)) { 종류 = 256; while (numero < lähde_muuttaa_kokoa && 문자이름규칙.이어진글자(lähdetiedosto[numero])) numero++; }
            else if (numero_ARVO(ARVO)) { 종류 = 257; while (numero < lähde_muuttaa_kokoa && numero_ARVO(lähdetiedosto[numero])) numero++; }
            else if (ARVO == '"' || ARVO == '\'') {
                종류 = ARVO == '"' ? 258 : 259; numero++;
                while (numero < lähde_muuttaa_kokoa && lähdetiedosto[numero] != ARVO && lähdetiedosto[numero] != 10 && lähdetiedosto[numero] != 13) {
                    if (lähdetiedosto[numero] == '\\') numero++;
                    numero++;
                }
                if (numero >= lähde_muuttaa_kokoa || lähdetiedosto[numero] != ARVO) { virhe_ARVO("unterminated literal"); break; }
                numero++;
            } else {
                numero++;
                if (numero < lähde_muuttaa_kokoa) {
                    int Seuraava_kohde = lähdetiedosto[numero];
                    if (ARVO == '=' && Seuraava_kohde == '=') 종류 = 300;
                    if (ARVO == '!' && Seuraava_kohde == '=') 종류 = 301;
                    if (ARVO == '<' && Seuraava_kohde == '=') 종류 = 302;
                    if (ARVO == '>' && Seuraava_kohde == '=') 종류 = 303;
                    if (ARVO == '&' && Seuraava_kohde == '&') 종류 = 304;
                    if (ARVO == '|' && Seuraava_kohde == '|') 종류 = 305;
                    if (ARVO == '+' && Seuraava_kohde == '+') 종류 = 306;
                    if (ARVO == '-' && Seuraava_kohde == '-') 종류 = 307;
                    if (ARVO == '+' && Seuraava_kohde == '=') 종류 = 308;
                    if (ARVO == '-' && Seuraava_kohde == '=') 종류 = 309;
                    if (ARVO == '*' && Seuraava_kohde == '=') 종류 = 310;
                    if (ARVO == '/' && Seuraava_kohde == '=') 종류 = 311;
                    if (ARVO == '%' && Seuraava_kohde == '=') 종류 = 312;
                    if (종류 >= 300) numero++;
                }
            }
            if (tunnus_LASKE == 토큰종류.length - 1) { virhe_ARVO("too many tokens (2047 maximum)"); break; }
            토큰종류[tunnus_LASKE] = 종류; tunnus_toimi[tunnus_LASKE] = Suorita_2; tunnus_kesto[tunnus_LASKE++] = numero - Suorita_2;
        }
    }
    static void kirjoitus_vakio_tavu(int ARVO) {
        if (vakio_muuttaa_kokoa == vakio_ARVO.length) { virhe_ARVO("constant pool too large"); return; }
        vakio_ARVO[vakio_muuttaa_kokoa++] = ARVO & 255;
    }
    static void 상짧(int ARVO) { kirjoitus_vakio_tavu(ARVO >> 8); kirjoitus_vakio_tavu(ARVO); }
    static int rekisteri_vakio(int Suorita_2) {
        for (int numero = 1; numero < vakio_LASKE; numero++) {
            int etukamera_ARVO = vakio_SIIRTYMÄ[numero], kesto_ARVO = (numero + 1 < vakio_LASKE ? vakio_SIIRTYMÄ[numero + 1] : Suorita_2) - etukamera_ARVO;
            if (kesto_ARVO != vakio_muuttaa_kokoa - Suorita_2) continue;
            boolean 같음 = true;
            for (int paikka_merkintä = 0; paikka_merkintä < kesto_ARVO; paikka_merkintä++) if (vakio_ARVO[etukamera_ARVO + paikka_merkintä] != vakio_ARVO[Suorita_2 + paikka_merkintä]) 같음 = false;
            if (같음) { vakio_muuttaa_kokoa = Suorita_2; return numero; }
        }
        if (vakio_LASKE == vakio_SIIRTYMÄ.length) { virhe_ARVO("too many constants"); return 0; }
        vakio_SIIRTYMÄ[vakio_LASKE] = Suorita_2;
        return vakio_LASKE++;
    }
    static void liitä_SMS(int ARVO) {
        if (merkki_kesto == 문자.length) { virhe_ARVO("text too long"); return; }
        문자[merkki_kesto++] = ARVO;
    }
    static void liitä_Word(String Word_SMS) { for (int numero = 0; numero < Word_SMS.length(); numero++) liitä_SMS(Word_SMS.charAt(numero)); }
    static int merkki_vakio() {
        int Suorita_2 = vakio_muuttaa_kokoa; kirjoitus_vakio_tavu(1); 상짧(0);
        for (int numero = 0; numero < merkki_kesto; numero++) {
            int ARVO = 문자[numero];
            if (ARVO > 0 && ARVO < 128) kirjoitus_vakio_tavu(ARVO);
            else if (ARVO < 2048) { kirjoitus_vakio_tavu(192 | ARVO >> 6); kirjoitus_vakio_tavu(128 | ARVO & 63); }
            else { kirjoitus_vakio_tavu(224 | ARVO >> 12); kirjoitus_vakio_tavu(128 | ARVO >> 6 & 63); kirjoitus_vakio_tavu(128 | ARVO & 63); }
        }
        if (VIRHE) return 0;
        int kesto_ARVO = vakio_muuttaa_kokoa - Suorita_2 - 3;
        vakio_ARVO[Suorita_2 + 1] = kesto_ARVO >> 8; vakio_ARVO[Suorita_2 + 2] = kesto_ARVO & 255;
        return rekisteri_vakio(Suorita_2);
    }
    static int Word_vakio(String Word_SMS) { merkki_kesto = 0; liitä_Word(Word_SMS); return merkki_vakio(); }
    static int tunnus_vakio(int tunnus_ARVO_eb540501) {
        merkki_kesto = 0;
        for (int numero = 0; numero < tunnus_kesto[tunnus_ARVO_eb540501]; numero++) liitä_SMS(lähdetiedosto[tunnus_toimi[tunnus_ARVO_eb540501] + numero]);
        return merkki_vakio();
    }
    static int viite(int 종류, int 가, int SEKUNNIT_operandi) {
        int Suorita_2 = vakio_muuttaa_kokoa; kirjoitus_vakio_tavu(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(SEKUNNIT_operandi);
        return rekisteri_vakio(Suorita_2);
    }
    static int ulkoinen_viite(int 종류, String omistaja_ARVO, String Nimi, String 서술) {
        int omistaja_tunniste = viite(7, Word_vakio(omistaja_ARVO), 0);
        int nimi_LASKE = Word_vakio(Nimi), muoto_LASKE = Word_vakio(서술);
        return viite(종류, omistaja_tunniste, viite(12, nimi_LASKE, muoto_LASKE));
    }
    static void 내보내기(int ARVO) {
        if (KOODI_muuttaa_kokoa == KOODI_ARVO.length) { virhe_ARVO("bytecode too large"); return; }
        KOODI_ARVO[KOODI_muuttaa_kokoa++] = ARVO & 255;
    }
    static void komento(int ARVO, int argumentit) { 내보내기(ARVO); 내보내기(argumentit >> 8); 내보내기(argumentit); }
    static void 수상수(int ARVO) {
        if (ARVO >= -1 && ARVO <= 5) { 내보내기(ARVO + 3); return; }
        int Suorita_2 = vakio_muuttaa_kokoa; kirjoitus_vakio_tavu(3); 상짧(ARVO >>> 16); 상짧(ARVO);
        komento(19, rekisteri_vakio(Suorita_2));
    }
    static int haara(int komento) { int TULOS = KOODI_muuttaa_kokoa; komento(komento, 0); return TULOS; }
    static void Linkki_ARVO(int haara, int kohde_objekti) {
        if (VIRHE) return;
        int 거리 = kohde_objekti - haara;
        if (거리 < -32768 || 거리 > 32767 || haara < 0 || haara + 2 >= KOODI_muuttaa_kokoa) { virhe_ARVO("invalid branch"); return; }
        KOODI_ARVO[haara + 1] = 거리 >> 8 & 255; KOODI_ARVO[haara + 2] = 거리 & 255;
    }
    static void Vertailu_ARVO(int komento) {
        int TOSI_ARVO = haara(komento); 내보내기(3); int 끝 = haara(167);
        Linkki_ARVO(TOSI_ARVO, KOODI_muuttaa_kokoa); 내보내기(4); Linkki_ARVO(끝, KOODI_muuttaa_kokoa);
    }
    static int muoto_ARVO() {
        if (OTA_Word("void")) return 0;
        if (OTA_Word("int")) return 1;
        if (OTA_Word("boolean")) return 2;
        if (OTA_Word("char")) return 5;
        if (OTA_Word("FileInputStream")) return 6;
        if (OTA_Word("FileOutputStream")) return 7;
        if (OTA_Word("String")) { if (saada('[')) { vaatimus_ARVO(']'); return 4; } return 3; }
        virhe_ARVO("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Lisää_muoto(int TYYPPI_ARVO) {
        if (TYYPPI_ARVO == 0) liitä_SMS('V');
        if (TYYPPI_ARVO == 1) liitä_SMS('I');
        if (TYYPPI_ARVO == 2) liitä_SMS('Z');
        if (TYYPPI_ARVO == 3) liitä_Word("Ljava/lang/String;");
        if (TYYPPI_ARVO == 4) liitä_Word("[Ljava/lang/String;");
        if (TYYPPI_ARVO == 5) liitä_SMS('C');
        if (TYYPPI_ARVO == 6) liitä_Word("Ljava/io/FileInputStream;");
        if (TYYPPI_ARVO == 7) liitä_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws esittely. poikkeus prosessi_ARVO_merkintä 본문은 isäntä javac를 사용한다.
    static void lukea_poikkeus_nimi() {
        boolean 한국어묶음 = OTA_Word("suomi");
        if (한국어묶음) { vaatimus_ARVO('.'); 말요구("oma"); vaatimus_ARVO('.'); }
        if (!한국어묶음 && (OTA_Word("Exception") || OTA_Word("IOException"))) return;
        if (OTA_Word("poikkeus") || OTA_Word("suoritus_poikkeus") || OTA_Word("I_O_poikkeus") || OTA_Word("odottaa_AIKAKATKAISU_poikkeus") || OTA_Word("OSOITE_HAKU_poikkeus") || OTA_Word("파일없음예외") || OTA_Word("통신예외") || OTA_Word("pätemätön_argumentti_poikkeus") || OTA_Word("numero_muoto_virhe") || OTA_Word("범위예외") || OTA_Word("배열범위예외") || OTA_Word("문자열범위예외") || OTA_Word("TYHJÄ_viite_poikkeus") || OTA_Word("산술예외") || OTA_Word("Tila_poikkeus") || OTA_Word("TYYPPI_lähetys_poikkeus") || OTA_Word("음수배열크기예외") || OTA_Word("MATRIISI_Store_virhe") || OTA_Word("säie_Tila_poikkeus") || OTA_Word("대기중단예외")) return;
        virhe_ARVO("unsupported throws type");
    }
    static void lukea_esittely() {
        while (OTA_Word("import")) {
            if (Word_ARVO(paikka, "suomi")) lukea_poikkeus_nimi();
            else {
                말요구("java"); vaatimus_ARVO('.'); 말요구("io"); vaatimus_ARVO('.');
                if (!(OTA_Word("FileInputStream") || OTA_Word("FileOutputStream") || OTA_Word("IOException"))) virhe_ARVO("unsupported import");
            }
            vaatimus_ARVO(';');
        }
        OTA_Word("public"); OTA_Word("final"); 말요구("class"); Luokka_tunnus = tunniste_ARVO();
        Luokka_vakio = viite(7, tunnus_vakio(Luokka_tunnus), 0);
        pää_vakio = viite(7, Word_vakio("java/lang/Object"), 0); KOODI_vakio = Word_vakio("Code"); vaatimus_ARVO('{');
        while (!VIRHE && 종류() != '}') {
            if (menetelmä_LASKE == 32) { virhe_ARVO("too many methods"); break; }
            int pääsy_merkintä_68aed533 = OTA_Word("public") ? 1 : OTA_Word("private") ? 2 : 0; 말요구("static");
            int funktio_ARVO = menetelmä_LASKE++;
            menetelmä_pääsy[funktio_ARVO] = pääsy_merkintä_68aed533 | 8;
            menetelmä_palauttaa[funktio_ARVO] = muoto_ARVO(); menetelmä_merkintä_nimi[funktio_ARVO] = tunniste_ARVO(); vaatimus_ARVO('(');
            for (int etukamera_ARVO = 0; etukamera_ARVO < funktio_ARVO; etukamera_ARVO++) if (이름같음(menetelmä_merkintä_nimi[etukamera_ARVO], menetelmä_merkintä_nimi[funktio_ARVO])) virhe_ARVO("duplicate method (overloading unsupported)");
            while (!VIRHE && 종류() != ')') {
                int numero = menetelmä_argumentti_LASKE[funktio_ARVO];
                if (numero == 16) { virhe_ARVO("too many parameters"); break; }
                int TYYPPI_ARVO = muoto_ARVO(); if (TYYPPI_ARVO == 0) virhe_ARVO("void parameter");
                menetelmä_argumentti_TYYPPI[funktio_ARVO * 16 + numero] = TYYPPI_ARVO; menetelmä_argumentti_nimi[funktio_ARVO * 16 + numero] = tunniste_ARVO();
                menetelmä_argumentti_LASKE[funktio_ARVO]++;
                if (!saada(',')) break;
            }
            vaatimus_ARVO(')');
            if (OTA_Word("throws")) {
                do { lukea_poikkeus_nimi(); } while (!VIRHE && saada(','));
            }
            menetelmä_teksti[funktio_ARVO] = paikka; vaatimus_ARVO('{');
            int sisäkkäistäminen_ARVO = 1;
            while (paikka < tunnus_LASKE && sisäkkäistäminen_ARVO > 0) {
                if (종류() == '{') sisäkkäistäminen_ARVO++;
                if (종류() == '}') sisäkkäistäminen_ARVO--;
                paikka++;
            }
            if (sisäkkäistäminen_ARVO != 0) virhe_ARVO("unclosed method body");
            menetelmä_lopettaa_puhelu[funktio_ARVO] = paikka;
            menetelmä_nimi_vakio[funktio_ARVO] = tunnus_vakio(menetelmä_merkintä_nimi[funktio_ARVO]);
            merkki_kesto = 0; liitä_SMS('(');
            for (int numero = 0; numero < menetelmä_argumentti_LASKE[funktio_ARVO]; numero++) Lisää_muoto(menetelmä_argumentti_TYYPPI[funktio_ARVO * 16 + numero]);
            liitä_SMS(')'); Lisää_muoto(menetelmä_palauttaa[funktio_ARVO]); 함수서술[funktio_ARVO] = merkki_vakio();
        }
        vaatimus_ARVO('}'); if (paikka != tunnus_LASKE) virhe_ARVO("extra input after class");
    }
    static int ETSI_paikallinen(int Nimi) {
        for (int numero = paikallinen_LASKE - 1; numero >= 0; numero--) if (지역깊이[numero] >= 0 && 이름같음(paikallinen_nimi[numero], Nimi)) return numero;
        virhe_ARVO("unknown variable"); return 0;
    }
    static int Lisää_paikallinen(int Nimi, int TYYPPI_ARVO) {
        for (int numero = 0; numero < paikallinen_LASKE; numero++) if (지역깊이[numero] >= 0 && 이름같음(paikallinen_nimi[numero], Nimi)) virhe_ARVO("duplicate local variable");
        if (paikallinen_LASKE == 128) { virhe_ARVO("too many locals"); return 0; }
        paikallinen_nimi[paikallinen_LASKE] = Nimi; paikallinen_TYYPPI[paikallinen_LASKE] = TYYPPI_ARVO; 지역깊이[paikallinen_LASKE] = 깊이;
        return paikallinen_LASKE++;
    }
    static boolean kokonaisluku_TYYPPI(int TYYPPI_ARVO) { return TYYPPI_ARVO == 1 || TYYPPI_ARVO == 5; }
    static void lukea_paikallinen(int numero) { 내보내기(paikallinen_TYYPPI[numero] <= 2 || paikallinen_TYYPPI[numero] == 5 ? 21 : 25); 내보내기(numero); }
    static void kirjoitus_paikallinen(int numero) { 내보내기(paikallinen_TYYPPI[numero] <= 2 || paikallinen_TYYPPI[numero] == 5 ? 54 : 58); 내보내기(numero); }
    static void tarkistaa_TYYPPI(int todellinen_data, int 기대) { if (todellinen_data != 기대 && !(todellinen_data == 5 && 기대 == 1)) virhe_ARVO("type mismatch"); }
    static void lukea_merkki_ARVO(int tunnus_ARVO_eb540501) {
        merkki_kesto = 0; int Suorita_2 = tunnus_toimi[tunnus_ARVO_eb540501] + 1, 끝 = tunnus_toimi[tunnus_ARVO_eb540501] + tunnus_kesto[tunnus_ARVO_eb540501] - 1;
        while (Suorita_2 < 끝 && !VIRHE) {
            int ARVO = lähdetiedosto[Suorita_2++];
            if (ARVO == '\\') {
                if (Suorita_2 == 끝) { virhe_ARVO("invalid escape"); break; }
                ARVO = lähdetiedosto[Suorita_2++];
                if (ARVO == 'n') ARVO = 10;
                else if (ARVO == 'r') ARVO = 13;
                else if (ARVO == 't') ARVO = 9;
                else if (ARVO == 'b') ARVO = 8;
                else if (ARVO == 'f') ARVO = 12;
                else if (ARVO != '\\' && ARVO != '"' && ARVO != '\'') virhe_ARVO("unsupported escape");
            }
            liitä_SMS(ARVO);
        }
    }
    static int jäsentää_kokonaisluku(int tunnus_ARVO_eb540501, boolean 음수) {
        if (tunnus_kesto[tunnus_ARVO_eb540501] > 1 && lähdetiedosto[tunnus_toimi[tunnus_ARVO_eb540501]] == '0') virhe_ARVO("octal literals unsupported");
        int ARVO = 0;
        for (int numero = 0; numero < tunnus_kesto[tunnus_ARVO_eb540501]; numero++) {
            int numero_kohde = lähdetiedosto[tunnus_toimi[tunnus_ARVO_eb540501] + numero] - '0';
            if (ARVO < -214748364 || ARVO == -214748364 && numero_kohde > (음수 ? 8 : 7)) virhe_ARVO("integer literal out of range");
            ARVO = ARVO * 10 - numero_kohde;
        }
        return 음수 ? ARVO : -ARVO;
    }
    static int 기본식() {
        if (OTA_Word("new")) {
            int TYYPPI_ARVO = muoto_ARVO();
            if (TYYPPI_ARVO != 6 && TYYPPI_ARVO != 7) { virhe_ARVO("only file streams supported by new in source"); return 0; }
            String omistaja_ARVO = TYYPPI_ARVO == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            komento(187, viite(7, Word_vakio(omistaja_ARVO), 0)); 내보내기(89);
            vaatimus_ARVO('('); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 3); boolean 이어 = false;
            if (saada(',')) { if (TYYPPI_ARVO != 7) virhe_ARVO("input stream constructor arguments"); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 2); 이어 = true; }
            vaatimus_ARVO(')');
            komento(183, ulkoinen_viite(10, omistaja_ARVO, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYYPPI_ARVO;
        }
        if (saada('(')) { int TYYPPI_ARVO = lauseke_ARVO_eb3593ac(); vaatimus_ARVO(')'); return TYYPPI_ARVO; }
        if (종류() == 257) { 수상수(jäsentää_kokonaisluku(paikka++, false)); return 1; }
        if (종류() == 258) { lukea_merkki_ARVO(paikka++); komento(19, viite(8, merkki_vakio(), 0)); return 3; }
        if (종류() == 259) { lukea_merkki_ARVO(paikka++); if (merkki_kesto != 1) virhe_ARVO("character literal length"); 수상수(문자[0]); return 5; }
        if (OTA_Word("true")) { 내보내기(4); return 2; }
        if (OTA_Word("false")) { 내보내기(3); return 2; }
        if (OTA_Word("suomi")) {
            vaatimus_ARVO('.'); 말요구("oma"); vaatimus_ARVO('.');
            String omistaja_ARVO = "", menetelmä_ARVO = "", 서술 = ""; int 가 = 0, SEKUNNIT_operandi = 0, 다 = 0, 라 = 0, 마 = 0, TULOS = 0;
            if (OTA_Word("tulostuspaikka")) {
                omistaja_ARVO = "suomi/oma/tulostuspaikka"; vaatimus_ARVO('.');
                if (OTA_Word("kirjoitus_rivi")) { menetelmä_ARVO = "kirjoitus_rivi"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (OTA_Word("Kirjoitus")) { menetelmä_ARVO = "Kirjoitus"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (OTA_Word("kirjoitus_numero")) { menetelmä_ARVO = "kirjoitus_numero"; 서술 = "(I)V"; 가 = 1; }
                else virhe_ARVO("unknown Korean output method");
            } else if (OTA_Word("문자")) {
                omistaja_ARVO = "suomi/oma/문자"; vaatimus_ARVO('.'); 가 = 3;
                if (OTA_Word("kesto_ARVO")) { menetelmä_ARVO = "kesto_ARVO"; 서술 = "(Ljava/lang/String;)I"; TULOS = 1; }
                else if (OTA_Word("koodipiste_LASKE")) { menetelmä_ARVO = "koodipiste_LASKE"; 서술 = "(Ljava/lang/String;)I"; TULOS = 1; }
                else if (OTA_Word("jäsentää_kokonaisluku")) { menetelmä_ARVO = "jäsentää_kokonaisluku"; 서술 = "(Ljava/lang/String;)I"; TULOS = 1; }
                else if (OTA_Word("kirjoitus_kokonaisluku_ARVO")) { menetelmä_ARVO = "kirjoitus_kokonaisluku_ARVO"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; TULOS = 3; }
                else if (OTA_Word("같음")) { menetelmä_ARVO = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SEKUNNIT_operandi = 3; TULOS = 2; }
                else if (OTA_Word("liitä_SMS_ea0cc186")) { menetelmä_ARVO = "liitä_SMS_ea0cc186"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SEKUNNIT_operandi = 3; TULOS = 3; }
                else if (OTA_Word("leikata_ARVO_4601577b")) { menetelmä_ARVO = "leikata_ARVO_4601577b"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SEKUNNIT_operandi = 1; 다 = 1; TULOS = 3; }
                else virhe_ARVO("unknown Korean text method");
            } else if (OTA_Word("tiedoston_nimi")) {
                omistaja_ARVO = "suomi/oma/tiedoston_nimi"; vaatimus_ARVO('.'); 가 = 3;
                if (OTA_Word("Luku")) { menetelmä_ARVO = "Luku"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; TULOS = 3; }
                else if (OTA_Word("Kirjoitus")) { menetelmä_ARVO = "Kirjoitus"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SEKUNNIT_operandi = 3; }
                else virhe_ARVO("unknown Korean file method");
            } else if (OTA_Word("화면")) {
                omistaja_ARVO = "suomi/oma/화면"; vaatimus_ARVO('.');
                if (OTA_Word("너비")) { menetelmä_ARVO = "너비"; 서술 = "()I"; TULOS = 1; }
                else if (OTA_Word("높이")) { menetelmä_ARVO = "높이"; 서술 = "()I"; TULOS = 1; }
                else if (OTA_Word("suorakulmio")) { menetelmä_ARVO = "suorakulmio"; 서술 = "(IIIII)V"; 가 = 1; SEKUNNIT_operandi = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (OTA_Word("poistaa_merkintä_c8dbc399")) { menetelmä_ARVO = "poistaa_merkintä_c8dbc399"; 서술 = "(I)V"; 가 = 1; }
                else if (OTA_Word("기다리기")) { menetelmä_ARVO = "기다리기"; 서술 = "()V"; }
                else virhe_ARVO("unknown Korean framebuffer method");
            } else virhe_ARVO("unsupported Korean library class");
            vaatimus_ARVO('('); if (가 != 0) tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 가);
            if (SEKUNNIT_operandi != 0) { vaatimus_ARVO(','); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), SEKUNNIT_operandi); }
            if (다 != 0) { vaatimus_ARVO(','); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 다); }
            if (라 != 0) { vaatimus_ARVO(','); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 라); }
            if (마 != 0) { vaatimus_ARVO(','); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 마); }
            vaatimus_ARVO(')'); komento(184, ulkoinen_viite(10, omistaja_ARVO, menetelmä_ARVO, 서술)); return TULOS;
        }
        if (OTA_Word("Integer")) {
            vaatimus_ARVO('.'); 말요구("parseInt"); vaatimus_ARVO('('); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 3); vaatimus_ARVO(')');
            komento(184, ulkoinen_viite(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nimi = tunniste_ARVO();
        if (saada('(')) {
            int funktio_ARVO = -1;
            for (int numero = 0; numero < menetelmä_LASKE; numero++) if (이름같음(Nimi, menetelmä_merkintä_nimi[numero])) funktio_ARVO = numero;
            if (funktio_ARVO < 0) { virhe_ARVO("unknown static method"); return 0; }
            int numero = 0;
            while (!VIRHE && 종류() != ')') {
                if (numero >= menetelmä_argumentti_LASKE[funktio_ARVO]) { virhe_ARVO("too many arguments"); break; }
                tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), menetelmä_argumentti_TYYPPI[funktio_ARVO * 16 + numero++]); if (!saada(',')) break;
            }
            vaatimus_ARVO(')'); if (numero != menetelmä_argumentti_LASKE[funktio_ARVO]) virhe_ARVO("argument count mismatch");
            komento(184, viite(10, Luokka_vakio, viite(12, menetelmä_nimi_vakio[funktio_ARVO], 함수서술[funktio_ARVO])));
            return menetelmä_palauttaa[funktio_ARVO];
        }
        int paikallinen_laajuus = ETSI_paikallinen(Nimi), TYYPPI_ARVO = paikallinen_TYYPPI[paikallinen_laajuus]; lukea_paikallinen(paikallinen_laajuus);
        while (!VIRHE) {
            if (saada('[')) { tarkistaa_TYYPPI(TYYPPI_ARVO, 4); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 1); vaatimus_ARVO(']'); 내보내기(50); TYYPPI_ARVO = 3; }
            else if (saada('.')) {
                if (TYYPPI_ARVO == 6 || TYYPPI_ARVO == 7) {
                    String omistaja_ARVO = TYYPPI_ARVO == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (OTA_Word("close")) { vaatimus_ARVO('('); vaatimus_ARVO(')'); komento(182, ulkoinen_viite(10, omistaja_ARVO, "close", "()V")); TYYPPI_ARVO = 0; }
                    else if (TYYPPI_ARVO == 6 && OTA_Word("read")) { vaatimus_ARVO('('); vaatimus_ARVO(')'); komento(182, ulkoinen_viite(10, omistaja_ARVO, "read", "()I")); TYYPPI_ARVO = 1; }
                    else if (TYYPPI_ARVO == 7 && OTA_Word("write")) { vaatimus_ARVO('('); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 1); vaatimus_ARVO(')'); komento(182, ulkoinen_viite(10, omistaja_ARVO, "write", "(I)V")); TYYPPI_ARVO = 0; }
                    else { virhe_ARVO("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYYPPI_ARVO == 4) { 내보내기(190); TYYPPI_ARVO = 1; }
                else { tarkistaa_TYYPPI(TYYPPI_ARVO, 3); vaatimus_ARVO('('); vaatimus_ARVO(')'); komento(182, ulkoinen_viite(10, "java/lang/String", "length", "()I")); TYYPPI_ARVO = 1; }
            } else break;
        }
        return TYYPPI_ARVO;
    }
    static int 단항() {
        if (++식깊이 > 64) { virhe_ARVO("expression nesting too deep"); 식깊이--; return 0; }
        int TYYPPI_ARVO;
        if (saada('!')) { tarkistaa_TYYPPI(단항(), 2); Vertailu_ARVO(153); TYYPPI_ARVO = 2; }
        else if (saada('-')) {
            if (종류() == 257) 수상수(jäsentää_kokonaisluku(paikka++, true));
            else { tarkistaa_TYYPPI(단항(), 1); 내보내기(116); }
            TYYPPI_ARVO = 1;
        } else if (saada('+')) { tarkistaa_TYYPPI(단항(), 1); TYYPPI_ARVO = 1; }
        else TYYPPI_ARVO = 기본식();
        식깊이--; return TYYPPI_ARVO;
    }
    static int 곱식() {
        int TYYPPI_ARVO = 단항();
        while (!VIRHE && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int koodaus_ARVO = 종류(); paikka++; tarkistaa_TYYPPI(TYYPPI_ARVO, 1); tarkistaa_TYYPPI(단항(), 1);
            내보내기(koodaus_ARVO == '*' ? 104 : koodaus_ARVO == '/' ? 108 : 112); TYYPPI_ARVO = 1;
        }
        return TYYPPI_ARVO;
    }
    static int 합식() {
        int TYYPPI_ARVO = 곱식();
        while (!VIRHE && (종류() == '+' || 종류() == '-')) {
            int koodaus_ARVO = 종류(); paikka++; int rajattu_alue_ARVO = KOODI_muuttaa_kokoa, BACK_arvon_tyyppi = 곱식();
            if (koodaus_ARVO == '+' && (TYYPPI_ARVO == 3 || BACK_arvon_tyyppi == 3)) { 결합(rajattu_alue_ARVO, TYYPPI_ARVO, BACK_arvon_tyyppi); TYYPPI_ARVO = 3; }
            else { tarkistaa_TYYPPI(TYYPPI_ARVO, 1); tarkistaa_TYYPPI(BACK_arvon_tyyppi, 1); 내보내기(koodaus_ARVO == '+' ? 96 : 100); TYYPPI_ARVO = 1; }
        }
        return TYYPPI_ARVO;
    }
    static int liitetty_viite(int TYYPPI_ARVO) {
        if (TYYPPI_ARVO != 1 && TYYPPI_ARVO != 2 && TYYPPI_ARVO != 3 && TYYPPI_ARVO != 5) virhe_ARVO("unsupported concatenation type");
        return ulkoinen_viite(10, "java/lang/StringBuilder", "append", TYYPPI_ARVO == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYYPPI_ARVO == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYYPPI_ARVO == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int rajattu_alue_ARVO, int etukamera_arvon_tyyppi, int BACK_arvon_tyyppi) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 OIKEA KOODI_ARVO 앞에 generoida 코드를 삽입한다.
        // OIKEA lauseke_ARVO_eb3593ac 내부의 vertaissolmu_ARVO haara 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = KOODI_muuttaa_kokoa;
        komento(187, viite(7, Word_vakio("java/lang/StringBuilder"), 0)); 내보내기(89);
        komento(183, ulkoinen_viite(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); komento(182, liitetty_viite(etukamera_arvon_tyyppi));
        if (VIRHE) return;
        int kesto_ARVO = KOODI_muuttaa_kokoa - 끝;
        for (int numero = 0; numero < kesto_ARVO; numero++) 삽입코드[numero] = KOODI_ARVO[끝 + numero];
        for (int numero = 끝 - 1; numero >= rajattu_alue_ARVO; numero--) KOODI_ARVO[numero + kesto_ARVO] = KOODI_ARVO[numero];
        for (int numero = 0; numero < kesto_ARVO; numero++) KOODI_ARVO[rajattu_alue_ARVO + numero] = 삽입코드[numero];
        komento(182, liitetty_viite(BACK_arvon_tyyppi)); komento(182, ulkoinen_viite(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Vertailu_lauseke() {
        int TYYPPI_ARVO = 합식();
        while (!VIRHE && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int koodaus_ARVO = 종류(); paikka++; tarkistaa_TYYPPI(TYYPPI_ARVO, 1); tarkistaa_TYYPPI(합식(), 1);
            Vertailu_ARVO(koodaus_ARVO == '<' ? 161 : koodaus_ARVO == '>' ? 163 : koodaus_ARVO == 302 ? 164 : 162); TYYPPI_ARVO = 2;
        }
        return TYYPPI_ARVO;
    }
    static int 동등식() {
        int TYYPPI_ARVO = Vertailu_lauseke();
        while (!VIRHE && (종류() == 300 || 종류() == 301)) {
            int koodaus_ARVO = 종류(); paikka++; int BACK_arvon_tyyppi = Vertailu_lauseke();
            if (TYYPPI_ARVO == 0 || BACK_arvon_tyyppi == 0) virhe_ARVO("void expression");
            if (!(kokonaisluku_TYYPPI(TYYPPI_ARVO) && kokonaisluku_TYYPPI(BACK_arvon_tyyppi))) tarkistaa_TYYPPI(BACK_arvon_tyyppi, TYYPPI_ARVO);
            Vertailu_ARVO((TYYPPI_ARVO <= 2 || TYYPPI_ARVO == 5 ? 159 : 165) + (koodaus_ARVO == 301 ? 1 : 0)); TYYPPI_ARVO = 2;
        }
        return TYYPPI_ARVO;
    }
    static int AND() {
        int TYYPPI_ARVO = 동등식();
        while (!VIRHE && saada(304)) {
            tarkistaa_TYYPPI(TYYPPI_ARVO, 2); int 가 = haara(153); tarkistaa_TYYPPI(동등식(), 2); int SEKUNNIT_operandi = haara(153);
            내보내기(4); int 끝 = haara(167); Linkki_ARVO(가, KOODI_muuttaa_kokoa); Linkki_ARVO(SEKUNNIT_operandi, KOODI_muuttaa_kokoa); 내보내기(3); Linkki_ARVO(끝, KOODI_muuttaa_kokoa); TYYPPI_ARVO = 2;
        }
        return TYYPPI_ARVO;
    }
    static int lauseke_ARVO_eb3593ac() {
        int TYYPPI_ARVO = AND();
        while (!VIRHE && saada(305)) {
            tarkistaa_TYYPPI(TYYPPI_ARVO, 2); int 가 = haara(154); tarkistaa_TYYPPI(AND(), 2); int SEKUNNIT_operandi = haara(154);
            내보내기(3); int 끝 = haara(167); Linkki_ARVO(가, KOODI_muuttaa_kokoa); Linkki_ARVO(SEKUNNIT_operandi, KOODI_muuttaa_kokoa); 내보내기(4); Linkki_ARVO(끝, KOODI_muuttaa_kokoa); TYYPPI_ARVO = 2;
        }
        return TYYPPI_ARVO;
    }
    static void tehtävä_ARVO(boolean Salli_esittely) {
        if (Word_ARVO(paikka, "int") || Word_ARVO(paikka, "boolean") || Word_ARVO(paikka, "String") || Word_ARVO(paikka, "char")
            || Word_ARVO(paikka, "FileInputStream") || Word_ARVO(paikka, "FileOutputStream")) {
            if (!Salli_esittely) virhe_ARVO("declaration not allowed here");
            int TYYPPI_ARVO = muoto_ARVO(), Nimi = tunniste_ARVO(); vaatimus_ARVO('='); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), TYYPPI_ARVO);
            kirjoitus_paikallinen(Lisää_paikallinen(Nimi, TYYPPI_ARVO)); return;
        }
        int Nimi = tunniste_ARVO(), paikallinen_laajuus = ETSI_paikallinen(Nimi);
        if (saada('=')) { tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), paikallinen_TYYPPI[paikallinen_laajuus]); kirjoitus_paikallinen(paikallinen_laajuus); }
        else if (종류() >= 308 && 종류() <= 312) {
            int koodaus_ARVO = 종류(); paikka++; lukea_paikallinen(paikallinen_laajuus); int rajattu_alue_ARVO = KOODI_muuttaa_kokoa, BACK_arvon_tyyppi = lauseke_ARVO_eb3593ac();
            if (koodaus_ARVO == 308 && paikallinen_TYYPPI[paikallinen_laajuus] == 3) 결합(rajattu_alue_ARVO, 3, BACK_arvon_tyyppi);
            else {
                tarkistaa_TYYPPI(paikallinen_TYYPPI[paikallinen_laajuus], 1); tarkistaa_TYYPPI(BACK_arvon_tyyppi, 1);
                내보내기(koodaus_ARVO == 308 ? 96 : koodaus_ARVO == 309 ? 100 : koodaus_ARVO == 310 ? 104 : koodaus_ARVO == 311 ? 108 : 112);
                if (paikallinen_TYYPPI[paikallinen_laajuus] == 5) 내보내기(146);
            }
            kirjoitus_paikallinen(paikallinen_laajuus);
        }
        else if (종류() == 306 || 종류() == 307) {
            tarkistaa_TYYPPI(paikallinen_TYYPPI[paikallinen_laajuus], 1); 내보내기(132); 내보내기(paikallinen_laajuus); 내보내기(종류() == 306 ? 1 : 255); paikka++;
            if (paikallinen_TYYPPI[paikallinen_laajuus] == 5) { lukea_paikallinen(paikallinen_laajuus); 내보내기(146); kirjoitus_paikallinen(paikallinen_laajuus); }
        } else virhe_ARVO("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); vaatimus_ARVO('.'); 말요구("out"); vaatimus_ARVO('.');
        boolean 줄바꿈 = OTA_Word("println"); if (!줄바꿈) 말요구("print"); vaatimus_ARVO('(');
        komento(178, ulkoinen_viite(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean 빈인수 = 종류() == ')';
        int TYYPPI_ARVO = 빈인수 ? 0 : lauseke_ARVO_eb3593ac(); vaatimus_ARVO(')'); vaatimus_ARVO(';');
        String 서술 = TYYPPI_ARVO == 0 ? "()V" : TYYPPI_ARVO == 1 ? "(I)V" : TYYPPI_ARVO == 2 ? "(Z)V" : TYYPPI_ARVO == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYYPPI_ARVO == 4 || TYYPPI_ARVO >= 6 || TYYPPI_ARVO == 0 && (!줄바꿈 || !빈인수)) virhe_ARVO("unsupported print argument");
        komento(182, ulkoinen_viite(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean lauseke_ARVO() {
        if (VIRHE) return false;
        if (깊이 > 32) { virhe_ARVO("statement nesting too deep"); return false; }
        if (saada('{')) {
            깊이++; boolean palauttaa_KR = false;
            while (!VIRHE && 종류() != '}') { if (palauttaa_KR) virhe_ARVO("unreachable statement"); palauttaa_KR = lauseke_ARVO(); }
            vaatimus_ARVO('}'); for (int numero = 0; numero < paikallinen_LASKE; numero++) if (지역깊이[numero] == 깊이) 지역깊이[numero] = -1;
            깊이--; return palauttaa_KR;
        }
        if (saada(';')) return false;
        if (OTA_Word("return")) {
            int TYYPPI_ARVO = 종류() == ';' ? 0 : lauseke_ARVO_eb3593ac(); tarkistaa_TYYPPI(TYYPPI_ARVO, menetelmä_palauttaa[nykyinen_menetelmä]); vaatimus_ARVO(';');
            내보내기(TYYPPI_ARVO == 0 ? 177 : TYYPPI_ARVO <= 2 || TYYPPI_ARVO == 5 ? 172 : 176); return true;
        }
        if (OTA_Word("if")) {
            vaatimus_ARVO('('); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 2); vaatimus_ARVO(')'); int EPÄTOSI_ARVO = haara(153);
            깊이++; boolean 가 = ohjain_lauseke(); 깊이--;
            if (OTA_Word("else")) { int 끝 = haara(167); Linkki_ARVO(EPÄTOSI_ARVO, KOODI_muuttaa_kokoa); 깊이++; boolean SEKUNNIT_operandi = ohjain_lauseke(); 깊이--; Linkki_ARVO(끝, KOODI_muuttaa_kokoa); return 가 && SEKUNNIT_operandi; }
            Linkki_ARVO(EPÄTOSI_ARVO, KOODI_muuttaa_kokoa); return false;
        }
        if (OTA_Word("while")) {
            int Suorita_2 = KOODI_muuttaa_kokoa; vaatimus_ARVO('('); tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 2); vaatimus_ARVO(')'); int 끝 = haara(153);
            깊이++; ohjain_lauseke(); 깊이--; Linkki_ARVO(haara(167), Suorita_2); Linkki_ARVO(끝, KOODI_muuttaa_kokoa); return false;
        }
        if (OTA_Word("for")) {
            깊이++; vaatimus_ARVO('('); if (종류() != ';') tehtävä_ARVO(true); vaatimus_ARVO(';');
            int ehto = KOODI_muuttaa_kokoa; if (종류() == ';') 내보내기(4); else tarkistaa_TYYPPI(lauseke_ARVO_eb3593ac(), 2); vaatimus_ARVO(';');
            int 끝 = haara(153), leipäteksti = haara(167), päivittää = KOODI_muuttaa_kokoa;
            if (종류() != ')') tehtävä_ARVO(false); vaatimus_ARVO(')'); Linkki_ARVO(haara(167), ehto); Linkki_ARVO(leipäteksti, KOODI_muuttaa_kokoa);
            ohjain_lauseke(); Linkki_ARVO(haara(167), päivittää); Linkki_ARVO(끝, KOODI_muuttaa_kokoa);
            for (int numero = 0; numero < paikallinen_LASKE; numero++) if (지역깊이[numero] == 깊이) 지역깊이[numero] = -1;
            깊이--; return false;
        }
        if (Word_ARVO(paikka, "System")) { 화면출력(); return false; }
        if (종류() == 256 && paikka + 1 < tunnus_LASKE && (토큰종류[paikka + 1] == '(' || 토큰종류[paikka + 1] == '.')) {
            int TYYPPI_ARVO = lauseke_ARVO_eb3593ac(); if (TYYPPI_ARVO != 0) 내보내기(87); vaatimus_ARVO(';'); return false;
        }
        tehtävä_ARVO(true); vaatimus_ARVO(';'); return false;
    }
    static boolean ohjain_lauseke() {
        if (Word_ARVO(paikka, "int") || Word_ARVO(paikka, "boolean") || Word_ARVO(paikka, "char") || Word_ARVO(paikka, "String")
            || Word_ARVO(paikka, "FileInputStream") || Word_ARVO(paikka, "FileOutputStream")) virhe_ARVO("local declaration requires braces");
        return lauseke_ARVO();
    }
    static void 출바(int ARVO) { if (tulos_muuttaa_kokoa == tulostuspaikka.length) virhe_ARVO("class file too large"); else tulostuspaikka[tulos_muuttaa_kokoa++] = ARVO & 255; }
    static void 출짧(int ARVO) { 출바(ARVO >> 8); 출바(ARVO); }
    static void 출정(int ARVO) { 출짧(ARVO >>> 16); 출짧(ARVO); }
    static void kirjoitus_Luokka() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(vakio_LASKE);
        for (int numero = 0; numero < vakio_muuttaa_kokoa; numero++) 출바(vakio_ARVO[numero]);
        출짧(0x21); 출짧(Luokka_vakio); 출짧(pää_vakio); 출짧(0); 출짧(0); 출짧(menetelmä_LASKE);
        for (int numero = 0; numero < menetelmä_LASKE; numero++) {
            출짧(menetelmä_pääsy[numero]); 출짧(menetelmä_nimi_vakio[numero]); 출짧(함수서술[numero]); 출짧(1); 출짧(KOODI_vakio);
            출정(12 + menetelmä_kesto[numero]); 출짧(128); 출짧(함수지역[numero]); 출정(menetelmä_kesto[numero]);
            for (int paikka_merkintä = 0; paikka_merkintä < menetelmä_kesto[numero]; paikka_merkintä++) 출바(KOODI_ARVO[menetelmä_KOODI[numero] + paikka_merkintä]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Suorita_2() {
        if (käyttäjätila.인수개수() == 1 && 자바도구.같음(käyttäjätila.argumentit(0), "-version")) {
            käyttäjätila.Kirjoitus("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (käyttäjätila.인수개수() != 1) { käyttäjätila.Kirjoitus("Usage: javac FILE.java\n"); return 2; }
        int nimi_muuttaa_kokoa = 자바도구.Nimi(tiedostonimi_SMS, käyttäjätila.argumentit(0));
        if (nimi_muuttaa_kokoa < 6 || nimi_muuttaa_kokoa > 62 || tiedostonimi_SMS[nimi_muuttaa_kokoa - 5] != '.' || tiedostonimi_SMS[nimi_muuttaa_kokoa - 4] != 'j'
            || tiedostonimi_SMS[nimi_muuttaa_kokoa - 3] != 'a' || tiedostonimi_SMS[nimi_muuttaa_kokoa - 2] != 'v' || tiedostonimi_SMS[nimi_muuttaa_kokoa - 1] != 'a') {
            käyttäjätila.Kirjoitus("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        lähde_muuttaa_kokoa = käyttäjätila.lukea_Tiedosto(tiedostonimi_SMS, lähdetiedosto);
        if (lähde_muuttaa_kokoa < 0) { käyttäjätila.Kirjoitus("javac: cannot read source: "); 자바도구.kirjoitus_numero(lähde_muuttaa_kokoa); käyttäjätila.kirjoitus_merkki_ARVO(10); return 1; }
        lähde_muuttaa_kokoa = 자바도구.원문해독(lähdetiedosto, lähde_muuttaa_kokoa);
        if (lähde_muuttaa_kokoa < 0) { käyttäjätila.Kirjoitus("javac error: invalid UTF-8 source\n"); return 1; }
        leikata_ARVO_4601577b(); if (!VIRHE) lukea_esittely();
        if (!VIRHE) {
            if (tunnus_kesto[Luokka_tunnus] != nimi_muuttaa_kokoa - 5) virhe_ARVO("class name must match file name");
            for (int numero = 0; numero < nimi_muuttaa_kokoa - 5; numero++) if (lähdetiedosto[tunnus_toimi[Luokka_tunnus] + numero] != tiedostonimi_SMS[numero]) virhe_ARVO("class name must match file name");
        }
        for (nykyinen_menetelmä = 0; nykyinen_menetelmä < menetelmä_LASKE && !VIRHE; nykyinen_menetelmä++) {
            paikka = menetelmä_teksti[nykyinen_menetelmä]; menetelmä_KOODI[nykyinen_menetelmä] = KOODI_muuttaa_kokoa; paikallinen_LASKE = 0; 깊이 = 0;
            for (int numero = 0; numero < menetelmä_argumentti_LASKE[nykyinen_menetelmä]; numero++) Lisää_paikallinen(menetelmä_argumentti_nimi[nykyinen_menetelmä * 16 + numero], menetelmä_argumentti_TYYPPI[nykyinen_menetelmä * 16 + numero]);
            boolean palauttaa_KR = lauseke_ARVO();
            if (!palauttaa_KR && menetelmä_palauttaa[nykyinen_menetelmä] != 0) virhe_ARVO("missing return");
            // haara 뒤의 합류 지점은 반드시 todellinen_data 명령이어야 한다 (버전 49 검증기).
            if (menetelmä_palauttaa[nykyinen_menetelmä] == 0) 내보내기(177);
            else { boolean kokonaisluku = menetelmä_palauttaa[nykyinen_menetelmä] <= 2 || menetelmä_palauttaa[nykyinen_menetelmä] == 5; 내보내기(kokonaisluku ? 3 : 1); 내보내기(kokonaisluku ? 172 : 176); }
            if (paikka != menetelmä_lopettaa_puhelu[nykyinen_menetelmä]) virhe_ARVO("invalid method body");
            함수지역[nykyinen_menetelmä] = paikallinen_LASKE; menetelmä_kesto[nykyinen_menetelmä] = KOODI_muuttaa_kokoa - menetelmä_KOODI[nykyinen_menetelmä];
        }
        if (VIRHE) return 1;
        kirjoitus_Luokka(); if (VIRHE) return 1;
        tiedostonimi_SMS[nimi_muuttaa_kokoa - 4] = 'c'; tiedostonimi_SMS[nimi_muuttaa_kokoa - 3] = 'l'; tiedostonimi_SMS[nimi_muuttaa_kokoa - 2] = 'a';
        tiedostonimi_SMS[nimi_muuttaa_kokoa - 1] = 's'; tiedostonimi_SMS[nimi_muuttaa_kokoa] = 's'; tiedostonimi_SMS[nimi_muuttaa_kokoa + 1] = 0;
        int TULOS = käyttäjätila.kirjoitus_Tiedosto(tiedostonimi_SMS, tulostuspaikka, tulos_muuttaa_kokoa);
        if (TULOS < 0) { käyttäjätila.Kirjoitus("javac: cannot save class: "); 자바도구.kirjoitus_numero(TULOS); käyttäjätila.kirjoitus_merkki_ARVO(10); return 1; }
        käyttäjätila.Kirjoitus("Compiled: "); for (int numero = 0; tiedostonimi_SMS[numero] != 0; numero++) käyttäjätila.kirjoitus_merkki_ARVO(tiedostonimi_SMS[numero]);
        käyttäjätila.Kirjoitus(" (JVM class version 49)\n"); return 0;
    }
}
