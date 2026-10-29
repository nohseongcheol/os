// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. tiedoston_nimi/operandi_Pino/viite/haara 경계를 Suorita_komento 중 검사한다. */
public final class 자바가상기계 {
    static int[] tiedoston_nimi = new int[16384], tiedostonimi_SMS = new int[64];
    static int[] vakio_tunnus = new int[512], 상가 = new int[512], vakio_SEKUNNIT_ARVO = new int[512], merkkijono_viite = new int[512];
    static int[] menetelmä_nimi_SMS = new int[32], menetelmä_TYYPPI = new int[32], menetelmä_pääsy = new int[32];
    static int[] menetelmä_alku = new int[32], menetelmä_lopettaa_puhelu = new int[32], menetelmä_Pino = new int[32], 함수지역 = new int[32];
    static int[] menetelmä_argumentti_LASKE = new int[32], menetelmä_argumentti_TYYPPI = new int[512], menetelmä_palauttaa = new int[32];
    static int[] rajattu_alue_ARVO = new int[16384];
    static int[] paikallinen_ARVO = new int[4096], paikallinen_TYYPPI = new int[4096], operandi_Pino_ARVO = new int[4096], operandi_Pino_TYYPPI = new int[4096];
    static int[] kuva_menetelmä = new int[32], kuva_toimi = new int[32], kuva_Pino = new int[32];
    static int[] keko_ARVO = new int[8192];
    static int Koko, lukea_toimi, vakio_LASKE, menetelmä_LASKE, luokan_nimi, kuva_INDEKSI = -1, keko_lopettaa_puhelu_toimi = 1, palauttaa_TYYPPI;
    static boolean VIRHE;

    static void virhe_ARVO(String Word_SMS) {
        if (!VIRHE) { käyttäjätila.Kirjoitus("JVM error: "); käyttäjätila.Kirjoitus(Word_SMS); käyttäjätila.kirjoitus_merkki_ARVO(10); }
        VIRHE = true;
    }
    static boolean leikata(int Suorita_2, int kesto_ARVO) { return Suorita_2 >= 0 && kesto_ARVO >= 0 && Suorita_2 <= Koko - kesto_ARVO; }
    static int tavu_ARVO() {
        if (!leikata(lukea_toimi, 1)) { virhe_ARVO("truncated class file"); return 0; }
        return tiedoston_nimi[lukea_toimi++];
    }
    static int 짧은수() { return tavu_ARVO() << 8 | tavu_ARVO(); }
    static int kokonaisluku() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int kesto_ARVO) { if (!leikata(lukea_toimi, kesto_ARVO)) virhe_ARVO("invalid attribute size"); else lukea_toimi += kesto_ARVO; }
    static boolean sekki_vakio(int numero, int 종류) {
        if (numero <= 0 || numero >= vakio_LASKE || vakio_tunnus[numero] != 종류) { virhe_ARVO("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_alue(int Suorita_2, int kesto_ARVO, String Word_SMS) {
        if (!leikata(Suorita_2, kesto_ARVO) || kesto_ARVO != Word_SMS.length()) return false;
        for (int numero = 0; numero < kesto_ARVO; numero++) if (tiedoston_nimi[Suorita_2 + numero] != Word_SMS.charAt(numero)) return false;
        return true;
    }
    static boolean Word_SMS(int vakio_ARVO, String Word_SMS) { return sekki_vakio(vakio_ARVO, 1) && SMS_alue(상가[vakio_ARVO], vakio_SEKUNNIT_ARVO[vakio_ARVO], Word_SMS); }
    static boolean kohdistus_Word(int 가, int SEKUNNIT_operandi) {
        if (!sekki_vakio(가, 1) || !sekki_vakio(SEKUNNIT_operandi, 1) || vakio_SEKUNNIT_ARVO[가] != vakio_SEKUNNIT_ARVO[SEKUNNIT_operandi]) return false;
        for (int numero = 0; numero < vakio_SEKUNNIT_ARVO[가]; numero++) if (tiedoston_nimi[상가[가] + numero] != tiedoston_nimi[상가[SEKUNNIT_operandi] + numero]) return false;
        return true;
    }
    static int luokan_nimi_SMS(int numero) { return sekki_vakio(numero, 7) && sekki_vakio(상가[numero], 1) ? 상가[numero] : 0; }
    static int viite_nimi(int numero) { return sekki_vakio(numero, 12) && sekki_vakio(상가[numero], 1) ? 상가[numero] : 0; }
    static int viittauksen_tyyppi(int numero) { return sekki_vakio(numero, 12) && sekki_vakio(vakio_SEKUNNIT_ARVO[numero], 1) ? vakio_SEKUNNIT_ARVO[numero] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (lukea_toimi >= 끝) { virhe_ARVO("invalid descriptor"); return 0; }
        int ARVO = tavu_ARVO();
        if (ARVO == 'V' && 빈형) return 0;
        if (ARVO == 'I' || ARVO == 'B' || ARVO == 'C' || ARVO == 'S' || ARVO == 'Z') return 1;
        if (ARVO == '[') { 서술형(끝, false); return 2; }
        if (ARVO == 'L') {
            int Suorita_2 = lukea_toimi;
            while (lukea_toimi < 끝 && tiedoston_nimi[lukea_toimi] != ';') lukea_toimi++;
            if (lukea_toimi == 끝 || lukea_toimi == Suorita_2) virhe_ARVO("invalid reference descriptor");
            else lukea_toimi++;
            return 2;
        }
        virhe_ARVO("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int funktio_ARVO) {
        int Edellinen_kohde = lukea_toimi, numero = menetelmä_TYYPPI[funktio_ARVO];
        if (!sekki_vakio(numero, 1)) return;
        lukea_toimi = 상가[numero]; int 끝 = lukea_toimi + vakio_SEKUNNIT_ARVO[numero];
        if (tavu_ARVO() != '(') virhe_ARVO("invalid method descriptor");
        int kohde_LASKE = 0;
        while (!VIRHE && lukea_toimi < 끝 && tiedoston_nimi[lukea_toimi] != ')') {
            if (kohde_LASKE == 16) { virhe_ARVO("too many method arguments"); break; }
            menetelmä_argumentti_TYYPPI[funktio_ARVO * 16 + kohde_LASKE++] = 서술형(끝, false);
        }
        if (lukea_toimi >= 끝 || tavu_ARVO() != ')') virhe_ARVO("invalid method descriptor");
        menetelmä_palauttaa[funktio_ARVO] = 서술형(끝, true); menetelmä_argumentti_LASKE[funktio_ARVO] = kohde_LASKE;
        if (lukea_toimi != 끝) virhe_ARVO("invalid method descriptor");
        lukea_toimi = Edellinen_kohde;
    }
    static void ohita_määrite() {
        int kohde_LASKE = 짧은수();
        for (int numero = 0; numero < kohde_LASKE && !VIRHE; numero++) { sekki_vakio(짧은수(), 1); 건너(kokonaisluku()); }
    }
    static int komento_kesto(int ARVO) {
        if (ARVO == 16 || ARVO == 18 || ARVO == 21 || ARVO == 25 || ARVO == 54 || ARVO == 58 || ARVO == 188) return 2;
        if (ARVO == 17 || ARVO == 19 || ARVO == 132 || ARVO >= 153 && ARVO <= 167
            || ARVO >= 178 && ARVO <= 184 || ARVO == 187 || ARVO == 189 || ARVO == 192 || ARVO == 198 || ARVO == 199) return 3;
        if (ARVO >= 0 && ARVO <= 8 || ARVO >= 26 && ARVO <= 29 || ARVO >= 42 && ARVO <= 46 || ARVO == 50
            || ARVO >= 59 && ARVO <= 62 || ARVO >= 75 && ARVO <= 79 || ARVO == 83 || ARVO == 87 || ARVO == 89 || ARVO == 95
            || ARVO == 96 || ARVO == 100 || ARVO == 104 || ARVO == 108 || ARVO == 112 || ARVO == 116
            || ARVO == 120 || ARVO == 122 || ARVO == 124 || ARVO == 126 || ARVO == 128 || ARVO == 130
            || ARVO >= 145 && ARVO <= 147 || ARVO == 172 || ARVO == 176 || ARVO == 177 || ARVO == 190) return 1;
        return 0;
    }
    static void lukea_Luokka() {
        if (kokonaisluku() != 0xcafebabe) virhe_ARVO("not a class file");
        int 부판 = 짧은수(), versio_ARVO = 짧은수();
        if (versio_ARVO < 45 || versio_ARVO > 52 || 부판 != 0) virhe_ARVO("supported class versions: 45..52, minor 0");
        vakio_LASKE = 짧은수();
        if (vakio_LASKE < 1 || vakio_LASKE > 512) { virhe_ARVO("constant pool limit (511)"); return; }
        for (int numero = 1; numero < vakio_LASKE && !VIRHE; numero++) {
            int 종류 = tavu_ARVO(); vakio_tunnus[numero] = 종류;
            if (종류 == 1) { vakio_SEKUNNIT_ARVO[numero] = 짧은수(); 상가[numero] = lukea_toimi; 건너(vakio_SEKUNNIT_ARVO[numero]); }
            else if (종류 == 3) 상가[numero] = kokonaisluku();
            else if (종류 == 7 || 종류 == 8) 상가[numero] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[numero] = 짧은수(); vakio_SEKUNNIT_ARVO[numero] = 짧은수(); }
            else virhe_ARVO("unsupported constant type");
        }
        int lupa_ARVO = 짧은수();
        if ((lupa_ARVO & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) virhe_ARVO("unsupported class flags");
        luokan_nimi = luokan_nimi_SMS(짧은수());
        if (!Word_SMS(luokan_nimi_SMS(짧은수()), "java/lang/Object")) virhe_ARVO("inheritance unsupported");
        if (짧은수() != 0) virhe_ARVO("interfaces unsupported");
        if (짧은수() != 0) virhe_ARVO("fields unsupported");
        menetelmä_LASKE = 짧은수();
        if (menetelmä_LASKE < 1 || menetelmä_LASKE > 32) { virhe_ARVO("method count limit (32)"); return; }
        for (int numero = 0; numero < menetelmä_LASKE && !VIRHE; numero++) {
            menetelmä_pääsy[numero] = 짧은수(); menetelmä_nimi_SMS[numero] = 짧은수(); menetelmä_TYYPPI[numero] = 짧은수();
            sekki_vakio(menetelmä_nimi_SMS[numero], 1); 서술읽기(numero);
            if ((menetelmä_pääsy[numero] & (0x100 | 0x400 | 0x20)) != 0) virhe_ARVO("native, abstract and synchronized methods unsupported");
            if ((menetelmä_pääsy[numero] & 8) == 0 && !Word_SMS(menetelmä_nimi_SMS[numero], "<init>")) virhe_ARVO("instance methods unsupported");
            if (Word_SMS(menetelmä_nimi_SMS[numero], "<clinit>")) virhe_ARVO("class initializers unsupported");
            for (int etukamera_ARVO = 0; etukamera_ARVO < numero; etukamera_ARVO++) if (kohdistus_Word(menetelmä_nimi_SMS[etukamera_ARVO], menetelmä_nimi_SMS[numero]) && kohdistus_Word(menetelmä_TYYPPI[etukamera_ARVO], menetelmä_TYYPPI[numero])) virhe_ARVO("duplicate method");
            int kohde_LASKE = 짧은수();
            for (int määritteen_arvo = 0; määritteen_arvo < kohde_LASKE && !VIRHE; määritteen_arvo++) {
                int Nimi = 짧은수(), kesto_ARVO = kokonaisluku(), Suorita_2 = lukea_toimi;
                if (!leikata(Suorita_2, kesto_ARVO)) { virhe_ARVO("truncated method attribute"); break; }
                if (Word_SMS(Nimi, "Code")) {
                    if (menetelmä_alku[numero] != 0) virhe_ARVO("duplicate Code attribute");
                    menetelmä_Pino[numero] = 짧은수(); 함수지역[numero] = 짧은수(); int KOODI_kesto = kokonaisluku();
                    if (menetelmä_Pino[numero] > 128 || 함수지역[numero] > 128 || 함수지역[numero] < menetelmä_argumentti_LASKE[numero]
                        || KOODI_kesto < 1 || KOODI_kesto > 8192) virhe_ARVO("method memory limits exceeded");
                    menetelmä_alku[numero] = lukea_toimi; 건너(KOODI_kesto); menetelmä_lopettaa_puhelu[numero] = lukea_toimi;
                    if (짧은수() != 0) virhe_ARVO("exception handlers unsupported");
                    ohita_määrite();
                    if (lukea_toimi != Suorita_2 + kesto_ARVO) virhe_ARVO("Code attribute size mismatch");
                } else 건너(kesto_ARVO);
            }
            if (menetelmä_alku[numero] == 0) virhe_ARVO("missing Code attribute");
            int paikka_merkintä = menetelmä_alku[numero];
            while (paikka_merkintä < menetelmä_lopettaa_puhelu[numero] && !VIRHE) {
                int kesto_ARVO = komento_kesto(tiedoston_nimi[paikka_merkintä]);
                if (kesto_ARVO == 0 || kesto_ARVO > menetelmä_lopettaa_puhelu[numero] - paikka_merkintä) { virhe_ARVO("unsupported or truncated bytecode"); break; }
                rajattu_alue_ARVO[paikka_merkintä] = numero + 1; paikka_merkintä += kesto_ARVO;
            }
            // 실행하지 않는 경로에도 잘못된 haara 목적지를 허용하지 않는다.
            paikka_merkintä = menetelmä_alku[numero];
            while (paikka_merkintä < menetelmä_lopettaa_puhelu[numero] && !VIRHE) {
                int ARVO = tiedoston_nimi[paikka_merkintä];
                if (ARVO >= 153 && ARVO <= 167 || ARVO == 198 || ARVO == 199) {
                    int kohde_ARVO = paikka_merkintä + (short)(tiedoston_nimi[paikka_merkintä + 1] << 8 | tiedoston_nimi[paikka_merkintä + 2]);
                    if (kohde_ARVO < menetelmä_alku[numero] || kohde_ARVO >= menetelmä_lopettaa_puhelu[numero] || rajattu_alue_ARVO[kohde_ARVO] != numero + 1) virhe_ARVO("invalid branch target");
                }
                paikka_merkintä += komento_kesto(ARVO);
            }
        }
        if (!VIRHE) ohita_määrite();
        if (lukea_toimi != Koko) virhe_ARVO("extra class file data");
    }
    static int jakaa_Tallennus(int 종류, int kesto_ARVO) {
        if (kesto_ARVO < 0 || kesto_ARVO > keko_ARVO.length - keko_lopettaa_puhelu_toimi - 2) { virhe_ARVO("object heap exhausted or negative array size"); return 0; }
        int viite = keko_lopettaa_puhelu_toimi; keko_lopettaa_puhelu_toimi += kesto_ARVO + 2; keko_ARVO[viite] = 종류; keko_ARVO[viite + 1] = kesto_ARVO;
        return viite;
    }
    static boolean objekti_ARVO(int viite, int 종류) {
        if (viite < 1 || viite >= keko_lopettaa_puhelu_toimi - 1 || keko_ARVO[viite] != 종류) { virhe_ARVO("null or invalid object reference"); return false; }
        return true;
    }
    static int vakio_SMS(int INDEKSI) {
        if (!sekki_vakio(INDEKSI, 1)) return 0;
        if (merkkijono_viite[INDEKSI] != 0) return merkkijono_viite[INDEKSI];
        int viite = jakaa_Tallennus(1, vakio_SEKUNNIT_ARVO[INDEKSI]); if (VIRHE) return 0;
        int 끝 = 상가[INDEKSI] + vakio_SEKUNNIT_ARVO[INDEKSI], numero = 상가[INDEKSI], kesto_ARVO = 0;
        while (numero < 끝 && !VIRHE) {
            int ARVO = tiedoston_nimi[numero++];
            if (ARVO == 0) virhe_ARVO("invalid modified UTF-8");
            else if (ARVO >= 192 && ARVO <= 223 && numero < 끝) {
                int Seuraava_kohde = tiedoston_nimi[numero++];
                if ((Seuraava_kohde & 192) != 128) virhe_ARVO("invalid modified UTF-8");
                ARVO = (ARVO & 31) << 6 | Seuraava_kohde & 63;
                if (ARVO != 0 && ARVO < 128) virhe_ARVO("overlong modified UTF-8");
            } else if (ARVO >= 224 && ARVO <= 239 && numero + 1 < 끝) {
                int 가 = tiedoston_nimi[numero++], SEKUNNIT_operandi = tiedoston_nimi[numero++];
                if ((가 & 192) != 128 || (SEKUNNIT_operandi & 192) != 128) virhe_ARVO("invalid modified UTF-8");
                ARVO = (ARVO & 15) << 12 | (가 & 63) << 6 | SEKUNNIT_operandi & 63;
                if (ARVO < 2048) virhe_ARVO("overlong modified UTF-8");
            } else if (ARVO >= 128) virhe_ARVO("invalid modified UTF-8");
            keko_ARVO[viite + 2 + kesto_ARVO++] = ARVO;
        }
        keko_ARVO[viite + 1] = kesto_ARVO; merkkijono_viite[INDEKSI] = viite; return viite;
    }
    static int isäntä_merkki(String ARVO) {
        int viite = jakaa_Tallennus(1, ARVO.length()); if (VIRHE) return 0;
        for (int numero = 0; numero < ARVO.length(); numero++) keko_ARVO[viite + 2 + numero] = ARVO.charAt(numero);
        return viite;
    }
    static void kirjoitus_SMS(int viite) {
        if (viite == 0) { käyttäjätila.Kirjoitus("null"); return; }
        if (!objekti_ARVO(viite, 1)) return;
        for (int numero = 0; numero < keko_ARVO[viite + 1]; numero++) käyttäjätila.kirjoitus_merkki_ARVO(keko_ARVO[viite + 2 + numero]);
    }
    static int numero_merkki(int ARVO) {
        int viite = jakaa_Tallennus(1, 11); if (VIRHE) return 0;
        int kesto_ARVO = 0;
        if (ARVO < 0) keko_ARVO[viite + 2 + kesto_ARVO++] = '-'; else ARVO = -ARVO;
        int sijainti = 1000000000; boolean Suorita_2 = false;
        while (sijainti != 0) {
            int numero = -(ARVO / sijainti);
            if (numero != 0 || Suorita_2 || sijainti == 1) { keko_ARVO[viite + 2 + kesto_ARVO++] = '0' + numero; Suorita_2 = true; }
            ARVO %= sijainti; sijainti /= 10;
        }
        keko_ARVO[viite + 1] = kesto_ARVO; return viite;
    }
    static int 정수해독(int viite) {
        if (!objekti_ARVO(viite, 1)) return 0;
        int kesto_ARVO = keko_ARVO[viite + 1], numero = 0, ARVO = 0; boolean 음수 = false;
        if (kesto_ARVO > 0 && (keko_ARVO[viite + 2] == '-' || keko_ARVO[viite + 2] == '+')) { 음수 = keko_ARVO[viite + 2] == '-'; numero++; }
        if (numero == kesto_ARVO) virhe_ARVO("NumberFormatException");
        for (; numero < kesto_ARVO && !VIRHE; numero++) {
            int numero_ARVO = keko_ARVO[viite + 2 + numero] - '0';
            if (numero_ARVO < 0 || numero_ARVO > 9 || ARVO < -214748364 || ARVO == -214748364 && numero_ARVO > (음수 ? 8 : 7)) virhe_ARVO("NumberFormatException");
            ARVO = ARVO * 10 - numero_ARVO;
        }
        return 음수 ? ARVO : -ARVO;
    }
    static void 넣기(int ARVO, int TYYPPI_ARVO) {
        if (VIRHE) return;
        if (kuva_INDEKSI < 0 || kuva_Pino[kuva_INDEKSI] >= menetelmä_Pino[kuva_menetelmä[kuva_INDEKSI]]) { virhe_ARVO("operand stack overflow"); return; }
        int paikka_merkintä = kuva_INDEKSI * 128 + kuva_Pino[kuva_INDEKSI]++; operandi_Pino_ARVO[paikka_merkintä] = ARVO; operandi_Pino_TYYPPI[paikka_merkintä] = TYYPPI_ARVO;
    }
    static int 빼기(int TYYPPI_ARVO) {
        if (VIRHE) return 0;
        if (kuva_INDEKSI < 0 || kuva_Pino[kuva_INDEKSI] < 1) { virhe_ARVO("operand stack underflow"); return 0; }
        int paikka_merkintä = kuva_INDEKSI * 128 + --kuva_Pino[kuva_INDEKSI]; palauttaa_TYYPPI = operandi_Pino_TYYPPI[paikka_merkintä];
        if (TYYPPI_ARVO != 0 && palauttaa_TYYPPI != TYYPPI_ARVO) virhe_ARVO("operand type mismatch");
        return operandi_Pino_ARVO[paikka_merkintä];
    }
    static void lukea_paikallinen(int INDEKSI, int TYYPPI_ARVO) {
        if (INDEKSI >= 함수지역[kuva_menetelmä[kuva_INDEKSI]] || INDEKSI < 0 || paikallinen_TYYPPI[kuva_INDEKSI * 128 + INDEKSI] != TYYPPI_ARVO) { virhe_ARVO("invalid or uninitialized local"); return; }
        넣기(paikallinen_ARVO[kuva_INDEKSI * 128 + INDEKSI], TYYPPI_ARVO);
    }
    static void kirjoitus_paikallinen(int INDEKSI, int TYYPPI_ARVO) {
        if (INDEKSI >= 함수지역[kuva_menetelmä[kuva_INDEKSI]] || INDEKSI < 0) { virhe_ARVO("local index out of range"); return; }
        int ARVO = 빼기(TYYPPI_ARVO); paikallinen_ARVO[kuva_INDEKSI * 128 + INDEKSI] = ARVO; paikallinen_TYYPPI[kuva_INDEKSI * 128 + INDEKSI] = TYYPPI_ARVO;
    }
    static int lukea_toimintokoodi_tavu() {
        int paikka = kuva_toimi[kuva_INDEKSI];
        if (paikka < menetelmä_alku[kuva_menetelmä[kuva_INDEKSI]] || paikka >= menetelmä_lopettaa_puhelu[kuva_menetelmä[kuva_INDEKSI]]) { virhe_ARVO("instruction pointer out of range"); return 0; }
        kuva_toimi[kuva_INDEKSI]++; return tiedoston_nimi[paikka];
    }
    static int 명짧() { return lukea_toimintokoodi_tavu() << 8 | lukea_toimintokoodi_tavu(); }
    static void siirrä_ARVO_83b651b8(int paikka) {
        int funktio_ARVO = kuva_menetelmä[kuva_INDEKSI];
        if (paikka < menetelmä_alku[funktio_ARVO] || paikka >= menetelmä_lopettaa_puhelu[funktio_ARVO] || rajattu_alue_ARVO[paikka] != funktio_ARVO + 1) virhe_ARVO("invalid branch target");
        else kuva_toimi[kuva_INDEKSI] = paikka;
    }
    static void 호출(int funktio_ARVO) {
        if (kuva_INDEKSI == 31) { virhe_ARVO("call stack limit (32)"); return; }
        int Seuraava_kohde = kuva_INDEKSI + 1;
        for (int numero = 0; numero < 128; numero++) paikallinen_TYYPPI[Seuraava_kohde * 128 + numero] = 0;
        for (int numero = menetelmä_argumentti_LASKE[funktio_ARVO] - 1; numero >= 0; numero--) {
            paikallinen_ARVO[Seuraava_kohde * 128 + numero] = 빼기(menetelmä_argumentti_TYYPPI[funktio_ARVO * 16 + numero]); paikallinen_TYYPPI[Seuraava_kohde * 128 + numero] = menetelmä_argumentti_TYYPPI[funktio_ARVO * 16 + numero];
        }
        kuva_INDEKSI = Seuraava_kohde; kuva_menetelmä[kuva_INDEKSI] = funktio_ARVO; kuva_toimi[kuva_INDEKSI] = menetelmä_alku[funktio_ARVO]; kuva_Pino[kuva_INDEKSI] = 0;
    }
    static void palauttaa_KR(int TYYPPI_ARVO) {
        if (TYYPPI_ARVO != menetelmä_palauttaa[kuva_menetelmä[kuva_INDEKSI]]) { virhe_ARVO("return type mismatch"); return; }
        int ARVO = TYYPPI_ARVO == 0 ? 0 : 빼기(TYYPPI_ARVO);
        kuva_INDEKSI--; if (kuva_INDEKSI >= 0 && TYYPPI_ARVO != 0) 넣기(ARVO, TYYPPI_ARVO);
    }
    static int[] virta_tiedostonimi = new int[64];
    static void Tiedosto_virta_KUTSU(int omistaja_ARVO, int Nimi, int muoto_ARVO, int komento) {
        boolean tulostuspaikka = Word_SMS(omistaja_ARVO, "java/io/FileOutputStream");
        int 종류 = tulostuspaikka ? 6 : 5;
        if (komento == 183 && Word_SMS(Nimi, "<init>")) {
            boolean 이어 = false;
            if (tulostuspaikka && Word_SMS(muoto_ARVO, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(muoto_ARVO, "(Ljava/lang/String;)V")) { virhe_ARVO("unsupported file stream constructor"); return; }
            int Tiedosto_merkintä_nimi = 빼기(2), virta_ARVO = 빼기(2);
            if (!objekti_ARVO(Tiedosto_merkintä_nimi, 1) || !objekti_ARVO(virta_ARVO, 종류) || VIRHE) return;
            if (keko_ARVO[virta_ARVO + 3] != 0) { virhe_ARVO("file stream already initialized"); return; }
            int kesto_ARVO = keko_ARVO[Tiedosto_merkintä_nimi + 1];
            if (kesto_ARVO < 1 || kesto_ARVO > 63) { virhe_ARVO("invalid file name length"); return; }
            for (int paikka_merkintä = 0; paikka_merkintä < kesto_ARVO; paikka_merkintä++) {
                int ARVO = keko_ARVO[Tiedosto_merkintä_nimi + 2 + paikka_merkintä];
                if (ARVO < 1 || ARVO > 127) { virhe_ARVO("file stream paths currently require ASCII"); return; }
                virta_tiedostonimi[paikka_merkintä] = ARVO;
            }
            virta_tiedostonimi[kesto_ARVO] = 0;
            int 서술자 = käyttäjätila.파일서술자열기(virta_tiedostonimi, tulostuspaikka ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { virhe_ARVO("FileNotFoundException: file open failed"); return; }
            keko_ARVO[virta_ARVO + 2] = 서술자; keko_ARVO[virta_ARVO + 3] = 1;
            return;
        }
        if (komento != 182) { virhe_ARVO("invalid file stream invocation"); return; }
        int Toiminto = -1, ARVO = 0;
        if (Word_SMS(Nimi, "close") && Word_SMS(muoto_ARVO, "()V")) Toiminto = 0;
        if (!tulostuspaikka && Word_SMS(Nimi, "read") && Word_SMS(muoto_ARVO, "()I")) Toiminto = 1;
        if (tulostuspaikka && Word_SMS(Nimi, "write") && Word_SMS(muoto_ARVO, "(I)V")) { Toiminto = 2; ARVO = 빼기(1); }
        if (Toiminto < 0) { virhe_ARVO("unsupported file stream method"); return; }
        int virta_ARVO = 빼기(2);
        if (!objekti_ARVO(virta_ARVO, 종류) || VIRHE) return;
        if (keko_ARVO[virta_ARVO + 3] == 0) { virhe_ARVO("uninitialized file stream"); return; }
        int 서술자 = keko_ARVO[virta_ARVO + 2];
        if (Toiminto == 0) {
            if (서술자 >= 0 && käyttäjätila.파일서술자닫기(서술자) < 0) virhe_ARVO("IOException: close failed");
            keko_ARVO[virta_ARVO + 2] = -1; return;
        }
        if (서술자 < 0) { virhe_ARVO("IOException: stream closed"); return; }
        if (Toiminto == 1) {
            int TULOS = käyttäjätila.파일한바이트읽기(서술자);
            if (TULOS < -1) virhe_ARVO("IOException: read failed"); else 넣기(TULOS, 1);
        } else if (käyttäjätila.파일한바이트쓰기(서술자, ARVO) != 1) virhe_ARVO("IOException: write failed");
    }
    static void KUTSU_menetelmä(int INDEKSI, int komento) {
        if (!sekki_vakio(INDEKSI, 10)) return;
        int omistaja_ARVO = luokan_nimi_SMS(상가[INDEKSI]), Nimi = viite_nimi(vakio_SEKUNNIT_ARVO[INDEKSI]), muoto_ARVO = viittauksen_tyyppi(vakio_SEKUNNIT_ARVO[INDEKSI]);
        if (VIRHE) return;
        if (kohdistus_Word(omistaja_ARVO, luokan_nimi)) {
            if (komento != 184) { virhe_ARVO("only static user methods are supported"); return; }
            for (int numero = 0; numero < menetelmä_LASKE; numero++) if (kohdistus_Word(Nimi, menetelmä_nimi_SMS[numero]) && kohdistus_Word(muoto_ARVO, menetelmä_TYYPPI[numero])) {
                if ((menetelmä_pääsy[numero] & 8) == 0) virhe_ARVO("method is not static"); else 호출(numero);
                return;
            }
            virhe_ARVO("NoSuchMethodError"); return;
        }
        if (Word_SMS(omistaja_ARVO, "java/io/FileInputStream") || Word_SMS(omistaja_ARVO, "java/io/FileOutputStream")) {
            Tiedosto_virta_KUTSU(omistaja_ARVO, Nimi, muoto_ARVO, komento); return;
        }
        if (komento == 184 && Word_SMS(omistaja_ARVO, "java/lang/Integer") && Word_SMS(Nimi, "parseInt") && Word_SMS(muoto_ARVO, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (komento == 182 && Word_SMS(omistaja_ARVO, "java/io/PrintStream") && (Word_SMS(Nimi, "println") || Word_SMS(Nimi, "print"))) {
            int TYYPPI_ARVO = 0, ARVO = 0;
            if (Word_SMS(muoto_ARVO, "(I)V")) { TYYPPI_ARVO = 1; ARVO = 빼기(1); }
            else if (Word_SMS(muoto_ARVO, "(Z)V")) { TYYPPI_ARVO = 2; ARVO = 빼기(1); }
            else if (Word_SMS(muoto_ARVO, "(C)V")) { TYYPPI_ARVO = 3; ARVO = 빼기(1); }
            else if (Word_SMS(muoto_ARVO, "(Ljava/lang/String;)V")) { TYYPPI_ARVO = 4; ARVO = 빼기(2); }
            else if (!Word_SMS(muoto_ARVO, "()V") || !Word_SMS(Nimi, "println")) virhe_ARVO("unsupported print descriptor");
            if (빼기(2) != -1) virhe_ARVO("invalid PrintStream receiver");
            if (VIRHE) return;
            if (TYYPPI_ARVO == 1) 자바도구.kirjoitus_numero(ARVO);
            if (TYYPPI_ARVO == 2) käyttäjätila.Kirjoitus(ARVO == 0 ? "false" : "true");
            if (TYYPPI_ARVO == 3) käyttäjätila.kirjoitus_merkki_ARVO(ARVO & 65535);
            if (TYYPPI_ARVO == 4) kirjoitus_SMS(ARVO);
            if (Word_SMS(Nimi, "println")) käyttäjätila.kirjoitus_merkki_ARVO(10);
            return;
        }
        if (komento == 182 && Word_SMS(omistaja_ARVO, "java/lang/String")) {
            if (Word_SMS(Nimi, "length") && Word_SMS(muoto_ARVO, "()I")) {
                int viite = 빼기(2); if (objekti_ARVO(viite, 1)) 넣기(keko_ARVO[viite + 1], 1); return;
            }
            if (Word_SMS(Nimi, "charAt") && Word_SMS(muoto_ARVO, "(I)C")) {
                int alaindeksi_ARVO = 빼기(1), viite = 빼기(2);
                if (objekti_ARVO(viite, 1)) {
                    if (alaindeksi_ARVO < 0 || alaindeksi_ARVO >= keko_ARVO[viite + 1]) virhe_ARVO("StringIndexOutOfBoundsException"); else 넣기(keko_ARVO[viite + 2 + alaindeksi_ARVO], 1);
                }
                return;
            }
        }
        if (Word_SMS(omistaja_ARVO, "java/lang/StringBuilder")) {
            if (komento == 183 && Word_SMS(Nimi, "<init>") && Word_SMS(muoto_ARVO, "()V")) { objekti_ARVO(빼기(2), 4); return; }
            if (komento == 182 && Word_SMS(Nimi, "toString") && Word_SMS(muoto_ARVO, "()Ljava/lang/String;")) {
                int viite = 빼기(2); if (objekti_ARVO(viite, 4)) 넣기(keko_ARVO[viite + 2] == 0 ? isäntä_merkki("") : keko_ARVO[viite + 2], 2); return;
            }
            if (komento == 182 && Word_SMS(Nimi, "append")) {
                int teksti = 0;
                if (Word_SMS(muoto_ARVO, "(I)Ljava/lang/StringBuilder;")) teksti = numero_merkki(빼기(1));
                else if (Word_SMS(muoto_ARVO, "(Z)Ljava/lang/StringBuilder;")) teksti = isäntä_merkki(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(muoto_ARVO, "(C)Ljava/lang/StringBuilder;")) {
                    int ARVO = 빼기(1); teksti = jakaa_Tallennus(1, 1); if (!VIRHE) keko_ARVO[teksti + 2] = ARVO & 65535;
                }
                else if (Word_SMS(muoto_ARVO, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { teksti = 빼기(2); if (teksti == 0) teksti = isäntä_merkki("null"); }
                else { virhe_ARVO("unsupported StringBuilder append"); return; }
                int viite = 빼기(2); if (!objekti_ARVO(viite, 4) || !objekti_ARVO(teksti, 1)) return;
                int etukamera_ARVO = keko_ARVO[viite + 2], etukamera_ARVO_kesto = etukamera_ARVO == 0 ? 0 : keko_ARVO[etukamera_ARVO + 1], BACK_ARVO_kesto = keko_ARVO[teksti + 1];
                int 새글 = jakaa_Tallennus(1, etukamera_ARVO_kesto + BACK_ARVO_kesto); if (VIRHE) return;
                for (int numero = 0; numero < etukamera_ARVO_kesto; numero++) keko_ARVO[새글 + 2 + numero] = keko_ARVO[etukamera_ARVO + 2 + numero];
                for (int numero = 0; numero < BACK_ARVO_kesto; numero++) keko_ARVO[새글 + 2 + etukamera_ARVO_kesto + numero] = keko_ARVO[teksti + 2 + numero];
                keko_ARVO[viite + 2] = 새글; 넣기(viite, 2); return;
            }
        }
        virhe_ARVO("unsupported library method");
    }
    static int MATRIISI_paikka(int viite, int alaindeksi_ARVO, int TYYPPI_ARVO) {
        if (!objekti_ARVO(viite, TYYPPI_ARVO)) return 0;
        if (alaindeksi_ARVO < 0 || alaindeksi_ARVO >= keko_ARVO[viite + 1]) { virhe_ARVO("ArrayIndexOutOfBoundsException"); return 0; }
        return viite + 2 + alaindeksi_ARVO;
    }
    static void Suorita_komento() {
        int 남음 = 500000;
        while (kuva_INDEKSI >= 0 && !VIRHE) {
            if (--남음 == 0) { virhe_ARVO("instruction limit (500000)"); break; }
            int Suorita_2 = kuva_toimi[kuva_INDEKSI], ARVO = lukea_toimintokoodi_tavu();
            if (VIRHE) break;
            if (ARVO == 0) continue;
            if (ARVO == 1) { 넣기(0, 2); continue; }
            if (ARVO >= 2 && ARVO <= 8) { 넣기(ARVO - 3, 1); continue; }
            if (ARVO == 16) { 넣기((byte)lukea_toimintokoodi_tavu(), 1); continue; }
            if (ARVO == 17) { 넣기((short)명짧(), 1); continue; }
            if (ARVO == 18 || ARVO == 19) {
                int numero = ARVO == 18 ? lukea_toimintokoodi_tavu() : 명짧();
                if (numero <= 0 || numero >= vakio_LASKE) virhe_ARVO("invalid ldc constant");
                else if (vakio_tunnus[numero] == 3) 넣기(상가[numero], 1);
                else if (vakio_tunnus[numero] == 8) 넣기(vakio_SMS(상가[numero]), 2);
                else virhe_ARVO("unsupported ldc constant");
                continue;
            }
            if (ARVO == 21 || ARVO == 25) { lukea_paikallinen(lukea_toimintokoodi_tavu(), ARVO == 21 ? 1 : 2); continue; }
            if (ARVO >= 26 && ARVO <= 29) { lukea_paikallinen(ARVO - 26, 1); continue; }
            if (ARVO >= 42 && ARVO <= 45) { lukea_paikallinen(ARVO - 42, 2); continue; }
            if (ARVO == 54 || ARVO == 58) { kirjoitus_paikallinen(lukea_toimintokoodi_tavu(), ARVO == 54 ? 1 : 2); continue; }
            if (ARVO >= 59 && ARVO <= 62) { kirjoitus_paikallinen(ARVO - 59, 1); continue; }
            if (ARVO >= 75 && ARVO <= 78) { kirjoitus_paikallinen(ARVO - 75, 2); continue; }
            if (ARVO == 46 || ARVO == 50) {
                int alaindeksi_ARVO = 빼기(1), viite = 빼기(2), paikka_merkintä = MATRIISI_paikka(viite, alaindeksi_ARVO, ARVO == 46 ? 2 : 3);
                if (!VIRHE) 넣기(keko_ARVO[paikka_merkintä], ARVO == 46 ? 1 : 2); continue;
            }
            if (ARVO == 79 || ARVO == 83) {
                int kohde_elementti = 빼기(ARVO == 79 ? 1 : 2), alaindeksi_ARVO = 빼기(1), viite = 빼기(2), paikka_merkintä = MATRIISI_paikka(viite, alaindeksi_ARVO, ARVO == 79 ? 2 : 3);
                if (ARVO == 83 && kohde_elementti != 0) objekti_ARVO(kohde_elementti, 1);
                if (!VIRHE) keko_ARVO[paikka_merkintä] = kohde_elementti; continue;
            }
            if (ARVO == 87) { 빼기(0); continue; }
            if (ARVO == 89) { int 가 = 빼기(0), TYYPPI_ARVO = palauttaa_TYYPPI; 넣기(가, TYYPPI_ARVO); 넣기(가, TYYPPI_ARVO); continue; }
            if (ARVO == 95) { int 가 = 빼기(0), 가형 = palauttaa_TYYPPI, SEKUNNIT_operandi = 빼기(0), SEKUNNIT_operandi_TYYPPI = palauttaa_TYYPPI; 넣기(가, 가형); 넣기(SEKUNNIT_operandi, SEKUNNIT_operandi_TYYPPI); continue; }
            if (ARVO == 96 || ARVO == 100 || ARVO == 104 || ARVO == 108 || ARVO == 112 || ARVO == 120
                || ARVO == 122 || ARVO == 124 || ARVO == 126 || ARVO == 128 || ARVO == 130) {
                int SEKUNNIT_operandi = 빼기(1), 가 = 빼기(1), TULOS = 0;
                if ((ARVO == 108 || ARVO == 112) && SEKUNNIT_operandi == 0) { virhe_ARVO("ArithmeticException: / by zero"); continue; }
                if (ARVO == 96) TULOS = 가 + SEKUNNIT_operandi;
                if (ARVO == 100) TULOS = 가 - SEKUNNIT_operandi;
                if (ARVO == 104) TULOS = 가 * SEKUNNIT_operandi;
                if (ARVO == 108) TULOS = 가 / SEKUNNIT_operandi;
                if (ARVO == 112) TULOS = 가 % SEKUNNIT_operandi;
                if (ARVO == 120) TULOS = 가 << SEKUNNIT_operandi;
                if (ARVO == 122) TULOS = 가 >> SEKUNNIT_operandi;
                if (ARVO == 124) TULOS = 가 >>> SEKUNNIT_operandi;
                if (ARVO == 126) TULOS = 가 & SEKUNNIT_operandi;
                if (ARVO == 128) TULOS = 가 | SEKUNNIT_operandi;
                if (ARVO == 130) TULOS = 가 ^ SEKUNNIT_operandi;
                넣기(TULOS, 1); continue;
            }
            if (ARVO == 116) { 넣기(-빼기(1), 1); continue; }
            if (ARVO == 132) {
                int paikallinen_laajuus = lukea_toimintokoodi_tavu(), 증분 = (byte)lukea_toimintokoodi_tavu(); lukea_paikallinen(paikallinen_laajuus, 1); 넣기(빼기(1) + 증분, 1); kirjoitus_paikallinen(paikallinen_laajuus, 1); continue;
            }
            if (ARVO >= 145 && ARVO <= 147) {
                int numero = 빼기(1); 넣기(ARVO == 145 ? (byte)numero : ARVO == 146 ? (char)numero : (short)numero, 1); continue;
            }
            if (ARVO >= 153 && ARVO <= 167 || ARVO == 198 || ARVO == 199) {
                int kohde_ARVO = Suorita_2 + (short)명짧(); boolean 갈까 = ARVO == 167;
                if (ARVO >= 153 && ARVO <= 158) {
                    int numero = 빼기(1); 갈까 = ARVO == 153 ? numero == 0 : ARVO == 154 ? numero != 0 : ARVO == 155 ? numero < 0 : ARVO == 156 ? numero >= 0 : ARVO == 157 ? numero > 0 : numero <= 0;
                } else if (ARVO >= 159 && ARVO <= 166) {
                    int SEKUNNIT_operandi = 빼기(ARVO >= 165 ? 2 : 1), 가 = 빼기(ARVO >= 165 ? 2 : 1);
                    갈까 = ARVO == 159 || ARVO == 165 ? 가 == SEKUNNIT_operandi : ARVO == 160 || ARVO == 166 ? 가 != SEKUNNIT_operandi : ARVO == 161 ? 가 < SEKUNNIT_operandi : ARVO == 162 ? 가 >= SEKUNNIT_operandi : ARVO == 163 ? 가 > SEKUNNIT_operandi : 가 <= SEKUNNIT_operandi;
                } else if (ARVO == 198 || ARVO == 199) { int numero = 빼기(2); 갈까 = ARVO == 198 ? numero == 0 : numero != 0; }
                if (갈까) siirrä_ARVO_83b651b8(kohde_ARVO); continue;
            }
            if (ARVO == 172 || ARVO == 176 || ARVO == 177) { palauttaa_KR(ARVO == 172 ? 1 : ARVO == 176 ? 2 : 0); continue; }
            if (ARVO == 178) {
                int numero = 명짧(); if (!sekki_vakio(numero, 9)) continue;
                if (!Word_SMS(luokan_nimi_SMS(상가[numero]), "java/lang/System") || !Word_SMS(viite_nimi(vakio_SEKUNNIT_ARVO[numero]), "out")
                    || !Word_SMS(viittauksen_tyyppi(vakio_SEKUNNIT_ARVO[numero]), "Ljava/io/PrintStream;")) virhe_ARVO("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (ARVO == 182 || ARVO == 183 || ARVO == 184) { KUTSU_menetelmä(명짧(), ARVO); continue; }
            if (ARVO == 187) {
                int Nimi = luokan_nimi_SMS(명짧());
                if (Word_SMS(Nimi, "java/lang/StringBuilder")) 넣기(jakaa_Tallennus(4, 1), 2);
                else if (Word_SMS(Nimi, "java/io/FileInputStream") || Word_SMS(Nimi, "java/io/FileOutputStream")) {
                    int viite = jakaa_Tallennus(Word_SMS(Nimi, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!VIRHE) { keko_ARVO[viite + 2] = -1; 넣기(viite, 2); }
                } else virhe_ARVO("unsupported object construction");
                continue;
            }
            if (ARVO == 188 || ARVO == 189) {
                if (ARVO == 188) { if (lukea_toimintokoodi_tavu() != 10) virhe_ARVO("only int[] newarray is supported"); }
                else if (!Word_SMS(luokan_nimi_SMS(명짧()), "java/lang/String")) virhe_ARVO("only String[] anewarray is supported");
                int kesto_ARVO = 빼기(1); 넣기(jakaa_Tallennus(ARVO == 188 ? 2 : 3, kesto_ARVO), 2); continue;
            }
            if (ARVO == 190) {
                int viite = 빼기(2);
                if (viite < 1 || viite >= keko_lopettaa_puhelu_toimi - 1 || (keko_ARVO[viite] != 2 && keko_ARVO[viite] != 3)) virhe_ARVO("null or invalid array");
                else 넣기(keko_ARVO[viite + 1], 1); continue;
            }
            if (ARVO == 192) {
                int Nimi = luokan_nimi_SMS(명짧()), viite = 빼기(2);
                if (!Word_SMS(Nimi, "java/lang/String")) virhe_ARVO("unsupported checkcast");
                else if (viite != 0) objekti_ARVO(viite, 1);
                넣기(viite, 2); continue;
            }
            virhe_ARVO("unsupported bytecode");
        }
    }
    public static int Suorita_2() {
        if (käyttäjätila.인수개수() == 1 && 자바도구.같음(käyttäjätila.argumentit(0), "-version")) {
            käyttäjätila.Kirjoitus("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (käyttäjätila.인수개수() < 1) { käyttäjätila.Kirjoitus("Usage: java CLASS [ARGS]\n"); return 2; }
        int kesto_ARVO = 자바도구.Nimi(tiedostonimi_SMS, käyttäjätila.argumentit(0));
        if (kesto_ARVO < 1 || kesto_ARVO > 57) { käyttäjätila.Kirjoitus("java: invalid class name\n"); return 2; }
        tiedostonimi_SMS[kesto_ARVO] = '.'; tiedostonimi_SMS[kesto_ARVO + 1] = 'c'; tiedostonimi_SMS[kesto_ARVO + 2] = 'l'; tiedostonimi_SMS[kesto_ARVO + 3] = 'a'; tiedostonimi_SMS[kesto_ARVO + 4] = 's'; tiedostonimi_SMS[kesto_ARVO + 5] = 's';
        Koko = käyttäjätila.lukea_Tiedosto(tiedostonimi_SMS, tiedoston_nimi);
        if (Koko < 0) { käyttäjätila.Kirjoitus("java: cannot read class: "); 자바도구.kirjoitus_numero(Koko); käyttäjätila.kirjoitus_merkki_ARVO(10); return 1; }
        lukea_Luokka(); if (VIRHE) return 1;
        int merkki_nimi = vakio_SMS(luokan_nimi);
        if (!VIRHE && keko_ARVO[merkki_nimi + 1] != kesto_ARVO) virhe_ARVO("class name does not match file");
        for (int numero = 0; numero < kesto_ARVO && !VIRHE; numero++) if (keko_ARVO[merkki_nimi + 2 + numero] != tiedostonimi_SMS[numero]) virhe_ARVO("class name does not match file");
        int aloituskohta_ARVO = -1;
        for (int numero = 0; numero < menetelmä_LASKE; numero++) if (Word_SMS(menetelmä_nimi_SMS[numero], "main") && Word_SMS(menetelmä_TYYPPI[numero], "([Ljava/lang/String;)V") && (menetelmä_pääsy[numero] & 9) == 9) aloituskohta_ARVO = numero;
        if (aloituskohta_ARVO < 0) virhe_ARVO("public static void main(String[] args) required");
        if (VIRHE) return 1;
        int argumentit = jakaa_Tallennus(3, käyttäjätila.인수개수() - 1);
        for (int numero = 1; numero < käyttäjätila.인수개수() && !VIRHE; numero++) keko_ARVO[argumentit + 1 + numero] = isäntä_merkki(käyttäjätila.argumentit(numero));
        kuva_INDEKSI = 0; kuva_menetelmä[0] = aloituskohta_ARVO; kuva_toimi[0] = menetelmä_alku[aloituskohta_ARVO]; paikallinen_ARVO[0] = argumentit; paikallinen_TYYPPI[0] = 2;
        Suorita_komento(); return VIRHE ? 1 : 0;
    }
}
