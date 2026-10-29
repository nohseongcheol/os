// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package San_Marino.JSmrOS.dispositivo_di_archiviazione;

import java.util.Arrays;

/** ATA 28비트 comando 계층과 같은 512바이트 논리 sezione_VALORE 장치다. */
public final class 고급기술결합장치 {
    public static final int sezione_ridimensionare = 512;
    private final byte[] dati;
    private final boolean di_sola_lettura_VALORE;

    public 고급기술결합장치(int sezione_CONTA_NUMERI, boolean di_sola_lettura_VALORE) {
        if (sezione_CONTA_NUMERI <= 0) {
            throw new IllegalArgumentException("sezione_VALORE 수가 올바르지 않습니다.");
        }
        dati = new byte[Math.multiplyExact(sezione_CONTA_NUMERI, sezione_ridimensionare)];
        this.di_sola_lettura_VALORE = di_sola_lettura_VALORE;
    }

    public int sezione_CONTA_NUMERI() {
        return dati.length / sezione_ridimensionare;
    }

    public void Lettura(int sezione_INDICE, byte[] ricevere_meta) {
        assegno_intervallo(sezione_INDICE, ricevere_meta);
        System.arraycopy(dati, sezione_INDICE * sezione_ridimensionare, ricevere_meta, 0, sezione_ridimensionare);
    }

    public void Scrittura(int sezione_INDICE, byte[] 쓸자료) {
        if (di_sola_lettura_VALORE) {
            throw new IllegalStateException("Lettura 전용 장치입니다.");
        }
        assegno_intervallo(sezione_INDICE, 쓸자료);
        System.arraycopy(쓸자료, 0, dati, sezione_INDICE * sezione_ridimensionare, sezione_ridimensionare);
    }

    public void cancellare_voce() {
        if (di_sola_lettura_VALORE) {
            throw new IllegalStateException("Lettura 전용 장치입니다.");
        }
        Arrays.fill(dati, (byte) 0);
    }

    private void assegno_intervallo(int sezione_INDICE, byte[] 임시공간) {
        if (sezione_INDICE < 0 || sezione_INDICE >= sezione_CONTA_NUMERI() || 임시공간.length < sezione_ridimensionare) {
            throw new IllegalArgumentException("ATA sezione_VALORE 범위가 올바르지 않습니다.");
        }
    }
}

