// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 felhasználó 과정의 파일서술자와 열린 Fájl 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int 읽기쓰기 = 2, készít_bejegyzés = 64, 독점생성 = 128, töröl_Tartalom = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] készít_leíró = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] Altípus_ÉRTÉK = new int[서술자한도], cél = new int[서술자한도];
    static int[] Fájl_pozíció = new int[서술자한도], készít_Gépház = new int[서술자한도], hivatkozik_DARAB = new int[서술자한도];
    static int[] hálózat_leíró = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] útvonal_név = new int[64], átvisz_adat = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return készít_leíró[파일서술자] - 1;
    }
    static int 빈서술자(int Futtatás) {
        for (int INDEX = Futtatás; INDEX < 서술자한도; INDEX++) if (készít_leíró[INDEX] == 0) return INDEX;
        return -24;
    }
    static int üres_leíró() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (hivatkozik_DARAB[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Kapcsolódás(int 서술자, int 기술, int Fájl_Altípus, int Fájl_cél, int Beállítások) {
        készít_leíró[서술자] = 기술 + 1; 서술자설정[서술자] = (Beállítások & 실행시닫기) != 0 ? 1 : 0;
        Altípus_ÉRTÉK[기술] = Fájl_Altípus; cél[기술] = Fájl_cél; hivatkozik_DARAB[기술] = 1;
        készít_Gépház[기술] = Beállítások & (3 | 이어쓰기 | 기다리지않기); Fájl_pozíció[기술] = 0;
        hálózat_leíró[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_folyamat() {
        TISZTÍT_folyamat();
        for (int INDEX = 0; INDEX < 3; INDEX++) Kapcsolódás(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void TISZTÍT_folyamat() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (készít_leíró[INDEX] != 0) bezár_Fájl(INDEX);
    }
    static int bezár_Fájl(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        készít_leíró[서술자] = 0; 서술자설정[서술자] = 0;
        hivatkozik_DARAB[기술]--;
        if (hivatkozik_DARAB[기술] == 0) {
            if (Altípus_ÉRTÉK[기술] == 2) Memória_fájlrendszer.készít_DARAB[cél[기술]]--;
            if (Altípus_ÉRTÉK[기술] == 3 && hálózat_leíró[기술] != 0) hálózat_Sor.Bezárás(hálózat_leíró[기술]);
            Altípus_ÉRTÉK[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bájt_ÉRTÉK 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int CÍM) {
        if (!végrehajtás_kezelő.klip(CÍM, 1)) return -14;
        int Pozíció = mobil_ÉRTÉK.기억읽기(CÍM) == '/' ? 1 : 0;
        for (int hossz_ÉRTÉK = 0; hossz_ÉRTÉK < 64; hossz_ÉRTÉK++) {
            if (!végrehajtás_kezelő.klip(CÍM + Pozíció + hossz_ÉRTÉK, 1)) return -14;
            int ÉRTÉK = mobil_ÉRTÉK.기억읽기(CÍM + Pozíció + hossz_ÉRTÉK);
            útvonal_név[hossz_ÉRTÉK] = ÉRTÉK;
            if (ÉRTÉK == 0) return hossz_ÉRTÉK == 0 ? -2 : (Memória_fájlrendszer.csekk_név(útvonal_név, hossz_ÉRTÉK) ? hossz_ÉRTÉK : -22);
            if (ÉRTÉK == '/') return -20;
        }
        return -36;
    }
    static int készít_Fájl(int név_CÍM, int Beállítások, int engedély_engedély) {
        int hossz_ÉRTÉK = 경로읽기(név_CÍM);
        if (hossz_ÉRTÉK < 0) return hossz_ÉRTÉK;
        if ((Beállítások & ~(3 | készít_bejegyzés | 독점생성 | töröl_Tartalom | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Beállítások & 3) == 3 || ((Beállítások & töröl_Tartalom) != 0 && (Beállítások & 3) == 0)) return -22;
        int Fájl = Memória_fájlrendszer.keres_bejegyzés(útvonal_név, hossz_ÉRTÉK);
        if (Fájl >= 0 && (Beállítások & (készít_bejegyzés | 독점생성)) == (készít_bejegyzés | 독점생성)) return -17;
        if (Fájl == -2 && (Beállítások & készít_bejegyzés) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = üres_leíró();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fájl == -2) {
            int KR = Memória_fájlrendszer.tár_ÉRTÉK(útvonal_név, hossz_ÉRTÉK, útvonal_név, 0);
            if (KR < 0) return KR;
            Fájl = Memória_fájlrendszer.keres_bejegyzés(útvonal_név, hossz_ÉRTÉK);
            Memória_fájlrendszer.허가들[Fájl] = engedély_engedély & 511;
        }
        if (Fájl < 0) return Fájl;
        if ((Beállítások & töröl_Tartalom) != 0) Memória_fájlrendszer.méretez_Lista[Fájl] = 0;
        Memória_fájlrendszer.készít_DARAB[Fájl]++;
        return Kapcsolódás(서술자, 기술, 2, Fájl, Beállítások);
    }
    static int 파일읽기(int 서술자, int adat_CÍM, int hossz_ÉRTÉK) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (készít_Gépház[기술] & 3) == 1) return -9;
        if (hossz_ÉRTÉK < 0) return -22;
        if (hossz_ÉRTÉK == 0) return 0;
        if (!végrehajtás_kezelő.klip(adat_CÍM, hossz_ÉRTÉK)) return -14;
        if (Altípus_ÉRTÉK[기술] == 3) return fogad_datagram_adat(서술자, adat_CÍM, hossz_ÉRTÉK, 0, 0);
        if (Altípus_ÉRTÉK[기술] == 1) {
            int KAPOTT_DARAB = 0;
            while (KAPOTT_DARAB < hossz_ÉRTÉK) {
                int ÉRTÉK = SMS_Terminál.직렬읽기();
                if (ÉRTÉK < 0) ÉRTÉK = billentyűzet.Olvasás();
                if (ÉRTÉK < 0) {
                    if (KAPOTT_DARAB > 0) return KAPOTT_DARAB;
                    if ((készít_Gépház[기술] & 기다리지않기) != 0) return -11;
                    if (mobil_ÉRTÉK.사용자남은밀리초() <= 10) return -11;
                    hálózat_Sor.igazol(); mobil_ÉRTÉK.잠시양보();
                } else {
                    mobil_ÉRTÉK.ír_Memória(adat_CÍM + KAPOTT_DARAB, ÉRTÉK); KAPOTT_DARAB++;
                }
            }
            return KAPOTT_DARAB;
        }
        int Fájl = cél[기술], Pozíció = Fájl_pozíció[기술];
        if (Pozíció >= Memória_fájlrendszer.méretez_Lista[Fájl]) return 0;
        if (hossz_ÉRTÉK > Memória_fájlrendszer.méretez_Lista[Fájl] - Pozíció) hossz_ÉRTÉK = Memória_fájlrendszer.méretez_Lista[Fájl] - Pozíció;
        int 원본주소 = mobil_ÉRTÉK.Fájl_Memória() + Fájl * Memória_fájlrendszer.최대크기 + Pozíció;
        for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) mobil_ÉRTÉK.ír_Memória(adat_CÍM + INDEX, mobil_ÉRTÉK.기억읽기(원본주소 + INDEX));
        Fájl_pozíció[기술] += hossz_ÉRTÉK;
        return hossz_ÉRTÉK;
    }
    static int ír_Fájl(int 서술자, int adat_CÍM, int hossz_ÉRTÉK) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (készít_Gépház[기술] & 3) == 0) return -9;
        if (hossz_ÉRTÉK < 0) return -22;
        if (hossz_ÉRTÉK == 0) return 0;
        if (!végrehajtás_kezelő.klip(adat_CÍM, hossz_ÉRTÉK)) return -14;
        if (Altípus_ÉRTÉK[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 cél_ÉRTÉK 주소가 필요하다.
        if (Altípus_ÉRTÉK[기술] == 1) {
            if (hossz_ÉRTÉK > 16384) hossz_ÉRTÉK = 16384;
            for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) {
                int ÉRTÉK = mobil_ÉRTÉK.기억읽기(adat_CÍM + INDEX);
                SMS_Terminál.직렬바이트(ÉRTÉK); SMS_Terminál.화면문자(ÉRTÉK);
            }
            return hossz_ÉRTÉK;
        }
        int Fájl = cél[기술], Méret = Memória_fájlrendszer.méretez_Lista[Fájl];
        int Pozíció = (készít_Gépház[기술] & 이어쓰기) != 0 ? Méret : Fájl_pozíció[기술];
        if (Pozíció >= Memória_fájlrendszer.최대크기) return -27;
        if (hossz_ÉRTÉK > Memória_fájlrendszer.최대크기 - Pozíció) hossz_ÉRTÉK = Memória_fájlrendszer.최대크기 - Pozíció;
        int cél_CÍM_08bbd577 = mobil_ÉRTÉK.Fájl_Memória() + Fájl * Memória_fájlrendszer.최대크기;
        for (int INDEX = Méret; INDEX < Pozíció; INDEX++) mobil_ÉRTÉK.ír_Memória(cél_CÍM_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) mobil_ÉRTÉK.ír_Memória(cél_CÍM_08bbd577 + Pozíció + INDEX, mobil_ÉRTÉK.기억읽기(adat_CÍM + INDEX));
        Fájl_pozíció[기술] = Pozíció + hossz_ÉRTÉK;
        if (Pozíció + hossz_ÉRTÉK > Méret) Memória_fájlrendszer.méretez_Lista[Fájl] = Pozíció + hossz_ÉRTÉK;
        return hossz_ÉRTÉK;
    }
    static int keres_Fájl(int 서술자, int Ofszet_ÉRTÉK, int teendő_gyök) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Altípus_ÉRTÉK[기술] != 2) return -29;
        if (teendő_gyök < 0 || teendő_gyök > 2) return -22;
        int Háttér_ÉRTÉK = teendő_gyök == 0 ? 0 : (teendő_gyök == 1 ? Fájl_pozíció[기술] : Memória_fájlrendszer.méretez_Lista[cél[기술]]);
        if (Ofszet_ÉRTÉK > 0 && Háttér_ÉRTÉK > 2147483647 - Ofszet_ÉRTÉK) return -75;
        if (Ofszet_ÉRTÉK < 0 && Ofszet_ÉRTÉK < -Háttér_ÉRTÉK) return -22;
        Fájl_pozíció[기술] = Háttér_ÉRTÉK + Ofszet_ÉRTÉK;
        return Fájl_pozíció[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean átruház_ÉRTÉK, int Beállítások) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return átruház_ÉRTÉK ? -9 : -22;
        if (átruház_ÉRTÉK && 서술자 == 새서술자) return 새서술자;
        if (átruház_ÉRTÉK) { if (készít_leíró[새서술자] != 0) bezár_Fájl(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        készít_leíró[새서술자] = 기술 + 1; 서술자설정[새서술자] = Beállítások; hivatkozik_DARAB[기술]++;
        return 새서술자;
    }
    static int eltávolít_Fájl_bejegyzés_név(int név_CÍM) {
        int hossz_ÉRTÉK = 경로읽기(név_CÍM);
        if (hossz_ÉRTÉK < 0) return hossz_ÉRTÉK;
        int Fájl = Memória_fájlrendszer.keres_bejegyzés(útvonal_név, hossz_ÉRTÉK);
        if (Fájl < 0) return Fájl;
        Memória_fájlrendszer.이름들[Fájl * 64] = 0;
        return 0;
    }
    static int halmaz_Fájl_hossz(int 서술자, int hossz_ÉRTÉK) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Altípus_ÉRTÉK[기술] != 2 || (készít_Gépház[기술] & 3) == 0 || hossz_ÉRTÉK < 0) return -22;
        if (hossz_ÉRTÉK > Memória_fájlrendszer.최대크기) return -27;
        int Fájl = cél[기술], CÍM = mobil_ÉRTÉK.Fájl_Memória() + Fájl * Memória_fájlrendszer.최대크기;
        for (int INDEX = Memória_fájlrendszer.méretez_Lista[Fájl]; INDEX < hossz_ÉRTÉK; INDEX++) mobil_ÉRTÉK.ír_Memória(CÍM + INDEX, 0);
        Memória_fájlrendszer.méretez_Lista[Fájl] = hossz_ÉRTÉK;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int CÍM) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!végrehajtás_kezelő.klip(CÍM, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) végrehajtás_kezelő.ír_szám(CÍM + INDEX * 4, 0);
        int Fájl = cél[기술], Méret = Altípus_ÉRTÉK[기술] == 2 ? Memória_fájlrendszer.méretez_Lista[Fájl] : 0;
        int engedély_engedély = Altípus_ÉRTÉK[기술] == 2 ? Memória_fájlrendszer.허가들[Fájl] : 438;
        végrehajtás_kezelő.ír_szám(CÍM, 1);
        végrehajtás_kezelő.ír_szám(CÍM + 4, Altípus_ÉRTÉK[기술] == 2 ? Fájl + 1 : 100 + 기술);
        végrehajtás_kezelő.ír_szám(CÍM + 8, (Altípus_ÉRTÉK[기술] == 2 ? 32768 : (Altípus_ÉRTÉK[기술] == 1 ? 8192 : 49152)) | engedély_engedély);
        végrehajtás_kezelő.ír_szám(CÍM + 12, Altípus_ÉRTÉK[기술] == 2 && Memória_fájlrendszer.이름들[Fájl * 64] == 0 ? 0 : 1);
        végrehajtás_kezelő.ír_szám(CÍM + 28, Méret); végrehajtás_kezelő.ír_szám(CÍM + 32, 512);
        végrehajtás_kezelő.ír_szám(CÍM + 36, (Méret + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Parancs, int ÉRTÉK) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Parancs == 0 || Parancs == 1030) return 서술자복제(서술자, ÉRTÉK, false, Parancs == 1030 ? 1 : 0);
        if (Parancs == 1) return 서술자설정[서술자];
        if (Parancs == 2) { if ((ÉRTÉK & ~1) != 0) return -22; 서술자설정[서술자] = ÉRTÉK; return 0; }
        if (Parancs == 3) return készít_Gépház[기술];
        if (Parancs == 4) {
            if ((ÉRTÉK & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            készít_Gépház[기술] = (készít_Gépház[기술] & 3) | (ÉRTÉK & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int készít_végpont(int 주소체계, int hálózat_Altípus, int eset_szám) {
        if (주소체계 != 2) return -97;
        if (hálózat_Altípus != 2) return -93;
        if (eset_szám != 0 && eset_szám != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = üres_leíró();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Kapcsolódás(서술자, 기술, 3, 0, 읽기쓰기);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return Altípus_ÉRTÉK[기술] == 3 ? 기술 : -88;
    }
    static int CÍM_32(int CÍM) {
        return mobil_ÉRTÉK.기억읽기(CÍM) << 24 | mobil_ÉRTÉK.기억읽기(CÍM + 1) << 16
            | mobil_ÉRTÉK.기억읽기(CÍM + 2) << 8 | mobil_ÉRTÉK.기억읽기(CÍM + 3);
    }
    static int csekk_CÍM(int CÍM, int hossz_ÉRTÉK) {
        if (hossz_ÉRTÉK < 16) return -22;
        if (!végrehajtás_kezelő.klip(CÍM, 16)) return -14;
        return végrehajtás_kezelő.짧은수(CÍM) == 2 ? 0 : -97;
    }
    static int BIND_CÍM(int 서술자, int CÍM, int hossz_ÉRTÉK) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int KR = csekk_CÍM(CÍM, hossz_ÉRTÉK);
        if (KR < 0) return KR;
        if (hálózat_leíró[기술] != 0) return -22;
        int hálózati_azonosító = CÍM_32(CÍM + 4);
        if (hálózati_azonosító != 0 && hálózati_azonosító != hálózat_Sor.내주소) return -99;
        int portszám = mobil_ÉRTÉK.기억읽기(CÍM + 2) << 8 | mobil_ÉRTÉK.기억읽기(CÍM + 3);
        KR = hálózat_Sor.Megnyitás(portszám);
        if (KR < 0) return KR;
        hálózat_leíró[기술] = KR; cél[기술] = hálózati_azonosító;
        return 0;
    }
    static int Automata_BIND(int 기술) {
        if (hálózat_leíró[기술] != 0) return 0;
        int KR = hálózat_Sor.Megnyitás(0);
        if (KR < 0) return KR;
        hálózat_leíró[기술] = KR;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 kérés 구조체로 전달한다.
    static int küld_datagram_adat(int 서술자, int adat_CÍM, int hossz_ÉRTÉK, int Beállítások, int igényelt_CÍM) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Beállítások != 0) return -95;
        if (hossz_ÉRTÉK < 0 || hossz_ÉRTÉK > 1024) return -90;
        if (hossz_ÉRTÉK != 0 && !végrehajtás_kezelő.klip(adat_CÍM, hossz_ÉRTÉK)) return -14;
        if (!végrehajtás_kezelő.klip(igényelt_CÍM, 8)) return -14;
        int CÍM = végrehajtás_kezelő.szám(igényelt_CÍM);
        int KR = csekk_CÍM(CÍM, végrehajtás_kezelő.szám(igényelt_CÍM + 4));
        if (KR < 0) return KR;
        int portszám = mobil_ÉRTÉK.기억읽기(CÍM + 2) << 8 | mobil_ÉRTÉK.기억읽기(CÍM + 3);
        if (portszám == 0) return -22;
        KR = Automata_BIND(기술);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) átvisz_adat[INDEX] = mobil_ÉRTÉK.기억읽기(adat_CÍM + INDEX);
        return hálózat_Sor.küld(hálózat_leíró[기술], CÍM_32(CÍM + 4), portszám, átvisz_adat, hossz_ÉRTÉK);
    }
    static void ír_CÍM(int CÍM, int hossz_ÉRTÉK, int hálózati_azonosító, int portszám) {
        for (int INDEX = 0; INDEX < hossz_ÉRTÉK && INDEX < 16; INDEX++) {
            int ÉRTÉK = 0;
            if (INDEX == 0) ÉRTÉK = 2;
            if (INDEX == 2) ÉRTÉK = portszám >>> 8;
            if (INDEX == 3) ÉRTÉK = portszám;
            if (INDEX >= 4 && INDEX < 8) ÉRTÉK = hálózati_azonosító >>> (56 - INDEX * 8);
            mobil_ÉRTÉK.ír_Memória(CÍM + INDEX, ÉRTÉK & 255);
        }
    }
    static int fogad_datagram_adat(int 서술자, int adat_CÍM, int hossz_ÉRTÉK, int Beállítások, int igényelt_CÍM) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Beállítások & ~64) != 0) return -95;
        if (hossz_ÉRTÉK < 0) return -22;
        if (hossz_ÉRTÉK != 0 && !végrehajtás_kezelő.klip(adat_CÍM, hossz_ÉRTÉK)) return -14;
        int CÍM = 0, CÍM_hossz_CÍM = 0, CÍM_hossz = 0;
        if (igényelt_CÍM != 0) {
            if (!végrehajtás_kezelő.klip(igényelt_CÍM, 8)) return -14;
            CÍM = végrehajtás_kezelő.szám(igényelt_CÍM); CÍM_hossz_CÍM = végrehajtás_kezelő.szám(igényelt_CÍM + 4);
            if (CÍM != 0) {
                if (!végrehajtás_kezelő.klip(CÍM_hossz_CÍM, 4)) return -14;
                CÍM_hossz = végrehajtás_kezelő.szám(CÍM_hossz_CÍM);
                if (CÍM_hossz < 0) return -22;
                if (!végrehajtás_kezelő.klip(CÍM, CÍM_hossz < 16 ? CÍM_hossz : 16)) return -14;
            }
        }
        int KR = Automata_BIND(기술);
        if (KR < 0) return KR;
        int Futtatás = mobil_ÉRTÉK.밀리초();
        while (true) {
            KR = hálózat_Sor.fogad(hálózat_leíró[기술], átvisz_adat, 1024, 0);
            if (KR != -11) break;
            if ((Beállítások & 64) != 0 || (készít_Gépház[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && mobil_ÉRTÉK.밀리초() - Futtatás >= 수신대기밀리초[기술]) return -11;
            if (mobil_ÉRTÉK.사용자남은밀리초() <= 10) return -11;
            mobil_ÉRTÉK.잠시양보();
        }
        if (KR < 0) return KR;
        if (KR > hossz_ÉRTÉK) KR = hossz_ÉRTÉK;
        for (int INDEX = 0; INDEX < KR; INDEX++) mobil_ÉRTÉK.ír_Memória(adat_CÍM + INDEX, átvisz_adat[INDEX]);
        if (CÍM != 0) {
            ír_CÍM(CÍM, CÍM_hossz, hálózat_Sor.társ_CÍM(hálózat_leíró[기술]), hálózat_Sor.társ_portszám(hálózat_leíró[기술]));
            végrehajtás_kezelő.ír_szám(CÍM_hossz_CÍM, 16);
        }
        return KR;
    }
    static int 통신주소읽기(int 서술자, int CÍM, int hossz_CÍM) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!végrehajtás_kezelő.klip(hossz_CÍM, 4)) return -14;
        int hossz_ÉRTÉK = végrehajtás_kezelő.szám(hossz_CÍM);
        if (hossz_ÉRTÉK < 0) return -22;
        if (!végrehajtás_kezelő.klip(CÍM, hossz_ÉRTÉK < 16 ? hossz_ÉRTÉK : 16)) return -14;
        int tárolóhely_bejegyzés = hálózat_Sor.INDEX(hálózat_leíró[기술]);
        ír_CÍM(CÍM, hossz_ÉRTÉK, cél[기술], tárolóhely_bejegyzés < 0 ? 0 : hálózat_Sor.접속번호들[tárolóhely_bejegyzés]);
        végrehajtás_kezelő.ír_szám(hossz_CÍM, 16);
        return 0;
    }
    static int halmaz_fogad_IDŐTÚLLÉPÉS(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
