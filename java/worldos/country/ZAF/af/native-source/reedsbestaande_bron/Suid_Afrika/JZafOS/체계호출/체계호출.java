// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suid_Afrika.JZafOS.체계호출;

import Suid_Afrika.JZafOS.기억공간.bladsy_bestuurder;
import Suid_Afrika.JZafOS.작업.Proses_VALUE;
import Suid_Afrika.JZafOS.작업.Skeduleerder;
import Suid_Afrika.JZafOS.lêerstelsel.실행파일적재기;
import Suid_Afrika.JZafOS.lêerstelsel.lêerstelsel;
import Suid_Afrika.JZafOS.lêerstelsel.lêer_inligting;
import Suid_Afrika.JZafOS.kern.hardeware_VALUE;
import Suid_Afrika.JZafOS.입력.입력관리자;
import Suid_Afrika.JZafOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int leesalleen_vlag = 0;
    public static final int Soek_BEGIN = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_inskrywing_beëindig = 2;

    private final lêerstelsel lêerstelsel;
    private final bladsy_bestuurder 쪽관리;
    private final Skeduleerder Skeduleerder;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final hardeware_VALUE mobiel_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(lêerstelsel lêerstelsel, bladsy_bestuurder 쪽관리, Skeduleerder Skeduleerder, hardeware_VALUE mobiel_VALUE, 입력관리자 입력관리) {
        this.lêerstelsel = lêerstelsel;
        this.쪽관리 = 쪽관리;
        this.Skeduleerder = Skeduleerder;
        this.mobiel_VALUE = mobiel_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Proses_waarde(Proses_VALUE 현재과정) {
        return 현재과정.waarde_VALUE();
    }

    public int 부모과정식별자(Proses_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int skep(Proses_VALUE 현재과정, String Naam, int vlag_VALUE) {
        if (vlag_VALUE != leesalleen_vlag) {
            return -30;
        }
        return 현재과정.파일서술자().skep(Naam);
    }

    public int Lees(Proses_VALUE 현재과정, int 서술자, byte[] 받을곳, int Grootte) {
        if (서술자 == 0) {
            if (Grootte <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 gebeurtenis = 입력관리.Volgende_gebeurtenis();
            if (gebeurtenis == null || gebeurtenis.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) gebeurtenis.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Lees(서술자, 받을곳, Grootte);
    }

    public int Skryf(Proses_VALUE 현재과정, int 서술자, byte[] data, int Grootte) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (Grootte < 0 || Grootte > data.length) {
            return -22;
        }
        mobiel_VALUE.직렬출력(new String(data, 0, Grootte, java.nio.charset.StandardCharsets.UTF_8));
        return Grootte;
    }

    public int Sluit(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Sluit(서술자);
    }

    public int skuif_plaas(Proses_VALUE 현재과정, int 서술자, int 거리, int Project_wortel) {
        return 현재과정.파일서술자().skuif_plaas(서술자, 거리, Project_wortel);
    }

    public int 서술자복제(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proses_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Naam, int metode_MODE) {
        lêer_inligting Stelselinfo = lêerstelsel.Stelselinfo(Naam);
        if (Stelselinfo == null) {
            return -2;
        }
        if ((metode_MODE & 1) != 0 && (Stelselinfo.형태() & 0111) == 0) {
            return -13;
        }
        if ((metode_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_taaklys(String Naam) {
        return "/".equals(Naam) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int gebruiker_waarde() { return 0; }
    public int effektief_gebruiker_waarde() { return 0; }
    public int Groep_waarde() { return 0; }
    public int effektief_Groep_waarde() { return 0; }

    public int sinc_lêer(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Stelselinfo(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Lees 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Proses_VALUE 현재과정, int 서술자) {
        lêer_inligting Stelselinfo = 현재과정.파일서술자().Stelselinfo(서술자);
        return Stelselinfo != null && (Stelselinfo.형태() & 0170000) == 0020000;
    }

    public int lêer_kontrole(Proses_VALUE 현재과정, int 서술자, int Opdrag, int 인자) {
        if (Opdrag == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (Opdrag == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Opdrag == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (Opdrag == 3) {
            return 현재과정.파일서술자().Stelselinfo(서술자) == null ? -9 : leesalleen_vlag;
        }
        if (Opdrag == 4) {
            return 인자 == leesalleen_vlag ? 0 : -30;
        }
        return -22;
    }

    public int Skep_inskrywing(String Naam, int toestemming_VALUE) {
        return -30;
    }

    public lêer_inligting 서술자정보(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Stelselinfo(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JZafOS", "JZafOS", "0.1", "Java managed kernel", "i386");
    }

    public lêer_inligting lêer_inligting(String Naam) {
        return lêerstelsel.Stelselinfo(Naam);
    }

    public Proses_VALUE 과정복제(Proses_VALUE 부모) {
        return Skeduleerder.복제(부모);
    }

    public int 자식기다리기(Proses_VALUE 부모, int kind_waarde, boolean 기다리지않음) {
        return Skeduleerder.자식기다리기(부모, kind_waarde, 기다리지않음);
    }

    public int 프로그램끝(Proses_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / bladsy_bestuurder.bladsygrootte;
        int 끝쪽 = (새끝 + bladsy_bestuurder.bladsygrootte - 1) / bladsy_bestuurder.bladsygrootte;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adres = INDEX * bladsy_bestuurder.bladsygrootte;
                try {
                    쪽관리.바이트읽기(현재과정.adres_ruimte(), adres);
                } catch (IllegalStateException Fout) {
                    쪽관리.MAP_bladsy(현재과정.adres_ruimte(), adres, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Proses_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int maatreël = 프로그램끝(현재과정, 이전끝 + 증가량);
        return maatreël < 0 ? maatreël : 이전끝;
    }

    public int uitvoer_bevel(Proses_VALUE 현재과정, byte[] 실행파일) {
        return uitvoer_bevel(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int uitvoer_bevel(Proses_VALUE 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.foto foto_VALUE;
        try {
            foto_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Fout) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.seksie_VALUE seksie_VALUE : foto_VALUE.구역들()) {
            if ((seksie_VALUE.vlag_VALUE() & 2) == 0 || seksie_VALUE.Grootte() == 0) {
                continue;
            }
            int 첫쪽 = seksie_VALUE.adres() / bladsy_bestuurder.bladsygrootte;
            int 끝쪽 = (seksie_VALUE.adres() + seksie_VALUE.Grootte() + bladsy_bestuurder.bladsygrootte - 1) / bladsy_bestuurder.bladsygrootte;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int adres = INDEX * bladsy_bestuurder.bladsygrootte;
                try {
                    쪽관리.바이트읽기(현재과정.adres_ruimte(), adres);
                    쪽관리.범위개인쓰기(현재과정.adres_ruimte(), adres, bladsy_bestuurder.bladsygrootte);
                } catch (IllegalStateException Fout) {
                    쪽관리.MAP_bladsy(현재과정.adres_ruimte(), adres, true);
                }
            }
            for (int INDEX = 0; INDEX < seksie_VALUE.Grootte(); INDEX++) {
                byte VALUE = seksie_VALUE.종류() == 8 ? 0 : 실행파일[seksie_VALUE.lêer_plaas() + INDEX];
                쪽관리.skryf_greep_VALUE(현재과정.adres_ruimte(), seksie_VALUE.adres() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(foto_VALUE.BEGIN_adres(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void gaan_uit_program(Proses_VALUE 현재과정, int stand_VALUE) {
        현재과정.Verlaat_program(stand_VALUE);
    }
}
