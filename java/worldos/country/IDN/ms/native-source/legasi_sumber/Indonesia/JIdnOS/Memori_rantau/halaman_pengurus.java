// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.JIdnOS.Memori_rantau;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB halaman_VALUE 연결과 Tulis 시 복사를 제공한다. */
public final class halaman_pengurus {
    public static final int saiz_halaman = 4096;

    private static final class halaman_VALUE {
        private byte[] data = new byte[saiz_halaman];
        private int Rujukan_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean COW;
    }

    public static final class e_mel_SPACE {
        private final Map<Integer, halaman_VALUE> halaman_jadual = new HashMap<Integer, halaman_VALUE>();
    }

    public e_mel_SPACE 새주소공간() {
        return new e_mel_SPACE();
    }

    public void MAP_halaman(e_mel_SPACE e_mel_rantau, int alamat_maya, boolean 쓰기가능) {
        int INDEX = 쪽번호(alamat_maya);
        halaman_VALUE 새쪽 = new halaman_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        e_mel_rantau.halaman_jadual.put(Integer.valueOf(INDEX), 새쪽);
    }

    public e_mel_SPACE klon_COW(e_mel_SPACE 원본) {
        e_mel_SPACE 복제본 = new e_mel_SPACE();
        for (Map.Entry<Integer, halaman_VALUE> pemasukan_VALUE : 원본.halaman_jadual.entrySet()) {
            halaman_VALUE 공유쪽 = pemasukan_VALUE.getValue();
            공유쪽.Rujukan_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.COW = true;
            }
            복제본.halaman_jadual.put(pemasukan_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(e_mel_SPACE e_mel_rantau, int alamat_maya) {
        halaman_VALUE sasaran = Cari_halaman(e_mel_rantau, alamat_maya);
        return sasaran.data[Math.floorMod(alamat_maya, saiz_halaman)];
    }

    public void tulis_bait_VALUE(e_mel_SPACE e_mel_rantau, int alamat_maya, byte VALUE) {
        int INDEX = 쪽번호(alamat_maya);
        halaman_VALUE sasaran = Cari_halaman(e_mel_rantau, alamat_maya);
        if (!sasaran.쓰기가능) {
            if (!sasaran.COW) {
                throw new IllegalStateException("Baca 전용 쪽입니다.");
            }
            sasaran = cipta_Peribadi_halaman(e_mel_rantau, INDEX, sasaran);
        }
        sasaran.data[Math.floorMod(alamat_maya, saiz_halaman)] = VALUE;
    }

    public void Peribadi_julat_tulis(e_mel_SPACE e_mel_rantau, int alamat_mula, int Saiz) {
        if (Saiz < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int tamat_e_mel = Math.addExact(alamat_mula, Saiz);
        for (int e_mel = alamat_mula; e_mel < tamat_e_mel; e_mel = (쪽번호(e_mel) + 1) * saiz_halaman) {
            int INDEX = 쪽번호(e_mel);
            halaman_VALUE sasaran = Cari_halaman(e_mel_rantau, e_mel);
            if (sasaran.COW) {
                cipta_Peribadi_halaman(e_mel_rantau, INDEX, sasaran);
            } else {
                sasaran.쓰기가능 = true;
            }
        }
    }

    public void julat_tulis(e_mel_SPACE e_mel_rantau, int alamat_mula, byte[] data) {
        for (int INDEX = 0; INDEX < data.length; INDEX++) {
            tulis_bait_VALUE(e_mel_rantau, alamat_mula + INDEX, data[INDEX]);
        }
    }

    private halaman_VALUE cipta_Peribadi_halaman(e_mel_SPACE e_mel_rantau, int INDEX, halaman_VALUE 공유쪽) {
        halaman_VALUE Peribadi_halaman = new halaman_VALUE();
        Peribadi_halaman.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        Peribadi_halaman.쓰기가능 = true;
        Peribadi_halaman.COW = false;
        공유쪽.Rujukan_COUNT--;
        e_mel_rantau.halaman_jadual.put(Integer.valueOf(INDEX), Peribadi_halaman);
        return Peribadi_halaman;
    }

    private halaman_VALUE Cari_halaman(e_mel_SPACE e_mel_rantau, int e_mel) {
        halaman_VALUE sasaran = e_mel_rantau.halaman_jadual.get(Integer.valueOf(쪽번호(e_mel)));
        if (sasaran == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return sasaran;
    }

    private int 쪽번호(int e_mel) {
        if (e_mel < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return e_mel / saiz_halaman;
    }
}

