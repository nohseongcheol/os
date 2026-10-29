// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package საქართველო.JGeoOS.საცავი_მობილური;

import java.util.Arrays;

/** ATA 28비트 ბრძანება 계층과 같은 512바이트 논리 სექცია_მნიშვნელობა 장치다. */
public final class 고급기술결합장치 {
    public static final int სექცია_ზომის_შეცვლა = 512;
    private final byte[] მონაცემები;
    private final boolean მხოლოდ_კითხვადი_მნიშვნელობა;

    public 고급기술결합장치(int 구역수, boolean მხოლოდ_კითხვადი_მნიშვნელობა) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("სექცია_მნიშვნელობა 수가 올바르지 않습니다.");
        }
        მონაცემები = new byte[Math.multiplyExact(구역수, სექცია_ზომის_შეცვლა)];
        this.მხოლოდ_კითხვადი_მნიშვნელობა = მხოლოდ_კითხვადი_მნიშვნელობა;
    }

    public int 구역수() {
        return მონაცემები.length / სექცია_ზომის_შეცვლა;
    }

    public void კითხვა(int სექცია_ინდექსი, byte[] 받을곳) {
        범위확인(სექცია_ინდექსი, 받을곳);
        System.arraycopy(მონაცემები, სექცია_ინდექსი * სექცია_ზომის_შეცვლა, 받을곳, 0, სექცია_ზომის_შეცვლა);
    }

    public void ჩაწერა(int სექცია_ინდექსი, byte[] 쓸자료) {
        if (მხოლოდ_კითხვადი_მნიშვნელობა) {
            throw new IllegalStateException("კითხვა 전용 장치입니다.");
        }
        범위확인(სექცია_ინდექსი, 쓸자료);
        System.arraycopy(쓸자료, 0, მონაცემები, სექცია_ინდექსი * სექცია_ზომის_შეცვლა, სექცია_ზომის_შეცვლა);
    }

    public void 지우기() {
        if (მხოლოდ_კითხვადი_მნიშვნელობა) {
            throw new IllegalStateException("კითხვა 전용 장치입니다.");
        }
        Arrays.fill(მონაცემები, (byte) 0);
    }

    private void 범위확인(int სექცია_ინდექსი, byte[] 임시공간) {
        if (სექცია_ინდექსი < 0 || სექცია_ინდექსი >= 구역수() || 임시공간.length < სექცია_ზომის_შეცვლა) {
            throw new IllegalArgumentException("ATA სექცია_მნიშვნელობა 범위가 올바르지 않습니다.");
        }
    }
}

