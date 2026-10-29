// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਕੀਨੀਆ.JKenOS.ਫਾਈਲ_ਸਿਸਟਮ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class ਵਿਭਾਗ_ਕੀਮਤ {
        private final int 종류;
        private final int ਨਿਸ਼ਾਨ_ਕੀਮਤ;
        private final int ਪਤਾ;
        private final int ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ;
        private final int ਆਕਾਰ;

        ਵਿਭਾਗ_ਕੀਮਤ(int 종류, int ਨਿਸ਼ਾਨ_ਕੀਮਤ, int ਪਤਾ, int ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ, int ਆਕਾਰ) {
            this.종류 = 종류;
            this.ਨਿਸ਼ਾਨ_ਕੀਮਤ = ਨਿਸ਼ਾਨ_ਕੀਮਤ;
            this.ਪਤਾ = ਪਤਾ;
            this.ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ = ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ;
            this.ਆਕਾਰ = ਆਕਾਰ;
        }

        public int 종류() {
            return 종류;
        }

        public int ਨਿਸ਼ਾਨ_ਕੀਮਤ() {
            return ਨਿਸ਼ਾਨ_ਕੀਮਤ;
        }

        public int ਪਤਾ() {
            return ਪਤਾ;
        }

        public int ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ() {
            return ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ;
        }

        public int ਆਕਾਰ() {
            return ਆਕਾਰ;
        }
    }

    public static final class ਤਸਵੀਰ {
        private final int ਸੁਰੂ_ਪਤਾ;
        private final List<ਵਿਭਾਗ_ਕੀਮਤ> 구역들;

        ਤਸਵੀਰ(int ਸੁਰੂ_ਪਤਾ, List<ਵਿਭਾਗ_ਕੀਮਤ> 구역들) {
            this.ਸੁਰੂ_ਪਤਾ = ਸੁਰੂ_ਪਤਾ;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ਸੁਰੂ_ਪਤਾ() {
            return ਸੁਰੂ_ਪਤਾ;
        }

        public List<ਵਿਭਾਗ_ਕੀਮਤ> 구역들() {
            return 구역들;
        }
    }

    public ਤਸਵੀਰ 검사(byte[] ਸਮੱਗਰੀ) {
        if (ਸਮੱਗਰੀ == null || ਸਮੱਗਰੀ.length < 52
                || ਸਮੱਗਰੀ[0] != 0x7f || ਸਮੱਗਰੀ[1] != 'E' || ਸਮੱਗਰੀ[2] != 'L' || ਸਮੱਗਰੀ[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ਸਮੱਗਰੀ[4] != 1 || ਸਮੱਗਰੀ[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ਸੁਰੂ_ਪਤਾ = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਪੂਰਣ_ਅੰਕ(ਸਮੱਗਰੀ, 24);
        int ਵਿਭਾਗ_ਤਾਲਿਕਾ_ਸਥਿਤੀ_ਬਦਲੋ = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਪੂਰਣ_ਅੰਕ(ਸਮੱਗਰੀ, 32);
        int ਵਿਭਾਗ_ਦਾਖਲਾ_ਆਕਾਰ = 짧은정수읽기(ਸਮੱਗਰੀ, 46);
        int 구역수 = 짧은정수읽기(ਸਮੱਗਰੀ, 48);
        if (ਵਿਭਾਗ_ਦਾਖਲਾ_ਆਕਾਰ < 40 || ਵਿਭਾਗ_ਤਾਲਿਕਾ_ਸਥਿਤੀ_ਬਦਲੋ < 0
                || (long) ਵਿਭਾਗ_ਤਾਲਿਕਾ_ਸਥਿਤੀ_ਬਦਲੋ + (long) ਵਿਭਾਗ_ਦਾਖਲਾ_ਆਕਾਰ * 구역수 > ਸਮੱਗਰੀ.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<ਵਿਭਾਗ_ਕੀਮਤ> 구역들 = new ArrayList<ਵਿਭਾਗ_ਕੀਮਤ>();
        for (int ਅਨੁਕ੍ਰਮਣਿਕਾ = 0; ਅਨੁਕ੍ਰਮਣਿਕਾ < 구역수; ਅਨੁਕ੍ਰਮਣਿਕਾ++) {
            int ਸਥਿਤੀ = ਵਿਭਾਗ_ਤਾਲਿਕਾ_ਸਥਿਤੀ_ਬਦਲੋ + ਅਨੁਕ੍ਰਮਣਿਕਾ * ਵਿਭਾਗ_ਦਾਖਲਾ_ਆਕਾਰ;
            int 종류 = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਪੂਰਣ_ਅੰਕ(ਸਮੱਗਰੀ, ਸਥਿਤੀ + 4);
            int ਨਿਸ਼ਾਨ_ਕੀਮਤ = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਪੂਰਣ_ਅੰਕ(ਸਮੱਗਰੀ, ਸਥਿਤੀ + 8);
            int ਪਤਾ = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਪੂਰਣ_ਅੰਕ(ਸਮੱਗਰੀ, ਸਥਿਤੀ + 12);
            int ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਪੂਰਣ_ਅੰਕ(ਸਮੱਗਰੀ, ਸਥਿਤੀ + 16);
            int ਆਕਾਰ = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਪੂਰਣ_ਅੰਕ(ਸਮੱਗਰੀ, ਸਥਿਤੀ + 20);
            if (ਆਕਾਰ < 0 || (종류 != 8 && ((long) ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ + ਆਕਾਰ > ਸਮੱਗਰੀ.length || ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ < 0))) {
                throw new IllegalArgumentException("ELF ਵਿਭਾਗ_ਕੀਮਤ ਸਮੱਗਰੀ 범위가 올바르지 않습니다.");
            }
            구역들.add(new ਵਿਭਾਗ_ਕੀਮਤ(종류, ਨਿਸ਼ਾਨ_ਕੀਮਤ, ਪਤਾ, ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ, ਆਕਾਰ));
        }
        return new ਤਸਵੀਰ(ਸੁਰੂ_ਪਤਾ, 구역들);
    }

    private int ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਪੂਰਣ_ਅੰਕ(byte[] ਸਮੱਗਰੀ, int ਸਥਿਤੀ) {
        if (ਸਥਿਤੀ < 0 || ਸਥਿਤੀ > ਸਮੱਗਰੀ.length - 4) {
            throw new IllegalArgumentException("ELF ਪੂਰਣ_ਅੰਕ 범위를 벗어났습니다.");
        }
        return (ਸਮੱਗਰੀ[ਸਥਿਤੀ] & 0xff)
                | ((ਸਮੱਗਰੀ[ਸਥਿਤੀ + 1] & 0xff) << 8)
                | ((ਸਮੱਗਰੀ[ਸਥਿਤੀ + 2] & 0xff) << 16)
                | ((ਸਮੱਗਰੀ[ਸਥਿਤੀ + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ਸਮੱਗਰੀ, int ਸਥਿਤੀ) {
        if (ਸਥਿਤੀ < 0 || ਸਥਿਤੀ > ਸਮੱਗਰੀ.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ਪੂਰਣ_ਅੰਕ 범위를 벗어났습니다.");
        }
        return (ਸਮੱਗਰੀ[ਸਥਿਤੀ] & 0xff) | ((ਸਮੱਗਰੀ[ਸਥਿਤੀ + 1] & 0xff) << 8);
    }
}
