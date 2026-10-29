// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Venäjä.JRusOS.Muisti_alue;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 tasaa_ARVO jakaa_Tallennus, julkaista_Tallennus, 병합을 담당한다. */
public final class Muisti_Valvoja {
    private final byte[] Muisti_alue;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Muisti_Valvoja(int summa_muuttaa_kokoa) {
        if (summa_muuttaa_kokoa < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Muisti_alue = new byte[summa_muuttaa_kokoa];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(summa_muuttaa_kokoa - 4096));
    }

    public synchronized int jakaa_Tallennus(int Koko) {
        return 정렬할당(Koko, 1);
    }

    public synchronized int 정렬할당(int Koko, int tasaa_ARVO) {
        if (Koko <= 0 || tasaa_ARVO <= 0 || (tasaa_ARVO & (tasaa_ARVO - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> merkintä_ARVO_962f286b : 빈영역.entrySet()) {
            int Suorita_2 = merkintä_ARVO_962f286b.getKey().intValue();
            int alue_muuttaa_kokoa = merkintä_ARVO_962f286b.getValue().intValue();
            int 정렬시작 = (Suorita_2 + tasaa_ARVO - 1) & -tasaa_ARVO;
            int etukamera_ARVO_muuttaa_kokoa = 정렬시작 - Suorita_2;
            int 끝크기 = alue_muuttaa_kokoa - etukamera_ARVO_muuttaa_kokoa - Koko;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Suorita_2));
            if (etukamera_ARVO_muuttaa_kokoa > 0) {
                빈영역.put(Integer.valueOf(Suorita_2), Integer.valueOf(etukamera_ARVO_muuttaa_kokoa));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Koko), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Koko));
            Arrays.fill(Muisti_alue, 정렬시작, 정렬시작 + Koko, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void julkaista_Tallennus(int OSOITE) {
        Integer muuttaa_kokoa_objekti = 사용영역.remove(Integer.valueOf(OSOITE));
        if (muuttaa_kokoa_objekti == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Suorita_2 = OSOITE;
        int Koko = muuttaa_kokoa_objekti.intValue();
        Map.Entry<Integer, Integer> etukamera_ARVO = 빈영역.lowerEntry(Integer.valueOf(Suorita_2));
        if (etukamera_ARVO != null && etukamera_ARVO.getKey().intValue() + etukamera_ARVO.getValue().intValue() == Suorita_2) {
            Suorita_2 = etukamera_ARVO.getKey().intValue();
            Koko += etukamera_ARVO.getValue().intValue();
            빈영역.remove(etukamera_ARVO.getKey());
        }
        Map.Entry<Integer, Integer> BACK_ARVO = 빈영역.ceilingEntry(Integer.valueOf(Suorita_2));
        if (BACK_ARVO != null && Suorita_2 + Koko == BACK_ARVO.getKey().intValue()) {
            Koko += BACK_ARVO.getValue().intValue();
            빈영역.remove(BACK_ARVO.getKey());
        }
        빈영역.put(Integer.valueOf(Suorita_2), Integer.valueOf(Koko));
    }

    public synchronized byte lukea_tavu_ARVO(int OSOITE) {
        sekki_alue(OSOITE, 1);
        return Muisti_alue[OSOITE];
    }

    public synchronized void kirjoitus_tavu_ARVO(int OSOITE, byte ARVO) {
        sekki_alue(OSOITE, 1);
        Muisti_alue[OSOITE] = ARVO;
    }

    public synchronized int summa_muuttaa_kokoa() {
        return Muisti_alue.length;
    }

    public synchronized int 사용크기() {
        int summa_ARVO = 0;
        for (Integer Koko : 사용영역.values()) {
            summa_ARVO += Koko.intValue();
        }
        return summa_ARVO;
    }

    private void sekki_alue(int OSOITE, int Koko) {
        if (OSOITE < 0 || Koko < 0 || OSOITE > Muisti_alue.length - Koko) {
            throw new IndexOutOfBoundsException("Muisti_alue 범위를 벗어났습니다.");
        }
    }
}

