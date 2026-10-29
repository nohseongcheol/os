// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 erabiltzaile 과정의 파일서술자와 열린 Fitxategia 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int irakurri_idatzi_marka = 2, sortu_sarrera = 64, 독점생성 = 128, garbitu_Edukia = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] ireki_helduleku = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], helburu_balio = new int[서술자한도];
    static int[] fitxategi_kargu = new int[서술자한도], ireki_Ezarpenak = new int[서술자한도], Erreferentzia_materiala_ZENBATU = new int[서술자한도];
    static int[] sare_helduleku = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] bide_izen_izen = new int[64], transferitu_datuak = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return ireki_helduleku[파일서술자] - 1;
    }
    static int 빈서술자(int Exekutatu_2) {
        for (int INDIZE = Exekutatu_2; INDIZE < 서술자한도; INDIZE++) if (ireki_helduleku[INDIZE] == 0) return INDIZE;
        return -24;
    }
    static int 빈기술() {
        for (int INDIZE = 0; INDIZE < 서술자한도; INDIZE++) if (Erreferentzia_materiala_ZENBATU[INDIZE] == 0) return INDIZE;
        return -24;
    }
    static int Konektatu(int 서술자, int 기술, int 파일종류, int fitxategi_helburu_balio, int Ezarpenak) {
        ireki_helduleku[서술자] = 기술 + 1; 서술자설정[서술자] = (Ezarpenak & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; helburu_balio[기술] = fitxategi_helburu_balio; Erreferentzia_materiala_ZENBATU[기술] = 1;
        ireki_Ezarpenak[기술] = Ezarpenak & (3 | 이어쓰기 | 기다리지않기); fitxategi_kargu[기술] = 0;
        sare_helduleku[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void HASI_prozesu() {
        GARBITU_prozesu();
        for (int INDIZE = 0; INDIZE < 3; INDIZE++) Konektatu(INDIZE, INDIZE, 1, INDIZE, INDIZE == 0 ? 0 : 1);
    }
    static void GARBITU_prozesu() {
        for (int INDIZE = 0; INDIZE < 서술자한도; INDIZE++) if (ireki_helduleku[INDIZE] != 0) itxi_fitxategi(INDIZE);
    }
    static int itxi_fitxategi(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        ireki_helduleku[서술자] = 0; 서술자설정[서술자] = 0;
        Erreferentzia_materiala_ZENBATU[기술]--;
        if (Erreferentzia_materiala_ZENBATU[기술] == 0) {
            if (종류[기술] == 2) Memoria_fitxategi_sistema.ireki_ZENBATU[helburu_balio[기술]]--;
            if (종류[기술] == 3 && sare_helduleku[기술] != 0) sare_pila.Itxi(sare_helduleku[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_balio 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int helbide) {
        if (!실행관리.klip(helbide, 1)) return -14;
        int Posizioa = gailu_balio.기억읽기(helbide) == '/' ? 1 : 0;
        for (int luzera_balio = 0; luzera_balio < 64; luzera_balio++) {
            if (!실행관리.klip(helbide + Posizioa + luzera_balio, 1)) return -14;
            int balio = gailu_balio.기억읽기(helbide + Posizioa + luzera_balio);
            bide_izen_izen[luzera_balio] = balio;
            if (balio == 0) return luzera_balio == 0 ? -2 : (Memoria_fitxategi_sistema.txeke_izen(bide_izen_izen, luzera_balio) ? luzera_balio : -22);
            if (balio == '/') return -20;
        }
        return -36;
    }
    static int ireki_fitxategi(int izen_helbide, int Ezarpenak, int 허가) {
        int luzera_balio = 경로읽기(izen_helbide);
        if (luzera_balio < 0) return luzera_balio;
        if ((Ezarpenak & ~(3 | sortu_sarrera | 독점생성 | garbitu_Edukia | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Ezarpenak & 3) == 3 || ((Ezarpenak & garbitu_Edukia) != 0 && (Ezarpenak & 3) == 0)) return -22;
        int Fitxategia = Memoria_fitxategi_sistema.Bilatu_sarrera(bide_izen_izen, luzera_balio);
        if (Fitxategia >= 0 && (Ezarpenak & (sortu_sarrera | 독점생성)) == (sortu_sarrera | 독점생성)) return -17;
        if (Fitxategia == -2 && (Ezarpenak & sortu_sarrera) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fitxategia == -2) {
            int EMAITZA = Memoria_fitxategi_sistema.Store_balio(bide_izen_izen, luzera_balio, bide_izen_izen, 0);
            if (EMAITZA < 0) return EMAITZA;
            Fitxategia = Memoria_fitxategi_sistema.Bilatu_sarrera(bide_izen_izen, luzera_balio);
            Memoria_fitxategi_sistema.허가들[Fitxategia] = 허가 & 511;
        }
        if (Fitxategia < 0) return Fitxategia;
        if ((Ezarpenak & garbitu_Edukia) != 0) Memoria_fitxategi_sistema.크기들[Fitxategia] = 0;
        Memoria_fitxategi_sistema.ireki_ZENBATU[Fitxategia]++;
        return Konektatu(서술자, 기술, 2, Fitxategia, Ezarpenak);
    }
    static int 파일읽기(int 서술자, int datuak_helbide, int luzera_balio) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (ireki_Ezarpenak[기술] & 3) == 1) return -9;
        if (luzera_balio < 0) return -22;
        if (luzera_balio == 0) return 0;
        if (!실행관리.klip(datuak_helbide, luzera_balio)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, datuak_helbide, luzera_balio, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_ZENBATU = 0;
            while (RECEIVED_ZENBATU < luzera_balio) {
                int balio = SMS_Terminal.직렬읽기();
                if (balio < 0) balio = teklatu.Irakurri();
                if (balio < 0) {
                    if (RECEIVED_ZENBATU > 0) return RECEIVED_ZENBATU;
                    if ((ireki_Ezarpenak[기술] & 기다리지않기) != 0) return -11;
                    if (gailu_balio.사용자남은밀리초() <= 10) return -11;
                    sare_pila.egiaztatu(); gailu_balio.잠시양보();
                } else {
                    gailu_balio.idatzi_Memoria(datuak_helbide + RECEIVED_ZENBATU, balio); RECEIVED_ZENBATU++;
                }
            }
            return RECEIVED_ZENBATU;
        }
        int Fitxategia = helburu_balio[기술], Posizioa = fitxategi_kargu[기술];
        if (Posizioa >= Memoria_fitxategi_sistema.크기들[Fitxategia]) return 0;
        if (luzera_balio > Memoria_fitxategi_sistema.크기들[Fitxategia] - Posizioa) luzera_balio = Memoria_fitxategi_sistema.크기들[Fitxategia] - Posizioa;
        int 원본주소 = gailu_balio.fitxategi_Memoria() + Fitxategia * Memoria_fitxategi_sistema.최대크기 + Posizioa;
        for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) gailu_balio.idatzi_Memoria(datuak_helbide + INDIZE, gailu_balio.기억읽기(원본주소 + INDIZE));
        fitxategi_kargu[기술] += luzera_balio;
        return luzera_balio;
    }
    static int idatzi_fitxategi(int 서술자, int datuak_helbide, int luzera_balio) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (ireki_Ezarpenak[기술] & 3) == 0) return -9;
        if (luzera_balio < 0) return -22;
        if (luzera_balio == 0) return 0;
        if (!실행관리.klip(datuak_helbide, luzera_balio)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 helburu_balio_a0fbc067 주소가 필요하다.
        if (종류[기술] == 1) {
            if (luzera_balio > 16384) luzera_balio = 16384;
            for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) {
                int balio = gailu_balio.기억읽기(datuak_helbide + INDIZE);
                SMS_Terminal.직렬바이트(balio); SMS_Terminal.화면문자(balio);
            }
            return luzera_balio;
        }
        int Fitxategia = helburu_balio[기술], Tamaina = Memoria_fitxategi_sistema.크기들[Fitxategia];
        int Posizioa = (ireki_Ezarpenak[기술] & 이어쓰기) != 0 ? Tamaina : fitxategi_kargu[기술];
        if (Posizioa >= Memoria_fitxategi_sistema.최대크기) return -27;
        if (luzera_balio > Memoria_fitxategi_sistema.최대크기 - Posizioa) luzera_balio = Memoria_fitxategi_sistema.최대크기 - Posizioa;
        int helburu_helbide_08bbd577 = gailu_balio.fitxategi_Memoria() + Fitxategia * Memoria_fitxategi_sistema.최대크기;
        for (int INDIZE = Tamaina; INDIZE < Posizioa; INDIZE++) gailu_balio.idatzi_Memoria(helburu_helbide_08bbd577 + INDIZE, 0);
        for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) gailu_balio.idatzi_Memoria(helburu_helbide_08bbd577 + Posizioa + INDIZE, gailu_balio.기억읽기(datuak_helbide + INDIZE));
        fitxategi_kargu[기술] = Posizioa + luzera_balio;
        if (Posizioa + luzera_balio > Tamaina) Memoria_fitxategi_sistema.크기들[Fitxategia] = Posizioa + luzera_balio;
        return luzera_balio;
    }
    static int bilatu_fitxategi(int 서술자, int Geruzak_balio, int Project_erro) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_erro < 0 || Project_erro > 2) return -22;
        int horma_paper_balio = Project_erro == 0 ? 0 : (Project_erro == 1 ? fitxategi_kargu[기술] : Memoria_fitxategi_sistema.크기들[helburu_balio[기술]]);
        if (Geruzak_balio > 0 && horma_paper_balio > 2147483647 - Geruzak_balio) return -75;
        if (Geruzak_balio < 0 && Geruzak_balio < -horma_paper_balio) return -22;
        fitxategi_kargu[기술] = horma_paper_balio + Geruzak_balio;
        return fitxategi_kargu[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Esleitu_balio, int Ezarpenak) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Esleitu_balio ? -9 : -22;
        if (Esleitu_balio && 서술자 == 새서술자) return 새서술자;
        if (Esleitu_balio) { if (ireki_helduleku[새서술자] != 0) itxi_fitxategi(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        ireki_helduleku[새서술자] = 기술 + 1; 서술자설정[새서술자] = Ezarpenak; Erreferentzia_materiala_ZENBATU[기술]++;
        return 새서술자;
    }
    static int kendu_fitxategi_sarrera_izen(int izen_helbide) {
        int luzera_balio = 경로읽기(izen_helbide);
        if (luzera_balio < 0) return luzera_balio;
        int Fitxategia = Memoria_fitxategi_sistema.Bilatu_sarrera(bide_izen_izen, luzera_balio);
        if (Fitxategia < 0) return Fitxategia;
        Memoria_fitxategi_sistema.이름들[Fitxategia * 64] = 0;
        return 0;
    }
    static int sorta_fitxategi_luzera(int 서술자, int luzera_balio) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (ireki_Ezarpenak[기술] & 3) == 0 || luzera_balio < 0) return -22;
        if (luzera_balio > Memoria_fitxategi_sistema.최대크기) return -27;
        int Fitxategia = helburu_balio[기술], helbide = gailu_balio.fitxategi_Memoria() + Fitxategia * Memoria_fitxategi_sistema.최대크기;
        for (int INDIZE = Memoria_fitxategi_sistema.크기들[Fitxategia]; INDIZE < luzera_balio; INDIZE++) gailu_balio.idatzi_Memoria(helbide + INDIZE, 0);
        Memoria_fitxategi_sistema.크기들[Fitxategia] = luzera_balio;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int helbide) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klip(helbide, 48)) return -14;
        for (int INDIZE = 0; INDIZE < 12; INDIZE++) 실행관리.수쓰기(helbide + INDIZE * 4, 0);
        int Fitxategia = helburu_balio[기술], Tamaina = 종류[기술] == 2 ? Memoria_fitxategi_sistema.크기들[Fitxategia] : 0;
        int 허가 = 종류[기술] == 2 ? Memoria_fitxategi_sistema.허가들[Fitxategia] : 438;
        실행관리.수쓰기(helbide, 1);
        실행관리.수쓰기(helbide + 4, 종류[기술] == 2 ? Fitxategia + 1 : 100 + 기술);
        실행관리.수쓰기(helbide + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(helbide + 12, 종류[기술] == 2 && Memoria_fitxategi_sistema.이름들[Fitxategia * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(helbide + 28, Tamaina); 실행관리.수쓰기(helbide + 32, 512);
        실행관리.수쓰기(helbide + 36, (Tamaina + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Komandoa, int balio) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Komandoa == 0 || Komandoa == 1030) return 서술자복제(서술자, balio, false, Komandoa == 1030 ? 1 : 0);
        if (Komandoa == 1) return 서술자설정[서술자];
        if (Komandoa == 2) { if ((balio & ~1) != 0) return -22; 서술자설정[서술자] = balio; return 0; }
        if (Komandoa == 3) return ireki_Ezarpenak[기술];
        if (Komandoa == 4) {
            if ((balio & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            ireki_Ezarpenak[기술] = (ireki_Ezarpenak[기술] & 3) | (balio & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int sortu_amaiera_puntu(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Konektatu(서술자, 기술, 3, 0, irakurri_idatzi_marka);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int helbide_32(int helbide) {
        return gailu_balio.기억읽기(helbide) << 24 | gailu_balio.기억읽기(helbide + 1) << 16
            | gailu_balio.기억읽기(helbide + 2) << 8 | gailu_balio.기억읽기(helbide + 3);
    }
    static int txeke_helbide(int helbide, int luzera_balio) {
        if (luzera_balio < 16) return -22;
        if (!실행관리.klip(helbide, 16)) return -14;
        return 실행관리.짧은수(helbide) == 2 ? 0 : -97;
    }
    static int lotu_helbide(int 서술자, int helbide, int luzera_balio) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int EMAITZA = txeke_helbide(helbide, luzera_balio);
        if (EMAITZA < 0) return EMAITZA;
        if (sare_helduleku[기술] != 0) return -22;
        int sare_helbide = helbide_32(helbide + 4);
        if (sare_helbide != 0 && sare_helbide != sare_pila.내주소) return -99;
        int ataka_zenbaki = gailu_balio.기억읽기(helbide + 2) << 8 | gailu_balio.기억읽기(helbide + 3);
        EMAITZA = sare_pila.Ireki(ataka_zenbaki);
        if (EMAITZA < 0) return EMAITZA;
        sare_helduleku[기술] = EMAITZA; helburu_balio[기술] = sare_helbide;
        return 0;
    }
    static int Automatikoa_lotu(int 기술) {
        if (sare_helduleku[기술] != 0) return 0;
        int EMAITZA = sare_pila.Ireki(0);
        if (EMAITZA < 0) return EMAITZA;
        sare_helduleku[기술] = EMAITZA;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 eskaera 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int datuak_helbide, int luzera_balio, int Ezarpenak, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Ezarpenak != 0) return -95;
        if (luzera_balio < 0 || luzera_balio > 1024) return -90;
        if (luzera_balio != 0 && !실행관리.klip(datuak_helbide, luzera_balio)) return -14;
        if (!실행관리.klip(요청주소, 8)) return -14;
        int helbide = 실행관리.수(요청주소);
        int EMAITZA = txeke_helbide(helbide, 실행관리.수(요청주소 + 4));
        if (EMAITZA < 0) return EMAITZA;
        int ataka_zenbaki = gailu_balio.기억읽기(helbide + 2) << 8 | gailu_balio.기억읽기(helbide + 3);
        if (ataka_zenbaki == 0) return -22;
        EMAITZA = Automatikoa_lotu(기술);
        if (EMAITZA < 0) return EMAITZA;
        for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) transferitu_datuak[INDIZE] = gailu_balio.기억읽기(datuak_helbide + INDIZE);
        return sare_pila.bidali(sare_helduleku[기술], helbide_32(helbide + 4), ataka_zenbaki, transferitu_datuak, luzera_balio);
    }
    static void idatzi_helbide(int helbide, int luzera_balio, int sare_helbide, int ataka_zenbaki) {
        for (int INDIZE = 0; INDIZE < luzera_balio && INDIZE < 16; INDIZE++) {
            int balio = 0;
            if (INDIZE == 0) balio = 2;
            if (INDIZE == 2) balio = ataka_zenbaki >>> 8;
            if (INDIZE == 3) balio = ataka_zenbaki;
            if (INDIZE >= 4 && INDIZE < 8) balio = sare_helbide >>> (56 - INDIZE * 8);
            gailu_balio.idatzi_Memoria(helbide + INDIZE, balio & 255);
        }
    }
    static int 자료전문받기(int 서술자, int datuak_helbide, int luzera_balio, int Ezarpenak, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Ezarpenak & ~64) != 0) return -95;
        if (luzera_balio < 0) return -22;
        if (luzera_balio != 0 && !실행관리.klip(datuak_helbide, luzera_balio)) return -14;
        int helbide = 0, helbide_luzera_helbide = 0, helbide_luzera = 0;
        if (요청주소 != 0) {
            if (!실행관리.klip(요청주소, 8)) return -14;
            helbide = 실행관리.수(요청주소); helbide_luzera_helbide = 실행관리.수(요청주소 + 4);
            if (helbide != 0) {
                if (!실행관리.klip(helbide_luzera_helbide, 4)) return -14;
                helbide_luzera = 실행관리.수(helbide_luzera_helbide);
                if (helbide_luzera < 0) return -22;
                if (!실행관리.klip(helbide, helbide_luzera < 16 ? helbide_luzera : 16)) return -14;
            }
        }
        int EMAITZA = Automatikoa_lotu(기술);
        if (EMAITZA < 0) return EMAITZA;
        int Exekutatu_2 = gailu_balio.밀리초();
        while (true) {
            EMAITZA = sare_pila.받기(sare_helduleku[기술], transferitu_datuak, 1024, 0);
            if (EMAITZA != -11) break;
            if ((Ezarpenak & 64) != 0 || (ireki_Ezarpenak[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && gailu_balio.밀리초() - Exekutatu_2 >= 수신대기밀리초[기술]) return -11;
            if (gailu_balio.사용자남은밀리초() <= 10) return -11;
            gailu_balio.잠시양보();
        }
        if (EMAITZA < 0) return EMAITZA;
        if (EMAITZA > luzera_balio) EMAITZA = luzera_balio;
        for (int INDIZE = 0; INDIZE < EMAITZA; INDIZE++) gailu_balio.idatzi_Memoria(datuak_helbide + INDIZE, transferitu_datuak[INDIZE]);
        if (helbide != 0) {
            idatzi_helbide(helbide, helbide_luzera, sare_pila.pareko_helbide(sare_helduleku[기술]), sare_pila.pareko_ataka_zenbaki(sare_helduleku[기술]));
            실행관리.수쓰기(helbide_luzera_helbide, 16);
        }
        return EMAITZA;
    }
    static int 통신주소읽기(int 서술자, int helbide, int luzera_helbide) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klip(luzera_helbide, 4)) return -14;
        int luzera_balio = 실행관리.수(luzera_helbide);
        if (luzera_balio < 0) return -22;
        if (!실행관리.klip(helbide, luzera_balio < 16 ? luzera_balio : 16)) return -14;
        int 칸 = sare_pila.INDIZE(sare_helduleku[기술]);
        idatzi_helbide(helbide, luzera_balio, helburu_balio[기술], 칸 < 0 ? 0 : sare_pila.접속번호들[칸]);
        실행관리.수쓰기(luzera_helbide, 16);
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
