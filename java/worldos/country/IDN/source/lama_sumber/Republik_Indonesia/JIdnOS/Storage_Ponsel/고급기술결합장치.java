// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Republik_Indonesia.JIdnOS.Storage_Ponsel;

import java.util.Arrays;

/** ATA 28비트 perintah 계층과 같은 512바이트 논리 seksi_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int seksi_ukuran = 512;
    private final byte[] data;
    private final boolean baca_saja_VALUE;

    public 고급기술결합장치(int seksi_COUNT, boolean baca_saja_VALUE) {
        if (seksi_COUNT <= 0) {
            throw new IllegalArgumentException("seksi_VALUE 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(seksi_COUNT, seksi_ukuran)];
        this.baca_saja_VALUE = baca_saja_VALUE;
    }

    public int seksi_COUNT() {
        return data.length / seksi_ukuran;
    }

    public void Baca(int seksi_INDEX, byte[] terima_tujuan) {
        cek_rentang(seksi_INDEX, terima_tujuan);
        System.arraycopy(data, seksi_INDEX * seksi_ukuran, terima_tujuan, 0, seksi_ukuran);
    }

    public void Tulis(int seksi_INDEX, byte[] 쓸자료) {
        if (baca_saja_VALUE) {
            throw new IllegalStateException("Baca 전용 장치입니다.");
        }
        cek_rentang(seksi_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, data, seksi_INDEX * seksi_ukuran, seksi_ukuran);
    }

    public void hapus_entri_c8dbc399() {
        if (baca_saja_VALUE) {
            throw new IllegalStateException("Baca 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void cek_rentang(int seksi_INDEX, byte[] 임시공간) {
        if (seksi_INDEX < 0 || seksi_INDEX >= seksi_COUNT() || 임시공간.length < seksi_ukuran) {
            throw new IllegalArgumentException("ATA seksi_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

