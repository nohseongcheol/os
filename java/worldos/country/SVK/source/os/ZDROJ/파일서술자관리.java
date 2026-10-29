// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 používateľ 과정의 파일서술자와 열린 Súbor 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int na_čítanie_a_zapisovanie_príznak = 2, Create_položka = 64, 독점생성 = 128, vymazať_Obsah = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] otvoriť_rukoväť = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], cieľová_hodnota = new int[서술자한도];
    static int[] Súbor_pozícia = new int[서술자한도], otvoriť_Nastavenia = new int[서술자한도], zdroj_COUNT = new int[서술자한도];
    static int[] sieť_rukoväť = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] cesta_názov = new int[64], prenos_údaje = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return otvoriť_rukoväť[파일서술자] - 1;
    }
    static int 빈서술자(int Spustiť_2) {
        for (int INDEX = Spustiť_2; INDEX < 서술자한도; INDEX++) if (otvoriť_rukoväť[INDEX] == 0) return INDEX;
        return -24;
    }
    static int prázdny_rukoväť() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (zdroj_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Pripojiť(int 서술자, int 기술, int 파일종류, int Súbor_cieľová_hodnota, int Nastavenia) {
        otvoriť_rukoväť[서술자] = 기술 + 1; 서술자설정[서술자] = (Nastavenia & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; cieľová_hodnota[기술] = Súbor_cieľová_hodnota; zdroj_COUNT[기술] = 1;
        otvoriť_Nastavenia[기술] = Nastavenia & (3 | 이어쓰기 | 기다리지않기); Súbor_pozícia[기술] = 0;
        sieť_rukoväť[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_Proces() {
        CLEAN_Proces();
        for (int INDEX = 0; INDEX < 3; INDEX++) Pripojiť(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proces() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (otvoriť_rukoväť[INDEX] != 0) Zavrieť_Súbor(INDEX);
    }
    static int Zavrieť_Súbor(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        otvoriť_rukoväť[서술자] = 0; 서술자설정[서술자] = 0;
        zdroj_COUNT[기술]--;
        if (zdroj_COUNT[기술] == 0) {
            if (종류[기술] == 2) Pamäť_systém_súborov.otvoriť_COUNT[cieľová_hodnota[기술]]--;
            if (종류[기술] == 3 && sieť_rukoväť[기술] != 0) sieť_Vrstvy.Zatvoriť(sieť_rukoväť[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 Byte_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int adresa) {
        if (!실행관리.klip(adresa, 1)) return -14;
        int Pozícia = telefón_VALUE.기억읽기(adresa) == '/' ? 1 : 0;
        for (int dĺžka_VALUE = 0; dĺžka_VALUE < 64; dĺžka_VALUE++) {
            if (!실행관리.klip(adresa + Pozícia + dĺžka_VALUE, 1)) return -14;
            int VALUE = telefón_VALUE.기억읽기(adresa + Pozícia + dĺžka_VALUE);
            cesta_názov[dĺžka_VALUE] = VALUE;
            if (VALUE == 0) return dĺžka_VALUE == 0 ? -2 : (Pamäť_systém_súborov.skontrolovať_názov(cesta_názov, dĺžka_VALUE) ? dĺžka_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int otvoriť_Súbor(int názov_adresa, int Nastavenia, int 허가) {
        int dĺžka_VALUE = 경로읽기(názov_adresa);
        if (dĺžka_VALUE < 0) return dĺžka_VALUE;
        if ((Nastavenia & ~(3 | Create_položka | 독점생성 | vymazať_Obsah | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Nastavenia & 3) == 3 || ((Nastavenia & vymazať_Obsah) != 0 && (Nastavenia & 3) == 0)) return -22;
        int Súbor = Pamäť_systém_súborov.FIND_položka(cesta_názov, dĺžka_VALUE);
        if (Súbor >= 0 && (Nastavenia & (Create_položka | 독점생성)) == (Create_položka | 독점생성)) return -17;
        if (Súbor == -2 && (Nastavenia & Create_položka) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = prázdny_rukoväť();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Súbor == -2) {
            int KR = Pamäť_systém_súborov.Store_VALUE(cesta_názov, dĺžka_VALUE, cesta_názov, 0);
            if (KR < 0) return KR;
            Súbor = Pamäť_systém_súborov.FIND_položka(cesta_názov, dĺžka_VALUE);
            Pamäť_systém_súborov.허가들[Súbor] = 허가 & 511;
        }
        if (Súbor < 0) return Súbor;
        if ((Nastavenia & vymazať_Obsah) != 0) Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor] = 0;
        Pamäť_systém_súborov.otvoriť_COUNT[Súbor]++;
        return Pripojiť(서술자, 기술, 2, Súbor, Nastavenia);
    }
    static int 파일읽기(int 서술자, int údaje_adresa, int dĺžka_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (otvoriť_Nastavenia[기술] & 3) == 1) return -9;
        if (dĺžka_VALUE < 0) return -22;
        if (dĺžka_VALUE == 0) return 0;
        if (!실행관리.klip(údaje_adresa, dĺžka_VALUE)) return -14;
        if (종류[기술] == 3) return dostať_datagram_údaje(서술자, údaje_adresa, dĺžka_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < dĺžka_VALUE) {
                int VALUE = SMS_Terminál.직렬읽기();
                if (VALUE < 0) VALUE = klávesnica.Čítanie();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((otvoriť_Nastavenia[기술] & 기다리지않기) != 0) return -11;
                    if (telefón_VALUE.사용자남은밀리초() <= 10) return -11;
                    sieť_Vrstvy.overiť(); telefón_VALUE.잠시양보();
                } else {
                    telefón_VALUE.zapísať_Pamäť(údaje_adresa + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Súbor = cieľová_hodnota[기술], Pozícia = Súbor_pozícia[기술];
        if (Pozícia >= Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor]) return 0;
        if (dĺžka_VALUE > Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor] - Pozícia) dĺžka_VALUE = Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor] - Pozícia;
        int 원본주소 = telefón_VALUE.Súbor_Pamäť() + Súbor * Pamäť_systém_súborov.최대크기 + Pozícia;
        for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) telefón_VALUE.zapísať_Pamäť(údaje_adresa + INDEX, telefón_VALUE.기억읽기(원본주소 + INDEX));
        Súbor_pozícia[기술] += dĺžka_VALUE;
        return dĺžka_VALUE;
    }
    static int zapísať_Súbor(int 서술자, int údaje_adresa, int dĺžka_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (otvoriť_Nastavenia[기술] & 3) == 0) return -9;
        if (dĺžka_VALUE < 0) return -22;
        if (dĺžka_VALUE == 0) return 0;
        if (!실행관리.klip(údaje_adresa, dĺžka_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 cieľ_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (dĺžka_VALUE > 16384) dĺžka_VALUE = 16384;
            for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) {
                int VALUE = telefón_VALUE.기억읽기(údaje_adresa + INDEX);
                SMS_Terminál.직렬바이트(VALUE); SMS_Terminál.화면문자(VALUE);
            }
            return dĺžka_VALUE;
        }
        int Súbor = cieľová_hodnota[기술], Veľkosť = Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor];
        int Pozícia = (otvoriť_Nastavenia[기술] & 이어쓰기) != 0 ? Veľkosť : Súbor_pozícia[기술];
        if (Pozícia >= Pamäť_systém_súborov.최대크기) return -27;
        if (dĺžka_VALUE > Pamäť_systém_súborov.최대크기 - Pozícia) dĺžka_VALUE = Pamäť_systém_súborov.최대크기 - Pozícia;
        int cieľ_adresa_08bbd577 = telefón_VALUE.Súbor_Pamäť() + Súbor * Pamäť_systém_súborov.최대크기;
        for (int INDEX = Veľkosť; INDEX < Pozícia; INDEX++) telefón_VALUE.zapísať_Pamäť(cieľ_adresa_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) telefón_VALUE.zapísať_Pamäť(cieľ_adresa_08bbd577 + Pozícia + INDEX, telefón_VALUE.기억읽기(údaje_adresa + INDEX));
        Súbor_pozícia[기술] = Pozícia + dĺžka_VALUE;
        if (Pozícia + dĺžka_VALUE > Veľkosť) Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor] = Pozícia + dĺžka_VALUE;
        return dĺžka_VALUE;
    }
    static int hľadať_Súbor(int 서술자, int Posun_VALUE, int akcia_koreň) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (akcia_koreň < 0 || akcia_koreň > 2) return -22;
        int tapeta_VALUE = akcia_koreň == 0 ? 0 : (akcia_koreň == 1 ? Súbor_pozícia[기술] : Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[cieľová_hodnota[기술]]);
        if (Posun_VALUE > 0 && tapeta_VALUE > 2147483647 - Posun_VALUE) return -75;
        if (Posun_VALUE < 0 && Posun_VALUE < -tapeta_VALUE) return -22;
        Súbor_pozícia[기술] = tapeta_VALUE + Posun_VALUE;
        return Súbor_pozícia[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Priradiť_VALUE, int Nastavenia) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Priradiť_VALUE ? -9 : -22;
        if (Priradiť_VALUE && 서술자 == 새서술자) return 새서술자;
        if (Priradiť_VALUE) { if (otvoriť_rukoväť[새서술자] != 0) Zavrieť_Súbor(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        otvoriť_rukoväť[새서술자] = 기술 + 1; 서술자설정[새서술자] = Nastavenia; zdroj_COUNT[기술]++;
        return 새서술자;
    }
    static int odobrať_Súbor_položka_názov(int názov_adresa) {
        int dĺžka_VALUE = 경로읽기(názov_adresa);
        if (dĺžka_VALUE < 0) return dĺžka_VALUE;
        int Súbor = Pamäť_systém_súborov.FIND_položka(cesta_názov, dĺžka_VALUE);
        if (Súbor < 0) return Súbor;
        Pamäť_systém_súborov.이름들[Súbor * 64] = 0;
        return 0;
    }
    static int množina_Súbor_dĺžka(int 서술자, int dĺžka_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (otvoriť_Nastavenia[기술] & 3) == 0 || dĺžka_VALUE < 0) return -22;
        if (dĺžka_VALUE > Pamäť_systém_súborov.최대크기) return -27;
        int Súbor = cieľová_hodnota[기술], adresa = telefón_VALUE.Súbor_Pamäť() + Súbor * Pamäť_systém_súborov.최대크기;
        for (int INDEX = Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor]; INDEX < dĺžka_VALUE; INDEX++) telefón_VALUE.zapísať_Pamäť(adresa + INDEX, 0);
        Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor] = dĺžka_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int adresa) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klip(adresa, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(adresa + INDEX * 4, 0);
        int Súbor = cieľová_hodnota[기술], Veľkosť = 종류[기술] == 2 ? Pamäť_systém_súborov.zmeniť_veľkosť_Zoznam[Súbor] : 0;
        int 허가 = 종류[기술] == 2 ? Pamäť_systém_súborov.허가들[Súbor] : 438;
        실행관리.수쓰기(adresa, 1);
        실행관리.수쓰기(adresa + 4, 종류[기술] == 2 ? Súbor + 1 : 100 + 기술);
        실행관리.수쓰기(adresa + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(adresa + 12, 종류[기술] == 2 && Pamäť_systém_súborov.이름들[Súbor * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(adresa + 28, Veľkosť); 실행관리.수쓰기(adresa + 32, 512);
        실행관리.수쓰기(adresa + 36, (Veľkosť + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Príkaz, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Príkaz == 0 || Príkaz == 1030) return 서술자복제(서술자, VALUE, false, Príkaz == 1030 ? 1 : 0);
        if (Príkaz == 1) return 서술자설정[서술자];
        if (Príkaz == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Príkaz == 3) return otvoriť_Nastavenia[기술];
        if (Príkaz == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            otvoriť_Nastavenia[기술] = (otvoriť_Nastavenia[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Create_účastník(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = prázdny_rukoväť();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Pripojiť(서술자, 기술, 3, 0, na_čítanie_a_zapisovanie_príznak);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int adresa_32(int adresa) {
        return telefón_VALUE.기억읽기(adresa) << 24 | telefón_VALUE.기억읽기(adresa + 1) << 16
            | telefón_VALUE.기억읽기(adresa + 2) << 8 | telefón_VALUE.기억읽기(adresa + 3);
    }
    static int skontrolovať_adresa(int adresa, int dĺžka_VALUE) {
        if (dĺžka_VALUE < 16) return -22;
        if (!실행관리.klip(adresa, 16)) return -14;
        return 실행관리.짧은수(adresa) == 2 ? 0 : -97;
    }
    static int BIND_adresa(int 서술자, int adresa, int dĺžka_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int KR = skontrolovať_adresa(adresa, dĺžka_VALUE);
        if (KR < 0) return KR;
        if (sieť_rukoväť[기술] != 0) return -22;
        int sieťová_identifikácia = adresa_32(adresa + 4);
        if (sieťová_identifikácia != 0 && sieťová_identifikácia != sieť_Vrstvy.내주소) return -99;
        int číslo_portu = telefón_VALUE.기억읽기(adresa + 2) << 8 | telefón_VALUE.기억읽기(adresa + 3);
        KR = sieť_Vrstvy.Otvoriť(číslo_portu);
        if (KR < 0) return KR;
        sieť_rukoväť[기술] = KR; cieľová_hodnota[기술] = sieťová_identifikácia;
        return 0;
    }
    static int Auto_BIND(int 기술) {
        if (sieť_rukoväť[기술] != 0) return 0;
        int KR = sieť_Vrstvy.Otvoriť(0);
        if (KR < 0) return KR;
        sieť_rukoväť[기술] = KR;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 požiadavka 구조체로 전달한다.
    static int odoslať_datagram_údaje(int 서술자, int údaje_adresa, int dĺžka_VALUE, int Nastavenia, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Nastavenia != 0) return -95;
        if (dĺžka_VALUE < 0 || dĺžka_VALUE > 1024) return -90;
        if (dĺžka_VALUE != 0 && !실행관리.klip(údaje_adresa, dĺžka_VALUE)) return -14;
        if (!실행관리.klip(요청주소, 8)) return -14;
        int adresa = 실행관리.수(요청주소);
        int KR = skontrolovať_adresa(adresa, 실행관리.수(요청주소 + 4));
        if (KR < 0) return KR;
        int číslo_portu = telefón_VALUE.기억읽기(adresa + 2) << 8 | telefón_VALUE.기억읽기(adresa + 3);
        if (číslo_portu == 0) return -22;
        KR = Auto_BIND(기술);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) prenos_údaje[INDEX] = telefón_VALUE.기억읽기(údaje_adresa + INDEX);
        return sieť_Vrstvy.odoslať(sieť_rukoväť[기술], adresa_32(adresa + 4), číslo_portu, prenos_údaje, dĺžka_VALUE);
    }
    static void zapísať_adresa(int adresa, int dĺžka_VALUE, int sieťová_identifikácia, int číslo_portu) {
        for (int INDEX = 0; INDEX < dĺžka_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = číslo_portu >>> 8;
            if (INDEX == 3) VALUE = číslo_portu;
            if (INDEX >= 4 && INDEX < 8) VALUE = sieťová_identifikácia >>> (56 - INDEX * 8);
            telefón_VALUE.zapísať_Pamäť(adresa + INDEX, VALUE & 255);
        }
    }
    static int dostať_datagram_údaje(int 서술자, int údaje_adresa, int dĺžka_VALUE, int Nastavenia, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Nastavenia & ~64) != 0) return -95;
        if (dĺžka_VALUE < 0) return -22;
        if (dĺžka_VALUE != 0 && !실행관리.klip(údaje_adresa, dĺžka_VALUE)) return -14;
        int adresa = 0, adresa_dĺžka_adresa = 0, adresa_dĺžka = 0;
        if (요청주소 != 0) {
            if (!실행관리.klip(요청주소, 8)) return -14;
            adresa = 실행관리.수(요청주소); adresa_dĺžka_adresa = 실행관리.수(요청주소 + 4);
            if (adresa != 0) {
                if (!실행관리.klip(adresa_dĺžka_adresa, 4)) return -14;
                adresa_dĺžka = 실행관리.수(adresa_dĺžka_adresa);
                if (adresa_dĺžka < 0) return -22;
                if (!실행관리.klip(adresa, adresa_dĺžka < 16 ? adresa_dĺžka : 16)) return -14;
            }
        }
        int KR = Auto_BIND(기술);
        if (KR < 0) return KR;
        int Spustiť_2 = telefón_VALUE.밀리초();
        while (true) {
            KR = sieť_Vrstvy.dostať(sieť_rukoväť[기술], prenos_údaje, 1024, 0);
            if (KR != -11) break;
            if ((Nastavenia & 64) != 0 || (otvoriť_Nastavenia[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && telefón_VALUE.밀리초() - Spustiť_2 >= 수신대기밀리초[기술]) return -11;
            if (telefón_VALUE.사용자남은밀리초() <= 10) return -11;
            telefón_VALUE.잠시양보();
        }
        if (KR < 0) return KR;
        if (KR > dĺžka_VALUE) KR = dĺžka_VALUE;
        for (int INDEX = 0; INDEX < KR; INDEX++) telefón_VALUE.zapísať_Pamäť(údaje_adresa + INDEX, prenos_údaje[INDEX]);
        if (adresa != 0) {
            zapísať_adresa(adresa, adresa_dĺžka, sieť_Vrstvy.partnerský_uzol_adresa(sieť_rukoväť[기술]), sieť_Vrstvy.partnerský_uzol_číslo_portu(sieť_rukoväť[기술]));
            실행관리.수쓰기(adresa_dĺžka_adresa, 16);
        }
        return KR;
    }
    static int 통신주소읽기(int 서술자, int adresa, int dĺžka_adresa) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klip(dĺžka_adresa, 4)) return -14;
        int dĺžka_VALUE = 실행관리.수(dĺžka_adresa);
        if (dĺžka_VALUE < 0) return -22;
        if (!실행관리.klip(adresa, dĺžka_VALUE < 16 ? dĺžka_VALUE : 16)) return -14;
        int 칸 = sieť_Vrstvy.INDEX(sieť_rukoväť[기술]);
        zapísať_adresa(adresa, dĺžka_VALUE, cieľová_hodnota[기술], 칸 < 0 ? 0 : sieť_Vrstvy.접속번호들[칸]);
        실행관리.수쓰기(dĺžka_adresa, 16);
        return 0;
    }
    static int množina_dostať_TIMEOUT(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
