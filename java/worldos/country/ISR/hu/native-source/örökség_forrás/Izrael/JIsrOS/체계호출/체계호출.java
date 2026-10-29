// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Izrael.JIsrOS.체계호출;

import Izrael.JIsrOS.Memória_régió.lap_kezelő;
import Izrael.JIsrOS.작업.folyamat_ÉRTÉK;
import Izrael.JIsrOS.작업.Ütemező;
import Izrael.JIsrOS.fájlrendszer.végrehajtható_betöltő;
import Izrael.JIsrOS.fájlrendszer.fájlrendszer;
import Izrael.JIsrOS.fájlrendszer.Fájl_infó;
import Izrael.JIsrOS.kernel.hardver_ÉRTÉK;
import Izrael.JIsrOS.bevitel_ÉRTÉK.bevitel_kezelő;
import Izrael.JIsrOS.bevitel_ÉRTÉK.bevitel_esemény;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int írásvédett_jelölő = 0;
    public static final int keres_START = 0;
    public static final int keres_aktuális = 1;
    public static final int keres_bejegyzés_megszüntet = 2;

    private final fájlrendszer fájlrendszer;
    private final lap_kezelő 쪽관리;
    private final Ütemező Ütemező;
    private final végrehajtható_betöltő betöltő = new végrehajtható_betöltő();
    private final hardver_ÉRTÉK mobil_ÉRTÉK;
    private final bevitel_kezelő 입력관리;

    public 체계호출(fájlrendszer fájlrendszer, lap_kezelő 쪽관리, Ütemező Ütemező, hardver_ÉRTÉK mobil_ÉRTÉK, bevitel_kezelő 입력관리) {
        this.fájlrendszer = fájlrendszer;
        this.쪽관리 = 쪽관리;
        this.Ütemező = Ütemező;
        this.mobil_ÉRTÉK = mobil_ÉRTÉK;
        this.입력관리 = 입력관리;
    }

    public int folyamat_azonosító(folyamat_ÉRTÉK aktuális_folyamat) {
        return aktuális_folyamat.azonosító_ÉRTÉK();
    }

    public int szülő_folyamat_azonosító(folyamat_ÉRTÉK aktuális_folyamat) {
        return aktuális_folyamat.szülő_azonosító();
    }

    public int Megnyitás(folyamat_ÉRTÉK aktuális_folyamat, String Név, int jelölő_ÉRTÉK_58846146) {
        if (jelölő_ÉRTÉK_58846146 != írásvédett_jelölő) {
            return -30;
        }
        return aktuális_folyamat.파일서술자().Megnyitás(Név);
    }

    public int Olvasás(folyamat_ÉRTÉK aktuális_folyamat, int 서술자, byte[] fogad_cél, int Méret) {
        if (서술자 == 0) {
            if (Méret <= 0 || fogad_cél.length == 0) {
                return 0;
            }
            bevitel_esemény Esemény = 입력관리.Tovább_esemény();
            if (Esemény == null || Esemény.eseményfajta() != bevitel_esemény.Altípus_ÉRTÉK.키누름) {
                return -11;
            }
            fogad_cél[0] = (byte) Esemény.첫째값();
            return 1;
        }
        return aktuális_folyamat.파일서술자().Olvasás(서술자, fogad_cél, Méret);
    }

    public int Írás(folyamat_ÉRTÉK aktuális_folyamat, int 서술자, byte[] adat, int Méret) {
        if (서술자 != 1 && 서술자 != 2) {
            return aktuális_folyamat.파일서술자().informatikai_részleg_készít(서술자) ? -30 : -9;
        }
        if (Méret < 0 || Méret > adat.length) {
            return -22;
        }
        mobil_ÉRTÉK.직렬출력(new String(adat, 0, Méret, java.nio.charset.StandardCharsets.UTF_8));
        return Méret;
    }

    public int Bezárás(folyamat_ÉRTÉK aktuális_folyamat, int 서술자) {
        return aktuális_folyamat.파일서술자().Bezárás(서술자);
    }

    public int áthelyez_pozíció(folyamat_ÉRTÉK aktuális_folyamat, int 서술자, int 거리, int teendő_gyök) {
        return aktuális_folyamat.파일서술자().áthelyez_pozíció(서술자, 거리, teendő_gyök);
    }

    public int 서술자복제(folyamat_ÉRTÉK aktuális_folyamat, int 서술자) {
        return aktuális_folyamat.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(folyamat_ÉRTÉK aktuális_folyamat, int 서술자, int 새서술자) {
        return aktuális_folyamat.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Név, int metódus_mód) {
        Fájl_infó msinfo32_exe = fájlrendszer.msinfo32_exe(Név);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metódus_mód & 1) != 0 && (msinfo32_exe.alakzat_Altípus() & 0111) == 0) {
            return -13;
        }
        if ((metódus_mód & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int vált_Feladatlista(String Név) {
        return "/".equals(Név) ? 0 : -20;
    }

    public String aktuális_Feladatlista(int fogad_méretez) {
        return fogad_méretez >= 2 ? "/" : null;
    }

    public int felhasználóazonosító() { return 0; }
    public int hatékony_felhasználóazonosító() { return 0; }
    public int GID() { return 0; }
    public int hatékony_GID() { return 0; }

    public int szinkronizál_Fájl(folyamat_ÉRTÉK aktuális_folyamat, int 서술자) {
        return aktuális_folyamat.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // aktuális_cikk 파일체계는 Olvasás 전용이어서 밀어낼 자료가 없다.
    }

    public boolean informatikai_részleg_Terminál(folyamat_ÉRTÉK aktuális_folyamat, int 서술자) {
        Fájl_infó msinfo32_exe = aktuális_folyamat.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.alakzat_Altípus() & 0170000) == 0020000;
    }

    public int Fájl_vezérlő(folyamat_ÉRTÉK aktuális_folyamat, int 서술자, int Parancs, int paraméter_argumentum) {
        if (Parancs == 0) {
            return aktuális_folyamat.파일서술자().복제서술자(서술자, paraméter_argumentum);
        }
        if (Parancs == 1) {
            return aktuális_folyamat.파일서술자().실행시닫기값(서술자);
        }
        if (Parancs == 2) {
            return aktuális_folyamat.파일서술자().실행시닫기설정(서술자, (paraméter_argumentum & 1) != 0);
        }
        if (Parancs == 3) {
            return aktuális_folyamat.파일서술자().msinfo32_exe(서술자) == null ? -9 : írásvédett_jelölő;
        }
        if (Parancs == 4) {
            return paraméter_argumentum == írásvédett_jelölő ? 0 : -30;
        }
        return -22;
    }

    public int készít_bejegyzés(String Név, int engedély_ÉRTÉK) {
        return -30;
    }

    public Fájl_infó 서술자정보(folyamat_ÉRTÉK aktuális_folyamat, int 서술자) {
        return aktuális_folyamat.파일서술자().msinfo32_exe(서술자);
    }

    public Rendszer_Részletek Rendszer_Részletek() {
        return new Rendszer_Részletek("JIsrOS", "JIsrOS", "0.1", "Java managed kernel", "i386");
    }

    public Fájl_infó Fájl_infó(String Név) {
        return fájlrendszer.msinfo32_exe(Név);
    }

    public folyamat_ÉRTÉK klón_folyamat(folyamat_ÉRTÉK szülő_ÉRTÉK) {
        return Ütemező.klón_ÉRTÉK(szülő_ÉRTÉK);
    }

    public int 자식기다리기(folyamat_ÉRTÉK szülő_ÉRTÉK, int gyermek_azonosító, boolean 기다리지않음) {
        return Ütemező.자식기다리기(szülő_ÉRTÉK, gyermek_azonosító, 기다리지않음);
    }

    public int app_szünet(folyamat_ÉRTÉK aktuális_folyamat, int 새끝) {
        int Előző_megszüntet = aktuális_folyamat.app_szünet();
        if (새끝 == 0) {
            return Előző_megszüntet;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Előző_megszüntet / lap_kezelő.oldalméret;
        int 끝쪽 = (새끝 + lap_kezelő.oldalméret - 1) / lap_kezelő.oldalméret;
        if (새끝 > Előző_megszüntet) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int CÍM = INDEX * lap_kezelő.oldalméret;
                try {
                    쪽관리.바이트읽기(aktuális_folyamat.címtartomány(), CÍM);
                } catch (IllegalStateException HIBA) {
                    쪽관리.MAP_lap(aktuális_folyamat.címtartomány(), CÍM, true);
                }
            }
        }
        aktuális_folyamat.halmaz_app_szünet(새끝);
        return 새끝;
    }

    public int növelés_app_szünet(folyamat_ÉRTÉK aktuális_folyamat, int növekmény_összeg) {
        int Előző_megszüntet = aktuális_folyamat.app_szünet();
        int KR = app_szünet(aktuális_folyamat, Előző_megszüntet + növekmény_összeg);
        return KR < 0 ? KR : Előző_megszüntet;
    }

    public int végrehajt_parancs(folyamat_ÉRTÉK aktuális_folyamat, byte[] végrehajtható_Fájl) {
        return végrehajt_parancs(aktuális_folyamat, végrehajtható_Fájl, new String[0], new String[0]);
    }

    public int végrehajt_parancs(folyamat_ÉRTÉK aktuális_folyamat, byte[] végrehajtható_Fájl, String[] paraméter_argumentum, String[] környezet_5d36e09c) {
        végrehajtható_betöltő.KÉP KÉP_ÉRTÉK;
        try {
            KÉP_ÉRTÉK = betöltő.검사(végrehajtható_Fájl);
        } catch (IllegalArgumentException HIBA) {
            return -8;
        }
        if (paraméter_argumentum == null || környezet_5d36e09c == null || paraméter_argumentum.length > 16 || környezet_5d36e09c.length > 16) {
            return -7;
        }
        for (végrehajtható_betöltő.szakasz_ÉRTÉK szakasz_ÉRTÉK : KÉP_ÉRTÉK.구역들()) {
            if ((szakasz_ÉRTÉK.jelölő_ÉRTÉK_58846146() & 2) == 0 || szakasz_ÉRTÉK.Méret() == 0) {
                continue;
            }
            int 첫쪽 = szakasz_ÉRTÉK.CÍM() / lap_kezelő.oldalméret;
            int 끝쪽 = (szakasz_ÉRTÉK.CÍM() + szakasz_ÉRTÉK.Méret() + lap_kezelő.oldalméret - 1) / lap_kezelő.oldalméret;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int CÍM = INDEX * lap_kezelő.oldalméret;
                try {
                    쪽관리.바이트읽기(aktuális_folyamat.címtartomány(), CÍM);
                    쪽관리.privát_tartomány_ír(aktuális_folyamat.címtartomány(), CÍM, lap_kezelő.oldalméret);
                } catch (IllegalStateException HIBA) {
                    쪽관리.MAP_lap(aktuális_folyamat.címtartomány(), CÍM, true);
                }
            }
            for (int INDEX = 0; INDEX < szakasz_ÉRTÉK.Méret(); INDEX++) {
                byte ÉRTÉK = szakasz_ÉRTÉK.Altípus_ÉRTÉK() == 8 ? 0 : végrehajtható_Fájl[szakasz_ÉRTÉK.Fájl_pozíció() + INDEX];
                쪽관리.ír_bájt_ÉRTÉK(aktuális_folyamat.címtartomány(), szakasz_ÉRTÉK.CÍM() + INDEX, ÉRTÉK);
            }
        }
        aktuális_folyamat.halmaz_végrehajtás_környezet(KÉP_ÉRTÉK.START_CÍM(), paraméter_argumentum, környezet_5d36e09c);
        aktuális_folyamat.파일서술자().실행시닫기();
        return 0;
    }

    public void kilépés_app(folyamat_ÉRTÉK aktuális_folyamat, int Állapot_ÉRTÉK) {
        aktuális_folyamat.kilép_app(Állapot_ÉRTÉK);
    }
}
