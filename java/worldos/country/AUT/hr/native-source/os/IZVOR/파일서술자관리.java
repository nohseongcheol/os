// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 korisnik 과정의 파일서술자와 열린 Datoteka 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int 읽기쓰기 = 2, Create_unos = 64, 독점생성 = 128, očistiti_Sadržaj = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] otvoreno_ustroj = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], cilj = new int[서술자한도];
    static int[] Datoteka_položaj = new int[서술자한도], otvoreno_Postavke = new int[서술자한도], Reference_COUNT = new int[서술자한도];
    static int[] mreža_ustroj = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] put_naziv = new int[64], Prijenos_podaci_a0b6d4e1 = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return otvoreno_ustroj[파일서술자] - 1;
    }
    static int 빈서술자(int Pokreni) {
        for (int INDEX = Pokreni; INDEX < 서술자한도; INDEX++) if (otvoreno_ustroj[INDEX] == 0) return INDEX;
        return -24;
    }
    static int 빈기술() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Reference_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Spoji_se(int 서술자, int 기술, int 파일종류, int Datoteka_cilj, int Postavke) {
        otvoreno_ustroj[서술자] = 기술 + 1; 서술자설정[서술자] = (Postavke & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; cilj[기술] = Datoteka_cilj; Reference_COUNT[기술] = 1;
        otvoreno_Postavke[기술] = Postavke & (3 | 이어쓰기 | 기다리지않기); Datoteka_položaj[기술] = 0;
        mreža_ustroj[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_Proces() {
        CLEAN_Proces();
        for (int INDEX = 0; INDEX < 3; INDEX++) Spoji_se(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proces() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (otvoreno_ustroj[INDEX] != 0) Zatvori_Datoteka(INDEX);
    }
    static int Zatvori_Datoteka(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        otvoreno_ustroj[서술자] = 0; 서술자설정[서술자] = 0;
        Reference_COUNT[기술]--;
        if (Reference_COUNT[기술] == 0) {
            if (종류[기술] == 2) Memorija_datotečni_sustav.otvoreno_COUNT[cilj[기술]]--;
            if (종류[기술] == 3 && mreža_ustroj[기술] != 0) mreža_hrpa.Zatvori(mreža_ustroj[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bajt_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int adresa) {
        if (!실행관리.isječak(adresa, 1)) return -14;
        int Položaj = uređaj_VALUE.기억읽기(adresa) == '/' ? 1 : 0;
        for (int 길이 = 0; 길이 < 64; 길이++) {
            if (!실행관리.isječak(adresa + Položaj + 길이, 1)) return -14;
            int VALUE = uređaj_VALUE.기억읽기(adresa + Položaj + 길이);
            put_naziv[길이] = VALUE;
            if (VALUE == 0) return 길이 == 0 ? -2 : (Memorija_datotečni_sustav.이름검사(put_naziv, 길이) ? 길이 : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int otvoreno_Datoteka(int naziv_adresa, int Postavke, int 허가) {
        int 길이 = 경로읽기(naziv_adresa);
        if (길이 < 0) return 길이;
        if ((Postavke & ~(3 | Create_unos | 독점생성 | očistiti_Sadržaj | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Postavke & 3) == 3 || ((Postavke & očistiti_Sadržaj) != 0 && (Postavke & 3) == 0)) return -22;
        int Datoteka = Memorija_datotečni_sustav.FIND_unos(put_naziv, 길이);
        if (Datoteka >= 0 && (Postavke & (Create_unos | 독점생성)) == (Create_unos | 독점생성)) return -17;
        if (Datoteka == -2 && (Postavke & Create_unos) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Datoteka == -2) {
            int REZULTAT = Memorija_datotečni_sustav.Store_VALUE(put_naziv, 길이, put_naziv, 0);
            if (REZULTAT < 0) return REZULTAT;
            Datoteka = Memorija_datotečni_sustav.FIND_unos(put_naziv, 길이);
            Memorija_datotečni_sustav.허가들[Datoteka] = 허가 & 511;
        }
        if (Datoteka < 0) return Datoteka;
        if ((Postavke & očistiti_Sadržaj) != 0) Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka] = 0;
        Memorija_datotečni_sustav.otvoreno_COUNT[Datoteka]++;
        return Spoji_se(서술자, 기술, 2, Datoteka, Postavke);
    }
    static int 파일읽기(int 서술자, int podaci_adresa, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (otvoreno_Postavke[기술] & 3) == 1) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.isječak(podaci_adresa, 길이)) return -14;
        if (종류[기술] == 3) return primiti_datogram_podaci(서술자, podaci_adresa, 길이, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < 길이) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = tipkovnica.Čitaj();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((otvoreno_Postavke[기술] & 기다리지않기) != 0) return -11;
                    if (uređaj_VALUE.사용자남은밀리초() <= 10) return -11;
                    mreža_hrpa.provjeriti(); uređaj_VALUE.잠시양보();
                } else {
                    uređaj_VALUE.zapisivanje_Memorija(podaci_adresa + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Datoteka = cilj[기술], Položaj = Datoteka_položaj[기술];
        if (Položaj >= Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka]) return 0;
        if (길이 > Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka] - Položaj) 길이 = Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka] - Položaj;
        int 원본주소 = uređaj_VALUE.Datoteka_Memorija() + Datoteka * Memorija_datotečni_sustav.최대크기 + Položaj;
        for (int INDEX = 0; INDEX < 길이; INDEX++) uređaj_VALUE.zapisivanje_Memorija(podaci_adresa + INDEX, uređaj_VALUE.기억읽기(원본주소 + INDEX));
        Datoteka_položaj[기술] += 길이;
        return 길이;
    }
    static int zapisivanje_Datoteka(int 서술자, int podaci_adresa, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (otvoreno_Postavke[기술] & 3) == 0) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.isječak(podaci_adresa, 길이)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 odredište_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (길이 > 16384) 길이 = 16384;
            for (int INDEX = 0; INDEX < 길이; INDEX++) {
                int VALUE = uređaj_VALUE.기억읽기(podaci_adresa + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return 길이;
        }
        int Datoteka = cilj[기술], Veličina = Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka];
        int Položaj = (otvoreno_Postavke[기술] & 이어쓰기) != 0 ? Veličina : Datoteka_položaj[기술];
        if (Položaj >= Memorija_datotečni_sustav.최대크기) return -27;
        if (길이 > Memorija_datotečni_sustav.최대크기 - Položaj) 길이 = Memorija_datotečni_sustav.최대크기 - Položaj;
        int odredište_adresa = uređaj_VALUE.Datoteka_Memorija() + Datoteka * Memorija_datotečni_sustav.최대크기;
        for (int INDEX = Veličina; INDEX < Položaj; INDEX++) uređaj_VALUE.zapisivanje_Memorija(odredište_adresa + INDEX, 0);
        for (int INDEX = 0; INDEX < 길이; INDEX++) uređaj_VALUE.zapisivanje_Memorija(odredište_adresa + Položaj + INDEX, uređaj_VALUE.기억읽기(podaci_adresa + INDEX));
        Datoteka_položaj[기술] = Položaj + 길이;
        if (Položaj + 길이 > Veličina) Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka] = Položaj + 길이;
        return 길이;
    }
    static int tražiti_Datoteka(int 서술자, int pomak_VALUE, int akcija_korijen) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (akcija_korijen < 0 || akcija_korijen > 2) return -22;
        int podloga_VALUE = akcija_korijen == 0 ? 0 : (akcija_korijen == 1 ? Datoteka_položaj[기술] : Memorija_datotečni_sustav.promijeniti_veličinu_Popis[cilj[기술]]);
        if (pomak_VALUE > 0 && podloga_VALUE > 2147483647 - pomak_VALUE) return -75;
        if (pomak_VALUE < 0 && pomak_VALUE < -podloga_VALUE) return -22;
        Datoteka_položaj[기술] = podloga_VALUE + pomak_VALUE;
        return Datoteka_položaj[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Dodijeli_VALUE, int Postavke) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Dodijeli_VALUE ? -9 : -22;
        if (Dodijeli_VALUE && 서술자 == 새서술자) return 새서술자;
        if (Dodijeli_VALUE) { if (otvoreno_ustroj[새서술자] != 0) Zatvori_Datoteka(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        otvoreno_ustroj[새서술자] = 기술 + 1; 서술자설정[새서술자] = Postavke; Reference_COUNT[기술]++;
        return 새서술자;
    }
    static int ukloniti_Datoteka_unos_naziv(int naziv_adresa) {
        int 길이 = 경로읽기(naziv_adresa);
        if (길이 < 0) return 길이;
        int Datoteka = Memorija_datotečni_sustav.FIND_unos(put_naziv, 길이);
        if (Datoteka < 0) return Datoteka;
        Memorija_datotečni_sustav.이름들[Datoteka * 64] = 0;
        return 0;
    }
    static int 파일길이정하기(int 서술자, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (otvoreno_Postavke[기술] & 3) == 0 || 길이 < 0) return -22;
        if (길이 > Memorija_datotečni_sustav.최대크기) return -27;
        int Datoteka = cilj[기술], adresa = uređaj_VALUE.Datoteka_Memorija() + Datoteka * Memorija_datotečni_sustav.최대크기;
        for (int INDEX = Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka]; INDEX < 길이; INDEX++) uređaj_VALUE.zapisivanje_Memorija(adresa + INDEX, 0);
        Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka] = 길이;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int adresa) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.isječak(adresa, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(adresa + INDEX * 4, 0);
        int Datoteka = cilj[기술], Veličina = 종류[기술] == 2 ? Memorija_datotečni_sustav.promijeniti_veličinu_Popis[Datoteka] : 0;
        int 허가 = 종류[기술] == 2 ? Memorija_datotečni_sustav.허가들[Datoteka] : 438;
        실행관리.수쓰기(adresa, 1);
        실행관리.수쓰기(adresa + 4, 종류[기술] == 2 ? Datoteka + 1 : 100 + 기술);
        실행관리.수쓰기(adresa + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(adresa + 12, 종류[기술] == 2 && Memorija_datotečni_sustav.이름들[Datoteka * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(adresa + 28, Veličina); 실행관리.수쓰기(adresa + 32, 512);
        실행관리.수쓰기(adresa + 36, (Veličina + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Naredba, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Naredba == 0 || Naredba == 1030) return 서술자복제(서술자, VALUE, false, Naredba == 1030 ? 1 : 0);
        if (Naredba == 1) return 서술자설정[서술자];
        if (Naredba == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Naredba == 3) return otvoreno_Postavke[기술];
        if (Naredba == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            otvoreno_Postavke[기술] = (otvoreno_Postavke[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Create_sudionik(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Spoji_se(서술자, 기술, 3, 0, 읽기쓰기);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int adresa_32(int adresa) {
        return uređaj_VALUE.기억읽기(adresa) << 24 | uređaj_VALUE.기억읽기(adresa + 1) << 16
            | uređaj_VALUE.기억읽기(adresa + 2) << 8 | uređaj_VALUE.기억읽기(adresa + 3);
    }
    static int 주소검사(int adresa, int 길이) {
        if (길이 < 16) return -22;
        if (!실행관리.isječak(adresa, 16)) return -14;
        return 실행관리.짧은수(adresa) == 2 ? 0 : -97;
    }
    static int BIND_adresa(int 서술자, int adresa, int 길이) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int REZULTAT = 주소검사(adresa, 길이);
        if (REZULTAT < 0) return REZULTAT;
        if (mreža_ustroj[기술] != 0) return -22;
        int mrežni_ID = adresa_32(adresa + 4);
        if (mrežni_ID != 0 && mrežni_ID != mreža_hrpa.내주소) return -99;
        int broj_priključka = uređaj_VALUE.기억읽기(adresa + 2) << 8 | uređaj_VALUE.기억읽기(adresa + 3);
        REZULTAT = mreža_hrpa.Otvori(broj_priključka);
        if (REZULTAT < 0) return REZULTAT;
        mreža_ustroj[기술] = REZULTAT; cilj[기술] = mrežni_ID;
        return 0;
    }
    static int Automatski_način_rada_BIND(int 기술) {
        if (mreža_ustroj[기술] != 0) return 0;
        int REZULTAT = mreža_hrpa.Otvori(0);
        if (REZULTAT < 0) return REZULTAT;
        mreža_ustroj[기술] = REZULTAT;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 zahtjev 구조체로 전달한다.
    static int slati_datogram_podaci(int 서술자, int podaci_adresa, int 길이, int Postavke, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Postavke != 0) return -95;
        if (길이 < 0 || 길이 > 1024) return -90;
        if (길이 != 0 && !실행관리.isječak(podaci_adresa, 길이)) return -14;
        if (!실행관리.isječak(요청주소, 8)) return -14;
        int adresa = 실행관리.수(요청주소);
        int REZULTAT = 주소검사(adresa, 실행관리.수(요청주소 + 4));
        if (REZULTAT < 0) return REZULTAT;
        int broj_priključka = uređaj_VALUE.기억읽기(adresa + 2) << 8 | uređaj_VALUE.기억읽기(adresa + 3);
        if (broj_priključka == 0) return -22;
        REZULTAT = Automatski_način_rada_BIND(기술);
        if (REZULTAT < 0) return REZULTAT;
        for (int INDEX = 0; INDEX < 길이; INDEX++) Prijenos_podaci_a0b6d4e1[INDEX] = uređaj_VALUE.기억읽기(podaci_adresa + INDEX);
        return mreža_hrpa.slati(mreža_ustroj[기술], adresa_32(adresa + 4), broj_priključka, Prijenos_podaci_a0b6d4e1, 길이);
    }
    static void zapisivanje_adresa(int adresa, int 길이, int mrežni_ID, int broj_priključka) {
        for (int INDEX = 0; INDEX < 길이 && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = broj_priključka >>> 8;
            if (INDEX == 3) VALUE = broj_priključka;
            if (INDEX >= 4 && INDEX < 8) VALUE = mrežni_ID >>> (56 - INDEX * 8);
            uređaj_VALUE.zapisivanje_Memorija(adresa + INDEX, VALUE & 255);
        }
    }
    static int primiti_datogram_podaci(int 서술자, int podaci_adresa, int 길이, int Postavke, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Postavke & ~64) != 0) return -95;
        if (길이 < 0) return -22;
        if (길이 != 0 && !실행관리.isječak(podaci_adresa, 길이)) return -14;
        int adresa = 0, 주소길이주소 = 0, 주소길이 = 0;
        if (요청주소 != 0) {
            if (!실행관리.isječak(요청주소, 8)) return -14;
            adresa = 실행관리.수(요청주소); 주소길이주소 = 실행관리.수(요청주소 + 4);
            if (adresa != 0) {
                if (!실행관리.isječak(주소길이주소, 4)) return -14;
                주소길이 = 실행관리.수(주소길이주소);
                if (주소길이 < 0) return -22;
                if (!실행관리.isječak(adresa, 주소길이 < 16 ? 주소길이 : 16)) return -14;
            }
        }
        int REZULTAT = Automatski_način_rada_BIND(기술);
        if (REZULTAT < 0) return REZULTAT;
        int Pokreni = uređaj_VALUE.밀리초();
        while (true) {
            REZULTAT = mreža_hrpa.primiti(mreža_ustroj[기술], Prijenos_podaci_a0b6d4e1, 1024, 0);
            if (REZULTAT != -11) break;
            if ((Postavke & 64) != 0 || (otvoreno_Postavke[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && uređaj_VALUE.밀리초() - Pokreni >= 수신대기밀리초[기술]) return -11;
            if (uređaj_VALUE.사용자남은밀리초() <= 10) return -11;
            uređaj_VALUE.잠시양보();
        }
        if (REZULTAT < 0) return REZULTAT;
        if (REZULTAT > 길이) REZULTAT = 길이;
        for (int INDEX = 0; INDEX < REZULTAT; INDEX++) uređaj_VALUE.zapisivanje_Memorija(podaci_adresa + INDEX, Prijenos_podaci_a0b6d4e1[INDEX]);
        if (adresa != 0) {
            zapisivanje_adresa(adresa, 주소길이, mreža_hrpa.ravnopravan_član_adresa(mreža_ustroj[기술]), mreža_hrpa.ravnopravan_član_broj_priključka(mreža_ustroj[기술]));
            실행관리.수쓰기(주소길이주소, 16);
        }
        return REZULTAT;
    }
    static int 통신주소읽기(int 서술자, int adresa, int 길이주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.isječak(길이주소, 4)) return -14;
        int 길이 = 실행관리.수(길이주소);
        if (길이 < 0) return -22;
        if (!실행관리.isječak(adresa, 길이 < 16 ? 길이 : 16)) return -14;
        int 칸 = mreža_hrpa.INDEX(mreža_ustroj[기술]);
        zapisivanje_adresa(adresa, 길이, cilj[기술], 칸 < 0 ? 0 : mreža_hrpa.접속번호들[칸]);
        실행관리.수쓰기(길이주소, 16);
        return 0;
    }
    static int skup_primiti_TIMEOUT(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
