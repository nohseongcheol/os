// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.ଷ୍ଟୋରେଜ୍_ଡିଭାଇସ;

import java.util.Arrays;

/** ATA 28비트 ନିର୍ଦ୍ଦେଶ 계층과 같은 512바이트 논리 ବିଭାଗ_ମୂଲ୍ୟ 장치다. */
public final class 고급기술결합장치 {
    public static final int ବିଭାଗ_ଅକାର = 512;
    private final byte[] ଡାଟା;
    private final boolean ରିଡ଼୍_ଓନ୍ଲି_ମୂଲ୍ୟ;

    public 고급기술결합장치(int 구역수, boolean ରିଡ଼୍_ଓନ୍ଲି_ମୂଲ୍ୟ) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("ବିଭାଗ_ମୂଲ୍ୟ 수가 올바르지 않습니다.");
        }
        ଡାଟା = new byte[Math.multiplyExact(구역수, ବିଭାଗ_ଅକାର)];
        this.ରିଡ଼୍_ଓନ୍ଲି_ମୂଲ୍ୟ = ରିଡ଼୍_ଓନ୍ଲି_ମୂଲ୍ୟ;
    }

    public int 구역수() {
        return ଡାଟା.length / ବିଭାଗ_ଅକାର;
    }

    public void ପଢନ୍ତୁ(int ବିଭାଗ_ଅନୁକ୍ରମଣିକା, byte[] 받을곳) {
        범위확인(ବିଭାଗ_ଅନୁକ୍ରମଣିକା, 받을곳);
        System.arraycopy(ଡାଟା, ବିଭାଗ_ଅନୁକ୍ରମଣିକା * ବିଭାଗ_ଅକାର, 받을곳, 0, ବିଭାଗ_ଅକାର);
    }

    public void ଲେଖନ୍ତୁ(int ବିଭାଗ_ଅନୁକ୍ରମଣିକା, byte[] 쓸자료) {
        if (ରିଡ଼୍_ଓନ୍ଲି_ମୂଲ୍ୟ) {
            throw new IllegalStateException("ପଢନ୍ତୁ 전용 장치입니다.");
        }
        범위확인(ବିଭାଗ_ଅନୁକ୍ରମଣିକା, 쓸자료);
        System.arraycopy(쓸자료, 0, ଡାଟା, ବିଭାଗ_ଅନୁକ୍ରମଣିକା * ବିଭାଗ_ଅକାର, ବିଭାଗ_ଅକାର);
    }

    public void 지우기() {
        if (ରିଡ଼୍_ଓନ୍ଲି_ମୂଲ୍ୟ) {
            throw new IllegalStateException("ପଢନ୍ତୁ 전용 장치입니다.");
        }
        Arrays.fill(ଡାଟା, (byte) 0);
    }

    private void 범위확인(int ବିଭାଗ_ଅନୁକ୍ରମଣିକା, byte[] 임시공간) {
        if (ବିଭାଗ_ଅନୁକ୍ରମଣିକା < 0 || ବିଭାଗ_ଅନୁକ୍ରମଣିକା >= 구역수() || 임시공간.length < ବିଭାଗ_ଅକାର) {
            throw new IllegalArgumentException("ATA ବିଭାଗ_ମୂଲ୍ୟ 범위가 올바르지 않습니다.");
        }
    }
}

