// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.Memori_wilayah;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 ratakan_VALUE alokasi_Storage, lepas_Storage, 병합을 담당한다. */
public final class Memori_Manajer {
    private final byte[] Memori_wilayah;
    private final TreeMap<Integer, Integer> kosong_wilayah = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memori_Manajer(int total_ukuran) {
        if (total_ukuran < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Memori_wilayah = new byte[total_ukuran];
        kosong_wilayah.put(Integer.valueOf(4096), Integer.valueOf(total_ukuran - 4096));
    }

    public synchronized int alokasi_Storage(int Ukuran) {
        return 정렬할당(Ukuran, 1);
    }

    public synchronized int 정렬할당(int Ukuran, int ratakan_VALUE) {
        if (Ukuran <= 0 || ratakan_VALUE <= 0 || (ratakan_VALUE & (ratakan_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> entri_VALUE : kosong_wilayah.entrySet()) {
            int jalankan = entri_VALUE.getKey().intValue();
            int wilayah_ukuran = entri_VALUE.getValue().intValue();
            int 정렬시작 = (jalankan + ratakan_VALUE - 1) & -ratakan_VALUE;
            int depan_VALUE_ukuran = 정렬시작 - jalankan;
            int 끝크기 = wilayah_ukuran - depan_VALUE_ukuran - Ukuran;
            if (끝크기 < 0) {
                continue;
            }
            kosong_wilayah.remove(Integer.valueOf(jalankan));
            if (depan_VALUE_ukuran > 0) {
                kosong_wilayah.put(Integer.valueOf(jalankan), Integer.valueOf(depan_VALUE_ukuran));
            }
            if (끝크기 > 0) {
                kosong_wilayah.put(Integer.valueOf(정렬시작 + Ukuran), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Ukuran));
            Arrays.fill(Memori_wilayah, 정렬시작, 정렬시작 + Ukuran, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void lepas_Storage(int surel) {
        Integer ukuran_objek = 사용영역.remove(Integer.valueOf(surel));
        if (ukuran_objek == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int jalankan = surel;
        int Ukuran = ukuran_objek.intValue();
        Map.Entry<Integer, Integer> depan_VALUE = kosong_wilayah.lowerEntry(Integer.valueOf(jalankan));
        if (depan_VALUE != null && depan_VALUE.getKey().intValue() + depan_VALUE.getValue().intValue() == jalankan) {
            jalankan = depan_VALUE.getKey().intValue();
            Ukuran += depan_VALUE.getValue().intValue();
            kosong_wilayah.remove(depan_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> BACK_VALUE = kosong_wilayah.ceilingEntry(Integer.valueOf(jalankan));
        if (BACK_VALUE != null && jalankan + Ukuran == BACK_VALUE.getKey().intValue()) {
            Ukuran += BACK_VALUE.getValue().intValue();
            kosong_wilayah.remove(BACK_VALUE.getKey());
        }
        kosong_wilayah.put(Integer.valueOf(jalankan), Integer.valueOf(Ukuran));
    }

    public synchronized byte 바이트읽기(int surel) {
        cek_rentang(surel, 1);
        return Memori_wilayah[surel];
    }

    public synchronized void tulis_byte_VALUE(int surel, byte VALUE) {
        cek_rentang(surel, 1);
        Memori_wilayah[surel] = VALUE;
    }

    public synchronized int total_ukuran() {
        return Memori_wilayah.length;
    }

    public synchronized int 사용크기() {
        int total_VALUE = 0;
        for (Integer Ukuran : 사용영역.values()) {
            total_VALUE += Ukuran.intValue();
        }
        return total_VALUE;
    }

    private void cek_rentang(int surel, int Ukuran) {
        if (surel < 0 || Ukuran < 0 || surel > Memori_wilayah.length - Ukuran) {
            throw new IndexOutOfBoundsException("Memori_wilayah 범위를 벗어났습니다.");
        }
    }
}

