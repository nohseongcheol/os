// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package কানাডা.JCanOS.ফাইল_পদ্ধতি;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 নথির_নাম 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ফাইল_পদ্ধতি.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ফাইল_পদ্ধতি.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ফাইল_পদ্ধতি ফাইল_পদ্ধতি;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ফাইল_পদ্ধতি ফাইল_পদ্ধতি) {
        this.ফাইল_পদ্ধতি = ফাইল_পদ্ধতি;
    }

    public int খুলুন(String নাম) {
        ফাইল_পদ্ধতি.열린파일 열린파일 = ফাইল_পদ্ধতি.খুলুন(নাম);
        if (열린파일 == null) {
            return -2;
        }
        int সূচি = খালি_সূচি(3);
        if (সূচি < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(সূচি), new 서술자(열린파일));
        return সূচি;
    }

    public int পড়া(int সূচি, byte[] 받을곳, int আকার) {
        서술자 ভুক্তি_মান = 서술자들.get(Integer.valueOf(সূচি));
        if (ভুক্তি_মান == null) {
            return -9;
        }
        if (আকার < 0 || আকার > 받을곳.length) {
            return -22;
        }
        int 남음 = ভুক্তি_মান.열린파일.ডাটা.length - ভুক্তি_মান.열린파일.অবস্থান;
        int 읽을크기 = Math.min(আকার, Math.max(남음, 0));
        System.arraycopy(ভুক্তি_মান.열린파일.ডাটা, ভুক্তি_মান.열린파일.অবস্থান, 받을곳, 0, 읽을크기);
        ভুক্তি_মান.열린파일.অবস্থান += 읽을크기;
        return 읽을크기;
    }

    public int অপসারণ_করা_পদ(int সূচি, int 거리, int প্রকল্প_মূল) {
        서술자 ভুক্তি_মান = 서술자들.get(Integer.valueOf(সূচি));
        if (ভুক্তি_মান == null) {
            return -9;
        }
        int পটভূমি_মান;
        if (প্রকল্প_মূল == 0) {
            পটভূমি_মান = 0;
        } else if (প্রকল্প_মূল == 1) {
            পটভূমি_মান = ভুক্তি_মান.열린파일.অবস্থান;
        } else if (প্রকল্প_মূল == 2) {
            পটভূমি_মান = ভুক্তি_মান.열린파일.ডাটা.length;
        } else {
            return -22;
        }
        int 새위치 = পটভূমি_মান + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ভুক্তি_মান.열린파일.অবস্থান = 새위치;
        return 새위치;
    }

    public int বন্ধ_করুন(int সূচি) {
        서술자 ভুক্তি_মান = 서술자들.remove(Integer.valueOf(সূচি));
        if (ভুক্তি_মান == null) {
            return -9;
        }
        ভুক্তি_মান.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int সূচি, int 최소번호) {
        서술자 ভুক্তি_মান = 서술자들.get(Integer.valueOf(সূচি));
        if (ভুক্তি_মান == null) {
            return -9;
        }
        int 새번호 = খালি_সূচি(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ভুক্তি_মান.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ভুক্তি_মান.열린파일));
        return 새번호;
    }

    public int 지정복제(int সূচি, int 새번호) {
        if (সূচি == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(সূচি)) ? সূচি : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(সূচি));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            বন্ধ_করুন(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int সূচি, boolean মান) {
        서술자 ভুক্তি_মান = 서술자들.get(Integer.valueOf(সূচি));
        if (ভুক্তি_মান == null) {
            return -9;
        }
        ভুক্তি_মান.실행시닫기 = মান;
        return 0;
    }

    public int 실행시닫기값(int সূচি) {
        서술자 ভুক্তি_মান = 서술자들.get(Integer.valueOf(সূচি));
        if (ভুক্তি_মান == null) {
            return -9;
        }
        return ভুক্তি_মান.실행시닫기 ? 1 : 0;
    }

    public ফাইল_তথ্য সিসটেম_তথ্য(int সূচি) {
        if (সূচি >= 0 && সূচি <= 2) {
            return new ফাইল_তথ্য(0, 0020666);
        }
        서술자 ভুক্তি_মান = 서술자들.get(Integer.valueOf(সূচি));
        if (ভুক্তি_মান == null) {
            return null;
        }
        return new ফাইল_তথ্য(ভুক্তি_মান.열린파일.ডাটা.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer সূচি : 번호들) {
            서술자 ভুক্তি_মান = 서술자들.get(সূচি);
            if (ভুক্তি_মান != null && ভুক্তি_মান.실행시닫기) {
                বন্ধ_করুন(সূচি.intValue());
            }
        }
    }

    public boolean তথ্য_প্রযুক্তি_খোলা(int সূচি) {
        return 서술자들.containsKey(Integer.valueOf(সূচি));
    }

    public 파일서술자표 복제() {
        파일서술자표 পরিমাপ = new 파일서술자표(ফাইল_পদ্ধতি);
        for (Map.Entry<Integer, 서술자> ভুক্তি_মান : 서술자들.entrySet()) {
            ভুক্তি_মান.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ভুক্তি_মান.getValue().열린파일);
            새서술자.실행시닫기 = ভুক্তি_মান.getValue().실행시닫기;
            পরিমাপ.서술자들.put(ভুক্তি_মান.getKey(), 새서술자);
        }
        return পরিমাপ;
    }

    private int খালি_সূচি(int 최소번호) {
        for (int সূচি = Math.max(0, 최소번호); সূচি < 최대서술자; সূচি++) {
            if (!서술자들.containsKey(Integer.valueOf(সূচি))) {
                return সূচি;
            }
        }
        return -1;
    }
}
