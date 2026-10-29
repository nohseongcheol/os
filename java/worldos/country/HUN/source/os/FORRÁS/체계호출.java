// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 felhasználó mutató/길이는 hozzáfér_bejegyzés 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int TÖMB_hossz(int CÍM) {
        if (!végrehajtás_kezelő.klip(CÍM, 4)) return -14;
        int hossz_ÉRTÉK = végrehajtás_kezelő.szám(CÍM);
        if (hossz_ÉRTÉK < 0 || hossz_ÉRTÉK > (végrehajtás_kezelő.felhasználó_megszüntet - CÍM - 4) / 4) return -14;
        return hossz_ÉRTÉK;
    }

    public static int folyamat_ÉRTÉK_bejegyzés(int INDEX, int 가, int MPERC_operandus, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.készít_Fájl(가, MPERC_operandus, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, MPERC_operandus, 다);
        if (INDEX == 32) return 파일서술자관리.ír_Fájl(가, MPERC_operandus, 다);
        if (INDEX == 33) return 파일서술자관리.bezár_Fájl(가);
        if (INDEX == 34) return 파일서술자관리.keres_Fájl(가, MPERC_operandus, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, MPERC_operandus, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, MPERC_operandus);
        if (INDEX == 38) return 파일서술자관리.eltávolít_Fájl_bejegyzés_név(가);
        if (INDEX == 39) return 파일서술자관리.halmaz_Fájl_hossz(가, MPERC_operandus);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, MPERC_operandus, 다);
        if (INDEX == 41) return 파일서술자관리.készít_végpont(가, MPERC_operandus, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_CÍM(가, MPERC_operandus, 다);
        if (INDEX == 43) return 파일서술자관리.küld_datagram_adat(가, MPERC_operandus, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.fogad_datagram_adat(가, MPERC_operandus, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, MPERC_operandus, 다);
        if (INDEX == 46) return 파일서술자관리.halmaz_fogad_IDŐTÚLLÉPÉS(가, MPERC_operandus);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.Altípus_ÉRTÉK[기술] != 2) return -22;
            return 파일보존.szinkronizál();
        }
        if (INDEX == 1) {
            int hossz_ÉRTÉK = TÖMB_hossz(가);
            if (hossz_ÉRTÉK < 0) return hossz_ÉRTÉK;
            if (hossz_ÉRTÉK > 4096) return -90;
            for (int karakter_ÉRTÉK = 0; karakter_ÉRTÉK < hossz_ÉRTÉK; karakter_ÉRTÉK++) SMS_Terminál.문자(végrehajtás_kezelő.szám(가 + 4 + karakter_ÉRTÉK * 4) & 65535);
            return hossz_ÉRTÉK;
        }
        if (INDEX == 2) return végrehajtás_kezelő.argumentum_DARAB;
        if (INDEX == 3) return 가 >= 0 && 가 < végrehajtás_kezelő.argumentum_DARAB ? végrehajtás_kezelő.argumentum_CÍM[가] : 0;
        if (INDEX == 10) return hálózat_Sor.Megnyitás(가);
        if (INDEX == 11) {
            int hossz_ÉRTÉK = TÖMB_hossz(라);
            if (hossz_ÉRTÉK < 0) return hossz_ÉRTÉK;
            if (마 < 0 || 마 > hossz_ÉRTÉK || 마 > 1024) return -90;
            for (int Pozíció = 0; Pozíció < 마; Pozíció++) 임시자료[Pozíció] = végrehajtás_kezelő.szám(라 + 4 + Pozíció * 4) & 255;
            return hálózat_Sor.küld(가, MPERC_operandus, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int hossz_ÉRTÉK = TÖMB_hossz(MPERC_operandus);
            if (hossz_ÉRTÉK < 0) return hossz_ÉRTÉK;
            if (다 < 0 || 다 > 2000) return -22;
            int KR = hálózat_Sor.fogad(가, 임시자료, hossz_ÉRTÉK < 1024 ? hossz_ÉRTÉK : 1024, 다);
            if (KR >= 0) for (int Pozíció = 0; Pozíció < KR; Pozíció++) végrehajtás_kezelő.ír_szám(MPERC_operandus + 4 + Pozíció * 4, 임시자료[Pozíció]);
            return KR;
        }
        if (INDEX == 13) return hálózat_Sor.Bezárás(가);
        if (INDEX == 14) return hálózat_Sor.내주소;
        if (INDEX == 15) return hálózat_Sor.társ_CÍM(가);
        if (INDEX == 16) return hálózat_Sor.társ_portszám(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminál.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int név_méretez = TÖMB_hossz(가), adat_méretez = TÖMB_hossz(MPERC_operandus);
            if (név_méretez < 0 || adat_méretez < 0) return -14;
            if (név_méretez < 1 || név_méretez > 64) return -22;
            int hossz_ÉRTÉK = 0;
            while (hossz_ÉRTÉK < név_méretez && végrehajtás_kezelő.szám(가 + 4 + hossz_ÉRTÉK * 4) != 0) {
                Memória_fájlrendszer.Név[hossz_ÉRTÉK] = végrehajtás_kezelő.szám(가 + 4 + hossz_ÉRTÉK * 4);
                hossz_ÉRTÉK++;
            }
            if (!Memória_fájlrendszer.csekk_név(Memória_fájlrendszer.Név, hossz_ÉRTÉK)) return -22;
            if (INDEX == 20) {
                int Fájl = Memória_fájlrendszer.keres_bejegyzés(Memória_fájlrendszer.Név, hossz_ÉRTÉK);
                if (Fájl < 0) return Fájl;
                int Méret = Memória_fájlrendszer.méretez_Lista[Fájl];
                if (Méret > adat_méretez) return -90;
                int CÍM = mobil_ÉRTÉK.Fájl_Memória() + Fájl * Memória_fájlrendszer.최대크기;
                for (int szám = 0; szám < Méret; szám++) végrehajtás_kezelő.ír_szám(MPERC_operandus + 4 + szám * 4, mobil_ÉRTÉK.기억읽기(CÍM + szám));
                return Méret;
            }
            if (다 < 0 || 다 > adat_méretez) return -22;
            if (다 > Memória_fájlrendszer.최대크기) return -90;
            for (int szám = 0; szám < 다; szám++) Memória_fájlrendszer.szerkeszt_ÉRTÉK[szám] = végrehajtás_kezelő.szám(MPERC_operandus + 4 + szám * 4) & 255;
            return Memória_fájlrendszer.tár_ÉRTÉK(Memória_fájlrendszer.Név, hossz_ÉRTÉK, Memória_fájlrendszer.szerkeszt_ÉRTÉK, 다);
        }
        return -38;
    }
}
