// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB पान_मोल 연결과 बरोवचें 시 복사를 제공한다. */
public final class पान_वेवस्थापक {
    public static final int पानाचो_आंवाठ = 4096;

    private static final class पान_मोल {
        private byte[] डेटा = new byte[पानाचो_आंवाठ];
        private int संदर्भ_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class नामो_SPACE {
        private final Map<Integer, पान_मोल> पान_तकटो = new HashMap<Integer, पान_मोल>();
    }

    public नामो_SPACE 새주소공간() {
        return new नामो_SPACE();
    }

    public void नकसो_पान(नामो_SPACE 공간, int व्हर्चुअल_नामो, boolean 쓰기가능) {
        int INDEX = 쪽번호(व्हर्चुअल_नामो);
        पान_मोल 새쪽 = new पान_मोल();
        새쪽.쓰기가능 = 쓰기가능;
        공간.पान_तकटो.put(Integer.valueOf(INDEX), 새쪽);
    }

    public नामो_SPACE 쓰기시복사복제(नामो_SPACE 원본) {
        नामो_SPACE 복제본 = new नामो_SPACE();
        for (Map.Entry<Integer, पान_मोल> प्रवेश_मोल : 원본.पान_तकटो.entrySet()) {
            पान_मोल 공유쪽 = प्रवेश_मोल.getValue();
            공유쪽.संदर्भ_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.पान_तकटो.put(प्रवेश_मोल.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(नामो_SPACE 공간, int व्हर्चुअल_नामो) {
        पान_मोल लक्ष्य = FIND_पान(공간, व्हर्चुअल_नामो);
        return लक्ष्य.डेटा[Math.floorMod(व्हर्चुअल_नामो, पानाचो_आंवाठ)];
    }

    public void बरोवचें_बायट_मोल(नामो_SPACE 공간, int व्हर्चुअल_नामो, byte मोल) {
        int INDEX = 쪽번호(व्हर्चुअल_नामो);
        पान_मोल लक्ष्य = FIND_पान(공간, व्हर्चुअल_नामो);
        if (!लक्ष्य.쓰기가능) {
            if (!लक्ष्य.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            लक्ष्य = निर्माण_करचें_खाजगी_पान(공간, INDEX, लक्ष्य);
        }
        लक्ष्य.डेटा[Math.floorMod(व्हर्चुअल_नामो, पानाचो_आंवाठ)] = मोल;
    }

    public void 범위개인쓰기(नामो_SPACE 공간, int Start_नामो, int आवाठ) {
        if (आवाठ < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int सोपोवचें_नामो = Math.addExact(Start_नामो, आवाठ);
        for (int नामो = Start_नामो; नामो < सोपोवचें_नामो; नामो = (쪽번호(नामो) + 1) * पानाचो_आंवाठ) {
            int INDEX = 쪽번호(नामो);
            पान_मोल लक्ष्य = FIND_पान(공간, नामो);
            if (लक्ष्य.쓰기시복사) {
                निर्माण_करचें_खाजगी_पान(공간, INDEX, लक्ष्य);
            } else {
                लक्ष्य.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(नामो_SPACE 공간, int Start_नामो, byte[] डेटा) {
        for (int INDEX = 0; INDEX < डेटा.length; INDEX++) {
            बरोवचें_बायट_मोल(공간, Start_नामो + INDEX, डेटा[INDEX]);
        }
    }

    private पान_मोल निर्माण_करचें_खाजगी_पान(नामो_SPACE 공간, int INDEX, पान_मोल 공유쪽) {
        पान_मोल खाजगी_पान = new पान_मोल();
        खाजगी_पान.डेटा = Arrays.copyOf(공유쪽.डेटा, 공유쪽.डेटा.length);
        खाजगी_पान.쓰기가능 = true;
        खाजगी_पान.쓰기시복사 = false;
        공유쪽.संदर्भ_COUNT--;
        공간.पान_तकटो.put(Integer.valueOf(INDEX), खाजगी_पान);
        return खाजगी_पान;
    }

    private पान_मोल FIND_पान(नामो_SPACE 공간, int नामो) {
        पान_मोल लक्ष्य = 공간.पान_तकटो.get(Integer.valueOf(쪽번호(नामो)));
        if (लक्ष्य == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return लक्ष्य;
    }

    private int 쪽번호(int नामो) {
        if (नामो < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return नामो / पानाचो_आंवाठ;
    }
}

