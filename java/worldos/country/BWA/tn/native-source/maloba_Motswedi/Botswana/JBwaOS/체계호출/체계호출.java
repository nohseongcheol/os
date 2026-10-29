// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.체계호출;

import Botswana.JBwaOS.기억공간.tsebe_motsamaisi;
import Botswana.JBwaOS.작업.Thulaganyo_Boleng;
import Botswana.JBwaOS.작업.배정기;
import Botswana.JBwaOS.setsamaisadifaele.실행파일적재기;
import Botswana.JBwaOS.setsamaisadifaele.setsamaisadifaele;
import Botswana.JBwaOS.setsamaisadifaele.faele_tshedimosetso;
import Botswana.JBwaOS.Khenele.하드웨어;
import Botswana.JBwaOS.입력.입력관리자;
import Botswana.JBwaOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int puiso_fela_folaga = 0;
    public static final int batla_simolola = 0;
    public static final int batla_ga_jaana = 1;
    public static final int batla_tsenyo_kgaola = 2;

    private final setsamaisadifaele setsamaisadifaele;
    private final tsebe_motsamaisi 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 mobaele_Boleng;
    private final 입력관리자 입력관리;

    public 체계호출(setsamaisadifaele setsamaisadifaele, tsebe_motsamaisi 쪽관리, 배정기 배정기, 하드웨어 mobaele_Boleng, 입력관리자 입력관리) {
        this.setsamaisadifaele = setsamaisadifaele;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.mobaele_Boleng = mobaele_Boleng;
        this.입력관리 = 입력관리;
    }

    public int Thulaganyo_setlhaodi(Thulaganyo_Boleng ga_jaana_Thulaganyo) {
        return ga_jaana_Thulaganyo.setlhaodi_Boleng();
    }

    public int 부모과정식별자(Thulaganyo_Boleng ga_jaana_Thulaganyo) {
        return ga_jaana_Thulaganyo.부모식별자();
    }

    public int bula(Thulaganyo_Boleng ga_jaana_Thulaganyo, String leina, int folaga_Boleng) {
        if (folaga_Boleng != puiso_fela_folaga) {
            return -30;
        }
        return ga_jaana_Thulaganyo.파일서술자().bula(leina);
    }

    public int 읽기(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 서술자, byte[] 받을곳, int lekanya) {
        if (서술자 == 0) {
            if (lekanya <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 tiragalo = 입력관리.다음사건();
            if (tiragalo == null || tiragalo.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) tiragalo.첫째값();
            return 1;
        }
        return ga_jaana_Thulaganyo.파일서술자().읽기(서술자, 받을곳, lekanya);
    }

    public int kwala(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 서술자, byte[] tshedimosetso, int lekanya) {
        if (서술자 != 1 && 서술자 != 2) {
            return ga_jaana_Thulaganyo.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (lekanya < 0 || lekanya > tshedimosetso.length) {
            return -22;
        }
        mobaele_Boleng.직렬출력(new String(tshedimosetso, 0, lekanya, java.nio.charset.StandardCharsets.UTF_8));
        return lekanya;
    }

    public int tswala(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 서술자) {
        return ga_jaana_Thulaganyo.파일서술자().tswala(서술자);
    }

    public int 위치옮기기(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 서술자, int 거리, int 기준) {
        return ga_jaana_Thulaganyo.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 서술자) {
        return ga_jaana_Thulaganyo.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 서술자, int 새서술자) {
        return ga_jaana_Thulaganyo.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String leina, int mokgwa_mokgwa) {
        faele_tshedimosetso msinfo32_exe = setsamaisadifaele.msinfo32_exe(leina);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((mokgwa_mokgwa & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((mokgwa_mokgwa & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int fetola_lenaneotiro(String leina) {
        return "/".equals(leina) ? 0 : -20;
    }

    public String ga_jaana_lenaneotiro(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int modirisi_setlhaodi() { return 0; }
    public int kgonang_modirisi_setlhaodi() { return 0; }
    public int setlhopha_setlhaodi() { return 0; }
    public int kgonang_setlhopha_setlhaodi() { return 0; }

    public int tsamaisanya_faele(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 서술자) {
        return ga_jaana_Thulaganyo.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // ga_jaana_selwana 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 서술자) {
        faele_tshedimosetso msinfo32_exe = ga_jaana_Thulaganyo.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int faele_taolo(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 서술자, int Taelo, int 인자) {
        if (Taelo == 0) {
            return ga_jaana_Thulaganyo.파일서술자().복제서술자(서술자, 인자);
        }
        if (Taelo == 1) {
            return ga_jaana_Thulaganyo.파일서술자().실행시닫기값(서술자);
        }
        if (Taelo == 2) {
            return ga_jaana_Thulaganyo.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (Taelo == 3) {
            return ga_jaana_Thulaganyo.파일서술자().msinfo32_exe(서술자) == null ? -9 : puiso_fela_folaga;
        }
        if (Taelo == 4) {
            return 인자 == puiso_fela_folaga ? 0 : -30;
        }
        return -22;
    }

    public int tlhama_tsenyo(String leina, int tetla_Boleng) {
        return -30;
    }

    public faele_tshedimosetso 서술자정보(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 서술자) {
        return ga_jaana_Thulaganyo.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JBwaOS", "JBwaOS", "0.1", "Java managed kernel", "i386");
    }

    public faele_tshedimosetso faele_tshedimosetso(String leina) {
        return setsamaisadifaele.msinfo32_exe(leina);
    }

    public Thulaganyo_Boleng 과정복제(Thulaganyo_Boleng 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(Thulaganyo_Boleng 부모, int ngwana_setlhaodi, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, ngwana_setlhaodi, 기다리지않음);
    }

    public int 프로그램끝(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 새끝) {
        int 이전끝 = ga_jaana_Thulaganyo.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / tsebe_motsamaisi.bogolo_jwa_tsebe;
        int 끝쪽 = (새끝 + tsebe_motsamaisi.bogolo_jwa_tsebe - 1) / tsebe_motsamaisi.bogolo_jwa_tsebe;
        if (새끝 > 이전끝) {
            for (int tshupane = 첫쪽; tshupane < 끝쪽; tshupane++) {
                int aterese = tshupane * tsebe_motsamaisi.bogolo_jwa_tsebe;
                try {
                    쪽관리.바이트읽기(ga_jaana_Thulaganyo.aterese_sebaka(), aterese);
                } catch (IllegalStateException phoso) {
                    쪽관리.mepa_tsebe(ga_jaana_Thulaganyo.aterese_sebaka(), aterese, true);
                }
            }
        }
        ga_jaana_Thulaganyo.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Thulaganyo_Boleng ga_jaana_Thulaganyo, int 증가량) {
        int 이전끝 = ga_jaana_Thulaganyo.프로그램끝();
        int 결과 = 프로그램끝(ga_jaana_Thulaganyo, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int diragatsa_Taelo(Thulaganyo_Boleng ga_jaana_Thulaganyo, byte[] 실행파일) {
        return diragatsa_Taelo(ga_jaana_Thulaganyo, 실행파일, new String[0], new String[0]);
    }

    public int diragatsa_Taelo(Thulaganyo_Boleng ga_jaana_Thulaganyo, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.Setshwantsho Setshwantsho_Boleng;
        try {
            Setshwantsho_Boleng = 적재기.검사(실행파일);
        } catch (IllegalArgumentException phoso) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.karolo_Boleng karolo_Boleng : Setshwantsho_Boleng.구역들()) {
            if ((karolo_Boleng.folaga_Boleng() & 2) == 0 || karolo_Boleng.lekanya() == 0) {
                continue;
            }
            int 첫쪽 = karolo_Boleng.aterese() / tsebe_motsamaisi.bogolo_jwa_tsebe;
            int 끝쪽 = (karolo_Boleng.aterese() + karolo_Boleng.lekanya() + tsebe_motsamaisi.bogolo_jwa_tsebe - 1) / tsebe_motsamaisi.bogolo_jwa_tsebe;
            for (int tshupane = 첫쪽; tshupane < 끝쪽; tshupane++) {
                int aterese = tshupane * tsebe_motsamaisi.bogolo_jwa_tsebe;
                try {
                    쪽관리.바이트읽기(ga_jaana_Thulaganyo.aterese_sebaka(), aterese);
                    쪽관리.범위개인쓰기(ga_jaana_Thulaganyo.aterese_sebaka(), aterese, tsebe_motsamaisi.bogolo_jwa_tsebe);
                } catch (IllegalStateException phoso) {
                    쪽관리.mepa_tsebe(ga_jaana_Thulaganyo.aterese_sebaka(), aterese, true);
                }
            }
            for (int tshupane = 0; tshupane < karolo_Boleng.lekanya(); tshupane++) {
                byte Boleng = karolo_Boleng.종류() == 8 ? 0 : 실행파일[karolo_Boleng.파일위치() + tshupane];
                쪽관리.kwala_baete_Boleng(ga_jaana_Thulaganyo.aterese_sebaka(), karolo_Boleng.aterese() + tshupane, Boleng);
            }
        }
        ga_jaana_Thulaganyo.실행문맥설정(Setshwantsho_Boleng.simolola_aterese(), 인자, 환경);
        ga_jaana_Thulaganyo.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(Thulaganyo_Boleng ga_jaana_Thulaganyo, int kemo_Boleng) {
        ga_jaana_Thulaganyo.tswaya_Tiriso(kemo_Boleng);
    }
}
