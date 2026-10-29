// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package iLesotho.JLsoOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 qondisa_inani abela_Indawo_yokugcina, khulula_Indawo_yokugcina, 병합을 담당한다. */
public final class inkumbulo_imeneja {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public inkumbulo_imeneja(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int abela_Indawo_yokugcina(int Ubungako) {
        return 정렬할당(Ubungako, 1);
    }

    public synchronized int 정렬할당(int Ubungako, int qondisa_inani) {
        if (Ubungako <= 0 || qondisa_inani <= 0 || (qondisa_inani & (qondisa_inani - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> okufakwayo_inani : 빈영역.entrySet()) {
            int Sebenzisa = okufakwayo_inani.getKey().intValue();
            int 영역크기 = okufakwayo_inani.getValue().intValue();
            int 정렬시작 = (Sebenzisa + qondisa_inani - 1) & -qondisa_inani;
            int 앞크기 = 정렬시작 - Sebenzisa;
            int 끝크기 = 영역크기 - 앞크기 - Ubungako;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Sebenzisa));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Sebenzisa), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Ubungako), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Ubungako));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Ubungako, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void khulula_Indawo_yokugcina(int ikheli) {
        Integer linganisa_into = 사용영역.remove(Integer.valueOf(ikheli));
        if (linganisa_into == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Sebenzisa = ikheli;
        int Ubungako = linganisa_into.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Sebenzisa));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Sebenzisa) {
            Sebenzisa = 앞.getKey().intValue();
            Ubungako += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Impindamuva_inani = 빈영역.ceilingEntry(Integer.valueOf(Sebenzisa));
        if (Impindamuva_inani != null && Sebenzisa + Ubungako == Impindamuva_inani.getKey().intValue()) {
            Ubungako += Impindamuva_inani.getValue().intValue();
            빈영역.remove(Impindamuva_inani.getKey());
        }
        빈영역.put(Integer.valueOf(Sebenzisa), Integer.valueOf(Ubungako));
    }

    public synchronized byte 바이트읽기(int ikheli) {
        범위확인(ikheli, 1);
        return 기억공간[ikheli];
    }

    public synchronized void bhala_ibhayithi_inani(int ikheli, byte inani) {
        범위확인(ikheli, 1);
        기억공간[ikheli] = inani;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Ubungako : 사용영역.values()) {
            합계 += Ubungako.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ikheli, int Ubungako) {
        if (ikheli < 0 || Ubungako < 0 || ikheli > 기억공간.length - Ubungako) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

