// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Republica_Moldova.JMdaOS.Memorie_regiune;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 alinia_VALUE aloca_Stocare, lansa_Stocare, 병합을 담당한다. */
public final class 기억공간관리자 {
    private final byte[] Memorie_regiune;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public 기억공간관리자(int total_dimensiona) {
        if (total_dimensiona < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Memorie_regiune = new byte[total_dimensiona];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(total_dimensiona - 4096));
    }

    public synchronized int aloca_Stocare(int Mărime) {
        return 정렬할당(Mărime, 1);
    }

    public synchronized int 정렬할당(int Mărime, int alinia_VALUE) {
        if (Mărime <= 0 || alinia_VALUE <= 0 || (alinia_VALUE & (alinia_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> intrare_VALUE : 빈영역.entrySet()) {
            int Pornește = intrare_VALUE.getKey().intValue();
            int regiune_dimensiona = intrare_VALUE.getValue().intValue();
            int 정렬시작 = (Pornește + alinia_VALUE - 1) & -alinia_VALUE;
            int frontală_VALUE_dimensiona = 정렬시작 - Pornește;
            int 끝크기 = regiune_dimensiona - frontală_VALUE_dimensiona - Mărime;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Pornește));
            if (frontală_VALUE_dimensiona > 0) {
                빈영역.put(Integer.valueOf(Pornește), Integer.valueOf(frontală_VALUE_dimensiona));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Mărime), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Mărime));
            Arrays.fill(Memorie_regiune, 정렬시작, 정렬시작 + Mărime, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void lansa_Stocare(int adresa) {
        Integer dimensiona_obiect = 사용영역.remove(Integer.valueOf(adresa));
        if (dimensiona_obiect == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Pornește = adresa;
        int Mărime = dimensiona_obiect.intValue();
        Map.Entry<Integer, Integer> frontală_VALUE = 빈영역.lowerEntry(Integer.valueOf(Pornește));
        if (frontală_VALUE != null && frontală_VALUE.getKey().intValue() + frontală_VALUE.getValue().intValue() == Pornește) {
            Pornește = frontală_VALUE.getKey().intValue();
            Mărime += frontală_VALUE.getValue().intValue();
            빈영역.remove(frontală_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> ÎNAPOI_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Pornește));
        if (ÎNAPOI_VALUE != null && Pornește + Mărime == ÎNAPOI_VALUE.getKey().intValue()) {
            Mărime += ÎNAPOI_VALUE.getValue().intValue();
            빈영역.remove(ÎNAPOI_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Pornește), Integer.valueOf(Mărime));
    }

    public synchronized byte 바이트읽기(int adresa) {
        verifica_zonă(adresa, 1);
        return Memorie_regiune[adresa];
    }

    public synchronized void scriere_byte_VALUE(int adresa, byte VALUE) {
        verifica_zonă(adresa, 1);
        Memorie_regiune[adresa] = VALUE;
    }

    public synchronized int total_dimensiona() {
        return Memorie_regiune.length;
    }

    public synchronized int 사용크기() {
        int total_VALUE = 0;
        for (Integer Mărime : 사용영역.values()) {
            total_VALUE += Mărime.intValue();
        }
        return total_VALUE;
    }

    private void verifica_zonă(int adresa, int Mărime) {
        if (adresa < 0 || Mărime < 0 || adresa > Memorie_regiune.length - Mărime) {
            throw new IndexOutOfBoundsException("Memorie_regiune 범위를 벗어났습니다.");
        }
    }
}

