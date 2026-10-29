// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 kaiwhakamahi 과정의 파일서술자와 열린 Kōnae 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int 읽기쓰기 = 2, Waihanga_tāurunga = 64, 독점생성 = 128, ūkui_IRI = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] tiwhikete_raweke = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], ūnga = new int[서술자한도];
    static int[] kōnae_tūranga = new int[서술자한도], tiwhikete_Ngā_Tautuhinga = new int[서술자한도], Pūranga_kōrero_COUNT = new int[서술자한도];
    static int[] whatunga_raweke = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] ara_ingoa = new int[64], whakawhiti_raraunga = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return tiwhikete_raweke[파일서술자] - 1;
    }
    static int 빈서술자(int whakahaere) {
        for (int INDEX = whakahaere; INDEX < 서술자한도; INDEX++) if (tiwhikete_raweke[INDEX] == 0) return INDEX;
        return -24;
    }
    static int putua_raweke() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Pūranga_kōrero_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int TŪHONO(int 서술자, int 기술, int 파일종류, int kōnae_ūnga, int Ngā_Tautuhinga) {
        tiwhikete_raweke[서술자] = 기술 + 1; 서술자설정[서술자] = (Ngā_Tautuhinga & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; ūnga[기술] = kōnae_ūnga; Pūranga_kōrero_COUNT[기술] = 1;
        tiwhikete_Ngā_Tautuhinga[기술] = Ngā_Tautuhinga & (3 | 이어쓰기 | 기다리지않기); kōnae_tūranga[기술] = 0;
        whatunga_raweke[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Start_Hātepe() {
        CLEAN_Hātepe();
        for (int INDEX = 0; INDEX < 3; INDEX++) TŪHONO(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Hātepe() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (tiwhikete_raweke[INDEX] != 0) kati_kōnae(INDEX);
    }
    static int kati_kōnae(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        tiwhikete_raweke[서술자] = 0; 서술자설정[서술자] = 0;
        Pūranga_kōrero_COUNT[기술]--;
        if (Pūranga_kōrero_COUNT[기술] == 0) {
            if (종류[기술] == 2) Pūmahara_pūnaha_kōnae.tiwhikete_COUNT[ūnga[기술]]--;
            if (종류[기술] == 3 && whatunga_raweke[기술] != 0) whatunga_Huinga.Kati(whatunga_raweke[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 paita_uara 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ADDRESS) {
        if (!실행관리.topenga(ADDRESS, 1)) return -14;
        int tūranga = pūkoro_uara.기억읽기(ADDRESS) == '/' ? 1 : 0;
        for (int roa_uara = 0; roa_uara < 64; roa_uara++) {
            if (!실행관리.topenga(ADDRESS + tūranga + roa_uara, 1)) return -14;
            int uara = pūkoro_uara.기억읽기(ADDRESS + tūranga + roa_uara);
            ara_ingoa[roa_uara] = uara;
            if (uara == 0) return roa_uara == 0 ? -2 : (Pūmahara_pūnaha_kōnae.taki_ingoa(ara_ingoa, roa_uara) ? roa_uara : -22);
            if (uara == '/') return -20;
        }
        return -36;
    }
    static int tiwhikete_kōnae(int ingoa_ADDRESS, int Ngā_Tautuhinga, int 허가) {
        int roa_uara = 경로읽기(ingoa_ADDRESS);
        if (roa_uara < 0) return roa_uara;
        if ((Ngā_Tautuhinga & ~(3 | Waihanga_tāurunga | 독점생성 | ūkui_IRI | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Ngā_Tautuhinga & 3) == 3 || ((Ngā_Tautuhinga & ūkui_IRI) != 0 && (Ngā_Tautuhinga & 3) == 0)) return -22;
        int Kōnae = Pūmahara_pūnaha_kōnae.FIND_tāurunga(ara_ingoa, roa_uara);
        if (Kōnae >= 0 && (Ngā_Tautuhinga & (Waihanga_tāurunga | 독점생성)) == (Waihanga_tāurunga | 독점생성)) return -17;
        if (Kōnae == -2 && (Ngā_Tautuhinga & Waihanga_tāurunga) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = putua_raweke();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Kōnae == -2) {
            int mēhua = Pūmahara_pūnaha_kōnae.Store_uara(ara_ingoa, roa_uara, ara_ingoa, 0);
            if (mēhua < 0) return mēhua;
            Kōnae = Pūmahara_pūnaha_kōnae.FIND_tāurunga(ara_ingoa, roa_uara);
            Pūmahara_pūnaha_kōnae.허가들[Kōnae] = 허가 & 511;
        }
        if (Kōnae < 0) return Kōnae;
        if ((Ngā_Tautuhinga & ūkui_IRI) != 0) Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae] = 0;
        Pūmahara_pūnaha_kōnae.tiwhikete_COUNT[Kōnae]++;
        return TŪHONO(서술자, 기술, 2, Kōnae, Ngā_Tautuhinga);
    }
    static int 파일읽기(int 서술자, int raraunga_ADDRESS, int roa_uara) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (tiwhikete_Ngā_Tautuhinga[기술] & 3) == 1) return -9;
        if (roa_uara < 0) return -22;
        if (roa_uara == 0) return 0;
        if (!실행관리.topenga(raraunga_ADDRESS, roa_uara)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, raraunga_ADDRESS, roa_uara, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < roa_uara) {
                int uara = TEXT_Tauranga.직렬읽기();
                if (uara < 0) uara = papapātuhi.Pānuitia();
                if (uara < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((tiwhikete_Ngā_Tautuhinga[기술] & 기다리지않기) != 0) return -11;
                    if (pūkoro_uara.사용자남은밀리초() <= 10) return -11;
                    whatunga_Huinga.manatoko(); pūkoro_uara.잠시양보();
                } else {
                    pūkoro_uara.tuhi_Pūmahara(raraunga_ADDRESS + RECEIVED_COUNT, uara); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Kōnae = ūnga[기술], tūranga = kōnae_tūranga[기술];
        if (tūranga >= Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae]) return 0;
        if (roa_uara > Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae] - tūranga) roa_uara = Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae] - tūranga;
        int 원본주소 = pūkoro_uara.kōnae_Pūmahara() + Kōnae * Pūmahara_pūnaha_kōnae.최대크기 + tūranga;
        for (int INDEX = 0; INDEX < roa_uara; INDEX++) pūkoro_uara.tuhi_Pūmahara(raraunga_ADDRESS + INDEX, pūkoro_uara.기억읽기(원본주소 + INDEX));
        kōnae_tūranga[기술] += roa_uara;
        return roa_uara;
    }
    static int tuhi_kōnae(int 서술자, int raraunga_ADDRESS, int roa_uara) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (tiwhikete_Ngā_Tautuhinga[기술] & 3) == 0) return -9;
        if (roa_uara < 0) return -22;
        if (roa_uara == 0) return 0;
        if (!실행관리.topenga(raraunga_ADDRESS, roa_uara)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 ūnga_uara 주소가 필요하다.
        if (종류[기술] == 1) {
            if (roa_uara > 16384) roa_uara = 16384;
            for (int INDEX = 0; INDEX < roa_uara; INDEX++) {
                int uara = pūkoro_uara.기억읽기(raraunga_ADDRESS + INDEX);
                TEXT_Tauranga.직렬바이트(uara); TEXT_Tauranga.화면문자(uara);
            }
            return roa_uara;
        }
        int Kōnae = ūnga[기술], rahi = Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae];
        int tūranga = (tiwhikete_Ngā_Tautuhinga[기술] & 이어쓰기) != 0 ? rahi : kōnae_tūranga[기술];
        if (tūranga >= Pūmahara_pūnaha_kōnae.최대크기) return -27;
        if (roa_uara > Pūmahara_pūnaha_kōnae.최대크기 - tūranga) roa_uara = Pūmahara_pūnaha_kōnae.최대크기 - tūranga;
        int ūnga_ADDRESS_08bbd577 = pūkoro_uara.kōnae_Pūmahara() + Kōnae * Pūmahara_pūnaha_kōnae.최대크기;
        for (int INDEX = rahi; INDEX < tūranga; INDEX++) pūkoro_uara.tuhi_Pūmahara(ūnga_ADDRESS_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < roa_uara; INDEX++) pūkoro_uara.tuhi_Pūmahara(ūnga_ADDRESS_08bbd577 + tūranga + INDEX, pūkoro_uara.기억읽기(raraunga_ADDRESS + INDEX));
        kōnae_tūranga[기술] = tūranga + roa_uara;
        if (tūranga + roa_uara > rahi) Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae] = tūranga + roa_uara;
        return roa_uara;
    }
    static int kimi_kōnae(int 서술자, int OFFSET_uara, int whakaatu_pūtake) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (whakaatu_pūtake < 0 || whakaatu_pūtake > 2) return -22;
        int Papamuri_uara = whakaatu_pūtake == 0 ? 0 : (whakaatu_pūtake == 1 ? kōnae_tūranga[기술] : Pūmahara_pūnaha_kōnae.rahi_Rārangi[ūnga[기술]]);
        if (OFFSET_uara > 0 && Papamuri_uara > 2147483647 - OFFSET_uara) return -75;
        if (OFFSET_uara < 0 && OFFSET_uara < -Papamuri_uara) return -22;
        kōnae_tūranga[기술] = Papamuri_uara + OFFSET_uara;
        return kōnae_tūranga[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean tautapa_uara, int Ngā_Tautuhinga) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return tautapa_uara ? -9 : -22;
        if (tautapa_uara && 서술자 == 새서술자) return 새서술자;
        if (tautapa_uara) { if (tiwhikete_raweke[새서술자] != 0) kati_kōnae(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        tiwhikete_raweke[새서술자] = 기술 + 1; 서술자설정[새서술자] = Ngā_Tautuhinga; Pūranga_kōrero_COUNT[기술]++;
        return 새서술자;
    }
    static int tango_kōnae_tāurunga_ingoa(int ingoa_ADDRESS) {
        int roa_uara = 경로읽기(ingoa_ADDRESS);
        if (roa_uara < 0) return roa_uara;
        int Kōnae = Pūmahara_pūnaha_kōnae.FIND_tāurunga(ara_ingoa, roa_uara);
        if (Kōnae < 0) return Kōnae;
        Pūmahara_pūnaha_kōnae.이름들[Kōnae * 64] = 0;
        return 0;
    }
    static int huinga_kōnae_roa(int 서술자, int roa_uara) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (tiwhikete_Ngā_Tautuhinga[기술] & 3) == 0 || roa_uara < 0) return -22;
        if (roa_uara > Pūmahara_pūnaha_kōnae.최대크기) return -27;
        int Kōnae = ūnga[기술], ADDRESS = pūkoro_uara.kōnae_Pūmahara() + Kōnae * Pūmahara_pūnaha_kōnae.최대크기;
        for (int INDEX = Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae]; INDEX < roa_uara; INDEX++) pūkoro_uara.tuhi_Pūmahara(ADDRESS + INDEX, 0);
        Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae] = roa_uara;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ADDRESS) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.topenga(ADDRESS, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(ADDRESS + INDEX * 4, 0);
        int Kōnae = ūnga[기술], rahi = 종류[기술] == 2 ? Pūmahara_pūnaha_kōnae.rahi_Rārangi[Kōnae] : 0;
        int 허가 = 종류[기술] == 2 ? Pūmahara_pūnaha_kōnae.허가들[Kōnae] : 438;
        실행관리.수쓰기(ADDRESS, 1);
        실행관리.수쓰기(ADDRESS + 4, 종류[기술] == 2 ? Kōnae + 1 : 100 + 기술);
        실행관리.수쓰기(ADDRESS + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(ADDRESS + 12, 종류[기술] == 2 && Pūmahara_pūnaha_kōnae.이름들[Kōnae * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(ADDRESS + 28, rahi); 실행관리.수쓰기(ADDRESS + 32, 512);
        실행관리.수쓰기(ADDRESS + 36, (rahi + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int tono, int uara) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (tono == 0 || tono == 1030) return 서술자복제(서술자, uara, false, tono == 1030 ? 1 : 0);
        if (tono == 1) return 서술자설정[서술자];
        if (tono == 2) { if ((uara & ~1) != 0) return -22; 서술자설정[서술자] = uara; return 0; }
        if (tono == 3) return tiwhikete_Ngā_Tautuhinga[기술];
        if (tono == 4) {
            if ((uara & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            tiwhikete_Ngā_Tautuhinga[기술] = (tiwhikete_Ngā_Tautuhinga[기술] & 3) | (uara & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = putua_raweke();
        if (서술자 < 0 || 기술 < 0) return -24;
        return TŪHONO(서술자, 기술, 3, 0, 읽기쓰기);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ADDRESS_32(int ADDRESS) {
        return pūkoro_uara.기억읽기(ADDRESS) << 24 | pūkoro_uara.기억읽기(ADDRESS + 1) << 16
            | pūkoro_uara.기억읽기(ADDRESS + 2) << 8 | pūkoro_uara.기억읽기(ADDRESS + 3);
    }
    static int taki_ADDRESS(int ADDRESS, int roa_uara) {
        if (roa_uara < 16) return -22;
        if (!실행관리.topenga(ADDRESS, 16)) return -14;
        return 실행관리.짧은수(ADDRESS) == 2 ? 0 : -97;
    }
    static int BIND_ADDRESS(int 서술자, int ADDRESS, int roa_uara) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int mēhua = taki_ADDRESS(ADDRESS, roa_uara);
        if (mēhua < 0) return mēhua;
        if (whatunga_raweke[기술] != 0) return -22;
        int whatunga_ADDRESS = ADDRESS_32(ADDRESS + 4);
        if (whatunga_ADDRESS != 0 && whatunga_ADDRESS != whatunga_Huinga.내주소) return -99;
        int 접속번호 = pūkoro_uara.기억읽기(ADDRESS + 2) << 8 | pūkoro_uara.기억읽기(ADDRESS + 3);
        mēhua = whatunga_Huinga.Huaki(접속번호);
        if (mēhua < 0) return mēhua;
        whatunga_raweke[기술] = mēhua; ūnga[기술] = whatunga_ADDRESS;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (whatunga_raweke[기술] != 0) return 0;
        int mēhua = whatunga_Huinga.Huaki(0);
        if (mēhua < 0) return mēhua;
        whatunga_raweke[기술] = mēhua;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int raraunga_ADDRESS, int roa_uara, int Ngā_Tautuhinga, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Ngā_Tautuhinga != 0) return -95;
        if (roa_uara < 0 || roa_uara > 1024) return -90;
        if (roa_uara != 0 && !실행관리.topenga(raraunga_ADDRESS, roa_uara)) return -14;
        if (!실행관리.topenga(요청주소, 8)) return -14;
        int ADDRESS = 실행관리.수(요청주소);
        int mēhua = taki_ADDRESS(ADDRESS, 실행관리.수(요청주소 + 4));
        if (mēhua < 0) return mēhua;
        int 접속번호 = pūkoro_uara.기억읽기(ADDRESS + 2) << 8 | pūkoro_uara.기억읽기(ADDRESS + 3);
        if (접속번호 == 0) return -22;
        mēhua = 자동묶기(기술);
        if (mēhua < 0) return mēhua;
        for (int INDEX = 0; INDEX < roa_uara; INDEX++) whakawhiti_raraunga[INDEX] = pūkoro_uara.기억읽기(raraunga_ADDRESS + INDEX);
        return whatunga_Huinga.tuku(whatunga_raweke[기술], ADDRESS_32(ADDRESS + 4), 접속번호, whakawhiti_raraunga, roa_uara);
    }
    static void tuhi_ADDRESS(int ADDRESS, int roa_uara, int whatunga_ADDRESS, int 접속번호) {
        for (int INDEX = 0; INDEX < roa_uara && INDEX < 16; INDEX++) {
            int uara = 0;
            if (INDEX == 0) uara = 2;
            if (INDEX == 2) uara = 접속번호 >>> 8;
            if (INDEX == 3) uara = 접속번호;
            if (INDEX >= 4 && INDEX < 8) uara = whatunga_ADDRESS >>> (56 - INDEX * 8);
            pūkoro_uara.tuhi_Pūmahara(ADDRESS + INDEX, uara & 255);
        }
    }
    static int 자료전문받기(int 서술자, int raraunga_ADDRESS, int roa_uara, int Ngā_Tautuhinga, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Ngā_Tautuhinga & ~64) != 0) return -95;
        if (roa_uara < 0) return -22;
        if (roa_uara != 0 && !실행관리.topenga(raraunga_ADDRESS, roa_uara)) return -14;
        int ADDRESS = 0, ADDRESS_roa_ADDRESS = 0, ADDRESS_roa = 0;
        if (요청주소 != 0) {
            if (!실행관리.topenga(요청주소, 8)) return -14;
            ADDRESS = 실행관리.수(요청주소); ADDRESS_roa_ADDRESS = 실행관리.수(요청주소 + 4);
            if (ADDRESS != 0) {
                if (!실행관리.topenga(ADDRESS_roa_ADDRESS, 4)) return -14;
                ADDRESS_roa = 실행관리.수(ADDRESS_roa_ADDRESS);
                if (ADDRESS_roa < 0) return -22;
                if (!실행관리.topenga(ADDRESS, ADDRESS_roa < 16 ? ADDRESS_roa : 16)) return -14;
            }
        }
        int mēhua = 자동묶기(기술);
        if (mēhua < 0) return mēhua;
        int whakahaere = pūkoro_uara.밀리초();
        while (true) {
            mēhua = whatunga_Huinga.받기(whatunga_raweke[기술], whakawhiti_raraunga, 1024, 0);
            if (mēhua != -11) break;
            if ((Ngā_Tautuhinga & 64) != 0 || (tiwhikete_Ngā_Tautuhinga[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && pūkoro_uara.밀리초() - whakahaere >= 수신대기밀리초[기술]) return -11;
            if (pūkoro_uara.사용자남은밀리초() <= 10) return -11;
            pūkoro_uara.잠시양보();
        }
        if (mēhua < 0) return mēhua;
        if (mēhua > roa_uara) mēhua = roa_uara;
        for (int INDEX = 0; INDEX < mēhua; INDEX++) pūkoro_uara.tuhi_Pūmahara(raraunga_ADDRESS + INDEX, whakawhiti_raraunga[INDEX]);
        if (ADDRESS != 0) {
            tuhi_ADDRESS(ADDRESS, ADDRESS_roa, whatunga_Huinga.hoa_ADDRESS(whatunga_raweke[기술]), whatunga_Huinga.상대접속번호(whatunga_raweke[기술]));
            실행관리.수쓰기(ADDRESS_roa_ADDRESS, 16);
        }
        return mēhua;
    }
    static int 통신주소읽기(int 서술자, int ADDRESS, int roa_ADDRESS) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.topenga(roa_ADDRESS, 4)) return -14;
        int roa_uara = 실행관리.수(roa_ADDRESS);
        if (roa_uara < 0) return -22;
        if (!실행관리.topenga(ADDRESS, roa_uara < 16 ? roa_uara : 16)) return -14;
        int kāniwha_tāurunga = whatunga_Huinga.INDEX(whatunga_raweke[기술]);
        tuhi_ADDRESS(ADDRESS, roa_uara, ūnga[기술], kāniwha_tāurunga < 0 ? 0 : whatunga_Huinga.접속번호들[kāniwha_tāurunga]);
        실행관리.수쓰기(roa_ADDRESS, 16);
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
