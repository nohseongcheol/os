// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Austria.JAutOS.Memoria_area;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB pagina_VALORE 연결과 Scrittura 시 복사를 제공한다. */
public final class Gestione_pagine {
    public static final int dimensioni_della_pagina = 4096;

    private static final class pagina_VALORE {
        private byte[] dati = new byte[dimensioni_della_pagina];
        private int fonti_CONTA_NUMERI = 1;
        private boolean 쓰기가능 = true;
        private boolean copia_su_scrittura;
    }

    public static final class spazio_indirizzi {
        private final Map<Integer, pagina_VALORE> pagina_tabella = new HashMap<Integer, pagina_VALORE>();
    }

    public spazio_indirizzi 새주소공간() {
        return new spazio_indirizzi();
    }

    public void MAP_pagina(spazio_indirizzi e_mail_area, int indirizzo_virtuale, boolean 쓰기가능) {
        int INDICE = pagina_numero(indirizzo_virtuale);
        pagina_VALORE 새쪽 = new pagina_VALORE();
        새쪽.쓰기가능 = 쓰기가능;
        e_mail_area.pagina_tabella.put(Integer.valueOf(INDICE), 새쪽);
    }

    public spazio_indirizzi clone_copia_su_scrittura(spazio_indirizzi 원본) {
        spazio_indirizzi 복제본 = new spazio_indirizzi();
        for (Map.Entry<Integer, pagina_VALORE> voce_VALORE : 원본.pagina_tabella.entrySet()) {
            pagina_VALORE Condiviso_pagina = voce_VALORE.getValue();
            Condiviso_pagina.fonti_CONTA_NUMERI++;
            if (Condiviso_pagina.쓰기가능) {
                Condiviso_pagina.쓰기가능 = false;
                Condiviso_pagina.copia_su_scrittura = true;
            }
            복제본.pagina_tabella.put(voce_VALORE.getKey(), Condiviso_pagina);
        }
        return 복제본;
    }

    public byte 바이트읽기(spazio_indirizzi e_mail_area, int indirizzo_virtuale) {
        pagina_VALORE target = TROVA_pagina(e_mail_area, indirizzo_virtuale);
        return target.dati[Math.floorMod(indirizzo_virtuale, dimensioni_della_pagina)];
    }

    public void scrivere_byte_VALORE(spazio_indirizzi e_mail_area, int indirizzo_virtuale, byte VALORE) {
        int INDICE = pagina_numero(indirizzo_virtuale);
        pagina_VALORE target = TROVA_pagina(e_mail_area, indirizzo_virtuale);
        if (!target.쓰기가능) {
            if (!target.copia_su_scrittura) {
                throw new IllegalStateException("Lettura 전용 쪽입니다.");
            }
            target = Crea_escludi_pagina(e_mail_area, INDICE, target);
        }
        target.dati[Math.floorMod(indirizzo_virtuale, dimensioni_della_pagina)] = VALORE;
    }

    public void escludi_intervallo_scrivere(spazio_indirizzi e_mail_area, int START_e_mail, int Dimensione) {
        if (Dimensione < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int indirizzo_finale = Math.addExact(START_e_mail, Dimensione);
        for (int e_mail = START_e_mail; e_mail < indirizzo_finale; e_mail = (pagina_numero(e_mail) + 1) * dimensioni_della_pagina) {
            int INDICE = pagina_numero(e_mail);
            pagina_VALORE target = TROVA_pagina(e_mail_area, e_mail);
            if (target.copia_su_scrittura) {
                Crea_escludi_pagina(e_mail_area, INDICE, target);
            } else {
                target.쓰기가능 = true;
            }
        }
    }

    public void intervallo_scrivere(spazio_indirizzi e_mail_area, int START_e_mail, byte[] dati) {
        for (int INDICE = 0; INDICE < dati.length; INDICE++) {
            scrivere_byte_VALORE(e_mail_area, START_e_mail + INDICE, dati[INDICE]);
        }
    }

    private pagina_VALORE Crea_escludi_pagina(spazio_indirizzi e_mail_area, int INDICE, pagina_VALORE Condiviso_pagina) {
        pagina_VALORE escludi_pagina = new pagina_VALORE();
        escludi_pagina.dati = Arrays.copyOf(Condiviso_pagina.dati, Condiviso_pagina.dati.length);
        escludi_pagina.쓰기가능 = true;
        escludi_pagina.copia_su_scrittura = false;
        Condiviso_pagina.fonti_CONTA_NUMERI--;
        e_mail_area.pagina_tabella.put(Integer.valueOf(INDICE), escludi_pagina);
        return escludi_pagina;
    }

    private pagina_VALORE TROVA_pagina(spazio_indirizzi e_mail_area, int e_mail) {
        pagina_VALORE target = e_mail_area.pagina_tabella.get(Integer.valueOf(pagina_numero(e_mail)));
        if (target == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return target;
    }

    private int pagina_numero(int e_mail) {
        if (e_mail < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return e_mail / dimensioni_della_pagina;
    }
}

