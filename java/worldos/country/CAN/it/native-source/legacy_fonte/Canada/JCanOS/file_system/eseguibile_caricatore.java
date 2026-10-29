// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.file_system;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Esegui_comando 파일의 머리부와 적재 구역을 검증한다. */
public final class eseguibile_caricatore {
    public static final class sezione_VALORE {
        private final int Kind_VALORE;
        private final int flag_VALORE;
        private final int e_mail;
        private final int File_funzione;
        private final int Dimensione;

        sezione_VALORE(int Kind_VALORE, int flag_VALORE, int e_mail, int File_funzione, int Dimensione) {
            this.Kind_VALORE = Kind_VALORE;
            this.flag_VALORE = flag_VALORE;
            this.e_mail = e_mail;
            this.File_funzione = File_funzione;
            this.Dimensione = Dimensione;
        }

        public int Kind_VALORE() {
            return Kind_VALORE;
        }

        public int flag_VALORE() {
            return flag_VALORE;
        }

        public int e_mail() {
            return e_mail;
        }

        public int File_funzione() {
            return File_funzione;
        }

        public int Dimensione() {
            return Dimensione;
        }
    }

    public static final class foto {
        private final int START_e_mail;
        private final List<sezione_VALORE> 구역들;

        foto(int START_e_mail, List<sezione_VALORE> 구역들) {
            this.START_e_mail = START_e_mail;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_e_mail() {
            return START_e_mail;
        }

        public List<sezione_VALORE> 구역들() {
            return 구역들;
        }
    }

    public foto 검사(byte[] dati) {
        if (dati == null || dati.length < 52
                || dati[0] != 0x7f || dati[1] != 'E' || dati[2] != 'L' || dati[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (dati[4] != 1 || dati[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_e_mail = analizzare_intero(dati, 24);
        int sezione_tabella_funzione = analizzare_intero(dati, 32);
        int sezione_voce_ridimensionare = 짧은정수읽기(dati, 46);
        int sezione_CONTA_NUMERI = 짧은정수읽기(dati, 48);
        if (sezione_voce_ridimensionare < 40 || sezione_tabella_funzione < 0
                || (long) sezione_tabella_funzione + (long) sezione_voce_ridimensionare * sezione_CONTA_NUMERI > dati.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sezione_VALORE> 구역들 = new ArrayList<sezione_VALORE>();
        for (int INDICE = 0; INDICE < sezione_CONTA_NUMERI; INDICE++) {
            int posizione = sezione_tabella_funzione + INDICE * sezione_voce_ridimensionare;
            int Kind_VALORE = analizzare_intero(dati, posizione + 4);
            int flag_VALORE = analizzare_intero(dati, posizione + 8);
            int e_mail = analizzare_intero(dati, posizione + 12);
            int File_funzione = analizzare_intero(dati, posizione + 16);
            int Dimensione = analizzare_intero(dati, posizione + 20);
            if (Dimensione < 0 || (Kind_VALORE != 8 && ((long) File_funzione + Dimensione > dati.length || File_funzione < 0))) {
                throw new IllegalArgumentException("ELF sezione_VALORE dati 범위가 올바르지 않습니다.");
            }
            구역들.add(new sezione_VALORE(Kind_VALORE, flag_VALORE, e_mail, File_funzione, Dimensione));
        }
        return new foto(START_e_mail, 구역들);
    }

    private int analizzare_intero(byte[] dati, int posizione) {
        if (posizione < 0 || posizione > dati.length - 4) {
            throw new IllegalArgumentException("ELF intero 범위를 벗어났습니다.");
        }
        return (dati[posizione] & 0xff)
                | ((dati[posizione + 1] & 0xff) << 8)
                | ((dati[posizione + 2] & 0xff) << 16)
                | ((dati[posizione + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] dati, int posizione) {
        if (posizione < 0 || posizione > dati.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 intero 범위를 벗어났습니다.");
        }
        return (dati[posizione] & 0xff) | ((dati[posizione + 1] & 0xff) << 8);
    }
}
