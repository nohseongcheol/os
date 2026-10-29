// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਕੈਨੇਡਾ.JCanOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ਪੰਨਾ_ਕੀਮਤ 연결과 ਲਿਖਣ 시 복사를 제공한다. */
public final class ਪੰਨਾ_ਪ੍ਰਬੰਧਕ {
    public static final int ਪੰਨਾ_ਆਕਾਰ = 4096;

    private static final class ਪੰਨਾ_ਕੀਮਤ {
        private byte[] ਸਮੱਗਰੀ = new byte[ਪੰਨਾ_ਆਕਾਰ];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ਪਤਾ_ਥਾਂ {
        private final Map<Integer, ਪੰਨਾ_ਕੀਮਤ> ਪੰਨਾ_ਤਾਲਿਕਾ = new HashMap<Integer, ਪੰਨਾ_ਕੀਮਤ>();
    }

    public ਪਤਾ_ਥਾਂ 새주소공간() {
        return new ਪਤਾ_ਥਾਂ();
    }

    public void ਮੈਪ_ਪੰਨਾ(ਪਤਾ_ਥਾਂ 공간, int ਵਰਚੁਅਲ_ਪਤਾ, boolean 쓰기가능) {
        int ਅਨੁਕ੍ਰਮਣਿਕਾ = 쪽번호(ਵਰਚੁਅਲ_ਪਤਾ);
        ਪੰਨਾ_ਕੀਮਤ 새쪽 = new ਪੰਨਾ_ਕੀਮਤ();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ਪੰਨਾ_ਤਾਲਿਕਾ.put(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ), 새쪽);
    }

    public ਪਤਾ_ਥਾਂ 쓰기시복사복제(ਪਤਾ_ਥਾਂ 원본) {
        ਪਤਾ_ਥਾਂ 복제본 = new ਪਤਾ_ਥਾਂ();
        for (Map.Entry<Integer, ਪੰਨਾ_ਕੀਮਤ> ਦਾਖਲਾ_ਕੀਮਤ : 원본.ਪੰਨਾ_ਤਾਲਿਕਾ.entrySet()) {
            ਪੰਨਾ_ਕੀਮਤ 공유쪽 = ਦਾਖਲਾ_ਕੀਮਤ.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ਪੰਨਾ_ਤਾਲਿਕਾ.put(ਦਾਖਲਾ_ਕੀਮਤ.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ਪਤਾ_ਥਾਂ 공간, int ਵਰਚੁਅਲ_ਪਤਾ) {
        ਪੰਨਾ_ਕੀਮਤ ਟੀਚਾ = ਲੱਭੋ_ਪੰਨਾ(공간, ਵਰਚੁਅਲ_ਪਤਾ);
        return ਟੀਚਾ.ਸਮੱਗਰੀ[Math.floorMod(ਵਰਚੁਅਲ_ਪਤਾ, ਪੰਨਾ_ਆਕਾਰ)];
    }

    public void ਲਿੱਖੋ_ਬਾਈਟ_ਕੀਮਤ(ਪਤਾ_ਥਾਂ 공간, int ਵਰਚੁਅਲ_ਪਤਾ, byte ਕੀਮਤ) {
        int ਅਨੁਕ੍ਰਮਣਿਕਾ = 쪽번호(ਵਰਚੁਅਲ_ਪਤਾ);
        ਪੰਨਾ_ਕੀਮਤ ਟੀਚਾ = ਲੱਭੋ_ਪੰਨਾ(공간, ਵਰਚੁਅਲ_ਪਤਾ);
        if (!ਟੀਚਾ.쓰기가능) {
            if (!ਟੀਚਾ.쓰기시복사) {
                throw new IllegalStateException("ਪੜ੍ਹਨ 전용 쪽입니다.");
            }
            ਟੀਚਾ = ਬਣਾਓ_ਨਿੱਜੀ_ਪੰਨਾ(공간, ਅਨੁਕ੍ਰਮਣਿਕਾ, ਟੀਚਾ);
        }
        ਟੀਚਾ.ਸਮੱਗਰੀ[Math.floorMod(ਵਰਚੁਅਲ_ਪਤਾ, ਪੰਨਾ_ਆਕਾਰ)] = ਕੀਮਤ;
    }

    public void 범위개인쓰기(ਪਤਾ_ਥਾਂ 공간, int ਸੁਰੂ_ਪਤਾ, int ਆਕਾਰ) {
        if (ਆਕਾਰ < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ਅੰਤ_ਪਤਾ = Math.addExact(ਸੁਰੂ_ਪਤਾ, ਆਕਾਰ);
        for (int ਪਤਾ = ਸੁਰੂ_ਪਤਾ; ਪਤਾ < ਅੰਤ_ਪਤਾ; ਪਤਾ = (쪽번호(ਪਤਾ) + 1) * ਪੰਨਾ_ਆਕਾਰ) {
            int ਅਨੁਕ੍ਰਮਣਿਕਾ = 쪽번호(ਪਤਾ);
            ਪੰਨਾ_ਕੀਮਤ ਟੀਚਾ = ਲੱਭੋ_ਪੰਨਾ(공간, ਪਤਾ);
            if (ਟੀਚਾ.쓰기시복사) {
                ਬਣਾਓ_ਨਿੱਜੀ_ਪੰਨਾ(공간, ਅਨੁਕ੍ਰਮਣਿਕਾ, ਟੀਚਾ);
            } else {
                ਟੀਚਾ.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ਪਤਾ_ਥਾਂ 공간, int ਸੁਰੂ_ਪਤਾ, byte[] ਸਮੱਗਰੀ) {
        for (int ਅਨੁਕ੍ਰਮਣਿਕਾ = 0; ਅਨੁਕ੍ਰਮਣਿਕਾ < ਸਮੱਗਰੀ.length; ਅਨੁਕ੍ਰਮਣਿਕਾ++) {
            ਲਿੱਖੋ_ਬਾਈਟ_ਕੀਮਤ(공간, ਸੁਰੂ_ਪਤਾ + ਅਨੁਕ੍ਰਮਣਿਕਾ, ਸਮੱਗਰੀ[ਅਨੁਕ੍ਰਮਣਿਕਾ]);
        }
    }

    private ਪੰਨਾ_ਕੀਮਤ ਬਣਾਓ_ਨਿੱਜੀ_ਪੰਨਾ(ਪਤਾ_ਥਾਂ 공간, int ਅਨੁਕ੍ਰਮਣਿਕਾ, ਪੰਨਾ_ਕੀਮਤ 공유쪽) {
        ਪੰਨਾ_ਕੀਮਤ ਨਿੱਜੀ_ਪੰਨਾ = new ਪੰਨਾ_ਕੀਮਤ();
        ਨਿੱਜੀ_ਪੰਨਾ.ਸਮੱਗਰੀ = Arrays.copyOf(공유쪽.ਸਮੱਗਰੀ, 공유쪽.ਸਮੱਗਰੀ.length);
        ਨਿੱਜੀ_ਪੰਨਾ.쓰기가능 = true;
        ਨਿੱਜੀ_ਪੰਨਾ.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ਪੰਨਾ_ਤਾਲਿਕਾ.put(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ), ਨਿੱਜੀ_ਪੰਨਾ);
        return ਨਿੱਜੀ_ਪੰਨਾ;
    }

    private ਪੰਨਾ_ਕੀਮਤ ਲੱਭੋ_ਪੰਨਾ(ਪਤਾ_ਥਾਂ 공간, int ਪਤਾ) {
        ਪੰਨਾ_ਕੀਮਤ ਟੀਚਾ = 공간.ਪੰਨਾ_ਤਾਲਿਕਾ.get(Integer.valueOf(쪽번호(ਪਤਾ)));
        if (ਟੀਚਾ == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ਟੀਚਾ;
    }

    private int 쪽번호(int ਪਤਾ) {
        if (ਪਤਾ < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ਪਤਾ / ਪੰਨਾ_ਆਕਾਰ;
    }
}

