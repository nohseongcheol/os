// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukrajna.JUkrOS.kernel;

import Ukrajna.JUkrOS.Memória_régió.Memória_kezelő;
import Ukrajna.JUkrOS.Memória_régió.lap_kezelő;
import Ukrajna.JUkrOS.bevitel_ÉRTÉK.bevitel_kezelő;
import Ukrajna.JUkrOS.작업.folyamat_ÉRTÉK;
import Ukrajna.JUkrOS.작업.Ütemező;
import Ukrajna.JUkrOS.체계호출.체계호출;
import Ukrajna.JUkrOS.fájlrendszer.파일서술자표;
import Ukrajna.JUkrOS.fájlrendszer.fájlrendszer;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kernel {
    private final hardver_ÉRTÉK mobil_ÉRTÉK;
    private final Memória_kezelő Memória_régió = new Memória_kezelő(32 * 1024 * 1024);
    private final lap_kezelő 쪽관리 = new lap_kezelő();
    private final fájlrendszer fájlrendszer = new fájlrendszer();
    private final Ütemező Ütemező = new Ütemező(쪽관리);
    private final bevitel_kezelő 입력관리 = new bevitel_kezelő(256);
    private final folyamat_ÉRTÉK 첫과정;
    private final 체계호출 체계호출;

    public kernel(hardver_ÉRTÉK mobil_ÉRTÉK) {
        this.mobil_ÉRTÉK = mobil_ÉRTÉK;
        첫과정 = Ütemező.첫과정(new 파일서술자표(fájlrendszer));
        체계호출 = new 체계호출(fájlrendszer, 쪽관리, Ütemező, mobil_ÉRTÉK, 입력관리);
    }

    public void Futtatás() {
        mobil_ÉRTÉK.직렬출력("=== JUkrOS 관리 kernel_ÉRTÉK ===\n");
    }

    public void végrehajt_lépés() {
        mobil_ÉRTÉK.중앙처리장치멈춤();
    }

    public Memória_kezelő Memória_régió() {
        return Memória_régió;
    }

    public lap_kezelő 쪽관리() {
        return 쪽관리;
    }

    public fájlrendszer fájlrendszer() {
        return fájlrendszer;
    }

    public Ütemező Ütemező() {
        return Ütemező;
    }

    public bevitel_kezelő 입력관리() {
        return 입력관리;
    }

    public folyamat_ÉRTÉK 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
