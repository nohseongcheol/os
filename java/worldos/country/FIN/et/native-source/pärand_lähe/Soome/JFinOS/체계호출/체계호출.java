// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.체계호출;

import Soome.JFinOS.Mälu_regioon.쪽관리자;
import Soome.JFinOS.작업.Joonis_VALUE;
import Soome.JFinOS.작업.plaanija;
import Soome.JFinOS.failisüsteem.실행파일적재기;
import Soome.JFinOS.failisüsteem.failisüsteem;
import Soome.JFinOS.failisüsteem.Fail_teave;
import Soome.JFinOS.tuum.하드웨어;
import Soome.JFinOS.입력.입력관리자;
import Soome.JFinOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int kirjutuskaitstud_lipp = 0;
    public static final int Otsi_START = 0;
    public static final int Otsi_tähtaja_piires = 1;
    public static final int FIND_kirje_lõpeta_kõne = 2;

    private final failisüsteem failisüsteem;
    private final 쪽관리자 쪽관리;
    private final plaanija plaanija;
    private final 실행파일적재기 laadur = new 실행파일적재기();
    private final 하드웨어 seade_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(failisüsteem failisüsteem, 쪽관리자 쪽관리, plaanija plaanija, 하드웨어 seade_VALUE, 입력관리자 입력관리) {
        this.failisüsteem = failisüsteem;
        this.쪽관리 = 쪽관리;
        this.plaanija = plaanija;
        this.seade_VALUE = seade_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Joonis_identifikaator(Joonis_VALUE tähtaja_piires_Joonis) {
        return tähtaja_piires_Joonis.identifikaator_VALUE();
    }

    public int ema_Joonis_identifikaator(Joonis_VALUE tähtaja_piires_Joonis) {
        return tähtaja_piires_Joonis.ema_identifikaator();
    }

    public int Ava(Joonis_VALUE tähtaja_piires_Joonis, String Nimi_2, int lipp_VALUE) {
        if (lipp_VALUE != kirjutuskaitstud_lipp) {
            return -30;
        }
        return tähtaja_piires_Joonis.파일서술자().Ava(Nimi_2);
    }

    public int Lugemine(Joonis_VALUE tähtaja_piires_Joonis, int 서술자, byte[] saama_sihtkoht, int Suurus) {
        if (서술자 == 0) {
            if (Suurus <= 0 || saama_sihtkoht.length == 0) {
                return 0;
            }
            입력사건 Sündmus = 입력관리.Edasi_sündmus();
            if (Sündmus == null || Sündmus.sündmuse_liik() != 입력사건.종류.Võti_rikkis) {
                return -11;
            }
            saama_sihtkoht[0] = (byte) Sündmus.첫째값();
            return 1;
        }
        return tähtaja_piires_Joonis.파일서술자().Lugemine(서술자, saama_sihtkoht, Suurus);
    }

    public int Kirjutamine(Joonis_VALUE tähtaja_piires_Joonis, int 서술자, byte[] andmed, int Suurus) {
        if (서술자 != 1 && 서술자 != 2) {
            return tähtaja_piires_Joonis.파일서술자().infotehnoloogia_avama(서술자) ? -30 : -9;
        }
        if (Suurus < 0 || Suurus > andmed.length) {
            return -22;
        }
        seade_VALUE.직렬출력(new String(andmed, 0, Suurus, java.nio.charset.StandardCharsets.UTF_8));
        return Suurus;
    }

    public int Suletud(Joonis_VALUE tähtaja_piires_Joonis, int 서술자) {
        return tähtaja_piires_Joonis.파일서술자().Suletud(서술자);
    }

    public int liigutama_ametikoht(Joonis_VALUE tähtaja_piires_Joonis, int 서술자, int 거리, int Project_juur) {
        return tähtaja_piires_Joonis.파일서술자().liigutama_ametikoht(서술자, 거리, Project_juur);
    }

    public int 서술자복제(Joonis_VALUE tähtaja_piires_Joonis, int 서술자) {
        return tähtaja_piires_Joonis.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Joonis_VALUE tähtaja_piires_Joonis, int 서술자, int 새서술자) {
        return tähtaja_piires_Joonis.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Nimi_2, int meetod_MODE) {
        Fail_teave msinfo32_exe = failisüsteem.msinfo32_exe(Nimi_2);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((meetod_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((meetod_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_ülesandeloend(String Nimi_2) {
        return "/".equals(Nimi_2) ? 0 : -20;
    }

    public String tähtaja_piires_ülesandeloend(int saama_suurust_muutma) {
        return saama_suurust_muutma >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int tõhus_UID() { return 0; }
    public int Rühm_identifikaator() { return 0; }
    public int tõhus_Rühm_identifikaator() { return 0; }

    public int sünkroonima_Fail(Joonis_VALUE tähtaja_piires_Joonis, int 서술자) {
        return tähtaja_piires_Joonis.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // tähtaja_piires_kaup 파일체계는 Lugemine 전용이어서 밀어낼 자료가 없다.
    }

    public boolean infotehnoloogia_terminal(Joonis_VALUE tähtaja_piires_Joonis, int 서술자) {
        Fail_teave msinfo32_exe = tähtaja_piires_Joonis.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int Fail_meede(Joonis_VALUE tähtaja_piires_Joonis, int 서술자, int Käsk, int parameeter_argument) {
        if (Käsk == 0) {
            return tähtaja_piires_Joonis.파일서술자().복제서술자(서술자, parameeter_argument);
        }
        if (Käsk == 1) {
            return tähtaja_piires_Joonis.파일서술자().실행시닫기값(서술자);
        }
        if (Käsk == 2) {
            return tähtaja_piires_Joonis.파일서술자().실행시닫기설정(서술자, (parameeter_argument & 1) != 0);
        }
        if (Käsk == 3) {
            return tähtaja_piires_Joonis.파일서술자().msinfo32_exe(서술자) == null ? -9 : kirjutuskaitstud_lipp;
        }
        if (Käsk == 4) {
            return parameeter_argument == kirjutuskaitstud_lipp ? 0 : -30;
        }
        return -22;
    }

    public int avama_kirje(String Nimi_2, int luba_VALUE) {
        return -30;
    }

    public Fail_teave 서술자정보(Joonis_VALUE tähtaja_piires_Joonis, int 서술자) {
        return tähtaja_piires_Joonis.파일서술자().msinfo32_exe(서술자);
    }

    public süsteem_Üksikasjad süsteem_Üksikasjad() {
        return new süsteem_Üksikasjad("JFinOS", "JFinOS", "0.1", "Java managed kernel", "i386");
    }

    public Fail_teave Fail_teave(String Nimi_2) {
        return failisüsteem.msinfo32_exe(Nimi_2);
    }

    public Joonis_VALUE kloon_Joonis(Joonis_VALUE ema_VALUE) {
        return plaanija.kloon_VALUE(ema_VALUE);
    }

    public int 자식기다리기(Joonis_VALUE ema_VALUE, int laps_identifikaator, boolean 기다리지않음) {
        return plaanija.자식기다리기(ema_VALUE, laps_identifikaator, 기다리지않음);
    }

    public int programm_vaheaeg(Joonis_VALUE tähtaja_piires_Joonis, int 새끝) {
        int 이전끝 = tähtaja_piires_Joonis.programm_vaheaeg();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / 쪽관리자.lehekülje_suurus;
        int 끝쪽 = (새끝 + 쪽관리자.lehekülje_suurus - 1) / 쪽관리자.lehekülje_suurus;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * 쪽관리자.lehekülje_suurus;
                try {
                    쪽관리.바이트읽기(tähtaja_piires_Joonis.ADDRESS_ruum(), ADDRESS);
                } catch (IllegalStateException VIGA) {
                    쪽관리.MAP_leht(tähtaja_piires_Joonis.ADDRESS_ruum(), ADDRESS, true);
                }
            }
        }
        tähtaja_piires_Joonis.hulk_programm_vaheaeg(새끝);
        return 새끝;
    }

    public int lisandumine_programm_vaheaeg(Joonis_VALUE tähtaja_piires_Joonis, int samm_kogus) {
        int 이전끝 = tähtaja_piires_Joonis.programm_vaheaeg();
        int TULEMUS = programm_vaheaeg(tähtaja_piires_Joonis, 이전끝 + samm_kogus);
        return TULEMUS < 0 ? TULEMUS : 이전끝;
    }

    public int Täida_käsk(Joonis_VALUE tähtaja_piires_Joonis, byte[] 실행파일) {
        return Täida_käsk(tähtaja_piires_Joonis, 실행파일, new String[0], new String[0]);
    }

    public int Täida_käsk(Joonis_VALUE tähtaja_piires_Joonis, byte[] 실행파일, String[] parameeter_argument, String[] 환경) {
        실행파일적재기.pilt pilt_VALUE;
        try {
            pilt_VALUE = laadur.검사(실행파일);
        } catch (IllegalArgumentException VIGA) {
            return -8;
        }
        if (parameeter_argument == null || 환경 == null || parameeter_argument.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.jaotis_VALUE jaotis_VALUE : pilt_VALUE.구역들()) {
            if ((jaotis_VALUE.lipp_VALUE() & 2) == 0 || jaotis_VALUE.Suurus() == 0) {
                continue;
            }
            int 첫쪽 = jaotis_VALUE.ADDRESS() / 쪽관리자.lehekülje_suurus;
            int 끝쪽 = (jaotis_VALUE.ADDRESS() + jaotis_VALUE.Suurus() + 쪽관리자.lehekülje_suurus - 1) / 쪽관리자.lehekülje_suurus;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * 쪽관리자.lehekülje_suurus;
                try {
                    쪽관리.바이트읽기(tähtaja_piires_Joonis.ADDRESS_ruum(), ADDRESS);
                    쪽관리.era_vahemik_kirjutamine(tähtaja_piires_Joonis.ADDRESS_ruum(), ADDRESS, 쪽관리자.lehekülje_suurus);
                } catch (IllegalStateException VIGA) {
                    쪽관리.MAP_leht(tähtaja_piires_Joonis.ADDRESS_ruum(), ADDRESS, true);
                }
            }
            for (int INDEX = 0; INDEX < jaotis_VALUE.Suurus(); INDEX++) {
                byte VALUE = jaotis_VALUE.종류() == 8 ? 0 : 실행파일[jaotis_VALUE.Fail_ametikoht() + INDEX];
                쪽관리.kirjutamine_bait_VALUE(tähtaja_piires_Joonis.ADDRESS_ruum(), jaotis_VALUE.ADDRESS() + INDEX, VALUE);
            }
        }
        tähtaja_piires_Joonis.실행문맥설정(pilt_VALUE.START_ADDRESS(), parameeter_argument, 환경);
        tähtaja_piires_Joonis.파일서술자().실행시닫기();
        return 0;
    }

    public void välju_programm(Joonis_VALUE tähtaja_piires_Joonis, int Olek_VALUE) {
        tähtaja_piires_Joonis.Välju_programm(Olek_VALUE);
    }
}
