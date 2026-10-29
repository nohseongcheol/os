// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.ናይ_ፋይል_ስርዓት;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ፋይል 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ናይ_ፋይል_ስርዓት.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ናይ_ፋይል_ስርዓት.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ናይ_ፋይል_ስርዓት ናይ_ፋይል_ስርዓት;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ናይ_ፋይል_ስርዓት ናይ_ፋይል_ስርዓት) {
        this.ናይ_ፋይል_ስርዓት = ናይ_ፋይል_ስርዓት;
    }

    public int ክፈት(String ሽም) {
        ናይ_ፋይል_ስርዓት.열린파일 열린파일 = ናይ_ፋይል_ስርዓት.ክፈት(ሽም);
        if (열린파일 == null) {
            return -2;
        }
        int መሐበሪ = ባዶ_መሐበሪ(3);
        if (መሐበሪ < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(መሐበሪ), new 서술자(열린파일));
        return መሐበሪ;
    }

    public int 읽기(int መሐበሪ, byte[] 받을곳, int መጠን) {
        서술자 ምእታው_ዋጋ = 서술자들.get(Integer.valueOf(መሐበሪ));
        if (ምእታው_ዋጋ == null) {
            return -9;
        }
        if (መጠን < 0 || መጠን > 받을곳.length) {
            return -22;
        }
        int 남음 = ምእታው_ዋጋ.열린파일.ሓበሬታ.length - ምእታው_ዋጋ.열린파일.위치;
        int 읽을크기 = Math.min(መጠን, Math.max(남음, 0));
        System.arraycopy(ምእታው_ዋጋ.열린파일.ሓበሬታ, ምእታው_ዋጋ.열린파일.위치, 받을곳, 0, 읽을크기);
        ምእታው_ዋጋ.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int መሐበሪ, int 거리, int 기준) {
        서술자 ምእታው_ዋጋ = 서술자들.get(Integer.valueOf(መሐበሪ));
        if (ምእታው_ዋጋ == null) {
            return -9;
        }
        int ድሕረባይታ_ዋጋ;
        if (기준 == 0) {
            ድሕረባይታ_ዋጋ = 0;
        } else if (기준 == 1) {
            ድሕረባይታ_ዋጋ = ምእታው_ዋጋ.열린파일.위치;
        } else if (기준 == 2) {
            ድሕረባይታ_ዋጋ = ምእታው_ዋጋ.열린파일.ሓበሬታ.length;
        } else {
            return -22;
        }
        int 새위치 = ድሕረባይታ_ዋጋ + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ምእታው_ዋጋ.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int ዕጸው(int መሐበሪ) {
        서술자 ምእታው_ዋጋ = 서술자들.remove(Integer.valueOf(መሐበሪ));
        if (ምእታው_ዋጋ == null) {
            return -9;
        }
        ምእታው_ዋጋ.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int መሐበሪ, int 최소번호) {
        서술자 ምእታው_ዋጋ = 서술자들.get(Integer.valueOf(መሐበሪ));
        if (ምእታው_ዋጋ == null) {
            return -9;
        }
        int 새번호 = ባዶ_መሐበሪ(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ምእታው_ዋጋ.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ምእታው_ዋጋ.열린파일));
        return 새번호;
    }

    public int 지정복제(int መሐበሪ, int 새번호) {
        if (መሐበሪ == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(መሐበሪ)) ? መሐበሪ : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(መሐበሪ));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            ዕጸው(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int መሐበሪ, boolean ዋጋ) {
        서술자 ምእታው_ዋጋ = 서술자들.get(Integer.valueOf(መሐበሪ));
        if (ምእታው_ዋጋ == null) {
            return -9;
        }
        ምእታው_ዋጋ.실행시닫기 = ዋጋ;
        return 0;
    }

    public int 실행시닫기값(int መሐበሪ) {
        서술자 ምእታው_ዋጋ = 서술자들.get(Integer.valueOf(መሐበሪ));
        if (ምእታው_ዋጋ == null) {
            return -9;
        }
        return ምእታው_ዋጋ.실행시닫기 ? 1 : 0;
    }

    public ፋይል_ሓበሬታ ናይ_ስርዓት_ሓበሬታ(int መሐበሪ) {
        if (መሐበሪ >= 0 && መሐበሪ <= 2) {
            return new ፋይል_ሓበሬታ(0, 0020666);
        }
        서술자 ምእታው_ዋጋ = 서술자들.get(Integer.valueOf(መሐበሪ));
        if (ምእታው_ዋጋ == null) {
            return null;
        }
        return new ፋይል_ሓበሬታ(ምእታው_ዋጋ.열린파일.ሓበሬታ.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer መሐበሪ : 번호들) {
            서술자 ምእታው_ዋጋ = 서술자들.get(መሐበሪ);
            if (ምእታው_ዋጋ != null && ምእታው_ዋጋ.실행시닫기) {
                ዕጸው(መሐበሪ.intValue());
            }
        }
    }

    public boolean 열려있음(int መሐበሪ) {
        return 서술자들.containsKey(Integer.valueOf(መሐበሪ));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(ናይ_ፋይል_ስርዓት);
        for (Map.Entry<Integer, 서술자> ምእታው_ዋጋ : 서술자들.entrySet()) {
            ምእታው_ዋጋ.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ምእታው_ዋጋ.getValue().열린파일);
            새서술자.실행시닫기 = ምእታው_ዋጋ.getValue().실행시닫기;
            결과.서술자들.put(ምእታው_ዋጋ.getKey(), 새서술자);
        }
        return 결과;
    }

    private int ባዶ_መሐበሪ(int 최소번호) {
        for (int መሐበሪ = Math.max(0, 최소번호); መሐበሪ < 최대서술자; መሐበሪ++) {
            if (!서술자들.containsKey(Integer.valueOf(መሐበሪ))) {
                return መሐበሪ;
            }
        }
        return -1;
    }
}
