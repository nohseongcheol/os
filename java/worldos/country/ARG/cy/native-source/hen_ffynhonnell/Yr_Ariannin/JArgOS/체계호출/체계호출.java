// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Yr_Ariannin.JArgOS.체계호출;

import Yr_Ariannin.JArgOS.기억공간.tudalen_rheolwr;
import Yr_Ariannin.JArgOS.작업.Proses_VALUE;
import Yr_Ariannin.JArgOS.작업.Trefnwr;
import Yr_Ariannin.JArgOS.system_ffeiliau.실행파일적재기;
import Yr_Ariannin.JArgOS.system_ffeiliau.system_ffeiliau;
import Yr_Ariannin.JArgOS.system_ffeiliau.ffeil_gwybodaeth;
import Yr_Ariannin.JArgOS.cnewyllyn.하드웨어;
import Yr_Ariannin.JArgOS.입력.입력관리자;
import Yr_Ariannin.JArgOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int darllen_yn_unig_fflag = 0;
    public static final int SEARCH_START = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_cofnod_gorffen = 2;

    private final system_ffeiliau system_ffeiliau;
    private final tudalen_rheolwr 쪽관리;
    private final Trefnwr Trefnwr;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 dyfais_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(system_ffeiliau system_ffeiliau, tudalen_rheolwr 쪽관리, Trefnwr Trefnwr, 하드웨어 dyfais_VALUE, 입력관리자 입력관리) {
        this.system_ffeiliau = system_ffeiliau;
        this.쪽관리 = 쪽관리;
        this.Trefnwr = Trefnwr;
        this.dyfais_VALUE = dyfais_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Proses_dynodwr(Proses_VALUE 현재과정) {
        return 현재과정.dynodwr_VALUE();
    }

    public int 부모과정식별자(Proses_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Agor(Proses_VALUE 현재과정, String Enw, int fflag_VALUE) {
        if (fflag_VALUE != darllen_yn_unig_fflag) {
            return -30;
        }
        return 현재과정.파일서술자().Agor(Enw);
    }

    public int Darllen(Proses_VALUE 현재과정, int 서술자, byte[] 받을곳, int Maint) {
        if (서술자 == 0) {
            if (Maint <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 digwyddiad = 입력관리.Nesaf_digwyddiad();
            if (digwyddiad == null || digwyddiad.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) digwyddiad.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Darllen(서술자, 받을곳, Maint);
    }

    public int Ysgrifennu(Proses_VALUE 현재과정, int 서술자, byte[] data, int Maint) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().technoleg_gwybodaeth_agor(서술자) ? -30 : -9;
        }
        if (Maint < 0 || Maint > data.length) {
            return -22;
        }
        dyfais_VALUE.직렬출력(new String(data, 0, Maint, java.nio.charset.StandardCharsets.UTF_8));
        return Maint;
    }

    public int Cau(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Cau(서술자);
    }

    public int symud_safle(Proses_VALUE 현재과정, int 서술자, int 거리, int prosiect_gwraidd) {
        return 현재과정.파일서술자().symud_safle(서술자, 거리, prosiect_gwraidd);
    }

    public int 서술자복제(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proses_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Enw, int dull_MODE) {
        ffeil_gwybodaeth msinfo32_exe = system_ffeiliau.msinfo32_exe(Enw);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((dull_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((dull_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int newid_rhestr_tasgau(String Enw) {
        return "/".equals(Enw) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int defnyddiwr_dynodwr() { return 0; }
    public int effeithiol_defnyddiwr_dynodwr() { return 0; }
    public int Grŵp_dynodwr() { return 0; }
    public int effeithiol_Grŵp_dynodwr() { return 0; }

    public int cysoni_ffeil(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Darllen 전용이어서 밀어낼 자료가 없다.
    }

    public boolean technoleg_gwybodaeth_Terfynell(Proses_VALUE 현재과정, int 서술자) {
        ffeil_gwybodaeth msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int ffeil_rheoli(Proses_VALUE 현재과정, int 서술자, int Gorchymyn, int paramedr_arg) {
        if (Gorchymyn == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, paramedr_arg);
        }
        if (Gorchymyn == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Gorchymyn == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (paramedr_arg & 1) != 0);
        }
        if (Gorchymyn == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : darllen_yn_unig_fflag;
        }
        if (Gorchymyn == 4) {
            return paramedr_arg == darllen_yn_unig_fflag ? 0 : -30;
        }
        return -22;
    }

    public int Creu_cofnod(String Enw, int hawl_VALUE) {
        return -30;
    }

    public ffeil_gwybodaeth 서술자정보(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JArgOS", "JArgOS", "0.1", "Java managed kernel", "i386");
    }

    public ffeil_gwybodaeth ffeil_gwybodaeth(String Enw) {
        return system_ffeiliau.msinfo32_exe(Enw);
    }

    public Proses_VALUE 과정복제(Proses_VALUE 부모) {
        return Trefnwr.복제(부모);
    }

    public int 자식기다리기(Proses_VALUE 부모, int iselfen_dynodwr, boolean 기다리지않음) {
        return Trefnwr.자식기다리기(부모, iselfen_dynodwr, 기다리지않음);
    }

    public int 프로그램끝(Proses_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / tudalen_rheolwr.maint_tudalen;
        int 끝쪽 = (새끝 + tudalen_rheolwr.maint_tudalen - 1) / tudalen_rheolwr.maint_tudalen;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * tudalen_rheolwr.maint_tudalen;
                try {
                    쪽관리.바이트읽기(현재과정.ADDRESS_lle(), ADDRESS);
                } catch (IllegalStateException Gwall) {
                    쪽관리.MAP_tudalen(현재과정.ADDRESS_lle(), ADDRESS, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Proses_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int mesur = 프로그램끝(현재과정, 이전끝 + 증가량);
        return mesur < 0 ? mesur : 이전끝;
    }

    public int Gweithredu_gorchymyn(Proses_VALUE 현재과정, byte[] 실행파일) {
        return Gweithredu_gorchymyn(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int Gweithredu_gorchymyn(Proses_VALUE 현재과정, byte[] 실행파일, String[] paramedr_arg, String[] 환경) {
        실행파일적재기.llun llun_VALUE;
        try {
            llun_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Gwall) {
            return -8;
        }
        if (paramedr_arg == null || 환경 == null || paramedr_arg.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.adran_VALUE adran_VALUE : llun_VALUE.구역들()) {
            if ((adran_VALUE.fflag_VALUE() & 2) == 0 || adran_VALUE.Maint() == 0) {
                continue;
            }
            int 첫쪽 = adran_VALUE.ADDRESS() / tudalen_rheolwr.maint_tudalen;
            int 끝쪽 = (adran_VALUE.ADDRESS() + adran_VALUE.Maint() + tudalen_rheolwr.maint_tudalen - 1) / tudalen_rheolwr.maint_tudalen;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * tudalen_rheolwr.maint_tudalen;
                try {
                    쪽관리.바이트읽기(현재과정.ADDRESS_lle(), ADDRESS);
                    쪽관리.범위개인쓰기(현재과정.ADDRESS_lle(), ADDRESS, tudalen_rheolwr.maint_tudalen);
                } catch (IllegalStateException Gwall) {
                    쪽관리.MAP_tudalen(현재과정.ADDRESS_lle(), ADDRESS, true);
                }
            }
            for (int INDEX = 0; INDEX < adran_VALUE.Maint(); INDEX++) {
                byte VALUE = adran_VALUE.종류() == 8 ? 0 : 실행파일[adran_VALUE.ffeil_safle() + INDEX];
                쪽관리.ysgrifennu_beit_VALUE(현재과정.ADDRESS_lle(), adran_VALUE.ADDRESS() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(llun_VALUE.cyfeiriad_cychwyn(), paramedr_arg, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void gadael_Rhaglen_55b3a1cd(Proses_VALUE 현재과정, int cyflwr_VALUE) {
        현재과정.gadael_Rhaglen(cyflwr_VALUE);
    }
}
