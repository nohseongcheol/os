// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 umsebenzisi 과정의 파일서술자와 열린 iFayili 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int funda_bhala_iflegi = 2, yila_ufako_nkcukacha = 64, 독점생성 = 128, susa_i_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] vula_isibambi = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], ithagethi = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], vula_Iisetingi = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] Inethiwekhi_isibambi = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] indlela_igama = new int[64], gqithisela_iingcombolo = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return vula_isibambi[파일서술자] - 1;
    }
    static int 빈서술자(int Phumeza) {
        for (int indeksa = Phumeza; indeksa < 서술자한도; indeksa++) if (vula_isibambi[indeksa] == 0) return indeksa;
        return -24;
    }
    static int engenanto_isibambi() {
        for (int indeksa = 0; indeksa < 서술자한도; indeksa++) if (참조수[indeksa] == 0) return indeksa;
        return -24;
    }
    static int Nxulumanisa(int 서술자, int 기술, int 파일종류, int ifayile_ithagethi, int Imimiselo) {
        vula_isibambi[서술자] = 기술 + 1; 서술자설정[서술자] = (Imimiselo & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; ithagethi[기술] = ifayile_ithagethi; 참조수[기술] = 1;
        vula_Iisetingi[기술] = Imimiselo & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        Inethiwekhi_isibambi[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void qala_Inkqubo() {
        과정정리();
        for (int indeksa = 0; indeksa < 3; indeksa++) Nxulumanisa(indeksa, indeksa, 1, indeksa, indeksa == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int indeksa = 0; indeksa < 서술자한도; indeksa++) if (vula_isibambi[indeksa] != 0) vala_ifayile(indeksa);
    }
    static int vala_ifayile(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        vula_isibambi[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) imemori_uhlobo_loseto_lwefayile.열림수[ithagethi[기술]]--;
            if (종류[기술] == 3 && Inethiwekhi_isibambi[기술] != 0) Inethiwekhi_fumba.Vala(Inethiwekhi_isibambi[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 ibhayithi_ixabiso 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int idilesi) {
        if (!실행관리.ikliphu(idilesi, 1)) return -14;
        int 위치 = isixhobo_ixabiso.기억읽기(idilesi) == '/' ? 1 : 0;
        for (int ubude_ixabiso = 0; ubude_ixabiso < 64; ubude_ixabiso++) {
            if (!실행관리.ikliphu(idilesi + 위치 + ubude_ixabiso, 1)) return -14;
            int ixabiso = isixhobo_ixabiso.기억읽기(idilesi + 위치 + ubude_ixabiso);
            indlela_igama[ubude_ixabiso] = ixabiso;
            if (ixabiso == 0) return ubude_ixabiso == 0 ? -2 : (imemori_uhlobo_loseto_lwefayile.jonga_igama(indlela_igama, ubude_ixabiso) ? ubude_ixabiso : -22);
            if (ixabiso == '/') return -20;
        }
        return -36;
    }
    static int vula_ifayile(int igama_idilesi, int Imimiselo, int 허가) {
        int ubude_ixabiso = 경로읽기(igama_idilesi);
        if (ubude_ixabiso < 0) return ubude_ixabiso;
        if ((Imimiselo & ~(3 | yila_ufako_nkcukacha | 독점생성 | susa_i_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Imimiselo & 3) == 3 || ((Imimiselo & susa_i_TOC) != 0 && (Imimiselo & 3) == 0)) return -22;
        int iFayili = imemori_uhlobo_loseto_lwefayile.fumana_ufako_nkcukacha(indlela_igama, ubude_ixabiso);
        if (iFayili >= 0 && (Imimiselo & (yila_ufako_nkcukacha | 독점생성)) == (yila_ufako_nkcukacha | 독점생성)) return -17;
        if (iFayili == -2 && (Imimiselo & yila_ufako_nkcukacha) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = engenanto_isibambi();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (iFayili == -2) {
            int 결과 = imemori_uhlobo_loseto_lwefayile.Store_ixabiso(indlela_igama, ubude_ixabiso, indlela_igama, 0);
            if (결과 < 0) return 결과;
            iFayili = imemori_uhlobo_loseto_lwefayile.fumana_ufako_nkcukacha(indlela_igama, ubude_ixabiso);
            imemori_uhlobo_loseto_lwefayile.허가들[iFayili] = 허가 & 511;
        }
        if (iFayili < 0) return iFayili;
        if ((Imimiselo & susa_i_TOC) != 0) imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili] = 0;
        imemori_uhlobo_loseto_lwefayile.열림수[iFayili]++;
        return Nxulumanisa(서술자, 기술, 2, iFayili, Imimiselo);
    }
    static int 파일읽기(int 서술자, int iingcombolo_idilesi, int ubude_ixabiso) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (vula_Iisetingi[기술] & 3) == 1) return -9;
        if (ubude_ixabiso < 0) return -22;
        if (ubude_ixabiso == 0) return 0;
        if (!실행관리.ikliphu(iingcombolo_idilesi, ubude_ixabiso)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, iingcombolo_idilesi, ubude_ixabiso, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < ubude_ixabiso) {
                int ixabiso = 문자단말.직렬읽기();
                if (ixabiso < 0) ixabiso = ikhibhodi.Funda();
                if (ixabiso < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((vula_Iisetingi[기술] & 기다리지않기) != 0) return -11;
                    if (isixhobo_ixabiso.사용자남은밀리초() <= 10) return -11;
                    Inethiwekhi_fumba.ngqinisisa(); isixhobo_ixabiso.잠시양보();
                } else {
                    isixhobo_ixabiso.bhala_imemori(iingcombolo_idilesi + 받은수, ixabiso); 받은수++;
                }
            }
            return 받은수;
        }
        int iFayili = ithagethi[기술], 위치 = 파일위치[기술];
        if (위치 >= imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili]) return 0;
        if (ubude_ixabiso > imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili] - 위치) ubude_ixabiso = imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili] - 위치;
        int 원본주소 = isixhobo_ixabiso.ifayile_imemori() + iFayili * imemori_uhlobo_loseto_lwefayile.최대크기 + 위치;
        for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) isixhobo_ixabiso.bhala_imemori(iingcombolo_idilesi + indeksa, isixhobo_ixabiso.기억읽기(원본주소 + indeksa));
        파일위치[기술] += ubude_ixabiso;
        return ubude_ixabiso;
    }
    static int bhala_ifayile(int 서술자, int iingcombolo_idilesi, int ubude_ixabiso) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (vula_Iisetingi[기술] & 3) == 0) return -9;
        if (ubude_ixabiso < 0) return -22;
        if (ubude_ixabiso == 0) return 0;
        if (!실행관리.ikliphu(iingcombolo_idilesi, ubude_ixabiso)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 indawo_ekuyiwa_kuyo_ixabiso 주소가 필요하다.
        if (종류[기술] == 1) {
            if (ubude_ixabiso > 16384) ubude_ixabiso = 16384;
            for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) {
                int ixabiso = isixhobo_ixabiso.기억읽기(iingcombolo_idilesi + indeksa);
                문자단말.직렬바이트(ixabiso); 문자단말.화면문자(ixabiso);
            }
            return ubude_ixabiso;
        }
        int iFayili = ithagethi[기술], Ubukhulu = imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili];
        int 위치 = (vula_Iisetingi[기술] & 이어쓰기) != 0 ? Ubukhulu : 파일위치[기술];
        if (위치 >= imemori_uhlobo_loseto_lwefayile.최대크기) return -27;
        if (ubude_ixabiso > imemori_uhlobo_loseto_lwefayile.최대크기 - 위치) ubude_ixabiso = imemori_uhlobo_loseto_lwefayile.최대크기 - 위치;
        int indawo_ekuyiwa_kuyo_idilesi = isixhobo_ixabiso.ifayile_imemori() + iFayili * imemori_uhlobo_loseto_lwefayile.최대크기;
        for (int indeksa = Ubukhulu; indeksa < 위치; indeksa++) isixhobo_ixabiso.bhala_imemori(indawo_ekuyiwa_kuyo_idilesi + indeksa, 0);
        for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) isixhobo_ixabiso.bhala_imemori(indawo_ekuyiwa_kuyo_idilesi + 위치 + indeksa, isixhobo_ixabiso.기억읽기(iingcombolo_idilesi + indeksa));
        파일위치[기술] = 위치 + ubude_ixabiso;
        if (위치 + ubude_ixabiso > Ubukhulu) imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili] = 위치 + ubude_ixabiso;
        return ubude_ixabiso;
    }
    static int khangela_ifayile(int 서술자, int Ukulinganisa_ixabiso, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int Ngasemva_ixabiso = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[ithagethi[기술]]);
        if (Ukulinganisa_ixabiso > 0 && Ngasemva_ixabiso > 2147483647 - Ukulinganisa_ixabiso) return -75;
        if (Ukulinganisa_ixabiso < 0 && Ukulinganisa_ixabiso < -Ngasemva_ixabiso) return -22;
        파일위치[기술] = Ngasemva_ixabiso + Ukulinganisa_ixabiso;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean yabela_ixabiso, int Imimiselo) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return yabela_ixabiso ? -9 : -22;
        if (yabela_ixabiso && 서술자 == 새서술자) return 새서술자;
        if (yabela_ixabiso) { if (vula_isibambi[새서술자] != 0) vala_ifayile(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        vula_isibambi[새서술자] = 기술 + 1; 서술자설정[새서술자] = Imimiselo; 참조수[기술]++;
        return 새서술자;
    }
    static int shenxisa_ifayile_ufako_nkcukacha_igama(int igama_idilesi) {
        int ubude_ixabiso = 경로읽기(igama_idilesi);
        if (ubude_ixabiso < 0) return ubude_ixabiso;
        int iFayili = imemori_uhlobo_loseto_lwefayile.fumana_ufako_nkcukacha(indlela_igama, ubude_ixabiso);
        if (iFayili < 0) return iFayili;
        imemori_uhlobo_loseto_lwefayile.이름들[iFayili * 64] = 0;
        return 0;
    }
    static int isethi_ifayile_ubude(int 서술자, int ubude_ixabiso) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (vula_Iisetingi[기술] & 3) == 0 || ubude_ixabiso < 0) return -22;
        if (ubude_ixabiso > imemori_uhlobo_loseto_lwefayile.최대크기) return -27;
        int iFayili = ithagethi[기술], idilesi = isixhobo_ixabiso.ifayile_imemori() + iFayili * imemori_uhlobo_loseto_lwefayile.최대크기;
        for (int indeksa = imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili]; indeksa < ubude_ixabiso; indeksa++) isixhobo_ixabiso.bhala_imemori(idilesi + indeksa, 0);
        imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili] = ubude_ixabiso;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int idilesi) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.ikliphu(idilesi, 48)) return -14;
        for (int indeksa = 0; indeksa < 12; indeksa++) 실행관리.수쓰기(idilesi + indeksa * 4, 0);
        int iFayili = ithagethi[기술], Ubukhulu = 종류[기술] == 2 ? imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili] : 0;
        int 허가 = 종류[기술] == 2 ? imemori_uhlobo_loseto_lwefayile.허가들[iFayili] : 438;
        실행관리.수쓰기(idilesi, 1);
        실행관리.수쓰기(idilesi + 4, 종류[기술] == 2 ? iFayili + 1 : 100 + 기술);
        실행관리.수쓰기(idilesi + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(idilesi + 12, 종류[기술] == 2 && imemori_uhlobo_loseto_lwefayile.이름들[iFayili * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(idilesi + 28, Ubukhulu); 실행관리.수쓰기(idilesi + 32, 512);
        실행관리.수쓰기(idilesi + 36, (Ubukhulu + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Umyalelo, int ixabiso) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Umyalelo == 0 || Umyalelo == 1030) return 서술자복제(서술자, ixabiso, false, Umyalelo == 1030 ? 1 : 0);
        if (Umyalelo == 1) return 서술자설정[서술자];
        if (Umyalelo == 2) { if ((ixabiso & ~1) != 0) return -22; 서술자설정[서술자] = ixabiso; return 0; }
        if (Umyalelo == 3) return vula_Iisetingi[기술];
        if (Umyalelo == 4) {
            if ((ixabiso & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            vula_Iisetingi[기술] = (vula_Iisetingi[기술] & 3) | (ixabiso & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = engenanto_isibambi();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Nxulumanisa(서술자, 기술, 3, 0, funda_bhala_iflegi);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int idilesi_32(int idilesi) {
        return isixhobo_ixabiso.기억읽기(idilesi) << 24 | isixhobo_ixabiso.기억읽기(idilesi + 1) << 16
            | isixhobo_ixabiso.기억읽기(idilesi + 2) << 8 | isixhobo_ixabiso.기억읽기(idilesi + 3);
    }
    static int jonga_idilesi(int idilesi, int ubude_ixabiso) {
        if (ubude_ixabiso < 16) return -22;
        if (!실행관리.ikliphu(idilesi, 16)) return -14;
        return 실행관리.짧은수(idilesi) == 2 ? 0 : -97;
    }
    static int BOPHELELA_idilesi(int 서술자, int idilesi, int ubude_ixabiso) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = jonga_idilesi(idilesi, ubude_ixabiso);
        if (결과 < 0) return 결과;
        if (Inethiwekhi_isibambi[기술] != 0) return -22;
        int Inethiwekhi_idilesi = idilesi_32(idilesi + 4);
        if (Inethiwekhi_idilesi != 0 && Inethiwekhi_idilesi != Inethiwekhi_fumba.내주소) return -99;
        int 접속번호 = isixhobo_ixabiso.기억읽기(idilesi + 2) << 8 | isixhobo_ixabiso.기억읽기(idilesi + 3);
        결과 = Inethiwekhi_fumba.Vula(접속번호);
        if (결과 < 0) return 결과;
        Inethiwekhi_isibambi[기술] = 결과; ithagethi[기술] = Inethiwekhi_idilesi;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Inethiwekhi_isibambi[기술] != 0) return 0;
        int 결과 = Inethiwekhi_fumba.Vula(0);
        if (결과 < 0) return 결과;
        Inethiwekhi_isibambi[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int iingcombolo_idilesi, int ubude_ixabiso, int Imimiselo, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Imimiselo != 0) return -95;
        if (ubude_ixabiso < 0 || ubude_ixabiso > 1024) return -90;
        if (ubude_ixabiso != 0 && !실행관리.ikliphu(iingcombolo_idilesi, ubude_ixabiso)) return -14;
        if (!실행관리.ikliphu(요청주소, 8)) return -14;
        int idilesi = 실행관리.수(요청주소);
        int 결과 = jonga_idilesi(idilesi, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = isixhobo_ixabiso.기억읽기(idilesi + 2) << 8 | isixhobo_ixabiso.기억읽기(idilesi + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) gqithisela_iingcombolo[indeksa] = isixhobo_ixabiso.기억읽기(iingcombolo_idilesi + indeksa);
        return Inethiwekhi_fumba.thumela(Inethiwekhi_isibambi[기술], idilesi_32(idilesi + 4), 접속번호, gqithisela_iingcombolo, ubude_ixabiso);
    }
    static void bhala_idilesi(int idilesi, int ubude_ixabiso, int Inethiwekhi_idilesi, int 접속번호) {
        for (int indeksa = 0; indeksa < ubude_ixabiso && indeksa < 16; indeksa++) {
            int ixabiso = 0;
            if (indeksa == 0) ixabiso = 2;
            if (indeksa == 2) ixabiso = 접속번호 >>> 8;
            if (indeksa == 3) ixabiso = 접속번호;
            if (indeksa >= 4 && indeksa < 8) ixabiso = Inethiwekhi_idilesi >>> (56 - indeksa * 8);
            isixhobo_ixabiso.bhala_imemori(idilesi + indeksa, ixabiso & 255);
        }
    }
    static int 자료전문받기(int 서술자, int iingcombolo_idilesi, int ubude_ixabiso, int Imimiselo, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Imimiselo & ~64) != 0) return -95;
        if (ubude_ixabiso < 0) return -22;
        if (ubude_ixabiso != 0 && !실행관리.ikliphu(iingcombolo_idilesi, ubude_ixabiso)) return -14;
        int idilesi = 0, idilesi_ubude_idilesi = 0, idilesi_ubude = 0;
        if (요청주소 != 0) {
            if (!실행관리.ikliphu(요청주소, 8)) return -14;
            idilesi = 실행관리.수(요청주소); idilesi_ubude_idilesi = 실행관리.수(요청주소 + 4);
            if (idilesi != 0) {
                if (!실행관리.ikliphu(idilesi_ubude_idilesi, 4)) return -14;
                idilesi_ubude = 실행관리.수(idilesi_ubude_idilesi);
                if (idilesi_ubude < 0) return -22;
                if (!실행관리.ikliphu(idilesi, idilesi_ubude < 16 ? idilesi_ubude : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int Phumeza = isixhobo_ixabiso.밀리초();
        while (true) {
            결과 = Inethiwekhi_fumba.받기(Inethiwekhi_isibambi[기술], gqithisela_iingcombolo, 1024, 0);
            if (결과 != -11) break;
            if ((Imimiselo & 64) != 0 || (vula_Iisetingi[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && isixhobo_ixabiso.밀리초() - Phumeza >= 수신대기밀리초[기술]) return -11;
            if (isixhobo_ixabiso.사용자남은밀리초() <= 10) return -11;
            isixhobo_ixabiso.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > ubude_ixabiso) 결과 = ubude_ixabiso;
        for (int indeksa = 0; indeksa < 결과; indeksa++) isixhobo_ixabiso.bhala_imemori(iingcombolo_idilesi + indeksa, gqithisela_iingcombolo[indeksa]);
        if (idilesi != 0) {
            bhala_idilesi(idilesi, idilesi_ubude, Inethiwekhi_fumba.untanga_idilesi(Inethiwekhi_isibambi[기술]), Inethiwekhi_fumba.상대접속번호(Inethiwekhi_isibambi[기술]));
            실행관리.수쓰기(idilesi_ubude_idilesi, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int idilesi, int ubude_idilesi) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.ikliphu(ubude_idilesi, 4)) return -14;
        int ubude_ixabiso = 실행관리.수(ubude_idilesi);
        if (ubude_ixabiso < 0) return -22;
        if (!실행관리.ikliphu(idilesi, ubude_ixabiso < 16 ? ubude_ixabiso : 16)) return -14;
        int isithuba_ufako_nkcukacha = Inethiwekhi_fumba.indeksa(Inethiwekhi_isibambi[기술]);
        bhala_idilesi(idilesi, ubude_ixabiso, ithagethi[기술], isithuba_ufako_nkcukacha < 0 ? 0 : Inethiwekhi_fumba.접속번호들[isithuba_ufako_nkcukacha]);
        실행관리.수쓰기(ubude_idilesi, 16);
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
