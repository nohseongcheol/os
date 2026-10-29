// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 aṣàmúlò 과정의 파일서술자와 열린 Fáìlì 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int tí_a_lè_kà_tí_a_lè_kọ_ipe_àkíyèsí_sí = 2, Ṣẹ̀dá_ìgbéwọlé = 64, 독점생성 = 128, mú_kúrò_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] ṣí_èkù = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], àfojúsùn = new int[서술자한도];
    static int[] 파일위치 = new int[서술자한도], ṣí_Àwọn_ààtò = new int[서술자한도], 참조수 = new int[서술자한도];
    static int[] Alásopọ̀_èkù = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] ọ̀nà_orúkọ = new int[64], ṣàgbélọ_détà = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return ṣí_èkù[파일서술자] - 1;
    }
    static int 빈서술자(int Rọ́ọ̀nù) {
        for (int wá_atọ̀ka_àkóónú = Rọ́ọ̀nù; wá_atọ̀ka_àkóónú < 서술자한도; wá_atọ̀ka_àkóónú++) if (ṣí_èkù[wá_atọ̀ka_àkóónú] == 0) return wá_atọ̀ka_àkóónú;
        return -24;
    }
    static int òfìfo_èkù() {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 서술자한도; wá_atọ̀ka_àkóónú++) if (참조수[wá_atọ̀ka_àkóónú] == 0) return wá_atọ̀ka_àkóónú;
        return -24;
    }
    static int Darapọ̀(int 서술자, int 기술, int 파일종류, int fáìlì_àfojúsùn, int Àwọn_ààtò) {
        ṣí_èkù[서술자] = 기술 + 1; 서술자설정[서술자] = (Àwọn_ààtò & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; àfojúsùn[기술] = fáìlì_àfojúsùn; 참조수[기술] = 1;
        ṣí_Àwọn_ààtò[기술] = Àwọn_ààtò & (3 | 이어쓰기 | 기다리지않기); 파일위치[기술] = 0;
        Alásopọ̀_èkù[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void bẹ̀rẹ̀_Ìlànà() {
        과정정리();
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 3; wá_atọ̀ka_àkóónú++) Darapọ̀(wá_atọ̀ka_àkóónú, wá_atọ̀ka_àkóónú, 1, wá_atọ̀ka_àkóónú, wá_atọ̀ka_àkóónú == 0 ? 0 : 1);
    }
    static void 과정정리() {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 서술자한도; wá_atọ̀ka_àkóónú++) if (ṣí_èkù[wá_atọ̀ka_àkóónú] != 0) pa_dé_fáìlì(wá_atọ̀ka_àkóónú);
    }
    static int pa_dé_fáìlì(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        ṣí_èkù[서술자] = 0; 서술자설정[서술자] = 0;
        참조수[기술]--;
        if (참조수[기술] == 0) {
            if (종류[기술] == 2) ibi_ìpamọ́_ìlànà_ètò_fáìlì.열림수[àfojúsùn[기술]]--;
            if (종류[기술] == 3 && Alásopọ̀_èkù[기술] != 0) Alásopọ̀_kójọ.Ti(Alásopọ̀_èkù[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 báìtì_iye 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int àdírẹ́ẹ̀sì) {
        if (!실행관리.ní_ṣókí(àdírẹ́ẹ̀sì, 1)) return -14;
        int 위치 = ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì) == '/' ? 1 : 0;
        for (int gígùn_iye = 0; gígùn_iye < 64; gígùn_iye++) {
            if (!실행관리.ní_ṣókí(àdírẹ́ẹ̀sì + 위치 + gígùn_iye, 1)) return -14;
            int iye = ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 위치 + gígùn_iye);
            ọ̀nà_orúkọ[gígùn_iye] = iye;
            if (iye == 0) return gígùn_iye == 0 ? -2 : (ibi_ìpamọ́_ìlànà_ètò_fáìlì.ṣàyẹ̀wò_orúkọ(ọ̀nà_orúkọ, gígùn_iye) ? gígùn_iye : -22);
            if (iye == '/') return -20;
        }
        return -36;
    }
    static int ṣí_fáìlì(int orúkọ_àdírẹ́ẹ̀sì, int Àwọn_ààtò, int 허가) {
        int gígùn_iye = 경로읽기(orúkọ_àdírẹ́ẹ̀sì);
        if (gígùn_iye < 0) return gígùn_iye;
        if ((Àwọn_ààtò & ~(3 | Ṣẹ̀dá_ìgbéwọlé | 독점생성 | mú_kúrò_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Àwọn_ààtò & 3) == 3 || ((Àwọn_ààtò & mú_kúrò_TOC) != 0 && (Àwọn_ààtò & 3) == 0)) return -22;
        int Fáìlì = ibi_ìpamọ́_ìlànà_ètò_fáìlì.wá_ìgbéwọlé(ọ̀nà_orúkọ, gígùn_iye);
        if (Fáìlì >= 0 && (Àwọn_ààtò & (Ṣẹ̀dá_ìgbéwọlé | 독점생성)) == (Ṣẹ̀dá_ìgbéwọlé | 독점생성)) return -17;
        if (Fáìlì == -2 && (Àwọn_ààtò & Ṣẹ̀dá_ìgbéwọlé) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = òfìfo_èkù();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fáìlì == -2) {
            int 결과 = ibi_ìpamọ́_ìlànà_ètò_fáìlì.Store_iye(ọ̀nà_orúkọ, gígùn_iye, ọ̀nà_orúkọ, 0);
            if (결과 < 0) return 결과;
            Fáìlì = ibi_ìpamọ́_ìlànà_ètò_fáìlì.wá_ìgbéwọlé(ọ̀nà_orúkọ, gígùn_iye);
            ibi_ìpamọ́_ìlànà_ètò_fáìlì.허가들[Fáìlì] = 허가 & 511;
        }
        if (Fáìlì < 0) return Fáìlì;
        if ((Àwọn_ààtò & mú_kúrò_TOC) != 0) ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì] = 0;
        ibi_ìpamọ́_ìlànà_ètò_fáìlì.열림수[Fáìlì]++;
        return Darapọ̀(서술자, 기술, 2, Fáìlì, Àwọn_ààtò);
    }
    static int 파일읽기(int 서술자, int détà_àdírẹ́ẹ̀sì, int gígùn_iye) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (ṣí_Àwọn_ààtò[기술] & 3) == 1) return -9;
        if (gígùn_iye < 0) return -22;
        if (gígùn_iye == 0) return 0;
        if (!실행관리.ní_ṣókí(détà_àdírẹ́ẹ̀sì, gígùn_iye)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, détà_àdírẹ́ẹ̀sì, gígùn_iye, 0, 0);
        if (종류[기술] == 1) {
            int 받은수 = 0;
            while (받은수 < gígùn_iye) {
                int iye = 문자단말.직렬읽기();
                if (iye < 0) iye = àtẹ_ìtẹ̀wé.Kàá();
                if (iye < 0) {
                    if (받은수 > 0) return 받은수;
                    if ((ṣí_Àwọn_ààtò[기술] & 기다리지않기) != 0) return -11;
                    if (ohun_èlò_iye.사용자남은밀리초() <= 10) return -11;
                    Alásopọ̀_kójọ.ridájú(); ohun_èlò_iye.잠시양보();
                } else {
                    ohun_èlò_iye.kọ_ibi_ìpamọ́(détà_àdírẹ́ẹ̀sì + 받은수, iye); 받은수++;
                }
            }
            return 받은수;
        }
        int Fáìlì = àfojúsùn[기술], 위치 = 파일위치[기술];
        if (위치 >= ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì]) return 0;
        if (gígùn_iye > ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì] - 위치) gígùn_iye = ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì] - 위치;
        int 원본주소 = ohun_èlò_iye.fáìlì_ibi_ìpamọ́() + Fáìlì * ibi_ìpamọ́_ìlànà_ètò_fáìlì.최대크기 + 위치;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) ohun_èlò_iye.kọ_ibi_ìpamọ́(détà_àdírẹ́ẹ̀sì + wá_atọ̀ka_àkóónú, ohun_èlò_iye.기억읽기(원본주소 + wá_atọ̀ka_àkóónú));
        파일위치[기술] += gígùn_iye;
        return gígùn_iye;
    }
    static int kọ_fáìlì(int 서술자, int détà_àdírẹ́ẹ̀sì, int gígùn_iye) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (ṣí_Àwọn_ààtò[기술] & 3) == 0) return -9;
        if (gígùn_iye < 0) return -22;
        if (gígùn_iye == 0) return 0;
        if (!실행관리.ní_ṣókí(détà_àdírẹ́ẹ̀sì, gígùn_iye)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 èbúté_iye 주소가 필요하다.
        if (종류[기술] == 1) {
            if (gígùn_iye > 16384) gígùn_iye = 16384;
            for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) {
                int iye = ohun_èlò_iye.기억읽기(détà_àdírẹ́ẹ̀sì + wá_atọ̀ka_àkóónú);
                문자단말.직렬바이트(iye); 문자단말.화면문자(iye);
            }
            return gígùn_iye;
        }
        int Fáìlì = àfojúsùn[기술], Ìwọ̀n = ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì];
        int 위치 = (ṣí_Àwọn_ààtò[기술] & 이어쓰기) != 0 ? Ìwọ̀n : 파일위치[기술];
        if (위치 >= ibi_ìpamọ́_ìlànà_ètò_fáìlì.최대크기) return -27;
        if (gígùn_iye > ibi_ìpamọ́_ìlànà_ètò_fáìlì.최대크기 - 위치) gígùn_iye = ibi_ìpamọ́_ìlànà_ètò_fáìlì.최대크기 - 위치;
        int èbúté_àdírẹ́ẹ̀sì = ohun_èlò_iye.fáìlì_ibi_ìpamọ́() + Fáìlì * ibi_ìpamọ́_ìlànà_ètò_fáìlì.최대크기;
        for (int wá_atọ̀ka_àkóónú = Ìwọ̀n; wá_atọ̀ka_àkóónú < 위치; wá_atọ̀ka_àkóónú++) ohun_èlò_iye.kọ_ibi_ìpamọ́(èbúté_àdírẹ́ẹ̀sì + wá_atọ̀ka_àkóónú, 0);
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) ohun_èlò_iye.kọ_ibi_ìpamọ́(èbúté_àdírẹ́ẹ̀sì + 위치 + wá_atọ̀ka_àkóónú, ohun_èlò_iye.기억읽기(détà_àdírẹ́ẹ̀sì + wá_atọ̀ka_àkóónú));
        파일위치[기술] = 위치 + gígùn_iye;
        if (위치 + gígùn_iye > Ìwọ̀n) ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì] = 위치 + gígùn_iye;
        return gígùn_iye;
    }
    static int ṣàwárí_fáìlì(int 서술자, int Ìtayọ_iye, int 기준) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (기준 < 0 || 기준 > 2) return -22;
        int Àgbétẹ́lẹ̀_iye = 기준 == 0 ? 0 : (기준 == 1 ? 파일위치[기술] : ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[àfojúsùn[기술]]);
        if (Ìtayọ_iye > 0 && Àgbétẹ́lẹ̀_iye > 2147483647 - Ìtayọ_iye) return -75;
        if (Ìtayọ_iye < 0 && Ìtayọ_iye < -Àgbétẹ́lẹ̀_iye) return -22;
        파일위치[기술] = Àgbétẹ́lẹ̀_iye + Ìtayọ_iye;
        return 파일위치[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int Àwọn_ààtò) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (ṣí_èkù[새서술자] != 0) pa_dé_fáìlì(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        ṣí_èkù[새서술자] = 기술 + 1; 서술자설정[새서술자] = Àwọn_ààtò; 참조수[기술]++;
        return 새서술자;
    }
    static int ṣèmúkúro_fáìlì_ìgbéwọlé_orúkọ(int orúkọ_àdírẹ́ẹ̀sì) {
        int gígùn_iye = 경로읽기(orúkọ_àdírẹ́ẹ̀sì);
        if (gígùn_iye < 0) return gígùn_iye;
        int Fáìlì = ibi_ìpamọ́_ìlànà_ètò_fáìlì.wá_ìgbéwọlé(ọ̀nà_orúkọ, gígùn_iye);
        if (Fáìlì < 0) return Fáìlì;
        ibi_ìpamọ́_ìlànà_ètò_fáìlì.이름들[Fáìlì * 64] = 0;
        return 0;
    }
    static int ọ̀wọ̀_fáìlì_gígùn(int 서술자, int gígùn_iye) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (ṣí_Àwọn_ààtò[기술] & 3) == 0 || gígùn_iye < 0) return -22;
        if (gígùn_iye > ibi_ìpamọ́_ìlànà_ètò_fáìlì.최대크기) return -27;
        int Fáìlì = àfojúsùn[기술], àdírẹ́ẹ̀sì = ohun_èlò_iye.fáìlì_ibi_ìpamọ́() + Fáìlì * ibi_ìpamọ́_ìlànà_ètò_fáìlì.최대크기;
        for (int wá_atọ̀ka_àkóónú = ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì]; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) ohun_èlò_iye.kọ_ibi_ìpamọ́(àdírẹ́ẹ̀sì + wá_atọ̀ka_àkóónú, 0);
        ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì] = gígùn_iye;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int àdírẹ́ẹ̀sì) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.ní_ṣókí(àdírẹ́ẹ̀sì, 48)) return -14;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 12; wá_atọ̀ka_àkóónú++) 실행관리.수쓰기(àdírẹ́ẹ̀sì + wá_atọ̀ka_àkóónú * 4, 0);
        int Fáìlì = àfojúsùn[기술], Ìwọ̀n = 종류[기술] == 2 ? ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì] : 0;
        int 허가 = 종류[기술] == 2 ? ibi_ìpamọ́_ìlànà_ètò_fáìlì.허가들[Fáìlì] : 438;
        실행관리.수쓰기(àdírẹ́ẹ̀sì, 1);
        실행관리.수쓰기(àdírẹ́ẹ̀sì + 4, 종류[기술] == 2 ? Fáìlì + 1 : 100 + 기술);
        실행관리.수쓰기(àdírẹ́ẹ̀sì + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(àdírẹ́ẹ̀sì + 12, 종류[기술] == 2 && ibi_ìpamọ́_ìlànà_ètò_fáìlì.이름들[Fáìlì * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(àdírẹ́ẹ̀sì + 28, Ìwọ̀n); 실행관리.수쓰기(àdírẹ́ẹ̀sì + 32, 512);
        실행관리.수쓰기(àdírẹ́ẹ̀sì + 36, (Ìwọ̀n + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Àṣẹ, int iye) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Àṣẹ == 0 || Àṣẹ == 1030) return 서술자복제(서술자, iye, false, Àṣẹ == 1030 ? 1 : 0);
        if (Àṣẹ == 1) return 서술자설정[서술자];
        if (Àṣẹ == 2) { if ((iye & ~1) != 0) return -22; 서술자설정[서술자] = iye; return 0; }
        if (Àṣẹ == 3) return ṣí_Àwọn_ààtò[기술];
        if (Àṣẹ == 4) {
            if ((iye & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            ṣí_Àwọn_ààtò[기술] = (ṣí_Àwọn_ààtò[기술] & 3) | (iye & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = òfìfo_èkù();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Darapọ̀(서술자, 기술, 3, 0, tí_a_lè_kà_tí_a_lè_kọ_ipe_àkíyèsí_sí);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int àdírẹ́ẹ̀sì_32(int àdírẹ́ẹ̀sì) {
        return ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì) << 24 | ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 1) << 16
            | ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 2) << 8 | ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 3);
    }
    static int ṣàyẹ̀wò_àdírẹ́ẹ̀sì(int àdírẹ́ẹ̀sì, int gígùn_iye) {
        if (gígùn_iye < 16) return -22;
        if (!실행관리.ní_ṣókí(àdírẹ́ẹ̀sì, 16)) return -14;
        return 실행관리.짧은수(àdírẹ́ẹ̀sì) == 2 ? 0 : -97;
    }
    static int BIND_àdírẹ́ẹ̀sì(int 서술자, int àdírẹ́ẹ̀sì, int gígùn_iye) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int 결과 = ṣàyẹ̀wò_àdírẹ́ẹ̀sì(àdírẹ́ẹ̀sì, gígùn_iye);
        if (결과 < 0) return 결과;
        if (Alásopọ̀_èkù[기술] != 0) return -22;
        int Alásopọ̀_àdírẹ́ẹ̀sì = àdírẹ́ẹ̀sì_32(àdírẹ́ẹ̀sì + 4);
        if (Alásopọ̀_àdírẹ́ẹ̀sì != 0 && Alásopọ̀_àdírẹ́ẹ̀sì != Alásopọ̀_kójọ.내주소) return -99;
        int 접속번호 = ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 2) << 8 | ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 3);
        결과 = Alásopọ̀_kójọ.Ṣi(접속번호);
        if (결과 < 0) return 결과;
        Alásopọ̀_èkù[기술] = 결과; àfojúsùn[기술] = Alásopọ̀_àdírẹ́ẹ̀sì;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Alásopọ̀_èkù[기술] != 0) return 0;
        int 결과 = Alásopọ̀_kójọ.Ṣi(0);
        if (결과 < 0) return 결과;
        Alásopọ̀_èkù[기술] = 결과;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int détà_àdírẹ́ẹ̀sì, int gígùn_iye, int Àwọn_ààtò, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Àwọn_ààtò != 0) return -95;
        if (gígùn_iye < 0 || gígùn_iye > 1024) return -90;
        if (gígùn_iye != 0 && !실행관리.ní_ṣókí(détà_àdírẹ́ẹ̀sì, gígùn_iye)) return -14;
        if (!실행관리.ní_ṣókí(요청주소, 8)) return -14;
        int àdírẹ́ẹ̀sì = 실행관리.수(요청주소);
        int 결과 = ṣàyẹ̀wò_àdírẹ́ẹ̀sì(àdírẹ́ẹ̀sì, 실행관리.수(요청주소 + 4));
        if (결과 < 0) return 결과;
        int 접속번호 = ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 2) << 8 | ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 3);
        if (접속번호 == 0) return -22;
        결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) ṣàgbélọ_détà[wá_atọ̀ka_àkóónú] = ohun_èlò_iye.기억읽기(détà_àdírẹ́ẹ̀sì + wá_atọ̀ka_àkóónú);
        return Alásopọ̀_kójọ.í_meèlì(Alásopọ̀_èkù[기술], àdírẹ́ẹ̀sì_32(àdírẹ́ẹ̀sì + 4), 접속번호, ṣàgbélọ_détà, gígùn_iye);
    }
    static void kọ_àdírẹ́ẹ̀sì(int àdírẹ́ẹ̀sì, int gígùn_iye, int Alásopọ̀_àdírẹ́ẹ̀sì, int 접속번호) {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye && wá_atọ̀ka_àkóónú < 16; wá_atọ̀ka_àkóónú++) {
            int iye = 0;
            if (wá_atọ̀ka_àkóónú == 0) iye = 2;
            if (wá_atọ̀ka_àkóónú == 2) iye = 접속번호 >>> 8;
            if (wá_atọ̀ka_àkóónú == 3) iye = 접속번호;
            if (wá_atọ̀ka_àkóónú >= 4 && wá_atọ̀ka_àkóónú < 8) iye = Alásopọ̀_àdírẹ́ẹ̀sì >>> (56 - wá_atọ̀ka_àkóónú * 8);
            ohun_èlò_iye.kọ_ibi_ìpamọ́(àdírẹ́ẹ̀sì + wá_atọ̀ka_àkóónú, iye & 255);
        }
    }
    static int 자료전문받기(int 서술자, int détà_àdírẹ́ẹ̀sì, int gígùn_iye, int Àwọn_ààtò, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Àwọn_ààtò & ~64) != 0) return -95;
        if (gígùn_iye < 0) return -22;
        if (gígùn_iye != 0 && !실행관리.ní_ṣókí(détà_àdírẹ́ẹ̀sì, gígùn_iye)) return -14;
        int àdírẹ́ẹ̀sì = 0, àdírẹ́ẹ̀sì_gígùn_àdírẹ́ẹ̀sì = 0, àdírẹ́ẹ̀sì_gígùn = 0;
        if (요청주소 != 0) {
            if (!실행관리.ní_ṣókí(요청주소, 8)) return -14;
            àdírẹ́ẹ̀sì = 실행관리.수(요청주소); àdírẹ́ẹ̀sì_gígùn_àdírẹ́ẹ̀sì = 실행관리.수(요청주소 + 4);
            if (àdírẹ́ẹ̀sì != 0) {
                if (!실행관리.ní_ṣókí(àdírẹ́ẹ̀sì_gígùn_àdírẹ́ẹ̀sì, 4)) return -14;
                àdírẹ́ẹ̀sì_gígùn = 실행관리.수(àdírẹ́ẹ̀sì_gígùn_àdírẹ́ẹ̀sì);
                if (àdírẹ́ẹ̀sì_gígùn < 0) return -22;
                if (!실행관리.ní_ṣókí(àdírẹ́ẹ̀sì, àdírẹ́ẹ̀sì_gígùn < 16 ? àdírẹ́ẹ̀sì_gígùn : 16)) return -14;
            }
        }
        int 결과 = 자동묶기(기술);
        if (결과 < 0) return 결과;
        int Rọ́ọ̀nù = ohun_èlò_iye.밀리초();
        while (true) {
            결과 = Alásopọ̀_kójọ.받기(Alásopọ̀_èkù[기술], ṣàgbélọ_détà, 1024, 0);
            if (결과 != -11) break;
            if ((Àwọn_ààtò & 64) != 0 || (ṣí_Àwọn_ààtò[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && ohun_èlò_iye.밀리초() - Rọ́ọ̀nù >= 수신대기밀리초[기술]) return -11;
            if (ohun_èlò_iye.사용자남은밀리초() <= 10) return -11;
            ohun_èlò_iye.잠시양보();
        }
        if (결과 < 0) return 결과;
        if (결과 > gígùn_iye) 결과 = gígùn_iye;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 결과; wá_atọ̀ka_àkóónú++) ohun_èlò_iye.kọ_ibi_ìpamọ́(détà_àdírẹ́ẹ̀sì + wá_atọ̀ka_àkóónú, ṣàgbélọ_détà[wá_atọ̀ka_àkóónú]);
        if (àdírẹ́ẹ̀sì != 0) {
            kọ_àdírẹ́ẹ̀sì(àdírẹ́ẹ̀sì, àdírẹ́ẹ̀sì_gígùn, Alásopọ̀_kójọ.ọ̀gbà_àdírẹ́ẹ̀sì(Alásopọ̀_èkù[기술]), Alásopọ̀_kójọ.상대접속번호(Alásopọ̀_èkù[기술]));
            실행관리.수쓰기(àdírẹ́ẹ̀sì_gígùn_àdírẹ́ẹ̀sì, 16);
        }
        return 결과;
    }
    static int 통신주소읽기(int 서술자, int àdírẹ́ẹ̀sì, int gígùn_àdírẹ́ẹ̀sì) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.ní_ṣókí(gígùn_àdírẹ́ẹ̀sì, 4)) return -14;
        int gígùn_iye = 실행관리.수(gígùn_àdírẹ́ẹ̀sì);
        if (gígùn_iye < 0) return -22;
        if (!실행관리.ní_ṣókí(àdírẹ́ẹ̀sì, gígùn_iye < 16 ? gígùn_iye : 16)) return -14;
        int ààyè_ìfàyọkàsí_ìgbéwọlé = Alásopọ̀_kójọ.wá_atọ̀ka_àkóónú(Alásopọ̀_èkù[기술]);
        kọ_àdírẹ́ẹ̀sì(àdírẹ́ẹ̀sì, gígùn_iye, àfojúsùn[기술], ààyè_ìfàyọkàsí_ìgbéwọlé < 0 ? 0 : Alásopọ̀_kójọ.접속번호들[ààyè_ìfàyọkàsí_ìgbéwọlé]);
        실행관리.수쓰기(gígùn_àdírẹ́ẹ̀sì, 16);
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
