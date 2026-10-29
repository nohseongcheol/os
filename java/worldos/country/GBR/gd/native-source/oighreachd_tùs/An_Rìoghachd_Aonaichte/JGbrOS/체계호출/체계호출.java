// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.체계호출;

import An_Rìoghachd_Aonaichte.JGbrOS.기억공간.duilleag_manaidsear;
import An_Rìoghachd_Aonaichte.JGbrOS.작업.Pròiseas_VALUE;
import An_Rìoghachd_Aonaichte.JGbrOS.작업.sgeidealaiche;
import An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean.실행파일적재기;
import An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean.siostam_fhaidhlichean;
import An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean.faidhle_fios;
import An_Rìoghachd_Aonaichte.JGbrOS.eitean.하드웨어;
import An_Rìoghachd_Aonaichte.JGbrOS.입력.입력관리자;
import An_Rìoghachd_Aonaichte.JGbrOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int ri_leughadh_a_mhàin_bratach = 0;
    public static final int lorg_Start = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_cur_a_steach_crìochnaich = 2;

    private final siostam_fhaidhlichean siostam_fhaidhlichean;
    private final duilleag_manaidsear 쪽관리;
    private final sgeidealaiche sgeidealaiche;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 uidheam_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(siostam_fhaidhlichean siostam_fhaidhlichean, duilleag_manaidsear 쪽관리, sgeidealaiche sgeidealaiche, 하드웨어 uidheam_VALUE, 입력관리자 입력관리) {
        this.siostam_fhaidhlichean = siostam_fhaidhlichean;
        this.쪽관리 = 쪽관리;
        this.sgeidealaiche = sgeidealaiche;
        this.uidheam_VALUE = uidheam_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Pròiseas_aithnichear(Pròiseas_VALUE 현재과정) {
        return 현재과정.aithnichear_VALUE();
    }

    public int 부모과정식별자(Pròiseas_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int fosgail(Pròiseas_VALUE 현재과정, String Ainm, int bratach_VALUE) {
        if (bratach_VALUE != ri_leughadh_a_mhàin_bratach) {
            return -30;
        }
        return 현재과정.파일서술자().fosgail(Ainm);
    }

    public int 읽기(Pròiseas_VALUE 현재과정, int 서술자, byte[] 받을곳, int atharraich_am_meud) {
        if (서술자 == 0) {
            if (atharraich_am_meud <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 tachartas = 입력관리.air_adhart_tachartas();
            if (tachartas == null || tachartas.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) tachartas.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, atharraich_am_meud);
    }

    public int sgrìobh(Pròiseas_VALUE 현재과정, int 서술자, byte[] dàta, int atharraich_am_meud) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (atharraich_am_meud < 0 || atharraich_am_meud > dàta.length) {
            return -22;
        }
        uidheam_VALUE.직렬출력(new String(dàta, 0, atharraich_am_meud, java.nio.charset.StandardCharsets.UTF_8));
        return atharraich_am_meud;
    }

    public int dùin(Pròiseas_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().dùin(서술자);
    }

    public int gluais_suidhich(Pròiseas_VALUE 현재과정, int 서술자, int 거리, int tilg_freumh) {
        return 현재과정.파일서술자().gluais_suidhich(서술자, 거리, tilg_freumh);
    }

    public int 서술자복제(Pròiseas_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Pròiseas_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Ainm, int dòigh_MODE) {
        faidhle_fios msinfo32_exe = siostam_fhaidhlichean.msinfo32_exe(Ainm);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((dòigh_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((dòigh_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_liosta_nan_saothair(String Ainm) {
        return "/".equals(Ainm) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int cleachdaiche_aithnichear() { return 0; }
    public int buadhach_cleachdaiche_aithnichear() { return 0; }
    public int buidheann_aithnichear() { return 0; }
    public int buadhach_buidheann_aithnichear() { return 0; }

    public int sioncronaich_faidhle(Pròiseas_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Pròiseas_VALUE 현재과정, int 서술자) {
        faidhle_fios msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int faidhle_smachd(Pròiseas_VALUE 현재과정, int 서술자, int àithne, int 인자) {
        if (àithne == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (àithne == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (àithne == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (àithne == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : ri_leughadh_a_mhàin_bratach;
        }
        if (àithne == 4) {
            return 인자 == ri_leughadh_a_mhàin_bratach ? 0 : -30;
        }
        return -22;
    }

    public int Create_cur_a_steach(String Ainm, int cead_VALUE) {
        return -30;
    }

    public faidhle_fios 서술자정보(Pròiseas_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JGbrOS", "JGbrOS", "0.1", "Java managed kernel", "i386");
    }

    public faidhle_fios faidhle_fios(String Ainm) {
        return siostam_fhaidhlichean.msinfo32_exe(Ainm);
    }

    public Pròiseas_VALUE 과정복제(Pròiseas_VALUE 부모) {
        return sgeidealaiche.복제(부모);
    }

    public int 자식기다리기(Pròiseas_VALUE 부모, int duine_cloinne_aithnichear, boolean 기다리지않음) {
        return sgeidealaiche.자식기다리기(부모, duine_cloinne_aithnichear, 기다리지않음);
    }

    public int 프로그램끝(Pròiseas_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / duilleag_manaidsear.meud_na_duilleige;
        int 끝쪽 = (새끝 + duilleag_manaidsear.meud_na_duilleige - 1) / duilleag_manaidsear.meud_na_duilleige;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * duilleag_manaidsear.meud_na_duilleige;
                try {
                    쪽관리.바이트읽기(현재과정.ADDRESS_spàs(), ADDRESS);
                } catch (IllegalStateException Mearachd) {
                    쪽관리.MAP_duilleag(현재과정.ADDRESS_spàs(), ADDRESS, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Pròiseas_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int tomhas = 프로그램끝(현재과정, 이전끝 + 증가량);
        return tomhas < 0 ? tomhas : 이전끝;
    }

    public int gnìomhaich_àithne(Pròiseas_VALUE 현재과정, byte[] 실행파일) {
        return gnìomhaich_àithne(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int gnìomhaich_àithne(Pròiseas_VALUE 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Mearachd) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.earrann_VALUE earrann_VALUE : IMAGE_VALUE.구역들()) {
            if ((earrann_VALUE.bratach_VALUE() & 2) == 0 || earrann_VALUE.atharraich_am_meud() == 0) {
                continue;
            }
            int 첫쪽 = earrann_VALUE.ADDRESS() / duilleag_manaidsear.meud_na_duilleige;
            int 끝쪽 = (earrann_VALUE.ADDRESS() + earrann_VALUE.atharraich_am_meud() + duilleag_manaidsear.meud_na_duilleige - 1) / duilleag_manaidsear.meud_na_duilleige;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * duilleag_manaidsear.meud_na_duilleige;
                try {
                    쪽관리.바이트읽기(현재과정.ADDRESS_spàs(), ADDRESS);
                    쪽관리.범위개인쓰기(현재과정.ADDRESS_spàs(), ADDRESS, duilleag_manaidsear.meud_na_duilleige);
                } catch (IllegalStateException Mearachd) {
                    쪽관리.MAP_duilleag(현재과정.ADDRESS_spàs(), ADDRESS, true);
                }
            }
            for (int INDEX = 0; INDEX < earrann_VALUE.atharraich_am_meud(); INDEX++) {
                byte VALUE = earrann_VALUE.종류() == 8 ? 0 : 실행파일[earrann_VALUE.faidhle_suidhich() + INDEX];
                쪽관리.sgrìobh_baidht_VALUE(현재과정.ADDRESS_spàs(), earrann_VALUE.ADDRESS() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(IMAGE_VALUE.Start_ADDRESS(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void fàg_an_seo_ap(Pròiseas_VALUE 현재과정, int cor_VALUE) {
        현재과정.fàg_ap(cor_VALUE);
    }
}
