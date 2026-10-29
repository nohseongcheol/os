// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.체계호출;

import Noreg.JNorOS.기억공간.side_leiar;
import Noreg.JNorOS.작업.Prosess_VALUE;
import Noreg.JNorOS.작업.Planleggjar;
import Noreg.JNorOS.filsystem.실행파일적재기;
import Noreg.JNorOS.filsystem.filsystem;
import Noreg.JNorOS.filsystem.fil_informasjon;
import Noreg.JNorOS.kjerne.하드웨어;
import Noreg.JNorOS.입력.입력관리자;
import Noreg.JNorOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int skriveverna_flagg = 0;
    public static final int Søk_START = 0;
    public static final int Søk_betalt = 1;
    public static final int Søk_oppføring_avslutte = 2;

    private final filsystem filsystem;
    private final side_leiar 쪽관리;
    private final Planleggjar Planleggjar;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 mobil_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(filsystem filsystem, side_leiar 쪽관리, Planleggjar Planleggjar, 하드웨어 mobil_VALUE, 입력관리자 입력관리) {
        this.filsystem = filsystem;
        this.쪽관리 = 쪽관리;
        this.Planleggjar = Planleggjar;
        this.mobil_VALUE = mobil_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Prosess_identifikator(Prosess_VALUE betalt_Prosess) {
        return betalt_Prosess.identifikator_VALUE();
    }

    public int forelder_Prosess_identifikator(Prosess_VALUE betalt_Prosess) {
        return betalt_Prosess.forelder_identifikator();
    }

    public int Opna(Prosess_VALUE betalt_Prosess, String Namn, int flagg_VALUE) {
        if (flagg_VALUE != skriveverna_flagg) {
            return -30;
        }
        return betalt_Prosess.파일서술자().Opna(Namn);
    }

    public int Les(Prosess_VALUE betalt_Prosess, int 서술자, byte[] 받을곳, int Storleik) {
        if (서술자 == 0) {
            if (Storleik <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 Hending = 입력관리.Neste_hending();
            if (Hending == null || Hending.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) Hending.첫째값();
            return 1;
        }
        return betalt_Prosess.파일서술자().Les(서술자, 받을곳, Storleik);
    }

    public int Skriv(Prosess_VALUE betalt_Prosess, int 서술자, byte[] data, int Storleik) {
        if (서술자 != 1 && 서술자 != 2) {
            return betalt_Prosess.파일서술자().informasjonsteknologi_opne(서술자) ? -30 : -9;
        }
        if (Storleik < 0 || Storleik > data.length) {
            return -22;
        }
        mobil_VALUE.직렬출력(new String(data, 0, Storleik, java.nio.charset.StandardCharsets.UTF_8));
        return Storleik;
    }

    public int Lukk(Prosess_VALUE betalt_Prosess, int 서술자) {
        return betalt_Prosess.파일서술자().Lukk(서술자);
    }

    public int flytte_plassere(Prosess_VALUE betalt_Prosess, int 서술자, int 거리, int spegle_rot) {
        return betalt_Prosess.파일서술자().flytte_plassere(서술자, 거리, spegle_rot);
    }

    public int 서술자복제(Prosess_VALUE betalt_Prosess, int 서술자) {
        return betalt_Prosess.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Prosess_VALUE betalt_Prosess, int 서술자, int 새서술자) {
        return betalt_Prosess.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Namn, int metode_MODE) {
        fil_informasjon msinfo32_exe = filsystem.msinfo32_exe(Namn);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metode_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metode_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int byte_oppgåveliste(String Namn) {
        return "/".equals(Namn) ? 0 : -20;
    }

    public String betalt_oppgåveliste(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int effektiv_UID() { return 0; }
    public int gruppe_identifikator() { return 0; }
    public int effektiv_gruppe_identifikator() { return 0; }

    public int synkronisere_fil(Prosess_VALUE betalt_Prosess, int 서술자) {
        return betalt_Prosess.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // betalt_vare 파일체계는 Les 전용이어서 밀어낼 자료가 없다.
    }

    public boolean informasjonsteknologi_Terminal(Prosess_VALUE betalt_Prosess, int 서술자) {
        fil_informasjon msinfo32_exe = betalt_Prosess.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int fil_styring(Prosess_VALUE betalt_Prosess, int 서술자, int Kommando, int parameter_argument) {
        if (Kommando == 0) {
            return betalt_Prosess.파일서술자().복제서술자(서술자, parameter_argument);
        }
        if (Kommando == 1) {
            return betalt_Prosess.파일서술자().실행시닫기값(서술자);
        }
        if (Kommando == 2) {
            return betalt_Prosess.파일서술자().실행시닫기설정(서술자, (parameter_argument & 1) != 0);
        }
        if (Kommando == 3) {
            return betalt_Prosess.파일서술자().msinfo32_exe(서술자) == null ? -9 : skriveverna_flagg;
        }
        if (Kommando == 4) {
            return parameter_argument == skriveverna_flagg ? 0 : -30;
        }
        return -22;
    }

    public int Opprett_oppføring(String Namn, int løyve_VALUE) {
        return -30;
    }

    public fil_informasjon 서술자정보(Prosess_VALUE betalt_Prosess, int 서술자) {
        return betalt_Prosess.파일서술자().msinfo32_exe(서술자);
    }

    public system_Detaljar system_Detaljar() {
        return new system_Detaljar("JNorOS", "JNorOS", "0.1", "Java managed kernel", "i386");
    }

    public fil_informasjon fil_informasjon(String Namn) {
        return filsystem.msinfo32_exe(Namn);
    }

    public Prosess_VALUE 과정복제(Prosess_VALUE forelder_VALUE) {
        return Planleggjar.복제(forelder_VALUE);
    }

    public int 자식기다리기(Prosess_VALUE forelder_VALUE, int underordna_identifikator, boolean 기다리지않음) {
        return Planleggjar.자식기다리기(forelder_VALUE, underordna_identifikator, 기다리지않음);
    }

    public int app_pause(Prosess_VALUE betalt_Prosess, int 새끝) {
        int 이전끝 = betalt_Prosess.app_pause();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / side_leiar.sidestorleik;
        int 끝쪽 = (새끝 + side_leiar.sidestorleik - 1) / side_leiar.sidestorleik;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * side_leiar.sidestorleik;
                try {
                    쪽관리.바이트읽기(betalt_Prosess.ADDRESS_område(), ADDRESS);
                } catch (IllegalStateException FEIL) {
                    쪽관리.MAP_side(betalt_Prosess.ADDRESS_område(), ADDRESS, true);
                }
            }
        }
        betalt_Prosess.sett_app_pause(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Prosess_VALUE betalt_Prosess, int 증가량) {
        int 이전끝 = betalt_Prosess.app_pause();
        int forretningsmål = app_pause(betalt_Prosess, 이전끝 + 증가량);
        return forretningsmål < 0 ? forretningsmål : 이전끝;
    }

    public int Utfør_kommando(Prosess_VALUE betalt_Prosess, byte[] 실행파일) {
        return Utfør_kommando(betalt_Prosess, 실행파일, new String[0], new String[0]);
    }

    public int Utfør_kommando(Prosess_VALUE betalt_Prosess, byte[] 실행파일, String[] parameter_argument, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException FEIL) {
            return -8;
        }
        if (parameter_argument == null || 환경 == null || parameter_argument.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.del_VALUE del_VALUE : IMAGE_VALUE.구역들()) {
            if ((del_VALUE.flagg_VALUE() & 2) == 0 || del_VALUE.Storleik() == 0) {
                continue;
            }
            int 첫쪽 = del_VALUE.ADDRESS() / side_leiar.sidestorleik;
            int 끝쪽 = (del_VALUE.ADDRESS() + del_VALUE.Storleik() + side_leiar.sidestorleik - 1) / side_leiar.sidestorleik;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * side_leiar.sidestorleik;
                try {
                    쪽관리.바이트읽기(betalt_Prosess.ADDRESS_område(), ADDRESS);
                    쪽관리.범위개인쓰기(betalt_Prosess.ADDRESS_område(), ADDRESS, side_leiar.sidestorleik);
                } catch (IllegalStateException FEIL) {
                    쪽관리.MAP_side(betalt_Prosess.ADDRESS_område(), ADDRESS, true);
                }
            }
            for (int INDEX = 0; INDEX < del_VALUE.Storleik(); INDEX++) {
                byte VALUE = del_VALUE.종류() == 8 ? 0 : 실행파일[del_VALUE.fil_plassere() + INDEX];
                쪽관리.skrive_byte_VALUE(betalt_Prosess.ADDRESS_område(), del_VALUE.ADDRESS() + INDEX, VALUE);
            }
        }
        betalt_Prosess.실행문맥설정(IMAGE_VALUE.START_ADDRESS(), parameter_argument, 환경);
        betalt_Prosess.파일서술자().실행시닫기();
        return 0;
    }

    public void avslutt_app(Prosess_VALUE betalt_Prosess, int status_VALUE) {
        betalt_Prosess.Utgang_app(status_VALUE);
    }
}
