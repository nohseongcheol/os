// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 Mai_anfani_da_kwamfuta 과정의 파일서술자와 열린 Fayil 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int Rubutuwa_karantuwa_Tuta = 2, ƙirƙíra_Mashigar_bayanai = 64, 독점생성 = 128, Share_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] buɗe_Mariki = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], tageti = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], buɗe_Saituna = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] Hanyar_sadarwa_Mariki = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] Hanyar_shiga_Suna = new int[64], Gusar_da_Tarin_bayani = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return buɗe_Mariki[파일서술자] - 1;
    }
    static int 빈서술자(int Tafiyar_da) {
        for (int Indes = Tafiyar_da; Indes < 서술자한도; Indes++) if (buɗe_Mariki[Indes] == 0) return Indes;
        return -24;
    }
    static int holoko_Mariki() {
        for (int Indes = 0; Indes < 서술자한도; Indes++) if (참조수[Indes] == 0) return Indes;
        return -24;
    }
    static int Haɗi(int 서술자, int 기술, int 파일종류, int Fayil_tageti, int Saituna) {
        buɗe_Mariki[서술자] = 기술 + 1; 서술자설정[서술자] = (Saituna & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; tageti[기술] = Fayil_tageti; 참조수[기술] = 1;
        buɗe_Saituna[기술] = Saituna & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        Hanyar_sadarwa_Mariki[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Fara_haryar_aikin_na_ura() {
        과정정리();
        for (int Indes = 0; Indes < 3; Indes++) Haɗi(Indes, Indes, 1, Indes, Indes == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int Indes = 0; Indes < 서술자한도; Indes++) if (buɗe_Mariki[Indes] != 0) Rufe_Fayil(Indes);
    }
    static int Rufe_Fayil(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        buɗe_Mariki[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.열림수[tageti[기술]]--;
            if (종류[기술] == 3 && Hanyar_sadarwa_Mariki[기술] != 0) Hanyar_sadarwa_tara.Rufe(Hanyar_sadarwa_Mariki[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bayit_Daraja 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int imel) {
        if (!실행관리.darfi(imel, 1)) return -14;
        int 위치 = na_ura_Daraja.기억읽기(imel) == '/' ? 1 : 0;
        for (int Tsawo_Daraja = 0; Tsawo_Daraja < 64; Tsawo_Daraja++) {
            if (!실행관리.darfi(imel + 위치 + Tsawo_Daraja, 1)) return -14;
            int Daraja = na_ura_Daraja.기억읽기(imel + 위치 + Tsawo_Daraja);
            Hanyar_shiga_Suna[Tsawo_Daraja] = Daraja;
            if (Daraja == 0) return Tsawo_Daraja == 0 ? -2 : (Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Bincika_Suna(Hanyar_shiga_Suna, Tsawo_Daraja) ? Tsawo_Daraja : -22);
            if (Daraja == '/') return -20;
        }
        return -36;
    }
    static int buɗe_Fayil(int Suna_imel, int Saituna, int 허가) {
        int Tsawo_Daraja = 경로읽기(Suna_imel);
        if (Tsawo_Daraja < 0) return Tsawo_Daraja;
        if ((Saituna & ~(3 | ƙirƙíra_Mashigar_bayanai | 독점생성 | Share_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Saituna & 3) == 3 || ((Saituna & Share_TOC) != 0 && (Saituna & 3) == 0)) return -22;
        int Fayil = Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.nema_Mashigar_bayanai(Hanyar_shiga_Suna, Tsawo_Daraja);
        if (Fayil >= 0 && (Saituna & (ƙirƙíra_Mashigar_bayanai | 독점생성)) == (ƙirƙíra_Mashigar_bayanai | 독점생성)) return -17;
        if (Fayil == -2 && (Saituna & ƙirƙíra_Mashigar_bayanai) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = holoko_Mariki();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fayil == -2) {
            int 결과 = Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Ajiye_Daraja(Hanyar_shiga_Suna, Tsawo_Daraja, Hanyar_shiga_Suna, 0);
            if (결과 < 0) return 결과;
            Fayil = Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.nema_Mashigar_bayanai(Hanyar_shiga_Suna, Tsawo_Daraja);
            Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.허가들[Fayil] = 허가 & 511;
        }
        if (Fayil < 0) return Fayil;
        if ((Saituna & Share_TOC) != 0) Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil] = 0;
        Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.열림수[Fayil]++;
        return Haɗi(서술자, 기술, 2, Fayil, Saituna);
    }
    static int 파일읽기(int 서술자, int Tarin_bayani_imel, int Tsawo_Daraja) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (buɗe_Saituna[기술] & 3) == 1) return -9;
        if (Tsawo_Daraja < 0) return -22;
        if (Tsawo_Daraja == 0) return 0;
        if (!실행관리.darfi(Tarin_bayani_imel, Tsawo_Daraja)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, Tarin_bayani_imel, Tsawo_Daraja, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < Tsawo_Daraja) {
                int Daraja = 문자단말.직렬읽기();
                if (Daraja < 0) Daraja = kibod.Yi_Karatu();
                if (Daraja < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((buɗe_Saituna[기술] & 기다리지않기) != 0) return -11;
                    if (na_ura_Daraja.사용자남은밀리초() <= 10) return -11;
                    Hanyar_sadarwa_tara.Tabbatar_da(); na_ura_Daraja.잠시양보();
                } else {
                    na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(Tarin_bayani_imel + 받은수, Daraja); 받은수++;
                }
            }
            return 받은수;
        }
        int Fayil = tageti[기술], 위치 = 파일위치[기술];
        if (위치 >= Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil]) return 0;
        if (Tsawo_Daraja > Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil] - 위치) Tsawo_Daraja = Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil] - 위치;
        int 원본주소 = na_ura_Daraja.Fayil_Mahardatar_kwamfuta() + Fayil * Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.최대크기 + 위치;
        for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(Tarin_bayani_imel + Indes, na_ura_Daraja.기억읽기(원본주소 + Indes));
        파일위치[기술] += Tsawo_Daraja;
        return Tsawo_Daraja;
    }
    static int Rubuta_Fayil(int 서술자, int Tarin_bayani_imel, int Tsawo_Daraja) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (buɗe_Saituna[기술] & 3) == 0) return -9;
        if (Tsawo_Daraja < 0) return -22;
        if (Tsawo_Daraja == 0) return 0;
        if (!실행관리.darfi(Tarin_bayani_imel, Tsawo_Daraja)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 Zangon_ƙarshe_Daraja 주소가 필요하다.
        if (종류[기술] == 1) {
            if (Tsawo_Daraja > 16384) Tsawo_Daraja = 16384;
            for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) {
                int Daraja = na_ura_Daraja.기억읽기(Tarin_bayani_imel + Indes);
                문자단말.직렬바이트(Daraja); 문자단말.화면문자(Daraja);
            }
            return Tsawo_Daraja;
        }
        int Fayil = tageti[기술], Girma = Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil];
        int 위치 = (buɗe_Saituna[기술] & 이어쓰기) != 0 ? Girma : 파일위치[기술];
        if (위치 >= Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.최대크기) return -27;
        if (Tsawo_Daraja > Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.최대크기 - 위치) Tsawo_Daraja = Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.최대크기 - 위치;
        int Zangon_ƙarshe_imel = na_ura_Daraja.Fayil_Mahardatar_kwamfuta() + Fayil * Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.최대크기;
        for (int Indes = Girma; Indes < 위치; Indes++) na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(Zangon_ƙarshe_imel + Indes, 0);
        for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(Zangon_ƙarshe_imel + 위치 + Indes, na_ura_Daraja.기억읽기(Tarin_bayani_imel + Indes));
        파일위치[기술] = 위치 + Tsawo_Daraja;
        if (위치 + Tsawo_Daraja > Girma) Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil] = 위치 + Tsawo_Daraja;
        return Tsawo_Daraja;
    }
    static int binciko_Fayil(int 서술자, int Sassautawa_Daraja, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int Bi_bango_Daraja = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[tageti[기술]]);
        if (Sassautawa_Daraja > 0 && Bi_bango_Daraja > 2147483647 - Sassautawa_Daraja) return -75;
        if (Sassautawa_Daraja < 0 && Sassautawa_Daraja < -Bi_bango_Daraja) return -22;
        파일위치[기술] = Bi_bango_Daraja + Sassautawa_Daraja;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean sanya_Daraja, int Saituna) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return sanya_Daraja ? -9 : -22;
        if (sanya_Daraja && 서술자 == 새서술자) return 새서술자;
        if (sanya_Daraja) { if (buɗe_Mariki[새서술자] != 0) Rufe_Fayil(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        buɗe_Mariki[새서술자] = 기술 + 1; 서술자설정[새서술자] = Saituna; 참조수[기술]++;
        return 새서술자;
    }
    static int Cire_Fayil_Mashigar_bayanai_Suna(int Suna_imel) {
        int Tsawo_Daraja = 경로읽기(Suna_imel);
        if (Tsawo_Daraja < 0) return Tsawo_Daraja;
        int Fayil = Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.nema_Mashigar_bayanai(Hanyar_shiga_Suna, Tsawo_Daraja);
        if (Fayil < 0) return Fayil;
        Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.이름들[Fayil * 64] = 0;
        return 0;
    }
    static int zubi_Fayil_Tsawo(int 서술자, int Tsawo_Daraja) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (buɗe_Saituna[기술] & 3) == 0 || Tsawo_Daraja < 0) return -22;
        if (Tsawo_Daraja > Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.최대크기) return -27;
        int Fayil = tageti[기술], imel = na_ura_Daraja.Fayil_Mahardatar_kwamfuta() + Fayil * Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.최대크기;
        for (int Indes = Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil]; Indes < Tsawo_Daraja; Indes++) na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(imel + Indes, 0);
        Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil] = Tsawo_Daraja;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int imel) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.darfi(imel, 48)) return -14;
        for (int Indes = 0; Indes < 12; Indes++) 실행관리.수쓰기(imel + Indes * 4, 0);
        int Fayil = tageti[기술], Girma = 종류[기술] == 2 ? Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.girma_Jeri[Fayil] : 0;
        int 허가 = 종류[기술] == 2 ? Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.허가들[Fayil] : 438;
        실행관리.수쓰기(imel, 1);
        실행관리.수쓰기(imel + 4, 종류[기술] == 2 ? Fayil + 1 : 100 + 기술);
        실행관리.수쓰기(imel + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(imel + 12, 종류[기술] == 2 && Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.이름들[Fayil * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(imel + 28, Girma); 실행관리.수쓰기(imel + 32, 512);
        실행관리.수쓰기(imel + 36, (Girma + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Umarni, int Daraja) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Umarni == 0 || Umarni == 1030) return 서술자복제(서술자, Daraja, false, Umarni == 1030 ? 1 : 0);
        if (Umarni == 1) return 서술자설정[서술자];
        if (Umarni == 2) { if ((Daraja & ~1) != 0) return -22; 서술자설정[서술자] = Daraja; return 0; }
        if (Umarni == 3) return buɗe_Saituna[기술];
        if (Umarni == 4) {
            if ((Daraja & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            buɗe_Saituna[기술] = (buɗe_Saituna[기술] & 3) | (Daraja & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = holoko_Mariki();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Haɗi(서술자, 기술, 3, 0, Rubutuwa_karantuwa_Tuta);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int imel_32(int imel) {
        return na_ura_Daraja.기억읽기(imel) << 24 | na_ura_Daraja.기억읽기(imel + 1) << 16
            | na_ura_Daraja.기억읽기(imel + 2) << 8 | na_ura_Daraja.기억읽기(imel + 3);
    }
    static int Bincika_imel(int imel, int Tsawo_Daraja) {
        if (Tsawo_Daraja < 16) return -22;
        if (!실행관리.darfi(imel, 16)) return -14;
        return 실행관리.짧은수(imel) == 2 ? 0 : -97;
    }
    static int BIND_imel(int 서술자, int imel, int Tsawo_Daraja) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = Bincika_imel(imel, Tsawo_Daraja);
        if (결과 < 0) return 결과;
        if (Hanyar_sadarwa_Mariki[기술] != 0) return -22;
        int Hanyar_sadarwa_imel_df3458bb = imel_32(imel + 4);
        if (Hanyar_sadarwa_imel_df3458bb != 0 && Hanyar_sadarwa_imel_df3458bb != Hanyar_sadarwa_tara.내주소) return -99;
        int lambar_kafa = na_ura_Daraja.기억읽기(imel + 2) << 8 | na_ura_Daraja.기억읽기(imel + 3);
        결과 = Hanyar_sadarwa_tara.Buɗe(lambar_kafa);
        if (결과 < 0) return 결과;
        Hanyar_sadarwa_Mariki[기술] = 결과; tageti[기술] = Hanyar_sadarwa_imel_df3458bb;
        return 0;
    }
    static int Oto_BIND(int 기술) {
        if (Hanyar_sadarwa_Mariki[기술] != 0) return 0;
        int 결과 = Hanyar_sadarwa_tara.Buɗe(0);
        if (결과 < 0) return 결과;
        Hanyar_sadarwa_Mariki[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int Tarin_bayani_imel, int Tsawo_Daraja, int Saituna, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Saituna != 0) return -95;
        if (Tsawo_Daraja < 0 || Tsawo_Daraja > 1024) return -90;
        if (Tsawo_Daraja != 0 && !실행관리.darfi(Tarin_bayani_imel, Tsawo_Daraja)) return -14;
        if (!실행관리.darfi(요청주소, 8)) return -14;
        int imel = 실행관리.수(요청주소);
        int 결과 = Bincika_imel(imel, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int lambar_kafa = na_ura_Daraja.기억읽기(imel + 2) << 8 | na_ura_Daraja.기억읽기(imel + 3);
        if (lambar_kafa == 0) return -22;
        결과 = Oto_BIND(기술);
        if (결과 < 0) return 결과;
        for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) Gusar_da_Tarin_bayani[Indes] = na_ura_Daraja.기억읽기(Tarin_bayani_imel + Indes);
        return Hanyar_sadarwa_tara.Aika(Hanyar_sadarwa_Mariki[기술], imel_32(imel + 4), lambar_kafa, Gusar_da_Tarin_bayani, Tsawo_Daraja);
    }
    static void Rubuta_imel(int imel, int Tsawo_Daraja, int Hanyar_sadarwa_imel_df3458bb, int lambar_kafa) {
        for (int Indes = 0; Indes < Tsawo_Daraja && Indes < 16; Indes++) {
            int Daraja = 0;
            if (Indes == 0) Daraja = 2;
            if (Indes == 2) Daraja = lambar_kafa >>> 8;
            if (Indes == 3) Daraja = lambar_kafa;
            if (Indes >= 4 && Indes < 8) Daraja = Hanyar_sadarwa_imel_df3458bb >>> (56 - Indes * 8);
            na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(imel + Indes, Daraja & 255);
        }
    }
    static int 자료전문받기(int 서술자, int Tarin_bayani_imel, int Tsawo_Daraja, int Saituna, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Saituna & ~64) != 0) return -95;
        if (Tsawo_Daraja < 0) return -22;
        if (Tsawo_Daraja != 0 && !실행관리.darfi(Tarin_bayani_imel, Tsawo_Daraja)) return -14;
        int imel = 0, imel_Tsawo_imel = 0, imel_Tsawo = 0;
        if (요청주소 != 0) {
            if (!실행관리.darfi(요청주소, 8)) return -14;
            imel = 실행관리.수(요청주소); imel_Tsawo_imel = 실행관리.수(요청주소 + 4);
            if (imel != 0) {
                if (!실행관리.darfi(imel_Tsawo_imel, 4)) return -14;
                imel_Tsawo = 실행관리.수(imel_Tsawo_imel);
                if (imel_Tsawo < 0) return -22;
                if (!실행관리.darfi(imel, imel_Tsawo < 16 ? imel_Tsawo : 16)) return -14;
            }
        }
        int 결과 = Oto_BIND(기술);
        if (결과 < 0) return 결과;
        int Tafiyar_da = na_ura_Daraja.밀리초();
        while (true) {
            결과 = Hanyar_sadarwa_tara.받기(Hanyar_sadarwa_Mariki[기술], Gusar_da_Tarin_bayani, 1024, 0);
            if (결과 != -11) break;
            if ((Saituna & 64) != 0 || (buɗe_Saituna[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && na_ura_Daraja.밀리초() - Tafiyar_da >= 수신대기밀리초[기술]) return -11;
            if (na_ura_Daraja.사용자남은밀리초() <= 10) return -11;
            na_ura_Daraja.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > Tsawo_Daraja) 결과 = Tsawo_Daraja;
        for (int Indes = 0; Indes < 결과; Indes++) na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(Tarin_bayani_imel + Indes, Gusar_da_Tarin_bayani[Indes]);
        if (imel != 0) {
            Rubuta_imel(imel, imel_Tsawo, Hanyar_sadarwa_tara.Fiya_imel(Hanyar_sadarwa_Mariki[기술]), Hanyar_sadarwa_tara.Fiya_lambar_kafa(Hanyar_sadarwa_Mariki[기술]));
            실행관리.수쓰기(imel_Tsawo_imel, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int imel, int Tsawo_imel) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.darfi(Tsawo_imel, 4)) return -14;
        int Tsawo_Daraja = 실행관리.수(Tsawo_imel);
        if (Tsawo_Daraja < 0) return -22;
        if (!실행관리.darfi(imel, Tsawo_Daraja < 16 ? Tsawo_Daraja : 16)) return -14;
        int rami_Mashigar_bayanai = Hanyar_sadarwa_tara.Indes(Hanyar_sadarwa_Mariki[기술]);
        Rubuta_imel(imel, Tsawo_Daraja, tageti[기술], rami_Mashigar_bayanai < 0 ? 0 : Hanyar_sadarwa_tara.접속번호들[rami_Mashigar_bayanai]);
        실행관리.수쓰기(Tsawo_imel, 16);
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
