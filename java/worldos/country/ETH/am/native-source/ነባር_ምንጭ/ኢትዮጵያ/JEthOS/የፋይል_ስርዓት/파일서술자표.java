// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.የፋይል_ስርዓት;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ፋይል 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final የፋይል_ስርዓት.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(የፋይል_ስርዓት.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final የፋይል_ስርዓት የፋይል_ስርዓት;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(የፋይል_ስርዓት የፋይል_ስርዓት) {
        this.የፋይል_ስርዓት = የፋይል_ስርዓት;
    }

    public int መክፈቻ(String ስም) {
        የፋይል_ስርዓት.열린파일 열린파일 = የፋይል_ስርዓት.መክፈቻ(ስም);
        if (열린파일 == null) {
            return -2;
        }
        int መረጃ_ጠቆመ = ባዶ_መረጃ_ጠቆመ(3);
        if (መረጃ_ጠቆመ < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(መረጃ_ጠቆመ), new 서술자(열린파일));
        return መረጃ_ጠቆመ;
    }

    public int ማንበቢያ(int መረጃ_ጠቆመ, byte[] 받을곳, int መጠን) {
        서술자 ምዝግብ_እሴት = 서술자들.get(Integer.valueOf(መረጃ_ጠቆመ));
        if (ምዝግብ_እሴት == null) {
            return -9;
        }
        if (መጠን < 0 || መጠን > 받을곳.length) {
            return -22;
        }
        int 남음 = ምዝግብ_እሴት.열린파일.ውሂብ.length - ምዝግብ_እሴት.열린파일.አካባቢ;
        int 읽을크기 = Math.min(መጠን, Math.max(남음, 0));
        System.arraycopy(ምዝግብ_እሴት.열린파일.ውሂብ, ምዝግብ_እሴት.열린파일.አካባቢ, 받을곳, 0, 읽을크기);
        ምዝግብ_እሴት.열린파일.አካባቢ += 읽을크기;
        return 읽을크기;
    }

    public int አንቀሳቅስ_በቦታ_አስቀመጠ(int መረጃ_ጠቆመ, int 거리, int አሳይ_ስር) {
        서술자 ምዝግብ_እሴት = 서술자들.get(Integer.valueOf(መረጃ_ጠቆመ));
        if (ምዝግብ_እሴት == null) {
            return -9;
        }
        int ልጣፍ_እሴት;
        if (አሳይ_ስር == 0) {
            ልጣፍ_እሴት = 0;
        } else if (አሳይ_ስር == 1) {
            ልጣፍ_እሴት = ምዝግብ_እሴት.열린파일.አካባቢ;
        } else if (አሳይ_ስር == 2) {
            ልጣፍ_እሴት = ምዝግብ_እሴት.열린파일.ውሂብ.length;
        } else {
            return -22;
        }
        int 새위치 = ልጣፍ_እሴት + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ምዝግብ_እሴት.열린파일.አካባቢ = 새위치;
        return 새위치;
    }

    public int መዝጊያ(int መረጃ_ጠቆመ) {
        서술자 ምዝግብ_እሴት = 서술자들.remove(Integer.valueOf(መረጃ_ጠቆመ));
        if (ምዝግብ_እሴት == null) {
            return -9;
        }
        ምዝግብ_እሴት.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int መረጃ_ጠቆመ, int 최소번호) {
        서술자 ምዝግብ_እሴት = 서술자들.get(Integer.valueOf(መረጃ_ጠቆመ));
        if (ምዝግብ_እሴት == null) {
            return -9;
        }
        int 새번호 = ባዶ_መረጃ_ጠቆመ(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ምዝግብ_እሴት.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ምዝግብ_እሴት.열린파일));
        return 새번호;
    }

    public int 지정복제(int መረጃ_ጠቆመ, int 새번호) {
        if (መረጃ_ጠቆመ == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(መረጃ_ጠቆመ)) ? መረጃ_ጠቆመ : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(መረጃ_ጠቆመ));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            መዝጊያ(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int መረጃ_ጠቆመ, boolean እሴት) {
        서술자 ምዝግብ_እሴት = 서술자들.get(Integer.valueOf(መረጃ_ጠቆመ));
        if (ምዝግብ_እሴት == null) {
            return -9;
        }
        ምዝግብ_እሴት.실행시닫기 = እሴት;
        return 0;
    }

    public int 실행시닫기값(int መረጃ_ጠቆመ) {
        서술자 ምዝግብ_እሴት = 서술자들.get(Integer.valueOf(መረጃ_ጠቆመ));
        if (ምዝግብ_እሴት == null) {
            return -9;
        }
        return ምዝግብ_እሴት.실행시닫기 ? 1 : 0;
    }

    public ፋይል_መረጃ የስርዓት_መረጃ(int መረጃ_ጠቆመ) {
        if (መረጃ_ጠቆመ >= 0 && መረጃ_ጠቆመ <= 2) {
            return new ፋይል_መረጃ(0, 0020666);
        }
        서술자 ምዝግብ_እሴት = 서술자들.get(Integer.valueOf(መረጃ_ጠቆመ));
        if (ምዝግብ_እሴት == null) {
            return null;
        }
        return new ፋይል_መረጃ(ምዝግብ_እሴት.열린파일.ውሂብ.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer መረጃ_ጠቆመ : 번호들) {
            서술자 ምዝግብ_እሴት = 서술자들.get(መረጃ_ጠቆመ);
            if (ምዝግብ_እሴት != null && ምዝግብ_እሴት.실행시닫기) {
                መዝጊያ(መረጃ_ጠቆመ.intValue());
            }
        }
    }

    public boolean የመረጃ_ቴክኖሎጂ_ክፈት(int መረጃ_ጠቆመ) {
        return 서술자들.containsKey(Integer.valueOf(መረጃ_ጠቆመ));
    }

    public 파일서술자표 복제() {
        파일서술자표 ልኬት = new 파일서술자표(የፋይል_ስርዓት);
        for (Map.Entry<Integer, 서술자> ምዝግብ_እሴት : 서술자들.entrySet()) {
            ምዝግብ_እሴት.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ምዝግብ_እሴት.getValue().열린파일);
            새서술자.실행시닫기 = ምዝግብ_እሴት.getValue().실행시닫기;
            ልኬት.서술자들.put(ምዝግብ_እሴት.getKey(), 새서술자);
        }
        return ልኬት;
    }

    private int ባዶ_መረጃ_ጠቆመ(int 최소번호) {
        for (int መረጃ_ጠቆመ = Math.max(0, 최소번호); መረጃ_ጠቆመ < 최대서술자; መረጃ_ጠቆመ++) {
            if (!서술자들.containsKey(Integer.valueOf(መረጃ_ጠቆመ))) {
                return መረጃ_ጠቆመ;
            }
        }
        return -1;
    }
}
