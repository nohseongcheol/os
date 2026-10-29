// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 ulanyjy 과정의 파일서술자와 열린 Faýl 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int okalýan_ýazylýan_alamat_goý = 2, döretmek_girizmeklik = 64, 독점생성 = 128, arassala_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] aç_ryçag = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], niýet = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], aç_Sazlamalar = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] Tor_ryçag = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] ýol_at = new int[64], geçir_maglumat = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return aç_ryçag[파일서술자] - 1;
    }
    static int 빈서술자(int Bitir) {
        for (int indeks = Bitir; indeks < 서술자한도; indeks++) if (aç_ryçag[indeks] == 0) return indeks;
        return -24;
    }
    static int boş_ryçag() {
        for (int indeks = 0; indeks < 서술자한도; indeks++) if (참조수[indeks] == 0) return indeks;
        return -24;
    }
    static int Birikme(int 서술자, int 기술, int 파일종류, int faýl_niýet, int Düzümler) {
        aç_ryçag[서술자] = 기술 + 1; 서술자설정[서술자] = (Düzümler & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; niýet[기술] = faýl_niýet; 참조수[기술] = 1;
        aç_Sazlamalar[기술] = Düzümler & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        Tor_ryçag[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void başlat_Proses() {
        Päkize_Proses();
        for (int indeks = 0; indeks < 3; indeks++) Birikme(indeks, indeks, 1, indeks, indeks == 0 ? 0 : 1);
    }
    static void Päkize_Proses() {
        for (int indeks = 0; indeks < 서술자한도; indeks++) if (aç_ryçag[indeks] != 0) ýap_faýl(indeks);
    }
    static int ýap_faýl(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        aç_ryçag[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) ýat_faýl_ulgamy.열림수[niýet[기술]]--;
            if (종류[기술] == 3 && Tor_ryçag[기술] != 0) Tor_Desse.Ýap(Tor_ryçag[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 baýt_baha 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int salgy) {
        if (!실행관리.klip(salgy, 1)) return -14;
        int 위치 = enjam_baha.기억읽기(salgy) == '/' ? 1 : 0;
        for (int dowamlylyk_baha = 0; dowamlylyk_baha < 64; dowamlylyk_baha++) {
            if (!실행관리.klip(salgy + 위치 + dowamlylyk_baha, 1)) return -14;
            int baha = enjam_baha.기억읽기(salgy + 위치 + dowamlylyk_baha);
            ýol_at[dowamlylyk_baha] = baha;
            if (baha == 0) return dowamlylyk_baha == 0 ? -2 : (ýat_faýl_ulgamy.derňe_at(ýol_at, dowamlylyk_baha) ? dowamlylyk_baha : -22);
            if (baha == '/') return -20;
        }
        return -36;
    }
    static int aç_faýl(int at_salgy, int Düzümler, int 허가) {
        int dowamlylyk_baha = 경로읽기(at_salgy);
        if (dowamlylyk_baha < 0) return dowamlylyk_baha;
        if ((Düzümler & ~(3 | döretmek_girizmeklik | 독점생성 | arassala_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Düzümler & 3) == 3 || ((Düzümler & arassala_TOC) != 0 && (Düzümler & 3) == 0)) return -22;
        int Faýl = ýat_faýl_ulgamy.tap_girizmeklik(ýol_at, dowamlylyk_baha);
        if (Faýl >= 0 && (Düzümler & (döretmek_girizmeklik | 독점생성)) == (döretmek_girizmeklik | 독점생성)) return -17;
        if (Faýl == -2 && (Düzümler & döretmek_girizmeklik) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = boş_ryçag();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Faýl == -2) {
            int 결과 = ýat_faýl_ulgamy.Store_baha(ýol_at, dowamlylyk_baha, ýol_at, 0);
            if (결과 < 0) return 결과;
            Faýl = ýat_faýl_ulgamy.tap_girizmeklik(ýol_at, dowamlylyk_baha);
            ýat_faýl_ulgamy.허가들[Faýl] = 허가 & 511;
        }
        if (Faýl < 0) return Faýl;
        if ((Düzümler & arassala_TOC) != 0) ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl] = 0;
        ýat_faýl_ulgamy.열림수[Faýl]++;
        return Birikme(서술자, 기술, 2, Faýl, Düzümler);
    }
    static int 파일읽기(int 서술자, int maglumat_salgy, int dowamlylyk_baha) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (aç_Sazlamalar[기술] & 3) == 1) return -9;
        if (dowamlylyk_baha < 0) return -22;
        if (dowamlylyk_baha == 0) return 0;
        if (!실행관리.klip(maglumat_salgy, dowamlylyk_baha)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, maglumat_salgy, dowamlylyk_baha, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < dowamlylyk_baha) {
                int baha = 문자단말.직렬읽기();
                if (baha < 0) baha = klawiatura.Oka();
                if (baha < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((aç_Sazlamalar[기술] & 기다리지않기) != 0) return -11;
                    if (enjam_baha.사용자남은밀리초() <= 10) return -11;
                    Tor_Desse.barla(); enjam_baha.잠시양보();
                } else {
                    enjam_baha.ýaz_ýat(maglumat_salgy + 받은수, baha); 받은수++;
                }
            }
            return 받은수;
        }
        int Faýl = niýet[기술], 위치 = 파일위치[기술];
        if (위치 >= ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl]) return 0;
        if (dowamlylyk_baha > ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl] - 위치) dowamlylyk_baha = ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl] - 위치;
        int 원본주소 = enjam_baha.faýl_ýat() + Faýl * ýat_faýl_ulgamy.최대크기 + 위치;
        for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) enjam_baha.ýaz_ýat(maglumat_salgy + indeks, enjam_baha.기억읽기(원본주소 + indeks));
        파일위치[기술] += dowamlylyk_baha;
        return dowamlylyk_baha;
    }
    static int ýaz_faýl(int 서술자, int maglumat_salgy, int dowamlylyk_baha) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (aç_Sazlamalar[기술] & 3) == 0) return -9;
        if (dowamlylyk_baha < 0) return -22;
        if (dowamlylyk_baha == 0) return 0;
        if (!실행관리.klip(maglumat_salgy, dowamlylyk_baha)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 barylmaly_ýer_baha 주소가 필요하다.
        if (종류[기술] == 1) {
            if (dowamlylyk_baha > 16384) dowamlylyk_baha = 16384;
            for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) {
                int baha = enjam_baha.기억읽기(maglumat_salgy + indeks);
                문자단말.직렬바이트(baha); 문자단말.화면문자(baha);
            }
            return dowamlylyk_baha;
        }
        int Faýl = niýet[기술], Ululyk = ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl];
        int 위치 = (aç_Sazlamalar[기술] & 이어쓰기) != 0 ? Ululyk : 파일위치[기술];
        if (위치 >= ýat_faýl_ulgamy.최대크기) return -27;
        if (dowamlylyk_baha > ýat_faýl_ulgamy.최대크기 - 위치) dowamlylyk_baha = ýat_faýl_ulgamy.최대크기 - 위치;
        int barylmaly_ýer_salgy = enjam_baha.faýl_ýat() + Faýl * ýat_faýl_ulgamy.최대크기;
        for (int indeks = Ululyk; indeks < 위치; indeks++) enjam_baha.ýaz_ýat(barylmaly_ýer_salgy + indeks, 0);
        for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) enjam_baha.ýaz_ýat(barylmaly_ýer_salgy + 위치 + indeks, enjam_baha.기억읽기(maglumat_salgy + indeks));
        파일위치[기술] = 위치 + dowamlylyk_baha;
        if (위치 + dowamlylyk_baha > Ululyk) ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl] = 위치 + dowamlylyk_baha;
        return dowamlylyk_baha;
    }
    static int gözle_faýl(int 서술자, int Süýşüriş_baha, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int Fon_baha = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[niýet[기술]]);
        if (Süýşüriş_baha > 0 && Fon_baha > 2147483647 - Süýşüriş_baha) return -75;
        if (Süýşüriş_baha < 0 && Süýşüriş_baha < -Fon_baha) return -22;
        파일위치[기술] = Fon_baha + Süýşüriş_baha;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int Düzümler) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (aç_ryçag[새서술자] != 0) ýap_faýl(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        aç_ryçag[새서술자] = 기술 + 1; 서술자설정[새서술자] = Düzümler; 참조수[기술]++;
        return 새서술자;
    }
    static int aýyr_faýl_girizmeklik_at(int at_salgy) {
        int dowamlylyk_baha = 경로읽기(at_salgy);
        if (dowamlylyk_baha < 0) return dowamlylyk_baha;
        int Faýl = ýat_faýl_ulgamy.tap_girizmeklik(ýol_at, dowamlylyk_baha);
        if (Faýl < 0) return Faýl;
        ýat_faýl_ulgamy.이름들[Faýl * 64] = 0;
        return 0;
    }
    static int köplük_faýl_dowamlylyk(int 서술자, int dowamlylyk_baha) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (aç_Sazlamalar[기술] & 3) == 0 || dowamlylyk_baha < 0) return -22;
        if (dowamlylyk_baha > ýat_faýl_ulgamy.최대크기) return -27;
        int Faýl = niýet[기술], salgy = enjam_baha.faýl_ýat() + Faýl * ýat_faýl_ulgamy.최대크기;
        for (int indeks = ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl]; indeks < dowamlylyk_baha; indeks++) enjam_baha.ýaz_ýat(salgy + indeks, 0);
        ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl] = dowamlylyk_baha;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int salgy) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klip(salgy, 48)) return -14;
        for (int indeks = 0; indeks < 12; indeks++) 실행관리.수쓰기(salgy + indeks * 4, 0);
        int Faýl = niýet[기술], Ululyk = 종류[기술] == 2 ? ýat_faýl_ulgamy.ölçegi_üýtget_Sanaw[Faýl] : 0;
        int 허가 = 종류[기술] == 2 ? ýat_faýl_ulgamy.허가들[Faýl] : 438;
        실행관리.수쓰기(salgy, 1);
        실행관리.수쓰기(salgy + 4, 종류[기술] == 2 ? Faýl + 1 : 100 + 기술);
        실행관리.수쓰기(salgy + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(salgy + 12, 종류[기술] == 2 && ýat_faýl_ulgamy.이름들[Faýl * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(salgy + 28, Ululyk); 실행관리.수쓰기(salgy + 32, 512);
        실행관리.수쓰기(salgy + 36, (Ululyk + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int buýruk, int baha) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (buýruk == 0 || buýruk == 1030) return 서술자복제(서술자, baha, false, buýruk == 1030 ? 1 : 0);
        if (buýruk == 1) return 서술자설정[서술자];
        if (buýruk == 2) { if ((baha & ~1) != 0) return -22; 서술자설정[서술자] = baha; return 0; }
        if (buýruk == 3) return aç_Sazlamalar[기술];
        if (buýruk == 4) {
            if ((baha & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            aç_Sazlamalar[기술] = (aç_Sazlamalar[기술] & 3) | (baha & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = boş_ryçag();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Birikme(서술자, 기술, 3, 0, okalýan_ýazylýan_alamat_goý);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int salgy_32(int salgy) {
        return enjam_baha.기억읽기(salgy) << 24 | enjam_baha.기억읽기(salgy + 1) << 16
            | enjam_baha.기억읽기(salgy + 2) << 8 | enjam_baha.기억읽기(salgy + 3);
    }
    static int derňe_salgy(int salgy, int dowamlylyk_baha) {
        if (dowamlylyk_baha < 16) return -22;
        if (!실행관리.klip(salgy, 16)) return -14;
        return 실행관리.짧은수(salgy) == 2 ? 0 : -97;
    }
    static int BIND_salgy(int 서술자, int salgy, int dowamlylyk_baha) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = derňe_salgy(salgy, dowamlylyk_baha);
        if (결과 < 0) return 결과;
        if (Tor_ryçag[기술] != 0) return -22;
        int Tor_salgy = salgy_32(salgy + 4);
        if (Tor_salgy != 0 && Tor_salgy != Tor_Desse.내주소) return -99;
        int 접속번호 = enjam_baha.기억읽기(salgy + 2) << 8 | enjam_baha.기억읽기(salgy + 3);
        결과 = Tor_Desse.Aç(접속번호);
        if (결과 < 0) return 결과;
        Tor_ryçag[기술] = 결과; niýet[기술] = Tor_salgy;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Tor_ryçag[기술] != 0) return 0;
        int 결과 = Tor_Desse.Aç(0);
        if (결과 < 0) return 결과;
        Tor_ryçag[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int maglumat_salgy, int dowamlylyk_baha, int Düzümler, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Düzümler != 0) return -95;
        if (dowamlylyk_baha < 0 || dowamlylyk_baha > 1024) return -90;
        if (dowamlylyk_baha != 0 && !실행관리.klip(maglumat_salgy, dowamlylyk_baha)) return -14;
        if (!실행관리.klip(요청주소, 8)) return -14;
        int salgy = 실행관리.수(요청주소);
        int 결과 = derňe_salgy(salgy, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = enjam_baha.기억읽기(salgy + 2) << 8 | enjam_baha.기억읽기(salgy + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) geçir_maglumat[indeks] = enjam_baha.기억읽기(maglumat_salgy + indeks);
        return Tor_Desse.iber(Tor_ryçag[기술], salgy_32(salgy + 4), 접속번호, geçir_maglumat, dowamlylyk_baha);
    }
    static void ýaz_salgy(int salgy, int dowamlylyk_baha, int Tor_salgy, int 접속번호) {
        for (int indeks = 0; indeks < dowamlylyk_baha && indeks < 16; indeks++) {
            int baha = 0;
            if (indeks == 0) baha = 2;
            if (indeks == 2) baha = 접속번호 >>> 8;
            if (indeks == 3) baha = 접속번호;
            if (indeks >= 4 && indeks < 8) baha = Tor_salgy >>> (56 - indeks * 8);
            enjam_baha.ýaz_ýat(salgy + indeks, baha & 255);
        }
    }
    static int 자료전문받기(int 서술자, int maglumat_salgy, int dowamlylyk_baha, int Düzümler, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Düzümler & ~64) != 0) return -95;
        if (dowamlylyk_baha < 0) return -22;
        if (dowamlylyk_baha != 0 && !실행관리.klip(maglumat_salgy, dowamlylyk_baha)) return -14;
        int salgy = 0, salgy_dowamlylyk_salgy = 0, salgy_dowamlylyk = 0;
        if (요청주소 != 0) {
            if (!실행관리.klip(요청주소, 8)) return -14;
            salgy = 실행관리.수(요청주소); salgy_dowamlylyk_salgy = 실행관리.수(요청주소 + 4);
            if (salgy != 0) {
                if (!실행관리.klip(salgy_dowamlylyk_salgy, 4)) return -14;
                salgy_dowamlylyk = 실행관리.수(salgy_dowamlylyk_salgy);
                if (salgy_dowamlylyk < 0) return -22;
                if (!실행관리.klip(salgy, salgy_dowamlylyk < 16 ? salgy_dowamlylyk : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int Bitir = enjam_baha.밀리초();
        while (true) {
            결과 = Tor_Desse.받기(Tor_ryçag[기술], geçir_maglumat, 1024, 0);
            if (결과 != -11) break;
            if ((Düzümler & 64) != 0 || (aç_Sazlamalar[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && enjam_baha.밀리초() - Bitir >= 수신대기밀리초[기술]) return -11;
            if (enjam_baha.사용자남은밀리초() <= 10) return -11;
            enjam_baha.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > dowamlylyk_baha) 결과 = dowamlylyk_baha;
        for (int indeks = 0; indeks < 결과; indeks++) enjam_baha.ýaz_ýat(maglumat_salgy + indeks, geçir_maglumat[indeks]);
        if (salgy != 0) {
            ýaz_salgy(salgy, salgy_dowamlylyk, Tor_Desse.deň_derejeli_düwün_salgy(Tor_ryçag[기술]), Tor_Desse.상대접속번호(Tor_ryçag[기술]));
            실행관리.수쓰기(salgy_dowamlylyk_salgy, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int salgy, int dowamlylyk_salgy) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klip(dowamlylyk_salgy, 4)) return -14;
        int dowamlylyk_baha = 실행관리.수(dowamlylyk_salgy);
        if (dowamlylyk_baha < 0) return -22;
        if (!실행관리.klip(salgy, dowamlylyk_baha < 16 ? dowamlylyk_baha : 16)) return -14;
        int ýer_girizmeklik = Tor_Desse.indeks(Tor_ryçag[기술]);
        ýaz_salgy(salgy, dowamlylyk_baha, niýet[기술], ýer_girizmeklik < 0 ? 0 : Tor_Desse.접속번호들[ýer_girizmeklik]);
        실행관리.수쓰기(dowamlylyk_salgy, 16);
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
