// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package UGA.JUgaOS.체계호출;

import UGA.JUgaOS.기억공간.paji_Umugenzuzi;
import UGA.JUgaOS.작업.Inzira_agaciro;
import UGA.JUgaOS.작업.배정기;
import UGA.JUgaOS.sisitemu_ya_dosiye.실행파일적재기;
import UGA.JUgaOS.sisitemu_ya_dosiye.sisitemu_ya_dosiye;
import UGA.JUgaOS.sisitemu_ya_dosiye.dosiye_amakuru;
import UGA.JUgaOS.intima.하드웨어;
import UGA.JUgaOS.입력.입력관리자;
import UGA.JUgaOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int soma_gusa_akabendera = 0;
    public static final int Gushaka_Itangira = 0;
    public static final int 찾기현재 = 1;
    public static final int gushaka_icyinjizwa_kurangiza = 2;

    private final sisitemu_ya_dosiye sisitemu_ya_dosiye;
    private final paji_Umugenzuzi 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 igendanwa_agaciro;
    private final 입력관리자 입력관리;

    public 체계호출(sisitemu_ya_dosiye sisitemu_ya_dosiye, paji_Umugenzuzi 쪽관리, 배정기 배정기, 하드웨어 igendanwa_agaciro, 입력관리자 입력관리) {
        this.sisitemu_ya_dosiye = sisitemu_ya_dosiye;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.igendanwa_agaciro = igendanwa_agaciro;
        this.입력관리 = 입력관리;
    }

    public int Inzira_indanga(Inzira_agaciro 현재과정) {
        return 현재과정.indanga_agaciro();
    }

    public int 부모과정식별자(Inzira_agaciro 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Gufungura(Inzira_agaciro 현재과정, String Izina, int akabendera_agaciro) {
        if (akabendera_agaciro != soma_gusa_akabendera) {
            return -30;
        }
        return 현재과정.파일서술자().Gufungura(Izina);
    }

    public int 읽기(Inzira_agaciro 현재과정, int 서술자, byte[] 받을곳, int Ingano) {
        if (서술자 == 0) {
            if (Ingano <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 icyabaye = 입력관리.다음사건();
            if (icyabaye == null || icyabaye.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) icyabaye.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, Ingano);
    }

    public int kwandika(Inzira_agaciro 현재과정, int 서술자, byte[] amakurushingiro, int Ingano) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (Ingano < 0 || Ingano > amakurushingiro.length) {
            return -22;
        }
        igendanwa_agaciro.직렬출력(new String(amakurushingiro, 0, Ingano, java.nio.charset.StandardCharsets.UTF_8));
        return Ingano;
    }

    public int Gufunga(Inzira_agaciro 현재과정, int 서술자) {
        return 현재과정.파일서술자().Gufunga(서술자);
    }

    public int 위치옮기기(Inzira_agaciro 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(Inzira_agaciro 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Inzira_agaciro 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Izina, int uburyo_uburyo) {
        dosiye_amakuru msinfo32_exe = sisitemu_ya_dosiye.msinfo32_exe(Izina);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((uburyo_uburyo & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((uburyo_uburyo & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int guhinduranya_ilisiti_y_imikoro(String Izina) {
        return "/".equals(Izina) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int ukoresha_indanga() { return 0; }
    public int ikora_neza_ukoresha_indanga() { return 0; }
    public int itsinda_indanga() { return 0; }
    public int ikora_neza_itsinda_indanga() { return 0; }

    public int guhuza_dosiye(Inzira_agaciro 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Inzira_agaciro 현재과정, int 서술자) {
        dosiye_amakuru msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int dosiye_icunga(Inzira_agaciro 현재과정, int 서술자, int Icyo_wifuza, int 인자) {
        if (Icyo_wifuza == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (Icyo_wifuza == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Icyo_wifuza == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (Icyo_wifuza == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : soma_gusa_akabendera;
        }
        if (Icyo_wifuza == 4) {
            return 인자 == soma_gusa_akabendera ? 0 : -30;
        }
        return -22;
    }

    public int kurema_icyinjizwa(String Izina, int 권한) {
        return -30;
    }

    public dosiye_amakuru 서술자정보(Inzira_agaciro 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JUgaOS", "JUgaOS", "0.1", "Java managed kernel", "i386");
    }

    public dosiye_amakuru dosiye_amakuru(String Izina) {
        return sisitemu_ya_dosiye.msinfo32_exe(Izina);
    }

    public Inzira_agaciro 과정복제(Inzira_agaciro 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(Inzira_agaciro 부모, int ishami_indanga, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, ishami_indanga, 기다리지않음);
    }

    public int 프로그램끝(Inzira_agaciro 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / paji_Umugenzuzi.ingano_ya_paji;
        int 끝쪽 = (새끝 + paji_Umugenzuzi.ingano_ya_paji - 1) / paji_Umugenzuzi.ingano_ya_paji;
        if (새끝 > 이전끝) {
            for (int umugerekashakiro = 첫쪽; umugerekashakiro < 끝쪽; umugerekashakiro++) {
                int aderesi = umugerekashakiro * paji_Umugenzuzi.ingano_ya_paji;
                try {
                    쪽관리.바이트읽기(현재과정.aderesi_akanya(), aderesi);
                } catch (IllegalStateException IKOSA) {
                    쪽관리.ikarita_paji(현재과정.aderesi_akanya(), aderesi, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Inzira_agaciro 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int gukora_ibwiriza(Inzira_agaciro 현재과정, byte[] 실행파일) {
        return gukora_ibwiriza(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int gukora_ibwiriza(Inzira_agaciro 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.ishusho ishusho_agaciro;
        try {
            ishusho_agaciro = 적재기.검사(실행파일);
        } catch (IllegalArgumentException IKOSA) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.igice_agaciro igice_agaciro : ishusho_agaciro.구역들()) {
            if ((igice_agaciro.akabendera_agaciro() & 2) == 0 || igice_agaciro.Ingano() == 0) {
                continue;
            }
            int 첫쪽 = igice_agaciro.aderesi() / paji_Umugenzuzi.ingano_ya_paji;
            int 끝쪽 = (igice_agaciro.aderesi() + igice_agaciro.Ingano() + paji_Umugenzuzi.ingano_ya_paji - 1) / paji_Umugenzuzi.ingano_ya_paji;
            for (int umugerekashakiro = 첫쪽; umugerekashakiro < 끝쪽; umugerekashakiro++) {
                int aderesi = umugerekashakiro * paji_Umugenzuzi.ingano_ya_paji;
                try {
                    쪽관리.바이트읽기(현재과정.aderesi_akanya(), aderesi);
                    쪽관리.범위개인쓰기(현재과정.aderesi_akanya(), aderesi, paji_Umugenzuzi.ingano_ya_paji);
                } catch (IllegalStateException IKOSA) {
                    쪽관리.ikarita_paji(현재과정.aderesi_akanya(), aderesi, true);
                }
            }
            for (int umugerekashakiro = 0; umugerekashakiro < igice_agaciro.Ingano(); umugerekashakiro++) {
                byte agaciro = igice_agaciro.종류() == 8 ? 0 : 실행파일[igice_agaciro.파일위치() + umugerekashakiro];
                쪽관리.kwandika_bayiti_agaciro(현재과정.aderesi_akanya(), igice_agaciro.aderesi() + umugerekashakiro, agaciro);
            }
        }
        현재과정.실행문맥설정(ishusho_agaciro.Itangira_aderesi(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(Inzira_agaciro 현재과정, int imimerere_agaciro) {
        현재과정.gusohoka_porogaramu(imimerere_agaciro);
    }
}
