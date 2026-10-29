// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Singapura.JSgpOS.Memori_rantau;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 jajar_VALUE peruntuk_Storan, keluaran_Storan, 병합을 담당한다. */
public final class Memori_pengurus {
    private final byte[] Memori_rantau;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memori_pengurus(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Memori_rantau = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int peruntuk_Storan(int Saiz) {
        return 정렬할당(Saiz, 1);
    }

    public synchronized int 정렬할당(int Saiz, int jajar_VALUE) {
        if (Saiz <= 0 || jajar_VALUE <= 0 || (jajar_VALUE & (jajar_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> pemasukan_VALUE : 빈영역.entrySet()) {
            int Jalan = pemasukan_VALUE.getKey().intValue();
            int rantau_saiz = pemasukan_VALUE.getValue().intValue();
            int 정렬시작 = (Jalan + jajar_VALUE - 1) & -jajar_VALUE;
            int hadapan_VALUE_saiz = 정렬시작 - Jalan;
            int 끝크기 = rantau_saiz - hadapan_VALUE_saiz - Saiz;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Jalan));
            if (hadapan_VALUE_saiz > 0) {
                빈영역.put(Integer.valueOf(Jalan), Integer.valueOf(hadapan_VALUE_saiz));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Saiz), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Saiz));
            Arrays.fill(Memori_rantau, 정렬시작, 정렬시작 + Saiz, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void keluaran_Storan(int e_mel) {
        Integer saiz_objek = 사용영역.remove(Integer.valueOf(e_mel));
        if (saiz_objek == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Jalan = e_mel;
        int Saiz = saiz_objek.intValue();
        Map.Entry<Integer, Integer> hadapan_VALUE = 빈영역.lowerEntry(Integer.valueOf(Jalan));
        if (hadapan_VALUE != null && hadapan_VALUE.getKey().intValue() + hadapan_VALUE.getValue().intValue() == Jalan) {
            Jalan = hadapan_VALUE.getKey().intValue();
            Saiz += hadapan_VALUE.getValue().intValue();
            빈영역.remove(hadapan_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> BACK_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Jalan));
        if (BACK_VALUE != null && Jalan + Saiz == BACK_VALUE.getKey().intValue()) {
            Saiz += BACK_VALUE.getValue().intValue();
            빈영역.remove(BACK_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Jalan), Integer.valueOf(Saiz));
    }

    public synchronized byte 바이트읽기(int e_mel) {
        cek_julat(e_mel, 1);
        return Memori_rantau[e_mel];
    }

    public synchronized void tulis_bait_VALUE(int e_mel, byte VALUE) {
        cek_julat(e_mel, 1);
        Memori_rantau[e_mel] = VALUE;
    }

    public synchronized int 전체크기() {
        return Memori_rantau.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Saiz : 사용영역.values()) {
            합계 += Saiz.intValue();
        }
        return 합계;
    }

    private void cek_julat(int e_mel, int Saiz) {
        if (e_mel < 0 || Saiz < 0 || e_mel > Memori_rantau.length - Saiz) {
            throw new IndexOutOfBoundsException("Memori_rantau 범위를 벗어났습니다.");
        }
    }
}

