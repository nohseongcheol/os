// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Brasile.JBraOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Brasile.JBraOS.Memoria_area.Gestione_pagine;
import Brasile.JBraOS.file_system.File_descrittore_tabella;

/** Processi_VALORE 식별자와 라운드로빈 Prepara 대기열을 관리한다. */
public final class Pianificatore {
    private final Gestione_pagine 쪽관리;
    private final Map<Integer, Processi_VALORE> Elenco_processo = new HashMap<Integer, Processi_VALORE>();
    private final Queue<Processi_VALORE> 준비대기열 = new ArrayDeque<Processi_VALORE>();
    private int Avanti_identificatore = 1;

    public Pianificatore(Gestione_pagine 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Processi_VALORE 첫과정(File_descrittore_tabella File_descrittore) {
        Processi_VALORE 새과정 = new Processi_VALORE(allocare_identificatore(), 0, 쪽관리.새주소공간(), File_descrittore);
        Elenco_processo.put(Integer.valueOf(새과정.identificatore_VALORE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Processi_VALORE clone_VALORE(Processi_VALORE padre_VALORE) {
        Processi_VALORE figlio_VALORE = new Processi_VALORE(
                allocare_identificatore(),
                padre_VALORE.identificatore_VALORE(),
                쪽관리.clone_copia_su_scrittura(padre_VALORE.spazio_indirizzi()),
                padre_VALORE.File_descrittore().clone_VALORE());
        figlio_VALORE.set_app_pausa(padre_VALORE.app_pausa());
        Elenco_processo.put(Integer.valueOf(figlio_VALORE.identificatore_VALORE()), figlio_VALORE);
        준비대기열.offer(figlio_VALORE);
        return figlio_VALORE;
    }

    public Processi_VALORE Avanti_Processi() {
        int assegno_CONTA_NUMERI = 준비대기열.size();
        for (int INDICE = 0; INDICE < assegno_CONTA_NUMERI; INDICE++) {
            Processi_VALORE Avanti_articolo = 준비대기열.poll();
            if (Avanti_articolo != null && (Avanti_articolo.Stato_VALORE() == Processi_Stato.Prepara || Avanti_articolo.Stato_VALORE() == Processi_Stato.Esegui_comando)) {
                Avanti_articolo.set_Stato(Processi_Stato.Esegui_comando);
                준비대기열.offer(Avanti_articolo);
                return Avanti_articolo;
            }
        }
        return null;
    }

    public int 자식기다리기(Processi_VALORE padre_VALORE, int figlio_identificatore, boolean 기다리지않음) {
        for (Processi_VALORE candidato : Elenco_processo.values()) {
            if (candidato.padre_identificatore() != padre_VALORE.identificatore_VALORE()) {
                continue;
            }
            if (figlio_identificatore > 0 && candidato.identificatore_VALORE() != figlio_identificatore) {
                continue;
            }
            if (candidato.Stato_VALORE() == Processi_Stato.Esci_app) {
                int risultato = (candidato.codice_di_uscita() & 0xff) << 8;
                Elenco_processo.remove(Integer.valueOf(candidato.identificatore_VALORE()));
                return risultato;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Processi_VALORE TROVA_Processi(int identificatore_VALORE) {
        return Elenco_processo.get(Integer.valueOf(identificatore_VALORE));
    }

    private int allocare_identificatore() {
        return Avanti_identificatore++;
    }
}
