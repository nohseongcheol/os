// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.Memori_wilayah;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB halaman_VALUE 연결과 Tulis 시 복사를 제공한다. */
public final class halaman_Manajer {
    public static final int ukuran_halaman = 4096;

    private static final class halaman_VALUE {
        private byte[] data = new byte[ukuran_halaman];
        private int Referensi_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class surel_SPACE {
        private final Map<Integer, halaman_VALUE> halaman_tabel = new HashMap<Integer, halaman_VALUE>();
    }

    public surel_SPACE 새주소공간() {
        return new surel_SPACE();
    }

    public void MAP_halaman(surel_SPACE surel_wilayah, int alamat_maya, boolean 쓰기가능) {
        int INDEX = 쪽번호(alamat_maya);
        halaman_VALUE 새쪽 = new halaman_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        surel_wilayah.halaman_tabel.put(Integer.valueOf(INDEX), 새쪽);
    }

    public surel_SPACE 쓰기시복사복제(surel_SPACE 원본) {
        surel_SPACE 복제본 = new surel_SPACE();
        for (Map.Entry<Integer, halaman_VALUE> entri_VALUE : 원본.halaman_tabel.entrySet()) {
            halaman_VALUE 공유쪽 = entri_VALUE.getValue();
            공유쪽.Referensi_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.halaman_tabel.put(entri_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(surel_SPACE surel_wilayah, int alamat_maya) {
        halaman_VALUE target = FIND_halaman(surel_wilayah, alamat_maya);
        return target.data[Math.floorMod(alamat_maya, ukuran_halaman)];
    }

    public void tulis_byte_VALUE(surel_SPACE surel_wilayah, int alamat_maya, byte VALUE) {
        int INDEX = 쪽번호(alamat_maya);
        halaman_VALUE target = FIND_halaman(surel_wilayah, alamat_maya);
        if (!target.쓰기가능) {
            if (!target.쓰기시복사) {
                throw new IllegalStateException("Baca 전용 쪽입니다.");
            }
            target = Buat_privat_halaman(surel_wilayah, INDEX, target);
        }
        target.data[Math.floorMod(alamat_maya, ukuran_halaman)] = VALUE;
    }

    public void privat_rentang_tulis(surel_SPACE surel_wilayah, int alamat_permulaan, int Ukuran) {
        if (Ukuran < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int mengakhiri_surel = Math.addExact(alamat_permulaan, Ukuran);
        for (int surel = alamat_permulaan; surel < mengakhiri_surel; surel = (쪽번호(surel) + 1) * ukuran_halaman) {
            int INDEX = 쪽번호(surel);
            halaman_VALUE target = FIND_halaman(surel_wilayah, surel);
            if (target.쓰기시복사) {
                Buat_privat_halaman(surel_wilayah, INDEX, target);
            } else {
                target.쓰기가능 = true;
            }
        }
    }

    public void rentang_tulis(surel_SPACE surel_wilayah, int alamat_permulaan, byte[] data) {
        for (int INDEX = 0; INDEX < data.length; INDEX++) {
            tulis_byte_VALUE(surel_wilayah, alamat_permulaan + INDEX, data[INDEX]);
        }
    }

    private halaman_VALUE Buat_privat_halaman(surel_SPACE surel_wilayah, int INDEX, halaman_VALUE 공유쪽) {
        halaman_VALUE privat_halaman = new halaman_VALUE();
        privat_halaman.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        privat_halaman.쓰기가능 = true;
        privat_halaman.쓰기시복사 = false;
        공유쪽.Referensi_COUNT--;
        surel_wilayah.halaman_tabel.put(Integer.valueOf(INDEX), privat_halaman);
        return privat_halaman;
    }

    private halaman_VALUE FIND_halaman(surel_SPACE surel_wilayah, int surel) {
        halaman_VALUE target = surel_wilayah.halaman_tabel.get(Integer.valueOf(쪽번호(surel)));
        if (target == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return target;
    }

    private int 쪽번호(int surel) {
        if (surel < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return surel / ukuran_halaman;
    }
}

