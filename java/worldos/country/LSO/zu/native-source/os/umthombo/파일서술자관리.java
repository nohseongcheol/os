// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 umsebenzisi 과정의 파일서술자와 열린 Ihele 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int fundeka_bhaleka_iflegi = 2, yakha_okufakwayo = 64, 독점생성 = 128, sula_i_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] vula_isibambo = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], impokophelo = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], vula_Amasethingi = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] iNethiwekhi_isibambo = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] umzila_igama = new int[64], dlulisa_imininingwane = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return vula_isibambo[파일서술자] - 1;
    }
    static int 빈서술자(int Sebenzisa) {
        for (int thola_inkomba = Sebenzisa; thola_inkomba < 서술자한도; thola_inkomba++) if (vula_isibambo[thola_inkomba] == 0) return thola_inkomba;
        return -24;
    }
    static int okungasho_lutho_isibambo() {
        for (int thola_inkomba = 0; thola_inkomba < 서술자한도; thola_inkomba++) if (참조수[thola_inkomba] == 0) return thola_inkomba;
        return -24;
    }
    static int Xhumanisa(int 서술자, int 기술, int 파일종류, int ifayela_impokophelo, int Izinhlelo) {
        vula_isibambo[서술자] = 기술 + 1; 서술자설정[서술자] = (Izinhlelo & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; impokophelo[기술] = ifayela_impokophelo; 참조수[기술] = 1;
        vula_Amasethingi[기술] = Izinhlelo & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        iNethiwekhi_isibambo[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void qala_Inqubo() {
        과정정리();
        for (int thola_inkomba = 0; thola_inkomba < 3; thola_inkomba++) Xhumanisa(thola_inkomba, thola_inkomba, 1, thola_inkomba, thola_inkomba == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int thola_inkomba = 0; thola_inkomba < 서술자한도; thola_inkomba++) if (vula_isibambo[thola_inkomba] != 0) vala_ifayela(thola_inkomba);
    }
    static int vala_ifayela(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        vula_isibambo[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) inkumbulo_isistimu_yefayela.열림수[impokophelo[기술]]--;
            if (종류[기술] == 3 && iNethiwekhi_isibambo[기술] != 0) iNethiwekhi_Isitaki.Vala(iNethiwekhi_isibambo[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 ibhayithi_inani 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ikheli) {
        if (!실행관리.isiqeshana(ikheli, 1)) return -14;
        int 위치 = idivayisi_inani.기억읽기(ikheli) == '/' ? 1 : 0;
        for (int ubude_inani = 0; ubude_inani < 64; ubude_inani++) {
            if (!실행관리.isiqeshana(ikheli + 위치 + ubude_inani, 1)) return -14;
            int inani = idivayisi_inani.기억읽기(ikheli + 위치 + ubude_inani);
            umzila_igama[ubude_inani] = inani;
            if (inani == 0) return ubude_inani == 0 ? -2 : (inkumbulo_isistimu_yefayela.hlola_igama(umzila_igama, ubude_inani) ? ubude_inani : -22);
            if (inani == '/') return -20;
        }
        return -36;
    }
    static int vula_ifayela(int igama_ikheli, int Izinhlelo, int 허가) {
        int ubude_inani = 경로읽기(igama_ikheli);
        if (ubude_inani < 0) return ubude_inani;
        if ((Izinhlelo & ~(3 | yakha_okufakwayo | 독점생성 | sula_i_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Izinhlelo & 3) == 3 || ((Izinhlelo & sula_i_TOC) != 0 && (Izinhlelo & 3) == 0)) return -22;
        int Ihele = inkumbulo_isistimu_yefayela.thola_okufakwayo(umzila_igama, ubude_inani);
        if (Ihele >= 0 && (Izinhlelo & (yakha_okufakwayo | 독점생성)) == (yakha_okufakwayo | 독점생성)) return -17;
        if (Ihele == -2 && (Izinhlelo & yakha_okufakwayo) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = okungasho_lutho_isibambo();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Ihele == -2) {
            int 결과 = inkumbulo_isistimu_yefayela.Store_inani(umzila_igama, ubude_inani, umzila_igama, 0);
            if (결과 < 0) return 결과;
            Ihele = inkumbulo_isistimu_yefayela.thola_okufakwayo(umzila_igama, ubude_inani);
            inkumbulo_isistimu_yefayela.허가들[Ihele] = 허가 & 511;
        }
        if (Ihele < 0) return Ihele;
        if ((Izinhlelo & sula_i_TOC) != 0) inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele] = 0;
        inkumbulo_isistimu_yefayela.열림수[Ihele]++;
        return Xhumanisa(서술자, 기술, 2, Ihele, Izinhlelo);
    }
    static int 파일읽기(int 서술자, int imininingwane_ikheli, int ubude_inani) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (vula_Amasethingi[기술] & 3) == 1) return -9;
        if (ubude_inani < 0) return -22;
        if (ubude_inani == 0) return 0;
        if (!실행관리.isiqeshana(imininingwane_ikheli, ubude_inani)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, imininingwane_ikheli, ubude_inani, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < ubude_inani) {
                int inani = 문자단말.직렬읽기();
                if (inani < 0) inani = ikhibhodi.Funda();
                if (inani < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((vula_Amasethingi[기술] & 기다리지않기) != 0) return -11;
                    if (idivayisi_inani.사용자남은밀리초() <= 10) return -11;
                    iNethiwekhi_Isitaki.qiniseka(); idivayisi_inani.잠시양보();
                } else {
                    idivayisi_inani.bhala_inkumbulo(imininingwane_ikheli + 받은수, inani); 받은수++;
                }
            }
            return 받은수;
        }
        int Ihele = impokophelo[기술], 위치 = 파일위치[기술];
        if (위치 >= inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele]) return 0;
        if (ubude_inani > inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele] - 위치) ubude_inani = inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele] - 위치;
        int 원본주소 = idivayisi_inani.ifayela_inkumbulo() + Ihele * inkumbulo_isistimu_yefayela.최대크기 + 위치;
        for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) idivayisi_inani.bhala_inkumbulo(imininingwane_ikheli + thola_inkomba, idivayisi_inani.기억읽기(원본주소 + thola_inkomba));
        파일위치[기술] += ubude_inani;
        return ubude_inani;
    }
    static int bhala_ifayela(int 서술자, int imininingwane_ikheli, int ubude_inani) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (vula_Amasethingi[기술] & 3) == 0) return -9;
        if (ubude_inani < 0) return -22;
        if (ubude_inani == 0) return 0;
        if (!실행관리.isiqeshana(imininingwane_ikheli, ubude_inani)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 isikhumulo_inani 주소가 필요하다.
        if (종류[기술] == 1) {
            if (ubude_inani > 16384) ubude_inani = 16384;
            for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) {
                int inani = idivayisi_inani.기억읽기(imininingwane_ikheli + thola_inkomba);
                문자단말.직렬바이트(inani); 문자단말.화면문자(inani);
            }
            return ubude_inani;
        }
        int Ihele = impokophelo[기술], Ubungako = inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele];
        int 위치 = (vula_Amasethingi[기술] & 이어쓰기) != 0 ? Ubungako : 파일위치[기술];
        if (위치 >= inkumbulo_isistimu_yefayela.최대크기) return -27;
        if (ubude_inani > inkumbulo_isistimu_yefayela.최대크기 - 위치) ubude_inani = inkumbulo_isistimu_yefayela.최대크기 - 위치;
        int isikhumulo_ikheli = idivayisi_inani.ifayela_inkumbulo() + Ihele * inkumbulo_isistimu_yefayela.최대크기;
        for (int thola_inkomba = Ubungako; thola_inkomba < 위치; thola_inkomba++) idivayisi_inani.bhala_inkumbulo(isikhumulo_ikheli + thola_inkomba, 0);
        for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) idivayisi_inani.bhala_inkumbulo(isikhumulo_ikheli + 위치 + thola_inkomba, idivayisi_inani.기억읽기(imininingwane_ikheli + thola_inkomba));
        파일위치[기술] = 위치 + ubude_inani;
        if (위치 + ubude_inani > Ubungako) inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele] = 위치 + ubude_inani;
        return ubude_inani;
    }
    static int cinga_ifayela(int 서술자, int I_ofisethi_inani, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int ngemuva_inani = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : inkumbulo_isistimu_yefayela.linganisa_Uhlu[impokophelo[기술]]);
        if (I_ofisethi_inani > 0 && ngemuva_inani > 2147483647 - I_ofisethi_inani) return -75;
        if (I_ofisethi_inani < 0 && I_ofisethi_inani < -ngemuva_inani) return -22;
        파일위치[기술] = ngemuva_inani + I_ofisethi_inani;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean yabela_inani, int Izinhlelo) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return yabela_inani ? -9 : -22;
        if (yabela_inani && 서술자 == 새서술자) return 새서술자;
        if (yabela_inani) { if (vula_isibambo[새서술자] != 0) vala_ifayela(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        vula_isibambo[새서술자] = 기술 + 1; 서술자설정[새서술자] = Izinhlelo; 참조수[기술]++;
        return 새서술자;
    }
    static int khipha_ifayela_okufakwayo_igama(int igama_ikheli) {
        int ubude_inani = 경로읽기(igama_ikheli);
        if (ubude_inani < 0) return ubude_inani;
        int Ihele = inkumbulo_isistimu_yefayela.thola_okufakwayo(umzila_igama, ubude_inani);
        if (Ihele < 0) return Ihele;
        inkumbulo_isistimu_yefayela.이름들[Ihele * 64] = 0;
        return 0;
    }
    static int isethi_ifayela_ubude(int 서술자, int ubude_inani) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (vula_Amasethingi[기술] & 3) == 0 || ubude_inani < 0) return -22;
        if (ubude_inani > inkumbulo_isistimu_yefayela.최대크기) return -27;
        int Ihele = impokophelo[기술], ikheli = idivayisi_inani.ifayela_inkumbulo() + Ihele * inkumbulo_isistimu_yefayela.최대크기;
        for (int thola_inkomba = inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele]; thola_inkomba < ubude_inani; thola_inkomba++) idivayisi_inani.bhala_inkumbulo(ikheli + thola_inkomba, 0);
        inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele] = ubude_inani;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ikheli) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.isiqeshana(ikheli, 48)) return -14;
        for (int thola_inkomba = 0; thola_inkomba < 12; thola_inkomba++) 실행관리.수쓰기(ikheli + thola_inkomba * 4, 0);
        int Ihele = impokophelo[기술], Ubungako = 종류[기술] == 2 ? inkumbulo_isistimu_yefayela.linganisa_Uhlu[Ihele] : 0;
        int 허가 = 종류[기술] == 2 ? inkumbulo_isistimu_yefayela.허가들[Ihele] : 438;
        실행관리.수쓰기(ikheli, 1);
        실행관리.수쓰기(ikheli + 4, 종류[기술] == 2 ? Ihele + 1 : 100 + 기술);
        실행관리.수쓰기(ikheli + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(ikheli + 12, 종류[기술] == 2 && inkumbulo_isistimu_yefayela.이름들[Ihele * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(ikheli + 28, Ubungako); 실행관리.수쓰기(ikheli + 32, 512);
        실행관리.수쓰기(ikheli + 36, (Ubungako + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Umlayelo, int inani) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Umlayelo == 0 || Umlayelo == 1030) return 서술자복제(서술자, inani, false, Umlayelo == 1030 ? 1 : 0);
        if (Umlayelo == 1) return 서술자설정[서술자];
        if (Umlayelo == 2) { if ((inani & ~1) != 0) return -22; 서술자설정[서술자] = inani; return 0; }
        if (Umlayelo == 3) return vula_Amasethingi[기술];
        if (Umlayelo == 4) {
            if ((inani & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            vula_Amasethingi[기술] = (vula_Amasethingi[기술] & 3) | (inani & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = okungasho_lutho_isibambo();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Xhumanisa(서술자, 기술, 3, 0, fundeka_bhaleka_iflegi);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ikheli_32(int ikheli) {
        return idivayisi_inani.기억읽기(ikheli) << 24 | idivayisi_inani.기억읽기(ikheli + 1) << 16
            | idivayisi_inani.기억읽기(ikheli + 2) << 8 | idivayisi_inani.기억읽기(ikheli + 3);
    }
    static int hlola_ikheli(int ikheli, int ubude_inani) {
        if (ubude_inani < 16) return -22;
        if (!실행관리.isiqeshana(ikheli, 16)) return -14;
        return 실행관리.짧은수(ikheli) == 2 ? 0 : -97;
    }
    static int i_BIND_ikheli(int 서술자, int ikheli, int ubude_inani) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = hlola_ikheli(ikheli, ubude_inani);
        if (결과 < 0) return 결과;
        if (iNethiwekhi_isibambo[기술] != 0) return -22;
        int iNethiwekhi_ikheli = ikheli_32(ikheli + 4);
        if (iNethiwekhi_ikheli != 0 && iNethiwekhi_ikheli != iNethiwekhi_Isitaki.내주소) return -99;
        int 접속번호 = idivayisi_inani.기억읽기(ikheli + 2) << 8 | idivayisi_inani.기억읽기(ikheli + 3);
        결과 = iNethiwekhi_Isitaki.Vula(접속번호);
        if (결과 < 0) return 결과;
        iNethiwekhi_isibambo[기술] = 결과; impokophelo[기술] = iNethiwekhi_ikheli;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (iNethiwekhi_isibambo[기술] != 0) return 0;
        int 결과 = iNethiwekhi_Isitaki.Vula(0);
        if (결과 < 0) return 결과;
        iNethiwekhi_isibambo[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int imininingwane_ikheli, int ubude_inani, int Izinhlelo, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Izinhlelo != 0) return -95;
        if (ubude_inani < 0 || ubude_inani > 1024) return -90;
        if (ubude_inani != 0 && !실행관리.isiqeshana(imininingwane_ikheli, ubude_inani)) return -14;
        if (!실행관리.isiqeshana(요청주소, 8)) return -14;
        int ikheli = 실행관리.수(요청주소);
        int 결과 = hlola_ikheli(ikheli, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = idivayisi_inani.기억읽기(ikheli + 2) << 8 | idivayisi_inani.기억읽기(ikheli + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) dlulisa_imininingwane[thola_inkomba] = idivayisi_inani.기억읽기(imininingwane_ikheli + thola_inkomba);
        return iNethiwekhi_Isitaki.Thumela(iNethiwekhi_isibambo[기술], ikheli_32(ikheli + 4), 접속번호, dlulisa_imininingwane, ubude_inani);
    }
    static void bhala_ikheli(int ikheli, int ubude_inani, int iNethiwekhi_ikheli, int 접속번호) {
        for (int thola_inkomba = 0; thola_inkomba < ubude_inani && thola_inkomba < 16; thola_inkomba++) {
            int inani = 0;
            if (thola_inkomba == 0) inani = 2;
            if (thola_inkomba == 2) inani = 접속번호 >>> 8;
            if (thola_inkomba == 3) inani = 접속번호;
            if (thola_inkomba >= 4 && thola_inkomba < 8) inani = iNethiwekhi_ikheli >>> (56 - thola_inkomba * 8);
            idivayisi_inani.bhala_inkumbulo(ikheli + thola_inkomba, inani & 255);
        }
    }
    static int 자료전문받기(int 서술자, int imininingwane_ikheli, int ubude_inani, int Izinhlelo, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Izinhlelo & ~64) != 0) return -95;
        if (ubude_inani < 0) return -22;
        if (ubude_inani != 0 && !실행관리.isiqeshana(imininingwane_ikheli, ubude_inani)) return -14;
        int ikheli = 0, ikheli_ubude_ikheli = 0, ikheli_ubude = 0;
        if (요청주소 != 0) {
            if (!실행관리.isiqeshana(요청주소, 8)) return -14;
            ikheli = 실행관리.수(요청주소); ikheli_ubude_ikheli = 실행관리.수(요청주소 + 4);
            if (ikheli != 0) {
                if (!실행관리.isiqeshana(ikheli_ubude_ikheli, 4)) return -14;
                ikheli_ubude = 실행관리.수(ikheli_ubude_ikheli);
                if (ikheli_ubude < 0) return -22;
                if (!실행관리.isiqeshana(ikheli, ikheli_ubude < 16 ? ikheli_ubude : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int Sebenzisa = idivayisi_inani.밀리초();
        while (true) {
            결과 = iNethiwekhi_Isitaki.받기(iNethiwekhi_isibambo[기술], dlulisa_imininingwane, 1024, 0);
            if (결과 != -11) break;
            if ((Izinhlelo & 64) != 0 || (vula_Amasethingi[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && idivayisi_inani.밀리초() - Sebenzisa >= 수신대기밀리초[기술]) return -11;
            if (idivayisi_inani.사용자남은밀리초() <= 10) return -11;
            idivayisi_inani.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > ubude_inani) 결과 = ubude_inani;
        for (int thola_inkomba = 0; thola_inkomba < 결과; thola_inkomba++) idivayisi_inani.bhala_inkumbulo(imininingwane_ikheli + thola_inkomba, dlulisa_imininingwane[thola_inkomba]);
        if (ikheli != 0) {
            bhala_ikheli(ikheli, ikheli_ubude, iNethiwekhi_Isitaki.untanga_ikheli(iNethiwekhi_isibambo[기술]), iNethiwekhi_Isitaki.상대접속번호(iNethiwekhi_isibambo[기술]));
            실행관리.수쓰기(ikheli_ubude_ikheli, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int ikheli, int ubude_ikheli) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.isiqeshana(ubude_ikheli, 4)) return -14;
        int ubude_inani = 실행관리.수(ubude_ikheli);
        if (ubude_inani < 0) return -22;
        if (!실행관리.isiqeshana(ikheli, ubude_inani < 16 ? ubude_inani : 16)) return -14;
        int isikhala_okufakwayo = iNethiwekhi_Isitaki.thola_inkomba(iNethiwekhi_isibambo[기술]);
        bhala_ikheli(ikheli, ubude_inani, impokophelo[기술], isikhala_okufakwayo < 0 ? 0 : iNethiwekhi_Isitaki.접속번호들[isikhala_okufakwayo]);
        실행관리.수쓰기(ubude_ikheli, 16);
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
