// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.फायल_प्रणाली;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 फायल 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final फायल_प्रणाली.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(फायल_प्रणाली.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final फायल_प्रणाली फायल_प्रणाली;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(फायल_प्रणाली फायल_प्रणाली) {
        this.फायल_प्रणाली = फायल_प्रणाली;
    }

    public int उगडचें(String नांव) {
        फायल_प्रणाली.열린파일 열린파일 = फायल_प्रणाली.उगडचें(नांव);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = रिकामें_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int 읽기(int INDEX, byte[] 받을곳, int आवाठ) {
        서술자 प्रवेश_मोल = 서술자들.get(Integer.valueOf(INDEX));
        if (प्रवेश_मोल == null) {
            return -9;
        }
        if (आवाठ < 0 || आवाठ > 받을곳.length) {
            return -22;
        }
        int 남음 = प्रवेश_मोल.열린파일.डेटा.length - प्रवेश_मोल.열린파일.स्थिती;
        int 읽을크기 = Math.min(आवाठ, Math.max(남음, 0));
        System.arraycopy(प्रवेश_मोल.열린파일.डेटा, प्रवेश_मोल.열린파일.स्थिती, 받을곳, 0, 읽을크기);
        प्रवेश_मोल.열린파일.स्थिती += 읽을크기;
        return 읽을크기;
    }

    public int हालोवचें_स्थिती(int INDEX, int 거리, int प्रॉजॅक्ट_रूट) {
        서술자 प्रवेश_मोल = 서술자들.get(Integer.valueOf(INDEX));
        if (प्रवेश_मोल == null) {
            return -9;
        }
        int फाटभूंय_मोल;
        if (प्रॉजॅक्ट_रूट == 0) {
            फाटभूंय_मोल = 0;
        } else if (प्रॉजॅक्ट_रूट == 1) {
            फाटभूंय_मोल = प्रवेश_मोल.열린파일.स्थिती;
        } else if (प्रॉजॅक्ट_रूट == 2) {
            फाटभूंय_मोल = प्रवेश_मोल.열린파일.डेटा.length;
        } else {
            return -22;
        }
        int 새위치 = फाटभूंय_मोल + 거리;
        if (새위치 < 0) {
            return -22;
        }
        प्रवेश_मोल.열린파일.स्थिती = 새위치;
        return 새위치;
    }

    public int शेवट(int INDEX) {
        서술자 प्रवेश_मोल = 서술자들.remove(Integer.valueOf(INDEX));
        if (प्रवेश_मोल == null) {
            return -9;
        }
        प्रवेश_मोल.열린파일.संदर्भ_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 प्रवेश_मोल = 서술자들.get(Integer.valueOf(INDEX));
        if (प्रवेश_मोल == null) {
            return -9;
        }
        int 새번호 = रिकामें_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        प्रवेश_मोल.열린파일.संदर्भ_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(प्रवेश_मोल.열린파일));
        return 새번호;
    }

    public int 지정복제(int INDEX, int 새번호) {
        if (INDEX == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            शेवट(새번호);
        }
        원본.열린파일.संदर्भ_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean मोल) {
        서술자 प्रवेश_मोल = 서술자들.get(Integer.valueOf(INDEX));
        if (प्रवेश_मोल == null) {
            return -9;
        }
        प्रवेश_मोल.실행시닫기 = मोल;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 प्रवेश_मोल = 서술자들.get(Integer.valueOf(INDEX));
        if (प्रवेश_मोल == null) {
            return -9;
        }
        return प्रवेश_मोल.실행시닫기 ? 1 : 0;
    }

    public फायल_म्हायती msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new फायल_म्हायती(0, 0020666);
        }
        서술자 प्रवेश_मोल = 서술자들.get(Integer.valueOf(INDEX));
        if (प्रवेश_मोल == null) {
            return null;
        }
        return new फायल_म्हायती(प्रवेश_मोल.열린파일.डेटा.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 प्रवेश_मोल = 서술자들.get(INDEX);
            if (प्रवेश_मोल != null && प्रवेश_मोल.실행시닫기) {
                शेवट(INDEX.intValue());
            }
        }
    }

    public boolean 열려있음(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 मेजप = new 파일서술자표(फायल_प्रणाली);
        for (Map.Entry<Integer, 서술자> प्रवेश_मोल : 서술자들.entrySet()) {
            प्रवेश_मोल.getValue().열린파일.संदर्भ_COUNT++;
            서술자 새서술자 = new 서술자(प्रवेश_मोल.getValue().열린파일);
            새서술자.실행시닫기 = प्रवेश_मोल.getValue().실행시닫기;
            मेजप.서술자들.put(प्रवेश_मोल.getKey(), 새서술자);
        }
        return मेजप;
    }

    private int रिकामें_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
