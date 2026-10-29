// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijeriya.JNgaOS.체계호출;

import Nijeriya.JNgaOS.기억공간.shafi_Manaja;
import Nijeriya.JNgaOS.작업.haryar_aikin_na_ura_Daraja;
import Nijeriya.JNgaOS.작업.배정기;
import Nijeriya.JNgaOS.tsarin_fayil_a_kwamfuta.실행파일적재기;
import Nijeriya.JNgaOS.tsarin_fayil_a_kwamfuta.tsarin_fayil_a_kwamfuta;
import Nijeriya.JNgaOS.tsarin_fayil_a_kwamfuta.Fayil_bayani;
import Nijeriya.JNgaOS.Kwara.kayan_haɗi_na_kwamfuta_Daraja;
import Nijeriya.JNgaOS.입력.입력관리자;
import Nijeriya.JNgaOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int karanta_kawai_Tuta = 0;
    public static final int Leko_Fara = 0;
    public static final int 찾기현재 = 1;
    public static final int nema_Mashigar_bayanai_Ƙarshe = 2;

    private final tsarin_fayil_a_kwamfuta tsarin_fayil_a_kwamfuta;
    private final shafi_Manaja 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final kayan_haɗi_na_kwamfuta_Daraja na_ura_Daraja;
    private final 입력관리자 입력관리;

    public 체계호출(tsarin_fayil_a_kwamfuta tsarin_fayil_a_kwamfuta, shafi_Manaja 쪽관리, 배정기 배정기, kayan_haɗi_na_kwamfuta_Daraja na_ura_Daraja, 입력관리자 입력관리) {
        this.tsarin_fayil_a_kwamfuta = tsarin_fayil_a_kwamfuta;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.na_ura_Daraja = na_ura_Daraja;
        this.입력관리 = 입력관리;
    }

    public int haryar_aikin_na_ura_mai_ganewa(haryar_aikin_na_ura_Daraja 현재과정) {
        return 현재과정.mai_ganewa_Daraja();
    }

    public int 부모과정식별자(haryar_aikin_na_ura_Daraja 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Buɗe(haryar_aikin_na_ura_Daraja 현재과정, String Suna, int Tuta_Daraja) {
        if (Tuta_Daraja != karanta_kawai_Tuta) {
            return -30;
        }
        return 현재과정.파일서술자().Buɗe(Suna);
    }

    public int Yi_Karatu(haryar_aikin_na_ura_Daraja 현재과정, int 서술자, byte[] 받을곳, int Girma) {
        if (서술자 == 0) {
            if (Girma <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 Faruwa = 입력관리.다음사건();
            if (Faruwa == null || Faruwa.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) Faruwa.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Yi_Karatu(서술자, 받을곳, Girma);
    }

    public int Yi_Rubutu(haryar_aikin_na_ura_Daraja 현재과정, int 서술자, byte[] Tarin_bayani, int Girma) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().kimiyar_bayanai_buɗe(서술자) ? -30 : -9;
        }
        if (Girma < 0 || Girma > Tarin_bayani.length) {
            return -22;
        }
        na_ura_Daraja.직렬출력(new String(Tarin_bayani, 0, Girma, java.nio.charset.StandardCharsets.UTF_8));
        return Girma;
    }

    public int Rufe(haryar_aikin_na_ura_Daraja 현재과정, int 서술자) {
        return 현재과정.파일서술자().Rufe(서술자);
    }

    public int 위치옮기기(haryar_aikin_na_ura_Daraja 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(haryar_aikin_na_ura_Daraja 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(haryar_aikin_na_ura_Daraja 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Suna, int tsari_yanayin_aiki) {
        Fayil_bayani msinfo32_exe = tsarin_fayil_a_kwamfuta.msinfo32_exe(Suna);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((tsari_yanayin_aiki & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((tsari_yanayin_aiki & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int Sauya_Jerin_tsarin_aiki(String Suna) {
        return "/".equals(Suna) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int Mai_anfani_da_kwamfuta_mai_ganewa() { return 0; }
    public int Mai_ingantaccen_aiki_Mai_anfani_da_kwamfuta_mai_ganewa() { return 0; }
    public int gungu_mai_ganewa() { return 0; }
    public int Mai_ingantaccen_aiki_gungu_mai_ganewa() { return 0; }

    public int daidaita_Fayil(haryar_aikin_na_ura_Daraja 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Yi_Karatu 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(haryar_aikin_na_ura_Daraja 현재과정, int 서술자) {
        Fayil_bayani msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int Fayil_masarrafa(haryar_aikin_na_ura_Daraja 현재과정, int 서술자, int Umarni, int maaunin_Tubalin_aiki) {
        if (Umarni == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, maaunin_Tubalin_aiki);
        }
        if (Umarni == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Umarni == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (maaunin_Tubalin_aiki & 1) != 0);
        }
        if (Umarni == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : karanta_kawai_Tuta;
        }
        if (Umarni == 4) {
            return maaunin_Tubalin_aiki == karanta_kawai_Tuta ? 0 : -30;
        }
        return -22;
    }

    public int ƙirƙíra_Mashigar_bayanai(String Suna, int izini_Daraja) {
        return -30;
    }

    public Fayil_bayani 서술자정보(haryar_aikin_na_ura_Daraja 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JNgaOS", "JNgaOS", "0.1", "Java managed kernel", "i386");
    }

    public Fayil_bayani Fayil_bayani(String Suna) {
        return tsarin_fayil_a_kwamfuta.msinfo32_exe(Suna);
    }

    public haryar_aikin_na_ura_Daraja 과정복제(haryar_aikin_na_ura_Daraja 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(haryar_aikin_na_ura_Daraja 부모, int yaro_mai_ganewa, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, yaro_mai_ganewa, 기다리지않음);
    }

    public int 프로그램끝(haryar_aikin_na_ura_Daraja 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / shafi_Manaja.Girman_shafi;
        int 끝쪽 = (새끝 + shafi_Manaja.Girman_shafi - 1) / shafi_Manaja.Girman_shafi;
        if (새끝 > 이전끝) {
            for (int Indes = 첫쪽; Indes < 끝쪽; Indes++) {
                int imel = Indes * shafi_Manaja.Girman_shafi;
                try {
                    쪽관리.바이트읽기(현재과정.imel_wuri(), imel);
                } catch (IllegalStateException Kuskure) {
                    쪽관리.taswira_shafi(현재과정.imel_wuri(), imel, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(haryar_aikin_na_ura_Daraja 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int gudanar_Umarni(haryar_aikin_na_ura_Daraja 현재과정, byte[] 실행파일) {
        return gudanar_Umarni(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int gudanar_Umarni(haryar_aikin_na_ura_Daraja 현재과정, byte[] 실행파일, String[] maaunin_Tubalin_aiki, String[] 환경) {
        실행파일적재기.Hoto Hoto_Daraja;
        try {
            Hoto_Daraja = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Kuskure) {
            return -8;
        }
        if (maaunin_Tubalin_aiki == null || 환경 == null || maaunin_Tubalin_aiki.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.Sashi_Daraja Sashi_Daraja : Hoto_Daraja.구역들()) {
            if ((Sashi_Daraja.Tuta_Daraja() & 2) == 0 || Sashi_Daraja.Girma() == 0) {
                continue;
            }
            int 첫쪽 = Sashi_Daraja.imel() / shafi_Manaja.Girman_shafi;
            int 끝쪽 = (Sashi_Daraja.imel() + Sashi_Daraja.Girma() + shafi_Manaja.Girman_shafi - 1) / shafi_Manaja.Girman_shafi;
            for (int Indes = 첫쪽; Indes < 끝쪽; Indes++) {
                int imel = Indes * shafi_Manaja.Girman_shafi;
                try {
                    쪽관리.바이트읽기(현재과정.imel_wuri(), imel);
                    쪽관리.범위개인쓰기(현재과정.imel_wuri(), imel, shafi_Manaja.Girman_shafi);
                } catch (IllegalStateException Kuskure) {
                    쪽관리.taswira_shafi(현재과정.imel_wuri(), imel, true);
                }
            }
            for (int Indes = 0; Indes < Sashi_Daraja.Girma(); Indes++) {
                byte Daraja = Sashi_Daraja.종류() == 8 ? 0 : 실행파일[Sashi_Daraja.파일위치() + Indes];
                쪽관리.Rubuta_bayit_Daraja(현재과정.imel_wuri(), Sashi_Daraja.imel() + Indes, Daraja);
            }
        }
        현재과정.실행문맥설정(Hoto_Daraja.Fara_imel(), maaunin_Tubalin_aiki, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(haryar_aikin_na_ura_Daraja 현재과정, int Matsayi_Daraja) {
        현재과정.Mafita_Shiri(Matsayi_Daraja);
    }
}
