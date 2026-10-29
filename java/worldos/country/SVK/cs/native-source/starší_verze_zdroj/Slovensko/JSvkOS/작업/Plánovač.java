// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Slovensko.JSvkOS.Paměť_oblast.stránka_Správce;
import Slovensko.JSvkOS.systém_souborů.Soubor_popisovač_tabulka;

/** Proces_HODNOTA 식별자와 라운드로빈 Připravit 대기열을 관리한다. */
public final class Plánovač {
    private final stránka_Správce 쪽관리;
    private final Map<Integer, Proces_HODNOTA> Seznam_procesu = new HashMap<Integer, Proces_HODNOTA>();
    private final Queue<Proces_HODNOTA> 준비대기열 = new ArrayDeque<Proces_HODNOTA>();
    private int Další_identifikátor = 1;

    public Plánovač(stránka_Správce 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proces_HODNOTA 첫과정(Soubor_popisovač_tabulka Soubor_popisovač) {
        Proces_HODNOTA 새과정 = new Proces_HODNOTA(přidělit_identifikátor(), 0, 쪽관리.새주소공간(), Soubor_popisovač);
        Seznam_procesu.put(Integer.valueOf(새과정.identifikátor_HODNOTA()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proces_HODNOTA klon_HODNOTA(Proces_HODNOTA nadřazený_HODNOTA) {
        Proces_HODNOTA dítě_HODNOTA = new Proces_HODNOTA(
                přidělit_identifikátor(),
                nadřazený_HODNOTA.identifikátor_HODNOTA(),
                쪽관리.쓰기시복사복제(nadřazený_HODNOTA.adresní_prostor()),
                nadřazený_HODNOTA.Soubor_popisovač().klon_HODNOTA());
        dítě_HODNOTA.sada_program_přerušení(nadřazený_HODNOTA.program_přerušení());
        Seznam_procesu.put(Integer.valueOf(dítě_HODNOTA.identifikátor_HODNOTA()), dítě_HODNOTA);
        준비대기열.offer(dítě_HODNOTA);
        return dítě_HODNOTA;
    }

    public Proces_HODNOTA Další_Proces() {
        int šek_POČET = 준비대기열.size();
        for (int INDEX = 0; INDEX < šek_POČET; INDEX++) {
            Proces_HODNOTA Další_zboží = 준비대기열.poll();
            if (Další_zboží != null && (Další_zboží.Stav_HODNOTA() == Proces_Stav.Připravit || Další_zboží.Stav_HODNOTA() == Proces_Stav.Provést_příkaz)) {
                Další_zboží.sada_Stav(Proces_Stav.Provést_příkaz);
                준비대기열.offer(Další_zboží);
                return Další_zboží;
            }
        }
        return null;
    }

    public int 자식기다리기(Proces_HODNOTA nadřazený_HODNOTA, int dítě_identifikátor, boolean 기다리지않음) {
        for (Proces_HODNOTA 후보 : Seznam_procesu.values()) {
            if (후보.nadřazený_identifikátor() != nadřazený_HODNOTA.identifikátor_HODNOTA()) {
                continue;
            }
            if (dítě_identifikátor > 0 && 후보.identifikátor_HODNOTA() != dítě_identifikátor) {
                continue;
            }
            if (후보.Stav_HODNOTA() == Proces_Stav.Konec_program) {
                int VÝSLEDEK = (후보.ukončovací_kód() & 0xff) << 8;
                Seznam_procesu.remove(Integer.valueOf(후보.identifikátor_HODNOTA()));
                return VÝSLEDEK;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proces_HODNOTA NAJÍT_Proces(int identifikátor_HODNOTA) {
        return Seznam_procesu.get(Integer.valueOf(identifikátor_HODNOTA));
    }

    private int přidělit_identifikátor() {
        return Další_identifikátor++;
    }
}
