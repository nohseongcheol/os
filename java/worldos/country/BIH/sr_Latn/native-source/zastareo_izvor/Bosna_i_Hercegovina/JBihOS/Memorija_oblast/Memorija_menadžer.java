// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.Memorija_oblast;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 poravnati_VALUE dodeliti_Skladište, izdanje_Skladište, 병합을 담당한다. */
public final class Memorija_menadžer {
    private final byte[] Memorija_oblast;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memorija_menadžer(int ukupan_promeniti_veličinu) {
        if (ukupan_promeniti_veličinu < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Memorija_oblast = new byte[ukupan_promeniti_veličinu];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(ukupan_promeniti_veličinu - 4096));
    }

    public synchronized int dodeliti_Skladište(int promeniti_veličinu) {
        return 정렬할당(promeniti_veličinu, 1);
    }

    public synchronized int 정렬할당(int promeniti_veličinu, int poravnati_VALUE) {
        if (promeniti_veličinu <= 0 || poravnati_VALUE <= 0 || (poravnati_VALUE & (poravnati_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> stavka_VALUE : 빈영역.entrySet()) {
            int koristiti = stavka_VALUE.getKey().intValue();
            int oblast_promeniti_veličinu = stavka_VALUE.getValue().intValue();
            int 정렬시작 = (koristiti + poravnati_VALUE - 1) & -poravnati_VALUE;
            int čeona_kamera_VALUE_promeniti_veličinu = 정렬시작 - koristiti;
            int 끝크기 = oblast_promeniti_veličinu - čeona_kamera_VALUE_promeniti_veličinu - promeniti_veličinu;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(koristiti));
            if (čeona_kamera_VALUE_promeniti_veličinu > 0) {
                빈영역.put(Integer.valueOf(koristiti), Integer.valueOf(čeona_kamera_VALUE_promeniti_veličinu));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + promeniti_veličinu), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(promeniti_veličinu));
            Arrays.fill(Memorija_oblast, 정렬시작, 정렬시작 + promeniti_veličinu, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void izdanje_Skladište(int adresa) {
        Integer promeniti_veličinu_objekat = 사용영역.remove(Integer.valueOf(adresa));
        if (promeniti_veličinu_objekat == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int koristiti = adresa;
        int promeniti_veličinu = promeniti_veličinu_objekat.intValue();
        Map.Entry<Integer, Integer> čeona_kamera_VALUE = 빈영역.lowerEntry(Integer.valueOf(koristiti));
        if (čeona_kamera_VALUE != null && čeona_kamera_VALUE.getKey().intValue() + čeona_kamera_VALUE.getValue().intValue() == koristiti) {
            koristiti = čeona_kamera_VALUE.getKey().intValue();
            promeniti_veličinu += čeona_kamera_VALUE.getValue().intValue();
            빈영역.remove(čeona_kamera_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> NAZAD_VALUE = 빈영역.ceilingEntry(Integer.valueOf(koristiti));
        if (NAZAD_VALUE != null && koristiti + promeniti_veličinu == NAZAD_VALUE.getKey().intValue()) {
            promeniti_veličinu += NAZAD_VALUE.getValue().intValue();
            빈영역.remove(NAZAD_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(koristiti), Integer.valueOf(promeniti_veličinu));
    }

    public synchronized byte 바이트읽기(int adresa) {
        proveriti_opseg(adresa, 1);
        return Memorija_oblast[adresa];
    }

    public synchronized void 바이트쓰기(int adresa, byte VALUE) {
        proveriti_opseg(adresa, 1);
        Memorija_oblast[adresa] = VALUE;
    }

    public synchronized int ukupan_promeniti_veličinu() {
        return Memorija_oblast.length;
    }

    public synchronized int 사용크기() {
        int ukupan_VALUE = 0;
        for (Integer promeniti_veličinu : 사용영역.values()) {
            ukupan_VALUE += promeniti_veličinu.intValue();
        }
        return ukupan_VALUE;
    }

    private void proveriti_opseg(int adresa, int promeniti_veličinu) {
        if (adresa < 0 || promeniti_veličinu < 0 || adresa > Memorija_oblast.length - promeniti_veličinu) {
            throw new IndexOutOfBoundsException("Memorija_oblast 범위를 벗어났습니다.");
        }
    }
}

