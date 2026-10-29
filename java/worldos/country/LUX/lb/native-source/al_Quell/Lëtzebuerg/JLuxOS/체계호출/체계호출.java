// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.체계호출;

import Lëtzebuerg.JLuxOS.기억공간.Säit_Manager;
import Lëtzebuerg.JLuxOS.작업.Prozess_VALUE;
import Lëtzebuerg.JLuxOS.작업.Planifikateur;
import Lëtzebuerg.JLuxOS.Fichierssystem.실행파일적재기;
import Lëtzebuerg.JLuxOS.Fichierssystem.Fichierssystem;
import Lëtzebuerg.JLuxOS.Fichierssystem.Fichier_Info;
import Lëtzebuerg.JLuxOS.Kernel.하드웨어;
import Lëtzebuerg.JLuxOS.입력.입력관리자;
import Lëtzebuerg.JLuxOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int schreifgeschützt_kennzeechnen = 0;
    public static final int Sich_Start = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_Agab_bëennegen = 2;

    private final Fichierssystem Fichierssystem;
    private final Säit_Manager 쪽관리;
    private final Planifikateur Planifikateur;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 Mobil_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(Fichierssystem Fichierssystem, Säit_Manager 쪽관리, Planifikateur Planifikateur, 하드웨어 Mobil_VALUE, 입력관리자 입력관리) {
        this.Fichierssystem = Fichierssystem;
        this.쪽관리 = 쪽관리;
        this.Planifikateur = Planifikateur;
        this.Mobil_VALUE = Mobil_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Prozess_Identifikateur(Prozess_VALUE 현재과정) {
        return 현재과정.Identifikateur_VALUE();
    }

    public int 부모과정식별자(Prozess_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int ariichten(Prozess_VALUE 현재과정, String Numm, int kennzeechnen_VALUE) {
        if (kennzeechnen_VALUE != schreifgeschützt_kennzeechnen) {
            return -30;
        }
        return 현재과정.파일서술자().ariichten(Numm);
    }

    public int 읽기(Prozess_VALUE 현재과정, int 서술자, byte[] 받을곳, int d_Gréisst_veränneren) {
        if (서술자 == 0) {
            if (d_Gréisst_veränneren <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 Evenement = 입력관리.Weider_Evenement();
            if (Evenement == null || Evenement.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) Evenement.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, d_Gréisst_veränneren);
    }

    public int schreiwen(Prozess_VALUE 현재과정, int 서술자, byte[] Daten, int d_Gréisst_veränneren) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (d_Gréisst_veränneren < 0 || d_Gréisst_veränneren > Daten.length) {
            return -22;
        }
        Mobil_VALUE.직렬출력(new String(Daten, 0, d_Gréisst_veränneren, java.nio.charset.StandardCharsets.UTF_8));
        return d_Gréisst_veränneren;
    }

    public int Clôture(Prozess_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Clôture(서술자);
    }

    public int verréckelen_positionéieren(Prozess_VALUE 현재과정, int 서술자, int 거리, int projezéieren_Racinn) {
        return 현재과정.파일서술자().verréckelen_positionéieren(서술자, 거리, projezéieren_Racinn);
    }

    public int 서술자복제(Prozess_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Prozess_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Numm, int Method_MODE) {
        Fichier_Info msinfo32_exe = Fichierssystem.msinfo32_exe(Numm);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((Method_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((Method_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_Aufgabelëscht(String Numm) {
        return "/".equals(Numm) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int Benotzer_Identifikateur() { return 0; }
    public int efficace_Benotzer_Identifikateur() { return 0; }
    public int Grupp_Identifikateur() { return 0; }
    public int efficace_Grupp_Identifikateur() { return 0; }

    public int synchroniséieren_Fichier(Prozess_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Prozess_VALUE 현재과정, int 서술자) {
        Fichier_Info msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int Fichier_Kontroll(Prozess_VALUE 현재과정, int 서술자, int Befeel, int 인자) {
        if (Befeel == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (Befeel == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Befeel == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (Befeel == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : schreifgeschützt_kennzeechnen;
        }
        if (Befeel == 4) {
            return 인자 == schreifgeschützt_kennzeechnen ? 0 : -30;
        }
        return -22;
    }

    public int Create_Agab(String Numm, int Geneemegung_VALUE) {
        return -30;
    }

    public Fichier_Info 서술자정보(Prozess_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JLuxOS", "JLuxOS", "0.1", "Java managed kernel", "i386");
    }

    public Fichier_Info Fichier_Info(String Numm) {
        return Fichierssystem.msinfo32_exe(Numm);
    }

    public Prozess_VALUE 과정복제(Prozess_VALUE 부모) {
        return Planifikateur.복제(부모);
    }

    public int 자식기다리기(Prozess_VALUE 부모, int Kand_Identifikateur, boolean 기다리지않음) {
        return Planifikateur.자식기다리기(부모, Kand_Identifikateur, 기다리지않음);
    }

    public int 프로그램끝(Prozess_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / Säit_Manager.Säitegréisst;
        int 끝쪽 = (새끝 + Säit_Manager.Säitegréisst - 1) / Säit_Manager.Säitegréisst;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int Adress = INDEX * Säit_Manager.Säitegréisst;
                try {
                    쪽관리.바이트읽기(현재과정.Adress_Plaz(), Adress);
                } catch (IllegalStateException Feeler) {
                    쪽관리.MAP_Säit(현재과정.Adress_Plaz(), Adress, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Prozess_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int Mooss = 프로그램끝(현재과정, 이전끝 + 증가량);
        return Mooss < 0 ? Mooss : 이전끝;
    }

    public int ausféieren_Befeel(Prozess_VALUE 현재과정, byte[] 실행파일) {
        return ausféieren_Befeel(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int ausféieren_Befeel(Prozess_VALUE 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.Bild Bild_VALUE;
        try {
            Bild_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Feeler) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.Beräich_VALUE Beräich_VALUE : Bild_VALUE.구역들()) {
            if ((Beräich_VALUE.kennzeechnen_VALUE() & 2) == 0 || Beräich_VALUE.d_Gréisst_veränneren() == 0) {
                continue;
            }
            int 첫쪽 = Beräich_VALUE.Adress() / Säit_Manager.Säitegréisst;
            int 끝쪽 = (Beräich_VALUE.Adress() + Beräich_VALUE.d_Gréisst_veränneren() + Säit_Manager.Säitegréisst - 1) / Säit_Manager.Säitegréisst;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int Adress = INDEX * Säit_Manager.Säitegréisst;
                try {
                    쪽관리.바이트읽기(현재과정.Adress_Plaz(), Adress);
                    쪽관리.범위개인쓰기(현재과정.Adress_Plaz(), Adress, Säit_Manager.Säitegréisst);
                } catch (IllegalStateException Feeler) {
                    쪽관리.MAP_Säit(현재과정.Adress_Plaz(), Adress, true);
                }
            }
            for (int INDEX = 0; INDEX < Beräich_VALUE.d_Gréisst_veränneren(); INDEX++) {
                byte VALUE = Beräich_VALUE.종류() == 8 ? 0 : 실행파일[Beräich_VALUE.Fichier_positionéieren() + INDEX];
                쪽관리.schreiwen_Byte_VALUE(현재과정.Adress_Plaz(), Beräich_VALUE.Adress() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(Bild_VALUE.Start_Adress(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void verloossen_App(Prozess_VALUE 현재과정, int Status_VALUE) {
        현재과정.Schluss_App(Status_VALUE);
    }
}
