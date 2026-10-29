// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਸਿੰਗਾਪੁਰ.JSgpOS.ਫਾਈਲ_ਸਿਸਟਮ;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ਫਾਇਲ 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ਫਾਈਲ_ਸਿਸਟਮ.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ਫਾਈਲ_ਸਿਸਟਮ.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ਫਾਈਲ_ਸਿਸਟਮ ਫਾਈਲ_ਸਿਸਟਮ;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ਫਾਈਲ_ਸਿਸਟਮ ਫਾਈਲ_ਸਿਸਟਮ) {
        this.ਫਾਈਲ_ਸਿਸਟਮ = ਫਾਈਲ_ਸਿਸਟਮ;
    }

    public int ਖੋਲ੍ਹੋ(String ਨਾਂ) {
        ਫਾਈਲ_ਸਿਸਟਮ.열린파일 열린파일 = ਫਾਈਲ_ਸਿਸਟਮ.ਖੋਲ੍ਹੋ(ਨਾਂ);
        if (열린파일 == null) {
            return -2;
        }
        int ਅਨੁਕ੍ਰਮਣਿਕਾ = ਖਾਲੀ_ਅਨੁਕ੍ਰਮਣਿਕਾ(3);
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ), new 서술자(열린파일));
        return ਅਨੁਕ੍ਰਮਣਿਕਾ;
    }

    public int ਪੜ੍ਹਨ(int ਅਨੁਕ੍ਰਮਣਿਕਾ, byte[] 받을곳, int ਆਕਾਰ) {
        서술자 ਦਾਖਲਾ_ਕੀਮਤ = 서술자들.get(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ));
        if (ਦਾਖਲਾ_ਕੀਮਤ == null) {
            return -9;
        }
        if (ਆਕਾਰ < 0 || ਆਕਾਰ > 받을곳.length) {
            return -22;
        }
        int 남음 = ਦਾਖਲਾ_ਕੀਮਤ.열린파일.ਸਮੱਗਰੀ.length - ਦਾਖਲਾ_ਕੀਮਤ.열린파일.ਸਥਿਤੀ;
        int 읽을크기 = Math.min(ਆਕਾਰ, Math.max(남음, 0));
        System.arraycopy(ਦਾਖਲਾ_ਕੀਮਤ.열린파일.ਸਮੱਗਰੀ, ਦਾਖਲਾ_ਕੀਮਤ.열린파일.ਸਥਿਤੀ, 받을곳, 0, 읽을크기);
        ਦਾਖਲਾ_ਕੀਮਤ.열린파일.ਸਥਿਤੀ += 읽을크기;
        return 읽을크기;
    }

    public int ਖਿਸਕਾਉਣਾ_ਸਥਿਤੀ_ਬਦਲੋ(int ਅਨੁਕ੍ਰਮਣਿਕਾ, int 거리, int ਪ੍ਰੋਜੈਕਟ_ਰੂਟ) {
        서술자 ਦਾਖਲਾ_ਕੀਮਤ = 서술자들.get(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ));
        if (ਦਾਖਲਾ_ਕੀਮਤ == null) {
            return -9;
        }
        int ਪਿਛੋਕੜ_ਕੀਮਤ;
        if (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ == 0) {
            ਪਿਛੋਕੜ_ਕੀਮਤ = 0;
        } else if (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ == 1) {
            ਪਿਛੋਕੜ_ਕੀਮਤ = ਦਾਖਲਾ_ਕੀਮਤ.열린파일.ਸਥਿਤੀ;
        } else if (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ == 2) {
            ਪਿਛੋਕੜ_ਕੀਮਤ = ਦਾਖਲਾ_ਕੀਮਤ.열린파일.ਸਮੱਗਰੀ.length;
        } else {
            return -22;
        }
        int 새위치 = ਪਿਛੋਕੜ_ਕੀਮਤ + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ਦਾਖਲਾ_ਕੀਮਤ.열린파일.ਸਥਿਤੀ = 새위치;
        return 새위치;
    }

    public int ਬੰਦ_ਕਰੋ(int ਅਨੁਕ੍ਰਮਣਿਕਾ) {
        서술자 ਦਾਖਲਾ_ਕੀਮਤ = 서술자들.remove(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ));
        if (ਦਾਖਲਾ_ਕੀਮਤ == null) {
            return -9;
        }
        ਦਾਖਲਾ_ਕੀਮਤ.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int ਅਨੁਕ੍ਰਮਣਿਕਾ, int 최소번호) {
        서술자 ਦਾਖਲਾ_ਕੀਮਤ = 서술자들.get(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ));
        if (ਦਾਖਲਾ_ਕੀਮਤ == null) {
            return -9;
        }
        int 새번호 = ਖਾਲੀ_ਅਨੁਕ੍ਰਮਣਿਕਾ(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ਦਾਖਲਾ_ਕੀਮਤ.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ਦਾਖਲਾ_ਕੀਮਤ.열린파일));
        return 새번호;
    }

    public int 지정복제(int ਅਨੁਕ੍ਰਮਣਿਕਾ, int 새번호) {
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ)) ? ਅਨੁਕ੍ਰਮਣਿਕਾ : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            ਬੰਦ_ਕਰੋ(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int ਅਨੁਕ੍ਰਮਣਿਕਾ, boolean ਕੀਮਤ) {
        서술자 ਦਾਖਲਾ_ਕੀਮਤ = 서술자들.get(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ));
        if (ਦਾਖਲਾ_ਕੀਮਤ == null) {
            return -9;
        }
        ਦਾਖਲਾ_ਕੀਮਤ.실행시닫기 = ਕੀਮਤ;
        return 0;
    }

    public int 실행시닫기값(int ਅਨੁਕ੍ਰਮਣਿਕਾ) {
        서술자 ਦਾਖਲਾ_ਕੀਮਤ = 서술자들.get(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ));
        if (ਦਾਖਲਾ_ਕੀਮਤ == null) {
            return -9;
        }
        return ਦਾਖਲਾ_ਕੀਮਤ.실행시닫기 ? 1 : 0;
    }

    public ਲਿਖਤ_ਪੱਤਰ_ਜਾਣਕਾਰੀ ਸਿਸਟਮ_ਜਾਣਕਾਰੀ(int ਅਨੁਕ੍ਰਮਣਿਕਾ) {
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ >= 0 && ਅਨੁਕ੍ਰਮਣਿਕਾ <= 2) {
            return new ਲਿਖਤ_ਪੱਤਰ_ਜਾਣਕਾਰੀ(0, 0020666);
        }
        서술자 ਦਾਖਲਾ_ਕੀਮਤ = 서술자들.get(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ));
        if (ਦਾਖਲਾ_ਕੀਮਤ == null) {
            return null;
        }
        return new ਲਿਖਤ_ਪੱਤਰ_ਜਾਣਕਾਰੀ(ਦਾਖਲਾ_ਕੀਮਤ.열린파일.ਸਮੱਗਰੀ.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ਅਨੁਕ੍ਰਮਣਿਕਾ : 번호들) {
            서술자 ਦਾਖਲਾ_ਕੀਮਤ = 서술자들.get(ਅਨੁਕ੍ਰਮਣਿਕਾ);
            if (ਦਾਖਲਾ_ਕੀਮਤ != null && ਦਾਖਲਾ_ਕੀਮਤ.실행시닫기) {
                ਬੰਦ_ਕਰੋ(ਅਨੁਕ੍ਰਮਣਿਕਾ.intValue());
            }
        }
    }

    public boolean 열려있음(int ਅਨੁਕ੍ਰਮਣਿਕਾ) {
        return 서술자들.containsKey(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ));
    }

    public 파일서술자표 복제() {
        파일서술자표 ਮਾਪ = new 파일서술자표(ਫਾਈਲ_ਸਿਸਟਮ);
        for (Map.Entry<Integer, 서술자> ਦਾਖਲਾ_ਕੀਮਤ : 서술자들.entrySet()) {
            ਦਾਖਲਾ_ਕੀਮਤ.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ਦਾਖਲਾ_ਕੀਮਤ.getValue().열린파일);
            새서술자.실행시닫기 = ਦਾਖਲਾ_ਕੀਮਤ.getValue().실행시닫기;
            ਮਾਪ.서술자들.put(ਦਾਖਲਾ_ਕੀਮਤ.getKey(), 새서술자);
        }
        return ਮਾਪ;
    }

    private int ਖਾਲੀ_ਅਨੁਕ੍ਰਮਣਿਕਾ(int 최소번호) {
        for (int ਅਨੁਕ੍ਰਮਣਿਕਾ = Math.max(0, 최소번호); ਅਨੁਕ੍ਰਮਣਿਕਾ < 최대서술자; ਅਨੁਕ੍ਰਮਣਿਕਾ++) {
            if (!서술자들.containsKey(Integer.valueOf(ਅਨੁਕ੍ਰਮਣਿਕਾ))) {
                return ਅਨੁਕ੍ਰਮਣਿਕਾ;
            }
        }
        return -1;
    }
}
