// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frantzia.JFraOS.체계호출;

import Frantzia.JFraOS.기억공간.orri_kudeatzaile;
import Frantzia.JFraOS.작업.prozesu_balio;
import Frantzia.JFraOS.작업.Antolatzailea;
import Frantzia.JFraOS.fitxategi_sistema.실행파일적재기;
import Frantzia.JFraOS.fitxategi_sistema.fitxategi_sistema;
import Frantzia.JFraOS.fitxategi_sistema.fitxategi_info;
import Frantzia.JFraOS.nukleo.하드웨어;
import Frantzia.JFraOS.입력.입력관리자;
import Frantzia.JFraOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int irakurtzeko_soilik_marka = 0;
    public static final int BILATU_HASI = 0;
    public static final int 찾기현재 = 1;
    public static final int Bilatu_sarrera_amaitu = 2;

    private final fitxategi_sistema fitxategi_sistema;
    private final orri_kudeatzaile 쪽관리;
    private final Antolatzailea Antolatzailea;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 gailu_balio;
    private final 입력관리자 입력관리;

    public 체계호출(fitxategi_sistema fitxategi_sistema, orri_kudeatzaile 쪽관리, Antolatzailea Antolatzailea, 하드웨어 gailu_balio, 입력관리자 입력관리) {
        this.fitxategi_sistema = fitxategi_sistema;
        this.쪽관리 = 쪽관리;
        this.Antolatzailea = Antolatzailea;
        this.gailu_balio = gailu_balio;
        this.입력관리 = 입력관리;
    }

    public int prozesu_identifikatzaile(prozesu_balio 현재과정) {
        return 현재과정.identifikatzaile_balio();
    }

    public int 부모과정식별자(prozesu_balio 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Ireki(prozesu_balio 현재과정, String Izena, int marka_balio) {
        if (marka_balio != irakurtzeko_soilik_marka) {
            return -30;
        }
        return 현재과정.파일서술자().Ireki(Izena);
    }

    public int Irakurri(prozesu_balio 현재과정, int 서술자, byte[] 받을곳, int Tamaina) {
        if (서술자 == 0) {
            if (Tamaina <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 Gertaera = 입력관리.Hurrengoa_gertaera();
            if (Gertaera == null || Gertaera.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) Gertaera.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Irakurri(서술자, 받을곳, Tamaina);
    }

    public int Idatzi(prozesu_balio 현재과정, int 서술자, byte[] datuak, int Tamaina) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().informatika_ireki(서술자) ? -30 : -9;
        }
        if (Tamaina < 0 || Tamaina > datuak.length) {
            return -22;
        }
        gailu_balio.직렬출력(new String(datuak, 0, Tamaina, java.nio.charset.StandardCharsets.UTF_8));
        return Tamaina;
    }

    public int Itxi(prozesu_balio 현재과정, int 서술자) {
        return 현재과정.파일서술자().Itxi(서술자);
    }

    public int eraman_kargu(prozesu_balio 현재과정, int 서술자, int 거리, int Project_erro) {
        return 현재과정.파일서술자().eraman_kargu(서술자, 거리, Project_erro);
    }

    public int 서술자복제(prozesu_balio 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(prozesu_balio 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Izena, int 방식) {
        fitxategi_info msinfo32_exe = fitxategi_sistema.msinfo32_exe(Izena);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((방식 & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((방식 & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int ALDATU_zeregin_zerrenda(String Izena) {
        return "/".equals(Izena) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int erabiltzaile_ID() { return 0; }
    public int eraginkor_erabiltzaile_ID() { return 0; }
    public int talde_identifikatzaile() { return 0; }
    public int eraginkor_talde_identifikatzaile() { return 0; }

    public int sinkronizatu_fitxategi(prozesu_balio 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Irakurri 전용이어서 밀어낼 자료가 없다.
    }

    public boolean informatika_Terminal(prozesu_balio 현재과정, int 서술자) {
        fitxategi_info msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int fitxategi_kontrol(prozesu_balio 현재과정, int 서술자, int Komandoa, int parametro_arg) {
        if (Komandoa == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, parametro_arg);
        }
        if (Komandoa == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Komandoa == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (parametro_arg & 1) != 0);
        }
        if (Komandoa == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : irakurtzeko_soilik_marka;
        }
        if (Komandoa == 4) {
            return parametro_arg == irakurtzeko_soilik_marka ? 0 : -30;
        }
        return -22;
    }

    public int sortu_sarrera(String Izena, int baimen_balio) {
        return -30;
    }

    public fitxategi_info 서술자정보(prozesu_balio 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public sistema_Xehetasunak sistema_Xehetasunak() {
        return new sistema_Xehetasunak("JFraOS", "JFraOS", "0.1", "Java managed kernel", "i386");
    }

    public fitxategi_info fitxategi_info(String Izena) {
        return fitxategi_sistema.msinfo32_exe(Izena);
    }

    public prozesu_balio klon_prozesu(prozesu_balio 부모) {
        return Antolatzailea.klon_balio(부모);
    }

    public int 자식기다리기(prozesu_balio 부모, int haur_identifikatzaile, boolean 기다리지않음) {
        return Antolatzailea.자식기다리기(부모, haur_identifikatzaile, 기다리지않음);
    }

    public int aplik_atseden(prozesu_balio 현재과정, int 새끝) {
        int 이전끝 = 현재과정.aplik_atseden();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / orri_kudeatzaile.orrialdearen_tamaina;
        int 끝쪽 = (새끝 + orri_kudeatzaile.orrialdearen_tamaina - 1) / orri_kudeatzaile.orrialdearen_tamaina;
        if (새끝 > 이전끝) {
            for (int INDIZE = 첫쪽; INDIZE < 끝쪽; INDIZE++) {
                int helbide = INDIZE * orri_kudeatzaile.orrialdearen_tamaina;
                try {
                    쪽관리.바이트읽기(현재과정.helbide_gune(), helbide);
                } catch (IllegalStateException errorea) {
                    쪽관리.MAP_orri(현재과정.helbide_gune(), helbide, true);
                }
            }
        }
        현재과정.sorta_aplik_atseden(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(prozesu_balio 현재과정, int 증가량) {
        int 이전끝 = 현재과정.aplik_atseden();
        int EMAITZA = aplik_atseden(현재과정, 이전끝 + 증가량);
        return EMAITZA < 0 ? EMAITZA : 이전끝;
    }

    public int exekutatu_komando(prozesu_balio 현재과정, byte[] 실행파일) {
        return exekutatu_komando(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int exekutatu_komando(prozesu_balio 현재과정, byte[] 실행파일, String[] parametro_arg, String[] 환경) {
        실행파일적재기.irudi irudi_balio;
        try {
            irudi_balio = 적재기.검사(실행파일);
        } catch (IllegalArgumentException errorea) {
            return -8;
        }
        if (parametro_arg == null || 환경 == null || parametro_arg.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.sekzio_balio sekzio_balio : irudi_balio.구역들()) {
            if ((sekzio_balio.marka_balio() & 2) == 0 || sekzio_balio.Tamaina() == 0) {
                continue;
            }
            int 첫쪽 = sekzio_balio.helbide() / orri_kudeatzaile.orrialdearen_tamaina;
            int 끝쪽 = (sekzio_balio.helbide() + sekzio_balio.Tamaina() + orri_kudeatzaile.orrialdearen_tamaina - 1) / orri_kudeatzaile.orrialdearen_tamaina;
            for (int INDIZE = 첫쪽; INDIZE < 끝쪽; INDIZE++) {
                int helbide = INDIZE * orri_kudeatzaile.orrialdearen_tamaina;
                try {
                    쪽관리.바이트읽기(현재과정.helbide_gune(), helbide);
                    쪽관리.Pribatu_barruti_idatzi(현재과정.helbide_gune(), helbide, orri_kudeatzaile.orrialdearen_tamaina);
                } catch (IllegalStateException errorea) {
                    쪽관리.MAP_orri(현재과정.helbide_gune(), helbide, true);
                }
            }
            for (int INDIZE = 0; INDIZE < sekzio_balio.Tamaina(); INDIZE++) {
                byte balio = sekzio_balio.종류() == 8 ? 0 : 실행파일[sekzio_balio.fitxategi_kargu() + INDIZE];
                쪽관리.idatzi_byte_balio(현재과정.helbide_gune(), sekzio_balio.helbide() + INDIZE, balio);
            }
        }
        현재과정.실행문맥설정(irudi_balio.HASI_helbide(), parametro_arg, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void irten_aplik_55b3a1cd(prozesu_balio 현재과정, int Egoera_balio) {
        현재과정.irten_aplik(Egoera_balio);
    }
}
