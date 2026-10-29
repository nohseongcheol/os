// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Finland.JFinOS.Minne_område;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 justera_värde allokera_minne, släppa_minne, 병합을 담당한다. */
public final class Minne_Ansvarig {
    private final byte[] Minne_område;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Minne_Ansvarig(int summa_storlek) {
        if (summa_storlek < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Minne_område = new byte[summa_storlek];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(summa_storlek - 4096));
    }

    public synchronized int allokera_minne(int Storlek) {
        return 정렬할당(Storlek, 1);
    }

    public synchronized int 정렬할당(int Storlek, int justera_värde) {
        if (Storlek <= 0 || justera_värde <= 0 || (justera_värde & (justera_värde - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> post_värde : 빈영역.entrySet()) {
            int Kör = post_värde.getKey().intValue();
            int område_storlek = post_värde.getValue().intValue();
            int 정렬시작 = (Kör + justera_värde - 1) & -justera_värde;
            int framåtvänd_värde_storlek = 정렬시작 - Kör;
            int 끝크기 = område_storlek - framåtvänd_värde_storlek - Storlek;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Kör));
            if (framåtvänd_värde_storlek > 0) {
                빈영역.put(Integer.valueOf(Kör), Integer.valueOf(framåtvänd_värde_storlek));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Storlek), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Storlek));
            Arrays.fill(Minne_område, 정렬시작, 정렬시작 + Storlek, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void släppa_minne(int Adress) {
        Integer storlek_objekt = 사용영역.remove(Integer.valueOf(Adress));
        if (storlek_objekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Kör = Adress;
        int Storlek = storlek_objekt.intValue();
        Map.Entry<Integer, Integer> framåtvänd_värde = 빈영역.lowerEntry(Integer.valueOf(Kör));
        if (framåtvänd_värde != null && framåtvänd_värde.getKey().intValue() + framåtvänd_värde.getValue().intValue() == Kör) {
            Kör = framåtvänd_värde.getKey().intValue();
            Storlek += framåtvänd_värde.getValue().intValue();
            빈영역.remove(framåtvänd_värde.getKey());
        }
        Map.Entry<Integer, Integer> BACK_värde = 빈영역.ceilingEntry(Integer.valueOf(Kör));
        if (BACK_värde != null && Kör + Storlek == BACK_värde.getKey().intValue()) {
            Storlek += BACK_värde.getValue().intValue();
            빈영역.remove(BACK_värde.getKey());
        }
        빈영역.put(Integer.valueOf(Kör), Integer.valueOf(Storlek));
    }

    public synchronized byte läsa_byte_värde(int Adress) {
        check_område(Adress, 1);
        return Minne_område[Adress];
    }

    public synchronized void skriva_byte_värde(int Adress, byte värde) {
        check_område(Adress, 1);
        Minne_område[Adress] = värde;
    }

    public synchronized int summa_storlek() {
        return Minne_område.length;
    }

    public synchronized int 사용크기() {
        int summa_värde = 0;
        for (Integer Storlek : 사용영역.values()) {
            summa_värde += Storlek.intValue();
        }
        return summa_värde;
    }

    private void check_område(int Adress, int Storlek) {
        if (Adress < 0 || Storlek < 0 || Adress > Minne_område.length - Storlek) {
            throw new IndexOutOfBoundsException("Minne_område 범위를 벗어났습니다.");
        }
    }
}

