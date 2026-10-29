// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਕੀਨੀਆ.JKenOS.ਸਟੋਰੇਜ_ਤਜਵੀਜ;

import java.util.Arrays;

/** ATA 28비트 ਕਮਾਂਡ 계층과 같은 512바이트 논리 ਵਿਭਾਗ_ਕੀਮਤ 장치다. */
public final class 고급기술결합장치 {
    public static final int ਵਿਭਾਗ_ਆਕਾਰ = 512;
    private final byte[] ਸਮੱਗਰੀ;
    private final boolean ਸਿਰਫ਼_ਪੜ੍ਹੋ_ਕੀਮਤ;

    public 고급기술결합장치(int 구역수, boolean ਸਿਰਫ਼_ਪੜ੍ਹੋ_ਕੀਮਤ) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("ਵਿਭਾਗ_ਕੀਮਤ 수가 올바르지 않습니다.");
        }
        ਸਮੱਗਰੀ = new byte[Math.multiplyExact(구역수, ਵਿਭਾਗ_ਆਕਾਰ)];
        this.ਸਿਰਫ਼_ਪੜ੍ਹੋ_ਕੀਮਤ = ਸਿਰਫ਼_ਪੜ੍ਹੋ_ਕੀਮਤ;
    }

    public int 구역수() {
        return ਸਮੱਗਰੀ.length / ਵਿਭਾਗ_ਆਕਾਰ;
    }

    public void ਪੜ੍ਹਨ(int ਵਿਭਾਗ_ਅਨੁਕ੍ਰਮਣਿਕਾ, byte[] 받을곳) {
        범위확인(ਵਿਭਾਗ_ਅਨੁਕ੍ਰਮਣਿਕਾ, 받을곳);
        System.arraycopy(ਸਮੱਗਰੀ, ਵਿਭਾਗ_ਅਨੁਕ੍ਰਮਣਿਕਾ * ਵਿਭਾਗ_ਆਕਾਰ, 받을곳, 0, ਵਿਭਾਗ_ਆਕਾਰ);
    }

    public void ਲਿਖਣ(int ਵਿਭਾਗ_ਅਨੁਕ੍ਰਮਣਿਕਾ, byte[] 쓸자료) {
        if (ਸਿਰਫ਼_ਪੜ੍ਹੋ_ਕੀਮਤ) {
            throw new IllegalStateException("ਪੜ੍ਹਨ 전용 장치입니다.");
        }
        범위확인(ਵਿਭਾਗ_ਅਨੁਕ੍ਰਮਣਿਕਾ, 쓸자료);
        System.arraycopy(쓸자료, 0, ਸਮੱਗਰੀ, ਵਿਭਾਗ_ਅਨੁਕ੍ਰਮਣਿਕਾ * ਵਿਭਾਗ_ਆਕਾਰ, ਵਿਭਾਗ_ਆਕਾਰ);
    }

    public void 지우기() {
        if (ਸਿਰਫ਼_ਪੜ੍ਹੋ_ਕੀਮਤ) {
            throw new IllegalStateException("ਪੜ੍ਹਨ 전용 장치입니다.");
        }
        Arrays.fill(ਸਮੱਗਰੀ, (byte) 0);
    }

    private void 범위확인(int ਵਿਭਾਗ_ਅਨੁਕ੍ਰਮਣਿਕਾ, byte[] 임시공간) {
        if (ਵਿਭਾਗ_ਅਨੁਕ੍ਰਮਣਿਕਾ < 0 || ਵਿਭਾਗ_ਅਨੁਕ੍ਰਮਣਿਕਾ >= 구역수() || 임시공간.length < ਵਿਭਾਗ_ਆਕਾਰ) {
            throw new IllegalArgumentException("ATA ਵਿਭਾਗ_ਕੀਮਤ 범위가 올바르지 않습니다.");
        }
    }
}

