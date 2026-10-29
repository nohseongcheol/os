// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 uporabnik 과정의 파일서술자와 열린 Datoteka 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int branje_pisanje_zastavica = 2, Ustvari_vnos = 64, 독점생성 = 128, počistiti_Vsebina = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] odprto_ročica = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], tarča = new int[서술자한도];
    static int[] Datoteka_položaj = new int[서술자한도], odprto_Nastavitve = new int[서술자한도], Gradiva_COUNT = new int[서술자한도];
    static int[] mreža_ročica = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] pot_ime = new int[64], Prenos_podatki = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return odprto_ročica[파일서술자] - 1;
    }
    static int 빈서술자(int Zaženi) {
        for (int INDEX = Zaženi; INDEX < 서술자한도; INDEX++) if (odprto_ročica[INDEX] == 0) return INDEX;
        return -24;
    }
    static int prazen_ročica() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Gradiva_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Poveži(int 서술자, int 기술, int 파일종류, int Datoteka_tarča, int Nastavitve) {
        odprto_ročica[서술자] = 기술 + 1; 서술자설정[서술자] = (Nastavitve & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; tarča[기술] = Datoteka_tarča; Gradiva_COUNT[기술] = 1;
        odprto_Nastavitve[기술] = Nastavitve & (3 | 이어쓰기 | 기다리지않기); Datoteka_položaj[기술] = 0;
        mreža_ročica[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Start_Proces() {
        CLEAN_Proces();
        for (int INDEX = 0; INDEX < 3; INDEX++) Poveži(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proces() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (odprto_ročica[INDEX] != 0) Zapri_Datoteka(INDEX);
    }
    static int Zapri_Datoteka(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        odprto_ročica[서술자] = 0; 서술자설정[서술자] = 0;
        Gradiva_COUNT[기술]--;
        if (Gradiva_COUNT[기술] == 0) {
            if (종류[기술] == 2) pomnilnik_datotečni_sistem.odprto_COUNT[tarča[기술]]--;
            if (종류[기술] == 3 && mreža_ročica[기술] != 0) mreža_Sklad.Zapri(mreža_ročica[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bajt_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int naslov) {
        if (!실행관리.izrezek(naslov, 1)) return -14;
        int Položaj = naprava_VALUE.기억읽기(naslov) == '/' ? 1 : 0;
        for (int 길이 = 0; 길이 < 64; 길이++) {
            if (!실행관리.izrezek(naslov + Položaj + 길이, 1)) return -14;
            int VALUE = naprava_VALUE.기억읽기(naslov + Položaj + 길이);
            pot_ime[길이] = VALUE;
            if (VALUE == 0) return 길이 == 0 ? -2 : (pomnilnik_datotečni_sistem.preveriti_ime(pot_ime, 길이) ? 길이 : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int odprto_Datoteka(int ime_naslov, int Nastavitve, int 허가) {
        int 길이 = 경로읽기(ime_naslov);
        if (길이 < 0) return 길이;
        if ((Nastavitve & ~(3 | Ustvari_vnos | 독점생성 | počistiti_Vsebina | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Nastavitve & 3) == 3 || ((Nastavitve & počistiti_Vsebina) != 0 && (Nastavitve & 3) == 0)) return -22;
        int Datoteka = pomnilnik_datotečni_sistem.FIND_vnos(pot_ime, 길이);
        if (Datoteka >= 0 && (Nastavitve & (Ustvari_vnos | 독점생성)) == (Ustvari_vnos | 독점생성)) return -17;
        if (Datoteka == -2 && (Nastavitve & Ustvari_vnos) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = prazen_ročica();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Datoteka == -2) {
            int REZULTAT = pomnilnik_datotečni_sistem.Store_VALUE(pot_ime, 길이, pot_ime, 0);
            if (REZULTAT < 0) return REZULTAT;
            Datoteka = pomnilnik_datotečni_sistem.FIND_vnos(pot_ime, 길이);
            pomnilnik_datotečni_sistem.허가들[Datoteka] = 허가 & 511;
        }
        if (Datoteka < 0) return Datoteka;
        if ((Nastavitve & počistiti_Vsebina) != 0) pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka] = 0;
        pomnilnik_datotečni_sistem.odprto_COUNT[Datoteka]++;
        return Poveži(서술자, 기술, 2, Datoteka, Nastavitve);
    }
    static int 파일읽기(int 서술자, int podatki_naslov, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (odprto_Nastavitve[기술] & 3) == 1) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.izrezek(podatki_naslov, 길이)) return -14;
        if (종류[기술] == 3) return sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(서술자, podatki_naslov, 길이, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < 길이) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = tipkovnica.Branje();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((odprto_Nastavitve[기술] & 기다리지않기) != 0) return -11;
                    if (naprava_VALUE.사용자남은밀리초() <= 10) return -11;
                    mreža_Sklad.확인(); naprava_VALUE.잠시양보();
                } else {
                    naprava_VALUE.pisati_pomnilnik(podatki_naslov + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Datoteka = tarča[기술], Položaj = Datoteka_položaj[기술];
        if (Položaj >= pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka]) return 0;
        if (길이 > pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka] - Položaj) 길이 = pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka] - Položaj;
        int 원본주소 = naprava_VALUE.Datoteka_pomnilnik() + Datoteka * pomnilnik_datotečni_sistem.최대크기 + Položaj;
        for (int INDEX = 0; INDEX < 길이; INDEX++) naprava_VALUE.pisati_pomnilnik(podatki_naslov + INDEX, naprava_VALUE.기억읽기(원본주소 + INDEX));
        Datoteka_položaj[기술] += 길이;
        return 길이;
    }
    static int pisati_Datoteka(int 서술자, int podatki_naslov, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (odprto_Nastavitve[기술] & 3) == 0) return -9;
        if (길이 < 0) return -22;
        if (길이 == 0) return 0;
        if (!실행관리.izrezek(podatki_naslov, 길이)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 cilj_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (길이 > 16384) 길이 = 16384;
            for (int INDEX = 0; INDEX < 길이; INDEX++) {
                int VALUE = naprava_VALUE.기억읽기(podatki_naslov + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return 길이;
        }
        int Datoteka = tarča[기술], Velikost = pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka];
        int Položaj = (odprto_Nastavitve[기술] & 이어쓰기) != 0 ? Velikost : Datoteka_položaj[기술];
        if (Položaj >= pomnilnik_datotečni_sistem.최대크기) return -27;
        if (길이 > pomnilnik_datotečni_sistem.최대크기 - Položaj) 길이 = pomnilnik_datotečni_sistem.최대크기 - Položaj;
        int cilj_naslov_08bbd577 = naprava_VALUE.Datoteka_pomnilnik() + Datoteka * pomnilnik_datotečni_sistem.최대크기;
        for (int INDEX = Velikost; INDEX < Položaj; INDEX++) naprava_VALUE.pisati_pomnilnik(cilj_naslov_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < 길이; INDEX++) naprava_VALUE.pisati_pomnilnik(cilj_naslov_08bbd577 + Položaj + INDEX, naprava_VALUE.기억읽기(podatki_naslov + INDEX));
        Datoteka_položaj[기술] = Položaj + 길이;
        if (Položaj + 길이 > Velikost) pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka] = Položaj + 길이;
        return 길이;
    }
    static int iskati_Datoteka(int 서술자, int odmik_VALUE, int pobuda_koren) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (pobuda_koren < 0 || pobuda_koren > 2) return -22;
        int Ozadje_VALUE = pobuda_koren == 0 ? 0 : (pobuda_koren == 1 ? Datoteka_položaj[기술] : pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[tarča[기술]]);
        if (odmik_VALUE > 0 && Ozadje_VALUE > 2147483647 - odmik_VALUE) return -75;
        if (odmik_VALUE < 0 && odmik_VALUE < -Ozadje_VALUE) return -22;
        Datoteka_položaj[기술] = Ozadje_VALUE + odmik_VALUE;
        return Datoteka_položaj[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Dodeli_VALUE, int Nastavitve) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Dodeli_VALUE ? -9 : -22;
        if (Dodeli_VALUE && 서술자 == 새서술자) return 새서술자;
        if (Dodeli_VALUE) { if (odprto_ročica[새서술자] != 0) Zapri_Datoteka(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        odprto_ročica[새서술자] = 기술 + 1; 서술자설정[새서술자] = Nastavitve; Gradiva_COUNT[기술]++;
        return 새서술자;
    }
    static int odstraniti_Datoteka_vnos_ime(int ime_naslov) {
        int 길이 = 경로읽기(ime_naslov);
        if (길이 < 0) return 길이;
        int Datoteka = pomnilnik_datotečni_sistem.FIND_vnos(pot_ime, 길이);
        if (Datoteka < 0) return Datoteka;
        pomnilnik_datotečni_sistem.이름들[Datoteka * 64] = 0;
        return 0;
    }
    static int 파일길이정하기(int 서술자, int 길이) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (odprto_Nastavitve[기술] & 3) == 0 || 길이 < 0) return -22;
        if (길이 > pomnilnik_datotečni_sistem.최대크기) return -27;
        int Datoteka = tarča[기술], naslov = naprava_VALUE.Datoteka_pomnilnik() + Datoteka * pomnilnik_datotečni_sistem.최대크기;
        for (int INDEX = pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka]; INDEX < 길이; INDEX++) naprava_VALUE.pisati_pomnilnik(naslov + INDEX, 0);
        pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka] = 길이;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int naslov) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.izrezek(naslov, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(naslov + INDEX * 4, 0);
        int Datoteka = tarča[기술], Velikost = 종류[기술] == 2 ? pomnilnik_datotečni_sistem.spremeniti_velikost_Seznam[Datoteka] : 0;
        int 허가 = 종류[기술] == 2 ? pomnilnik_datotečni_sistem.허가들[Datoteka] : 438;
        실행관리.수쓰기(naslov, 1);
        실행관리.수쓰기(naslov + 4, 종류[기술] == 2 ? Datoteka + 1 : 100 + 기술);
        실행관리.수쓰기(naslov + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(naslov + 12, 종류[기술] == 2 && pomnilnik_datotečni_sistem.이름들[Datoteka * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(naslov + 28, Velikost); 실행관리.수쓰기(naslov + 32, 512);
        실행관리.수쓰기(naslov + 36, (Velikost + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Ukaz, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Ukaz == 0 || Ukaz == 1030) return 서술자복제(서술자, VALUE, false, Ukaz == 1030 ? 1 : 0);
        if (Ukaz == 1) return 서술자설정[서술자];
        if (Ukaz == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Ukaz == 3) return odprto_Nastavitve[기술];
        if (Ukaz == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            odprto_Nastavitve[기술] = (odprto_Nastavitve[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Ustvari_končna_točka(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = prazen_ročica();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Poveži(서술자, 기술, 3, 0, branje_pisanje_zastavica);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int naslov_32(int naslov) {
        return naprava_VALUE.기억읽기(naslov) << 24 | naprava_VALUE.기억읽기(naslov + 1) << 16
            | naprava_VALUE.기억읽기(naslov + 2) << 8 | naprava_VALUE.기억읽기(naslov + 3);
    }
    static int preveriti_naslov(int naslov, int 길이) {
        if (길이 < 16) return -22;
        if (!실행관리.izrezek(naslov, 16)) return -14;
        return 실행관리.짧은수(naslov) == 2 ? 0 : -97;
    }
    static int BIND_naslov(int 서술자, int naslov, int 길이) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int REZULTAT = preveriti_naslov(naslov, 길이);
        if (REZULTAT < 0) return REZULTAT;
        if (mreža_ročica[기술] != 0) return -22;
        int omrežni_identifikator = naslov_32(naslov + 4);
        if (omrežni_identifikator != 0 && omrežni_identifikator != mreža_Sklad.내주소) return -99;
        int številka_vrat = naprava_VALUE.기억읽기(naslov + 2) << 8 | naprava_VALUE.기억읽기(naslov + 3);
        REZULTAT = mreža_Sklad.Odpri(številka_vrat);
        if (REZULTAT < 0) return REZULTAT;
        mreža_ročica[기술] = REZULTAT; tarča[기술] = omrežni_identifikator;
        return 0;
    }
    static int Samodejni_način_BIND(int 기술) {
        if (mreža_ročica[기술] != 0) return 0;
        int REZULTAT = mreža_Sklad.Odpri(0);
        if (REZULTAT < 0) return REZULTAT;
        mreža_ročica[기술] = REZULTAT;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 zahteva 구조체로 전달한다.
    static int poslati_datagram_podatki(int 서술자, int podatki_naslov, int 길이, int Nastavitve, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Nastavitve != 0) return -95;
        if (길이 < 0 || 길이 > 1024) return -90;
        if (길이 != 0 && !실행관리.izrezek(podatki_naslov, 길이)) return -14;
        if (!실행관리.izrezek(요청주소, 8)) return -14;
        int naslov = 실행관리.수(요청주소);
        int REZULTAT = preveriti_naslov(naslov, 실행관리.수(요청주소 + 4));
        if (REZULTAT < 0) return REZULTAT;
        int številka_vrat = naprava_VALUE.기억읽기(naslov + 2) << 8 | naprava_VALUE.기억읽기(naslov + 3);
        if (številka_vrat == 0) return -22;
        REZULTAT = Samodejni_način_BIND(기술);
        if (REZULTAT < 0) return REZULTAT;
        for (int INDEX = 0; INDEX < 길이; INDEX++) Prenos_podatki[INDEX] = naprava_VALUE.기억읽기(podatki_naslov + INDEX);
        return mreža_Sklad.poslati(mreža_ročica[기술], naslov_32(naslov + 4), številka_vrat, Prenos_podatki, 길이);
    }
    static void pisati_naslov(int naslov, int 길이, int omrežni_identifikator, int številka_vrat) {
        for (int INDEX = 0; INDEX < 길이 && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = številka_vrat >>> 8;
            if (INDEX == 3) VALUE = številka_vrat;
            if (INDEX >= 4 && INDEX < 8) VALUE = omrežni_identifikator >>> (56 - INDEX * 8);
            naprava_VALUE.pisati_pomnilnik(naslov + INDEX, VALUE & 255);
        }
    }
    static int sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(int 서술자, int podatki_naslov, int 길이, int Nastavitve, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Nastavitve & ~64) != 0) return -95;
        if (길이 < 0) return -22;
        if (길이 != 0 && !실행관리.izrezek(podatki_naslov, 길이)) return -14;
        int naslov = 0, 주소길이주소 = 0, 주소길이 = 0;
        if (요청주소 != 0) {
            if (!실행관리.izrezek(요청주소, 8)) return -14;
            naslov = 실행관리.수(요청주소); 주소길이주소 = 실행관리.수(요청주소 + 4);
            if (naslov != 0) {
                if (!실행관리.izrezek(주소길이주소, 4)) return -14;
                주소길이 = 실행관리.수(주소길이주소);
                if (주소길이 < 0) return -22;
                if (!실행관리.izrezek(naslov, 주소길이 < 16 ? 주소길이 : 16)) return -14;
            }
        }
        int REZULTAT = Samodejni_način_BIND(기술);
        if (REZULTAT < 0) return REZULTAT;
        int Zaženi = naprava_VALUE.밀리초();
        while (true) {
            REZULTAT = mreža_Sklad.sprejeti_sprejemati_prejeti_prejemati(mreža_ročica[기술], Prenos_podatki, 1024, 0);
            if (REZULTAT != -11) break;
            if ((Nastavitve & 64) != 0 || (odprto_Nastavitve[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && naprava_VALUE.밀리초() - Zaženi >= 수신대기밀리초[기술]) return -11;
            if (naprava_VALUE.사용자남은밀리초() <= 10) return -11;
            naprava_VALUE.잠시양보();
        }
        if (REZULTAT < 0) return REZULTAT;
        if (REZULTAT > 길이) REZULTAT = 길이;
        for (int INDEX = 0; INDEX < REZULTAT; INDEX++) naprava_VALUE.pisati_pomnilnik(podatki_naslov + INDEX, Prenos_podatki[INDEX]);
        if (naslov != 0) {
            pisati_naslov(naslov, 주소길이, mreža_Sklad.enakovreden_naslov(mreža_ročica[기술]), mreža_Sklad.enakovreden_številka_vrat(mreža_ročica[기술]));
            실행관리.수쓰기(주소길이주소, 16);
        }
        return REZULTAT;
    }
    static int 통신주소읽기(int 서술자, int naslov, int 길이주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.izrezek(길이주소, 4)) return -14;
        int 길이 = 실행관리.수(길이주소);
        if (길이 < 0) return -22;
        if (!실행관리.izrezek(naslov, 길이 < 16 ? 길이 : 16)) return -14;
        int 칸 = mreža_Sklad.INDEX(mreža_ročica[기술]);
        pisati_naslov(naslov, 길이, tarča[기술], 칸 < 0 ? 0 : mreža_Sklad.접속번호들[칸]);
        실행관리.수쓰기(길이주소, 16);
        return 0;
    }
    static int nabor_sprejeti_sprejemati_prejeti_prejemati_TIMEOUT(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
