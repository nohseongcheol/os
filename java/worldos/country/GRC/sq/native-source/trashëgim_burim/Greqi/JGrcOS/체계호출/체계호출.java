// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Greqi.JGrcOS.체계호출;

import Greqi.JGrcOS.기억공간.faqe_menaxher;
import Greqi.JGrcOS.작업.Proces_VALUE;
import Greqi.JGrcOS.작업.Planifikuesi;
import Greqi.JGrcOS.sistemi_i_skedarëve.실행파일적재기;
import Greqi.JGrcOS.sistemi_i_skedarëve.sistemi_i_skedarëve;
import Greqi.JGrcOS.sistemi_i_skedarëve.skedar_informacion;
import Greqi.JGrcOS.bërthamë.하드웨어;
import Greqi.JGrcOS.입력.입력관리자;
import Greqi.JGrcOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int vetëm_për_lexim_flamur = 0;
    public static final int Kërkim_nis = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_futje_mbaroj = 2;

    private final sistemi_i_skedarëve sistemi_i_skedarëve;
    private final faqe_menaxher 쪽관리;
    private final Planifikuesi Planifikuesi;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 pajisje_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(sistemi_i_skedarëve sistemi_i_skedarëve, faqe_menaxher 쪽관리, Planifikuesi Planifikuesi, 하드웨어 pajisje_VALUE, 입력관리자 입력관리) {
        this.sistemi_i_skedarëve = sistemi_i_skedarëve;
        this.쪽관리 = 쪽관리;
        this.Planifikuesi = Planifikuesi;
        this.pajisje_VALUE = pajisje_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Proces_identifikues(Proces_VALUE 현재과정) {
        return 현재과정.identifikues_VALUE();
    }

    public int 부모과정식별자(Proces_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Hap(Proces_VALUE 현재과정, String Emër, int flamur_VALUE) {
        if (flamur_VALUE != vetëm_për_lexim_flamur) {
            return -30;
        }
        return 현재과정.파일서술자().Hap(Emër);
    }

    public int Leximi(Proces_VALUE 현재과정, int 서술자, byte[] 받을곳, int Madhësi) {
        if (서술자 == 0) {
            if (Madhësi <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 Ngjarje = 입력관리.Tjetër_ngjarje();
            if (Ngjarje == null || Ngjarje.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) Ngjarje.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Leximi(서술자, 받을곳, Madhësi);
    }

    public int Shkrimi(Proces_VALUE 현재과정, int 서술자, byte[] të_dhëna, int Madhësi) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().teknologjia_e_informacionit_hap(서술자) ? -30 : -9;
        }
        if (Madhësi < 0 || Madhësi > të_dhëna.length) {
            return -22;
        }
        pajisje_VALUE.직렬출력(new String(të_dhëna, 0, Madhësi, java.nio.charset.StandardCharsets.UTF_8));
        return Madhësi;
    }

    public int Mbyll(Proces_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Mbyll(서술자);
    }

    public int lëviz_pozicioni(Proces_VALUE 현재과정, int 서술자, int 거리, int Project_rrënjë) {
        return 현재과정.파일서술자().lëviz_pozicioni(서술자, 거리, Project_rrënjë);
    }

    public int 서술자복제(Proces_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proces_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Emër, int metoda_MODE) {
        skedar_informacion msinfo32_exe = sistemi_i_skedarëve.msinfo32_exe(Emër);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metoda_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metoda_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_lista_e_detyrave(String Emër) {
        return "/".equals(Emër) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int përdorues_identifikues() { return 0; }
    public int efektiv_përdorues_identifikues() { return 0; }
    public int grup_identifikues() { return 0; }
    public int efektiv_grup_identifikues() { return 0; }

    public int sinkronizoj_skedar(Proces_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Leximi 전용이어서 밀어낼 자료가 없다.
    }

    public boolean teknologjia_e_informacionit_Terminali(Proces_VALUE 현재과정, int 서술자) {
        skedar_informacion msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int skedar_kontroll(Proces_VALUE 현재과정, int 서술자, int Komanda, int parametër_argument) {
        if (Komanda == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, parametër_argument);
        }
        if (Komanda == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Komanda == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (parametër_argument & 1) != 0);
        }
        if (Komanda == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : vetëm_për_lexim_flamur;
        }
        if (Komanda == 4) {
            return parametër_argument == vetëm_për_lexim_flamur ? 0 : -30;
        }
        return -22;
    }

    public int Krijo_futje(String Emër, int leje_VALUE) {
        return -30;
    }

    public skedar_informacion 서술자정보(Proces_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JGrcOS", "JGrcOS", "0.1", "Java managed kernel", "i386");
    }

    public skedar_informacion skedar_informacion(String Emër) {
        return sistemi_i_skedarëve.msinfo32_exe(Emër);
    }

    public Proces_VALUE 과정복제(Proces_VALUE 부모) {
        return Planifikuesi.복제(부모);
    }

    public int 자식기다리기(Proces_VALUE 부모, int fëmijë_identifikues, boolean 기다리지않음) {
        return Planifikuesi.자식기다리기(부모, fëmijë_identifikues, 기다리지않음);
    }

    public int 프로그램끝(Proces_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / faqe_menaxher.përmasat_e_faqes;
        int 끝쪽 = (새끝 + faqe_menaxher.përmasat_e_faqes - 1) / faqe_menaxher.përmasat_e_faqes;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int email = INDEX * faqe_menaxher.përmasat_e_faqes;
                try {
                    쪽관리.바이트읽기(현재과정.email_HAPËSIRË(), email);
                } catch (IllegalStateException GABIM) {
                    쪽관리.MAP_faqe(현재과정.email_HAPËSIRË(), email, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Proces_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int llogaritje = 프로그램끝(현재과정, 이전끝 + 증가량);
        return llogaritje < 0 ? llogaritje : 이전끝;
    }

    public int zbatoj_komandë(Proces_VALUE 현재과정, byte[] 실행파일) {
        return zbatoj_komandë(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int zbatoj_komandë(Proces_VALUE 현재과정, byte[] 실행파일, String[] parametër_argument, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException GABIM) {
            return -8;
        }
        if (parametër_argument == null || 환경 == null || parametër_argument.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.seksion_VALUE seksion_VALUE : IMAGE_VALUE.구역들()) {
            if ((seksion_VALUE.flamur_VALUE() & 2) == 0 || seksion_VALUE.Madhësi() == 0) {
                continue;
            }
            int 첫쪽 = seksion_VALUE.email() / faqe_menaxher.përmasat_e_faqes;
            int 끝쪽 = (seksion_VALUE.email() + seksion_VALUE.Madhësi() + faqe_menaxher.përmasat_e_faqes - 1) / faqe_menaxher.përmasat_e_faqes;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int email = INDEX * faqe_menaxher.përmasat_e_faqes;
                try {
                    쪽관리.바이트읽기(현재과정.email_HAPËSIRË(), email);
                    쪽관리.범위개인쓰기(현재과정.email_HAPËSIRË(), email, faqe_menaxher.përmasat_e_faqes);
                } catch (IllegalStateException GABIM) {
                    쪽관리.MAP_faqe(현재과정.email_HAPËSIRË(), email, true);
                }
            }
            for (int INDEX = 0; INDEX < seksion_VALUE.Madhësi(); INDEX++) {
                byte VALUE = seksion_VALUE.종류() == 8 ? 0 : 실행파일[seksion_VALUE.skedar_pozicioni() + INDEX];
                쪽관리.shkruaj_bajt_VALUE(현재과정.email_HAPËSIRË(), seksion_VALUE.email() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(IMAGE_VALUE.nis_email(), parametër_argument, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void mbyll_program(Proces_VALUE 현재과정, int status_VALUE) {
        현재과정.dal_program(status_VALUE);
    }
}
