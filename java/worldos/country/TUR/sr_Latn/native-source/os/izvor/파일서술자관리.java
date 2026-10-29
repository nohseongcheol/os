// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 korisnik 과정의 파일서술자와 열린 Datoteka 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int za_čitanje_pisanje_zastavica = 2, Create_stavka = 64, 독점생성 = 128, obrisati_Sadržaj = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] otvoren_pokazivač = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], cilj = new int[서술자한도];
    static int[] Datoteka_pozicija = new int[서술자한도], otvoren_Postavke = new int[서술자한도], referenca_COUNT = new int[서술자한도];
    static int[] Mreža_pokazivač = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] putanja_ime = new int[64], prenos_podaci = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return otvoren_pokazivač[파일서술자] - 1;
    }
    static int 빈서술자(int koristiti) {
        for (int INDEX = koristiti; INDEX < 서술자한도; INDEX++) if (otvoren_pokazivač[INDEX] == 0) return INDEX;
        return -24;
    }
    static int 빈기술() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (referenca_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int veze(int 서술자, int 기술, int 파일종류, int Datoteka_cilj, int Postavke) {
        otvoren_pokazivač[서술자] = 기술 + 1; 서술자설정[서술자] = (Postavke & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; cilj[기술] = Datoteka_cilj; referenca_COUNT[기술] = 1;
        otvoren_Postavke[기술] = Postavke & (3 | 이어쓰기 | 기다리지않기); Datoteka_pozicija[기술] = 0;
        Mreža_pokazivač[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_Proces() {
        CLEAN_Proces();
        for (int INDEX = 0; INDEX < 3; INDEX++) veze(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proces() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (otvoren_pokazivač[INDEX] != 0) Zatvori_Datoteka(INDEX);
    }
    static int Zatvori_Datoteka(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        otvoren_pokazivač[서술자] = 0; 서술자설정[서술자] = 0;
        referenca_COUNT[기술]--;
        if (referenca_COUNT[기술] == 0) {
            if (종류[기술] == 2) Memorija_sistem_datoteka.otvoren_COUNT[cilj[기술]]--;
            if (종류[기술] == 3 && Mreža_pokazivač[기술] != 0) Mreža_stek.Zatvori(Mreža_pokazivač[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bajt_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int adresa) {
        if (!실행관리.klip(adresa, 1)) return -14;
        int pozicija = uređaj_VALUE.기억읽기(adresa) == '/' ? 1 : 0;
        for (int 길이 = 0; 길이 < 64; 길이++) {
            if (!실행관리.klip(adresa + pozicija + 길이, 1)) return -14;
            int VALUE = uređaj_VALUE.기억읽기(adresa + pozicija + 길이);
            putanja_ime[길이] = VALUE;
            if (VALUE == 0) return 길이 == 0 ? -2 : (Memorija_sistem_datoteka.proveriti_ime(putanja_ime, 길이) ? 길이 : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int otvoren_Datoteka(int ime_adresa, int Postavke, int 허가) {
        int 길이 = 경로읽기(ime_adresa);
        if (길이 < 0) return 길이;
        if ((Postavke & ~(3 | Create_stavka | 독점생성 | obrisati_Sadržaj | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Postavke & 3) == 3 || ((Postavke & obrisati_Sadržaj) != 0 && (Postavke & 3) == 0)) return -22;
        int Datoteka = Memorija_sistem_datoteka.FIND_stavka(putanja_ime, 길이);
        if (Datoteka >= 0 && (Postavke & (Create_stavka | 독점생성)) == (Create_stavka | 독점생성)) return -17;
        if (Datoteka == -2 && (Postavke & Create_stavka) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Datoteka == -2) {
            int KR = Memorija_sistem_datoteka.Store_VALUE(putanja_ime, 길이, putanja_ime, 0);
            if (KR < 0) return KR;
            Datoteka = Memorija_sistem_datoteka.FIND_stavka(putanja_ime, 길이);
            Memorija_sistem_datoteka.허가들[Datoteka] = 허가 & 511;
        }
        if (Datoteka < 0) return Datoteka;
        if ((Postavke & obrisati_Sadržaj) != 0) Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka] = 0;
        Memorija_sistem_datoteka.otvoren_COUNT[Datoteka]++;
        return veze(서술자, 기술, 2, Datoteka, Postavke);
    }
    static int 파일읽기(int 서술자, int podaci_adresa, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (otvoren_Postavke[기술] & 3) == 1) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.klip(podaci_adresa, 길이)) return -14;
        if (종류[기술] == 3) return primiti_datagram_podaci(서술자, podaci_adresa, 길이, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < 길이) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = tastatura.읽기();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((otvoren_Postavke[기술] & 기다리지않기) != 0) return -11;
                    if (uređaj_VALUE.사용자남은밀리초() <= 10) return -11;
                    Mreža_stek.verifikovati(); uređaj_VALUE.잠시양보();
                } else {
                    uređaj_VALUE.기억쓰기(podaci_adresa + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Datoteka = cilj[기술], pozicija = Datoteka_pozicija[기술];
        if (pozicija >= Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka]) return 0;
        if (길이 > Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka] - pozicija) 길이 = Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka] - pozicija;
        int 원본주소 = uređaj_VALUE.Datoteka_Memorija() + Datoteka * Memorija_sistem_datoteka.최대크기 + pozicija;
        for (int INDEX = 0; INDEX < 길이; INDEX++) uređaj_VALUE.기억쓰기(podaci_adresa + INDEX, uređaj_VALUE.기억읽기(원본주소 + INDEX));
        Datoteka_pozicija[기술] += 길이;
        return 길이;
    }
    static int 파일쓰기(int 서술자, int podaci_adresa, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (otvoren_Postavke[기술] & 3) == 0) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.klip(podaci_adresa, 길이)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 odredište_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (길이 > 16384) 길이 = 16384;
            for (int INDEX = 0; INDEX < 길이; INDEX++) {
                int VALUE = uređaj_VALUE.기억읽기(podaci_adresa + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return 길이;
        }
        int Datoteka = cilj[기술], promeniti_veličinu = Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka];
        int pozicija = (otvoren_Postavke[기술] & 이어쓰기) != 0 ? promeniti_veličinu : Datoteka_pozicija[기술];
        if (pozicija >= Memorija_sistem_datoteka.최대크기) return -27;
        if (길이 > Memorija_sistem_datoteka.최대크기 - pozicija) 길이 = Memorija_sistem_datoteka.최대크기 - pozicija;
        int odredište_adresa = uređaj_VALUE.Datoteka_Memorija() + Datoteka * Memorija_sistem_datoteka.최대크기;
        for (int INDEX = promeniti_veličinu; INDEX < pozicija; INDEX++) uređaj_VALUE.기억쓰기(odredište_adresa + INDEX, 0);
        for (int INDEX = 0; INDEX < 길이; INDEX++) uređaj_VALUE.기억쓰기(odredište_adresa + pozicija + INDEX, uređaj_VALUE.기억읽기(podaci_adresa + INDEX));
        Datoteka_pozicija[기술] = pozicija + 길이;
        if (pozicija + 길이 > promeniti_veličinu) Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka] = pozicija + 길이;
        return 길이;
    }
    static int tražiti_Datoteka(int 서술자, int Pomak_VALUE, int radnja_koren) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (radnja_koren < 0 || radnja_koren > 2) return -22;
        int poster_VALUE = radnja_koren == 0 ? 0 : (radnja_koren == 1 ? Datoteka_pozicija[기술] : Memorija_sistem_datoteka.promeniti_veličinu_Lista[cilj[기술]]);
        if (Pomak_VALUE > 0 && poster_VALUE > 2147483647 - Pomak_VALUE) return -75;
        if (Pomak_VALUE < 0 && Pomak_VALUE < -poster_VALUE) return -22;
        Datoteka_pozicija[기술] = poster_VALUE + Pomak_VALUE;
        return Datoteka_pozicija[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Dodeli_VALUE, int Postavke) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Dodeli_VALUE ? -9 : -22;
        if (Dodeli_VALUE && 서술자 == 새서술자) return 새서술자;
        if (Dodeli_VALUE) { if (otvoren_pokazivač[새서술자] != 0) Zatvori_Datoteka(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        otvoren_pokazivač[새서술자] = 기술 + 1; 서술자설정[새서술자] = Postavke; referenca_COUNT[기술]++;
        return 새서술자;
    }
    static int ukloniti_Datoteka_stavka_ime(int ime_adresa) {
        int 길이 = 경로읽기(ime_adresa);
        if (길이 < 0) return 길이;
        int Datoteka = Memorija_sistem_datoteka.FIND_stavka(putanja_ime, 길이);
        if (Datoteka < 0) return Datoteka;
        Memorija_sistem_datoteka.이름들[Datoteka * 64] = 0;
        return 0;
    }
    static int 파일길이정하기(int 서술자, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (otvoren_Postavke[기술] & 3) == 0 || 길이 < 0) return -22;
        if (길이 > Memorija_sistem_datoteka.최대크기) return -27;
        int Datoteka = cilj[기술], adresa = uređaj_VALUE.Datoteka_Memorija() + Datoteka * Memorija_sistem_datoteka.최대크기;
        for (int INDEX = Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka]; INDEX < 길이; INDEX++) uređaj_VALUE.기억쓰기(adresa + INDEX, 0);
        Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka] = 길이;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int adresa) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klip(adresa, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(adresa + INDEX * 4, 0);
        int Datoteka = cilj[기술], promeniti_veličinu = 종류[기술] == 2 ? Memorija_sistem_datoteka.promeniti_veličinu_Lista[Datoteka] : 0;
        int 허가 = 종류[기술] == 2 ? Memorija_sistem_datoteka.허가들[Datoteka] : 438;
        실행관리.수쓰기(adresa, 1);
        실행관리.수쓰기(adresa + 4, 종류[기술] == 2 ? Datoteka + 1 : 100 + 기술);
        실행관리.수쓰기(adresa + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(adresa + 12, 종류[기술] == 2 && Memorija_sistem_datoteka.이름들[Datoteka * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(adresa + 28, promeniti_veličinu); 실행관리.수쓰기(adresa + 32, 512);
        실행관리.수쓰기(adresa + 36, (promeniti_veličinu + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int komanda, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (komanda == 0 || komanda == 1030) return 서술자복제(서술자, VALUE, false, komanda == 1030 ? 1 : 0);
        if (komanda == 1) return 서술자설정[서술자];
        if (komanda == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (komanda == 3) return otvoren_Postavke[기술];
        if (komanda == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            otvoren_Postavke[기술] = (otvoren_Postavke[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Create_učesnik(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return veze(서술자, 기술, 3, 0, za_čitanje_pisanje_zastavica);
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
    static int proveriti_adresa(int adresa, int 길이) {
        if (길이 < 16) return -22;
        if (!실행관리.klip(adresa, 16)) return -14;
        return 실행관리.짧은수(adresa) == 2 ? 0 : -97;
    }
    static int povezati_adresa(int 서술자, int adresa, int 길이) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int KR = proveriti_adresa(adresa, 길이);
        if (KR < 0) return KR;
        if (Mreža_pokazivač[기술] != 0) return -22;
        int ID_mreže = adresa_32(adresa + 4);
        if (ID_mreže != 0 && ID_mreže != Mreža_stek.내주소) return -99;
        int broj_porta = uređaj_VALUE.기억읽기(adresa + 2) << 8 | uređaj_VALUE.기억읽기(adresa + 3);
        KR = Mreža_stek.otvoren(broj_porta);
        if (KR < 0) return KR;
        Mreža_pokazivač[기술] = KR; cilj[기술] = ID_mreže;
        return 0;
    }
    static int Automatski_režim_povezati(int 기술) {
        if (Mreža_pokazivač[기술] != 0) return 0;
        int KR = Mreža_stek.otvoren(0);
        if (KR < 0) return KR;
        Mreža_pokazivač[기술] = KR;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 zahtev 구조체로 전달한다.
    static int poslati_datagram_podaci(int 서술자, int podaci_adresa, int 길이, int Postavke, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Postavke != 0) return -95;
        if (길이 < 0 || 길이 > 1024) return -90;
        if (길이 != 0 && !실행관리.klip(podaci_adresa, 길이)) return -14;
        if (!실행관리.klip(요청주소, 8)) return -14;
        int adresa = 실행관리.수(요청주소);
        int KR = proveriti_adresa(adresa, 실행관리.수(요청주소 + 4));
        if (KR < 0) return KR;
        int broj_porta = uređaj_VALUE.기억읽기(adresa + 2) << 8 | uređaj_VALUE.기억읽기(adresa + 3);
        if (broj_porta == 0) return -22;
        KR = Automatski_režim_povezati(기술);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < 길이; INDEX++) prenos_podaci[INDEX] = uređaj_VALUE.기억읽기(podaci_adresa + INDEX);
        return Mreža_stek.poslati(Mreža_pokazivač[기술], adresa_32(adresa + 4), broj_porta, prenos_podaci, 길이);
    }
    static void 주소쓰기(int adresa, int 길이, int ID_mreže, int broj_porta) {
        for (int INDEX = 0; INDEX < 길이 && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = broj_porta >>> 8;
            if (INDEX == 3) VALUE = broj_porta;
            if (INDEX >= 4 && INDEX < 8) VALUE = ID_mreže >>> (56 - INDEX * 8);
            uređaj_VALUE.기억쓰기(adresa + INDEX, VALUE & 255);
        }
    }
    static int primiti_datagram_podaci(int 서술자, int podaci_adresa, int 길이, int Postavke, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Postavke & ~64) != 0) return -95;
        if (길이 < 0) return -22;
        if (길이 != 0 && !실행관리.klip(podaci_adresa, 길이)) return -14;
        int adresa = 0, 주소길이주소 = 0, 주소길이 = 0;
        if (요청주소 != 0) {
            if (!실행관리.klip(요청주소, 8)) return -14;
            adresa = 실행관리.수(요청주소); 주소길이주소 = 실행관리.수(요청주소 + 4);
            if (adresa != 0) {
                if (!실행관리.klip(주소길이주소, 4)) return -14;
                주소길이 = 실행관리.수(주소길이주소);
                if (주소길이 < 0) return -22;
                if (!실행관리.klip(adresa, 주소길이 < 16 ? 주소길이 : 16)) return -14;
            }
        }
        int KR = Automatski_režim_povezati(기술);
        if (KR < 0) return KR;
        int koristiti = uređaj_VALUE.밀리초();
        while (true) {
            KR = Mreža_stek.primiti(Mreža_pokazivač[기술], prenos_podaci, 1024, 0);
            if (KR != -11) break;
            if ((Postavke & 64) != 0 || (otvoren_Postavke[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && uređaj_VALUE.밀리초() - koristiti >= 수신대기밀리초[기술]) return -11;
            if (uređaj_VALUE.사용자남은밀리초() <= 10) return -11;
            uređaj_VALUE.잠시양보();
        }
        if (KR < 0) return KR;
        if (KR > 길이) KR = 길이;
        for (int INDEX = 0; INDEX < KR; INDEX++) uređaj_VALUE.기억쓰기(podaci_adresa + INDEX, prenos_podaci[INDEX]);
        if (adresa != 0) {
            주소쓰기(adresa, 주소길이, Mreža_stek.ravnopravni_uređaj_adresa(Mreža_pokazivač[기술]), Mreža_stek.ravnopravni_uređaj_broj_porta(Mreža_pokazivač[기술]));
            실행관리.수쓰기(주소길이주소, 16);
        }
        return KR;
    }
    static int 통신주소읽기(int 서술자, int adresa, int 길이주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klip(길이주소, 4)) return -14;
        int 길이 = 실행관리.수(길이주소);
        if (길이 < 0) return -22;
        if (!실행관리.klip(adresa, 길이 < 16 ? 길이 : 16)) return -14;
        int 칸 = Mreža_stek.INDEX(Mreža_pokazivač[기술]);
        주소쓰기(adresa, 길이, cilj[기술], 칸 < 0 ? 0 : Mreža_stek.접속번호들[칸]);
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
