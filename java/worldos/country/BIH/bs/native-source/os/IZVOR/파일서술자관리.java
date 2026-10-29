// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 korisnik 과정의 파일서술자와 열린 Fajl 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int i_za_čitanje_i_za_pisanje_zastavica = 2, Create_unos = 64, 독점생성 = 128, obrisati_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] kreirati_hvatište = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], cilj = new int[서술자한도];
    static int[] fajl_položaj = new int[서술자한도], kreirati_Postavke = new int[서술자한도], Reference_COUNT = new int[서술자한도];
    static int[] Mreža_hvatište = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] put_naziv = new int[64], prijenos_podaci = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return kreirati_hvatište[파일서술자] - 1;
    }
    static int 빈서술자(int Pokreni) {
        for (int INDEX = Pokreni; INDEX < 서술자한도; INDEX++) if (kreirati_hvatište[INDEX] == 0) return INDEX;
        return -24;
    }
    static int prazno_hvatište() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Reference_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Spoji_se(int 서술자, int 기술, int 파일종류, int fajl_cilj, int Postavke) {
        kreirati_hvatište[서술자] = 기술 + 1; 서술자설정[서술자] = (Postavke & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; cilj[기술] = fajl_cilj; Reference_COUNT[기술] = 1;
        kreirati_Postavke[기술] = Postavke & (3 | 이어쓰기 | 기다리지않기); fajl_položaj[기술] = 0;
        Mreža_hvatište[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_proces() {
        CLEAN_proces();
        for (int INDEX = 0; INDEX < 3; INDEX++) Spoji_se(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_proces() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (kreirati_hvatište[INDEX] != 0) zatvoriti_fajl(INDEX);
    }
    static int zatvoriti_fajl(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        kreirati_hvatište[서술자] = 0; 서술자설정[서술자] = 0;
        Reference_COUNT[기술]--;
        if (Reference_COUNT[기술] == 0) {
            if (종류[기술] == 2) Memorija_fajl_sistem.kreirati_COUNT[cilj[기술]]--;
            if (종류[기술] == 3 && Mreža_hvatište[기술] != 0) Mreža_snop.Zatvori(Mreža_hvatište[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bajt_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int adresa) {
        if (!실행관리.isječak(adresa, 1)) return -14;
        int Pozicija = uređaj_VALUE.기억읽기(adresa) == '/' ? 1 : 0;
        for (int dužina_VALUE = 0; dužina_VALUE < 64; dužina_VALUE++) {
            if (!실행관리.isječak(adresa + Pozicija + dužina_VALUE, 1)) return -14;
            int VALUE = uređaj_VALUE.기억읽기(adresa + Pozicija + dužina_VALUE);
            put_naziv[dužina_VALUE] = VALUE;
            if (VALUE == 0) return dužina_VALUE == 0 ? -2 : (Memorija_fajl_sistem.ček_naziv(put_naziv, dužina_VALUE) ? dužina_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int kreirati_fajl(int naziv_adresa, int Postavke, int 허가) {
        int dužina_VALUE = 경로읽기(naziv_adresa);
        if (dužina_VALUE < 0) return dužina_VALUE;
        if ((Postavke & ~(3 | Create_unos | 독점생성 | obrisati_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Postavke & 3) == 3 || ((Postavke & obrisati_TOC) != 0 && (Postavke & 3) == 0)) return -22;
        int Fajl = Memorija_fajl_sistem.FIND_unos(put_naziv, dužina_VALUE);
        if (Fajl >= 0 && (Postavke & (Create_unos | 독점생성)) == (Create_unos | 독점생성)) return -17;
        if (Fajl == -2 && (Postavke & Create_unos) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = prazno_hvatište();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fajl == -2) {
            int mjera = Memorija_fajl_sistem.Store_VALUE(put_naziv, dužina_VALUE, put_naziv, 0);
            if (mjera < 0) return mjera;
            Fajl = Memorija_fajl_sistem.FIND_unos(put_naziv, dužina_VALUE);
            Memorija_fajl_sistem.허가들[Fajl] = 허가 & 511;
        }
        if (Fajl < 0) return Fajl;
        if ((Postavke & obrisati_TOC) != 0) Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl] = 0;
        Memorija_fajl_sistem.kreirati_COUNT[Fajl]++;
        return Spoji_se(서술자, 기술, 2, Fajl, Postavke);
    }
    static int 파일읽기(int 서술자, int podaci_adresa, int dužina_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (kreirati_Postavke[기술] & 3) == 1) return -9;
        if (dužina_VALUE < 0) return -22;
        if (dužina_VALUE == 0) return 0;
        if (!실행관리.isječak(podaci_adresa, dužina_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, podaci_adresa, dužina_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < dužina_VALUE) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = tastatura.Čitaj();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((kreirati_Postavke[기술] & 기다리지않기) != 0) return -11;
                    if (uređaj_VALUE.사용자남은밀리초() <= 10) return -11;
                    Mreža_snop.potvrditi(); uređaj_VALUE.잠시양보();
                } else {
                    uređaj_VALUE.pisati_Memorija(podaci_adresa + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Fajl = cilj[기술], Pozicija = fajl_položaj[기술];
        if (Pozicija >= Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl]) return 0;
        if (dužina_VALUE > Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl] - Pozicija) dužina_VALUE = Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl] - Pozicija;
        int 원본주소 = uređaj_VALUE.fajl_Memorija() + Fajl * Memorija_fajl_sistem.최대크기 + Pozicija;
        for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) uređaj_VALUE.pisati_Memorija(podaci_adresa + INDEX, uređaj_VALUE.기억읽기(원본주소 + INDEX));
        fajl_položaj[기술] += dužina_VALUE;
        return dužina_VALUE;
    }
    static int pisati_fajl(int 서술자, int podaci_adresa, int dužina_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (kreirati_Postavke[기술] & 3) == 0) return -9;
        if (dužina_VALUE < 0) return -22;
        if (dužina_VALUE == 0) return 0;
        if (!실행관리.isječak(podaci_adresa, dužina_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 odredište_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (dužina_VALUE > 16384) dužina_VALUE = 16384;
            for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) {
                int VALUE = uređaj_VALUE.기억읽기(podaci_adresa + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return dužina_VALUE;
        }
        int Fajl = cilj[기술], Veličina = Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl];
        int Pozicija = (kreirati_Postavke[기술] & 이어쓰기) != 0 ? Veličina : fajl_položaj[기술];
        if (Pozicija >= Memorija_fajl_sistem.최대크기) return -27;
        if (dužina_VALUE > Memorija_fajl_sistem.최대크기 - Pozicija) dužina_VALUE = Memorija_fajl_sistem.최대크기 - Pozicija;
        int odredište_adresa = uređaj_VALUE.fajl_Memorija() + Fajl * Memorija_fajl_sistem.최대크기;
        for (int INDEX = Veličina; INDEX < Pozicija; INDEX++) uređaj_VALUE.pisati_Memorija(odredište_adresa + INDEX, 0);
        for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) uređaj_VALUE.pisati_Memorija(odredište_adresa + Pozicija + INDEX, uređaj_VALUE.기억읽기(podaci_adresa + INDEX));
        fajl_položaj[기술] = Pozicija + dužina_VALUE;
        if (Pozicija + dužina_VALUE > Veličina) Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl] = Pozicija + dužina_VALUE;
        return dužina_VALUE;
    }
    static int tražiti_fajl(int 서술자, int Pomak_VALUE, int projicirati_koijen) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (projicirati_koijen < 0 || projicirati_koijen > 2) return -22;
        int poster_VALUE = projicirati_koijen == 0 ? 0 : (projicirati_koijen == 1 ? fajl_položaj[기술] : Memorija_fajl_sistem.podesiti_veličinu_spisak[cilj[기술]]);
        if (Pomak_VALUE > 0 && poster_VALUE > 2147483647 - Pomak_VALUE) return -75;
        if (Pomak_VALUE < 0 && Pomak_VALUE < -poster_VALUE) return -22;
        fajl_položaj[기술] = poster_VALUE + Pomak_VALUE;
        return fajl_položaj[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean dodijeliti_VALUE, int Postavke) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return dodijeliti_VALUE ? -9 : -22;
        if (dodijeliti_VALUE && 서술자 == 새서술자) return 새서술자;
        if (dodijeliti_VALUE) { if (kreirati_hvatište[새서술자] != 0) zatvoriti_fajl(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        kreirati_hvatište[새서술자] = 기술 + 1; 서술자설정[새서술자] = Postavke; Reference_COUNT[기술]++;
        return 새서술자;
    }
    static int ukloniti_fajl_unos_naziv(int naziv_adresa) {
        int dužina_VALUE = 경로읽기(naziv_adresa);
        if (dužina_VALUE < 0) return dužina_VALUE;
        int Fajl = Memorija_fajl_sistem.FIND_unos(put_naziv, dužina_VALUE);
        if (Fajl < 0) return Fajl;
        Memorija_fajl_sistem.이름들[Fajl * 64] = 0;
        return 0;
    }
    static int skup_fajl_dužina(int 서술자, int dužina_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (kreirati_Postavke[기술] & 3) == 0 || dužina_VALUE < 0) return -22;
        if (dužina_VALUE > Memorija_fajl_sistem.최대크기) return -27;
        int Fajl = cilj[기술], adresa = uređaj_VALUE.fajl_Memorija() + Fajl * Memorija_fajl_sistem.최대크기;
        for (int INDEX = Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl]; INDEX < dužina_VALUE; INDEX++) uređaj_VALUE.pisati_Memorija(adresa + INDEX, 0);
        Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl] = dužina_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int adresa) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.isječak(adresa, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(adresa + INDEX * 4, 0);
        int Fajl = cilj[기술], Veličina = 종류[기술] == 2 ? Memorija_fajl_sistem.podesiti_veličinu_spisak[Fajl] : 0;
        int 허가 = 종류[기술] == 2 ? Memorija_fajl_sistem.허가들[Fajl] : 438;
        실행관리.수쓰기(adresa, 1);
        실행관리.수쓰기(adresa + 4, 종류[기술] == 2 ? Fajl + 1 : 100 + 기술);
        실행관리.수쓰기(adresa + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(adresa + 12, 종류[기술] == 2 && Memorija_fajl_sistem.이름들[Fajl * 64] == 0 ? 0 : 1);
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
        if (Naredba == 3) return kreirati_Postavke[기술];
        if (Naredba == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            kreirati_Postavke[기술] = (kreirati_Postavke[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Create_završna_tačka(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = prazno_hvatište();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Spoji_se(서술자, 기술, 3, 0, i_za_čitanje_i_za_pisanje_zastavica);
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
    static int ček_adresa(int adresa, int dužina_VALUE) {
        if (dužina_VALUE < 16) return -22;
        if (!실행관리.isječak(adresa, 16)) return -14;
        return 실행관리.짧은수(adresa) == 2 ? 0 : -97;
    }
    static int BIND_adresa(int 서술자, int adresa, int dužina_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int mjera = ček_adresa(adresa, dužina_VALUE);
        if (mjera < 0) return mjera;
        if (Mreža_hvatište[기술] != 0) return -22;
        int Mreža_adresa = adresa_32(adresa + 4);
        if (Mreža_adresa != 0 && Mreža_adresa != Mreža_snop.내주소) return -99;
        int broj_priključka = uređaj_VALUE.기억읽기(adresa + 2) << 8 | uređaj_VALUE.기억읽기(adresa + 3);
        mjera = Mreža_snop.Otvori(broj_priključka);
        if (mjera < 0) return mjera;
        Mreža_hvatište[기술] = mjera; cilj[기술] = Mreža_adresa;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Mreža_hvatište[기술] != 0) return 0;
        int mjera = Mreža_snop.Otvori(0);
        if (mjera < 0) return mjera;
        Mreža_hvatište[기술] = mjera;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 HTTP_zahtjev 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int podaci_adresa, int dužina_VALUE, int Postavke, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Postavke != 0) return -95;
        if (dužina_VALUE < 0 || dužina_VALUE > 1024) return -90;
        if (dužina_VALUE != 0 && !실행관리.isječak(podaci_adresa, dužina_VALUE)) return -14;
        if (!실행관리.isječak(요청주소, 8)) return -14;
        int adresa = 실행관리.수(요청주소);
        int mjera = ček_adresa(adresa, 실행관리.수(요청주소 + 4));
        if (mjera < 0) return mjera;
        int broj_priključka = uređaj_VALUE.기억읽기(adresa + 2) << 8 | uređaj_VALUE.기억읽기(adresa + 3);
        if (broj_priključka == 0) return -22;
        mjera = 자동묶기(기술);
        if (mjera < 0) return mjera;
        for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) prijenos_podaci[INDEX] = uređaj_VALUE.기억읽기(podaci_adresa + INDEX);
        return Mreža_snop.poslati(Mreža_hvatište[기술], adresa_32(adresa + 4), broj_priključka, prijenos_podaci, dužina_VALUE);
    }
    static void pisati_adresa(int adresa, int dužina_VALUE, int Mreža_adresa, int broj_priključka) {
        for (int INDEX = 0; INDEX < dužina_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = broj_priključka >>> 8;
            if (INDEX == 3) VALUE = broj_priključka;
            if (INDEX >= 4 && INDEX < 8) VALUE = Mreža_adresa >>> (56 - INDEX * 8);
            uređaj_VALUE.pisati_Memorija(adresa + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int podaci_adresa, int dužina_VALUE, int Postavke, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Postavke & ~64) != 0) return -95;
        if (dužina_VALUE < 0) return -22;
        if (dužina_VALUE != 0 && !실행관리.isječak(podaci_adresa, dužina_VALUE)) return -14;
        int adresa = 0, adresa_dužina_adresa = 0, adresa_dužina = 0;
        if (요청주소 != 0) {
            if (!실행관리.isječak(요청주소, 8)) return -14;
            adresa = 실행관리.수(요청주소); adresa_dužina_adresa = 실행관리.수(요청주소 + 4);
            if (adresa != 0) {
                if (!실행관리.isječak(adresa_dužina_adresa, 4)) return -14;
                adresa_dužina = 실행관리.수(adresa_dužina_adresa);
                if (adresa_dužina < 0) return -22;
                if (!실행관리.isječak(adresa, adresa_dužina < 16 ? adresa_dužina : 16)) return -14;
            }
        }
        int mjera = 자동묶기(기술);
        if (mjera < 0) return mjera;
        int Pokreni = uređaj_VALUE.밀리초();
        while (true) {
            mjera = Mreža_snop.받기(Mreža_hvatište[기술], prijenos_podaci, 1024, 0);
            if (mjera != -11) break;
            if ((Postavke & 64) != 0 || (kreirati_Postavke[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && uređaj_VALUE.밀리초() - Pokreni >= 수신대기밀리초[기술]) return -11;
            if (uređaj_VALUE.사용자남은밀리초() <= 10) return -11;
            uređaj_VALUE.잠시양보();
        }
        if (mjera < 0) return mjera;
        if (mjera > dužina_VALUE) mjera = dužina_VALUE;
        for (int INDEX = 0; INDEX < mjera; INDEX++) uređaj_VALUE.pisati_Memorija(podaci_adresa + INDEX, prijenos_podaci[INDEX]);
        if (adresa != 0) {
            pisati_adresa(adresa, adresa_dužina, Mreža_snop.peer_adresa(Mreža_hvatište[기술]), Mreža_snop.peer_broj_priključka(Mreža_hvatište[기술]));
            실행관리.수쓰기(adresa_dužina_adresa, 16);
        }
        return mjera;
    }
    static int 통신주소읽기(int 서술자, int adresa, int dužina_adresa) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.isječak(dužina_adresa, 4)) return -14;
        int dužina_VALUE = 실행관리.수(dužina_adresa);
        if (dužina_VALUE < 0) return -22;
        if (!실행관리.isječak(adresa, dužina_VALUE < 16 ? dužina_VALUE : 16)) return -14;
        int prostor_za_unos_unos = Mreža_snop.INDEX(Mreža_hvatište[기술]);
        pisati_adresa(adresa, dužina_VALUE, cilj[기술], prostor_za_unos_unos < 0 ? 0 : Mreža_snop.접속번호들[prostor_za_unos_unos]);
        실행관리.수쓰기(dužina_adresa, 16);
        return 0;
    }
    static int 수신대기정하기(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
