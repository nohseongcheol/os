// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frantzia.JFraOS.biltegi_gailu;

import java.util.Arrays;

/** ATA 28비트 Komandoa 계층과 같은 512바이트 논리 sekzio_balio 장치다. */
public final class 고급기술결합장치 {
    public static final int 구역크기 = 512;
    private final byte[] datuak;
    private final boolean irakurtzeko_soilik_balio;

    public 고급기술결합장치(int sekzio_ZENBATU, boolean irakurtzeko_soilik_balio) {
        if (sekzio_ZENBATU <= 0) {
            throw new IllegalArgumentException("sekzio_balio 수가 올바르지 않습니다.");
        }
        datuak = new byte[Math.multiplyExact(sekzio_ZENBATU, 구역크기)];
        this.irakurtzeko_soilik_balio = irakurtzeko_soilik_balio;
    }

    public int sekzio_ZENBATU() {
        return datuak.length / 구역크기;
    }

    public void Irakurri(int sekzio_INDIZE, byte[] 받을곳) {
        txeke_barruti(sekzio_INDIZE, 받을곳);
        System.arraycopy(datuak, sekzio_INDIZE * 구역크기, 받을곳, 0, 구역크기);
    }

    public void Idatzi(int sekzio_INDIZE, byte[] 쓸자료) {
        if (irakurtzeko_soilik_balio) {
            throw new IllegalStateException("Irakurri 전용 장치입니다.");
        }
        txeke_barruti(sekzio_INDIZE, 쓸자료);
        System.arraycopy(쓸자료, 0, datuak, sekzio_INDIZE * 구역크기, 구역크기);
    }

    public void ezabatu_sarrera() {
        if (irakurtzeko_soilik_balio) {
            throw new IllegalStateException("Irakurri 전용 장치입니다.");
        }
        Arrays.fill(datuak, (byte) 0);
    }

    private void txeke_barruti(int sekzio_INDIZE, byte[] 임시공간) {
        if (sekzio_INDIZE < 0 || sekzio_INDIZE >= sekzio_ZENBATU() || 임시공간.length < 구역크기) {
            throw new IllegalArgumentException("ATA sekzio_balio 범위가 올바르지 않습니다.");
        }
    }
}

