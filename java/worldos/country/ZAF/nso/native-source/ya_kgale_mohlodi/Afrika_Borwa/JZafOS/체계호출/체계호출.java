// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.체계호출;

import Afrika_Borwa.JZafOS.기억공간.letlakala_molaodi;
import Afrika_Borwa.JZafOS.작업.tiragalo_boleng;
import Afrika_Borwa.JZafOS.작업.배정기;
import Afrika_Borwa.JZafOS.tshepedišo_ya_difaele.실행파일적재기;
import Afrika_Borwa.JZafOS.tshepedišo_ya_difaele.tshepedišo_ya_difaele;
import Afrika_Borwa.JZafOS.tshepedišo_ya_difaele.faele_tshedimošo;
import Afrika_Borwa.JZafOS.khenele.하드웨어;
import Afrika_Borwa.JZafOS.입력.입력관리자;
import Afrika_Borwa.JZafOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int balwago_fela_folaga = 0;
    public static final int Nyaka_Thomišo = 0;
    public static final int 찾기현재 = 1;
    public static final int hwetša_go_tsenya_tshedimošo_fetša = 2;

    private final tshepedišo_ya_difaele tshepedišo_ya_difaele;
    private final letlakala_molaodi 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 sedirišwa_boleng;
    private final 입력관리자 입력관리;

    public 체계호출(tshepedišo_ya_difaele tshepedišo_ya_difaele, letlakala_molaodi 쪽관리, 배정기 배정기, 하드웨어 sedirišwa_boleng, 입력관리자 입력관리) {
        this.tshepedišo_ya_difaele = tshepedišo_ya_difaele;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.sedirišwa_boleng = sedirišwa_boleng;
        this.입력관리 = 입력관리;
    }

    public int tiragalo_sešupi(tiragalo_boleng 현재과정) {
        return 현재과정.sešupi_boleng();
    }

    public int 부모과정식별자(tiragalo_boleng 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Bula(tiragalo_boleng 현재과정, String Leina, int folaga_boleng) {
        if (folaga_boleng != balwago_fela_folaga) {
            return -30;
        }
        return 현재과정.파일서술자().Bula(Leina);
    }

    public int Bala(tiragalo_boleng 현재과정, int 서술자, byte[] 받을곳, int Bogolo) {
        if (서술자 == 0) {
            if (Bogolo <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 tiragalo = 입력관리.다음사건();
            if (tiragalo == null || tiragalo.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) tiragalo.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Bala(서술자, 받을곳, Bogolo);
    }

    public int Ngwala(tiragalo_boleng 현재과정, int 서술자, byte[] data, int Bogolo) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (Bogolo < 0 || Bogolo > data.length) {
            return -22;
        }
        sedirišwa_boleng.직렬출력(new String(data, 0, Bogolo, java.nio.charset.StandardCharsets.UTF_8));
        return Bogolo;
    }

    public int Tswalela(tiragalo_boleng 현재과정, int 서술자) {
        return 현재과정.파일서술자().Tswalela(서술자);
    }

    public int 위치옮기기(tiragalo_boleng 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(tiragalo_boleng 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(tiragalo_boleng 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Leina, int mokgwa_mokgwa) {
        faele_tshedimošo msinfo32_exe = tshepedišo_ya_difaele.msinfo32_exe(Leina);
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

    public int fetogela_lenaneo_la_ditiro(String Leina) {
        return "/".equals(Leina) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int mošomiši_sešupi() { return 0; }
    public int ya_go_šoma_gabotse_mošomiši_sešupi() { return 0; }
    public int sehlopha_sešupi() { return 0; }
    public int ya_go_šoma_gabotse_sehlopha_sešupi() { return 0; }

    public int kopanya_faele(tiragalo_boleng 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Bala 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(tiragalo_boleng 현재과정, int 서술자) {
        faele_tshedimošo msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int faele_taolo(tiragalo_boleng 현재과정, int 서술자, int Taelo, int 인자) {
        if (Taelo == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (Taelo == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Taelo == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (Taelo == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : balwago_fela_folaga;
        }
        if (Taelo == 4) {
            return 인자 == balwago_fela_folaga ? 0 : -30;
        }
        return -22;
    }

    public int 만들기(String Leina, int tumelelo_boleng) {
        return -30;
    }

    public faele_tshedimošo 서술자정보(tiragalo_boleng 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JZafOS", "JZafOS", "0.1", "Java managed kernel", "i386");
    }

    public faele_tshedimošo faele_tshedimošo(String Leina) {
        return tshepedišo_ya_difaele.msinfo32_exe(Leina);
    }

    public tiragalo_boleng 과정복제(tiragalo_boleng 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(tiragalo_boleng 부모, int ngwana_sešupi, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, ngwana_sešupi, 기다리지않음);
    }

    public int 프로그램끝(tiragalo_boleng 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / letlakala_molaodi.bogolo_bja_letlakala;
        int 끝쪽 = (새끝 + letlakala_molaodi.bogolo_bja_letlakala - 1) / letlakala_molaodi.bogolo_bja_letlakala;
        if (새끝 > 이전끝) {
            for (int lokela = 첫쪽; lokela < 끝쪽; lokela++) {
                int atrese = lokela * letlakala_molaodi.bogolo_bja_letlakala;
                try {
                    쪽관리.바이트읽기(현재과정.atrese_sekgoba(), atrese);
                } catch (IllegalStateException Phošo) {
                    쪽관리.mmepe_letlakala(현재과정.atrese_sekgoba(), atrese, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(tiragalo_boleng 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int phethagatša_taelo(tiragalo_boleng 현재과정, byte[] 실행파일) {
        return phethagatša_taelo(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int phethagatša_taelo(tiragalo_boleng 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.seswantšho seswantšho_boleng;
        try {
            seswantšho_boleng = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Phošo) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.karolo_boleng karolo_boleng : seswantšho_boleng.구역들()) {
            if ((karolo_boleng.folaga_boleng() & 2) == 0 || karolo_boleng.Bogolo() == 0) {
                continue;
            }
            int 첫쪽 = karolo_boleng.atrese() / letlakala_molaodi.bogolo_bja_letlakala;
            int 끝쪽 = (karolo_boleng.atrese() + karolo_boleng.Bogolo() + letlakala_molaodi.bogolo_bja_letlakala - 1) / letlakala_molaodi.bogolo_bja_letlakala;
            for (int lokela = 첫쪽; lokela < 끝쪽; lokela++) {
                int atrese = lokela * letlakala_molaodi.bogolo_bja_letlakala;
                try {
                    쪽관리.바이트읽기(현재과정.atrese_sekgoba(), atrese);
                    쪽관리.범위개인쓰기(현재과정.atrese_sekgoba(), atrese, letlakala_molaodi.bogolo_bja_letlakala);
                } catch (IllegalStateException Phošo) {
                    쪽관리.mmepe_letlakala(현재과정.atrese_sekgoba(), atrese, true);
                }
            }
            for (int lokela = 0; lokela < karolo_boleng.Bogolo(); lokela++) {
                byte boleng = karolo_boleng.종류() == 8 ? 0 : 실행파일[karolo_boleng.파일위치() + lokela];
                쪽관리.ngwala_paete_boleng(현재과정.atrese_sekgoba(), karolo_boleng.atrese() + lokela, boleng);
            }
        }
        현재과정.실행문맥설정(seswantšho_boleng.Thomišo_atrese(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(tiragalo_boleng 현재과정, int boemo_boleng) {
        현재과정.Etšwa_tirišo(boemo_boleng);
    }
}
