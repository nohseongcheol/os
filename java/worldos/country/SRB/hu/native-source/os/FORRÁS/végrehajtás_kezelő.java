// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Olvasás 전용 végrehajt_parancs 묶음의 ELF32 ellenőriz, Argumentumok Előre_ÉRTÉK, 한 번에 한 felhasználó folyamat_ÉRTÉK végrehajt_parancs. */
public final class végrehajtás_kezelő {
    static final int START_felhasználó_app = 0x04000000;
    static final int felhasználó_megszüntet = 0x04400000;
    static final int KÉP_megszüntet_CÍM = 0x04200000;
    static final int argumentum_START = 0x04300000;
    static int argumentum_DARAB = 0;
    static int[] argumentum_CÍM = new int[16];

    static boolean klip(int CÍM, int hossz_ÉRTÉK) {
        return CÍM >= START_felhasználó_app && CÍM < felhasználó_megszüntet && hossz_ÉRTÉK >= 0 && hossz_ÉRTÉK <= felhasználó_megszüntet - CÍM;
    }

    static int szám(int CÍM) { return Memória_régió.elemez_egész_szám(CÍM); }
    static int 짧은수(int CÍM) { return mobil_ÉRTÉK.기억읽기(CÍM) | mobil_ÉRTÉK.기억읽기(CÍM + 1) << 8; }
    static void ír_szám(int CÍM, int ÉRTÉK) {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobil_ÉRTÉK.ír_Memória(CÍM + INDEX, ÉRTÉK >>> (INDEX * 8));
    }

    static int Csoport_DARAB() {
        int CÍM = mobil_ÉRTÉK.végrehajtható_köteg();
        int Méret = mobil_ÉRTÉK.végrehajtható_köteg_méretez();
        if (Méret < 8 || szám(CÍM) != 0x50414b4a) return 0;
        int cikk_DARAB = szám(CÍM + 4);
        return cikk_DARAB >= 0 && cikk_DARAB <= 32 && cikk_DARAB <= (Méret - 8) / 24 ? cikk_DARAB : 0;
    }

    static void bejegyzés_Lista() {
        for (int INDEX = 0; INDEX < Csoport_DARAB(); INDEX++) {
            int bejegyzés_ÉRTÉK = mobil_ÉRTÉK.végrehajtható_köteg() + 8 + INDEX * 24;
            for (int karakter_ÉRTÉK = 0; karakter_ÉRTÉK < 16 && mobil_ÉRTÉK.기억읽기(bejegyzés_ÉRTÉK + karakter_ÉRTÉK) != 0; karakter_ÉRTÉK++)
                SMS_Terminál.문자(mobil_ÉRTÉK.기억읽기(bejegyzés_ÉRTÉK + karakter_ÉRTÉK));
            SMS_Terminál.Írás("\n");
        }
    }

    static int keres_bejegyzés(int[] bevitel_ÉRTÉK, int Futtatás, int hossz_ÉRTÉK) {
        if (hossz_ÉRTÉK <= 0 || hossz_ÉRTÉK >= 16) return 0;
        for (int INDEX = 0; INDEX < Csoport_DARAB(); INDEX++) {
            int bejegyzés_ÉRTÉK = mobil_ÉRTÉK.végrehajtható_köteg() + 8 + INDEX * 24;
            boolean 같음 = mobil_ÉRTÉK.기억읽기(bejegyzés_ÉRTÉK + hossz_ÉRTÉK) == 0;
            for (int karakter_ÉRTÉK = 0; karakter_ÉRTÉK < hossz_ÉRTÉK; karakter_ÉRTÉK++)
                if (bevitel_ÉRTÉK[Futtatás + karakter_ÉRTÉK] != mobil_ÉRTÉK.기억읽기(bejegyzés_ÉRTÉK + karakter_ÉRTÉK)) 같음 = false;
            if (같음) return bejegyzés_ÉRTÉK;
        }
        return 0;
    }

    static int ellenőriz(int Fájl, int hossz_ÉRTÉK) {
        if (hossz_ÉRTÉK < 52 || szám(Fájl) != 0x464c457f || mobil_ÉRTÉK.기억읽기(Fájl + 4) != 1
            || mobil_ÉRTÉK.기억읽기(Fájl + 5) != 1 || mobil_ÉRTÉK.기억읽기(Fájl + 6) != 1
            || 짧은수(Fájl + 16) != 2 || 짧은수(Fájl + 18) != 3 || szám(Fájl + 20) != 1
            || 짧은수(Fájl + 40) != 52 || 짧은수(Fájl + 42) != 32) return -8;
        int belépési_pont_ÉRTÉK = szám(Fájl + 24);
        int tábla_pozíció = szám(Fájl + 28);
        int cikk_DARAB = 짧은수(Fájl + 44);
        if (cikk_DARAB == 0 || cikk_DARAB > 16 || tábla_pozíció < 52 || tábla_pozíció > hossz_ÉRTÉK - cikk_DARAB * 32) return -8;
        boolean informatikai_részleg_végrehajtható = false;
        for (int INDEX = 0; INDEX < cikk_DARAB; INDEX++) {
            int keresőtáblázat = Fájl + tábla_pozíció + INDEX * 32;
            int Altípus_ÉRTÉK = szám(keresőtáblázat);
            if (Altípus_ÉRTÉK == 2 || Altípus_ÉRTÉK == 3) return -8; // 동적 Kapcsolódás/elemző_48ee4b1b 미지원
            if (Altípus_ÉRTÉK != 1) continue;
            int Pozíció = szám(keresőtáblázat + 4), CÍM = szám(keresőtáblázat + 8), fájlméret = szám(keresőtáblázat + 16), Memória_méretez = szám(keresőtáblázat + 20);
            int igazít_ÉRTÉK = szám(keresőtáblázat + 28);
            if (CÍM < START_felhasználó_app || CÍM >= KÉP_megszüntet_CÍM || Memória_méretez < 0 || Memória_méretez > KÉP_megszüntet_CÍM - CÍM
                || fájlméret < 0 || fájlméret > Memória_méretez || Pozíció < 0 || (fájlméret > 0 && Pozíció > hossz_ÉRTÉK - fájlméret)
                || (igazít_ÉRTÉK != 0 && (igazít_ÉRTÉK < 0 || (igazít_ÉRTÉK & (igazít_ÉRTÉK - 1)) != 0
                    || ((CÍM - Pozíció) & (igazít_ÉRTÉK - 1)) != 0))) return -8;
            for (int elülső_kamera_ÉRTÉK = 0; elülső_kamera_ÉRTÉK < INDEX; elülső_kamera_ÉRTÉK++) {
                int Előző_cikk = Fájl + tábla_pozíció + elülső_kamera_ÉRTÉK * 32;
                if (szám(Előző_cikk) == 1 && Memória_méretez > 0 && szám(Előző_cikk + 20) > 0
                    && CÍM < szám(Előző_cikk + 8) + szám(Előző_cikk + 20) && szám(Előző_cikk + 8) < CÍM + Memória_méretez) return -8;
            }
            if ((szám(keresőtáblázat + 24) & 1) != 0 && belépési_pont_ÉRTÉK >= CÍM && belépési_pont_ÉRTÉK - CÍM < fájlméret) informatikai_részleg_végrehajtható = true;
        }
        return informatikai_részleg_végrehajtható ? belépési_pont_ÉRTÉK : -8;
    }

    static int végrehajt_parancs(int[] bevitel_ÉRTÉK, int Futtatás, int hossz_ÉRTÉK) {
        while (Futtatás < hossz_ÉRTÉK && bevitel_ÉRTÉK[Futtatás] == ' ') Futtatás++;
        int 끝 = Futtatás;
        while (끝 < hossz_ÉRTÉK && bevitel_ÉRTÉK[끝] != ' ') 끝++;
        int bejegyzés_ÉRTÉK = keres_bejegyzés(bevitel_ÉRTÉK, Futtatás, 끝 - Futtatás);
        if (bejegyzés_ÉRTÉK == 0) return -2;
        int Pozíció = szám(bejegyzés_ÉRTÉK + 16), Méret = szám(bejegyzés_ÉRTÉK + 20);
        if (Pozíció < 8 + Csoport_DARAB() * 24 || Méret < 52 || Pozíció > mobil_ÉRTÉK.végrehajtható_köteg_méretez() - Méret) return -8;
        int Fájl = mobil_ÉRTÉK.végrehajtható_köteg() + Pozíció;
        int belépési_pont_ÉRTÉK = ellenőriz(Fájl, Méret);
        if (belépési_pont_ÉRTÉK < 0) return belépési_pont_ÉRTÉK;
        mobil_ÉRTÉK.felhasználó_töröl_Tartalom();
        int tábla_pozíció = szám(Fájl + 28), cikk_DARAB = 짧은수(Fájl + 44);
        for (int INDEX = 0; INDEX < cikk_DARAB; INDEX++) {
            int keresőtáblázat = Fájl + tábla_pozíció + INDEX * 32;
            if (szám(keresőtáblázat) != 1) continue;
            int 원본 = Fájl + szám(keresőtáblázat + 4), cél_ÉRTÉK = szám(keresőtáblázat + 8), fájlméret = szám(keresőtáblázat + 16);
            for (int bájt_ÉRTÉK = 0; bájt_ÉRTÉK < fájlméret; bájt_ÉRTÉK++) mobil_ÉRTÉK.ír_Memória(cél_ÉRTÉK + bájt_ÉRTÉK, mobil_ÉRTÉK.기억읽기(원본 + bájt_ÉRTÉK));
        }
        argumentum_DARAB = 0;
        int tár_ÉRTÉK = argumentum_START;
        while (끝 < hossz_ÉRTÉK) {
            while (끝 < hossz_ÉRTÉK && bevitel_ÉRTÉK[끝] == ' ') 끝++;
            if (끝 == hossz_ÉRTÉK) break;
            if (argumentum_DARAB == argumentum_CÍM.length) return -22;
            Futtatás = 끝;
            while (끝 < hossz_ÉRTÉK && bevitel_ÉRTÉK[끝] != ' ') 끝++;
            argumentum_CÍM[argumentum_DARAB++] = tár_ÉRTÉK;
            ír_szám(tár_ÉRTÉK, 끝 - Futtatás);
            for (int karakter_ÉRTÉK = Futtatás; karakter_ÉRTÉK < 끝; karakter_ÉRTÉK++) ír_szám(tár_ÉRTÉK + 4 + (karakter_ÉRTÉK - Futtatás) * 4, bevitel_ÉRTÉK[karakter_ÉRTÉK]);
            tár_ÉRTÉK += 4 + (끝 - Futtatás) * 4;
        }
        hálózat_Sor.TISZTÍT_folyamat();
        파일서술자관리.START_folyamat();
        int KR = mobil_ÉRTÉK.futtat_felhasználó_app(belépési_pont_ÉRTÉK, felhasználó_megszüntet - 16);
        파일서술자관리.TISZTÍT_folyamat();
        hálózat_Sor.TISZTÍT_folyamat();
        return KR;
    }
}
