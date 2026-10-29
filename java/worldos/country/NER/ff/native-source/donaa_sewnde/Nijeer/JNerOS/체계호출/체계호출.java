// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijeer.JNerOS.체계호출;

import Nijeer.JNerOS.기억공간.hello_kisnoowo;
import Nijeer.JNerOS.작업.Yuɓɓo_golle_njaru;
import Nijeer.JNerOS.작업.배정기;
import Nijeer.JNerOS.yuɓɓo_piille.실행파일적재기;
import Nijeer.JNerOS.yuɓɓo_piille.yuɓɓo_piille;
import Nijeer.JNerOS.yuɓɓo_piille.fiilde_kumpital;
import Nijeer.JNerOS.aaluude.하드웨어;
import Nijeer.JNerOS.입력.입력관리자;
import Nijeer.JNerOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int janngotooɗo_tan_maantaade = 0;
    public static final int njiilawu_huɓɓude = 0;
    public static final int 찾기현재 = 1;
    public static final int yiylaade_naatnugol_taƴde = 2;

    private final yuɓɓo_piille yuɓɓo_piille;
    private final hello_kisnoowo 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 kaɓirgal_njaru;
    private final 입력관리자 입력관리;

    public 체계호출(yuɓɓo_piille yuɓɓo_piille, hello_kisnoowo 쪽관리, 배정기 배정기, 하드웨어 kaɓirgal_njaru, 입력관리자 입력관리) {
        this.yuɓɓo_piille = yuɓɓo_piille;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.kaɓirgal_njaru = kaɓirgal_njaru;
        this.입력관리 = 입력관리;
    }

    public int 과정식별자(Yuɓɓo_golle_njaru 현재과정) {
        return 현재과정.식별자();
    }

    public int 부모과정식별자(Yuɓɓo_golle_njaru 현재과정) {
        return 현재과정.부모식별자();
    }

    public int udditde(Yuɓɓo_golle_njaru 현재과정, String innde, int maantaade_njaru) {
        if (maantaade_njaru != janngotooɗo_tan_maantaade) {
            return -30;
        }
        return 현재과정.파일서술자().udditde(innde);
    }

    public int 읽기(Yuɓɓo_golle_njaru 현재과정, int 서술자, byte[] 받을곳, int waylude_etannde) {
        if (서술자 == 0) {
            if (waylude_etannde <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 saɗteende = 입력관리.다음사건();
            if (saɗteende == null || saɗteende.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) saɗteende.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, waylude_etannde);
    }

    public int winndude(Yuɓɓo_golle_njaru 현재과정, int 서술자, byte[] keɓe, int waylude_etannde) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (waylude_etannde < 0 || waylude_etannde > keɓe.length) {
            return -22;
        }
        kaɓirgal_njaru.직렬출력(new String(keɓe, 0, waylude_etannde, java.nio.charset.StandardCharsets.UTF_8));
        return waylude_etannde;
    }

    public int uddude(Yuɓɓo_golle_njaru 현재과정, int 서술자) {
        return 현재과정.파일서술자().uddude(서술자);
    }

    public int 위치옮기기(Yuɓɓo_golle_njaru 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(Yuɓɓo_golle_njaru 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Yuɓɓo_golle_njaru 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String innde, int 방식) {
        fiilde_kumpital msinfo32_exe = yuɓɓo_piille.msinfo32_exe(innde);
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

    public int waylude_golle_Doggol(String innde) {
        return "/".equals(innde) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int 사용자식별자() { return 0; }
    public int 유효사용자식별자() { return 0; }
    public int 무리식별자() { return 0; }
    public int 유효무리식별자() { return 0; }

    public int sanngoɗinde_fiilde(Yuɓɓo_golle_njaru 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Yuɓɓo_golle_njaru 현재과정, int 서술자) {
        fiilde_kumpital msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int fiilde_yuurnitorde(Yuɓɓo_golle_njaru 현재과정, int 서술자, int ginol, int 인자) {
        if (ginol == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (ginol == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (ginol == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (ginol == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : janngotooɗo_tan_maantaade;
        }
        if (ginol == 4) {
            return 인자 == janngotooɗo_tan_maantaade ? 0 : -30;
        }
        return -22;
    }

    public int 만들기(String innde, int 권한) {
        return -30;
    }

    public fiilde_kumpital 서술자정보(Yuɓɓo_golle_njaru 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JNerOS", "JNerOS", "0.1", "Java managed kernel", "i386");
    }

    public fiilde_kumpital fiilde_kumpital(String innde) {
        return yuɓɓo_piille.msinfo32_exe(innde);
    }

    public Yuɓɓo_golle_njaru 과정복제(Yuɓɓo_golle_njaru 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(Yuɓɓo_golle_njaru 부모, int 자식식별자, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, 자식식별자, 기다리지않음);
    }

    public int 프로그램끝(Yuɓɓo_golle_njaru 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / hello_kisnoowo.hello_waylude_etannde;
        int 끝쪽 = (새끝 + hello_kisnoowo.hello_waylude_etannde - 1) / hello_kisnoowo.hello_waylude_etannde;
        if (새끝 > 이전끝) {
            for (int joopirdu = 첫쪽; joopirdu < 끝쪽; joopirdu++) {
                int ñiiɓirde = joopirdu * hello_kisnoowo.hello_waylude_etannde;
                try {
                    쪽관리.바이트읽기(현재과정.ñiiɓirde_wonorde(), ñiiɓirde);
                } catch (IllegalStateException juumre) {
                    쪽관리.쪽연결(현재과정.ñiiɓirde_wonorde(), ñiiɓirde, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Yuɓɓo_golle_njaru 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int 실행(Yuɓɓo_golle_njaru 현재과정, byte[] 실행파일) {
        return 실행(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int 실행(Yuɓɓo_golle_njaru 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.natal natal_njaru;
        try {
            natal_njaru = 적재기.검사(실행파일);
        } catch (IllegalArgumentException juumre) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.taƴre_njaru taƴre_njaru : natal_njaru.구역들()) {
            if ((taƴre_njaru.maantaade_njaru() & 2) == 0 || taƴre_njaru.waylude_etannde() == 0) {
                continue;
            }
            int 첫쪽 = taƴre_njaru.ñiiɓirde() / hello_kisnoowo.hello_waylude_etannde;
            int 끝쪽 = (taƴre_njaru.ñiiɓirde() + taƴre_njaru.waylude_etannde() + hello_kisnoowo.hello_waylude_etannde - 1) / hello_kisnoowo.hello_waylude_etannde;
            for (int joopirdu = 첫쪽; joopirdu < 끝쪽; joopirdu++) {
                int ñiiɓirde = joopirdu * hello_kisnoowo.hello_waylude_etannde;
                try {
                    쪽관리.바이트읽기(현재과정.ñiiɓirde_wonorde(), ñiiɓirde);
                    쪽관리.범위개인쓰기(현재과정.ñiiɓirde_wonorde(), ñiiɓirde, hello_kisnoowo.hello_waylude_etannde);
                } catch (IllegalStateException juumre) {
                    쪽관리.쪽연결(현재과정.ñiiɓirde_wonorde(), ñiiɓirde, true);
                }
            }
            for (int joopirdu = 0; joopirdu < taƴre_njaru.waylude_etannde(); joopirdu++) {
                byte njaru = taƴre_njaru.종류() == 8 ? 0 : 실행파일[taƴre_njaru.파일위치() + joopirdu];
                쪽관리.winndude_oktee_njaru(현재과정.ñiiɓirde_wonorde(), taƴre_njaru.ñiiɓirde() + joopirdu, njaru);
            }
        }
        현재과정.실행문맥설정(natal_njaru.huɓɓude_ñiiɓirde(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(Yuɓɓo_golle_njaru 현재과정, int ngonka_njaru) {
        현재과정.yaltude_tafirde(ngonka_njaru);
    }
}
