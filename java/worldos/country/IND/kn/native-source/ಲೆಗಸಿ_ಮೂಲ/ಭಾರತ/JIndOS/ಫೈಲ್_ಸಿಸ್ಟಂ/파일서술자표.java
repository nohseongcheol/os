// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ಫೈಲ್_ಸಿಸ್ಟಂ;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ಕಡತ 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ಫೈಲ್_ಸಿಸ್ಟಂ.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ಫೈಲ್_ಸಿಸ್ಟಂ.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ಫೈಲ್_ಸಿಸ್ಟಂ ಫೈಲ್_ಸಿಸ್ಟಂ;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ಫೈಲ್_ಸಿಸ್ಟಂ ಫೈಲ್_ಸಿಸ್ಟಂ) {
        this.ಫೈಲ್_ಸಿಸ್ಟಂ = ಫೈಲ್_ಸಿಸ್ಟಂ;
    }

    public int ತೆರೆ(String ಹೆಸರು) {
        ಫೈಲ್_ಸಿಸ್ಟಂ.열린파일 열린파일 = ಫೈಲ್_ಸಿಸ್ಟಂ.ತೆರೆ(ಹೆಸರು);
        if (열린파일 == null) {
            return -2;
        }
        int ಪದಸೂಚಿ = ಖಾಲಿ_ಪದಸೂಚಿ(3);
        if (ಪದಸೂಚಿ < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ಪದಸೂಚಿ), new 서술자(열린파일));
        return ಪದಸೂಚಿ;
    }

    public int ಓದು(int ಪದಸೂಚಿ, byte[] 받을곳, int ಗಾತ್ರ) {
        서술자 ನಮೂದು_ಮೌಲ್ಯ = 서술자들.get(Integer.valueOf(ಪದಸೂಚಿ));
        if (ನಮೂದು_ಮೌಲ್ಯ == null) {
            return -9;
        }
        if (ಗಾತ್ರ < 0 || ಗಾತ್ರ > 받을곳.length) {
            return -22;
        }
        int 남음 = ನಮೂದು_ಮೌಲ್ಯ.열린파일.ಡೇಟಾ.length - ನಮೂದು_ಮೌಲ್ಯ.열린파일.ಸ್ಥಾನ;
        int 읽을크기 = Math.min(ಗಾತ್ರ, Math.max(남음, 0));
        System.arraycopy(ನಮೂದು_ಮೌಲ್ಯ.열린파일.ಡೇಟಾ, ನಮೂದು_ಮೌಲ್ಯ.열린파일.ಸ್ಥಾನ, 받을곳, 0, 읽을크기);
        ನಮೂದು_ಮೌಲ್ಯ.열린파일.ಸ್ಥಾನ += 읽을크기;
        return 읽을크기;
    }

    public int ಸರಿಸು_ಹುದ್ದೆ(int ಪದಸೂಚಿ, int 거리, int ಬಿಂಬಿಸು_ಮೂಲ) {
        서술자 ನಮೂದು_ಮೌಲ್ಯ = 서술자들.get(Integer.valueOf(ಪದಸೂಚಿ));
        if (ನಮೂದು_ಮೌಲ್ಯ == null) {
            return -9;
        }
        int ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ;
        if (ಬಿಂಬಿಸು_ಮೂಲ == 0) {
            ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ = 0;
        } else if (ಬಿಂಬಿಸು_ಮೂಲ == 1) {
            ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ = ನಮೂದು_ಮೌಲ್ಯ.열린파일.ಸ್ಥಾನ;
        } else if (ಬಿಂಬಿಸು_ಮೂಲ == 2) {
            ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ = ನಮೂದು_ಮೌಲ್ಯ.열린파일.ಡೇಟಾ.length;
        } else {
            return -22;
        }
        int 새위치 = ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ನಮೂದು_ಮೌಲ್ಯ.열린파일.ಸ್ಥಾನ = 새위치;
        return 새위치;
    }

    public int ಮುಚ್ಚು(int ಪದಸೂಚಿ) {
        서술자 ನಮೂದು_ಮೌಲ್ಯ = 서술자들.remove(Integer.valueOf(ಪದಸೂಚಿ));
        if (ನಮೂದು_ಮೌಲ್ಯ == null) {
            return -9;
        }
        ನಮೂದು_ಮೌಲ್ಯ.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int ಪದಸೂಚಿ, int 최소번호) {
        서술자 ನಮೂದು_ಮೌಲ್ಯ = 서술자들.get(Integer.valueOf(ಪದಸೂಚಿ));
        if (ನಮೂದು_ಮೌಲ್ಯ == null) {
            return -9;
        }
        int 새번호 = ಖಾಲಿ_ಪದಸೂಚಿ(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ನಮೂದು_ಮೌಲ್ಯ.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ನಮೂದು_ಮೌಲ್ಯ.열린파일));
        return 새번호;
    }

    public int 지정복제(int ಪದಸೂಚಿ, int 새번호) {
        if (ಪದಸೂಚಿ == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(ಪದಸೂಚಿ)) ? ಪದಸೂಚಿ : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ಪದಸೂಚಿ));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            ಮುಚ್ಚು(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int ಪದಸೂಚಿ, boolean ಮೌಲ್ಯ) {
        서술자 ನಮೂದು_ಮೌಲ್ಯ = 서술자들.get(Integer.valueOf(ಪದಸೂಚಿ));
        if (ನಮೂದು_ಮೌಲ್ಯ == null) {
            return -9;
        }
        ನಮೂದು_ಮೌಲ್ಯ.실행시닫기 = ಮೌಲ್ಯ;
        return 0;
    }

    public int 실행시닫기값(int ಪದಸೂಚಿ) {
        서술자 ನಮೂದು_ಮೌಲ್ಯ = 서술자들.get(Integer.valueOf(ಪದಸೂಚಿ));
        if (ನಮೂದು_ಮೌಲ್ಯ == null) {
            return -9;
        }
        return ನಮೂದು_ಮೌಲ್ಯ.실행시닫기 ? 1 : 0;
    }

    public ಫೈಲ್_ಮಾಹಿತಿ ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ(int ಪದಸೂಚಿ) {
        if (ಪದಸೂಚಿ >= 0 && ಪದಸೂಚಿ <= 2) {
            return new ಫೈಲ್_ಮಾಹಿತಿ(0, 0020666);
        }
        서술자 ನಮೂದು_ಮೌಲ್ಯ = 서술자들.get(Integer.valueOf(ಪದಸೂಚಿ));
        if (ನಮೂದು_ಮೌಲ್ಯ == null) {
            return null;
        }
        return new ಫೈಲ್_ಮಾಹಿತಿ(ನಮೂದು_ಮೌಲ್ಯ.열린파일.ಡೇಟಾ.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ಪದಸೂಚಿ : 번호들) {
            서술자 ನಮೂದು_ಮೌಲ್ಯ = 서술자들.get(ಪದಸೂಚಿ);
            if (ನಮೂದು_ಮೌಲ್ಯ != null && ನಮೂದು_ಮೌಲ್ಯ.실행시닫기) {
                ಮುಚ್ಚು(ಪದಸೂಚಿ.intValue());
            }
        }
    }

    public boolean ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ರಚಿಸು(int ಪದಸೂಚಿ) {
        return 서술자들.containsKey(Integer.valueOf(ಪದಸೂಚಿ));
    }

    public 파일서술자표 복제() {
        파일서술자표 ಮಾಪನ = new 파일서술자표(ಫೈಲ್_ಸಿಸ್ಟಂ);
        for (Map.Entry<Integer, 서술자> ನಮೂದು_ಮೌಲ್ಯ : 서술자들.entrySet()) {
            ನಮೂದು_ಮೌಲ್ಯ.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ನಮೂದು_ಮೌಲ್ಯ.getValue().열린파일);
            새서술자.실행시닫기 = ನಮೂದು_ಮೌಲ್ಯ.getValue().실행시닫기;
            ಮಾಪನ.서술자들.put(ನಮೂದು_ಮೌಲ್ಯ.getKey(), 새서술자);
        }
        return ಮಾಪನ;
    }

    private int ಖಾಲಿ_ಪದಸೂಚಿ(int 최소번호) {
        for (int ಪದಸೂಚಿ = Math.max(0, 최소번호); ಪದಸೂಚಿ < 최대서술자; ಪದಸೂಚಿ++) {
            if (!서술자들.containsKey(Integer.valueOf(ಪದಸೂಚಿ))) {
                return ಪದಸೂಚಿ;
            }
        }
        return -1;
    }
}
