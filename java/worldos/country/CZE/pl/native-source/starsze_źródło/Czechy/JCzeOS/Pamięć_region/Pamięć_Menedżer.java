// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Czechy.JCzeOS.Pamięć_region;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 wyrównać_WARTOŚĆ przydzielić_Pamięć, wersja_Pamięć, 병합을 담당한다. */
public final class Pamięć_Menedżer {
    private final byte[] Pamięć_region;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Pamięć_Menedżer(int suma_zmienić_rozmiar) {
        if (suma_zmienić_rozmiar < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Pamięć_region = new byte[suma_zmienić_rozmiar];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(suma_zmienić_rozmiar - 4096));
    }

    public synchronized int przydzielić_Pamięć(int Rozmiar) {
        return 정렬할당(Rozmiar, 1);
    }

    public synchronized int 정렬할당(int Rozmiar, int wyrównać_WARTOŚĆ) {
        if (Rozmiar <= 0 || wyrównać_WARTOŚĆ <= 0 || (wyrównać_WARTOŚĆ & (wyrównać_WARTOŚĆ - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> wpis_WARTOŚĆ : 빈영역.entrySet()) {
            int Uruchom_2 = wpis_WARTOŚĆ.getKey().intValue();
            int region_zmienić_rozmiar = wpis_WARTOŚĆ.getValue().intValue();
            int 정렬시작 = (Uruchom_2 + wyrównać_WARTOŚĆ - 1) & -wyrównać_WARTOŚĆ;
            int przód_WARTOŚĆ_zmienić_rozmiar = 정렬시작 - Uruchom_2;
            int 끝크기 = region_zmienić_rozmiar - przód_WARTOŚĆ_zmienić_rozmiar - Rozmiar;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Uruchom_2));
            if (przód_WARTOŚĆ_zmienić_rozmiar > 0) {
                빈영역.put(Integer.valueOf(Uruchom_2), Integer.valueOf(przód_WARTOŚĆ_zmienić_rozmiar));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Rozmiar), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Rozmiar));
            Arrays.fill(Pamięć_region, 정렬시작, 정렬시작 + Rozmiar, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void wersja_Pamięć(int Adres) {
        Integer zmienić_rozmiar_obiekt = 사용영역.remove(Integer.valueOf(Adres));
        if (zmienić_rozmiar_obiekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Uruchom_2 = Adres;
        int Rozmiar = zmienić_rozmiar_obiekt.intValue();
        Map.Entry<Integer, Integer> przód_WARTOŚĆ = 빈영역.lowerEntry(Integer.valueOf(Uruchom_2));
        if (przód_WARTOŚĆ != null && przód_WARTOŚĆ.getKey().intValue() + przód_WARTOŚĆ.getValue().intValue() == Uruchom_2) {
            Uruchom_2 = przód_WARTOŚĆ.getKey().intValue();
            Rozmiar += przód_WARTOŚĆ.getValue().intValue();
            빈영역.remove(przód_WARTOŚĆ.getKey());
        }
        Map.Entry<Integer, Integer> BACK_WARTOŚĆ = 빈영역.ceilingEntry(Integer.valueOf(Uruchom_2));
        if (BACK_WARTOŚĆ != null && Uruchom_2 + Rozmiar == BACK_WARTOŚĆ.getKey().intValue()) {
            Rozmiar += BACK_WARTOŚĆ.getValue().intValue();
            빈영역.remove(BACK_WARTOŚĆ.getKey());
        }
        빈영역.put(Integer.valueOf(Uruchom_2), Integer.valueOf(Rozmiar));
    }

    public synchronized byte 바이트읽기(int Adres) {
        czek_zakres(Adres, 1);
        return Pamięć_region[Adres];
    }

    public synchronized void zapis_bajt_WARTOŚĆ(int Adres, byte WARTOŚĆ) {
        czek_zakres(Adres, 1);
        Pamięć_region[Adres] = WARTOŚĆ;
    }

    public synchronized int suma_zmienić_rozmiar() {
        return Pamięć_region.length;
    }

    public synchronized int 사용크기() {
        int suma_WARTOŚĆ = 0;
        for (Integer Rozmiar : 사용영역.values()) {
            suma_WARTOŚĆ += Rozmiar.intValue();
        }
        return suma_WARTOŚĆ;
    }

    private void czek_zakres(int Adres, int Rozmiar) {
        if (Adres < 0 || Rozmiar < 0 || Adres > Pamięć_region.length - Rozmiar) {
            throw new IndexOutOfBoundsException("Pamięć_region 범위를 벗어났습니다.");
        }
    }
}

