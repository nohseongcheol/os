// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.체계호출;

import Ísland.JIslOS.기억공간.síða_stjórnandi;
import Ísland.JIslOS.작업.Ferli_VALUE;
import Ísland.JIslOS.작업.Verkraðari;
import Ísland.JIslOS.skrárkerfi.실행파일적재기;
import Ísland.JIslOS.skrárkerfi.skrárkerfi;
import Ísland.JIslOS.skrárkerfi.skrá_uppl;
import Ísland.JIslOS.kjarni.하드웨어;
import Ísland.JIslOS.입력.입력관리자;
import Ísland.JIslOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int skrifvarið_flagg = 0;
    public static final int Leit_Opna = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_færsla_ljúka = 2;

    private final skrárkerfi skrárkerfi;
    private final síða_stjórnandi 쪽관리;
    private final Verkraðari Verkraðari;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 tæki_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(skrárkerfi skrárkerfi, síða_stjórnandi 쪽관리, Verkraðari Verkraðari, 하드웨어 tæki_VALUE, 입력관리자 입력관리) {
        this.skrárkerfi = skrárkerfi;
        this.쪽관리 = 쪽관리;
        this.Verkraðari = Verkraðari;
        this.tæki_VALUE = tæki_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Ferli_auðkenni(Ferli_VALUE 현재과정) {
        return 현재과정.auðkenni_VALUE();
    }

    public int yfireining_Ferli_auðkenni(Ferli_VALUE 현재과정) {
        return 현재과정.yfireining_auðkenni();
    }

    public int Opna(Ferli_VALUE 현재과정, String Heiti, int flagg_VALUE) {
        if (flagg_VALUE != skrifvarið_flagg) {
            return -30;
        }
        return 현재과정.파일서술자().Opna(Heiti);
    }

    public int Lestur(Ferli_VALUE 현재과정, int 서술자, byte[] 받을곳, int Stærð) {
        if (서술자 == 0) {
            if (Stærð <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 atvik = 입력관리.Áfram_atvik();
            if (atvik == null || atvik.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) atvik.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Lestur(서술자, 받을곳, Stærð);
    }

    public int Skrift(Ferli_VALUE 현재과정, int 서술자, byte[] gögn, int Stærð) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().upplýsingatækni_opið(서술자) ? -30 : -9;
        }
        if (Stærð < 0 || Stærð > gögn.length) {
            return -22;
        }
        tæki_VALUE.직렬출력(new String(gögn, 0, Stærð, java.nio.charset.StandardCharsets.UTF_8));
        return Stærð;
    }

    public int Loka(Ferli_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Loka(서술자);
    }

    public int færa_staða(Ferli_VALUE 현재과정, int 서술자, int 거리, int verk_rót) {
        return 현재과정.파일서술자().færa_staða(서술자, 거리, verk_rót);
    }

    public int 서술자복제(Ferli_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Ferli_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Heiti, int aðferð_MODE) {
        skrá_uppl msinfo32_exe = skrárkerfi.msinfo32_exe(Heiti);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((aðferð_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((aðferð_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_verklisti(String Heiti) {
        return "/".equals(Heiti) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int notandi_auðkenni() { return 0; }
    public int virkt_notandi_auðkenni() { return 0; }
    public int Hópur_auðkenni() { return 0; }
    public int virkt_Hópur_auðkenni() { return 0; }

    public int samstilla_skrá(Ferli_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Lestur 전용이어서 밀어낼 자료가 없다.
    }

    public boolean upplýsingatækni_Endastöð(Ferli_VALUE 현재과정, int 서술자) {
        skrá_uppl msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int skrá_stýring(Ferli_VALUE 현재과정, int 서술자, int Skipun, int færibreyta_frumbreyta) {
        if (Skipun == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, færibreyta_frumbreyta);
        }
        if (Skipun == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Skipun == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (færibreyta_frumbreyta & 1) != 0);
        }
        if (Skipun == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : skrifvarið_flagg;
        }
        if (Skipun == 4) {
            return færibreyta_frumbreyta == skrifvarið_flagg ? 0 : -30;
        }
        return -22;
    }

    public int stofna_færsla(String Heiti, int leyfi_VALUE) {
        return -30;
    }

    public skrá_uppl 서술자정보(Ferli_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JIslOS", "JIslOS", "0.1", "Java managed kernel", "i386");
    }

    public skrá_uppl skrá_uppl(String Heiti) {
        return skrárkerfi.msinfo32_exe(Heiti);
    }

    public Ferli_VALUE 과정복제(Ferli_VALUE yfireining_VALUE) {
        return Verkraðari.복제(yfireining_VALUE);
    }

    public int 자식기다리기(Ferli_VALUE yfireining_VALUE, int barn_auðkenni, boolean 기다리지않음) {
        return Verkraðari.자식기다리기(yfireining_VALUE, barn_auðkenni, 기다리지않음);
    }

    public int forrit_hlé(Ferli_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.forrit_hlé();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / síða_stjórnandi.síðustærð;
        int 끝쪽 = (새끝 + síða_stjórnandi.síðustærð - 1) / síða_stjórnandi.síðustærð;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int slóð = INDEX * síða_stjórnandi.síðustærð;
                try {
                    쪽관리.바이트읽기(현재과정.slóð_svæði(), slóð);
                } catch (IllegalStateException Villa) {
                    쪽관리.MAP_síða(현재과정.slóð_svæði(), slóð, true);
                }
            }
        }
        현재과정.sett_forrit_hlé(새끝);
        return 새끝;
    }

    public int hækkun_forrit_hlé(Ferli_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.forrit_hlé();
        int NIÐURSTAÐA = forrit_hlé(현재과정, 이전끝 + 증가량);
        return NIÐURSTAÐA < 0 ? NIÐURSTAÐA : 이전끝;
    }

    public int keyra_skipun(Ferli_VALUE 현재과정, byte[] 실행파일) {
        return keyra_skipun(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int keyra_skipun(Ferli_VALUE 현재과정, byte[] 실행파일, String[] færibreyta_frumbreyta, String[] 환경) {
        실행파일적재기.mynd mynd_VALUE;
        try {
            mynd_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Villa) {
            return -8;
        }
        if (færibreyta_frumbreyta == null || 환경 == null || færibreyta_frumbreyta.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.hluti_VALUE hluti_VALUE : mynd_VALUE.구역들()) {
            if ((hluti_VALUE.flagg_VALUE() & 2) == 0 || hluti_VALUE.Stærð() == 0) {
                continue;
            }
            int 첫쪽 = hluti_VALUE.slóð() / síða_stjórnandi.síðustærð;
            int 끝쪽 = (hluti_VALUE.slóð() + hluti_VALUE.Stærð() + síða_stjórnandi.síðustærð - 1) / síða_stjórnandi.síðustærð;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int slóð = INDEX * síða_stjórnandi.síðustærð;
                try {
                    쪽관리.바이트읽기(현재과정.slóð_svæði(), slóð);
                    쪽관리.범위개인쓰기(현재과정.slóð_svæði(), slóð, síða_stjórnandi.síðustærð);
                } catch (IllegalStateException Villa) {
                    쪽관리.MAP_síða(현재과정.slóð_svæði(), slóð, true);
                }
            }
            for (int INDEX = 0; INDEX < hluti_VALUE.Stærð(); INDEX++) {
                byte VALUE = hluti_VALUE.종류() == 8 ? 0 : 실행파일[hluti_VALUE.skrá_staða_2aa21a9a() + INDEX];
                쪽관리.skrifa_bæti_VALUE(현재과정.slóð_svæði(), hluti_VALUE.slóð() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(mynd_VALUE.Opna_slóð(), færibreyta_frumbreyta, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void hætta_forrit(Ferli_VALUE 현재과정, int staða_VALUE_e10195a1) {
        현재과정.loka_forrit(staða_VALUE_e10195a1);
    }
}
