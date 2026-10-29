// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.체계호출;

import ᑲᓇᑕᒥ.JCanOS.기억공간.mappigaq_aulattiji;
import ᑲᓇᑕᒥ.JCanOS.작업.Pivallianiq_atuutilik;
import ᑲᓇᑕᒥ.JCanOS.작업.배정기;
import ᑲᓇᑕᒥ.JCanOS.inikkuvik.실행파일적재기;
import ᑲᓇᑕᒥ.JCanOS.inikkuvik.inikkuvik;
import ᑲᓇᑕᒥ.JCanOS.inikkuvik.ini_tukisigiarut;
import ᑲᓇᑕᒥ.JCanOS.kernel.하드웨어;
import ᑲᓇᑕᒥ.JCanOS.입력.입력관리자;
import ᑲᓇᑕᒥ.JCanOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int takugatuinnaq_ujjiqsuut = 0;
    public static final int Qinirli_pigiarli = 0;
    public static final int 찾기현재 = 1;
    public static final int nanili_Iliniku_isulittuq = 2;

    private final inikkuvik inikkuvik;
    private final mappigaq_aulattiji 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 sunakkutaaq_atuutilik;
    private final 입력관리자 입력관리;

    public 체계호출(inikkuvik inikkuvik, mappigaq_aulattiji 쪽관리, 배정기 배정기, 하드웨어 sunakkutaaq_atuutilik, 입력관리자 입력관리) {
        this.inikkuvik = inikkuvik;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.sunakkutaaq_atuutilik = sunakkutaaq_atuutilik;
        this.입력관리 = 입력관리;
    }

    public int 과정식별자(Pivallianiq_atuutilik 현재과정) {
        return 현재과정.식별자();
    }

    public int 부모과정식별자(Pivallianiq_atuutilik 현재과정) {
        return 현재과정.부모식별자();
    }

    public int matuirli(Pivallianiq_atuutilik 현재과정, String atiq, int ujjiqsuut_atuutilik) {
        if (ujjiqsuut_atuutilik != takugatuinnaq_ujjiqsuut) {
            return -30;
        }
        return 현재과정.파일서술자().matuirli(atiq);
    }

    public int 읽기(Pivallianiq_atuutilik 현재과정, int 서술자, byte[] 받을곳, int anininga) {
        if (서술자 == 0) {
            if (anininga <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 piniku = 입력관리.다음사건();
            if (piniku == null || piniku.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) piniku.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, anininga);
    }

    public int titiraq(Pivallianiq_atuutilik 현재과정, int 서술자, byte[] titiqqat, int anininga) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (anininga < 0 || anininga > titiqqat.length) {
            return -22;
        }
        sunakkutaaq_atuutilik.직렬출력(new String(titiqqat, 0, anininga, java.nio.charset.StandardCharsets.UTF_8));
        return anininga;
    }

    public int matuli(Pivallianiq_atuutilik 현재과정, int 서술자) {
        return 현재과정.파일서술자().matuli(서술자);
    }

    public int 위치옮기기(Pivallianiq_atuutilik 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(Pivallianiq_atuutilik 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Pivallianiq_atuutilik 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String atiq, int 방식) {
        ini_tukisigiarut msinfo32_exe = inikkuvik.msinfo32_exe(atiq);
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

    public int kipulli_piliriatsanut_titiqpalliagat(String atiq) {
        return "/".equals(atiq) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int 사용자식별자() { return 0; }
    public int 유효사용자식별자() { return 0; }
    public int 무리식별자() { return 0; }
    public int 유효무리식별자() { return 0; }

    public int asiqqunniqannginniq_ini(Pivallianiq_atuutilik 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Pivallianiq_atuutilik 현재과정, int 서술자) {
        ini_tukisigiarut msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int ini_aulattivik(Pivallianiq_atuutilik 현재과정, int 서술자, int piqujijjut, int 인자) {
        if (piqujijjut == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (piqujijjut == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (piqujijjut == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (piqujijjut == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : takugatuinnaq_ujjiqsuut;
        }
        if (piqujijjut == 4) {
            return 인자 == takugatuinnaq_ujjiqsuut ? 0 : -30;
        }
        return -22;
    }

    public int 만들기(String atiq, int pijunnaqtittijjut_atuutilik) {
        return -30;
    }

    public ini_tukisigiarut 서술자정보(Pivallianiq_atuutilik 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JCanOS", "JCanOS", "0.1", "Java managed kernel", "i386");
    }

    public ini_tukisigiarut ini_tukisigiarut(String atiq) {
        return inikkuvik.msinfo32_exe(atiq);
    }

    public Pivallianiq_atuutilik 과정복제(Pivallianiq_atuutilik 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(Pivallianiq_atuutilik 부모, int 자식식별자, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, 자식식별자, 기다리지않음);
    }

    public int 프로그램끝(Pivallianiq_atuutilik 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / mappigaq_aulattiji.mappigap_angininga;
        int 끝쪽 = (새끝 + mappigaq_aulattiji.mappigap_angininga - 1) / mappigaq_aulattiji.mappigap_angininga;
        if (새끝 > 이전끝) {
            for (int nalunaiqsimavik = 첫쪽; nalunaiqsimavik < 끝쪽; nalunaiqsimavik++) {
                int turaarut = nalunaiqsimavik * mappigaq_aulattiji.mappigap_angininga;
                try {
                    쪽관리.바이트읽기(현재과정.turaarut_SPACEBAR(), turaarut);
                } catch (IllegalStateException tammarniq) {
                    쪽관리.nunannguarurli_mappigaq(현재과정.turaarut_SPACEBAR(), turaarut, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Pivallianiq_atuutilik 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int 실행(Pivallianiq_atuutilik 현재과정, byte[] 실행파일) {
        return 실행(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int 실행(Pivallianiq_atuutilik 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.ajjinnguaq ajjinnguaq_atuutilik;
        try {
            ajjinnguaq_atuutilik = 적재기.검사(실행파일);
        } catch (IllegalArgumentException tammarniq) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.sukuttia_atuutilik sukuttia_atuutilik : ajjinnguaq_atuutilik.구역들()) {
            if ((sukuttia_atuutilik.ujjiqsuut_atuutilik() & 2) == 0 || sukuttia_atuutilik.anininga() == 0) {
                continue;
            }
            int 첫쪽 = sukuttia_atuutilik.turaarut() / mappigaq_aulattiji.mappigap_angininga;
            int 끝쪽 = (sukuttia_atuutilik.turaarut() + sukuttia_atuutilik.anininga() + mappigaq_aulattiji.mappigap_angininga - 1) / mappigaq_aulattiji.mappigap_angininga;
            for (int nalunaiqsimavik = 첫쪽; nalunaiqsimavik < 끝쪽; nalunaiqsimavik++) {
                int turaarut = nalunaiqsimavik * mappigaq_aulattiji.mappigap_angininga;
                try {
                    쪽관리.바이트읽기(현재과정.turaarut_SPACEBAR(), turaarut);
                    쪽관리.범위개인쓰기(현재과정.turaarut_SPACEBAR(), turaarut, mappigaq_aulattiji.mappigap_angininga);
                } catch (IllegalStateException tammarniq) {
                    쪽관리.nunannguarurli_mappigaq(현재과정.turaarut_SPACEBAR(), turaarut, true);
                }
            }
            for (int nalunaiqsimavik = 0; nalunaiqsimavik < sukuttia_atuutilik.anininga(); nalunaiqsimavik++) {
                byte atuutilik = sukuttia_atuutilik.종류() == 8 ? 0 : 실행파일[sukuttia_atuutilik.파일위치() + nalunaiqsimavik];
                쪽관리.titiraq_byte_atuutilik(현재과정.turaarut_SPACEBAR(), sukuttia_atuutilik.turaarut() + nalunaiqsimavik, atuutilik);
            }
        }
        현재과정.실행문맥설정(ajjinnguaq_atuutilik.pigiarli_turaarut(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(Pivallianiq_atuutilik 현재과정, int qanuilinganiq_atuutilik) {
        현재과정.taima_pilirijjut(qanuilinganiq_atuutilik);
    }
}
