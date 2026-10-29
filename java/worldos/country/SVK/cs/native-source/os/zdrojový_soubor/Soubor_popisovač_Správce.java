// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 uživatelský_prostor 과정의 파일서술자와 열린 název_souboru 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class Soubor_popisovač_Správce {
    static final int 서술자한도 = 32;
    static final int pro_čtení_i_zápis_příznak = 2, Create_položka = 64, 독점생성 = 128, vymazat_Obsah = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] otevřít_úchyt = new int[서술자한도], sada_popisovač = new int[서술자한도];
    static int[] Druh_HODNOTA = new int[서술자한도], cílová_úroveň = new int[서술자한도];
    static int[] Soubor_pozice = new int[서술자한도], otevřít_Nastavení = new int[서술자한도], odkaz_POČET = new int[서술자한도];
    static int[] síť_úchyt = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] cesta_název = new int[64], přenos_data = new int[1024];

    static int NAJÍT_popisovač(int Soubor_popisovač) {
        if (Soubor_popisovač < 0 || Soubor_popisovač >= 서술자한도) return -9;
        return otevřít_úchyt[Soubor_popisovač] - 1;
    }
    static int 빈서술자(int Spustit_2) {
        for (int INDEX = Spustit_2; INDEX < 서술자한도; INDEX++) if (otevřít_úchyt[INDEX] == 0) return INDEX;
        return -24;
    }
    static int 빈기술() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (odkaz_POČET[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Připojit(int popisovač_položka, int popisovač_HODNOTA, int Soubor_Druh, int Soubor_cílová_úroveň, int Nastavení) {
        otevřít_úchyt[popisovač_položka] = popisovač_HODNOTA + 1; sada_popisovač[popisovač_položka] = (Nastavení & 실행시닫기) != 0 ? 1 : 0;
        Druh_HODNOTA[popisovač_HODNOTA] = Soubor_Druh; cílová_úroveň[popisovač_HODNOTA] = Soubor_cílová_úroveň; odkaz_POČET[popisovač_HODNOTA] = 1;
        otevřít_Nastavení[popisovač_HODNOTA] = Nastavení & (3 | 이어쓰기 | 기다리지않기); Soubor_pozice[popisovač_HODNOTA] = 0;
        síť_úchyt[popisovač_HODNOTA] = 0; 수신대기밀리초[popisovač_HODNOTA] = 0;
        return popisovač_položka;
    }
    static void START_Proces() {
        Čisté_Proces();
        for (int INDEX = 0; INDEX < 3; INDEX++) Připojit(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void Čisté_Proces() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (otevřít_úchyt[INDEX] != 0) Zavřít_Soubor(INDEX);
    }
    static int Zavřít_Soubor(int popisovač_položka) {
        int popisovač_HODNOTA = NAJÍT_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return -9;
        otevřít_úchyt[popisovač_položka] = 0; sada_popisovač[popisovač_položka] = 0;
        odkaz_POČET[popisovač_HODNOTA]--;
        if (odkaz_POČET[popisovač_HODNOTA] == 0) {
            if (Druh_HODNOTA[popisovač_HODNOTA] == 2) Paměť_systém_souborů.otevřít_POČET[cílová_úroveň[popisovač_HODNOTA]]--;
            if (Druh_HODNOTA[popisovač_HODNOTA] == 3 && síť_úchyt[popisovač_HODNOTA] != 0) síť_Štos.Zavřené(síť_úchyt[popisovač_HODNOTA]);
            Druh_HODNOTA[popisovač_HODNOTA] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bajt_HODNOTA 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int Adresa) {
        if (!spuštění_Správce.oříznout(Adresa, 1)) return -14;
        int pozice = mobilní_HODNOTA.기억읽기(Adresa) == '/' ? 1 : 0;
        for (int délka_HODNOTA = 0; délka_HODNOTA < 64; délka_HODNOTA++) {
            if (!spuštění_Správce.oříznout(Adresa + pozice + délka_HODNOTA, 1)) return -14;
            int HODNOTA = mobilní_HODNOTA.기억읽기(Adresa + pozice + délka_HODNOTA);
            cesta_název[délka_HODNOTA] = HODNOTA;
            if (HODNOTA == 0) return délka_HODNOTA == 0 ? -2 : (Paměť_systém_souborů.šek_název(cesta_název, délka_HODNOTA) ? délka_HODNOTA : -22);
            if (HODNOTA == '/') return -20;
        }
        return -36;
    }
    static int otevřít_Soubor(int název_ODKAZ, int Nastavení, int oprávnění_oprávnění) {
        int délka_HODNOTA = 경로읽기(název_ODKAZ);
        if (délka_HODNOTA < 0) return délka_HODNOTA;
        if ((Nastavení & ~(3 | Create_položka | 독점생성 | vymazat_Obsah | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Nastavení & 3) == 3 || ((Nastavení & vymazat_Obsah) != 0 && (Nastavení & 3) == 0)) return -22;
        int název_souboru = Paměť_systém_souborů.NAJÍT_položka(cesta_název, délka_HODNOTA);
        if (název_souboru >= 0 && (Nastavení & (Create_položka | 독점생성)) == (Create_položka | 독점생성)) return -17;
        if (název_souboru == -2 && (Nastavení & Create_položka) == 0) return -2;
        int popisovač_položka = 빈서술자(0), popisovač_HODNOTA = 빈기술();
        if (popisovač_položka < 0 || popisovač_HODNOTA < 0) return -24;
        if (název_souboru == -2) {
            int VÝSLEDEK = Paměť_systém_souborů.Store_HODNOTA(cesta_název, délka_HODNOTA, cesta_název, 0);
            if (VÝSLEDEK < 0) return VÝSLEDEK;
            název_souboru = Paměť_systém_souborů.NAJÍT_položka(cesta_název, délka_HODNOTA);
            Paměť_systém_souborů.허가들[název_souboru] = oprávnění_oprávnění & 511;
        }
        if (název_souboru < 0) return název_souboru;
        if ((Nastavení & vymazat_Obsah) != 0) Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru] = 0;
        Paměť_systém_souborů.otevřít_POČET[název_souboru]++;
        return Připojit(popisovač_položka, popisovač_HODNOTA, 2, název_souboru, Nastavení);
    }
    static int 파일읽기(int popisovač_položka, int data_ODKAZ, int délka_HODNOTA) {
        int popisovač_HODNOTA = NAJÍT_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0 || (otevřít_Nastavení[popisovač_HODNOTA] & 3) == 1) return -9;
        if (délka_HODNOTA < 0) return -22;
        if (délka_HODNOTA == 0) return 0;
        if (!spuštění_Správce.oříznout(data_ODKAZ, délka_HODNOTA)) return -14;
        if (Druh_HODNOTA[popisovač_HODNOTA] == 3) return dostat_datagram_data(popisovač_položka, data_ODKAZ, délka_HODNOTA, 0, 0);
        if (Druh_HODNOTA[popisovač_HODNOTA] == 1) {
            int RECEIVED_POČET = 0;
            while (RECEIVED_POČET < délka_HODNOTA) {
                int HODNOTA = SMS_Terminál.직렬읽기();
                if (HODNOTA < 0) HODNOTA = klávesnice.Čtení();
                if (HODNOTA < 0) {
                    if (RECEIVED_POČET > 0) return RECEIVED_POČET;
                    if ((otevřít_Nastavení[popisovač_HODNOTA] & 기다리지않기) != 0) return -11;
                    if (mobilní_HODNOTA.사용자남은밀리초() <= 10) return -11;
                    síť_Štos.ověřit(); mobilní_HODNOTA.잠시양보();
                } else {
                    mobilní_HODNOTA.zápis_Paměť(data_ODKAZ + RECEIVED_POČET, HODNOTA); RECEIVED_POČET++;
                }
            }
            return RECEIVED_POČET;
        }
        int název_souboru = cílová_úroveň[popisovač_HODNOTA], pozice = Soubor_pozice[popisovač_HODNOTA];
        if (pozice >= Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru]) return 0;
        if (délka_HODNOTA > Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru] - pozice) délka_HODNOTA = Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru] - pozice;
        int 원본주소 = mobilní_HODNOTA.Soubor_Paměť() + název_souboru * Paměť_systém_souborů.최대크기 + pozice;
        for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) mobilní_HODNOTA.zápis_Paměť(data_ODKAZ + INDEX, mobilní_HODNOTA.기억읽기(원본주소 + INDEX));
        Soubor_pozice[popisovač_HODNOTA] += délka_HODNOTA;
        return délka_HODNOTA;
    }
    static int zápis_Soubor(int popisovač_položka, int data_ODKAZ, int délka_HODNOTA) {
        int popisovač_HODNOTA = NAJÍT_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0 || (otevřít_Nastavení[popisovač_HODNOTA] & 3) == 0) return -9;
        if (délka_HODNOTA < 0) return -22;
        if (délka_HODNOTA == 0) return 0;
        if (!spuštění_Správce.oříznout(data_ODKAZ, délka_HODNOTA)) return -14;
        if (Druh_HODNOTA[popisovač_HODNOTA] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 cíl_HODNOTA 주소가 필요하다.
        if (Druh_HODNOTA[popisovač_HODNOTA] == 1) {
            if (délka_HODNOTA > 16384) délka_HODNOTA = 16384;
            for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) {
                int HODNOTA = mobilní_HODNOTA.기억읽기(data_ODKAZ + INDEX);
                SMS_Terminál.직렬바이트(HODNOTA); SMS_Terminál.화면문자(HODNOTA);
            }
            return délka_HODNOTA;
        }
        int název_souboru = cílová_úroveň[popisovač_HODNOTA], Velikost = Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru];
        int pozice = (otevřít_Nastavení[popisovač_HODNOTA] & 이어쓰기) != 0 ? Velikost : Soubor_pozice[popisovač_HODNOTA];
        if (pozice >= Paměť_systém_souborů.최대크기) return -27;
        if (délka_HODNOTA > Paměť_systém_souborů.최대크기 - pozice) délka_HODNOTA = Paměť_systém_souborů.최대크기 - pozice;
        int cíl_ODKAZ_08bbd577 = mobilní_HODNOTA.Soubor_Paměť() + název_souboru * Paměť_systém_souborů.최대크기;
        for (int INDEX = Velikost; INDEX < pozice; INDEX++) mobilní_HODNOTA.zápis_Paměť(cíl_ODKAZ_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) mobilní_HODNOTA.zápis_Paměť(cíl_ODKAZ_08bbd577 + pozice + INDEX, mobilní_HODNOTA.기억읽기(data_ODKAZ + INDEX));
        Soubor_pozice[popisovač_HODNOTA] = pozice + délka_HODNOTA;
        if (pozice + délka_HODNOTA > Velikost) Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru] = pozice + délka_HODNOTA;
        return délka_HODNOTA;
    }
    static int hledat_Soubor(int popisovač_položka, int POSUN_HODNOTA, int akce_kořen) {
        int popisovač_HODNOTA = NAJÍT_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return -9;
        if (Druh_HODNOTA[popisovač_HODNOTA] != 2) return -29;
        if (akce_kořen < 0 || akce_kořen > 2) return -22;
        int Pozadí_HODNOTA = akce_kořen == 0 ? 0 : (akce_kořen == 1 ? Soubor_pozice[popisovač_HODNOTA] : Paměť_systém_souborů.změnit_velikost_Seznam[cílová_úroveň[popisovač_HODNOTA]]);
        if (POSUN_HODNOTA > 0 && Pozadí_HODNOTA > 2147483647 - POSUN_HODNOTA) return -75;
        if (POSUN_HODNOTA < 0 && POSUN_HODNOTA < -Pozadí_HODNOTA) return -22;
        Soubor_pozice[popisovač_HODNOTA] = Pozadí_HODNOTA + POSUN_HODNOTA;
        return Soubor_pozice[popisovač_HODNOTA];
    }
    static int duplikát_popisovač(int popisovač_položka, int 새서술자, boolean Přiřadit_HODNOTA, int Nastavení) {
        int popisovač_HODNOTA = NAJÍT_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Přiřadit_HODNOTA ? -9 : -22;
        if (Přiřadit_HODNOTA && popisovač_položka == 새서술자) return 새서술자;
        if (Přiřadit_HODNOTA) { if (otevřít_úchyt[새서술자] != 0) Zavřít_Soubor(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        otevřít_úchyt[새서술자] = popisovač_HODNOTA + 1; sada_popisovač[새서술자] = Nastavení; odkaz_POČET[popisovač_HODNOTA]++;
        return 새서술자;
    }
    static int odebrat_Soubor_položka_název(int název_ODKAZ) {
        int délka_HODNOTA = 경로읽기(název_ODKAZ);
        if (délka_HODNOTA < 0) return délka_HODNOTA;
        int název_souboru = Paměť_systém_souborů.NAJÍT_položka(cesta_název, délka_HODNOTA);
        if (název_souboru < 0) return název_souboru;
        Paměť_systém_souborů.이름들[název_souboru * 64] = 0;
        return 0;
    }
    static int sada_Soubor_délka(int popisovač_položka, int délka_HODNOTA) {
        int popisovač_HODNOTA = NAJÍT_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return -9;
        if (Druh_HODNOTA[popisovač_HODNOTA] != 2 || (otevřít_Nastavení[popisovač_HODNOTA] & 3) == 0 || délka_HODNOTA < 0) return -22;
        if (délka_HODNOTA > Paměť_systém_souborů.최대크기) return -27;
        int název_souboru = cílová_úroveň[popisovač_HODNOTA], Adresa = mobilní_HODNOTA.Soubor_Paměť() + název_souboru * Paměť_systém_souborů.최대크기;
        for (int INDEX = Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru]; INDEX < délka_HODNOTA; INDEX++) mobilní_HODNOTA.zápis_Paměť(Adresa + INDEX, 0);
        Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru] = délka_HODNOTA;
        return 0;
    }
    static int 파일상태읽기(int popisovač_položka, int Adresa) {
        int popisovač_HODNOTA = NAJÍT_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return -9;
        if (!spuštění_Správce.oříznout(Adresa, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) spuštění_Správce.zápis_číslo(Adresa + INDEX * 4, 0);
        int název_souboru = cílová_úroveň[popisovač_HODNOTA], Velikost = Druh_HODNOTA[popisovač_HODNOTA] == 2 ? Paměť_systém_souborů.změnit_velikost_Seznam[název_souboru] : 0;
        int oprávnění_oprávnění = Druh_HODNOTA[popisovač_HODNOTA] == 2 ? Paměť_systém_souborů.허가들[název_souboru] : 438;
        spuštění_Správce.zápis_číslo(Adresa, 1);
        spuštění_Správce.zápis_číslo(Adresa + 4, Druh_HODNOTA[popisovač_HODNOTA] == 2 ? název_souboru + 1 : 100 + popisovač_HODNOTA);
        spuštění_Správce.zápis_číslo(Adresa + 8, (Druh_HODNOTA[popisovač_HODNOTA] == 2 ? 32768 : (Druh_HODNOTA[popisovač_HODNOTA] == 1 ? 8192 : 49152)) | oprávnění_oprávnění);
        spuštění_Správce.zápis_číslo(Adresa + 12, Druh_HODNOTA[popisovač_HODNOTA] == 2 && Paměť_systém_souborů.이름들[název_souboru * 64] == 0 ? 0 : 1);
        spuštění_Správce.zápis_číslo(Adresa + 28, Velikost); spuštění_Správce.zápis_číslo(Adresa + 32, 512);
        spuštění_Správce.zápis_číslo(Adresa + 36, (Velikost + 511) / 512);
        return 0;
    }
    static int řízení_popisovač(int popisovač_položka, int příkaz, int HODNOTA) {
        int popisovač_HODNOTA = NAJÍT_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return -9;
        if (příkaz == 0 || příkaz == 1030) return duplikát_popisovač(popisovač_položka, HODNOTA, false, příkaz == 1030 ? 1 : 0);
        if (příkaz == 1) return sada_popisovač[popisovač_položka];
        if (příkaz == 2) { if ((HODNOTA & ~1) != 0) return -22; sada_popisovač[popisovač_položka] = HODNOTA; return 0; }
        if (příkaz == 3) return otevřít_Nastavení[popisovač_HODNOTA];
        if (příkaz == 4) {
            if ((HODNOTA & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            otevřít_Nastavení[popisovač_HODNOTA] = (otevřít_Nastavení[popisovač_HODNOTA] & 3) | (HODNOTA & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Create_účastník(int 주소체계, int síť_Druh, int případ_číslo) {
        if (주소체계 != 2) return -97;
        if (síť_Druh != 2) return -93;
        if (případ_číslo != 0 && případ_číslo != 17) return -93;
        int popisovač_položka = 빈서술자(0), popisovač_HODNOTA = 빈기술();
        if (popisovač_položka < 0 || popisovač_HODNOTA < 0) return -24;
        return Připojit(popisovač_položka, popisovač_HODNOTA, 3, 0, pro_čtení_i_zápis_příznak);
    }
    static int účastník_popisovač(int popisovač_položka) {
        int popisovač_HODNOTA = NAJÍT_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return -9;
        return Druh_HODNOTA[popisovač_HODNOTA] == 3 ? popisovač_HODNOTA : -88;
    }
    static int ODKAZ_32(int Adresa) {
        return mobilní_HODNOTA.기억읽기(Adresa) << 24 | mobilní_HODNOTA.기억읽기(Adresa + 1) << 16
            | mobilní_HODNOTA.기억읽기(Adresa + 2) << 8 | mobilní_HODNOTA.기억읽기(Adresa + 3);
    }
    static int šek_ODKAZ(int Adresa, int délka_HODNOTA) {
        if (délka_HODNOTA < 16) return -22;
        if (!spuštění_Správce.oříznout(Adresa, 16)) return -14;
        return spuštění_Správce.짧은수(Adresa) == 2 ? 0 : -97;
    }
    static int vázat_ODKAZ(int popisovač_položka, int Adresa, int délka_HODNOTA) {
        int popisovač_HODNOTA = účastník_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return popisovač_HODNOTA;
        int VÝSLEDEK = šek_ODKAZ(Adresa, délka_HODNOTA);
        if (VÝSLEDEK < 0) return VÝSLEDEK;
        if (síť_úchyt[popisovač_HODNOTA] != 0) return -22;
        int ID_sítě = ODKAZ_32(Adresa + 4);
        if (ID_sítě != 0 && ID_sítě != síť_Štos.내주소) return -99;
        int číslo_portu = mobilní_HODNOTA.기억읽기(Adresa + 2) << 8 | mobilní_HODNOTA.기억읽기(Adresa + 3);
        VÝSLEDEK = síť_Štos.Otevřít(číslo_portu);
        if (VÝSLEDEK < 0) return VÝSLEDEK;
        síť_úchyt[popisovač_HODNOTA] = VÝSLEDEK; cílová_úroveň[popisovač_HODNOTA] = ID_sítě;
        return 0;
    }
    static int Automaticky_vázat(int popisovač_HODNOTA) {
        if (síť_úchyt[popisovač_HODNOTA] != 0) return 0;
        int VÝSLEDEK = síť_Štos.Otevřít(0);
        if (VÝSLEDEK < 0) return VÝSLEDEK;
        síť_úchyt[popisovač_HODNOTA] = VÝSLEDEK;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 žádost 구조체로 전달한다.
    static int poslat_datagram_data(int popisovač_položka, int data_ODKAZ, int délka_HODNOTA, int Nastavení, int vyžádáno_ODKAZ) {
        int popisovač_HODNOTA = účastník_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return popisovač_HODNOTA;
        if (Nastavení != 0) return -95;
        if (délka_HODNOTA < 0 || délka_HODNOTA > 1024) return -90;
        if (délka_HODNOTA != 0 && !spuštění_Správce.oříznout(data_ODKAZ, délka_HODNOTA)) return -14;
        if (!spuštění_Správce.oříznout(vyžádáno_ODKAZ, 8)) return -14;
        int Adresa = spuštění_Správce.číslo(vyžádáno_ODKAZ);
        int VÝSLEDEK = šek_ODKAZ(Adresa, spuštění_Správce.číslo(vyžádáno_ODKAZ + 4));
        if (VÝSLEDEK < 0) return VÝSLEDEK;
        int číslo_portu = mobilní_HODNOTA.기억읽기(Adresa + 2) << 8 | mobilní_HODNOTA.기억읽기(Adresa + 3);
        if (číslo_portu == 0) return -22;
        VÝSLEDEK = Automaticky_vázat(popisovač_HODNOTA);
        if (VÝSLEDEK < 0) return VÝSLEDEK;
        for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) přenos_data[INDEX] = mobilní_HODNOTA.기억읽기(data_ODKAZ + INDEX);
        return síť_Štos.poslat(síť_úchyt[popisovač_HODNOTA], ODKAZ_32(Adresa + 4), číslo_portu, přenos_data, délka_HODNOTA);
    }
    static void zápis_ODKAZ(int Adresa, int délka_HODNOTA, int ID_sítě, int číslo_portu) {
        for (int INDEX = 0; INDEX < délka_HODNOTA && INDEX < 16; INDEX++) {
            int HODNOTA = 0;
            if (INDEX == 0) HODNOTA = 2;
            if (INDEX == 2) HODNOTA = číslo_portu >>> 8;
            if (INDEX == 3) HODNOTA = číslo_portu;
            if (INDEX >= 4 && INDEX < 8) HODNOTA = ID_sítě >>> (56 - INDEX * 8);
            mobilní_HODNOTA.zápis_Paměť(Adresa + INDEX, HODNOTA & 255);
        }
    }
    static int dostat_datagram_data(int popisovač_položka, int data_ODKAZ, int délka_HODNOTA, int Nastavení, int vyžádáno_ODKAZ) {
        int popisovač_HODNOTA = účastník_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return popisovač_HODNOTA;
        if ((Nastavení & ~64) != 0) return -95;
        if (délka_HODNOTA < 0) return -22;
        if (délka_HODNOTA != 0 && !spuštění_Správce.oříznout(data_ODKAZ, délka_HODNOTA)) return -14;
        int Adresa = 0, ODKAZ_délka_ODKAZ = 0, ODKAZ_délka = 0;
        if (vyžádáno_ODKAZ != 0) {
            if (!spuštění_Správce.oříznout(vyžádáno_ODKAZ, 8)) return -14;
            Adresa = spuštění_Správce.číslo(vyžádáno_ODKAZ); ODKAZ_délka_ODKAZ = spuštění_Správce.číslo(vyžádáno_ODKAZ + 4);
            if (Adresa != 0) {
                if (!spuštění_Správce.oříznout(ODKAZ_délka_ODKAZ, 4)) return -14;
                ODKAZ_délka = spuštění_Správce.číslo(ODKAZ_délka_ODKAZ);
                if (ODKAZ_délka < 0) return -22;
                if (!spuštění_Správce.oříznout(Adresa, ODKAZ_délka < 16 ? ODKAZ_délka : 16)) return -14;
            }
        }
        int VÝSLEDEK = Automaticky_vázat(popisovač_HODNOTA);
        if (VÝSLEDEK < 0) return VÝSLEDEK;
        int Spustit_2 = mobilní_HODNOTA.밀리초();
        while (true) {
            VÝSLEDEK = síť_Štos.dostat(síť_úchyt[popisovač_HODNOTA], přenos_data, 1024, 0);
            if (VÝSLEDEK != -11) break;
            if ((Nastavení & 64) != 0 || (otevřít_Nastavení[popisovač_HODNOTA] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[popisovač_HODNOTA] > 0 && mobilní_HODNOTA.밀리초() - Spustit_2 >= 수신대기밀리초[popisovač_HODNOTA]) return -11;
            if (mobilní_HODNOTA.사용자남은밀리초() <= 10) return -11;
            mobilní_HODNOTA.잠시양보();
        }
        if (VÝSLEDEK < 0) return VÝSLEDEK;
        if (VÝSLEDEK > délka_HODNOTA) VÝSLEDEK = délka_HODNOTA;
        for (int INDEX = 0; INDEX < VÝSLEDEK; INDEX++) mobilní_HODNOTA.zápis_Paměť(data_ODKAZ + INDEX, přenos_data[INDEX]);
        if (Adresa != 0) {
            zápis_ODKAZ(Adresa, ODKAZ_délka, síť_Štos.partner_ODKAZ(síť_úchyt[popisovač_HODNOTA]), síť_Štos.partner_číslo_portu(síť_úchyt[popisovač_HODNOTA]));
            spuštění_Správce.zápis_číslo(ODKAZ_délka_ODKAZ, 16);
        }
        return VÝSLEDEK;
    }
    static int 통신주소읽기(int popisovač_položka, int Adresa, int délka_ODKAZ) {
        int popisovač_HODNOTA = účastník_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return popisovač_HODNOTA;
        if (!spuštění_Správce.oříznout(délka_ODKAZ, 4)) return -14;
        int délka_HODNOTA = spuštění_Správce.číslo(délka_ODKAZ);
        if (délka_HODNOTA < 0) return -22;
        if (!spuštění_Správce.oříznout(Adresa, délka_HODNOTA < 16 ? délka_HODNOTA : 16)) return -14;
        int přihrádka_položka = síť_Štos.INDEX(síť_úchyt[popisovač_HODNOTA]);
        zápis_ODKAZ(Adresa, délka_HODNOTA, cílová_úroveň[popisovač_HODNOTA], přihrádka_položka < 0 ? 0 : síť_Štos.접속번호들[přihrádka_položka]);
        spuštění_Správce.zápis_číslo(délka_ODKAZ, 16);
        return 0;
    }
    static int sada_dostat_TIMEOUT(int popisovač_položka, int 밀리초) {
        int popisovač_HODNOTA = účastník_popisovač(popisovač_položka);
        if (popisovač_HODNOTA < 0) return popisovač_HODNOTA;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[popisovač_HODNOTA] = 밀리초;
        return 0;
    }
}
