// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tanzania.JTzaOS.Hifadhi_kifaa;

import java.util.Arrays;

/** ATA 28비트 amri 계층과 같은 512바이트 논리 sehemu_thamani 장치다. */
public final class 고급기술결합장치 {
    public static final int sehemu_panga_ukubwa = 512;
    private final byte[] data;
    private final boolean soma_tu_thamani;

    public 고급기술결합장치(int 구역수, boolean soma_tu_thamani) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("sehemu_thamani 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(구역수, sehemu_panga_ukubwa)];
        this.soma_tu_thamani = soma_tu_thamani;
    }

    public int 구역수() {
        return data.length / sehemu_panga_ukubwa;
    }

    public void 읽기(int sehemu_kielezo, byte[] 받을곳) {
        범위확인(sehemu_kielezo, 받을곳);
        System.arraycopy(data, sehemu_kielezo * sehemu_panga_ukubwa, 받을곳, 0, sehemu_panga_ukubwa);
    }

    public void andika(int sehemu_kielezo, byte[] 쓸자료) {
        if (soma_tu_thamani) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(sehemu_kielezo, 쓸자료);
        System.arraycopy(쓸자료, 0, data, sehemu_kielezo * sehemu_panga_ukubwa, sehemu_panga_ukubwa);
    }

    public void futa_ingizo() {
        if (soma_tu_thamani) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void 범위확인(int sehemu_kielezo, byte[] 임시공간) {
        if (sehemu_kielezo < 0 || sehemu_kielezo >= 구역수() || 임시공간.length < sehemu_panga_ukubwa) {
            throw new IllegalArgumentException("ATA sehemu_thamani 범위가 올바르지 않습니다.");
        }
    }
}

