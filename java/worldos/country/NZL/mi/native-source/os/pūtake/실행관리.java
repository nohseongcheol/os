// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Pānuitia 전용 kawe_tono 묶음의 ELF32 whakamana, 인수 Whakamua_uara, 한 번에 한 kaiwhakamahi Hātepe_uara kawe_tono. */
public final class 실행관리 {
    static final int Start_kaiwhakamahi_kaupapa = 0x04000000;
    static final int kaiwhakamahi_mutu = 0x04400000;
    static final int IMAGE_mutu_ADDRESS = 0x04200000;
    static final int tohenga_Start = 0x04300000;
    static int tohenga_COUNT = 0;
    static int[] tohenga_ADDRESS = new int[16];

    static boolean topenga(int ADDRESS, int roa_uara) {
        return ADDRESS >= Start_kaiwhakamahi_kaupapa && ADDRESS < kaiwhakamahi_mutu && roa_uara >= 0 && roa_uara <= kaiwhakamahi_mutu - ADDRESS;
    }

    static int 수(int ADDRESS) { return 기억공간.poroporo_tau_tōpū(ADDRESS); }
    static int 짧은수(int ADDRESS) { return pūkoro_uara.기억읽기(ADDRESS) | pūkoro_uara.기억읽기(ADDRESS + 1) << 8; }
    static void 수쓰기(int ADDRESS, int uara) {
        for (int INDEX = 0; INDEX < 4; INDEX++) pūkoro_uara.tuhi_Pūmahara(ADDRESS + INDEX, uara >>> (INDEX * 8));
    }

    static int rōpū_COUNT() {
        int ADDRESS = pūkoro_uara.실행묶음();
        int rahi = pūkoro_uara.실행묶음크기();
        if (rahi < 8 || 수(ADDRESS) != 0x50414b4a) return 0;
        int tuemi_COUNT = 수(ADDRESS + 4);
        return tuemi_COUNT >= 0 && tuemi_COUNT <= 32 && tuemi_COUNT <= (rahi - 8) / 24 ? tuemi_COUNT : 0;
    }

    static void tāurunga_Rārangi() {
        for (int INDEX = 0; INDEX < rōpū_COUNT(); INDEX++) {
            int tāurunga_uara = pūkoro_uara.실행묶음() + 8 + INDEX * 24;
            for (int pūāhua_uara = 0; pūāhua_uara < 16 && pūkoro_uara.기억읽기(tāurunga_uara + pūāhua_uara) != 0; pūāhua_uara++)
                TEXT_Tauranga.문자(pūkoro_uara.기억읽기(tāurunga_uara + pūāhua_uara));
            TEXT_Tauranga.Tuhia("\n");
        }
    }

    static int FIND_tāurunga(int[] 입력, int whakahaere, int roa_uara) {
        if (roa_uara <= 0 || roa_uara >= 16) return 0;
        for (int INDEX = 0; INDEX < rōpū_COUNT(); INDEX++) {
            int tāurunga_uara = pūkoro_uara.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = pūkoro_uara.기억읽기(tāurunga_uara + roa_uara) == 0;
            for (int pūāhua_uara = 0; pūāhua_uara < roa_uara; pūāhua_uara++)
                if (입력[whakahaere + pūāhua_uara] != pūkoro_uara.기억읽기(tāurunga_uara + pūāhua_uara)) 같음 = false;
            if (같음) return tāurunga_uara;
        }
        return 0;
    }

    static int whakamana(int Kōnae, int roa_uara) {
        if (roa_uara < 52 || 수(Kōnae) != 0x464c457f || pūkoro_uara.기억읽기(Kōnae + 4) != 1
            || pūkoro_uara.기억읽기(Kōnae + 5) != 1 || pūkoro_uara.기억읽기(Kōnae + 6) != 1
            || 짧은수(Kōnae + 16) != 2 || 짧은수(Kōnae + 18) != 3 || 수(Kōnae + 20) != 1
            || 짧은수(Kōnae + 40) != 52 || 짧은수(Kōnae + 42) != 32) return -8;
        int tāurunga_ira_uara = 수(Kōnae + 24);
        int ripanga_tūranga = 수(Kōnae + 28);
        int tuemi_COUNT = 짧은수(Kōnae + 44);
        if (tuemi_COUNT == 0 || tuemi_COUNT > 16 || ripanga_tūranga < 52 || ripanga_tūranga > roa_uara - tuemi_COUNT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < tuemi_COUNT; INDEX++) {
            int Rapu_ripanga = Kōnae + ripanga_tūranga + INDEX * 32;
            int 종류 = 수(Rapu_ripanga);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 TŪHONO/해석기 미지원
            if (종류 != 1) continue;
            int tūranga = 수(Rapu_ripanga + 4), ADDRESS = 수(Rapu_ripanga + 8), kōnae_rahi = 수(Rapu_ripanga + 16), Pūmahara_rahi = 수(Rapu_ripanga + 20);
            int tiaro_uara = 수(Rapu_ripanga + 28);
            if (ADDRESS < Start_kaiwhakamahi_kaupapa || ADDRESS >= IMAGE_mutu_ADDRESS || Pūmahara_rahi < 0 || Pūmahara_rahi > IMAGE_mutu_ADDRESS - ADDRESS
                || kōnae_rahi < 0 || kōnae_rahi > Pūmahara_rahi || tūranga < 0 || (kōnae_rahi > 0 && tūranga > roa_uara - kōnae_rahi)
                || (tiaro_uara != 0 && (tiaro_uara < 0 || (tiaro_uara & (tiaro_uara - 1)) != 0
                    || ((ADDRESS - tūranga) & (tiaro_uara - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < INDEX; 앞++) {
                int 이전 = Kōnae + ripanga_tūranga + 앞 * 32;
                if (수(이전) == 1 && Pūmahara_rahi > 0 && 수(이전 + 20) > 0
                    && ADDRESS < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < ADDRESS + Pūmahara_rahi) return -8;
            }
            if ((수(Rapu_ripanga + 24) & 1) != 0 && tāurunga_ira_uara >= ADDRESS && tāurunga_ira_uara - ADDRESS < kōnae_rahi) 실행가능 = true;
        }
        return 실행가능 ? tāurunga_ira_uara : -8;
    }

    static int kawe_tono(int[] 입력, int whakahaere, int roa_uara) {
        while (whakahaere < roa_uara && 입력[whakahaere] == ' ') whakahaere++;
        int 끝 = whakahaere;
        while (끝 < roa_uara && 입력[끝] != ' ') 끝++;
        int tāurunga_uara = FIND_tāurunga(입력, whakahaere, 끝 - whakahaere);
        if (tāurunga_uara == 0) return -2;
        int tūranga = 수(tāurunga_uara + 16), rahi = 수(tāurunga_uara + 20);
        if (tūranga < 8 + rōpū_COUNT() * 24 || rahi < 52 || tūranga > pūkoro_uara.실행묶음크기() - rahi) return -8;
        int Kōnae = pūkoro_uara.실행묶음() + tūranga;
        int tāurunga_ira_uara = whakamana(Kōnae, rahi);
        if (tāurunga_ira_uara < 0) return tāurunga_ira_uara;
        pūkoro_uara.kaiwhakamahi_ūkui_IRI();
        int ripanga_tūranga = 수(Kōnae + 28), tuemi_COUNT = 짧은수(Kōnae + 44);
        for (int INDEX = 0; INDEX < tuemi_COUNT; INDEX++) {
            int Rapu_ripanga = Kōnae + ripanga_tūranga + INDEX * 32;
            if (수(Rapu_ripanga) != 1) continue;
            int 원본 = Kōnae + 수(Rapu_ripanga + 4), ūnga_uara = 수(Rapu_ripanga + 8), kōnae_rahi = 수(Rapu_ripanga + 16);
            for (int paita_uara = 0; paita_uara < kōnae_rahi; paita_uara++) pūkoro_uara.tuhi_Pūmahara(ūnga_uara + paita_uara, pūkoro_uara.기억읽기(원본 + paita_uara));
        }
        tohenga_COUNT = 0;
        int Store_uara = tohenga_Start;
        while (끝 < roa_uara) {
            while (끝 < roa_uara && 입력[끝] == ' ') 끝++;
            if (끝 == roa_uara) break;
            if (tohenga_COUNT == tohenga_ADDRESS.length) return -22;
            whakahaere = 끝;
            while (끝 < roa_uara && 입력[끝] != ' ') 끝++;
            tohenga_ADDRESS[tohenga_COUNT++] = Store_uara;
            수쓰기(Store_uara, 끝 - whakahaere);
            for (int pūāhua_uara = whakahaere; pūāhua_uara < 끝; pūāhua_uara++) 수쓰기(Store_uara + 4 + (pūāhua_uara - whakahaere) * 4, 입력[pūāhua_uara]);
            Store_uara += 4 + (끝 - whakahaere) * 4;
        }
        whatunga_Huinga.CLEAN_Hātepe();
        파일서술자관리.Start_Hātepe();
        int mēhua = pūkoro_uara.whakahaere_kaiwhakamahi_kaupapa(tāurunga_ira_uara, kaiwhakamahi_mutu - 16);
        파일서술자관리.CLEAN_Hātepe();
        whatunga_Huinga.CLEAN_Hātepe();
        return mēhua;
    }
}
