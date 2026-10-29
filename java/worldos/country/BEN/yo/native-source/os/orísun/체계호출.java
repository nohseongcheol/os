// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 aṣàmúlò ìtọ́ka/길이는 wáyè_sí_ìgbéwọlé 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ÀRÉÈ_gígùn(int àdírẹ́ẹ̀sì) {
        if (!실행관리.ní_ṣókí(àdírẹ́ẹ̀sì, 4)) return -14;
        int gígùn_iye = 실행관리.수(àdírẹ́ẹ̀sì);
        if (gígùn_iye < 0 || gígùn_iye > (실행관리.aṣàmúlò_parí - àdírẹ́ẹ̀sì - 4) / 4) return -14;
        return gígùn_iye;
    }

    public static int Ìlànà_iye_ìgbéwọlé(int wá_atọ̀ka_àkóónú, int 가, int 나, int 다, int 라, int 마) {
        if (wá_atọ̀ka_àkóónú == 30) return 파일서술자관리.ṣí_fáìlì(가, 나, 다);
        if (wá_atọ̀ka_àkóónú == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (wá_atọ̀ka_àkóónú == 32) return 파일서술자관리.kọ_fáìlì(가, 나, 다);
        if (wá_atọ̀ka_àkóónú == 33) return 파일서술자관리.pa_dé_fáìlì(가);
        if (wá_atọ̀ka_àkóónú == 34) return 파일서술자관리.ṣàwárí_fáìlì(가, 나, 다);
        if (wá_atọ̀ka_àkóónú == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (wá_atọ̀ka_àkóónú == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (wá_atọ̀ka_àkóónú == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (wá_atọ̀ka_àkóónú == 38) return 파일서술자관리.ṣèmúkúro_fáìlì_ìgbéwọlé_orúkọ(가);
        if (wá_atọ̀ka_àkóónú == 39) return 파일서술자관리.ọ̀wọ̀_fáìlì_gígùn(가, 나);
        if (wá_atọ̀ka_àkóónú == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (wá_atọ̀ka_àkóónú == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (wá_atọ̀ka_àkóónú == 42) return 파일서술자관리.BIND_àdírẹ́ẹ̀sì(가, 나, 다);
        if (wá_atọ̀ka_àkóónú == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (wá_atọ̀ka_àkóónú == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (wá_atọ̀ka_àkóónú == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (wá_atọ̀ka_àkóónú == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (wá_atọ̀ka_àkóónú == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.múdọ́gba();
        }
        if (wá_atọ̀ka_àkóónú == 1) {
            int gígùn_iye = ÀRÉÈ_gígùn(가);
            if (gígùn_iye < 0) return gígùn_iye;
            if (gígùn_iye > 4096) return -90;
            for (int ẹyọ_ọ̀rọ̀_iye = 0; ẹyọ_ọ̀rọ̀_iye < gígùn_iye; ẹyọ_ọ̀rọ̀_iye++) 문자단말.문자(실행관리.수(가 + 4 + ẹyọ_ọ̀rọ̀_iye * 4) & 65535);
            return gígùn_iye;
        }
        if (wá_atọ̀ka_àkóónú == 2) return 실행관리.인수수;
        if (wá_atọ̀ka_àkóónú == 3) return 가 >= 0 && 가 < 실행관리.인수수 ? 실행관리.ágúmẹ́ntì_àdírẹ́ẹ̀sì[가] : 0;
        if (wá_atọ̀ka_àkóónú == 10) return Alásopọ̀_kójọ.Ṣi(가);
        if (wá_atọ̀ka_àkóónú == 11) {
            int gígùn_iye = ÀRÉÈ_gígùn(라);
            if (gígùn_iye < 0) return gígùn_iye;
            if (마 < 0 || 마 > gígùn_iye || 마 > 1024) return -90;
            for (int 위치 = 0; 위치 < 마; 위치++) 임시자료[위치] = 실행관리.수(라 + 4 + 위치 * 4) & 255;
            return Alásopọ̀_kójọ.í_meèlì(가, 나, 다, 임시자료, 마);
        }
        if (wá_atọ̀ka_àkóónú == 12) {
            int gígùn_iye = ÀRÉÈ_gígùn(나);
            if (gígùn_iye < 0) return gígùn_iye;
            if (다 < 0 || 다 > 2000) return -22;
            int 결과 = Alásopọ̀_kójọ.받기(가, 임시자료, gígùn_iye < 1024 ? gígùn_iye : 1024, 다);
            if (결과 >= 0) for (int 위치 = 0; 위치 < 결과; 위치++) 실행관리.수쓰기(나 + 4 + 위치 * 4, 임시자료[위치]);
            return 결과;
        }
        if (wá_atọ̀ka_àkóónú == 13) return Alásopọ̀_kójọ.Ti(가);
        if (wá_atọ̀ka_àkóónú == 14) return Alásopọ̀_kójọ.내주소;
        if (wá_atọ̀ka_àkóónú == 15) return Alásopọ̀_kójọ.ọ̀gbà_àdírẹ́ẹ̀sì(가);
        if (wá_atọ̀ka_àkóónú == 16) return Alásopọ̀_kójọ.상대접속번호(가);
        if (wá_atọ̀ka_àkóónú == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            문자단말.문자(가); return 1;
        }
        if (wá_atọ̀ka_àkóónú == 20 || wá_atọ̀ka_àkóónú == 21) {
            int orúkọ_ìwọn = ÀRÉÈ_gígùn(가), détà_ìwọn = ÀRÉÈ_gígùn(나);
            if (orúkọ_ìwọn < 0 || détà_ìwọn < 0) return -14;
            if (orúkọ_ìwọn < 1 || orúkọ_ìwọn > 64) return -22;
            int gígùn_iye = 0;
            while (gígùn_iye < orúkọ_ìwọn && 실행관리.수(가 + 4 + gígùn_iye * 4) != 0) {
                ibi_ìpamọ́_ìlànà_ètò_fáìlì.Orúkọ[gígùn_iye] = 실행관리.수(가 + 4 + gígùn_iye * 4);
                gígùn_iye++;
            }
            if (!ibi_ìpamọ́_ìlànà_ètò_fáìlì.ṣàyẹ̀wò_orúkọ(ibi_ìpamọ́_ìlànà_ètò_fáìlì.Orúkọ, gígùn_iye)) return -22;
            if (wá_atọ̀ka_àkóónú == 20) {
                int Fáìlì = ibi_ìpamọ́_ìlànà_ètò_fáìlì.wá_ìgbéwọlé(ibi_ìpamọ́_ìlànà_ètò_fáìlì.Orúkọ, gígùn_iye);
                if (Fáìlì < 0) return Fáìlì;
                int Ìwọ̀n = ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì];
                if (Ìwọ̀n > détà_ìwọn) return -90;
                int àdírẹ́ẹ̀sì = ohun_èlò_iye.fáìlì_ibi_ìpamọ́() + Fáìlì * ibi_ìpamọ́_ìlànà_ètò_fáìlì.최대크기;
                for (int 수 = 0; 수 < Ìwọ̀n; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, ohun_èlò_iye.기억읽기(àdírẹ́ẹ̀sì + 수));
                return Ìwọ̀n;
            }
            if (다 < 0 || 다 > détà_ìwọn) return -22;
            if (다 > ibi_ìpamọ́_ìlànà_ètò_fáìlì.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) ibi_ìpamọ́_ìlànà_ètò_fáìlì.ṣàtúnṣe_iye[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return ibi_ìpamọ́_ìlànà_ètò_fáìlì.Store_iye(ibi_ìpamọ́_ìlànà_ètò_fáìlì.Orúkọ, gígùn_iye, ibi_ìpamọ́_ìlànà_ètò_fáìlì.ṣàtúnṣe_iye, 다);
        }
        return -38;
    }
}
