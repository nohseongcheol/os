// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukraina.JUkrOS.jądro;

import Ukraina.JUkrOS.Pamięć_region.Pamięć_Menedżer;
import Ukraina.JUkrOS.Pamięć_region.strona_Menedżer;
import Ukraina.JUkrOS.wejście_WARTOŚĆ.wejście_Menedżer;
import Ukraina.JUkrOS.작업.Proces_WARTOŚĆ;
import Ukraina.JUkrOS.작업.Scheduler;
import Ukraina.JUkrOS.wywołanie_systemowe.wywołanie_systemowe;
import Ukraina.JUkrOS.system_plików.Plik_deskryptor_tabela;
import Ukraina.JUkrOS.system_plików.system_plików;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class jądro {
    private final sprzęt_WARTOŚĆ urządzenie_WARTOŚĆ;
    private final Pamięć_Menedżer Pamięć_region = new Pamięć_Menedżer(32 * 1024 * 1024);
    private final strona_Menedżer 쪽관리 = new strona_Menedżer();
    private final system_plików system_plików = new system_plików();
    private final Scheduler Scheduler = new Scheduler(쪽관리);
    private final wejście_Menedżer 입력관리 = new wejście_Menedżer(256);
    private final Proces_WARTOŚĆ 첫과정;
    private final wywołanie_systemowe wywołanie_systemowe;

    public jądro(sprzęt_WARTOŚĆ urządzenie_WARTOŚĆ) {
        this.urządzenie_WARTOŚĆ = urządzenie_WARTOŚĆ;
        첫과정 = Scheduler.첫과정(new Plik_deskryptor_tabela(system_plików));
        wywołanie_systemowe = new wywołanie_systemowe(system_plików, 쪽관리, Scheduler, urządzenie_WARTOŚĆ, 입력관리);
    }

    public void Uruchom_2() {
        urządzenie_WARTOŚĆ.직렬출력("=== JUkrOS 관리 jądro_WARTOŚĆ ===\n");
    }

    public void Wykonaj_krok() {
        urządzenie_WARTOŚĆ.중앙처리장치멈춤();
    }

    public Pamięć_Menedżer Pamięć_region() {
        return Pamięć_region;
    }

    public strona_Menedżer 쪽관리() {
        return 쪽관리;
    }

    public system_plików system_plików() {
        return system_plików;
    }

    public Scheduler Scheduler() {
        return Scheduler;
    }

    public wejście_Menedżer 입력관리() {
        return 입력관리;
    }

    public Proces_WARTOŚĆ 첫과정() {
        return 첫과정;
    }

    public wywołanie_systemowe wywołanie_systemowe() {
        return wywołanie_systemowe;
    }
}
