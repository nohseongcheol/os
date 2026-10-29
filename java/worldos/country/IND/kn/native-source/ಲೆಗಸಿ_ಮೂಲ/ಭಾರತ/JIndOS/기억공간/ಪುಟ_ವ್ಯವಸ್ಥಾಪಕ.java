// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ಪುಟ_ಮೌಲ್ಯ 연결과 ಬರೆ 시 복사를 제공한다. */
public final class ಪುಟ_ವ್ಯವಸ್ಥಾಪಕ {
    public static final int ಪುಟದ_ಗಾತ್ರ = 4096;

    private static final class ಪುಟ_ಮೌಲ್ಯ {
        private byte[] ಡೇಟಾ = new byte[ಪುಟದ_ಗಾತ್ರ];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ಇಮೇಲ್_ಸ್ಪೇಸ್ {
        private final Map<Integer, ಪುಟ_ಮೌಲ್ಯ> ಪುಟ_ಕೋಷ್ಟಕ = new HashMap<Integer, ಪುಟ_ಮೌಲ್ಯ>();
    }

    public ಇಮೇಲ್_ಸ್ಪೇಸ್ 새주소공간() {
        return new ಇಮೇಲ್_ಸ್ಪೇಸ್();
    }

    public void ಮ್ಯಾಪ್_ಮಾಡಿ_ಪುಟ(ಇಮೇಲ್_ಸ್ಪೇಸ್ 공간, int ಅಗೋಚರ_ವಿಳಾಸ, boolean 쓰기가능) {
        int ಪದಸೂಚಿ = 쪽번호(ಅಗೋಚರ_ವಿಳಾಸ);
        ಪುಟ_ಮೌಲ್ಯ 새쪽 = new ಪುಟ_ಮೌಲ್ಯ();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ಪುಟ_ಕೋಷ್ಟಕ.put(Integer.valueOf(ಪದಸೂಚಿ), 새쪽);
    }

    public ಇಮೇಲ್_ಸ್ಪೇಸ್ 쓰기시복사복제(ಇಮೇಲ್_ಸ್ಪೇಸ್ 원본) {
        ಇಮೇಲ್_ಸ್ಪೇಸ್ 복제본 = new ಇಮೇಲ್_ಸ್ಪೇಸ್();
        for (Map.Entry<Integer, ಪುಟ_ಮೌಲ್ಯ> ನಮೂದು_ಮೌಲ್ಯ : 원본.ಪುಟ_ಕೋಷ್ಟಕ.entrySet()) {
            ಪುಟ_ಮೌಲ್ಯ 공유쪽 = ನಮೂದು_ಮೌಲ್ಯ.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ಪುಟ_ಕೋಷ್ಟಕ.put(ನಮೂದು_ಮೌಲ್ಯ.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ಇಮೇಲ್_ಸ್ಪೇಸ್ 공간, int ಅಗೋಚರ_ವಿಳಾಸ) {
        ಪುಟ_ಮೌಲ್ಯ ಲಕ್ಷ್ಯ = ಹುಡುಕಿ_ಪುಟ(공간, ಅಗೋಚರ_ವಿಳಾಸ);
        return ಲಕ್ಷ್ಯ.ಡೇಟಾ[Math.floorMod(ಅಗೋಚರ_ವಿಳಾಸ, ಪುಟದ_ಗಾತ್ರ)];
    }

    public void ಬರೆ_ಬೈಟ್_ಮೌಲ್ಯ(ಇಮೇಲ್_ಸ್ಪೇಸ್ 공간, int ಅಗೋಚರ_ವಿಳಾಸ, byte ಮೌಲ್ಯ) {
        int ಪದಸೂಚಿ = 쪽번호(ಅಗೋಚರ_ವಿಳಾಸ);
        ಪುಟ_ಮೌಲ್ಯ ಲಕ್ಷ್ಯ = ಹುಡುಕಿ_ಪುಟ(공간, ಅಗೋಚರ_ವಿಳಾಸ);
        if (!ಲಕ್ಷ್ಯ.쓰기가능) {
            if (!ಲಕ್ಷ್ಯ.쓰기시복사) {
                throw new IllegalStateException("ಓದು 전용 쪽입니다.");
            }
            ಲಕ್ಷ್ಯ = ರಚಿಸು_ಖಾಸಗಿ_ಪುಟ(공간, ಪದಸೂಚಿ, ಲಕ್ಷ್ಯ);
        }
        ಲಕ್ಷ್ಯ.ಡೇಟಾ[Math.floorMod(ಅಗೋಚರ_ವಿಳಾಸ, ಪುಟದ_ಗಾತ್ರ)] = ಮೌಲ್ಯ;
    }

    public void 범위개인쓰기(ಇಮೇಲ್_ಸ್ಪೇಸ್ 공간, int ಆರಂಭಿಸು_ಇಮೇಲ್, int ಗಾತ್ರ) {
        if (ಗಾತ್ರ < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ಅಂತ್ಯಗೊಳಿಸು_ಇಮೇಲ್ = Math.addExact(ಆರಂಭಿಸು_ಇಮೇಲ್, ಗಾತ್ರ);
        for (int ಇಮೇಲ್ = ಆರಂಭಿಸು_ಇಮೇಲ್; ಇಮೇಲ್ < ಅಂತ್ಯಗೊಳಿಸು_ಇಮೇಲ್; ಇಮೇಲ್ = (쪽번호(ಇಮೇಲ್) + 1) * ಪುಟದ_ಗಾತ್ರ) {
            int ಪದಸೂಚಿ = 쪽번호(ಇಮೇಲ್);
            ಪುಟ_ಮೌಲ್ಯ ಲಕ್ಷ್ಯ = ಹುಡುಕಿ_ಪುಟ(공간, ಇಮೇಲ್);
            if (ಲಕ್ಷ್ಯ.쓰기시복사) {
                ರಚಿಸು_ಖಾಸಗಿ_ಪುಟ(공간, ಪದಸೂಚಿ, ಲಕ್ಷ್ಯ);
            } else {
                ಲಕ್ಷ್ಯ.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ಇಮೇಲ್_ಸ್ಪೇಸ್ 공간, int ಆರಂಭಿಸು_ಇಮೇಲ್, byte[] ಡೇಟಾ) {
        for (int ಪದಸೂಚಿ = 0; ಪದಸೂಚಿ < ಡೇಟಾ.length; ಪದಸೂಚಿ++) {
            ಬರೆ_ಬೈಟ್_ಮೌಲ್ಯ(공간, ಆರಂಭಿಸು_ಇಮೇಲ್ + ಪದಸೂಚಿ, ಡೇಟಾ[ಪದಸೂಚಿ]);
        }
    }

    private ಪುಟ_ಮೌಲ್ಯ ರಚಿಸು_ಖಾಸಗಿ_ಪುಟ(ಇಮೇಲ್_ಸ್ಪೇಸ್ 공간, int ಪದಸೂಚಿ, ಪುಟ_ಮೌಲ್ಯ 공유쪽) {
        ಪುಟ_ಮೌಲ್ಯ ಖಾಸಗಿ_ಪುಟ = new ಪುಟ_ಮೌಲ್ಯ();
        ಖಾಸಗಿ_ಪುಟ.ಡೇಟಾ = Arrays.copyOf(공유쪽.ಡೇಟಾ, 공유쪽.ಡೇಟಾ.length);
        ಖಾಸಗಿ_ಪುಟ.쓰기가능 = true;
        ಖಾಸಗಿ_ಪುಟ.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ಪುಟ_ಕೋಷ್ಟಕ.put(Integer.valueOf(ಪದಸೂಚಿ), ಖಾಸಗಿ_ಪುಟ);
        return ಖಾಸಗಿ_ಪುಟ;
    }

    private ಪುಟ_ಮೌಲ್ಯ ಹುಡುಕಿ_ಪುಟ(ಇಮೇಲ್_ಸ್ಪೇಸ್ 공간, int ಇಮೇಲ್) {
        ಪುಟ_ಮೌಲ್ಯ ಲಕ್ಷ್ಯ = 공간.ಪುಟ_ಕೋಷ್ಟಕ.get(Integer.valueOf(쪽번호(ಇಮೇಲ್)));
        if (ಲಕ್ಷ್ಯ == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ಲಕ್ಷ್ಯ;
    }

    private int 쪽번호(int ಇಮೇಲ್) {
        if (ಇಮೇಲ್ < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ಇಮೇಲ್ / ಪುಟದ_ಗಾತ್ರ;
    }
}

