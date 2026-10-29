// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.ফাইল_ছিষ্টেম;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 নথিপত্ৰ 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ফাইল_ছিষ্টেম.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ফাইল_ছিষ্টেম.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ফাইল_ছিষ্টেম ফাইল_ছিষ্টেম;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ফাইল_ছিষ্টেম ফাইল_ছিষ্টেম) {
        this.ফাইল_ছিষ্টেম = ফাইল_ছিষ্টেম;
    }

    public int খোলো(String নাম) {
        ফাইল_ছিষ্টেম.열린파일 열린파일 = ফাইল_ছিষ্টেম.খোলো(নাম);
        if (열린파일 == null) {
            return -2;
        }
        int ইনডেক্স = খালী_ইনডেক্স(3);
        if (ইনডেক্স < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ইনডেক্স), new 서술자(열린파일));
        return ইনডেক্স;
    }

    public int পড়া(int ইনডেক্স, byte[] 받을곳, int মাপ) {
        서술자 প্রবিষ্ট_মান = 서술자들.get(Integer.valueOf(ইনডেক্স));
        if (প্রবিষ্ট_মান == null) {
            return -9;
        }
        if (মাপ < 0 || মাপ > 받을곳.length) {
            return -22;
        }
        int 남음 = প্রবিষ্ট_মান.열린파일.ডাটা.length - প্রবিষ্ট_মান.열린파일.অৱস্থান;
        int 읽을크기 = Math.min(মাপ, Math.max(남음, 0));
        System.arraycopy(প্রবিষ্ট_মান.열린파일.ডাটা, প্রবিষ্ট_মান.열린파일.অৱস্থান, 받을곳, 0, 읽을크기);
        প্রবিষ্ট_মান.열린파일.অৱস্থান += 읽을크기;
        return 읽을크기;
    }

    public int লৈ_যাওক_স্থান_সলনি_কৰক(int ইনডেক্স, int 거리, int 기준) {
        서술자 প্রবিষ্ট_মান = 서술자들.get(Integer.valueOf(ইনডেক্স));
        if (প্রবিষ্ট_মান == null) {
            return -9;
        }
        int পটভূমি_মান;
        if (기준 == 0) {
            পটভূমি_মান = 0;
        } else if (기준 == 1) {
            পটভূমি_মান = প্রবিষ্ট_মান.열린파일.অৱস্থান;
        } else if (기준 == 2) {
            পটভূমি_মান = প্রবিষ্ট_মান.열린파일.ডাটা.length;
        } else {
            return -22;
        }
        int 새위치 = পটভূমি_মান + 거리;
        if (새위치 < 0) {
            return -22;
        }
        প্রবিষ্ট_মান.열린파일.অৱস্থান = 새위치;
        return 새위치;
    }

    public int বন্ধ_কৰক(int ইনডেক্স) {
        서술자 প্রবিষ্ট_মান = 서술자들.remove(Integer.valueOf(ইনডেক্স));
        if (প্রবিষ্ট_মান == null) {
            return -9;
        }
        প্রবিষ্ট_মান.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int ইনডেক্স, int 최소번호) {
        서술자 প্রবিষ্ট_মান = 서술자들.get(Integer.valueOf(ইনডেক্স));
        if (প্রবিষ্ট_মান == null) {
            return -9;
        }
        int 새번호 = খালী_ইনডেক্স(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        প্রবিষ্ট_মান.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(প্রবিষ্ট_মান.열린파일));
        return 새번호;
    }

    public int 지정복제(int ইনডেক্স, int 새번호) {
        if (ইনডেক্স == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(ইনডেক্স)) ? ইনডেক্স : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ইনডেক্স));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            বন্ধ_কৰক(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int ইনডেক্স, boolean মান) {
        서술자 প্রবিষ্ট_মান = 서술자들.get(Integer.valueOf(ইনডেক্স));
        if (প্রবিষ্ট_মান == null) {
            return -9;
        }
        প্রবিষ্ট_মান.실행시닫기 = মান;
        return 0;
    }

    public int 실행시닫기값(int ইনডেক্স) {
        서술자 প্রবিষ্ট_মান = 서술자들.get(Integer.valueOf(ইনডেক্স));
        if (প্রবিষ্ট_মান == null) {
            return -9;
        }
        return প্রবিষ্ট_মান.실행시닫기 ? 1 : 0;
    }

    public ফাইল_তথ্য ছিষ্টেম_তথ্য(int ইনডেক্স) {
        if (ইনডেক্স >= 0 && ইনডেক্স <= 2) {
            return new ফাইল_তথ্য(0, 0020666);
        }
        서술자 প্রবিষ্ট_মান = 서술자들.get(Integer.valueOf(ইনডেক্স));
        if (প্রবিষ্ট_মান == null) {
            return null;
        }
        return new ফাইল_তথ্য(প্রবিষ্ট_মান.열린파일.ডাটা.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ইনডেক্স : 번호들) {
            서술자 প্রবিষ্ট_মান = 서술자들.get(ইনডেক্স);
            if (প্রবিষ্ট_মান != null && প্রবিষ্ট_মান.실행시닫기) {
                বন্ধ_কৰক(ইনডেক্স.intValue());
            }
        }
    }

    public boolean 열려있음(int ইনডেক্স) {
        return 서술자들.containsKey(Integer.valueOf(ইনডেক্স));
    }

    public 파일서술자표 복제() {
        파일서술자표 পৰিমাপ = new 파일서술자표(ফাইল_ছিষ্টেম);
        for (Map.Entry<Integer, 서술자> প্রবিষ্ট_মান : 서술자들.entrySet()) {
            প্রবিষ্ট_মান.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(প্রবিষ্ট_মান.getValue().열린파일);
            새서술자.실행시닫기 = প্রবিষ্ট_মান.getValue().실행시닫기;
            পৰিমাপ.서술자들.put(প্রবিষ্ট_মান.getKey(), 새서술자);
        }
        return পৰিমাপ;
    }

    private int খালী_ইনডেক্স(int 최소번호) {
        for (int ইনডেক্স = Math.max(0, 최소번호); ইনডেক্স < 최대서술자; ইনডেক্স++) {
            if (!서술자들.containsKey(Integer.valueOf(ইনডেক্স))) {
                return ইনডেক্স;
            }
        }
        return -1;
    }
}
