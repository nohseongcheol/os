// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Regno_Unito.JGbrOS.Memoria_area;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 allineare_VALORE allocare_Memoria, release_Memoria, 병합을 담당한다. */
public final class Memoria_manager {
    private final byte[] Memoria_area;
    private final TreeMap<Integer, Integer> vuota_area = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memoria_manager(int totale_ridimensionare) {
        if (totale_ridimensionare < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Memoria_area = new byte[totale_ridimensionare];
        vuota_area.put(Integer.valueOf(4096), Integer.valueOf(totale_ridimensionare - 4096));
    }

    public synchronized int allocare_Memoria(int Dimensione) {
        return 정렬할당(Dimensione, 1);
    }

    public synchronized int 정렬할당(int Dimensione, int allineare_VALORE) {
        if (Dimensione <= 0 || allineare_VALORE <= 0 || (allineare_VALORE & (allineare_VALORE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> voce_VALORE : vuota_area.entrySet()) {
            int avvia = voce_VALORE.getKey().intValue();
            int area_ridimensionare = voce_VALORE.getValue().intValue();
            int 정렬시작 = (avvia + allineare_VALORE - 1) & -allineare_VALORE;
            int frontale_VALORE_ridimensionare = 정렬시작 - avvia;
            int 끝크기 = area_ridimensionare - frontale_VALORE_ridimensionare - Dimensione;
            if (끝크기 < 0) {
                continue;
            }
            vuota_area.remove(Integer.valueOf(avvia));
            if (frontale_VALORE_ridimensionare > 0) {
                vuota_area.put(Integer.valueOf(avvia), Integer.valueOf(frontale_VALORE_ridimensionare));
            }
            if (끝크기 > 0) {
                vuota_area.put(Integer.valueOf(정렬시작 + Dimensione), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Dimensione));
            Arrays.fill(Memoria_area, 정렬시작, 정렬시작 + Dimensione, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void release_Memoria(int e_mail) {
        Integer ridimensionare_oggetto = 사용영역.remove(Integer.valueOf(e_mail));
        if (ridimensionare_oggetto == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int avvia = e_mail;
        int Dimensione = ridimensionare_oggetto.intValue();
        Map.Entry<Integer, Integer> frontale_VALORE = vuota_area.lowerEntry(Integer.valueOf(avvia));
        if (frontale_VALORE != null && frontale_VALORE.getKey().intValue() + frontale_VALORE.getValue().intValue() == avvia) {
            avvia = frontale_VALORE.getKey().intValue();
            Dimensione += frontale_VALORE.getValue().intValue();
            vuota_area.remove(frontale_VALORE.getKey());
        }
        Map.Entry<Integer, Integer> BACK_VALORE = vuota_area.ceilingEntry(Integer.valueOf(avvia));
        if (BACK_VALORE != null && avvia + Dimensione == BACK_VALORE.getKey().intValue()) {
            Dimensione += BACK_VALORE.getValue().intValue();
            vuota_area.remove(BACK_VALORE.getKey());
        }
        vuota_area.put(Integer.valueOf(avvia), Integer.valueOf(Dimensione));
    }

    public synchronized byte 바이트읽기(int e_mail) {
        assegno_intervallo(e_mail, 1);
        return Memoria_area[e_mail];
    }

    public synchronized void scrivere_byte_VALORE(int e_mail, byte VALORE) {
        assegno_intervallo(e_mail, 1);
        Memoria_area[e_mail] = VALORE;
    }

    public synchronized int totale_ridimensionare() {
        return Memoria_area.length;
    }

    public synchronized int 사용크기() {
        int totale_VALORE = 0;
        for (Integer Dimensione : 사용영역.values()) {
            totale_VALORE += Dimensione.intValue();
        }
        return totale_VALORE;
    }

    private void assegno_intervallo(int e_mail, int Dimensione) {
        if (e_mail < 0 || Dimensione < 0 || e_mail > Memoria_area.length - Dimensione) {
            throw new IndexOutOfBoundsException("Memoria_area 범위를 벗어났습니다.");
        }
    }
}

