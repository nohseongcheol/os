// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.체계호출;

import Canada.JCanOS.기억공간.page_tagapamahala;
import Canada.JCanOS.작업.Proseso_VALUE;
import Canada.JCanOS.작업.Scheduler;
import Canada.JCanOS.sistema_ng_file.실행파일적재기;
import Canada.JCanOS.sistema_ng_file.sistema_ng_file;
import Canada.JCanOS.sistema_ng_file.file_impormasyon;
import Canada.JCanOS.kernel.하드웨어;
import Canada.JCanOS.입력.입력관리자;
import Canada.JCanOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int mababasa_lamang_i_flag = 0;
    public static final int SEARCH_Start = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_pagpasok_tapusin = 2;

    private final sistema_ng_file sistema_ng_file;
    private final page_tagapamahala 쪽관리;
    private final Scheduler Scheduler;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 device_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(sistema_ng_file sistema_ng_file, page_tagapamahala 쪽관리, Scheduler Scheduler, 하드웨어 device_VALUE, 입력관리자 입력관리) {
        this.sistema_ng_file = sistema_ng_file;
        this.쪽관리 = 쪽관리;
        this.Scheduler = Scheduler;
        this.device_VALUE = device_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Proseso_tagakilala(Proseso_VALUE 현재과정) {
        return 현재과정.tagakilala_VALUE();
    }

    public int 부모과정식별자(Proseso_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int buksan(Proseso_VALUE 현재과정, String pangalan, int i_flag_VALUE) {
        if (i_flag_VALUE != mababasa_lamang_i_flag) {
            return -30;
        }
        return 현재과정.파일서술자().buksan(pangalan);
    }

    public int 읽기(Proseso_VALUE 현재과정, int 서술자, byte[] 받을곳, int sukat_82232621) {
        if (서술자 == 0) {
            if (sukat_82232621 <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 kaganapan = 입력관리.Susunod_kaganapan();
            if (kaganapan == null || kaganapan.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) kaganapan.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, sukat_82232621);
    }

    public int sumulat(Proseso_VALUE 현재과정, int 서술자, byte[] data, int sukat_82232621) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().information_technology_buksan(서술자) ? -30 : -9;
        }
        if (sukat_82232621 < 0 || sukat_82232621 > data.length) {
            return -22;
        }
        device_VALUE.직렬출력(new String(data, 0, sukat_82232621, java.nio.charset.StandardCharsets.UTF_8));
        return sukat_82232621;
    }

    public int isara(Proseso_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().isara(서술자);
    }

    public int ilipat_posisyon(Proseso_VALUE 현재과정, int 서술자, int 거리, int Project_root) {
        return 현재과정.파일서술자().ilipat_posisyon(서술자, 거리, Project_root);
    }

    public int 서술자복제(Proseso_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proseso_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String pangalan, int pamamaraan_MODE) {
        file_impormasyon msinfo32_exe = sistema_ng_file.msinfo32_exe(pangalan);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((pamamaraan_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((pamamaraan_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_listahan_ng_gawain(String pangalan) {
        return "/".equals(pangalan) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int gumagamit_tagakilala() { return 0; }
    public int epektibo_gumagamit_tagakilala() { return 0; }
    public int Grupo_tagakilala() { return 0; }
    public int epektibo_Grupo_tagakilala() { return 0; }

    public int iakma_file(Proseso_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean information_technology_Terminal(Proseso_VALUE 현재과정, int 서술자) {
        file_impormasyon msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int file_control(Proseso_VALUE 현재과정, int 서술자, int utos, int parameter_argumento) {
        if (utos == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, parameter_argumento);
        }
        if (utos == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (utos == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (parameter_argumento & 1) != 0);
        }
        if (utos == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : mababasa_lamang_i_flag;
        }
        if (utos == 4) {
            return parameter_argumento == mababasa_lamang_i_flag ? 0 : -30;
        }
        return -22;
    }

    public int Create_pagpasok(String pangalan, int pahintulot_VALUE) {
        return -30;
    }

    public file_impormasyon 서술자정보(Proseso_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JCanOS", "JCanOS", "0.1", "Java managed kernel", "i386");
    }

    public file_impormasyon file_impormasyon(String pangalan) {
        return sistema_ng_file.msinfo32_exe(pangalan);
    }

    public Proseso_VALUE 과정복제(Proseso_VALUE 부모) {
        return Scheduler.복제(부모);
    }

    public int 자식기다리기(Proseso_VALUE 부모, int anak_tagakilala, boolean 기다리지않음) {
        return Scheduler.자식기다리기(부모, anak_tagakilala, 기다리지않음);
    }

    public int app_break(Proseso_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.app_break();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / page_tagapamahala.laki_ng_pahina;
        int 끝쪽 = (새끝 + page_tagapamahala.laki_ng_pahina - 1) / page_tagapamahala.laki_ng_pahina;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int email = INDEX * page_tagapamahala.laki_ng_pahina;
                try {
                    쪽관리.바이트읽기(현재과정.email_SPACE(), email);
                } catch (IllegalStateException error) {
                    쪽관리.MAP_page(현재과정.email_SPACE(), email, true);
                }
            }
        }
        현재과정.set_app_break(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Proseso_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.app_break();
        int sukat = app_break(현재과정, 이전끝 + 증가량);
        return sukat < 0 ? sukat : 이전끝;
    }

    public int Mag_execute_utos(Proseso_VALUE 현재과정, byte[] 실행파일) {
        return Mag_execute_utos(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int Mag_execute_utos(Proseso_VALUE 현재과정, byte[] 실행파일, String[] parameter_argumento, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException error) {
            return -8;
        }
        if (parameter_argumento == null || 환경 == null || parameter_argumento.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.seksiyon_VALUE seksiyon_VALUE : IMAGE_VALUE.구역들()) {
            if ((seksiyon_VALUE.i_flag_VALUE() & 2) == 0 || seksiyon_VALUE.sukat_82232621() == 0) {
                continue;
            }
            int 첫쪽 = seksiyon_VALUE.email() / page_tagapamahala.laki_ng_pahina;
            int 끝쪽 = (seksiyon_VALUE.email() + seksiyon_VALUE.sukat_82232621() + page_tagapamahala.laki_ng_pahina - 1) / page_tagapamahala.laki_ng_pahina;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int email = INDEX * page_tagapamahala.laki_ng_pahina;
                try {
                    쪽관리.바이트읽기(현재과정.email_SPACE(), email);
                    쪽관리.범위개인쓰기(현재과정.email_SPACE(), email, page_tagapamahala.laki_ng_pahina);
                } catch (IllegalStateException error) {
                    쪽관리.MAP_page(현재과정.email_SPACE(), email, true);
                }
            }
            for (int INDEX = 0; INDEX < seksiyon_VALUE.sukat_82232621(); INDEX++) {
                byte VALUE = seksiyon_VALUE.종류() == 8 ? 0 : 실행파일[seksiyon_VALUE.file_posisyon() + INDEX];
                쪽관리.sumulat_byte_VALUE(현재과정.email_SPACE(), seksiyon_VALUE.email() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(IMAGE_VALUE.Start_email(), parameter_argumento, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void lumabas_app(Proseso_VALUE 현재과정, int katayuan_VALUE) {
        현재과정.Paglabas_app(katayuan_VALUE);
    }
}
