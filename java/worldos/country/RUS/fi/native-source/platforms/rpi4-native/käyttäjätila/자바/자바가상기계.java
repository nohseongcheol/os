// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. tiedoston_nimi/operandi_Pino/viite/haara 경계를 Suorita_komento 중 검사한다. */
public final class 자바가상기계 {
    static int[] tiedoston_nimi = new int[16 * 16384], väliaikainen_tiedosto = new int[16384], tiedostonimi_SMS = new int[512];
    static int[] vakio_tunnus = new int[8192], 상가 = new int[8192], vakio_SEKUNNIT_ARVO = new int[8192], merkkijono_viite = new int[8192];
    static int[] menetelmä_nimi_SMS = new int[512], menetelmä_TYYPPI = new int[512], menetelmä_pääsy = new int[512], menetelmä_omistaja = new int[512];
    static int[] menetelmä_alku = new int[512], menetelmä_lopettaa_puhelu = new int[512], menetelmä_Pino = new int[512], 함수지역 = new int[512];
    static int[] menetelmä_argumentti_LASKE = new int[512], menetelmä_argumentti_TYYPPI = new int[8192], menetelmä_palauttaa = new int[512];
    static int[] rajattu_alue_ARVO = new int[16 * 16384];
    static int[] paikallinen_ARVO = new int[16384], paikallinen_TYYPPI = new int[16384], operandi_Pino_ARVO = new int[16384], operandi_Pino_TYYPPI = new int[16384];
    static int[] kuva_menetelmä = new int[128], kuva_toimi = new int[128], kuva_Pino = new int[128], kuva_käsky = new int[128], alustaa_kuva = new int[128];
    static int[] Luokka_Määritelmä_nimi = new int[16], Luokka_Määritelmä_muuttaa_kokoa = new int[16], Luokka_Määritelmä_pää = new int[16], Luokka_Määritelmä_Tila = new int[16], Luokka_paikka_LASKE = new int[16], alustaa_Luokka_Määritelmä = new int[16];
    static int[] Luokka_liittymä = new int[16 * 16], Luokka_liittymä_LASKE = new int[16];
    static int[] paikka_nimi = new int[512], paikka_TYYPPI = new int[512], paikka_omistaja = new int[512], paikka_oikeudet = new int[512], paikka_toimi = new int[512], paikka_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] keko_ARVO = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], keko_viite = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], matriisielementti = new int[32768], Store_kokonaisluku = new int[256];
    static int Koko, lukea_toimi, menetelmä_LASKE, luokan_nimi, kuva_INDEKSI = -1, keko_lopettaa_puhelu_toimi = 1, palauttaa_TYYPPI;
    static int Luokka_Määritelmä_LASKE, paikka_LASKE, 잡기수, 현재읽는종, 던진객체, 잠시수, näyttö_LASKE, perintä_LASKE;
    static int nykyinen_säie, säikeiden_määrä = 1, merkintä_Luokka_Määritelmä;
    static int[] säie_kuva = new int[4], säie_Tila = new int[4], säie_objekti = new int[4], säie_kohde = new int[4], 가닥대기 = new int[4];
    static boolean VIRHE, muutospyyntö;
    static int[] lukita_omistaja = new int[32768], 잠금깊이 = new int[32768], kuva_lukita = new int[128], Luokka_lukita = new int[16], Luokka_säie = new int[16];

    static void virhe_ARVO(String Word_SMS) {
        if (VIRHE) return;
        int alue_KOODI = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) alue_KOODI = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) alue_KOODI = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) alue_KOODI = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) alue_KOODI = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) alue_KOODI = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) alue_KOODI = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) alue_KOODI = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) alue_KOODI = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) alue_KOODI = 15;
        if (alue_KOODI != 0 && kuva_INDEKSI >= 0) { 예외던짐(alue_KOODI, Word_SMS); return; }
        käyttäjätila.Kirjoitus("JVM error: "); käyttäjätila.Kirjoitus(Word_SMS); käyttäjätila.kirjoitus_merkki_ARVO(10); VIRHE = true;
    }
    static boolean leikata(int Suorita_2, int kesto_ARVO) {
        if (Suorita_2 < 0 || Suorita_2 >= tiedoston_nimi.length || kesto_ARVO < 0) return false;
        int Luokka_Määritelmä = Suorita_2 / 16384;
        return Suorita_2 % 16384 <= Luokka_Määritelmä_muuttaa_kokoa[Luokka_Määritelmä] && kesto_ARVO <= Luokka_Määritelmä_muuttaa_kokoa[Luokka_Määritelmä] - Suorita_2 % 16384;
    }
    static int tavu_ARVO() {
        if (!leikata(lukea_toimi, 1)) { virhe_ARVO("truncated class file"); return 0; }
        return tiedoston_nimi[lukea_toimi++];
    }
    static int 짧은수() { return tavu_ARVO() << 8 | tavu_ARVO(); }
    static int kokonaisluku() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int kesto_ARVO) { if (!leikata(lukea_toimi, kesto_ARVO)) virhe_ARVO("invalid attribute size"); else lukea_toimi += kesto_ARVO; }
    static boolean sekki_vakio(int numero, int 종류) {
        if (numero <= 0 || numero >= vakio_tunnus.length || vakio_tunnus[numero] != 종류) { virhe_ARVO("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_alue(int Suorita_2, int kesto_ARVO, String Word_SMS) {
        if (!leikata(Suorita_2, kesto_ARVO)) return false;
        int lukea_kohdistin = Suorita_2, 끝 = Suorita_2 + kesto_ARVO;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Word_SMS.length(); Loop_INDEKSI++) {
            int merkkikoodi = Word_SMS.charAt(Loop_INDEKSI);
            if (merkkikoodi > 0 && merkkikoodi < 128) { if (lukea_kohdistin >= 끝 || tiedoston_nimi[lukea_kohdistin++] != merkkikoodi) return false; }
            else if (merkkikoodi < 2048) {
                if (lukea_kohdistin + 2 > 끝 || tiedoston_nimi[lukea_kohdistin++] != (192 | (merkkikoodi >> 6)) || tiedoston_nimi[lukea_kohdistin++] != (128 | (merkkikoodi & 63))) return false;
            } else if (lukea_kohdistin + 3 > 끝 || tiedoston_nimi[lukea_kohdistin++] != (224 | (merkkikoodi >> 12)) || tiedoston_nimi[lukea_kohdistin++] != (128 | ((merkkikoodi >> 6) & 63)) || tiedoston_nimi[lukea_kohdistin++] != (128 | (merkkikoodi & 63))) return false;
        }
        return lukea_kohdistin == 끝;
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
    static int lukea_vakio_INDEKSI() { int ARVO = 짧은수(); return ARVO == 0 ? 0 : 현재읽는종 * 512 + ARVO; }
    static int lukea_toimintokoodi_vakio() { return menetelmä_omistaja[kuva_menetelmä[kuva_INDEKSI]] * 512 + 명짧(); }
    static void ohita_määrite() {
        int kohde_LASKE = 짧은수();
        for (int numero = 0; numero < kohde_LASKE && !VIRHE; numero++) { sekki_vakio(lukea_vakio_INDEKSI(), 1); 건너(kokonaisluku()); }
    }
    static int komento_kesto(int ARVO) {
        if (ARVO == 16 || ARVO == 18 || ARVO == 21 || ARVO == 25 || ARVO == 54 || ARVO == 58 || ARVO == 188) return 2;
        if (ARVO == 17 || ARVO == 19 || ARVO == 132 || ARVO >= 153 && ARVO <= 167
            || ARVO >= 178 && ARVO <= 184 || ARVO == 187 || ARVO == 189 || ARVO == 192 || ARVO == 193 || ARVO == 198 || ARVO == 199) return 3;
        if (ARVO == 185 || ARVO == 200) return 5;
        if (ARVO >= 0 && ARVO <= 8 || ARVO >= 26 && ARVO <= 29 || ARVO >= 42 && ARVO <= 46 || ARVO >= 50 && ARVO <= 53
            || ARVO >= 59 && ARVO <= 62 || ARVO >= 75 && ARVO <= 79 || ARVO >= 83 && ARVO <= 95
            || ARVO == 96 || ARVO == 100 || ARVO == 104 || ARVO == 108 || ARVO == 112 || ARVO == 116
            || ARVO == 120 || ARVO == 122 || ARVO == 124 || ARVO == 126 || ARVO == 128 || ARVO == 130
            || ARVO >= 145 && ARVO <= 147 || ARVO == 172 || ARVO == 176 || ARVO == 177 || ARVO == 190 || ARVO == 191
            || ARVO == 194 || ARVO == 195) return 1;
        return 0;
    }
    static int toimi_kokonaisluku(int lukea_kohdistin) {
        if (!leikata(lukea_kohdistin, 4)) { virhe_ARVO("truncated bytecode operand"); return 0; }
        return tiedoston_nimi[lukea_kohdistin] << 24 | tiedoston_nimi[lukea_kohdistin + 1] << 16 | tiedoston_nimi[lukea_kohdistin + 2] << 8 | tiedoston_nimi[lukea_kohdistin + 3];
    }
    static int lukea_kesto(int lukea_kohdistin, int Suorita_2, int 끝) {
        int ARVO = tiedoston_nimi[lukea_kohdistin], kesto_ARVO = komento_kesto(ARVO);
        if (ARVO == 170 || ARVO == 171) {
            int PERUS_toimi = lukea_kohdistin + 1;
            while ((PERUS_toimi - Suorita_2) % 4 != 0) PERUS_toimi++;
            if (끝 - PERUS_toimi < (ARVO == 170 ? 12 : 8)) return 0;
            int merkintä_LASKE = ARVO == 170 ? toimi_kokonaisluku(PERUS_toimi + 8) - toimi_kokonaisluku(PERUS_toimi + 4) + 1 : toimi_kokonaisluku(PERUS_toimi + 4);
            if (merkintä_LASKE < 0 || merkintä_LASKE > 2048) return 0;
            kesto_ARVO = PERUS_toimi - lukea_kohdistin + (ARVO == 170 ? 12 + 4 * merkintä_LASKE : 8 + 8 * merkintä_LASKE);
        }
        if (ARVO == 196 && lukea_kohdistin + 1 < 끝) {
            int Word_data = tiedoston_nimi[lukea_kohdistin + 1]; kesto_ARVO = Word_data == 132 ? 6 : (Word_data == 21 || Word_data == 25 || Word_data == 54 || Word_data == 58) ? 4 : 0;
        }
        return kesto_ARVO > 0 && kesto_ARVO <= 끝 - lukea_kohdistin ? kesto_ARVO : 0;
    }
    static void sekki_kohde_ARVO(int kohde_ARVO, int funktio_ARVO) {
        if (kohde_ARVO < menetelmä_alku[funktio_ARVO] || kohde_ARVO >= menetelmä_lopettaa_puhelu[funktio_ARVO] || rajattu_alue_ARVO[kohde_ARVO] != funktio_ARVO + 1) virhe_ARVO("invalid branch target");
    }
    static void lukea_Luokka(int Luokka_Määritelmä) {
        현재읽는종 = Luokka_Määritelmä; lukea_toimi = Luokka_Määritelmä * 16384; Koko = lukea_toimi + Luokka_Määritelmä_muuttaa_kokoa[Luokka_Määritelmä];
        if (kokonaisluku() != 0xcafebabe) { virhe_ARVO("not a class file"); return; }
        int 부판 = 짧은수(), versio_ARVO = 짧은수();
        if (versio_ARVO < 45 || versio_ARVO > 52 || 부판 != 0) { virhe_ARVO("supported class versions: 45..52, minor 0"); return; }
        int vakio_LASKE = 짧은수(), PERUS_toimi = Luokka_Määritelmä * 512;
        if (vakio_LASKE < 1 || vakio_LASKE > 512) { virhe_ARVO("constant pool limit (511)"); return; }
        for (int merkintä_LASKE = 1; merkintä_LASKE < vakio_LASKE && !VIRHE; merkintä_LASKE++) {
            int numero = PERUS_toimi + merkintä_LASKE, 종류 = tavu_ARVO(); vakio_tunnus[numero] = 종류;
            if (종류 == 1) { vakio_SEKUNNIT_ARVO[numero] = 짧은수(); 상가[numero] = lukea_toimi; 건너(vakio_SEKUNNIT_ARVO[numero]); }
            else if (종류 == 3) 상가[numero] = kokonaisluku();
            else if (종류 == 7 || 종류 == 8) 상가[numero] = lukea_vakio_INDEKSI();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[numero] = lukea_vakio_INDEKSI(); vakio_SEKUNNIT_ARVO[numero] = lukea_vakio_INDEKSI(); }
            else virhe_ARVO("unsupported constant type");
        }
        int lupa_ARVO = 짧은수();
        if ((lupa_ARVO & (0x2000 | 0x4000)) != 0) virhe_ARVO("annotation/enum class unsupported");
        Luokka_Määritelmä_nimi[Luokka_Määritelmä] = luokan_nimi_SMS(lukea_vakio_INDEKSI());
        Luokka_Määritelmä_pää[Luokka_Määritelmä] = luokan_nimi_SMS(lukea_vakio_INDEKSI());
        int liittymä_LASKE = 짧은수(); if (liittymä_LASKE > 16) { virhe_ARVO("interface count limit"); return; }
        Luokka_liittymä_LASKE[Luokka_Määritelmä] = liittymä_LASKE;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < liittymä_LASKE; Loop_INDEKSI++) Luokka_liittymä[Luokka_Määritelmä * 16 + Loop_INDEKSI] = luokan_nimi_SMS(lukea_vakio_INDEKSI());
        int kenttä_LASKE = 짧은수();
        if (kenttä_LASKE > 512 - paikka_LASKE) { virhe_ARVO("field count limit (512)"); return; }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < kenttä_LASKE && !VIRHE; Loop_INDEKSI++) {
            int Tiedosto_INDEKSI = paikka_LASKE++; paikka_omistaja[Tiedosto_INDEKSI] = Luokka_Määritelmä; paikka_oikeudet[Tiedosto_INDEKSI] = 짧은수(); paikka_nimi[Tiedosto_INDEKSI] = lukea_vakio_INDEKSI(); paikka_TYYPPI[Tiedosto_INDEKSI] = lukea_vakio_INDEKSI();
            sekki_vakio(paikka_nimi[Tiedosto_INDEKSI], 1); sekki_vakio(paikka_TYYPPI[Tiedosto_INDEKSI], 1);
            int 보존값 = lukea_toimi; lukea_toimi = 상가[paikka_TYYPPI[Tiedosto_INDEKSI]]; int alue_KOODI = 서술형(lukea_toimi + vakio_SEKUNNIT_ARVO[paikka_TYYPPI[Tiedosto_INDEKSI]], false); lukea_toimi = 보존값;
            if ((paikka_oikeudet[Tiedosto_INDEKSI] & 8) == 0) paikka_toimi[Tiedosto_INDEKSI] = Luokka_paikka_LASKE[Luokka_Määritelmä]++;
            int määrite_data = 짧은수();
            for (int sisäliitos_toimi = 0; sisäliitos_toimi < määrite_data && !VIRHE; sisäliitos_toimi++) {
                int nimi_vakio = lukea_vakio_INDEKSI(), kelvollinen_kesto = kokonaisluku();
                if (Word_SMS(nimi_vakio, "ConstantValue") && kelvollinen_kesto == 2) {
                    int data_ARVO = lukea_vakio_INDEKSI();
                    if (alue_KOODI == 1 && sekki_vakio(data_ARVO, 3)) paikka_data[Tiedosto_INDEKSI] = 상가[data_ARVO];
                    else if (alue_KOODI == 2 && sekki_vakio(data_ARVO, 8)) paikka_data[Tiedosto_INDEKSI] = vakio_SMS(상가[data_ARVO]);
                } else 건너(kelvollinen_kesto);
            }
        }
        int kohde_LASKE = 짧은수();
        if (kohde_LASKE > 512 - menetelmä_LASKE) { virhe_ARVO("method count limit (512)"); return; }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < kohde_LASKE && !VIRHE; Loop_INDEKSI++) {
            int numero = menetelmä_LASKE++; menetelmä_omistaja[numero] = Luokka_Määritelmä;
            menetelmä_pääsy[numero] = 짧은수(); menetelmä_nimi_SMS[numero] = lukea_vakio_INDEKSI(); menetelmä_TYYPPI[numero] = lukea_vakio_INDEKSI();
            sekki_vakio(menetelmä_nimi_SMS[numero], 1); 서술읽기(numero);
            if ((menetelmä_pääsy[numero] & 8) == 0) {
                if (menetelmä_argumentti_LASKE[numero] == 16) { virhe_ARVO("too many instance method arguments"); return; }
                for (int Vertailu_toimi = menetelmä_argumentti_LASKE[numero]; Vertailu_toimi > 0; Vertailu_toimi--) menetelmä_argumentti_TYYPPI[numero * 16 + Vertailu_toimi] = menetelmä_argumentti_TYYPPI[numero * 16 + Vertailu_toimi - 1];
                menetelmä_argumentti_TYYPPI[numero * 16] = 2; menetelmä_argumentti_LASKE[numero]++;
            }
            if ((menetelmä_pääsy[numero] & 0x100) != 0) virhe_ARVO("user native method unsupported");
            if (Word_SMS(menetelmä_nimi_SMS[numero], "<clinit>")) alustaa_Luokka_Määritelmä[Luokka_Määritelmä] = numero + 1;
            for (int etukamera_ARVO = 0; etukamera_ARVO < numero; etukamera_ARVO++) if (menetelmä_omistaja[etukamera_ARVO] == Luokka_Määritelmä && kohdistus_Word(menetelmä_nimi_SMS[etukamera_ARVO], menetelmä_nimi_SMS[numero]) && kohdistus_Word(menetelmä_TYYPPI[etukamera_ARVO], menetelmä_TYYPPI[numero])) virhe_ARVO("duplicate method");
            int määrite_LASKE = 짧은수();
            for (int määritteen_arvo = 0; määritteen_arvo < määrite_LASKE && !VIRHE; määritteen_arvo++) {
                int Nimi = lukea_vakio_INDEKSI(), kesto_ARVO = kokonaisluku(), Suorita_2 = lukea_toimi;
                if (!leikata(Suorita_2, kesto_ARVO)) { virhe_ARVO("truncated method attribute"); break; }
                if (Word_SMS(Nimi, "Code")) {
                    if (menetelmä_alku[numero] != 0) virhe_ARVO("duplicate Code attribute");
                    menetelmä_Pino[numero] = 짧은수(); 함수지역[numero] = 짧은수(); int KOODI_kesto = kokonaisluku();
                    if (menetelmä_Pino[numero] > 128 || 함수지역[numero] > 128 || 함수지역[numero] < menetelmä_argumentti_LASKE[numero]
                        || KOODI_kesto < 1 || KOODI_kesto > 8192) virhe_ARVO("method memory limits exceeded");
                    menetelmä_alku[numero] = lukea_toimi; 건너(KOODI_kesto); menetelmä_lopettaa_puhelu[numero] = lukea_toimi;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { virhe_ARVO("exception table limit"); return; }
                    for (int sisäliitos_toimi = 0; sisäliitos_toimi < 잡는수; sisäliitos_toimi++) {
                        int virhe_viite = 잡기수++; 잡기함수[virhe_viite] = numero;
                        잡기시작[virhe_viite] = menetelmä_alku[numero] + 짧은수(); 잡기끝[virhe_viite] = menetelmä_alku[numero] + 짧은수();
                        잡기위치[virhe_viite] = menetelmä_alku[numero] + 짧은수(); int 부호값 = lukea_vakio_INDEKSI(); 잡기종[virhe_viite] = 부호값 == 0 ? 0 : luokan_nimi_SMS(부호값);
                    }
                    ohita_määrite();
                    if (lukea_toimi != Suorita_2 + kesto_ARVO) virhe_ARVO("Code attribute size mismatch");
                } else 건너(kesto_ARVO);
            }
            if ((menetelmä_pääsy[numero] & 0x400) != 0) continue;
            if (menetelmä_alku[numero] == 0) virhe_ARVO("missing Code attribute");
            int paikka_merkintä = menetelmä_alku[numero];
            while (paikka_merkintä < menetelmä_lopettaa_puhelu[numero] && !VIRHE) {
                int kesto_ARVO = lukea_kesto(paikka_merkintä, menetelmä_alku[numero], menetelmä_lopettaa_puhelu[numero]);
                if (kesto_ARVO == 0) { virhe_ARVO("unsupported or truncated bytecode"); break; }
                rajattu_alue_ARVO[paikka_merkintä] = numero + 1; paikka_merkintä += kesto_ARVO;
            }
            paikka_merkintä = menetelmä_alku[numero];
            while (paikka_merkintä < menetelmä_lopettaa_puhelu[numero] && !VIRHE) {
                int ARVO = tiedoston_nimi[paikka_merkintä];
                if (ARVO >= 153 && ARVO <= 167 || ARVO == 198 || ARVO == 199) sekki_kohde_ARVO(paikka_merkintä + (short)(tiedoston_nimi[paikka_merkintä + 1] << 8 | tiedoston_nimi[paikka_merkintä + 2]), numero);
                if (ARVO == 200) sekki_kohde_ARVO(paikka_merkintä + toimi_kokonaisluku(paikka_merkintä + 1), numero);
                if (ARVO == 170 || ARVO == 171) {
                    int lukea_kohdistin = paikka_merkintä + 1; while ((lukea_kohdistin - menetelmä_alku[numero]) % 4 != 0) lukea_kohdistin++;
                    sekki_kohde_ARVO(paikka_merkintä + toimi_kokonaisluku(lukea_kohdistin), numero);
                    int merkintä_LASKE = ARVO == 170 ? toimi_kokonaisluku(lukea_kohdistin + 8) - toimi_kokonaisluku(lukea_kohdistin + 4) + 1 : toimi_kokonaisluku(lukea_kohdistin + 4);
                    lukea_kohdistin += ARVO == 170 ? 12 : 8;
                    for (int sisäliitos_toimi = 0; sisäliitos_toimi < merkintä_LASKE; sisäliitos_toimi++) sekki_kohde_ARVO(paikka_merkintä + toimi_kokonaisluku(lukea_kohdistin + sisäliitos_toimi * (ARVO == 170 ? 4 : 8) + (ARVO == 170 ? 0 : 4)), numero);
                }
                paikka_merkintä += lukea_kesto(paikka_merkintä, menetelmä_alku[numero], menetelmä_lopettaa_puhelu[numero]);
            }
            for (int sisäliitos_toimi = 0; sisäliitos_toimi < 잡기수; sisäliitos_toimi++) if (잡기함수[sisäliitos_toimi] == numero) {
                sekki_kohde_ARVO(잡기시작[sisäliitos_toimi], numero); sekki_kohde_ARVO(잡기위치[sisäliitos_toimi], numero);
                if (잡기끝[sisäliitos_toimi] != menetelmä_lopettaa_puhelu[numero]) sekki_kohde_ARVO(잡기끝[sisäliitos_toimi], numero);
                if (잡기시작[sisäliitos_toimi] >= 잡기끝[sisäliitos_toimi]) virhe_ARVO("invalid exception range");
            }
        }
        if (!VIRHE) ohita_määrite();
        if (lukea_toimi != Koko) virhe_ARVO("extra class file data");
    }
    static int jakaa_Tallennus(int 종류, int kesto_ARVO) { return 새기억(종류, kesto_ARVO); }
    static boolean objekti_ARVO(int viite, int 종류) {
        if (!tietojärjestelmät_kelvollinen_objekti(viite)) return false;
        if (keko_ARVO[viite] != 종류) { virhe_ARVO("object type mismatch"); return false; }
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
        if (palauttaa_TYYPPI == 2) suojata_ARVO(operandi_Pino_ARVO[paikka_merkintä]);
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
        if (kuva_INDEKSI % 32 == 31) { virhe_ARVO("call stack limit (32)"); return; }
        int Seuraava_kohde = kuva_INDEKSI + 1;
        for (int numero = 0; numero < 128; numero++) paikallinen_TYYPPI[Seuraava_kohde * 128 + numero] = 0;
        for (int numero = menetelmä_argumentti_LASKE[funktio_ARVO] - 1; numero >= 0; numero--) {
            paikallinen_ARVO[Seuraava_kohde * 128 + numero] = 빼기(menetelmä_argumentti_TYYPPI[funktio_ARVO * 16 + numero]); paikallinen_TYYPPI[Seuraava_kohde * 128 + numero] = menetelmä_argumentti_TYYPPI[funktio_ARVO * 16 + numero];
        }
        if (VIRHE) return;
        kuva_INDEKSI = Seuraava_kohde; alustaa_kuva[kuva_INDEKSI] = 0; kuva_menetelmä[kuva_INDEKSI] = funktio_ARVO; kuva_toimi[kuva_INDEKSI] = menetelmä_alku[funktio_ARVO]; kuva_Pino[kuva_INDEKSI] = 0;
    }
    static void palauttaa_KR(int TYYPPI_ARVO) {
        if (TYYPPI_ARVO != menetelmä_palauttaa[kuva_menetelmä[kuva_INDEKSI]]) { virhe_ARVO("return type mismatch"); return; }
        int ARVO = TYYPPI_ARVO == 0 ? 0 : 빼기(TYYPPI_ARVO);
        if (alustaa_kuva[kuva_INDEKSI] != 0) Luokka_Määritelmä_Tila[alustaa_kuva[kuva_INDEKSI] - 1] = 2;
        if (kuva_lukita[kuva_INDEKSI] != 0) { julkaista_lukita(kuva_lukita[kuva_INDEKSI]); kuva_lukita[kuva_INDEKSI] = 0; }
        kuva_INDEKSI--; if (kuva_INDEKSI >= nykyinen_säie * 32 && TYYPPI_ARVO != 0) 넣기(ARVO, TYYPPI_ARVO);
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
                if (ARVO < 1) { virhe_ARVO("invalid file stream path"); return; }
                virta_tiedostonimi[paikka_merkintä] = ARVO;
            }
            virta_tiedostonimi[kesto_ARVO] = 0;
            int 서술자 = käyttäjätila.파일서술자열기(virta_tiedostonimi, tulostuspaikka ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { virhe_ARVO("FileNotFoundException: file open failed"); return; }
            keko_ARVO[virta_ARVO + 2] = 서술자; keko_ARVO[virta_ARVO + 3] = 1;
            return;
        }
        if (komento != 182) { virhe_ARVO("invalid file stream invocation"); return; }
        if ((tulostuspaikka && Word_SMS(Nimi, "write") || !tulostuspaikka && Word_SMS(Nimi, "read"))
            && (Word_SMS(muoto_ARVO, tulostuspaikka ? "([B)V" : "([B)I") || Word_SMS(muoto_ARVO, tulostuspaikka ? "([BII)V" : "([BII)I"))) {
            boolean leikata_ARVO = Word_SMS(muoto_ARVO, tulostuspaikka ? "([BII)V" : "([BII)I");
            int merkintä_LASKE = leikata_ARVO ? 빼기(1) : 0, 시작점 = leikata_ARVO ? 빼기(1) : 0, data_MATRIISI = 빼기(2), objekti_viite = 빼기(2);
            if (!objekti_ARVO(data_MATRIISI, 20) || !objekti_ARVO(objekti_viite, 종류)) return;
            if (!leikata_ARVO) merkintä_LASKE = keko_ARVO[data_MATRIISI + 1];
            if (시작점 < 0 || merkintä_LASKE < 0 || 시작점 > keko_ARVO[data_MATRIISI + 1] - merkintä_LASKE) { 예외던짐(6, "file buffer bounds"); return; }
            if (keko_ARVO[objekti_viite + 3] == 0 || keko_ARVO[objekti_viite + 2] < 0) { virhe_ARVO("IOException: stream closed"); return; }
            int valmis_LASKE = 0;
            while (valmis_LASKE < merkintä_LASKE && !VIRHE) {
                int 반환값 = tulostuspaikka ? käyttäjätila.파일한바이트쓰기(keko_ARVO[objekti_viite + 2], keko_ARVO[data_MATRIISI + 2 + 시작점 + valmis_LASKE]) : käyttäjätila.파일한바이트읽기(keko_ARVO[objekti_viite + 2]);
                if (반환값 < 0) { virhe_ARVO(tulostuspaikka ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!tulostuspaikka && 반환값 == 256) break;
                if (!tulostuspaikka) keko_ARVO[data_MATRIISI + 2 + 시작점 + valmis_LASKE] = (byte)반환값;
                valmis_LASKE++;
            }
            if (!tulostuspaikka) 넣기(merkintä_LASKE != 0 && valmis_LASKE == 0 ? -1 : valmis_LASKE, 1);
            return;
        }
        if (tulostuspaikka && Word_SMS(Nimi, "flush") && Word_SMS(muoto_ARVO, "()V")) { int objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, 종류) && keko_ARVO[objekti_viite + 2] < 0) virhe_ARVO("IOException: stream closed"); return; }
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
            if (TULOS < -1) virhe_ARVO("IOException: read failed"); else 넣기(TULOS == 256 ? -1 : TULOS, 1);
        } else if (käyttäjätila.파일한바이트쓰기(서술자, ARVO) != 1) virhe_ARVO("IOException: write failed");
    }
    static void KUTSU_menetelmä(int INDEKSI, int komento) {
        if (INDEKSI <= 0 || INDEKSI >= vakio_tunnus.length || (vakio_tunnus[INDEKSI] != 10 && vakio_tunnus[INDEKSI] != 11)) { virhe_ARVO("invalid method reference"); return; }
        int omistaja_ARVO = luokan_nimi_SMS(상가[INDEKSI]), Nimi = viite_nimi(vakio_SEKUNNIT_ARVO[INDEKSI]), muoto_ARVO = viittauksen_tyyppi(vakio_SEKUNNIT_ARVO[INDEKSI]);
        if (VIRHE) return;
        if (기본호출(omistaja_ARVO, Nimi, muoto_ARVO, komento)) return;
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
        int Luokka_Määritelmä = ETSI_Luokka_Määritelmä(omistaja_ARVO); if (Luokka_Määritelmä < 0 || VIRHE) return;
        int Tiedosto_INDEKSI = ETSI_menetelmä(Luokka_Määritelmä, Nimi, muoto_ARVO);
        if (Tiedosto_INDEKSI < 0) {
            for (int merkkikoodi = Luokka_Määritelmä, merkintä_LASKE = 0; merkkikoodi >= 0 && merkintä_LASKE < 16; merkintä_LASKE++, merkkikoodi = pää_Luokka(merkkikoodi))
                if (Word_SMS(Luokka_Määritelmä_pää[merkkikoodi], "java/lang/Thread")) { 가닥호출(Nimi, muoto_ARVO, komento); return; }
            virhe_ARVO("NoSuchMethodError"); return;
        }
        if (((menetelmä_pääsy[Tiedosto_INDEKSI] & 8) != 0) != (komento == 184)) { virhe_ARVO("method static/instance mismatch"); return; }
        if (komento == 184) { if (!alustaa(menetelmä_omistaja[Tiedosto_INDEKSI], kuva_käsky[kuva_INDEKSI])) return; }
        else {
            int lukea_kohdistin = kuva_Pino[kuva_INDEKSI] - menetelmä_argumentti_LASKE[Tiedosto_INDEKSI];
            if (lukea_kohdistin < 0 || operandi_Pino_TYYPPI[kuva_INDEKSI * 128 + lukea_kohdistin] != 2) { virhe_ARVO("invalid method receiver"); return; }
            int objekti_viite = operandi_Pino_ARVO[kuva_INDEKSI * 128 + lukea_kohdistin];
            if (!tietojärjestelmät_kelvollinen_objekti(objekti_viite)) return;
            if (keko_ARVO[objekti_viite] < 32 || !종포함(keko_ARVO[objekti_viite] - 32, omistaja_ARVO)) { virhe_ARVO("method receiver type mismatch"); return; }
            if (komento != 183) Tiedosto_INDEKSI = ETSI_menetelmä(keko_ARVO[objekti_viite] - 32, Nimi, muoto_ARVO);
        }
        if (Tiedosto_INDEKSI < 0 || (menetelmä_pääsy[Tiedosto_INDEKSI] & 0x400) != 0) { virhe_ARVO("AbstractMethodError"); return; }
        int lukita_viite = 0;
        if ((menetelmä_pääsy[Tiedosto_INDEKSI] & 32) != 0) {
            if (komento == 184) { int merkkikoodi = menetelmä_omistaja[Tiedosto_INDEKSI]; if (Luokka_lukita[merkkikoodi] == 0) Luokka_lukita[merkkikoodi] = jakaa_Tallennus(8, 0); lukita_viite = Luokka_lukita[merkkikoodi]; }
            else lukita_viite = operandi_Pino_ARVO[kuva_INDEKSI * 128 + kuva_Pino[kuva_INDEKSI] - menetelmä_argumentti_LASKE[Tiedosto_INDEKSI]];
            if (!잠금얻기(lukita_viite)) { if (!VIRHE) kuva_toimi[kuva_INDEKSI] = kuva_käsky[kuva_INDEKSI]; return; }
        }
        호출(Tiedosto_INDEKSI); if (!VIRHE) kuva_lukita[kuva_INDEKSI] = lukita_viite;
    }
    static boolean 배열저장가능(int MATRIISI_viite, int data_ARVO) {
        if (data_ARVO == 0 || matriisielementti[MATRIISI_viite] == 0) return true;
        boolean 성공여부 = matriisielementti[MATRIISI_viite] == -1 ? (data_ARVO > 0 && data_ARVO < keko_lopettaa_puhelu_toimi && keko_ARVO[data_ARVO] == 1) : kohdistus_objekti(data_ARVO, matriisielementti[MATRIISI_viite]);
        if (!성공여부 && !VIRHE) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int MATRIISI_paikka(int viite, int alaindeksi_ARVO, int TYYPPI_ARVO) {
        if (!objekti_ARVO(viite, TYYPPI_ARVO)) return 0;
        if (alaindeksi_ARVO < 0 || alaindeksi_ARVO >= keko_ARVO[viite + 1]) { virhe_ARVO("ArrayIndexOutOfBoundsException"); return 0; }
        return viite + 2 + alaindeksi_ARVO;
    }
    static void Suorita_komento() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (VIRHE) { if (던진객체 != 0) kahva_poikkeus(); if (VIRHE || kuva_INDEKSI < nykyinen_säie * 32) break; }
            if (kuva_INDEKSI < nykyinen_säie * 32 || muutospyyntö || --조각 == 0) { if (!MUUTA_säie()) break; 조각 = 100; }
            if (kuva_INDEKSI == 0 && Luokka_Määritelmä_Tila[merkintä_Luokka_Määritelmä] != 2 && !alustaa(merkintä_Luokka_Määritelmä, kuva_toimi[kuva_INDEKSI])) continue;
            if (kuva_INDEKSI == nykyinen_säie * 32 && nykyinen_säie != 0 && (menetelmä_pääsy[kuva_menetelmä[kuva_INDEKSI]] & 32) != 0 && kuva_lukita[kuva_INDEKSI] == 0) {
                int objekti_viite = säie_kohde[nykyinen_säie]; if (!잠금얻기(objekti_viite)) { if (VIRHE) break; continue; } kuva_lukita[kuva_INDEKSI] = objekti_viite;
            }
            잠시수 = 0;
            if (--남음 == 0) { virhe_ARVO("instruction limit (500000)"); break; }
            int Suorita_2 = kuva_toimi[kuva_INDEKSI]; kuva_käsky[kuva_INDEKSI] = Suorita_2; int ARVO = lukea_toimintokoodi_tavu();
            if (VIRHE) break;
            if (ARVO == 0) continue;
            if (ARVO == 1) { 넣기(0, 2); continue; }
            if (ARVO >= 2 && ARVO <= 8) { 넣기(ARVO - 3, 1); continue; }
            if (ARVO == 16) { 넣기((byte)lukea_toimintokoodi_tavu(), 1); continue; }
            if (ARVO == 17) { 넣기((short)명짧(), 1); continue; }
            if (ARVO == 18 || ARVO == 19) {
                int numero = menetelmä_omistaja[kuva_menetelmä[kuva_INDEKSI]] * 512 + (ARVO == 18 ? lukea_toimintokoodi_tavu() : 명짧());
                if (numero <= 0 || numero >= vakio_tunnus.length) virhe_ARVO("invalid ldc constant");
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
            if (ARVO == 46 || ARVO >= 50 && ARVO <= 53) {
                int merkintä_toimi = 빼기(1), objekti_viite = 빼기(2), alue_KOODI = ARVO == 46 ? 2 : ARVO == 50 ? 3 : ARVO == 51 ? 20 : ARVO == 52 ? 22 : 23;
                if (ARVO == 51 && objekti_viite > 0 && objekti_viite < keko_lopettaa_puhelu_toimi && keko_ARVO[objekti_viite] == 21) alue_KOODI = 21;
                int lukea_kohdistin = MATRIISI_paikka(objekti_viite, merkintä_toimi, alue_KOODI); if (!VIRHE) 넣기(keko_ARVO[lukea_kohdistin], ARVO == 50 ? 2 : 1); continue;
            }
            if (ARVO == 79 || ARVO >= 83 && ARVO <= 86) {
                int merkintä_viite = 빼기(ARVO == 83 ? 2 : 1), merkintä_toimi = 빼기(1), objekti_viite = 빼기(2), alue_KOODI = ARVO == 79 ? 2 : ARVO == 83 ? 3 : ARVO == 84 ? 20 : ARVO == 85 ? 22 : 23;
                if (ARVO == 84 && objekti_viite > 0 && objekti_viite < keko_lopettaa_puhelu_toimi && keko_ARVO[objekti_viite] == 21) alue_KOODI = 21;
                int lukea_kohdistin = MATRIISI_paikka(objekti_viite, merkintä_toimi, alue_KOODI);
                if (!VIRHE && alue_KOODI == 3 && !배열저장가능(objekti_viite, merkintä_viite)) continue;
                if (!VIRHE) keko_ARVO[lukea_kohdistin] = alue_KOODI == 20 ? (byte)merkintä_viite : alue_KOODI == 21 ? merkintä_viite & 1 : alue_KOODI == 22 ? (char)merkintä_viite : alue_KOODI == 23 ? (short)merkintä_viite : merkintä_viite;
                continue;
            }
            if (ARVO >= 87 && ARVO <= 95) { Pino_käsky(ARVO); continue; }
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
            if (ARVO >= 178 && ARVO <= 181) { 필드호출(lukea_toimintokoodi_vakio(), ARVO, Suorita_2); continue; }
            if (ARVO >= 182 && ARVO <= 185) {
                int 부호값 = lukea_toimintokoodi_vakio();
                if (ARVO == 185) { int summa_LASKE = lukea_toimintokoodi_tavu(); if (summa_LASKE == 0 || lukea_toimintokoodi_tavu() != 0) { virhe_ARVO("invalid invokeinterface operands"); continue; } }
                KUTSU_menetelmä(부호값, ARVO); continue;
            }
            if (ARVO == 187) { 새객체(luokan_nimi_SMS(lukea_toimintokoodi_vakio()), Suorita_2); continue; }
            if (ARVO == 188 || ARVO == 189) {
                int alue_KOODI = 3, osa = 0;
                if (ARVO == 188) { int 임시값 = lukea_toimintokoodi_tavu(); alue_KOODI = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else osa = luokan_nimi_SMS(lukea_toimintokoodi_vakio());
                if (alue_KOODI == 0) { virhe_ARVO("unsupported primitive array type"); continue; }
                int kelvollinen_kesto = 빼기(1), objekti_viite = jakaa_Tallennus(alue_KOODI, kelvollinen_kesto); if (!VIRHE) matriisielementti[objekti_viite] = osa; 넣기(objekti_viite, 2); continue;
            }
            if (ARVO == 190) {
                int objekti_viite = 빼기(2);
                if (tietojärjestelmät_kelvollinen_objekti(objekti_viite)) { int Vertailu_toimi = keko_ARVO[objekti_viite]; if (Vertailu_toimi != 2 && Vertailu_toimi != 3 && (Vertailu_toimi < 20 || Vertailu_toimi > 23)) virhe_ARVO("not an array"); else 넣기(keko_ARVO[objekti_viite + 1], 1); }
                continue;
            }
            if (ARVO == 191) {
                int objekti_viite = 빼기(2); if (tietojärjestelmät_kelvollinen_objekti(objekti_viite)) { if (keko_ARVO[objekti_viite] != 9) virhe_ARVO("athrow requires supported Throwable"); else { 던진객체 = objekti_viite; VIRHE = true; } }
                continue;
            }
            if (ARVO == 192 || ARVO == 193) {
                int nimi_vakio = luokan_nimi_SMS(lukea_toimintokoodi_vakio()), objekti_viite = 빼기(2); boolean VASTINE = kohdistus_objekti(objekti_viite, nimi_vakio);
                if (ARVO == 193) 넣기(objekti_viite != 0 && VASTINE ? 1 : 0, 1);
                else { if (!VASTINE && !VIRHE) virhe_ARVO("ClassCastException"); 넣기(objekti_viite, 2); }
                continue;
            }
            if (ARVO == 170 || ARVO == 171) {
                int lukea_kohdistin = Suorita_2 + 1, Tiedosto_INDEKSI = kuva_menetelmä[kuva_INDEKSI], Avain_viite = 빼기(1);
                while ((lukea_kohdistin - menetelmä_alku[Tiedosto_INDEKSI]) % 4 != 0) lukea_kohdistin++;
                int kohde_OSOITE = toimi_kokonaisluku(lukea_kohdistin);
                if (ARVO == 170) { int 낮은값 = toimi_kokonaisluku(lukea_kohdistin + 4), 높은값 = toimi_kokonaisluku(lukea_kohdistin + 8); if (Avain_viite >= 낮은값 && Avain_viite <= 높은값) kohde_OSOITE = toimi_kokonaisluku(lukea_kohdistin + 12 + (Avain_viite - 낮은값) * 4); }
                else { int summa_LASKE = toimi_kokonaisluku(lukea_kohdistin + 4); for (int Loop_INDEKSI = 0; Loop_INDEKSI < summa_LASKE; Loop_INDEKSI++) if (toimi_kokonaisluku(lukea_kohdistin + 8 + Loop_INDEKSI * 8) == Avain_viite) kohde_OSOITE = toimi_kokonaisluku(lukea_kohdistin + 12 + Loop_INDEKSI * 8); }
                siirrä_ARVO_83b651b8(Suorita_2 + kohde_OSOITE); continue;
            }
            if (ARVO == 200) { siirrä_ARVO_83b651b8(Suorita_2 + toimi_kokonaisluku(Suorita_2 + 1)); continue; }
            if (ARVO == 194 || ARVO == 195) {
                int objekti_viite = 빼기(2);
                if (ARVO == 195) julkaista_lukita(objekti_viite);
                else if (!잠금얻기(objekti_viite) && !VIRHE) { 넣기(objekti_viite, 2); kuva_toimi[kuva_INDEKSI] = Suorita_2; }
                continue;
            }
            if (ARVO == 196) {
                int komento_KOODI = lukea_toimintokoodi_tavu(), merkintä_toimi = 명짧();
                if (komento_KOODI == 21 || komento_KOODI == 25) lukea_paikallinen(merkintä_toimi, komento_KOODI == 21 ? 1 : 2);
                else if (komento_KOODI == 54 || komento_KOODI == 58) kirjoitus_paikallinen(merkintä_toimi, komento_KOODI == 54 ? 1 : 2);
                else if (komento_KOODI == 132) { int SAMA_ARVO_ARVO = (short)명짧(); lukea_paikallinen(merkintä_toimi, 1); 넣기(빼기(1) + SAMA_ARVO_ARVO, 1); kirjoitus_paikallinen(merkintä_toimi, 1); }
                else virhe_ARVO("unsupported wide opcode");
                continue;
            }
            virhe_ARVO("unsupported bytecode");
        }
    }
    static int ETSI_Luokka_Määritelmä(int Nimi) {
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Luokka_Määritelmä_LASKE; Loop_INDEKSI++) if (Luokka_Määritelmä_nimi[Loop_INDEKSI] != 0 && kohdistus_Word(Luokka_Määritelmä_nimi[Loop_INDEKSI], Nimi)) return Loop_INDEKSI;
        return ladata_Luokka_Määritelmä(vakio_SMS(Nimi));
    }
    static int ladata_Luokka_Määritelmä(int nimi_merkkijono) {
        if (!objekti_ARVO(nimi_merkkijono, 1)) return -1;
        int kesto_ARVO = keko_ARVO[nimi_merkkijono + 1];
        if (kesto_ARVO < 1 || kesto_ARVO > 505 || Luokka_Määritelmä_LASKE == 16) { virhe_ARVO("class name/count limit"); return -1; }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < kesto_ARVO; Loop_INDEKSI++) { int merkkikoodi = keko_ARVO[nimi_merkkijono + 2 + Loop_INDEKSI]; tiedostonimi_SMS[Loop_INDEKSI] = merkkikoodi == '/' ? '.' : merkkikoodi; }
        tiedostonimi_SMS[kesto_ARVO] = '.'; tiedostonimi_SMS[kesto_ARVO + 1] = 'c'; tiedostonimi_SMS[kesto_ARVO + 2] = 'l'; tiedostonimi_SMS[kesto_ARVO + 3] = 'a'; tiedostonimi_SMS[kesto_ARVO + 4] = 's'; tiedostonimi_SMS[kesto_ARVO + 5] = 's'; tiedostonimi_SMS[kesto_ARVO + 6] = 0;
        int Koko = käyttäjätila.lukea_Tiedosto(tiedostonimi_SMS, väliaikainen_tiedosto);
        if (Koko < 0) { virhe_ARVO("ClassNotFoundException"); return -1; }
        int Luokka_Määritelmä = Luokka_Määritelmä_LASKE++; Luokka_Määritelmä_muuttaa_kokoa[Luokka_Määritelmä] = Koko;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Koko; Loop_INDEKSI++) tiedoston_nimi[Luokka_Määritelmä * 16384 + Loop_INDEKSI] = väliaikainen_tiedosto[Loop_INDEKSI];
        lukea_Luokka(Luokka_Määritelmä); if (VIRHE) return -1;
        int todellinen_data = vakio_SMS(Luokka_Määritelmä_nimi[Luokka_Määritelmä]);
        if (!tekstit_samat(todellinen_data, nimi_merkkijono, true)) { virhe_ARVO("class name does not match file"); return -1; }
        int pää_ARVO = Luokka_Määritelmä_pää[Luokka_Määritelmä];
        if (pää_ARVO != 0 && !Word_SMS(pää_ARVO, "java/lang/Object") && !Word_SMS(pää_ARVO, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 yrittää_uudelleen_ARVO 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = ETSI_Luokka_Määritelmä(pää_ARVO);
            if (VIRHE || 위 < 0) return -1;
            int lukea_kohdistin = 위, vaihe_LASKE = 0;
            while (lukea_kohdistin >= 0 && vaihe_LASKE++ < 16) {
                if (lukea_kohdistin == Luokka_Määritelmä) { virhe_ARVO("cyclic inheritance"); return -1; }
                lukea_kohdistin = pää_Luokka(lukea_kohdistin);
            }
            int 시작변위 = Luokka_paikka_LASKE[위];
            for (int Tiedosto_INDEKSI = 0; Tiedosto_INDEKSI < paikka_LASKE; Tiedosto_INDEKSI++) if (paikka_omistaja[Tiedosto_INDEKSI] == Luokka_Määritelmä && (paikka_oikeudet[Tiedosto_INDEKSI] & 8) == 0) paikka_toimi[Tiedosto_INDEKSI] += 시작변위;
            Luokka_paikka_LASKE[Luokka_Määritelmä] += 시작변위;
        }
        return Luokka_Määritelmä;
    }
    static int pää_Luokka(int Luokka_Määritelmä) {
        int Nimi = Luokka_Määritelmä_pää[Luokka_Määritelmä];
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Luokka_Määritelmä_LASKE; Loop_INDEKSI++) if (Nimi != 0 && Luokka_Määritelmä_nimi[Loop_INDEKSI] != 0 && kohdistus_Word(Luokka_Määritelmä_nimi[Loop_INDEKSI], Nimi)) return Loop_INDEKSI;
        return -1;
    }
    static int ETSI_menetelmä(int Luokka_Määritelmä, int Nimi, int muoto_ARVO) {
        for (int 깊이 = 0; Luokka_Määritelmä >= 0 && 깊이 < 16; 깊이++, Luokka_Määritelmä = pää_Luokka(Luokka_Määritelmä)) {
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < menetelmä_LASKE; Loop_INDEKSI++) if (menetelmä_omistaja[Loop_INDEKSI] == Luokka_Määritelmä && kohdistus_Word(menetelmä_nimi_SMS[Loop_INDEKSI], Nimi) && kohdistus_Word(menetelmä_TYYPPI[Loop_INDEKSI], muoto_ARVO)) return Loop_INDEKSI;
        }
        return -1;
    }
    static int nimi_menetelmä(int Luokka_Määritelmä, String Nimi, String muoto_ARVO) {
        for (int 깊이 = 0; Luokka_Määritelmä >= 0 && 깊이 < 16; 깊이++, Luokka_Määritelmä = pää_Luokka(Luokka_Määritelmä))
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < menetelmä_LASKE; Loop_INDEKSI++) if (menetelmä_omistaja[Loop_INDEKSI] == Luokka_Määritelmä && Word_SMS(menetelmä_nimi_SMS[Loop_INDEKSI], Nimi) && Word_SMS(menetelmä_TYYPPI[Loop_INDEKSI], muoto_ARVO)) return Loop_INDEKSI;
        return -1;
    }
    static int 형종류(int Nimi) { return tiedoston_nimi[상가[Nimi]] == 'L' || tiedoston_nimi[상가[Nimi]] == '[' ? 2 : 1; }
    static boolean alustaa(int Luokka_Määritelmä, int komento_alku) {
        if (Luokka_Määritelmä < 0 || VIRHE) return false;
        if (Luokka_Määritelmä_Tila[Luokka_Määritelmä] == 3) { virhe_ARVO("NoClassDefFoundError: initialization failed"); return false; }
        if (Luokka_Määritelmä_Tila[Luokka_Määritelmä] == 1 && Luokka_säie[Luokka_Määritelmä] != nykyinen_säie) { kuva_toimi[kuva_INDEKSI] = komento_alku; muutospyyntö = true; return false; }
        if (Luokka_Määritelmä_Tila[Luokka_Määritelmä] != 0) return true;
        int 위 = pää_Luokka(Luokka_Määritelmä);
        if (위 >= 0 && !alustaa(위, komento_alku)) return false;
        Luokka_Määritelmä_Tila[Luokka_Määritelmä] = 1; Luokka_säie[Luokka_Määritelmä] = nykyinen_säie;
        if (alustaa_Luokka_Määritelmä[Luokka_Määritelmä] != 0) {
            kuva_toimi[kuva_INDEKSI] = komento_alku;
            호출(alustaa_Luokka_Määritelmä[Luokka_Määritelmä] - 1); if (!VIRHE) alustaa_kuva[kuva_INDEKSI] = Luokka_Määritelmä + 1;
            return false;
        }
        Luokka_Määritelmä_Tila[Luokka_Määritelmä] = 2; return true;
    }
    static void 필드호출(int INDEKSI, int komento, int Suorita_2) {
        if (!sekki_vakio(INDEKSI, 9)) return;
        int omistaja_ARVO = luokan_nimi_SMS(상가[INDEKSI]), Nimi = viite_nimi(vakio_SEKUNNIT_ARVO[INDEKSI]), muoto_ARVO = viittauksen_tyyppi(vakio_SEKUNNIT_ARVO[INDEKSI]);
        if (Word_SMS(omistaja_ARVO, "java/lang/System") && (Word_SMS(Nimi, "out") || Word_SMS(Nimi, "err")) && Word_SMS(muoto_ARVO, "Ljava/io/PrintStream;") && komento == 178) { 넣기(-1, 2); return; }
        int Luokka_Määritelmä = ETSI_Luokka_Määritelmä(omistaja_ARVO); if (Luokka_Määritelmä < 0 || VIRHE) return;
        int 찾음 = -1;
        for (int lukea_kohdistin = Luokka_Määritelmä, 깊이 = 0; lukea_kohdistin >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, lukea_kohdistin = pää_Luokka(lukea_kohdistin))
            for (int Tiedosto_INDEKSI = 0; Tiedosto_INDEKSI < paikka_LASKE; Tiedosto_INDEKSI++) if (paikka_omistaja[Tiedosto_INDEKSI] == lukea_kohdistin && kohdistus_Word(paikka_nimi[Tiedosto_INDEKSI], Nimi) && kohdistus_Word(paikka_TYYPPI[Tiedosto_INDEKSI], muoto_ARVO)) 찾음 = Tiedosto_INDEKSI;
        if (찾음 < 0) { virhe_ARVO("NoSuchFieldError"); return; }
        boolean staattinen_ARVO = komento == 178 || komento == 179;
        if (staattinen_ARVO != ((paikka_oikeudet[찾음] & 8) != 0)) { virhe_ARVO("field static/instance mismatch"); return; }
        if (staattinen_ARVO && !alustaa(paikka_omistaja[찾음], Suorita_2)) return;
        int TYYPPI_ARVO = 형종류(muoto_ARVO), ARVO = 0;
        if (komento == 179 || komento == 181) ARVO = 빼기(TYYPPI_ARVO);
        if (staattinen_ARVO) { if (komento == 178) 넣기(paikka_data[찾음], TYYPPI_ARVO); else if (!VIRHE) paikka_data[찾음] = ARVO; return; }
        int objekti_viite = 빼기(2);
        if (!tietojärjestelmät_kelvollinen_objekti(objekti_viite)) return;
        if (keko_ARVO[objekti_viite] < 32 || !종포함(keko_ARVO[objekti_viite] - 32, omistaja_ARVO)) { virhe_ARVO("field receiver type mismatch"); return; }
        int 보관칸 = objekti_viite + 2 + paikka_toimi[찾음];
        if (komento == 180) 넣기(keko_ARVO[보관칸], TYYPPI_ARVO);
        else if (!VIRHE) { keko_ARVO[보관칸] = ARVO; keko_viite[보관칸] = TYYPPI_ARVO == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Luokka_Määritelmä, int Nimi) {
        for (int 중첩깊이 = 0; Luokka_Määritelmä >= 0 && 중첩깊이 < 16; 중첩깊이++, Luokka_Määritelmä = pää_Luokka(Luokka_Määritelmä)) {
            if (kohdistus_Word(Luokka_Määritelmä_nimi[Luokka_Määritelmä], Nimi) || (Luokka_Määritelmä_pää[Luokka_Määritelmä] != 0 && kohdistus_Word(Luokka_Määritelmä_pää[Luokka_Määritelmä], Nimi))) return true;
            for (int sisäliitos_toimi = 0; sisäliitos_toimi < Luokka_liittymä_LASKE[Luokka_Määritelmä]; sisäliitos_toimi++) if (kohdistus_Word(Luokka_liittymä[Luokka_Määritelmä * 16 + sisäliitos_toimi], Nimi)) return true;
        }
        return false;
    }
    static boolean tekstit_samat(int 첫값, int tavu_data, boolean polku_2) {
        if (첫값 == tavu_data) return true;
        if (첫값 <= 0 || tavu_data <= 0 || keko_ARVO[첫값] != 1 || keko_ARVO[tavu_data] != 1 || keko_ARVO[첫값 + 1] != keko_ARVO[tavu_data + 1]) return false;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < keko_ARVO[첫값 + 1]; Loop_INDEKSI++) {
            int x_koordinaatti = keko_ARVO[첫값 + 2 + Loop_INDEKSI], Y_koordinaatti = keko_ARVO[tavu_data + 2 + Loop_INDEKSI];
            if (polku_2) { if (x_koordinaatti == '.') x_koordinaatti = '/'; if (Y_koordinaatti == '.') Y_koordinaatti = '/'; }
            if (x_koordinaatti != Y_koordinaatti) return false;
        }
        return true;
    }
    static boolean tietojärjestelmät_kelvollinen_objekti(int objekti_viite) {
        if (objekti_viite == 0) { virhe_ARVO("NullPointerException"); return false; }
        if (objekti_viite < 1 || objekti_viite >= keko_lopettaa_puhelu_toimi || 힙폭[objekti_viite] < 2 || keko_ARVO[objekti_viite] == 0) { virhe_ARVO("invalid object reference"); return false; }
        return true;
    }
    static void suojata_ARVO(int objekti_viite) {
        if (objekti_viite > 0 && objekti_viite < keko_lopettaa_puhelu_toimi && 힙폭[objekti_viite] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekti_viite;
    }
    static void näyttää_ARVO(int objekti_viite) {
        if (objekti_viite > 0 && objekti_viite < keko_lopettaa_puhelu_toimi && 힙폭[objekti_viite] >= 2 && keko_ARVO[objekti_viite] != 0 && 힙표시[objekti_viite] == 0) {
            힙표시[objekti_viite] = 1; 표시대기[näyttö_LASKE++] = objekti_viite;
        }
    }
    static void 수거() {
        näyttö_LASKE = 0; perintä_LASKE++;
        for (int sekki_toimi = 1; sekki_toimi < keko_lopettaa_puhelu_toimi; sekki_toimi += 힙폭[sekki_toimi]) 힙표시[sekki_toimi] = 0;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkkijono_viite.length; Loop_INDEKSI++) näyttää_ARVO(merkkijono_viite[Loop_INDEKSI]);
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < paikka_LASKE; Loop_INDEKSI++) if ((paikka_oikeudet[Loop_INDEKSI] & 8) != 0 && 형종류(paikka_TYYPPI[Loop_INDEKSI]) == 2) näyttää_ARVO(paikka_data[Loop_INDEKSI]);
        for (int 임시값 = 0; 임시값 < säikeiden_määrä; 임시값++) {
            näyttää_ARVO(säie_objekti[임시값]); näyttää_ARVO(säie_kohde[임시값]);
            int 꼭대기자리 = 임시값 == nykyinen_säie ? kuva_INDEKSI : säie_kuva[임시값];
            for (int Tiedosto_INDEKSI = 임시값 * 32; Tiedosto_INDEKSI <= 꼭대기자리; Tiedosto_INDEKSI++) {
                for (int sisäliitos_toimi = 0; sisäliitos_toimi < 함수지역[kuva_menetelmä[Tiedosto_INDEKSI]]; sisäliitos_toimi++) if (paikallinen_TYYPPI[Tiedosto_INDEKSI * 128 + sisäliitos_toimi] == 2) näyttää_ARVO(paikallinen_ARVO[Tiedosto_INDEKSI * 128 + sisäliitos_toimi]);
                for (int sisäliitos_toimi = 0; sisäliitos_toimi < kuva_Pino[Tiedosto_INDEKSI]; sisäliitos_toimi++) if (operandi_Pino_TYYPPI[Tiedosto_INDEKSI * 128 + sisäliitos_toimi] == 2) näyttää_ARVO(operandi_Pino_ARVO[Tiedosto_INDEKSI * 128 + sisäliitos_toimi]);
            }
        }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 화면참조.length; Loop_INDEKSI++) näyttää_ARVO(화면참조[Loop_INDEKSI]);
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 나중수; Loop_INDEKSI++) näyttää_ARVO(나중실행[Loop_INDEKSI]);
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Store_kokonaisluku.length; Loop_INDEKSI++) näyttää_ARVO(Store_kokonaisluku[Loop_INDEKSI]);
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Luokka_Määritelmä_LASKE; Loop_INDEKSI++) näyttää_ARVO(Luokka_lukita[Loop_INDEKSI]);
        for (int sekki_toimi = 1; sekki_toimi < keko_lopettaa_puhelu_toimi; sekki_toimi += 힙폭[sekki_toimi]) if (잠금깊이[sekki_toimi] > 0) näyttää_ARVO(sekki_toimi);
        näyttää_ARVO(던진객체);
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 잠시수; Loop_INDEKSI++) näyttää_ARVO(잠시참조[Loop_INDEKSI]);
        while (näyttö_LASKE > 0) {
            int objekti_viite = 표시대기[--näyttö_LASKE], alue_KOODI = keko_ARVO[objekti_viite];
            for (int Loop_INDEKSI = objekti_viite + 2; Loop_INDEKSI < objekti_viite + 힙폭[objekti_viite]; Loop_INDEKSI++) if (alue_KOODI == 3 || alue_KOODI == 4 || keko_viite[Loop_INDEKSI] != 0) näyttää_ARVO(keko_ARVO[Loop_INDEKSI]);
        }
        for (int sekki_toimi = 1; sekki_toimi < keko_lopettaa_puhelu_toimi; sekki_toimi += 힙폭[sekki_toimi]) if (힙표시[sekki_toimi] == 0) keko_ARVO[sekki_toimi] = 0;
        for (int sekki_toimi = 1; sekki_toimi < keko_lopettaa_puhelu_toimi; sekki_toimi += 힙폭[sekki_toimi]) if (keko_ARVO[sekki_toimi] == 0) {
            while (sekki_toimi + 힙폭[sekki_toimi] < keko_lopettaa_puhelu_toimi && keko_ARVO[sekki_toimi + 힙폭[sekki_toimi]] == 0) { int Seuraava_toimi = sekki_toimi + 힙폭[sekki_toimi]; 힙폭[sekki_toimi] += 힙폭[Seuraava_toimi]; 힙폭[Seuraava_toimi] = 0; }
            if (sekki_toimi + 힙폭[sekki_toimi] == keko_lopettaa_puhelu_toimi) { keko_lopettaa_puhelu_toimi = sekki_toimi; break; }
        }
    }
    static int 새기억(int 종류, int kesto_ARVO) {
        if (kesto_ARVO < 0) { virhe_ARVO("NegativeArraySizeException"); return 0; }
        if (kesto_ARVO > keko_ARVO.length - 3) { virhe_ARVO("object heap exhausted"); return 0; }
        int 필요수 = kesto_ARVO + 2, objekti_viite = 0;
        if (필요수 <= keko_ARVO.length - keko_lopettaa_puhelu_toimi) { objekti_viite = keko_lopettaa_puhelu_toimi; keko_lopettaa_puhelu_toimi += 필요수; }
        else {
            수거();
            for (int lukea_kohdistin = 1; lukea_kohdistin < keko_lopettaa_puhelu_toimi; lukea_kohdistin += 힙폭[lukea_kohdistin]) if (keko_ARVO[lukea_kohdistin] == 0 && 힙폭[lukea_kohdistin] >= 필요수) { objekti_viite = lukea_kohdistin; break; }
            if (objekti_viite != 0) {
                int 남은길이 = 힙폭[objekti_viite] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekti_viite + 필요수] = 남은길이; keko_ARVO[objekti_viite + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= keko_ARVO.length - keko_lopettaa_puhelu_toimi) { objekti_viite = keko_lopettaa_puhelu_toimi; keko_lopettaa_puhelu_toimi += 필요수; }
        }
        if (objekti_viite == 0) { virhe_ARVO("object heap exhausted"); return 0; }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 필요수; Loop_INDEKSI++) { keko_ARVO[objekti_viite + Loop_INDEKSI] = 0; keko_viite[objekti_viite + Loop_INDEKSI] = 0; 힙폭[objekti_viite + Loop_INDEKSI] = 0; }
        matriisielementti[objekti_viite] = 0;
        힙폭[objekti_viite] = 필요수; keko_ARVO[objekti_viite] = 종류; keko_ARVO[objekti_viite + 1] = kesto_ARVO; suojata_ARVO(objekti_viite); return objekti_viite;
    }
    static int poikkeus_Luokka(String nimi_vakio) {
        if (자바도구.같음(nimi_vakio, "java/lang/Throwable")) return 1;
        if (자바도구.같음(nimi_vakio, "java/lang/Exception")) return 2;
        if (자바도구.같음(nimi_vakio, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(nimi_vakio, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(nimi_vakio, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(nimi_vakio, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(nimi_vakio, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(nimi_vakio, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(nimi_vakio, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(nimi_vakio, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(nimi_vakio, "java/io/IOException")) return 11;
        if (자바도구.같음(nimi_vakio, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(nimi_vakio, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(nimi_vakio, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(nimi_vakio, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int poikkeus_vakio(int Nimi) {
        for (int Loop_INDEKSI = 1; Loop_INDEKSI <= 41; Loop_INDEKSI++) if (Word_SMS(Nimi, poikkeus_nimi(Loop_INDEKSI))) return Loop_INDEKSI;
        return 0;
    }
    static String poikkeus_nimi(int tili_ARVO) {
        if (tili_ARVO == 40) return "java/lang/InterruptedException";
        if (tili_ARVO == 41) return "suomi/oma/대기중단예외";
        if (tili_ARVO == 39) return "java/net/SocketException";
        if (tili_ARVO == 20) return "suomi/oma/poikkeus";
        if (tili_ARVO == 21) return "suomi/oma/suoritus_poikkeus";
        if (tili_ARVO == 22) return "suomi/oma/I_O_poikkeus";
        if (tili_ARVO == 23) return "suomi/oma/odottaa_AIKAKATKAISU_poikkeus";
        if (tili_ARVO == 24) return "suomi/oma/OSOITE_HAKU_poikkeus";
        if (tili_ARVO == 25) return "suomi/oma/파일없음예외";
        if (tili_ARVO == 26) return "suomi/oma/통신예외";
        if (tili_ARVO == 27) return "suomi/oma/pätemätön_argumentti_poikkeus";
        if (tili_ARVO == 28) return "suomi/oma/numero_muoto_virhe";
        if (tili_ARVO == 29) return "suomi/oma/범위예외";
        if (tili_ARVO == 30) return "suomi/oma/배열범위예외";
        if (tili_ARVO == 31) return "suomi/oma/문자열범위예외";
        if (tili_ARVO == 32) return "suomi/oma/TYHJÄ_viite_poikkeus";
        if (tili_ARVO == 33) return "suomi/oma/산술예외";
        if (tili_ARVO == 34) return "suomi/oma/Tila_poikkeus";
        if (tili_ARVO == 35) return "suomi/oma/TYYPPI_lähetys_poikkeus";
        if (tili_ARVO == 36) return "suomi/oma/음수배열크기예외";
        if (tili_ARVO == 37) return "suomi/oma/MATRIISI_Store_virhe";
        if (tili_ARVO == 38) return "suomi/oma/säie_Tila_poikkeus";
        if (tili_ARVO == 1) return "java/lang/Throwable"; if (tili_ARVO == 2) return "java/lang/Exception";
        if (tili_ARVO == 3) return "java/lang/RuntimeException"; if (tili_ARVO == 4) return "java/lang/ArithmeticException";
        if (tili_ARVO == 5) return "java/lang/NullPointerException"; if (tili_ARVO == 6) return "java/lang/IndexOutOfBoundsException";
        if (tili_ARVO == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (tili_ARVO == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (tili_ARVO == 9) return "java/lang/IllegalArgumentException"; if (tili_ARVO == 10) return "java/lang/NumberFormatException";
        if (tili_ARVO == 11) return "java/io/IOException"; if (tili_ARVO == 12) return "java/io/FileNotFoundException";
        if (tili_ARVO == 17) return "java/lang/ArrayStoreException";
        if (tili_ARVO == 18) return "java/net/UnknownHostException";
        if (tili_ARVO == 19) return "java/net/SocketTimeoutException";
        if (tili_ARVO == 16) return "java/lang/IllegalThreadStateException";
        if (tili_ARVO == 13) return "java/lang/IllegalStateException"; if (tili_ARVO == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int poikkeus_pää(int tili_ARVO) {
        if (tili_ARVO == 40) return 2;
        if (tili_ARVO == 41) return 40;
        if (tili_ARVO == 39) return 11;
        if (tili_ARVO == 1) return 0;
        if (tili_ARVO == 2) return 1;
        if (tili_ARVO == 3) return 2;
        if (tili_ARVO == 4) return 3;
        if (tili_ARVO == 5) return 3;
        if (tili_ARVO == 6) return 3;
        if (tili_ARVO == 7) return 6;
        if (tili_ARVO == 8) return 6;
        if (tili_ARVO == 9) return 3;
        if (tili_ARVO == 10) return 9;
        if (tili_ARVO == 11) return 2;
        if (tili_ARVO == 12) return 11;
        if (tili_ARVO == 13) return 3;
        if (tili_ARVO == 14) return 3;
        if (tili_ARVO == 15) return 3;
        if (tili_ARVO == 16) return 9;
        if (tili_ARVO == 17) return 3;
        if (tili_ARVO == 18) return 11;
        if (tili_ARVO == 19) return 11;
        if (tili_ARVO == 20) return 2;
        if (tili_ARVO == 21) return 3;
        if (tili_ARVO == 22) return 11;
        if (tili_ARVO == 23) return 22;
        if (tili_ARVO == 24) return 22;
        if (tili_ARVO == 25) return 22;
        if (tili_ARVO == 26) return 22;
        if (tili_ARVO == 27) return 9;
        if (tili_ARVO == 28) return 27;
        if (tili_ARVO == 29) return 6;
        if (tili_ARVO == 30) return 29;
        if (tili_ARVO == 31) return 29;
        if (tili_ARVO == 32) return 5;
        if (tili_ARVO == 33) return 4;
        if (tili_ARVO == 34) return 13;
        if (tili_ARVO == 35) return 14;
        if (tili_ARVO == 36) return 15;
        if (tili_ARVO == 37) return 17;
        if (tili_ARVO == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int todellinen_arvo, int 요구값) {
        for (int 깊이 = 0; todellinen_arvo != 0 && 깊이 < 16; 깊이++, todellinen_arvo = poikkeus_pää(todellinen_arvo))
            if (todellinen_arvo == 요구값) return true;
        return false;
    }
    static void 예외던짐(int tili_ARVO, String Lueminut_viite) {
        int objekti_viite = 새기억(9, 2); if (VIRHE) return;
        keko_ARVO[objekti_viite + 2] = tili_ARVO; keko_ARVO[objekti_viite + 3] = isäntä_merkki(Lueminut_viite); keko_viite[objekti_viite + 3] = 1;
        던진객체 = objekti_viite; VIRHE = true;
    }
    static boolean kohdistus_objekti(int objekti_viite, int Nimi) {
        if (objekti_viite == 0) return true;
        if (!tietojärjestelmät_kelvollinen_objekti(objekti_viite)) return false;
        int alue_KOODI = keko_ARVO[objekti_viite];
        if (Word_SMS(Nimi, "java/lang/Object")) return true;
        if (alue_KOODI >= 32) return 종포함(alue_KOODI - 32, Nimi);
        if (alue_KOODI == 9) { int kohde_OSOITE = poikkeus_vakio(Nimi); return kohde_OSOITE != 0 && 예외포함(keko_ARVO[objekti_viite + 2], kohde_OSOITE); }
        if (alue_KOODI == 1) return Word_SMS(Nimi, "java/lang/String") || Word_SMS(Nimi, "java/lang/CharSequence");
        if (alue_KOODI == 4) return Word_SMS(Nimi, "java/lang/StringBuilder") || Word_SMS(Nimi, "java/lang/CharSequence");
        if (alue_KOODI == 10) return Word_SMS(Nimi, "java/util/ArrayList") || Word_SMS(Nimi, "java/util/List");
        if (alue_KOODI == 11) return Word_SMS(Nimi, "java/util/HashMap") || Word_SMS(Nimi, "java/util/Map");
        if (alue_KOODI == 12) return Word_SMS(Nimi, "java/lang/Integer") || Word_SMS(Nimi, "java/lang/Number");
        if (alue_KOODI >= 24 && alue_KOODI <= 28 && keko_ARVO[objekti_viite + 13] != 0) return 한국어화면종(Nimi) == alue_KOODI || Word_SMS(Nimi, "suomi/oma/화면구성요소");
        if (alue_KOODI >= 24 && alue_KOODI <= 28) return (한국어화면종(Nimi) == 0 && 화면종(Nimi) == alue_KOODI) || Word_SMS(Nimi, "java/awt/Component") || Word_SMS(Nimi, "java/awt/Container") || Word_SMS(Nimi, "javax/swing/JComponent");
        if (alue_KOODI == 29) return Word_SMS(Nimi, keko_ARVO[objekti_viite + 3] != 0 ? "suomi/oma/동작알림" : "java/awt/event/ActionEvent");
        if (alue_KOODI == 30) return Word_SMS(Nimi, "java/awt/FlowLayout") || Word_SMS(Nimi, "java/awt/LayoutManager");
        if (alue_KOODI == 17) return Word_SMS(Nimi, "java/net/Socket");
        if (alue_KOODI == 18) return Word_SMS(Nimi, "java/net/ServerSocket");
        if (alue_KOODI == 19) return Word_SMS(Nimi, keko_ARVO[objekti_viite + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (alue_KOODI == 14) return Word_SMS(Nimi, "java/net/InetAddress");
        if (alue_KOODI == 15) return Word_SMS(Nimi, "java/net/DatagramSocket");
        if (alue_KOODI == 16) return Word_SMS(Nimi, "java/net/DatagramPacket");
        if (alue_KOODI == 13) return Word_SMS(Nimi, keko_ARVO[objekti_viite + 3] != 0 ? "suomi/oma/työntekijä" : "java/lang/Thread");
        if (alue_KOODI == 2) return Word_SMS(Nimi, "[I"); if (alue_KOODI == 20) return Word_SMS(Nimi, "[B"); if (alue_KOODI == 21) return Word_SMS(Nimi, "[Z");
        if (alue_KOODI == 22) return Word_SMS(Nimi, "[C"); if (alue_KOODI == 23) return Word_SMS(Nimi, "[S");
        if (alue_KOODI != 3) return false;
        if (Word_SMS(Nimi, "[Ljava/lang/Object;")) return true;
        int osa = matriisielementti[objekti_viite];
        if (osa == -1) return Word_SMS(Nimi, "[Ljava/lang/String;") || Word_SMS(Nimi, "[Ljava/lang/CharSequence;");
        if (osa == 0) return false;
        if (배열종비교(osa, Nimi)) return true;
        if ((Word_SMS(osa, "java/lang/String") || Word_SMS(osa, "java/lang/StringBuilder")) && Word_SMS(Nimi, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Luokka_Määritelmä_LASKE; Loop_INDEKSI++) if (kohdistus_Word(Luokka_Määritelmä_nimi[Loop_INDEKSI], osa)) {
            for (int merkkikoodi = Loop_INDEKSI, 중첩깊이 = 0; merkkikoodi >= 0 && 중첩깊이 < 16; 중첩깊이++, merkkikoodi = pää_Luokka(merkkikoodi)) {
                if (배열종비교(Luokka_Määritelmä_pää[merkkikoodi], Nimi)) return true;
                for (int sisäliitos_toimi = 0; sisäliitos_toimi < Luokka_liittymä_LASKE[merkkikoodi]; sisäliitos_toimi++) if (배열종비교(Luokka_liittymä[merkkikoodi * 16 + sisäliitos_toimi], Nimi)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int nimi_vakio, int 형식참조) {
        int sekki_toimi = 상가[형식참조], merkintä_LASKE = vakio_SEKUNNIT_ARVO[형식참조];
        if (nimi_vakio == 0 || merkintä_LASKE < 4 || tiedoston_nimi[sekki_toimi] != '[' || tiedoston_nimi[sekki_toimi + 1] != 'L' || tiedoston_nimi[sekki_toimi + merkintä_LASKE - 1] != ';' || vakio_SEKUNNIT_ARVO[nimi_vakio] != merkintä_LASKE - 3) return false;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE - 3; Loop_INDEKSI++) if (tiedoston_nimi[상가[nimi_vakio] + Loop_INDEKSI] != tiedoston_nimi[sekki_toimi + 2 + Loop_INDEKSI]) return false;
        return true;
    }
    static void kahva_poikkeus() {
        if (던진객체 == 0) return;
        VIRHE = false;
        while (kuva_INDEKSI >= nykyinen_säie * 32) {
            int Tiedosto_INDEKSI = kuva_menetelmä[kuva_INDEKSI], lukea_kohdistin = kuva_käsky[kuva_INDEKSI];
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < 잡기수; Loop_INDEKSI++) if (잡기함수[Loop_INDEKSI] == Tiedosto_INDEKSI && lukea_kohdistin >= 잡기시작[Loop_INDEKSI] && lukea_kohdistin < 잡기끝[Loop_INDEKSI]
                && (잡기종[Loop_INDEKSI] == 0 || kohdistus_objekti(던진객체, 잡기종[Loop_INDEKSI]))) {
                kuva_toimi[kuva_INDEKSI] = 잡기위치[Loop_INDEKSI]; kuva_Pino[kuva_INDEKSI] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (alustaa_kuva[kuva_INDEKSI] != 0) Luokka_Määritelmä_Tila[alustaa_kuva[kuva_INDEKSI] - 1] = 3;
            if (kuva_lukita[kuva_INDEKSI] != 0) { julkaista_lukita(kuva_lukita[kuva_INDEKSI]); kuva_lukita[kuva_INDEKSI] = 0; }
            kuva_INDEKSI--;
        }
        käyttäjätila.Kirjoitus("Uncaught ");
        if (keko_ARVO[던진객체] == 9) { käyttäjätila.Kirjoitus(poikkeus_nimi(keko_ARVO[던진객체 + 2])); käyttäjätila.Kirjoitus(": "); kirjoitus_SMS(keko_ARVO[던진객체 + 3]); }
        else käyttäjätila.Kirjoitus("user exception");
        käyttäjätila.kirjoitus_merkki_ARVO(10); 던진객체 = 0; VIRHE = true;
    }
    // 이 JVM의 operandi_Pino 항목은 nykyinen_kohde category-1(int/reference)만 허용한다.
    static void Pino_käsky(int komento_KOODI) {
        int 첫값 = 빼기(0), 첫형식 = palauttaa_TYYPPI;
        if (komento_KOODI == 87) return;
        if (komento_KOODI == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int tavu_data = 빼기(0), SEKUNNIT_muoto = palauttaa_TYYPPI;
        if (komento_KOODI == 88) return;
        if (komento_KOODI == 90) { 넣기(첫값, 첫형식); 넣기(tavu_data, SEKUNNIT_muoto); 넣기(첫값, 첫형식); return; }
        if (komento_KOODI == 92) { 넣기(tavu_data, SEKUNNIT_muoto); 넣기(첫값, 첫형식); 넣기(tavu_data, SEKUNNIT_muoto); 넣기(첫값, 첫형식); return; }
        if (komento_KOODI == 95) { 넣기(첫값, 첫형식); 넣기(tavu_data, SEKUNNIT_muoto); return; }
        int merkkikoodi = 빼기(0), 셋째형식 = palauttaa_TYYPPI;
        if (komento_KOODI == 91) { 넣기(첫값, 첫형식); 넣기(merkkikoodi, 셋째형식); 넣기(tavu_data, SEKUNNIT_muoto); 넣기(첫값, 첫형식); return; }
        if (komento_KOODI == 93) { 넣기(tavu_data, SEKUNNIT_muoto); 넣기(첫값, 첫형식); 넣기(merkkikoodi, 셋째형식); 넣기(tavu_data, SEKUNNIT_muoto); 넣기(첫값, 첫형식); return; }
        int seuraava_ARVO = 빼기(0), 넷째형식 = palauttaa_TYYPPI;
        넣기(tavu_data, SEKUNNIT_muoto); 넣기(첫값, 첫형식); 넣기(seuraava_ARVO, 넷째형식); 넣기(merkkikoodi, 셋째형식); 넣기(tavu_data, SEKUNNIT_muoto); 넣기(첫값, 첫형식);
    }
    static void 새객체(int nimi_vakio, int 시작점) {
        int alue_KOODI = 0, kelvollinen_kesto = 0, poikkeus_viite = poikkeus_vakio(nimi_vakio);
        if (Word_SMS(nimi_vakio, "java/lang/StringBuilder")) { alue_KOODI = 4; kelvollinen_kesto = 1; }
        if (Word_SMS(nimi_vakio, "java/io/FileInputStream")) { alue_KOODI = 5; kelvollinen_kesto = 2; }
        if (Word_SMS(nimi_vakio, "java/io/FileOutputStream")) { alue_KOODI = 6; kelvollinen_kesto = 2; }
        if (poikkeus_viite != 0) { alue_KOODI = 9; kelvollinen_kesto = 2; }
        if (Word_SMS(nimi_vakio, "java/util/ArrayList")) { alue_KOODI = 10; kelvollinen_kesto = 2; }
        if (Word_SMS(nimi_vakio, "java/util/HashMap")) { alue_KOODI = 11; kelvollinen_kesto = 2; }
        if (Word_SMS(nimi_vakio, "java/lang/Integer")) { alue_KOODI = 12; kelvollinen_kesto = 1; }
        if (Word_SMS(nimi_vakio, "java/net/Socket")) { alue_KOODI = 17; kelvollinen_kesto = 5; }
        if (Word_SMS(nimi_vakio, "java/net/ServerSocket")) { alue_KOODI = 18; kelvollinen_kesto = 5; }
        if (Word_SMS(nimi_vakio, "java/net/DatagramSocket")) { alue_KOODI = 15; kelvollinen_kesto = 3; }
        if (Word_SMS(nimi_vakio, "java/net/DatagramPacket")) { alue_KOODI = 16; kelvollinen_kesto = 4; }
        if (Word_SMS(nimi_vakio, "java/lang/Thread") || Word_SMS(nimi_vakio, "suomi/oma/työntekijä")) { alue_KOODI = 13; kelvollinen_kesto = 2; }
        if (Word_SMS(nimi_vakio, "java/lang/Object")) { alue_KOODI = 8; }
        if (alue_KOODI == 0 && 화면종(nimi_vakio) != 0) { alue_KOODI = 화면종(nimi_vakio); kelvollinen_kesto = 12; }
        if (alue_KOODI == 0) {
            int merkkikoodi = ETSI_Luokka_Määritelmä(nimi_vakio); if (merkkikoodi < 0 || VIRHE || !alustaa(merkkikoodi, 시작점)) return;
            alue_KOODI = 32 + merkkikoodi; kelvollinen_kesto = Luokka_paikka_LASKE[merkkikoodi];
        }
        int objekti_viite = jakaa_Tallennus(alue_KOODI, kelvollinen_kesto); if (VIRHE) return;
        if (alue_KOODI == 13 && Word_SMS(nimi_vakio, "suomi/oma/työntekijä")) keko_ARVO[objekti_viite + 3] = 1;
        if (alue_KOODI >= 24 && alue_KOODI <= 28 && 한국어화면종(nimi_vakio) != 0) keko_ARVO[objekti_viite + 13] = 1;
        if (alue_KOODI == 5 || alue_KOODI == 6 || alue_KOODI == 15 || alue_KOODI == 17 || alue_KOODI == 18) keko_ARVO[objekti_viite + 2] = -1;
        if (alue_KOODI == 9) keko_ARVO[objekti_viite + 2] = poikkeus_viite;
        넣기(objekti_viite, 2);
    }
    static boolean 값같음(int 첫값, int tavu_data) {
        if (첫값 == tavu_data) return true;
        if (첫값 == 0 || tavu_data == 0 || 첫값 < 0 || tavu_data < 0 || 첫값 >= keko_lopettaa_puhelu_toimi || tavu_data >= keko_lopettaa_puhelu_toimi) return false;
        if (keko_ARVO[첫값] == 1 && keko_ARVO[tavu_data] == 1) return tekstit_samat(첫값, tavu_data, false);
        return keko_ARVO[첫값] == 12 && keko_ARVO[tavu_data] == 12 && keko_ARVO[첫값 + 2] == keko_ARVO[tavu_data + 2];
    }
    static int 글조각(int objekti_viite, int alku_toimi, int lopettaa_puhelu_toimi) {
        if (!objekti_ARVO(objekti_viite, 1)) return 0;
        if (alku_toimi < 0 || lopettaa_puhelu_toimi < alku_toimi || lopettaa_puhelu_toimi > keko_ARVO[objekti_viite + 1]) { virhe_ARVO("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = jakaa_Tallennus(1, lopettaa_puhelu_toimi - alku_toimi); if (VIRHE) return 0;
        for (int Loop_INDEKSI = alku_toimi; Loop_INDEKSI < lopettaa_puhelu_toimi; Loop_INDEKSI++) keko_ARVO[반환값 + 2 + Loop_INDEKSI - alku_toimi] = keko_ARVO[objekti_viite + 2 + Loop_INDEKSI];
        return 반환값;
    }
    static int Liity_SMS(int 첫값, int tavu_data) {
        if (!objekti_ARVO(첫값, 1) || !objekti_ARVO(tavu_data, 1)) return 0;
        int merkintä_LASKE = keko_ARVO[첫값 + 1], menetelmä_INDEKSI = keko_ARVO[tavu_data + 1], 반환값 = jakaa_Tallennus(1, merkintä_LASKE + menetelmä_INDEKSI); if (VIRHE) return 0;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) keko_ARVO[반환값 + 2 + Loop_INDEKSI] = keko_ARVO[첫값 + 2 + Loop_INDEKSI];
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < menetelmä_INDEKSI; Loop_INDEKSI++) keko_ARVO[반환값 + 2 + merkintä_LASKE + Loop_INDEKSI] = keko_ARVO[tavu_data + 2 + Loop_INDEKSI];
        return 반환값;
    }
    static boolean 기본호출(int omistaja, int nimi_vakio, int 서술상수, int komento_KOODI) {
        if (Word_SMS(omistaja, "suomi/oma/실행인수") && komento_KOODI == 184) {
            if (Word_SMS(nimi_vakio, "kohde_LASKE") && Word_SMS(서술상수, "()I")) { 넣기(käyttäjätila.인수개수() - 1, 1); return true; }
            if (Word_SMS(nimi_vakio, "teksti") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= käyttäjätila.인수개수() - 1) 예외던짐(29, "Suorita_komento argumentit 범위를 벗어났습니다");
                else 넣기(isäntä_merkki(käyttäjätila.argumentit(순번 + 1)), 2);
                return true;
            }
            virhe_ARVO("지원하지 않는 suomi Suorita_komento argumentit 호출"); return true;
        }
        if (Word_SMS(omistaja, "suomi/oma/työntekijä")) { prosessi_säie(nimi_vakio, 서술상수, komento_KOODI, true); return true; }
        if (한국어화면소유(omistaja)) { 한국어화면호출(omistaja, nimi_vakio, 서술상수, komento_KOODI); return true; }
        if (화면소유(omistaja)) { 화면호출(omistaja, nimi_vakio, 서술상수, komento_KOODI); return true; }
        if (Word_SMS(omistaja, "java/net/Socket") || Word_SMS(omistaja, "java/net/ServerSocket") || Word_SMS(omistaja, "java/io/InputStream") || Word_SMS(omistaja, "java/io/OutputStream")) { 흐름호출(omistaja, nimi_vakio, 서술상수, komento_KOODI); return true; }
        if (Word_SMS(omistaja, "suomi/oma/ydin_ARVO") && komento_KOODI == 184) {
            if (Word_SMS(nimi_vakio, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(käyttäjätila.화면너비(), 1); return true; }
            if (Word_SMS(nimi_vakio, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(käyttäjätila.화면높이(), 1); return true; }
            if (Word_SMS(nimi_vakio, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(käyttäjätila.밀리초(), 1); return true; }
            if (Word_SMS(nimi_vakio, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(käyttäjätila.그림대기(), 1); return true; }
            if (Word_SMS(nimi_vakio, "suorakulmio") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinaatti = 빼기(1), x_koordinaatti = 빼기(1); 넣기(käyttäjätila.suorakulmio(x_koordinaatti, Y_koordinaatti, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(omistaja, "java/net/InetAddress") || Word_SMS(omistaja, "java/net/DatagramPacket") || Word_SMS(omistaja, "java/net/DatagramSocket")) { 통신호출(omistaja, nimi_vakio, 서술상수, komento_KOODI); return true; }
        if (Word_SMS(omistaja, "java/lang/Thread")) { 가닥호출(nimi_vakio, 서술상수, komento_KOODI); return true; }
        if (Word_SMS(omistaja, "java/lang/Object")) {
            if (Word_SMS(nimi_vakio, "<init>") && Word_SMS(서술상수, "()V") && komento_KOODI == 183) { tietojärjestelmät_kelvollinen_objekti(빼기(2)); return true; }
            if (Word_SMS(nimi_vakio, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int tavu_data = 빼기(2), 첫값 = 빼기(2); if (tietojärjestelmät_kelvollinen_objekti(첫값)) 넣기(첫값 == tavu_data ? 1 : 0, 1); return true; }
        }
        if (poikkeus_vakio(omistaja) != 0) {
            if (Word_SMS(nimi_vakio, "<init>") && komento_KOODI == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int kehote = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekti_viite = 빼기(2);
                if (objekti_ARVO(objekti_viite, 9)) { keko_ARVO[objekti_viite + 3] = kehote; keko_viite[objekti_viite + 3] = 1; } return true;
            }
            if ((Word_SMS(nimi_vakio, "getMessage") || Word_SMS(nimi_vakio, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, 9)) 넣기(keko_ARVO[objekti_viite + 3], 2); return true; }
        }
        if (Word_SMS(omistaja, "java/lang/String")) {
            if (komento_KOODI == 182 && Word_SMS(nimi_vakio, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int koodaus_nimi = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objekti_viite = 빼기(2);
                if (!objekti_ARVO(objekti_viite, 1)) return true;
                if (koodaus_nimi != 0 && !tekstit_samat(koodaus_nimi, isäntä_merkki("UTF-8"), false) && !tekstit_samat(koodaus_nimi, isäntä_merkki("UTF8"), false) && !tekstit_samat(koodaus_nimi, isäntä_merkki("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int merkintä_LASKE = keko_ARVO[objekti_viite + 1], 반환값 = jakaa_Tallennus(20, merkintä_LASKE * 3), 사용수 = 0; if (VIRHE) return true;
                for (int sisäliitos_toimi = 0; sisäliitos_toimi < merkintä_LASKE; sisäliitos_toimi++) {
                    int merkkikoodi = keko_ARVO[objekti_viite + 2 + sisäliitos_toimi];
                    if (merkkikoodi >= 0xd800 && merkkikoodi <= 0xdbff && sisäliitos_toimi + 1 < merkintä_LASKE && keko_ARVO[objekti_viite + 3 + sisäliitos_toimi] >= 0xdc00 && keko_ARVO[objekti_viite + 3 + sisäliitos_toimi] <= 0xdfff) merkkikoodi = 0x10000 + ((merkkikoodi - 0xd800) << 10) + keko_ARVO[objekti_viite + 2 + ++sisäliitos_toimi] - 0xdc00;
                    else if (merkkikoodi >= 0xd800 && merkkikoodi <= 0xdfff) merkkikoodi = '?';
                    if (merkkikoodi < 128) keko_ARVO[반환값 + 2 + 사용수++] = merkkikoodi;
                    else { int tavu_LASKE = merkkikoodi < 2048 ? 2 : merkkikoodi < 65536 ? 3 : 4; keko_ARVO[반환값 + 2 + 사용수++] = (byte)((tavu_LASKE == 2 ? 192 : tavu_LASKE == 3 ? 224 : 240) | merkkikoodi >> (6 * (tavu_LASKE - 1))); for (int Vertailu_toimi = tavu_LASKE - 1; Vertailu_toimi > 0; Vertailu_toimi--) keko_ARVO[반환값 + 2 + 사용수++] = (byte)(128 | merkkikoodi >> (6 * (Vertailu_toimi - 1)) & 63); }
                }
                keko_ARVO[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (komento_KOODI == 184 && Word_SMS(nimi_vakio, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(numero_merkki(빼기(1)), 2); return true; }
            if (komento_KOODI != 182) return false;
            if (Word_SMS(nimi_vakio, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int tavu_data = 빼기(2), 첫값 = 빼기(2); if (objekti_ARVO(첫값, 1)) 넣기(tekstit_samat(첫값, tavu_data, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(nimi_vakio, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekti_ARVO(첫값, 1)) 넣기(keko_ARVO[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(nimi_vakio, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SEKUNNIT_ARVO = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int lopettaa_puhelu_toimi = SEKUNNIT_ARVO ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekti_ARVO(첫값, 1)) 넣기(글조각(첫값, 시작점, SEKUNNIT_ARVO ? lopettaa_puhelu_toimi : keko_ARVO[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(nimi_vakio, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int tavu_data = 빼기(2), 첫값 = 빼기(2); 넣기(Liity_SMS(첫값, tavu_data), 2); return true; }
            if (Word_SMS(nimi_vakio, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hajautusarvo_ARVO = 0; if (objekti_ARVO(첫값, 1)) { for (int Loop_INDEKSI = 0; Loop_INDEKSI < keko_ARVO[첫값 + 1]; Loop_INDEKSI++) hajautusarvo_ARVO = hajautusarvo_ARVO * 31 + keko_ARVO[첫값 + 2 + Loop_INDEKSI]; 넣기(hajautusarvo_ARVO, 1); } return true; }
            if (Word_SMS(nimi_vakio, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekti_ARVO(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(omistaja, "java/lang/Integer")) {
            if (komento_KOODI == 184 && Word_SMS(nimi_vakio, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_ARVO = 빼기(1), objekti_viite = data_ARVO >= -128 && data_ARVO <= 127 ? Store_kokonaisluku[data_ARVO + 128] : 0; if (objekti_viite == 0) { objekti_viite = jakaa_Tallennus(12, 1); if (!VIRHE) { keko_ARVO[objekti_viite + 2] = data_ARVO; if (data_ARVO >= -128 && data_ARVO <= 127) Store_kokonaisluku[data_ARVO + 128] = objekti_viite; } } 넣기(objekti_viite, 2); return true; }
            if (komento_KOODI == 183 && Word_SMS(nimi_vakio, "<init>") && Word_SMS(서술상수, "(I)V")) { int data_ARVO = 빼기(1), objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, 12)) keko_ARVO[objekti_viite + 2] = data_ARVO; return true; }
            if (komento_KOODI == 182 && Word_SMS(nimi_vakio, "intValue") && Word_SMS(서술상수, "()I")) { int objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, 12)) 넣기(keko_ARVO[objekti_viite + 2], 1); return true; }
            if (komento_KOODI == 184 && Word_SMS(nimi_vakio, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(numero_merkki(빼기(1)), 2); return true; }
        }
        if (Word_SMS(omistaja, "java/lang/Math") && komento_KOODI == 184) {
            if (Word_SMS(nimi_vakio, "abs") && Word_SMS(서술상수, "(I)I")) { int lukea_ARVO = 빼기(1); 넣기(lukea_ARVO < 0 ? -lukea_ARVO : lukea_ARVO, 1); return true; }
            if ((Word_SMS(nimi_vakio, "min") || Word_SMS(nimi_vakio, "max")) && Word_SMS(서술상수, "(II)I")) { int tavu_data = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(nimi_vakio, "min") ? (첫값 < tavu_data ? 첫값 : tavu_data) : (첫값 > tavu_data ? 첫값 : tavu_data), 1); return true; }
        }
        if (Word_SMS(omistaja, "java/lang/System") && komento_KOODI == 184) {
            if (Word_SMS(nimi_vakio, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(nimi_vakio, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int merkintä_LASKE = 빼기(1), kohde_ARVO_INDEKSI = 빼기(1), tavu_data = 빼기(2), alku_toimi = 빼기(1), 첫값 = 빼기(2);
                if (tietojärjestelmät_kelvollinen_objekti(첫값) && tietojärjestelmät_kelvollinen_objekti(tavu_data)) {
                    int alue_KOODI = keko_ARVO[첫값];
                    if (keko_ARVO[tavu_data] != alue_KOODI || (alue_KOODI != 2 && alue_KOODI != 3 && (alue_KOODI < 20 || alue_KOODI > 23))) virhe_ARVO("arraycopy type mismatch");
                    else if (merkintä_LASKE < 0 || alku_toimi < 0 || kohde_ARVO_INDEKSI < 0 || alku_toimi > keko_ARVO[첫값 + 1] - merkintä_LASKE || kohde_ARVO_INDEKSI > keko_ARVO[tavu_data + 1] - merkintä_LASKE) virhe_ARVO("ArrayIndexOutOfBoundsException");
                    else if (첫값 == tavu_data && kohde_ARVO_INDEKSI > alku_toimi) { for (int Loop_INDEKSI = merkintä_LASKE - 1; Loop_INDEKSI >= 0; Loop_INDEKSI--) keko_ARVO[tavu_data + 2 + kohde_ARVO_INDEKSI + Loop_INDEKSI] = keko_ARVO[첫값 + 2 + alku_toimi + Loop_INDEKSI]; }
                    else { for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE && !VIRHE; Loop_INDEKSI++) { int data_ARVO = keko_ARVO[첫값 + 2 + alku_toimi + Loop_INDEKSI]; if (alue_KOODI != 3 || 배열저장가능(tavu_data, data_ARVO)) keko_ARVO[tavu_data + 2 + kohde_ARVO_INDEKSI + Loop_INDEKSI] = data_ARVO; } }
                }
                return true;
            }
        }
        if (Word_SMS(omistaja, "java/util/ArrayList") || Word_SMS(omistaja, "java/util/List") || Word_SMS(omistaja, "java/util/HashMap") || Word_SMS(omistaja, "java/util/Map")) {
            모음호출(omistaja, nimi_vakio, 서술상수, komento_KOODI); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekti_viite, int 필요수) {
        int Edellinen_ARVO = keko_ARVO[objekti_viite + 2], kapasiteetti_data = Edellinen_ARVO == 0 ? 0 : keko_ARVO[Edellinen_ARVO + 1];
        if (kapasiteetti_data >= 필요수) return;
        int Seuraava_toimi = kapasiteetti_data < 8 ? 8 : kapasiteetti_data * 2; if (Seuraava_toimi < 필요수) Seuraava_toimi = 필요수;
        int data_MATRIISI = jakaa_Tallennus(3, Seuraava_toimi); if (VIRHE) return;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < kapasiteetti_data; Loop_INDEKSI++) keko_ARVO[data_MATRIISI + 2 + Loop_INDEKSI] = keko_ARVO[Edellinen_ARVO + 2 + Loop_INDEKSI];
        keko_ARVO[objekti_viite + 2] = data_MATRIISI; keko_viite[objekti_viite + 2] = 1;
    }
    static void 모음호출(int omistaja, int nimi_vakio, int 서술상수, int komento_KOODI) {
        boolean 대응참조 = Word_SMS(omistaja, "java/util/HashMap") || Word_SMS(omistaja, "java/util/Map"); int alue_KOODI = 대응참조 ? 11 : 10;
        if (Word_SMS(nimi_vakio, "<init>") && komento_KOODI == 183 && Word_SMS(서술상수, "()V")) { int objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, alue_KOODI)) 모음늘리기(objekti_viite, 8); return; }
        if (komento_KOODI != 182 && komento_KOODI != 185) { virhe_ARVO("invalid collection invocation"); return; }
        if (Word_SMS(nimi_vakio, "size") && Word_SMS(서술상수, "()I") || Word_SMS(nimi_vakio, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, alue_KOODI)) 넣기(Word_SMS(nimi_vakio, "size") ? keko_ARVO[objekti_viite + 3] : keko_ARVO[objekti_viite + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(nimi_vakio, "clear") && Word_SMS(서술상수, "()V")) { int objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, alue_KOODI)) { int data_MATRIISI = keko_ARVO[objekti_viite + 2]; for (int Loop_INDEKSI = 0; Loop_INDEKSI < keko_ARVO[data_MATRIISI + 1]; Loop_INDEKSI++) keko_ARVO[data_MATRIISI + 2 + Loop_INDEKSI] = 0; keko_ARVO[objekti_viite + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(nimi_vakio, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_ARVO = 빼기(2), objekti_viite = 빼기(2); if (!objekti_ARVO(objekti_viite, 10)) return;
            int merkintä_LASKE = keko_ARVO[objekti_viite + 3]; 모음늘리기(objekti_viite, merkintä_LASKE + 1); if (!VIRHE) { keko_ARVO[keko_ARVO[objekti_viite + 2] + 2 + merkintä_LASKE] = data_ARVO; keko_ARVO[objekti_viite + 3] = merkintä_LASKE + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(nimi_vakio, "get") || Word_SMS(nimi_vakio, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(nimi_vakio, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(nimi_vakio, "set"); int data_ARVO = 지정여부 ? 빼기(2) : 0, merkintä_toimi = 빼기(1), objekti_viite = 빼기(2);
            if (!objekti_ARVO(objekti_viite, 10)) return;
            int merkintä_LASKE = keko_ARVO[objekti_viite + 3], data_MATRIISI = keko_ARVO[objekti_viite + 2];
            if (merkintä_toimi < 0 || merkintä_toimi >= merkintä_LASKE) { 예외던짐(6, "list index"); return; }
            int Edellinen_ARVO = keko_ARVO[data_MATRIISI + 2 + merkintä_toimi];
            if (지정여부) keko_ARVO[data_MATRIISI + 2 + merkintä_toimi] = data_ARVO;
            if (Word_SMS(nimi_vakio, "remove")) { for (int Loop_INDEKSI = merkintä_toimi + 1; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) keko_ARVO[data_MATRIISI + 1 + Loop_INDEKSI] = keko_ARVO[data_MATRIISI + 2 + Loop_INDEKSI]; keko_ARVO[data_MATRIISI + 1 + merkintä_LASKE] = 0; keko_ARVO[objekti_viite + 3] = merkintä_LASKE - 1; }
            넣기(Edellinen_ARVO, 2); return;
        }
        if (대응참조 && (Word_SMS(nimi_vakio, "get") || Word_SMS(nimi_vakio, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nimi_vakio, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nimi_vakio, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(nimi_vakio, "put"), poistaa = Word_SMS(nimi_vakio, "remove");
            int data_ARVO = 넣기여부 ? 빼기(2) : 0, Avain_viite = 빼기(2), objekti_viite = 빼기(2); if (!objekti_ARVO(objekti_viite, 11)) return;
            int merkintä_LASKE = keko_ARVO[objekti_viite + 3], data_MATRIISI = keko_ARVO[objekti_viite + 2], 찾은여부 = -1;
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) if (값같음(Avain_viite, keko_ARVO[data_MATRIISI + 2 + 2 * Loop_INDEKSI])) { 찾은여부 = Loop_INDEKSI; break; }
            int Edellinen_ARVO = 찾은여부 < 0 ? 0 : keko_ARVO[data_MATRIISI + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekti_viite, (merkintä_LASKE + 1) * 2); data_MATRIISI = keko_ARVO[objekti_viite + 2]; 찾은여부 = merkintä_LASKE; if (!VIRHE) keko_ARVO[objekti_viite + 3] = merkintä_LASKE + 1; }
                if (!VIRHE) { keko_ARVO[data_MATRIISI + 2 + 2 * 찾은여부] = Avain_viite; keko_ARVO[data_MATRIISI + 3 + 2 * 찾은여부] = data_ARVO; }
            }
            if (poistaa && 찾은여부 >= 0) { for (int Loop_INDEKSI = 찾은여부 + 1; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) { keko_ARVO[data_MATRIISI + 2 * Loop_INDEKSI] = keko_ARVO[data_MATRIISI + 2 + 2 * Loop_INDEKSI]; keko_ARVO[data_MATRIISI + 1 + 2 * Loop_INDEKSI] = keko_ARVO[data_MATRIISI + 3 + 2 * Loop_INDEKSI]; } keko_ARVO[data_MATRIISI + 2 * merkintä_LASKE] = 0; keko_ARVO[data_MATRIISI + 1 + 2 * merkintä_LASKE] = 0; keko_ARVO[objekti_viite + 3] = merkintä_LASKE - 1; }
            if (Word_SMS(nimi_vakio, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Edellinen_ARVO, 2);
            return;
        }
        virhe_ARVO("unsupported collection method");
    }
    static boolean 잠금얻기(int objekti_viite) {
        if (!tietojärjestelmät_kelvollinen_objekti(objekti_viite)) return false;
        if (잠금깊이[objekti_viite] != 0 && lukita_omistaja[objekti_viite] != nykyinen_säie + 1) { muutospyyntö = true; return false; }
        lukita_omistaja[objekti_viite] = nykyinen_säie + 1; 잠금깊이[objekti_viite]++; return true;
    }
    static void julkaista_lukita(int objekti_viite) {
        if (!tietojärjestelmät_kelvollinen_objekti(objekti_viite)) return;
        if (잠금깊이[objekti_viite] == 0 || lukita_omistaja[objekti_viite] != nykyinen_säie + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekti_viite] == 0) lukita_omistaja[objekti_viite] = 0;
    }
    static boolean MUUTA_säie() {
        säie_kuva[nykyinen_säie] = kuva_INDEKSI;
        if (kuva_INDEKSI < nykyinen_säie * 32) säie_Tila[nykyinen_säie] = 3;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < säikeiden_määrä; Loop_INDEKSI++) if (säie_Tila[Loop_INDEKSI] == 2 && säie_Tila[가닥대기[Loop_INDEKSI]] == 3) säie_Tila[Loop_INDEKSI] = 1;
        for (int Loop_INDEKSI = 1; Loop_INDEKSI <= säikeiden_määrä; Loop_INDEKSI++) {
            int Seuraava_toimi = (nykyinen_säie + Loop_INDEKSI) % säikeiden_määrä;
            if (säie_Tila[Seuraava_toimi] == 1) { nykyinen_säie = Seuraava_toimi; kuva_INDEKSI = säie_kuva[Seuraava_toimi]; muutospyyntö = false; return true; }
        }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < säikeiden_määrä; Loop_INDEKSI++) if (säie_Tila[Loop_INDEKSI] != 3) { virhe_ARVO("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int nimi_vakio, int 서술상수, int komento_KOODI) { prosessi_säie(nimi_vakio, 서술상수, komento_KOODI, false); }
    static void prosessi_säie(int nimi_vakio, int 서술상수, int komento_KOODI, boolean suomi) {
        if (komento_KOODI == 184 && Word_SMS(nimi_vakio, suomi ? "TUOTTO_tehtävä" : "yield") && Word_SMS(서술상수, "()V")) { muutospyyntö = true; return; }
        if (komento_KOODI == 184 && Word_SMS(nimi_vakio, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(säie_objekti[nykyinen_säie], 2); return; }
        if (komento_KOODI == 183 && Word_SMS(nimi_vakio, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, suomi ? "(Lsuomi/oma/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int kohde_OSOITE = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekti_viite = 빼기(2);
            if (!tietojärjestelmät_kelvollinen_objekti(objekti_viite)) return;
            if (keko_ARVO[objekti_viite] == 13) { keko_ARVO[objekti_viite + 2] = kohde_OSOITE; keko_viite[objekti_viite + 2] = 1; }
            else if (kohde_OSOITE != 0) virhe_ARVO("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (komento_KOODI == 182 && (Word_SMS(nimi_vakio, suomi ? "alku_tehtävä" : "start") || Word_SMS(nimi_vakio, suomi ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || komento_KOODI == 182 && Word_SMS(nimi_vakio, suomi ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objekti_viite = 빼기(2); if (!tietojärjestelmät_kelvollinen_objekti(objekti_viite)) return;
            int tili_ARVO = -1; for (int Loop_INDEKSI = 0; Loop_INDEKSI < säikeiden_määrä; Loop_INDEKSI++) if (säie_objekti[Loop_INDEKSI] == objekti_viite) tili_ARVO = Loop_INDEKSI;
            if (Word_SMS(nimi_vakio, suomi ? "살아있는가" : "isAlive")) { 넣기(tili_ARVO >= 0 && säie_Tila[tili_ARVO] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(nimi_vakio, suomi ? "기다리기" : "join")) { if (tili_ARVO >= 0 && säie_Tila[tili_ARVO] != 3) { 가닥대기[nykyinen_säie] = tili_ARVO; säie_Tila[nykyinen_säie] = 2; muutospyyntö = true; } return; }
            if (tili_ARVO >= 0) { 예외던짐(suomi ? 38 : 16, "thread already started"); return; }
            if (säikeiden_määrä == 4) { virhe_ARVO("thread limit (4 including main)"); return; }
            int kohde_OSOITE = keko_ARVO[objekti_viite] == 13 ? keko_ARVO[objekti_viite + 2] : objekti_viite;
            int Tiedosto_INDEKSI = kohde_OSOITE > 0 && keko_ARVO[kohde_OSOITE] >= 32 ? nimi_menetelmä(keko_ARVO[kohde_OSOITE] - 32, suomi ? "Suorita" : "run", "()V") : -1;
            if (kohde_OSOITE != 0 && Tiedosto_INDEKSI < 0) { virhe_ARVO("Runnable.run required"); return; }
            tili_ARVO = säikeiden_määrä++; säie_objekti[tili_ARVO] = objekti_viite; säie_kohde[tili_ARVO] = kohde_OSOITE;
            int kuva = tili_ARVO * 32; säie_kuva[tili_ARVO] = Tiedosto_INDEKSI < 0 ? kuva - 1 : kuva; säie_Tila[tili_ARVO] = Tiedosto_INDEKSI < 0 ? 3 : 1;
            if (Tiedosto_INDEKSI >= 0) { kuva_menetelmä[kuva] = Tiedosto_INDEKSI; kuva_toimi[kuva] = menetelmä_alku[Tiedosto_INDEKSI]; paikallinen_ARVO[kuva * 128] = kohde_OSOITE; paikallinen_TYYPPI[kuva * 128] = 2; }
            return;
        }
        virhe_ARVO("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], OSOITE_SMS = new int[16];
    static int paikallinen_OSOITE() { return OSOITE_objekti(0x7f000001); }
    static int OSOITE_objekti(int ARVO) { int objekti_viite = jakaa_Tallennus(14, 1); if (!VIRHE) keko_ARVO[objekti_viite + 2] = ARVO; return objekti_viite; }
    static int 주소해독(int objekti_viite) {
        if (objekti_viite == 0 || tekstit_samat(objekti_viite, isäntä_merkki("localhost"), false)) return 0x7f000001;
        if (!objekti_ARVO(objekti_viite, 1)) return 0;
        int data_ARVO = 0, summa_LASKE = 0, OSOITE_tavu = 0, 자릿수 = 0, merkintä_LASKE = keko_ARVO[objekti_viite + 1];
        for (int Loop_INDEKSI = 0; Loop_INDEKSI <= merkintä_LASKE; Loop_INDEKSI++) {
            int merkkikoodi = Loop_INDEKSI == merkintä_LASKE ? '.' : keko_ARVO[objekti_viite + 2 + Loop_INDEKSI];
            if (merkkikoodi == '.') { if (자릿수 == 0 || summa_LASKE == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_ARVO = data_ARVO << 8 | OSOITE_tavu; summa_LASKE++; OSOITE_tavu = 자릿수 = 0; }
            else { if (merkkikoodi < '0' || merkkikoodi > '9' || ++자릿수 > 3 || (OSOITE_tavu = OSOITE_tavu * 10 + merkkikoodi - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (summa_LASKE != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_ARVO;
    }
    static int OSOITE_merkki(int data_ARVO) {
        int merkintä_LASKE = 0;
        for (int siirrä = 24; siirrä >= 0; siirrä -= 8) {
            int OSOITE_tavu = data_ARVO >>> siirrä & 255;
            if (OSOITE_tavu >= 100) OSOITE_SMS[merkintä_LASKE++] = '0' + OSOITE_tavu / 100;
            if (OSOITE_tavu >= 10) OSOITE_SMS[merkintä_LASKE++] = '0' + OSOITE_tavu / 10 % 10;
            OSOITE_SMS[merkintä_LASKE++] = '0' + OSOITE_tavu % 10; if (siirrä != 0) OSOITE_SMS[merkintä_LASKE++] = '.';
        }
        int objekti_viite = jakaa_Tallennus(1, merkintä_LASKE); if (!VIRHE) for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) keko_ARVO[objekti_viite + 2 + Loop_INDEKSI] = OSOITE_SMS[Loop_INDEKSI]; return objekti_viite;
    }
    static void 통신호출(int omistaja, int nimi_vakio, int 서술상수, int komento_KOODI) {
        if (Word_SMS(omistaja, "java/net/InetAddress")) {
            if (komento_KOODI == 184 && Word_SMS(nimi_vakio, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(paikallinen_OSOITE(), 2); return; }
            if (komento_KOODI == 184 && Word_SMS(nimi_vakio, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_ARVO = 주소해독(빼기(2)); if (던진객체 == 0 && !VIRHE) 넣기(OSOITE_objekti(data_ARVO), 2); return;
            }
            if (komento_KOODI == 182 && Word_SMS(nimi_vakio, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, 14)) 넣기(OSOITE_merkki(keko_ARVO[objekti_viite + 2]), 2); return; }
        }
        if (Word_SMS(omistaja, "java/net/DatagramPacket")) {
            if (komento_KOODI == 183 && Word_SMS(nimi_vakio, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean kohde_ARVO_viite = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int portin_numero = kohde_ARVO_viite ? 빼기(1) : 0, OSOITE_viite = kohde_ARVO_viite ? 빼기(2) : 0;
                int merkintä_LASKE = 빼기(1), data_MATRIISI = 빼기(2), objekti_viite = 빼기(2);
                if (!objekti_ARVO(objekti_viite, 16) || !objekti_ARVO(data_MATRIISI, 20)) return;
                if (merkintä_LASKE < 0 || merkintä_LASKE > keko_ARVO[data_MATRIISI + 1] || portin_numero < 0 || portin_numero > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (OSOITE_viite != 0 && !objekti_ARVO(OSOITE_viite, 14)) return;
                keko_ARVO[objekti_viite + 2] = data_MATRIISI; keko_viite[objekti_viite + 2] = 1; keko_ARVO[objekti_viite + 3] = merkintä_LASKE;
                keko_ARVO[objekti_viite + 4] = OSOITE_viite; keko_viite[objekti_viite + 4] = 1; keko_ARVO[objekti_viite + 5] = portin_numero; return;
            }
            if (komento_KOODI == 182 && Word_SMS(nimi_vakio, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int merkintä_LASKE = 빼기(1), objekti_viite = 빼기(2); if (!objekti_ARVO(objekti_viite, 16)) return;
                if (merkintä_LASKE < 0 || merkintä_LASKE > keko_ARVO[keko_ARVO[objekti_viite + 2] + 1]) 예외던짐(9, "invalid datagram length"); else keko_ARVO[objekti_viite + 3] = merkintä_LASKE; return;
            }
            if (komento_KOODI == 182 && (Word_SMS(nimi_vakio, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(nimi_vakio, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(nimi_vakio, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(nimi_vakio, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objekti_viite = 빼기(2); if (!objekti_ARVO(objekti_viite, 16)) return;
                int merkintä_toimi = Word_SMS(nimi_vakio, "getData") ? 2 : Word_SMS(nimi_vakio, "getLength") ? 3 : Word_SMS(nimi_vakio, "getAddress") ? 4 : 5;
                넣기(keko_ARVO[objekti_viite + merkintä_toimi], merkintä_toimi == 2 || merkintä_toimi == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(omistaja, "java/net/DatagramSocket")) {
            if (komento_KOODI == 183 && Word_SMS(nimi_vakio, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int portin_numero = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objekti_viite = 빼기(2); if (!objekti_ARVO(objekti_viite, 15)) return;
                if (portin_numero < 0 || portin_numero > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = käyttäjätila.avata_verkko(portin_numero); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else keko_ARVO[objekti_viite + 2] = 열린파일번호; return;
            }
            if (komento_KOODI == 182 && Word_SMS(nimi_vakio, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekti_viite = 빼기(2); if (!objekti_ARVO(objekti_viite, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else keko_ARVO[objekti_viite + 3] = 밀리초값; return;
            }
            if (komento_KOODI == 182 && Word_SMS(nimi_vakio, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, 15)) 넣기(keko_ARVO[objekti_viite + 2] < 0 ? -1 : käyttäjätila.verkko_portti(keko_ARVO[objekti_viite + 2]), 1); return; }
            if (komento_KOODI == 182 && Word_SMS(nimi_vakio, "isClosed") && Word_SMS(서술상수, "()Z")) { int objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, 15)) 넣기(keko_ARVO[objekti_viite + 2] < 0 ? 1 : 0, 1); return; }
            if (komento_KOODI == 182 && Word_SMS(nimi_vakio, "close") && Word_SMS(서술상수, "()V")) { int objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, 15) && keko_ARVO[objekti_viite + 2] >= 0) { käyttäjätila.파일서술자닫기(keko_ARVO[objekti_viite + 2]); keko_ARVO[objekti_viite + 2] = -1; } return; }
            if (komento_KOODI == 182 && (Word_SMS(nimi_vakio, "send") || Word_SMS(nimi_vakio, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paketti = 빼기(2), objekti_viite = 빼기(2); if (!objekti_ARVO(paketti, 16) || !objekti_ARVO(objekti_viite, 15)) return;
                int data_MATRIISI = keko_ARVO[paketti + 2], kelvollinen_kesto = keko_ARVO[paketti + 3], 열린파일번호 = keko_ARVO[objekti_viite + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(nimi_vakio, "send")) {
                    if (!objekti_ARVO(keko_ARVO[paketti + 4], 14)) return;
                    if (kelvollinen_kesto > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEKSI = 0; Loop_INDEKSI < kelvollinen_kesto; Loop_INDEKSI++) 통신임시[Loop_INDEKSI] = keko_ARVO[data_MATRIISI + 2 + Loop_INDEKSI];
                    if (käyttäjätila.lähettää_verkko(열린파일번호, keko_ARVO[keko_ARVO[paketti + 4] + 2], keko_ARVO[paketti + 5], 통신임시, kelvollinen_kesto) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int merkintä_LASKE = käyttäjätila.saada_verkko(열린파일번호, 통신임시, kelvollinen_kesto > 512 ? 512 : kelvollinen_kesto);
                    if (merkintä_LASKE == -11) {
                        int nykyhetki = käyttäjätila.밀리초();
                        if (keko_ARVO[objekti_viite + 4] == 0) keko_ARVO[objekti_viite + 4] = nykyhetki + 1;
                        if (keko_ARVO[objekti_viite + 3] > 0 && nykyhetki - (keko_ARVO[objekti_viite + 4] - 1) >= keko_ARVO[objekti_viite + 3]) { keko_ARVO[objekti_viite + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekti_viite, 2); 넣기(paketti, 2); kuva_toimi[kuva_INDEKSI] = kuva_käsky[kuva_INDEKSI]; muutospyyntö = true; return;
                    }
                    keko_ARVO[objekti_viite + 4] = 0;
                    if (merkintä_LASKE < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) keko_ARVO[data_MATRIISI + 2 + Loop_INDEKSI] = (byte)통신임시[Loop_INDEKSI];
                    keko_ARVO[paketti + 3] = merkintä_LASKE; keko_ARVO[paketti + 4] = OSOITE_objekti(통신임시[513]); keko_viite[paketti + 4] = 1; keko_ARVO[paketti + 5] = 통신임시[512];
                }
                return;
            }
        }
        virhe_ARVO("unsupported java.net method");
    }
    static boolean 흐름대기(int objekti_viite) {
        int nykyhetki = käyttäjätila.밀리초();
        if (keko_ARVO[objekti_viite + 5] == 0) keko_ARVO[objekti_viite + 5] = nykyhetki + 1;
        if (keko_ARVO[objekti_viite + 3] > 0 && nykyhetki - (keko_ARVO[objekti_viite + 5] - 1) >= keko_ARVO[objekti_viite + 3]) { keko_ARVO[objekti_viite + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        kuva_toimi[kuva_INDEKSI] = kuva_käsky[kuva_INDEKSI]; muutospyyntö = true; return true;
    }
    static void 흐름호출(int omistaja, int nimi_vakio, int 서술상수, int komento_KOODI) {
        boolean saada_page = Word_SMS(omistaja, "java/net/ServerSocket"), virta = Word_SMS(omistaja, "java/io/InputStream") || Word_SMS(omistaja, "java/io/OutputStream");
        if (!virta && komento_KOODI == 183 && Word_SMS(nimi_vakio, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || saada_page && Word_SMS(서술상수, "(I)V") || !saada_page && (이름지정여부 || 주소지정여부))) { virhe_ARVO("unsupported socket constructor"); return; }
            int portin_numero = 빈여부 ? 0 : 빼기(1), OSOITE_viite = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekti_viite = 빼기(2);
            if (!objekti_ARVO(objekti_viite, saada_page ? 18 : 17)) return;
            if (portin_numero < 0 || portin_numero > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekti_ARVO(OSOITE_viite, 14)) return;
            int verkkotunnus = 이름지정여부 ? 주소해독(OSOITE_viite) : 주소지정여부 ? keko_ARVO[OSOITE_viite + 2] : 0x7f000001;
            if (VIRHE || 던진객체 != 0) return;
            int 열린파일번호 = käyttäjätila.virta_ohjain(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : saada_page ? käyttäjätila.virta_ohjain(1, 열린파일번호, portin_numero) : käyttäjätila.YHDISTÄ_virta(열린파일번호, verkkotunnus, portin_numero);
            if (처리값 < 0) { käyttäjätila.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            keko_ARVO[objekti_viite + 2] = 열린파일번호; keko_ARVO[objekti_viite + 4] = portin_numero; keko_ARVO[objekti_viite + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!virta && Word_SMS(nimi_vakio, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekti_viite = 빼기(2); if (!objekti_ARVO(objekti_viite, saada_page ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else keko_ARVO[objekti_viite + 3] = 밀리초값; return; }
        if (!virta && Word_SMS(nimi_vakio, "close") && Word_SMS(서술상수, "()V")) { int objekti_viite = 빼기(2); if (objekti_ARVO(objekti_viite, saada_page ? 18 : 17) && keko_ARVO[objekti_viite + 2] >= 0) { käyttäjätila.파일서술자닫기(keko_ARVO[objekti_viite + 2]); keko_ARVO[objekti_viite + 2] = -1; } return; }
        if (!virta && (Word_SMS(nimi_vakio, "getLocalPort") || Word_SMS(nimi_vakio, "getPort") || Word_SMS(nimi_vakio, "isClosed") || Word_SMS(nimi_vakio, "isConnected"))) {
            int objekti_viite = 빼기(2); if (!objekti_ARVO(objekti_viite, saada_page ? 18 : 17)) return;
            넣기(Word_SMS(nimi_vakio, "isClosed") ? keko_ARVO[objekti_viite + 2] < 0 ? 1 : 0 : Word_SMS(nimi_vakio, "isConnected") ? keko_ARVO[objekti_viite + 6] : Word_SMS(nimi_vakio, "getPort") ? keko_ARVO[objekti_viite + 4] : keko_ARVO[objekti_viite + 2] < 0 ? -1 : käyttäjätila.virta_ohjain(4, keko_ARVO[objekti_viite + 2], 0), 1); return;
        }
        if (saada_page && Word_SMS(nimi_vakio, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objekti_viite = 빼기(2); if (!objekti_ARVO(objekti_viite, 18)) return; int 열린파일번호 = käyttäjätila.virta_ohjain(3, keko_ARVO[objekti_viite + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekti_viite)) 넣기(objekti_viite, 2); return; }
            keko_ARVO[objekti_viite + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = jakaa_Tallennus(17, 5); if (VIRHE) { käyttäjätila.파일서술자닫기(열린파일번호); return; } keko_ARVO[반환값 + 2] = 열린파일번호; keko_ARVO[반환값 + 4] = käyttäjätila.virta_ohjain(5, 열린파일번호, 0); keko_ARVO[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!saada_page && !virta && ((Word_SMS(nimi_vakio, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(nimi_vakio, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekti_viite = 빼기(2); if (!objekti_ARVO(objekti_viite, 17)) return; if (keko_ARVO[objekti_viite + 2] < 0 || keko_ARVO[objekti_viite + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = jakaa_Tallennus(19, 4); if (VIRHE) return; keko_ARVO[반환값 + 2] = objekti_viite; keko_viite[반환값 + 2] = 1; keko_ARVO[반환값 + 3] = Word_SMS(nimi_vakio, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (virta) {
            boolean 읽기여부 = Word_SMS(nimi_vakio, "read"), tietojärjestelmät_kirjoitus_leikkaus = Word_SMS(nimi_vakio, "write"), Esto = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), tietojärjestelmät_ALIMATRIISI = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int merkintä_LASKE = tietojärjestelmät_ALIMATRIISI ? 빼기(1) : 0, 시작변위 = tietojärjestelmät_ALIMATRIISI ? 빼기(1) : 0, data_MATRIISI = Esto || tietojärjestelmät_ALIMATRIISI ? 빼기(2) : 0;
            int data_ARVO = tietojärjestelmät_kirjoitus_leikkaus && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objekti_viite = 빼기(2);
            if (!objekti_ARVO(objekti_viite, 19)) return; int pää_viite = keko_ARVO[objekti_viite + 2], 열린파일번호 = keko_ARVO[pää_viite + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(nimi_vakio, "close") && Word_SMS(서술상수, "()V")) { käyttäjätila.파일서술자닫기(열린파일번호); keko_ARVO[pää_viite + 2] = -1; return; }
            if (Word_SMS(nimi_vakio, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !tietojärjestelmät_kirjoitus_leikkaus) || 읽기여부 != (keko_ARVO[objekti_viite + 3] == 0)) { virhe_ARVO("unsupported stream operation"); return; }
            if (Esto || tietojärjestelmät_ALIMATRIISI) { if (!objekti_ARVO(data_MATRIISI, 20)) return; if (Esto) merkintä_LASKE = keko_ARVO[data_MATRIISI + 1]; if (시작변위 < 0 || merkintä_LASKE < 0 || 시작변위 > keko_ARVO[data_MATRIISI + 1] - merkintä_LASKE) { 예외던짐(6, "stream array bounds"); return; } }
            else merkintä_LASKE = 1;
            if (merkintä_LASKE == 0) { if (읽기여부) 넣기(0, 1); return; }
            int valmis_LASKE = tietojärjestelmät_kirjoitus_leikkaus ? keko_ARVO[objekti_viite + 4] : 0, 처리값 = 0;
            while (valmis_LASKE < merkintä_LASKE) {
                처리값 = 읽기여부 ? käyttäjätila.파일한바이트읽기(열린파일번호) : käyttäjätila.파일한바이트쓰기(열린파일번호, Esto || tietojärjestelmät_ALIMATRIISI ? keko_ARVO[data_MATRIISI + 2 + 시작변위 + valmis_LASKE] : data_ARVO);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (Esto || tietojärjestelmät_ALIMATRIISI)) keko_ARVO[data_MATRIISI + 2 + 시작변위 + valmis_LASKE] = (byte)처리값;
                valmis_LASKE++; if (읽기여부 && !(Esto || tietojärjestelmät_ALIMATRIISI)) break;
            }
            if (처리값 == -11 && (tietojärjestelmät_kirjoitus_leikkaus || valmis_LASKE == 0)) {
                keko_ARVO[objekti_viite + 4] = valmis_LASKE;
                if (흐름대기(pää_viite)) { 넣기(objekti_viite, 2); if (Esto || tietojärjestelmät_ALIMATRIISI) 넣기(data_MATRIISI, 2); if (tietojärjestelmät_ALIMATRIISI) { 넣기(시작변위, 1); 넣기(merkintä_LASKE, 1); } if (tietojärjestelmät_kirjoitus_leikkaus && !(Esto || tietojärjestelmät_ALIMATRIISI)) 넣기(data_ARVO, 1); } return;
            }
            keko_ARVO[objekti_viite + 4] = 0; keko_ARVO[pää_viite + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(valmis_LASKE == 0 && 처리값 == 256 ? -1 : Esto || tietojärjestelmät_ALIMATRIISI ? valmis_LASKE : 처리값, 1); return;
        }
        virhe_ARVO("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int nimi_vakio) {
        if (Word_SMS(nimi_vakio, "suomi/oma/Ikkuna")) return 24;
        if (Word_SMS(nimi_vakio, "suomi/oma/Nimike")) return 26;
        if (Word_SMS(nimi_vakio, "suomi/oma/painike")) return 27;
        if (Word_SMS(nimi_vakio, "suomi/oma/tekstikenttä")) return 28;
        if (Word_SMS(nimi_vakio, "suomi/oma/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int nimi_vakio) {
        return 한국어화면종(nimi_vakio) != 0 || Word_SMS(nimi_vakio, "suomi/oma/화면구성요소") || Word_SMS(nimi_vakio, "suomi/oma/tapahtuma_jono");
    }
    static int 화면종(int nimi_vakio) {
        int 한국어종 = 한국어화면종(nimi_vakio); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(nimi_vakio, "javax/swing/JFrame")) return 24;
        if (Word_SMS(nimi_vakio, "javax/swing/JPanel")) return 25;
        if (Word_SMS(nimi_vakio, "javax/swing/JLabel")) return 26;
        if (Word_SMS(nimi_vakio, "javax/swing/JButton")) return 27;
        if (Word_SMS(nimi_vakio, "javax/swing/JTextField")) return 28;
        if (Word_SMS(nimi_vakio, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(nimi_vakio, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int nimi_vakio) {
        return 화면종(nimi_vakio) != 0 || Word_SMS(nimi_vakio, "java/awt/Component") || Word_SMS(nimi_vakio, "java/awt/Container") || Word_SMS(nimi_vakio, "javax/swing/JComponent") || Word_SMS(nimi_vakio, "javax/swing/AbstractButton") || Word_SMS(nimi_vakio, "javax/swing/text/JTextComponent") || Word_SMS(nimi_vakio, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objekti_viite) { if (!tietojärjestelmät_kelvollinen_objekti(objekti_viite)) return false; if (keko_ARVO[objekti_viite] < 24 || keko_ARVO[objekti_viite] > 28) { virhe_ARVO("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objekti_viite, int SMS_viite) {
        if (SMS_viite != 0 && !objekti_ARVO(SMS_viite, 1)) return;
        int merkintä_LASKE = SMS_viite == 0 ? 0 : keko_ARVO[SMS_viite + 1]; if (merkintä_LASKE > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) 화면글임시[Loop_INDEKSI] = keko_ARVO[SMS_viite + 2 + Loop_INDEKSI];
        if (käyttäjätila.화면글(keko_ARVO[objekti_viite + 2], 화면글임시, merkintä_LASKE) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        keko_ARVO[objekti_viite + 3] = SMS_viite; keko_viite[objekti_viite + 3] = 1;
    }
    static int 화면문자읽기(int objekti_viite) {
        int tili_ARVO = keko_ARVO[objekti_viite + 2], merkintä_LASKE = käyttäjätila.화면연결(8, tili_ARVO, 0, 0, 0, 0), 사용수 = 0;
        if (merkintä_LASKE < 0) { virhe_ARVO("GUI text read failed"); return 0; }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) { int 부호값 = käyttäjätila.화면연결(9, tili_ARVO, Loop_INDEKSI, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = jakaa_Tallennus(1, 사용수); if (!VIRHE) for (int Loop_INDEKSI = 0; Loop_INDEKSI < 사용수; Loop_INDEKSI++) keko_ARVO[반환값 + 2 + Loop_INDEKSI] = 화면글임시[Loop_INDEKSI]; return 반환값;
    }
    /* suomi 객체를 직접 만들고 ydin_ARVO 화면 기능에 연결한다. Swing objekti_ARVO/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int omistaja, int nimi_vakio, int 서술상수, int komento_KOODI) {
        if (Word_SMS(omistaja, "suomi/oma/tapahtuma_jono")) {
            if (komento_KOODI == 184 && Word_SMS(nimi_vakio, "나중에실행") && Word_SMS(서술상수, "(Lsuomi/oma/실행할일;)V")) {
                int tehtävä_toimi = 빼기(2); if (!tietojärjestelmät_kelvollinen_objekti(tehtävä_toimi)) return;
                if (나중수 == 8) { virhe_ARVO("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = tehtävä_toimi; return;
            }
            if (komento_KOODI == 184 && Word_SMS(nimi_vakio, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            virhe_ARVO("지원하지 않는 suomi 화면 일정 호출"); return;
        }
        if (Word_SMS(omistaja, "suomi/oma/동작알림")) {
            int 알림 = 빼기(2); if (!objekti_ARVO(알림, 29) || keko_ARVO[알림 + 3] == 0) return;
            if (Word_SMS(nimi_vakio, "tapahtumalähde") && Word_SMS(서술상수, "()Lsuomi/oma/화면구성요소;")) 넣기(keko_ARVO[알림 + 2], 2);
            else if (Word_SMS(nimi_vakio, "komento_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(keko_ARVO[알림 + 2]), 2);
            else if (Word_SMS(nimi_vakio, "INDEKSI") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else virhe_ARVO("지원하지 않는 suomi Toiminto 알림 호출"); return;
        }
        if (komento_KOODI == 183 && Word_SMS(nimi_vakio, "<init>")) {
            int 종류 = 한국어화면종(omistaja), 받이 = 0, 가로 = 0, toimiala_toimi = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (käyttäjätila.화면너비() - 폭) / 2; toimiala_toimi = (käyttäjätila.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILsuomi/oma/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); toimiala_toimi = 빼기(1); 가로 = 빼기(1);
            } else { virhe_ARVO("지원하지 않는 suomi 화면 생성자"); return; }
            int teksti = 빼기(2), elementti_ARVO = 빼기(2); if (!화면객체(elementti_ARVO)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || toimiala_toimi < 0 || 폭 > käyttäjätila.화면너비() - 가로 || 높이 > käyttäjätila.화면높이() - toimiala_toimi) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEKSI = käyttäjätila.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEKSI < 1 || INDEKSI > 32) { virhe_ARVO("화면 elementti_ARVO 자리가 가득 찼습니다"); return; }
            keko_ARVO[elementti_ARVO + 2] = INDEKSI; 화면참조[INDEKSI - 1] = elementti_ARVO;
            keko_ARVO[elementti_ARVO + 5] = 가로; keko_ARVO[elementti_ARVO + 6] = toimiala_toimi; keko_ARVO[elementti_ARVO + 7] = 폭; keko_ARVO[elementti_ARVO + 8] = 높이; keko_ARVO[elementti_ARVO + 10] = 2;
            keko_ARVO[elementti_ARVO + 4] = 받이; keko_viite[elementti_ARVO + 4] = 1; keko_ARVO[elementti_ARVO + 12] = 1;
            käyttäjätila.화면연결(1, INDEKSI, 가로, toimiala_toimi, 폭, 높이);
            if (종류 == 24) käyttäjätila.화면연결(7, INDEKSI, 2, 0, 0, 0);
            화면문자설정(elementti_ARVO, teksti); return;
        }
        if (komento_KOODI != 182) { virhe_ARVO("잘못된 suomi 화면 호출 komento"); return; }
        if (Word_SMS(nimi_vakio, "kirjoitus_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int teksti = 빼기(2), elementti_ARVO = 빼기(2); if (화면객체(elementti_ARVO)) 화면문자설정(elementti_ARVO, teksti); return;
        }
        if (Word_SMS(nimi_vakio, "lukea_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int elementti_ARVO = 빼기(2); if (화면객체(elementti_ARVO)) 넣기(화면문자읽기(elementti_ARVO), 2); return;
        }
        if (Word_SMS(nimi_vakio, "동작맡기기") && Word_SMS(서술상수, "(Lsuomi/oma/동작받이;)V")) {
            int 받이 = 빼기(2), elementti_ARVO = 빼기(2);
            if (화면객체(elementti_ARVO)) { keko_ARVO[elementti_ARVO + 4] = 받이; keko_viite[elementti_ARVO + 4] = 1; keko_ARVO[elementti_ARVO + 12] = 1; } return;
        }
        if (Word_SMS(nimi_vakio, "Lisää_elementti") && Word_SMS(서술상수, "(Lsuomi/oma/화면구성요소;)V")) {
            int ali_ARVO = 빼기(2), pää_ARVO = 빼기(2); if (!화면객체(ali_ARVO) || !화면객체(pää_ARVO)) return;
            if (käyttäjätila.화면연결(2, keko_ARVO[pää_ARVO + 2], keko_ARVO[ali_ARVO + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            keko_ARVO[ali_ARVO + 11] = pää_ARVO; keko_viite[ali_ARVO + 11] = 1; return;
        }
        if (Word_SMS(nimi_vakio, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), toimiala_toimi = 빼기(1), 가로 = 빼기(1), elementti_ARVO = 빼기(2); if (!화면객체(elementti_ARVO)) return;
            if (käyttäjätila.화면연결(1, keko_ARVO[elementti_ARVO + 2], 가로, toimiala_toimi, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            keko_ARVO[elementti_ARVO + 5] = 가로; keko_ARVO[elementti_ARVO + 6] = toimiala_toimi; keko_ARVO[elementti_ARVO + 7] = 폭; keko_ARVO[elementti_ARVO + 8] = 높이; return;
        }
        if ((Word_SMS(nimi_vakio, "näyttää_ikkuna") || Word_SMS(nimi_vakio, "Sulje")) && Word_SMS(서술상수, "()V")) {
            boolean näkyvyys_ARVO = Word_SMS(nimi_vakio, "näyttää_ikkuna"); int elementti_ARVO = 빼기(2); if (!화면객체(elementti_ARVO)) return;
            if (käyttäjätila.화면연결(näkyvyys_ARVO ? 3 : 4, keko_ARVO[elementti_ARVO + 2], näkyvyys_ARVO ? 1 : 0, 0, 0, 0) < 0) { virhe_ARVO("화면은 vuorovaikutteinen 명령에서 실행해야 합니다"); return; }
            keko_ARVO[elementti_ARVO + 9] = näkyvyys_ARVO ? 1 : 0; return;
        }
        if (Word_SMS(nimi_vakio, "보이는가") && Word_SMS(서술상수, "()Z")) { int elementti_ARVO = 빼기(2); if (화면객체(elementti_ARVO)) 넣기(keko_ARVO[elementti_ARVO + 9], 1); return; }
        virhe_ARVO("지원하지 않는 suomi 화면 menetelmä_ARVO");
    }
    static void 화면호출(int omistaja, int nimi_vakio, int 서술상수, int komento_KOODI) {
        if (Word_SMS(omistaja, "javax/swing/SwingUtilities")) {
            if (komento_KOODI == 184 && Word_SMS(nimi_vakio, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objekti_viite = 빼기(2); if (!tietojärjestelmät_kelvollinen_objekti(objekti_viite)) return; if (나중수 == 8) { virhe_ARVO("invokeLater queue full"); return; } 나중실행[나중수++] = objekti_viite; return; }
            if (komento_KOODI == 184 && Word_SMS(nimi_vakio, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            virhe_ARVO("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(omistaja, "java/awt/event/ActionEvent")) {
            int objekti_viite = 빼기(2); if (!objekti_ARVO(objekti_viite, 29)) return;
            if (Word_SMS(nimi_vakio, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(keko_ARVO[objekti_viite + 2], 2);
            else if (Word_SMS(nimi_vakio, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(keko_ARVO[objekti_viite + 2]), 2);
            else if (Word_SMS(nimi_vakio, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else virhe_ARVO("unsupported ActionEvent method"); return;
        }
        if (komento_KOODI == 183 && Word_SMS(nimi_vakio, "<init>")) {
            int SARAKKEET = 0, SMS_viite = 0;
            if (Word_SMS(서술상수, "(I)V")) SARAKKEET = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { SARAKKEET = 빼기(1); SMS_viite = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_viite = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { virhe_ARVO("unsupported Swing constructor"); return; }
            int objekti_viite = 빼기(2); if (!tietojärjestelmät_kelvollinen_objekti(objekti_viite)) return;
            if (keko_ARVO[objekti_viite] == 30) { virhe_ARVO("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objekti_viite) || SARAKKEET < 0) return;
            int tili_ARVO = käyttäjätila.화면연결(0, keko_ARVO[objekti_viite] - 23, 0, 0, 0, 0);
            if (tili_ARVO < 1 || tili_ARVO > 32) { virhe_ARVO("GUI widget slots exhausted"); return; }
            keko_ARVO[objekti_viite + 2] = tili_ARVO; 화면참조[tili_ARVO - 1] = objekti_viite; keko_ARVO[objekti_viite + 5] = keko_ARVO[objekti_viite] == 24 ? 130 : 16; keko_ARVO[objekti_viite + 6] = keko_ARVO[objekti_viite] == 24 ? 110 : 16;
            keko_ARVO[objekti_viite + 7] = keko_ARVO[objekti_viite] == 24 ? 380 : 220; keko_ARVO[objekti_viite + 8] = keko_ARVO[objekti_viite] == 24 ? 240 : 28; keko_ARVO[objekti_viite + 10] = 1;
            화면문자설정(objekti_viite, SMS_viite); return;
        }
        if (Word_SMS(nimi_vakio, "setText") || Word_SMS(nimi_vakio, "setTitle")) { int SMS_viite = 빼기(2), objekti_viite = 빼기(2); if (화면객체(objekti_viite) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objekti_viite, SMS_viite); return; }
        if (Word_SMS(nimi_vakio, "getText") || Word_SMS(nimi_vakio, "getTitle")) { int objekti_viite = 빼기(2); if (화면객체(objekti_viite) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekti_viite), 2); return; }
        if (Word_SMS(nimi_vakio, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int saada_viite = 빼기(2), objekti_viite = 빼기(2); if (화면객체(objekti_viite)) { keko_ARVO[objekti_viite + 4] = saada_viite; keko_viite[objekti_viite + 4] = 1; } return; }
        if (Word_SMS(nimi_vakio, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objekti_viite = 빼기(2); if (화면객체(objekti_viite)) 넣기(objekti_viite, 2); return; }
        if (Word_SMS(nimi_vakio, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Asettelu_viite = 빼기(2), objekti_viite = 빼기(2); if (화면객체(objekti_viite) && Asettelu_viite != 0) virhe_ARVO("only absolute layout (null) is supported"); return; }
        if (Word_SMS(nimi_vakio, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Asettelu_ehto = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Asettelu_ehto) 빼기(2);
            int ali_viite = 빼기(2), objekti_viite = 빼기(2); if (!화면객체(ali_viite) || !화면객체(objekti_viite)) return;
            if (käyttäjätila.화면연결(2, keko_ARVO[objekti_viite + 2], keko_ARVO[ali_viite + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            keko_ARVO[ali_viite + 11] = objekti_viite; keko_viite[ali_viite + 11] = 1; if (!Asettelu_ehto) 넣기(ali_viite, 2); return;
        }
        if (Word_SMS(nimi_vakio, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinaatti = 빼기(1), x_koordinaatti = 빼기(1), objekti_viite = 빼기(2); if (!화면객체(objekti_viite)) return;
            if (käyttäjätila.화면연결(1, keko_ARVO[objekti_viite + 2], x_koordinaatti, Y_koordinaatti, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            keko_ARVO[objekti_viite + 5] = x_koordinaatti; keko_ARVO[objekti_viite + 6] = Y_koordinaatti; keko_ARVO[objekti_viite + 7] = 너비; keko_ARVO[objekti_viite + 8] = 높이; return;
        }
        if (Word_SMS(nimi_vakio, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objekti_viite = 빼기(2); if (!화면객체(objekti_viite)) return;
            if (käyttäjätila.화면연결(1, keko_ARVO[objekti_viite + 2], keko_ARVO[objekti_viite + 5], keko_ARVO[objekti_viite + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { keko_ARVO[objekti_viite + 7] = 너비; keko_ARVO[objekti_viite + 8] = 높이; } return;
        }
        if (Word_SMS(nimi_vakio, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekti_viite = 빼기(2); if (!화면객체(objekti_viite)) return; if (상대배치 != 0) { virhe_ARVO("only screen centering supported"); return; } keko_ARVO[objekti_viite + 5] = (käyttäjätila.화면너비() - keko_ARVO[objekti_viite + 7]) / 2; keko_ARVO[objekti_viite + 6] = (käyttäjätila.화면높이() - keko_ARVO[objekti_viite + 8]) / 2; käyttäjätila.화면연결(1, keko_ARVO[objekti_viite + 2], keko_ARVO[objekti_viite + 5], keko_ARVO[objekti_viite + 6], keko_ARVO[objekti_viite + 7], keko_ARVO[objekti_viite + 8]); return; }
        if (Word_SMS(nimi_vakio, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int Käytäntö = 빼기(1), objekti_viite = 빼기(2); if (화면객체(objekti_viite)) { if (Käytäntö < 0 || Käytäntö > 3) 예외던짐(9, "close policy"); else { keko_ARVO[objekti_viite + 10] = Käytäntö; käyttäjätila.화면연결(7, keko_ARVO[objekti_viite + 2], Käytäntö, 0, 0, 0); } } return; }
        if (Word_SMS(nimi_vakio, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int data_ARVO = 빼기(1), objekti_viite = 빼기(2); if (화면객체(objekti_viite)) { int 처리값 = käyttäjätila.화면연결(3, keko_ARVO[objekti_viite + 2], data_ARVO, 0, 0, 0); if (처리값 < 0) virhe_ARVO("Swing requires a standalone interactive command"); else keko_ARVO[objekti_viite + 9] = data_ARVO; } return; }
        if (Word_SMS(nimi_vakio, "dispose") && Word_SMS(서술상수, "()V")) { int objekti_viite = 빼기(2); if (화면객체(objekti_viite)) { käyttäjätila.화면연결(4, keko_ARVO[objekti_viite + 2], 0, 0, 0, 0); keko_ARVO[objekti_viite + 9] = 0; } return; }
        if (Word_SMS(nimi_vakio, "repaint") || Word_SMS(nimi_vakio, "validate")) { int objekti_viite = 빼기(2); if (!화면객체(objekti_viite) || !Word_SMS(서술상수, "()V")) return; käyttäjätila.화면연결(1, keko_ARVO[objekti_viite + 2], keko_ARVO[objekti_viite + 5], keko_ARVO[objekti_viite + 6], keko_ARVO[objekti_viite + 7], keko_ARVO[objekti_viite + 8]); return; }
        if (Word_SMS(nimi_vakio, "isVisible") && Word_SMS(서술상수, "()Z")) { int objekti_viite = 빼기(2); if (화면객체(objekti_viite)) 넣기(keko_ARVO[objekti_viite + 9], 1); return; }
        virhe_ARVO("unsupported Swing method (native subset)");
    }
    static void resursoida_tapahtuma(int kohde_OSOITE, int tapahtuma_numero, boolean suomi) {
        if (kohde_OSOITE < 1 || keko_ARVO[kohde_OSOITE] < 32) { virhe_ARVO("Java event listener required"); return; }
        int Tiedosto_INDEKSI = nimi_menetelmä(keko_ARVO[kohde_OSOITE] - 32, tapahtuma_numero == 0 ? (suomi ? "Suorita" : "run") : (suomi ? "saada_toimi" : "actionPerformed"), tapahtuma_numero == 0 ? "()V" : (suomi ? "(Lsuomi/oma/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Tiedosto_INDEKSI < 0) { virhe_ARVO("event callback missing"); return; }
        nykyinen_säie = 0; säikeiden_määrä = 1; kuva_INDEKSI = 0; säie_Tila[0] = 1; kuva_Pino[0] = 0; kuva_lukita[0] = alustaa_kuva[0] = 0; muutospyyntö = false;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 128; Loop_INDEKSI++) { paikallinen_ARVO[Loop_INDEKSI] = paikallinen_TYYPPI[Loop_INDEKSI] = 0; }
        kuva_menetelmä[0] = Tiedosto_INDEKSI; kuva_toimi[0] = menetelmä_alku[Tiedosto_INDEKSI]; paikallinen_ARVO[0] = kohde_OSOITE; paikallinen_TYYPPI[0] = 2;
        if (tapahtuma_numero != 0) { paikallinen_ARVO[1] = tapahtuma_numero; paikallinen_TYYPPI[1] = 2; }
        사건중 = true; Suorita_komento(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!VIRHE) {
            if (나중수 > 0) { int kohde_OSOITE = 나중실행[0], suomi = 나중한국어[0]; for (int Loop_INDEKSI = 1; Loop_INDEKSI < 나중수; Loop_INDEKSI++) { 나중실행[Loop_INDEKSI - 1] = 나중실행[Loop_INDEKSI]; 나중한국어[Loop_INDEKSI - 1] = 나중한국어[Loop_INDEKSI]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; resursoida_tapahtuma(kohde_OSOITE, 0, suomi != 0); continue; }
            if (käyttäjätila.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int tapahtuma_numero = käyttäjätila.화면연결(5, 0, 0, 0, 0, 0); if (tapahtuma_numero == 0) continue;
            if (tapahtuma_numero < 0) { virhe_ARVO("GUI event I/O failed"); return; }
            int tili_ARVO = tapahtuma_numero & 65535; if (tili_ARVO < 1 || tili_ARVO > 32) continue; int objekti_viite = 화면참조[tili_ARVO - 1]; if (objekti_viite == 0) continue;
            if ((tapahtuma_numero & 65536) != 0) {
                if (keko_ARVO[objekti_viite + 10] != 0) keko_ARVO[objekti_viite + 9] = 0;
                if (keko_ARVO[objekti_viite + 10] == 3) for (int Loop_INDEKSI = 0; Loop_INDEKSI < 32; Loop_INDEKSI++) if (화면참조[Loop_INDEKSI] != 0 && keko_ARVO[화면참조[Loop_INDEKSI]] == 24) käyttäjätila.화면연결(4, Loop_INDEKSI + 1, 0, 0, 0, 0);
            } else if (keko_ARVO[objekti_viite + 4] != 0) {
                int Lueminut_viite = jakaa_Tallennus(29, 2); if (VIRHE) return; keko_ARVO[Lueminut_viite + 2] = objekti_viite; keko_ARVO[Lueminut_viite + 3] = keko_ARVO[objekti_viite + 12]; keko_viite[Lueminut_viite + 2] = 1; resursoida_tapahtuma(keko_ARVO[objekti_viite + 4], Lueminut_viite, keko_ARVO[objekti_viite + 12] != 0);
            }
        }
    }
    public static int Suorita_2() {
        if (käyttäjätila.인수개수() == 1 && 자바도구.같음(käyttäjätila.argumentit(0), "-version")) {
            käyttäjätila.Kirjoitus("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (käyttäjätila.인수개수() < 1) { käyttäjätila.Kirjoitus("Usage: java CLASS [ARGS]\n"); return 2; }
        merkintä_Luokka_Määritelmä = ladata_Luokka_Määritelmä(isäntä_merkki(käyttäjätila.argumentit(0))); if (VIRHE || merkintä_Luokka_Määritelmä < 0) return 1;
        int aloituskohta_ARVO = nimi_menetelmä(merkintä_Luokka_Määritelmä, "Suorita_2", "()V");
        boolean 한국어진입 = aloituskohta_ARVO >= 0 && (menetelmä_pääsy[aloituskohta_ARVO] & 9) == 9;
        if (!한국어진입) aloituskohta_ARVO = nimi_menetelmä(merkintä_Luokka_Määritelmä, "main", "([Ljava/lang/String;)V");
        if (aloituskohta_ARVO < 0 || (menetelmä_pääsy[aloituskohta_ARVO] & 9) != 9) virhe_ARVO("public static void Suorita_2() or main(String[] args) required");
        if (VIRHE) return 1;
        int argumentit = jakaa_Tallennus(3, käyttäjätila.인수개수() - 1); matriisielementti[argumentit] = -1;
        for (int numero = 1; numero < käyttäjätila.인수개수() && !VIRHE; numero++) keko_ARVO[argumentit + 1 + numero] = isäntä_merkki(käyttäjätila.argumentit(numero));
        kuva_INDEKSI = 0; kuva_menetelmä[0] = aloituskohta_ARVO; kuva_toimi[0] = menetelmä_alku[aloituskohta_ARVO]; paikallinen_ARVO[0] = 한국어진입 ? 0 : argumentit; paikallinen_TYYPPI[0] = 한국어진입 ? 0 : 2;
        säie_Tila[0] = 1; säie_objekti[0] = jakaa_Tallennus(13, 2);
        Suorita_komento(); if (!VIRHE) 화면사건들(); return VIRHE ? 1 : 0;
    }
}
