// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package متحده_عرب_امارات.JAreOS.دوتنه_سېسټم;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 دوتنه 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final دوتنه_سېسټم.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(دوتنه_سېسټم.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final دوتنه_سېسټم دوتنه_سېسټم;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(دوتنه_سېسټم دوتنه_سېسټم) {
        this.دوتنه_سېسټم = دوتنه_سېسټم;
    }

    public int پرانيستل(String نوم) {
        دوتنه_سېسټم.열린파일 열린파일 = دوتنه_سېسټم.پرانيستل(نوم);
        if (열린파일 == null) {
            return -2;
        }
        int لړیال = 빈번호(3);
        if (لړیال < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(لړیال), new 서술자(열린파일));
        return لړیال;
    }

    public int لوستل(int لړیال, byte[] 받을곳, int کچ) {
        서술자 ننوت_ارزښت = 서술자들.get(Integer.valueOf(لړیال));
        if (ننوت_ارزښت == null) {
            return -9;
        }
        if (کچ < 0 || کچ > 받을곳.length) {
            return -22;
        }
        int 남음 = ننوت_ارزښت.열린파일.اومتوک.length - ننوت_ارزښت.열린파일.ځای;
        int 읽을크기 = Math.min(کچ, Math.max(남음, 0));
        System.arraycopy(ننوت_ارزښت.열린파일.اومتوک, ننوت_ارزښت.열린파일.ځای, 받을곳, 0, 읽을크기);
        ننوت_ارزښت.열린파일.ځای += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int لړیال, int 거리, int 기준) {
        서술자 ننوت_ارزښت = 서술자들.get(Integer.valueOf(لړیال));
        if (ننوت_ارزښت == null) {
            return -9;
        }
        int شاليد_ارزښت;
        if (기준 == 0) {
            شاليد_ارزښت = 0;
        } else if (기준 == 1) {
            شاليد_ارزښت = ننوت_ارزښت.열린파일.ځای;
        } else if (기준 == 2) {
            شاليد_ارزښت = ننوت_ارزښت.열린파일.اومتوک.length;
        } else {
            return -22;
        }
        int 새위치 = شاليد_ارزښت + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ننوت_ارزښت.열린파일.ځای = 새위치;
        return 새위치;
    }

    public int بندول(int لړیال) {
        서술자 ننوت_ارزښت = 서술자들.remove(Integer.valueOf(لړیال));
        if (ننوت_ارزښت == null) {
            return -9;
        }
        ننوت_ارزښت.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int لړیال, int 최소번호) {
        서술자 ننوت_ارزښت = 서술자들.get(Integer.valueOf(لړیال));
        if (ننوت_ارزښت == null) {
            return -9;
        }
        int 새번호 = 빈번호(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ننوت_ارزښت.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ننوت_ارزښت.열린파일));
        return 새번호;
    }

    public int 지정복제(int لړیال, int 새번호) {
        if (لړیال == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(لړیال)) ? لړیال : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(لړیال));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            بندول(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int لړیال, boolean ارزښت) {
        서술자 ننوت_ارزښت = 서술자들.get(Integer.valueOf(لړیال));
        if (ننوت_ارزښت == null) {
            return -9;
        }
        ننوت_ارزښت.실행시닫기 = ارزښت;
        return 0;
    }

    public int 실행시닫기값(int لړیال) {
        서술자 ننوت_ارزښت = 서술자들.get(Integer.valueOf(لړیال));
        if (ننوت_ارزښت == null) {
            return -9;
        }
        return ننوت_ارزښت.실행시닫기 ? 1 : 0;
    }

    public 파일정보 정보(int لړیال) {
        if (لړیال >= 0 && لړیال <= 2) {
            return new 파일정보(0, 0020666);
        }
        서술자 ننوت_ارزښت = 서술자들.get(Integer.valueOf(لړیال));
        if (ننوت_ارزښت == null) {
            return null;
        }
        return new 파일정보(ننوت_ارزښت.열린파일.اومتوک.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer لړیال : 번호들) {
            서술자 ننوت_ارزښت = 서술자들.get(لړیال);
            if (ننوت_ارزښت != null && ننوت_ارزښت.실행시닫기) {
                بندول(لړیال.intValue());
            }
        }
    }

    public boolean 열려있음(int لړیال) {
        return 서술자들.containsKey(Integer.valueOf(لړیال));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(دوتنه_سېسټم);
        for (Map.Entry<Integer, 서술자> ننوت_ارزښت : 서술자들.entrySet()) {
            ننوت_ارزښت.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ننوت_ارزښت.getValue().열린파일);
            새서술자.실행시닫기 = ننوت_ارزښت.getValue().실행시닫기;
            결과.서술자들.put(ننوت_ارزښت.getKey(), 새서술자);
        }
        return 결과;
    }

    private int 빈번호(int 최소번호) {
        for (int لړیال = Math.max(0, 최소번호); لړیال < 최대서술자; لړیال++) {
            if (!서술자들.containsKey(Integer.valueOf(لړیال))) {
                return لړیال;
            }
        }
        return -1;
    }
}
