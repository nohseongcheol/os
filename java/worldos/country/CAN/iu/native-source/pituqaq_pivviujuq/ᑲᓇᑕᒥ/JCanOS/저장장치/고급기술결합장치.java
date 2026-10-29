// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.저장장치;

import java.util.Arrays;

/** ATA 28비트 piqujijjut 계층과 같은 512바이트 논리 sukuttia_atuutilik 장치다. */
public final class 고급기술결합장치 {
    public static final int sukuttia_anininga = 512;
    private final byte[] titiqqat;
    private final boolean takugatuinnaq_atuutilik;

    public 고급기술결합장치(int 구역수, boolean takugatuinnaq_atuutilik) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("sukuttia_atuutilik 수가 올바르지 않습니다.");
        }
        titiqqat = new byte[Math.multiplyExact(구역수, sukuttia_anininga)];
        this.takugatuinnaq_atuutilik = takugatuinnaq_atuutilik;
    }

    public int 구역수() {
        return titiqqat.length / sukuttia_anininga;
    }

    public void 읽기(int sukuttia_nalunaiqsimavik, byte[] 받을곳) {
        범위확인(sukuttia_nalunaiqsimavik, 받을곳);
        System.arraycopy(titiqqat, sukuttia_nalunaiqsimavik * sukuttia_anininga, 받을곳, 0, sukuttia_anininga);
    }

    public void titiraq(int sukuttia_nalunaiqsimavik, byte[] 쓸자료) {
        if (takugatuinnaq_atuutilik) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(sukuttia_nalunaiqsimavik, 쓸자료);
        System.arraycopy(쓸자료, 0, titiqqat, sukuttia_nalunaiqsimavik * sukuttia_anininga, sukuttia_anininga);
    }

    public void 지우기() {
        if (takugatuinnaq_atuutilik) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(titiqqat, (byte) 0);
    }

    private void 범위확인(int sukuttia_nalunaiqsimavik, byte[] 임시공간) {
        if (sukuttia_nalunaiqsimavik < 0 || sukuttia_nalunaiqsimavik >= 구역수() || 임시공간.length < sukuttia_anininga) {
            throw new IllegalArgumentException("ATA sukuttia_atuutilik 범위가 올바르지 않습니다.");
        }
    }
}

