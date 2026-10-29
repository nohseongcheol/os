// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Caribisch_Nederland.JBesOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Caribisch_Nederland.JBesOS.Geheugen_regio.Paginabeheer;
import Caribisch_Nederland.JBesOS.bestandssysteem.파일서술자표;

/** Proces_WAARDE 식별자와 라운드로빈 Bereid_voor 대기열을 관리한다. */
public final class Planner {
    private final Paginabeheer 쪽관리;
    private final Map<Integer, Proces_WAARDE> Proceslijst = new HashMap<Integer, Proces_WAARDE>();
    private final Queue<Proces_WAARDE> 준비대기열 = new ArrayDeque<Proces_WAARDE>();
    private int Volgende_id = 1;

    public Planner(Paginabeheer 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proces_WAARDE 첫과정(파일서술자표 파일서술자) {
        Proces_WAARDE 새과정 = new Proces_WAARDE(toewijzen_id(), 0, 쪽관리.새주소공간(), 파일서술자);
        Proceslijst.put(Integer.valueOf(새과정.id_WAARDE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proces_WAARDE kloon_WAARDE(Proces_WAARDE bovenliggend_WAARDE) {
        Proces_WAARDE kind_WAARDE = new Proces_WAARDE(
                toewijzen_id(),
                bovenliggend_WAARDE.id_WAARDE(),
                쪽관리.kloon_kopiëren_bij_schrijven(bovenliggend_WAARDE.adresruimte()),
                bovenliggend_WAARDE.파일서술자().kloon_WAARDE());
        kind_WAARDE.set_app_pauze(bovenliggend_WAARDE.app_pauze());
        Proceslijst.put(Integer.valueOf(kind_WAARDE.id_WAARDE()), kind_WAARDE);
        준비대기열.offer(kind_WAARDE);
        return kind_WAARDE;
    }

    public Proces_WAARDE Volgende_Proces() {
        int cheque_AANTAL = 준비대기열.size();
        for (int INDEX = 0; INDEX < cheque_AANTAL; INDEX++) {
            Proces_WAARDE Volgende_item = 준비대기열.poll();
            if (Volgende_item != null && (Volgende_item.Status_WAARDE() == Proces_Status.Bereid_voor || Volgende_item.Status_WAARDE() == Proces_Status.Uitvoeren_opdracht)) {
                Volgende_item.set_Status(Proces_Status.Uitvoeren_opdracht);
                준비대기열.offer(Volgende_item);
                return Volgende_item;
            }
        }
        return null;
    }

    public int 자식기다리기(Proces_WAARDE bovenliggend_WAARDE, int kind_id, boolean 기다리지않음) {
        for (Proces_WAARDE sollicitant : Proceslijst.values()) {
            if (sollicitant.bovenliggend_id() != bovenliggend_WAARDE.id_WAARDE()) {
                continue;
            }
            if (kind_id > 0 && sollicitant.id_WAARDE() != kind_id) {
                continue;
            }
            if (sollicitant.Status_WAARDE() == Proces_Status.Einde_app) {
                int resultaat = (sollicitant.afsluitcode() & 0xff) << 8;
                Proceslijst.remove(Integer.valueOf(sollicitant.id_WAARDE()));
                return resultaat;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proces_WAARDE Zoeken_Proces(int id_WAARDE) {
        return Proceslijst.get(Integer.valueOf(id_WAARDE));
    }

    private int toewijzen_id() {
        return Volgende_id++;
    }
}
