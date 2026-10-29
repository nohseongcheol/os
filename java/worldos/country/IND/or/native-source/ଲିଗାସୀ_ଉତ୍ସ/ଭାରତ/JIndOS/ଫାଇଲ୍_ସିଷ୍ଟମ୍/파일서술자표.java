// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.ଫାଇଲ୍_ସିଷ୍ଟମ୍;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ଫାଇଲ 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ଫାଇଲ୍_ସିଷ୍ଟମ୍.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ଫାଇଲ୍_ସିଷ୍ଟମ୍.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ଫାଇଲ୍_ସିଷ୍ଟମ୍ ଫାଇଲ୍_ସିଷ୍ଟମ୍;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ଫାଇଲ୍_ସିଷ୍ଟମ୍ ଫାଇଲ୍_ସିଷ୍ଟମ୍) {
        this.ଫାଇଲ୍_ସିଷ୍ଟମ୍ = ଫାଇଲ୍_ସିଷ୍ଟମ୍;
    }

    public int ଖୋଲନ୍ତୁ(String ନାମ) {
        ଫାଇଲ୍_ସିଷ୍ଟମ୍.열린파일 열린파일 = ଫାଇଲ୍_ସିଷ୍ଟମ୍.ଖୋଲନ୍ତୁ(ନାମ);
        if (열린파일 == null) {
            return -2;
        }
        int ଅନୁକ୍ରମଣିକା = ଖାଲି_ଅନୁକ୍ରମଣିକା(3);
        if (ଅନୁକ୍ରମଣିକା < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ଅନୁକ୍ରମଣିକା), new 서술자(열린파일));
        return ଅନୁକ୍ରମଣିକା;
    }

    public int ପଢନ୍ତୁ(int ଅନୁକ୍ରମଣିକା, byte[] 받을곳, int ଆକାର) {
        서술자 ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = 서술자들.get(Integer.valueOf(ଅନୁକ୍ରମଣିକା));
        if (ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ == null) {
            return -9;
        }
        if (ଆକାର < 0 || ଆକାର > 받을곳.length) {
            return -22;
        }
        int 남음 = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일.ଡାଟା.length - ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일.ଅବସ୍ଥାନ;
        int 읽을크기 = Math.min(ଆକାର, Math.max(남음, 0));
        System.arraycopy(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일.ଡାଟା, ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일.ଅବସ୍ଥାନ, 받을곳, 0, 읽을크기);
        ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일.ଅବସ୍ଥାନ += 읽을크기;
        return 읽을크기;
    }

    public int ଘୁଞ୍ଚାଇବା_ସ୍ଥିତି(int ଅନୁକ୍ରମଣିକା, int 거리, int ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍) {
        서술자 ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = 서술자들.get(Integer.valueOf(ଅନୁକ୍ରମଣିକା));
        if (ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ == null) {
            return -9;
        }
        int ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ;
        if (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ == 0) {
            ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ = 0;
        } else if (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ == 1) {
            ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일.ଅବସ୍ଥାନ;
        } else if (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ == 2) {
            ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일.ଡାଟା.length;
        } else {
            return -22;
        }
        int 새위치 = ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일.ଅବସ୍ଥାନ = 새위치;
        return 새위치;
    }

    public int ବନ୍ଦ_କରନ୍ତୁ(int ଅନୁକ୍ରମଣିକା) {
        서술자 ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = 서술자들.remove(Integer.valueOf(ଅନୁକ୍ରମଣିକା));
        if (ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ == null) {
            return -9;
        }
        ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int ଅନୁକ୍ରମଣିକା, int 최소번호) {
        서술자 ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = 서술자들.get(Integer.valueOf(ଅନୁକ୍ରମଣିକା));
        if (ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ == null) {
            return -9;
        }
        int 새번호 = ଖାଲି_ଅନୁକ୍ରମଣିକା(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일));
        return 새번호;
    }

    public int 지정복제(int ଅନୁକ୍ରମଣିକା, int 새번호) {
        if (ଅନୁକ୍ରମଣିକା == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(ଅନୁକ୍ରମଣିକା)) ? ଅନୁକ୍ରମଣିକା : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ଅନୁକ୍ରମଣିକା));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            ବନ୍ଦ_କରନ୍ତୁ(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int ଅନୁକ୍ରମଣିକା, boolean ମୂଲ୍ୟ) {
        서술자 ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = 서술자들.get(Integer.valueOf(ଅନୁକ୍ରମଣିକା));
        if (ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ == null) {
            return -9;
        }
        ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.실행시닫기 = ମୂଲ୍ୟ;
        return 0;
    }

    public int 실행시닫기값(int ଅନୁକ୍ରମଣିକା) {
        서술자 ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = 서술자들.get(Integer.valueOf(ଅନୁକ୍ରମଣିକା));
        if (ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ == null) {
            return -9;
        }
        return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.실행시닫기 ? 1 : 0;
    }

    public ଫାଇଲ୍_ସୂଚନା ସିଷ୍ଟମ୍_ସୂଚନା(int ଅନୁକ୍ରମଣିକା) {
        if (ଅନୁକ୍ରମଣିକା >= 0 && ଅନୁକ୍ରମଣିକା <= 2) {
            return new ଫାଇଲ୍_ସୂଚନା(0, 0020666);
        }
        서술자 ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = 서술자들.get(Integer.valueOf(ଅନୁକ୍ରମଣିକା));
        if (ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ == null) {
            return null;
        }
        return new ଫାଇଲ୍_ସୂଚନା(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.열린파일.ଡାଟା.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ଅନୁକ୍ରମଣିକା : 번호들) {
            서술자 ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = 서술자들.get(ଅନୁକ୍ରମଣିକା);
            if (ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ != null && ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.실행시닫기) {
                ବନ୍ଦ_କରନ୍ତୁ(ଅନୁକ୍ରମଣିକା.intValue());
            }
        }
    }

    public boolean ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଖୋଲିବା(int ଅନୁକ୍ରମଣିକା) {
        return 서술자들.containsKey(Integer.valueOf(ଅନୁକ୍ରମଣିକା));
    }

    public 파일서술자표 복제() {
        파일서술자표 ମାପ = new 파일서술자표(ଫାଇଲ୍_ସିଷ୍ଟମ୍);
        for (Map.Entry<Integer, 서술자> ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ : 서술자들.entrySet()) {
            ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.getValue().열린파일);
            새서술자.실행시닫기 = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.getValue().실행시닫기;
            ମାପ.서술자들.put(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.getKey(), 새서술자);
        }
        return ମାପ;
    }

    private int ଖାଲି_ଅନୁକ୍ରମଣିକା(int 최소번호) {
        for (int ଅନୁକ୍ରମଣିକା = Math.max(0, 최소번호); ଅନୁକ୍ରମଣିକା < 최대서술자; ଅନୁକ୍ରମଣିକା++) {
            if (!서술자들.containsKey(Integer.valueOf(ଅନୁକ୍ରମଣିକା))) {
                return ଅନୁକ୍ରମଣିକା;
            }
        }
        return -1;
    }
}
