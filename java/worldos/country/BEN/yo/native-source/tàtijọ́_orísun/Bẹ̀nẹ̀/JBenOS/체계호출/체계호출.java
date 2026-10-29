// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bẹ̀nẹ̀.JBenOS.체계호출;

import Bẹ̀nẹ̀.JBenOS.기억공간.ojú_ìwé_alákòóso;
import Bẹ̀nẹ̀.JBenOS.작업.Ìlànà_iye;
import Bẹ̀nẹ̀.JBenOS.작업.배정기;
import Bẹ̀nẹ̀.JBenOS.ìlànà_ètò_fáìlì.실행파일적재기;
import Bẹ̀nẹ̀.JBenOS.ìlànà_ètò_fáìlì.ìlànà_ètò_fáìlì;
import Bẹ̀nẹ̀.JBenOS.ìlànà_ètò_fáìlì.fáìlì_Ìwífún;
import Bẹ̀nẹ̀.JBenOS.kánẹ́ẹ̀lì.ohun_èlò_alárídìmú_iye;
import Bẹ̀nẹ̀.JBenOS.입력.입력관리자;
import Bẹ̀nẹ̀.JBenOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int kàn_kàá_ipe_àkíyèsí_sí = 0;
    public static final int wákiri_bẹ̀rẹ̀ = 0;
    public static final int 찾기현재 = 1;
    public static final int wá_ìgbéwọlé_parí = 2;

    private final ìlànà_ètò_fáìlì ìlànà_ètò_fáìlì;
    private final ojú_ìwé_alákòóso 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final ohun_èlò_alárídìmú_iye ohun_èlò_iye;
    private final 입력관리자 입력관리;

    public 체계호출(ìlànà_ètò_fáìlì ìlànà_ètò_fáìlì, ojú_ìwé_alákòóso 쪽관리, 배정기 배정기, ohun_èlò_alárídìmú_iye ohun_èlò_iye, 입력관리자 입력관리) {
        this.ìlànà_ètò_fáìlì = ìlànà_ètò_fáìlì;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.ohun_èlò_iye = ohun_èlò_iye;
        this.입력관리 = 입력관리;
    }

    public int Ìlànà_Àfidámọ̀(Ìlànà_iye 현재과정) {
        return 현재과정.Àfidámọ̀_iye();
    }

    public int 부모과정식별자(Ìlànà_iye 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Ṣi(Ìlànà_iye 현재과정, String Orúkọ, int ipe_àkíyèsí_sí_iye) {
        if (ipe_àkíyèsí_sí_iye != kàn_kàá_ipe_àkíyèsí_sí) {
            return -30;
        }
        return 현재과정.파일서술자().Ṣi(Orúkọ);
    }

    public int Kàá(Ìlànà_iye 현재과정, int 서술자, byte[] 받을곳, int Ìwọ̀n) {
        if (서술자 == 0) {
            if (Ìwọ̀n <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 ìgbéṣẹ̀ = 입력관리.다음사건();
            if (ìgbéṣẹ̀ == null || ìgbéṣẹ̀.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) ìgbéṣẹ̀.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Kàá(서술자, 받을곳, Ìwọ̀n);
    }

    public int Kọ(Ìlànà_iye 현재과정, int 서술자, byte[] détà, int Ìwọ̀n) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (Ìwọ̀n < 0 || Ìwọ̀n > détà.length) {
            return -22;
        }
        ohun_èlò_iye.직렬출력(new String(détà, 0, Ìwọ̀n, java.nio.charset.StandardCharsets.UTF_8));
        return Ìwọ̀n;
    }

    public int Ti(Ìlànà_iye 현재과정, int 서술자) {
        return 현재과정.파일서술자().Ti(서술자);
    }

    public int 위치옮기기(Ìlànà_iye 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(Ìlànà_iye 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Ìlànà_iye 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Orúkọ, int ìlànà_móòdù) {
        fáìlì_Ìwífún msinfo32_exe = ìlànà_ètò_fáìlì.msinfo32_exe(Orúkọ);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((ìlànà_móòdù & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((ìlànà_móòdù & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int ṣèpapòdà_àtòkọ_iṣẹ́(String Orúkọ) {
        return "/".equals(Orúkọ) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int aṣàmúlò_Àfidámọ̀() { return 0; }
    public int ìmọ̀ọ́ṣe_aṣàmúlò_Àfidámọ̀() { return 0; }
    public int Àjọṣe_Àfidámọ̀() { return 0; }
    public int ìmọ̀ọ́ṣe_Àjọṣe_Àfidámọ̀() { return 0; }

    public int múdọ́gba_fáìlì(Ìlànà_iye 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Kàá 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Ìlànà_iye 현재과정, int 서술자) {
        fáìlì_Ìwífún msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int fáìlì_ìdarí(Ìlànà_iye 현재과정, int 서술자, int Àṣẹ, int 인자) {
        if (Àṣẹ == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (Àṣẹ == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Àṣẹ == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (Àṣẹ == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : kàn_kàá_ipe_àkíyèsí_sí;
        }
        if (Àṣẹ == 4) {
            return 인자 == kàn_kàá_ipe_àkíyèsí_sí ? 0 : -30;
        }
        return -22;
    }

    public int Ṣẹ̀dá_ìgbéwọlé(String Orúkọ, int Ìyànda_iye) {
        return -30;
    }

    public fáìlì_Ìwífún 서술자정보(Ìlànà_iye 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JBenOS", "JBenOS", "0.1", "Java managed kernel", "i386");
    }

    public fáìlì_Ìwífún fáìlì_Ìwífún(String Orúkọ) {
        return ìlànà_ètò_fáìlì.msinfo32_exe(Orúkọ);
    }

    public Ìlànà_iye 과정복제(Ìlànà_iye 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(Ìlànà_iye 부모, int ọmọ_Àfidámọ̀, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, ọmọ_Àfidámọ̀, 기다리지않음);
    }

    public int 프로그램끝(Ìlànà_iye 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / ojú_ìwé_alákòóso.ìwọ̀n_ojú_ìwé;
        int 끝쪽 = (새끝 + ojú_ìwé_alákòóso.ìwọ̀n_ojú_ìwé - 1) / ojú_ìwé_alákòóso.ìwọ̀n_ojú_ìwé;
        if (새끝 > 이전끝) {
            for (int wá_atọ̀ka_àkóónú = 첫쪽; wá_atọ̀ka_àkóónú < 끝쪽; wá_atọ̀ka_àkóónú++) {
                int àdírẹ́ẹ̀sì = wá_atọ̀ka_àkóónú * ojú_ìwé_alákòóso.ìwọ̀n_ojú_ìwé;
                try {
                    쪽관리.바이트읽기(현재과정.àdírẹ́ẹ̀sì_àlàfo(), àdírẹ́ẹ̀sì);
                } catch (IllegalStateException àṣìṣe) {
                    쪽관리.máàpù_ojú_ìwé(현재과정.àdírẹ́ẹ̀sì_àlàfo(), àdírẹ́ẹ̀sì, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Ìlànà_iye 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int ṣiṣẹ́_àṣẹ(Ìlànà_iye 현재과정, byte[] 실행파일) {
        return ṣiṣẹ́_àṣẹ(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int ṣiṣẹ́_àṣẹ(Ìlànà_iye 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.àwòrán àwòrán_iye;
        try {
            àwòrán_iye = 적재기.검사(실행파일);
        } catch (IllegalArgumentException àṣìṣe) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.abala_iye abala_iye : àwòrán_iye.구역들()) {
            if ((abala_iye.ipe_àkíyèsí_sí_iye() & 2) == 0 || abala_iye.Ìwọ̀n() == 0) {
                continue;
            }
            int 첫쪽 = abala_iye.àdírẹ́ẹ̀sì() / ojú_ìwé_alákòóso.ìwọ̀n_ojú_ìwé;
            int 끝쪽 = (abala_iye.àdírẹ́ẹ̀sì() + abala_iye.Ìwọ̀n() + ojú_ìwé_alákòóso.ìwọ̀n_ojú_ìwé - 1) / ojú_ìwé_alákòóso.ìwọ̀n_ojú_ìwé;
            for (int wá_atọ̀ka_àkóónú = 첫쪽; wá_atọ̀ka_àkóónú < 끝쪽; wá_atọ̀ka_àkóónú++) {
                int àdírẹ́ẹ̀sì = wá_atọ̀ka_àkóónú * ojú_ìwé_alákòóso.ìwọ̀n_ojú_ìwé;
                try {
                    쪽관리.바이트읽기(현재과정.àdírẹ́ẹ̀sì_àlàfo(), àdírẹ́ẹ̀sì);
                    쪽관리.범위개인쓰기(현재과정.àdírẹ́ẹ̀sì_àlàfo(), àdírẹ́ẹ̀sì, ojú_ìwé_alákòóso.ìwọ̀n_ojú_ìwé);
                } catch (IllegalStateException àṣìṣe) {
                    쪽관리.máàpù_ojú_ìwé(현재과정.àdírẹ́ẹ̀sì_àlàfo(), àdírẹ́ẹ̀sì, true);
                }
            }
            for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < abala_iye.Ìwọ̀n(); wá_atọ̀ka_àkóónú++) {
                byte iye = abala_iye.종류() == 8 ? 0 : 실행파일[abala_iye.파일위치() + wá_atọ̀ka_àkóónú];
                쪽관리.kọ_báìtì_iye(현재과정.àdírẹ́ẹ̀sì_àlàfo(), abala_iye.àdírẹ́ẹ̀sì() + wá_atọ̀ka_àkóónú, iye);
            }
        }
        현재과정.실행문맥설정(àwòrán_iye.bẹ̀rẹ̀_àdírẹ́ẹ̀sì(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(Ìlànà_iye 현재과정, int ipò_iye) {
        현재과정.jáde_àtòjọ_ètò(ipò_iye);
    }
}
