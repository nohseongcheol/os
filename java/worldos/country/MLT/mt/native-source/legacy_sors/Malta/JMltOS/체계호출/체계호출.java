// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.체계호출;

import Malta.JMltOS.기억공간.paġna_maniġer;
import Malta.JMltOS.작업.Proċess_VALUE;
import Malta.JMltOS.작업.Skedatur;
import Malta.JMltOS.sistema_tal_fajls.실행파일적재기;
import Malta.JMltOS.sistema_tal_fajls.sistema_tal_fajls;
import Malta.JMltOS.sistema_tal_fajls.fajl_informazzjoni;
import Malta.JMltOS.kernel.하드웨어;
import Malta.JMltOS.입력.입력관리자;
import Malta.JMltOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int qari_biss_mmarka = 0;
    public static final int SEARCH_Bidu = 0;
    public static final int 찾기현재 = 1;
    public static final int sab_entrata_ttermina = 2;

    private final sistema_tal_fajls sistema_tal_fajls;
    private final paġna_maniġer 쪽관리;
    private final Skedatur Skedatur;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 mowbajl_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(sistema_tal_fajls sistema_tal_fajls, paġna_maniġer 쪽관리, Skedatur Skedatur, 하드웨어 mowbajl_VALUE, 입력관리자 입력관리) {
        this.sistema_tal_fajls = sistema_tal_fajls;
        this.쪽관리 = 쪽관리;
        this.Skedatur = Skedatur;
        this.mowbajl_VALUE = mowbajl_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Proċess_identifikatur(Proċess_VALUE 현재과정) {
        return 현재과정.identifikatur_VALUE();
    }

    public int 부모과정식별자(Proċess_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int fetaħ(Proċess_VALUE 현재과정, String isem, int mmarka_VALUE) {
        if (mmarka_VALUE != qari_biss_mmarka) {
            return -30;
        }
        return 현재과정.파일서술자().fetaħ(isem);
    }

    public int 읽기(Proċess_VALUE 현재과정, int 서술자, byte[] 받을곳, int daqqas) {
        if (서술자 == 0) {
            if (daqqas <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 avveniment = 입력관리.Li_Jmiss_avveniment();
            if (avveniment == null || avveniment.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) avveniment.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, daqqas);
    }

    public int kiteb(Proċess_VALUE 현재과정, int 서술자, byte[] data, int daqqas) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (daqqas < 0 || daqqas > data.length) {
            return -22;
        }
        mowbajl_VALUE.직렬출력(new String(data, 0, daqqas, java.nio.charset.StandardCharsets.UTF_8));
        return daqqas;
    }

    public int agħlaq(Proċess_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().agħlaq(서술자);
    }

    public int mexxi_pożizzjoni(Proċess_VALUE 현재과정, int 서술자, int 거리, int pprojetta_għerq) {
        return 현재과정.파일서술자().mexxi_pożizzjoni(서술자, 거리, pprojetta_għerq);
    }

    public int 서술자복제(Proċess_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proċess_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String isem, int metodu_MODE) {
        fajl_informazzjoni msinfo32_exe = sistema_tal_fajls.msinfo32_exe(isem);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metodu_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metodu_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int qaleb_lista_ta_attivitajiet(String isem) {
        return "/".equals(isem) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int utent_identifikatur() { return 0; }
    public int effettiv_utent_identifikatur() { return 0; }
    public int grupp_identifikatur() { return 0; }
    public int effettiv_grupp_identifikatur() { return 0; }

    public int ssinkronizza_fajl(Proċess_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Proċess_VALUE 현재과정, int 서술자) {
        fajl_informazzjoni msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int fajl_kontroll(Proċess_VALUE 현재과정, int 서술자, int kmand, int 인자) {
        if (kmand == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (kmand == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (kmand == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (kmand == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : qari_biss_mmarka;
        }
        if (kmand == 4) {
            return 인자 == qari_biss_mmarka ? 0 : -30;
        }
        return -22;
    }

    public int ħalaq_entrata(String isem, int permess_VALUE) {
        return -30;
    }

    public fajl_informazzjoni 서술자정보(Proċess_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JMltOS", "JMltOS", "0.1", "Java managed kernel", "i386");
    }

    public fajl_informazzjoni fajl_informazzjoni(String isem) {
        return sistema_tal_fajls.msinfo32_exe(isem);
    }

    public Proċess_VALUE 과정복제(Proċess_VALUE 부모) {
        return Skedatur.복제(부모);
    }

    public int 자식기다리기(Proċess_VALUE 부모, int tfal_identifikatur, boolean 기다리지않음) {
        return Skedatur.자식기다리기(부모, tfal_identifikatur, 기다리지않음);
    }

    public int 프로그램끝(Proċess_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / paġna_maniġer.daqs_tal_paġna;
        int 끝쪽 = (새끝 + paġna_maniġer.daqs_tal_paġna - 1) / paġna_maniġer.daqs_tal_paġna;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * paġna_maniġer.daqs_tal_paġna;
                try {
                    쪽관리.바이트읽기(현재과정.ADDRESS_SPACE(), ADDRESS);
                } catch (IllegalStateException żball) {
                    쪽관리.MAP_paġna(현재과정.ADDRESS_SPACE(), ADDRESS, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Proċess_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int miżura = 프로그램끝(현재과정, 이전끝 + 증가량);
        return miżura < 0 ? miżura : 이전끝;
    }

    public int eżegwixxa_kmand(Proċess_VALUE 현재과정, byte[] 실행파일) {
        return eżegwixxa_kmand(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int eżegwixxa_kmand(Proċess_VALUE 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException żball) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.taqsima_VALUE_366e0bfa taqsima_VALUE_366e0bfa : IMAGE_VALUE.구역들()) {
            if ((taqsima_VALUE_366e0bfa.mmarka_VALUE() & 2) == 0 || taqsima_VALUE_366e0bfa.daqqas() == 0) {
                continue;
            }
            int 첫쪽 = taqsima_VALUE_366e0bfa.ADDRESS() / paġna_maniġer.daqs_tal_paġna;
            int 끝쪽 = (taqsima_VALUE_366e0bfa.ADDRESS() + taqsima_VALUE_366e0bfa.daqqas() + paġna_maniġer.daqs_tal_paġna - 1) / paġna_maniġer.daqs_tal_paġna;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int ADDRESS = INDEX * paġna_maniġer.daqs_tal_paġna;
                try {
                    쪽관리.바이트읽기(현재과정.ADDRESS_SPACE(), ADDRESS);
                    쪽관리.범위개인쓰기(현재과정.ADDRESS_SPACE(), ADDRESS, paġna_maniġer.daqs_tal_paġna);
                } catch (IllegalStateException żball) {
                    쪽관리.MAP_paġna(현재과정.ADDRESS_SPACE(), ADDRESS, true);
                }
            }
            for (int INDEX = 0; INDEX < taqsima_VALUE_366e0bfa.daqqas(); INDEX++) {
                byte VALUE = taqsima_VALUE_366e0bfa.종류() == 8 ? 0 : 실행파일[taqsima_VALUE_366e0bfa.fajl_pożizzjoni() + INDEX];
                쪽관리.kiteb_byte_VALUE(현재과정.ADDRESS_SPACE(), taqsima_VALUE_366e0bfa.ADDRESS() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(IMAGE_VALUE.Bidu_ADDRESS(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void ħruġ_programm(Proċess_VALUE 현재과정, int stat_VALUE) {
        현재과정.Ħruġ_programm(stat_VALUE);
    }
}
