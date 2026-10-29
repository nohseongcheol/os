// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mooritani.JMrtOS.체계호출;

import Mooritani.JMrtOS.기억공간.xët_doxalkat;
import Mooritani.JMrtOS.작업.yokkute_xëyma;
import Mooritani.JMrtOS.작업.배정기;
import Mooritani.JMrtOS.barabu_boolebdenc_yu_ñu_bennal.실행파일적재기;
import Mooritani.JMrtOS.barabu_boolebdenc_yu_ñu_bennal.barabu_boolebdenc_yu_ñu_bennal;
import Mooritani.JMrtOS.barabu_boolebdenc_yu_ñu_bennal.bara_denc_yëglë;
import Mooritani.JMrtOS.xoox.jumtukaay_xëyma;
import Mooritani.JMrtOS.입력.입력관리자;
import Mooritani.JMrtOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int ngir_jaŋarek_la_tektalukaay = 0;
    public static final int Wut_Door = 0;
    public static final int 찾기현재 = 1;
    public static final int seet_dugal_xabaar_jeexal = 2;

    private final barabu_boolebdenc_yu_ñu_bennal barabu_boolebdenc_yu_ñu_bennal;
    private final xët_doxalkat 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final jumtukaay_xëyma toftal_xëyma;
    private final 입력관리자 입력관리;

    public 체계호출(barabu_boolebdenc_yu_ñu_bennal barabu_boolebdenc_yu_ñu_bennal, xët_doxalkat 쪽관리, 배정기 배정기, jumtukaay_xëyma toftal_xëyma, 입력관리자 입력관리) {
        this.barabu_boolebdenc_yu_ñu_bennal = barabu_boolebdenc_yu_ñu_bennal;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.toftal_xëyma = toftal_xëyma;
        this.입력관리 = 입력관리;
    }

    public int yokkute_raññeekaay(yokkute_xëyma 현재과정) {
        return 현재과정.raññeekaay_xëyma();
    }

    public int 부모과정식별자(yokkute_xëyma 현재과정) {
        return 현재과정.부모식별자();
    }

    public int sos(yokkute_xëyma 현재과정, String tur_253d1510, int tektalukaay_xëyma) {
        if (tektalukaay_xëyma != ngir_jaŋarek_la_tektalukaay) {
            return -30;
        }
        return 현재과정.파일서술자().sos(tur_253d1510);
    }

    public int 읽기(yokkute_xëyma 현재과정, int 서술자, byte[] 받을곳, int tolluwaay) {
        if (서술자 == 0) {
            if (tolluwaay <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 xewxew = 입력관리.다음사건();
            if (xewxew == null || xewxew.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) xewxew.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, tolluwaay);
    }

    public int biir(yokkute_xëyma 현재과정, int 서술자, byte[] mbir, int tolluwaay) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (tolluwaay < 0 || tolluwaay > mbir.length) {
            return -22;
        }
        toftal_xëyma.직렬출력(new String(mbir, 0, tolluwaay, java.nio.charset.StandardCharsets.UTF_8));
        return tolluwaay;
    }

    public int Tej(yokkute_xëyma 현재과정, int 서술자) {
        return 현재과정.파일서술자().Tej(서술자);
    }

    public int 위치옮기기(yokkute_xëyma 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(yokkute_xëyma 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(yokkute_xëyma 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String tur_253d1510, int doxalin_anam) {
        bara_denc_yëglë msinfo32_exe = barabu_boolebdenc_yu_ñu_bennal.msinfo32_exe(tur_253d1510);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((doxalin_anam & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((doxalin_anam & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int jalantu_alluwa_ligeey_yi(String tur_253d1510) {
        return "/".equals(tur_253d1510) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int kiy_jariñoo_internet_raññeekaay() { return 0; }
    public int anam_bu_beru_kiy_jariñoo_internet_raññeekaay() { return 0; }
    public int mboolo_raññeekaay() { return 0; }
    public int anam_bu_beru_mboolo_raññeekaay() { return 0; }

    public int lëkkale_bara_denc(yokkute_xëyma 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(yokkute_xëyma 현재과정, int 서술자) {
        bara_denc_yëglë msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int bara_denc_Saytu_doxinu_ordinateur(yokkute_xëyma 현재과정, int 서술자, int ndigel, int 인자) {
        if (ndigel == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (ndigel == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (ndigel == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (ndigel == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : ngir_jaŋarek_la_tektalukaay;
        }
        if (ndigel == 4) {
            return 인자 == ngir_jaŋarek_la_tektalukaay ? 0 : -30;
        }
        return -22;
    }

    public int sos_dugal_xabaar(String tur_253d1510, int sañ_sañ_xëyma) {
        return -30;
    }

    public bara_denc_yëglë 서술자정보(yokkute_xëyma 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JMrtOS", "JMrtOS", "0.1", "Java managed kernel", "i386");
    }

    public bara_denc_yëglë bara_denc_yëglë(String tur_253d1510) {
        return barabu_boolebdenc_yu_ñu_bennal.msinfo32_exe(tur_253d1510);
    }

    public yokkute_xëyma 과정복제(yokkute_xëyma 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(yokkute_xëyma 부모, int xale_raññeekaay, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, xale_raññeekaay, 기다리지않음);
    }

    public int 프로그램끝(yokkute_xëyma 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / xët_doxalkat.dayob_xët;
        int 끝쪽 = (새끝 + xët_doxalkat.dayob_xët - 1) / xët_doxalkat.dayob_xët;
        if (새끝 > 이전끝) {
            for (int àlluwa_tur = 첫쪽; àlluwa_tur < 끝쪽; àlluwa_tur++) {
                int dëkkuwaay = àlluwa_tur * xët_doxalkat.dayob_xët;
                try {
                    쪽관리.바이트읽기(현재과정.dëkkuwaay_Espace(), dëkkuwaay);
                } catch (IllegalStateException njumte) {
                    쪽관리.fésal_dëkkuwaay_bi_ciw_kart_xët(현재과정.dëkkuwaay_Espace(), dëkkuwaay, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(yokkute_xëyma 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int def_ndigel(yokkute_xëyma 현재과정, byte[] 실행파일) {
        return def_ndigel(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int def_ndigel(yokkute_xëyma 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.nataal nataal_xëyma;
        try {
            nataal_xëyma = 적재기.검사(실행파일);
        } catch (IllegalArgumentException njumte) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.dog_xëyma dog_xëyma : nataal_xëyma.구역들()) {
            if ((dog_xëyma.tektalukaay_xëyma() & 2) == 0 || dog_xëyma.tolluwaay() == 0) {
                continue;
            }
            int 첫쪽 = dog_xëyma.dëkkuwaay() / xët_doxalkat.dayob_xët;
            int 끝쪽 = (dog_xëyma.dëkkuwaay() + dog_xëyma.tolluwaay() + xët_doxalkat.dayob_xët - 1) / xët_doxalkat.dayob_xët;
            for (int àlluwa_tur = 첫쪽; àlluwa_tur < 끝쪽; àlluwa_tur++) {
                int dëkkuwaay = àlluwa_tur * xët_doxalkat.dayob_xët;
                try {
                    쪽관리.바이트읽기(현재과정.dëkkuwaay_Espace(), dëkkuwaay);
                    쪽관리.범위개인쓰기(현재과정.dëkkuwaay_Espace(), dëkkuwaay, xët_doxalkat.dayob_xët);
                } catch (IllegalStateException njumte) {
                    쪽관리.fésal_dëkkuwaay_bi_ciw_kart_xët(현재과정.dëkkuwaay_Espace(), dëkkuwaay, true);
                }
            }
            for (int àlluwa_tur = 0; àlluwa_tur < dog_xëyma.tolluwaay(); àlluwa_tur++) {
                byte xëyma = dog_xëyma.종류() == 8 ? 0 : 실행파일[dog_xëyma.파일위치() + àlluwa_tur];
                쪽관리.biir_okte_xëyma(현재과정.dëkkuwaay_Espace(), dog_xëyma.dëkkuwaay() + àlluwa_tur, xëyma);
            }
        }
        현재과정.실행문맥설정(nataal_xëyma.Door_dëkkuwaay(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(yokkute_xëyma 현재과정, int nekkin_xëyma) {
        현재과정.Génn_jëfekaay(nekkin_xëyma);
    }
}
