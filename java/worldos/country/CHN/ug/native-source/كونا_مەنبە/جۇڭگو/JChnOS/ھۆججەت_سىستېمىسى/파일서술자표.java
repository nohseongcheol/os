// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package جۇڭگو.JChnOS.ھۆججەت_سىستېمىسى;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ھۆججەت 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ھۆججەت_سىستېمىسى.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ھۆججەت_سىستېمىسى.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ھۆججەت_سىستېمىسى ھۆججەت_سىستېمىسى;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ھۆججەت_سىستېمىسى ھۆججەت_سىستېمىسى) {
        this.ھۆججەت_سىستېمىسى = ھۆججەت_سىستېمىسى;
    }

    public int ئاچ(String ئاتى) {
        ھۆججەت_سىستېمىسى.열린파일 열린파일 = ھۆججەت_سىستېمىسى.ئاچ(ئاتى);
        if (열린파일 == null) {
            return -2;
        }
        int ئىندېكس = بوش_ئىندېكس(3);
        if (ئىندېكس < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ئىندېكس), new 서술자(열린파일));
        return ئىندېكس;
    }

    public int ئوقۇ(int ئىندېكس, byte[] 받을곳, int چوڭلۇقى) {
        서술자 كىرگۈزۈش_قىممىتى = 서술자들.get(Integer.valueOf(ئىندېكس));
        if (كىرگۈزۈش_قىممىتى == null) {
            return -9;
        }
        if (چوڭلۇقى < 0 || چوڭلۇقى > 받을곳.length) {
            return -22;
        }
        int 남음 = كىرگۈزۈش_قىممىتى.열린파일.مەلۇمات.length - كىرگۈزۈش_قىممىتى.열린파일.ئورۇن;
        int 읽을크기 = Math.min(چوڭلۇقى, Math.max(남음, 0));
        System.arraycopy(كىرگۈزۈش_قىممىتى.열린파일.مەلۇمات, كىرگۈزۈش_قىممىتى.열린파일.ئورۇن, 받을곳, 0, 읽을크기);
        كىرگۈزۈش_قىممىتى.열린파일.ئورۇن += 읽을크기;
        return 읽을크기;
    }

    public int يۆتكىمەك_ئورۇنلاشتۇرۇش(int ئىندېكس, int 거리, int كۆرسىتىش_يىلتىز) {
        서술자 كىرگۈزۈش_قىممىتى = 서술자들.get(Integer.valueOf(ئىندېكس));
        if (كىرگۈزۈش_قىممىتى == null) {
            return -9;
        }
        int تەگلىك_قىممىتى;
        if (كۆرسىتىش_يىلتىز == 0) {
            تەگلىك_قىممىتى = 0;
        } else if (كۆرسىتىش_يىلتىز == 1) {
            تەگلىك_قىممىتى = كىرگۈزۈش_قىممىتى.열린파일.ئورۇن;
        } else if (كۆرسىتىش_يىلتىز == 2) {
            تەگلىك_قىممىتى = كىرگۈزۈش_قىممىتى.열린파일.مەلۇمات.length;
        } else {
            return -22;
        }
        int 새위치 = تەگلىك_قىممىتى + 거리;
        if (새위치 < 0) {
            return -22;
        }
        كىرگۈزۈش_قىممىتى.열린파일.ئورۇن = 새위치;
        return 새위치;
    }

    public int ياپ(int ئىندېكس) {
        서술자 كىرگۈزۈش_قىممىتى = 서술자들.remove(Integer.valueOf(ئىندېكس));
        if (كىرگۈزۈش_قىممىتى == null) {
            return -9;
        }
        كىرگۈزۈش_قىممىتى.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int ئىندېكس, int 최소번호) {
        서술자 كىرگۈزۈش_قىممىتى = 서술자들.get(Integer.valueOf(ئىندېكس));
        if (كىرگۈزۈش_قىممىتى == null) {
            return -9;
        }
        int 새번호 = بوش_ئىندېكس(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        كىرگۈزۈش_قىممىتى.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(كىرگۈزۈش_قىممىتى.열린파일));
        return 새번호;
    }

    public int 지정복제(int ئىندېكس, int 새번호) {
        if (ئىندېكس == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(ئىندېكس)) ? ئىندېكس : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ئىندېكس));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            ياپ(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int ئىندېكس, boolean قىممىتى) {
        서술자 كىرگۈزۈش_قىممىتى = 서술자들.get(Integer.valueOf(ئىندېكس));
        if (كىرگۈزۈش_قىممىتى == null) {
            return -9;
        }
        كىرگۈزۈش_قىممىتى.실행시닫기 = قىممىتى;
        return 0;
    }

    public int 실행시닫기값(int ئىندېكس) {
        서술자 كىرگۈزۈش_قىممىتى = 서술자들.get(Integer.valueOf(ئىندېكس));
        if (كىرگۈزۈش_قىممىتى == null) {
            return -9;
        }
        return كىرگۈزۈش_قىممىتى.실행시닫기 ? 1 : 0;
    }

    public ھۆججەت_ئۇچۇر سىستېما_ئۇچۇرى(int ئىندېكس) {
        if (ئىندېكس >= 0 && ئىندېكس <= 2) {
            return new ھۆججەت_ئۇچۇر(0, 0020666);
        }
        서술자 كىرگۈزۈش_قىممىتى = 서술자들.get(Integer.valueOf(ئىندېكس));
        if (كىرگۈزۈش_قىممىتى == null) {
            return null;
        }
        return new ھۆججەت_ئۇچۇر(كىرگۈزۈش_قىممىتى.열린파일.مەلۇمات.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ئىندېكس : 번호들) {
            서술자 كىرگۈزۈش_قىممىتى = 서술자들.get(ئىندېكس);
            if (كىرگۈزۈش_قىممىتى != null && كىرگۈزۈش_قىممىتى.실행시닫기) {
                ياپ(ئىندېكس.intValue());
            }
        }
    }

    public boolean 열려있음(int ئىندېكس) {
        return 서술자들.containsKey(Integer.valueOf(ئىندېكس));
    }

    public 파일서술자표 복제() {
        파일서술자표 ئۆلچەم = new 파일서술자표(ھۆججەت_سىستېمىسى);
        for (Map.Entry<Integer, 서술자> كىرگۈزۈش_قىممىتى : 서술자들.entrySet()) {
            كىرگۈزۈش_قىممىتى.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(كىرگۈزۈش_قىممىتى.getValue().열린파일);
            새서술자.실행시닫기 = كىرگۈزۈش_قىممىتى.getValue().실행시닫기;
            ئۆلچەم.서술자들.put(كىرگۈزۈش_قىممىتى.getKey(), 새서술자);
        }
        return ئۆلچەم;
    }

    private int بوش_ئىندېكس(int 최소번호) {
        for (int ئىندېكس = Math.max(0, 최소번호); ئىندېكس < 최대서술자; ئىندېكس++) {
            if (!서술자들.containsKey(Integer.valueOf(ئىندېكس))) {
                return ئىندېكس;
            }
        }
        return -1;
    }
}
