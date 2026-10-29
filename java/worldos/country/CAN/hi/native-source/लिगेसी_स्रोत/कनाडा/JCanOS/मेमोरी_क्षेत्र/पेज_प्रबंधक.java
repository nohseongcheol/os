// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package कनाडा.JCanOS.मेमोरी_क्षेत्र;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB पेज_मान 연결과 लिखें 시 복사를 제공한다. */
public final class पेज_प्रबंधक {
    public static final int पृष्ठ_आकार = 4096;

    private static final class पेज_मान {
        private byte[] आँकड़े = new byte[पृष्ठ_आकार];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class पता_स्थान {
        private final Map<Integer, पेज_मान> पेज_तालिका = new HashMap<Integer, पेज_मान>();
    }

    public पता_स्थान 새주소공간() {
        return new पता_स्थान();
    }

    public void मैप_पेज(पता_स्थान पता_क्षेत्र, int वर्चुअल_पता, boolean 쓰기가능) {
        int इंडेक्स = 쪽번호(वर्चुअल_पता);
        पेज_मान 새쪽 = new पेज_मान();
        새쪽.쓰기가능 = 쓰기가능;
        पता_क्षेत्र.पेज_तालिका.put(Integer.valueOf(इंडेक्स), 새쪽);
    }

    public पता_स्थान 쓰기시복사복제(पता_स्थान 원본) {
        पता_स्थान 복제본 = new पता_स्थान();
        for (Map.Entry<Integer, पेज_मान> एन्ट्री_मान : 원본.पेज_तालिका.entrySet()) {
            पेज_मान 공유쪽 = एन्ट्री_मान.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.पेज_तालिका.put(एन्ट्री_मान.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte पढें_बाइट_मान(पता_स्थान पता_क्षेत्र, int वर्चुअल_पता) {
        पेज_मान लक्ष्य = खोजें_पेज(पता_क्षेत्र, वर्चुअल_पता);
        return लक्ष्य.आँकड़े[Math.floorMod(वर्चुअल_पता, पृष्ठ_आकार)];
    }

    public void लिखना_बाइट_मान(पता_स्थान पता_क्षेत्र, int वर्चुअल_पता, byte मान) {
        int इंडेक्स = 쪽번호(वर्चुअल_पता);
        पेज_मान लक्ष्य = खोजें_पेज(पता_क्षेत्र, वर्चुअल_पता);
        if (!लक्ष्य.쓰기가능) {
            if (!लक्ष्य.쓰기시복사) {
                throw new IllegalStateException("पढ़ें 전용 쪽입니다.");
            }
            लक्ष्य = बनाएँ_निजी_पेज(पता_क्षेत्र, इंडेक्स, लक्ष्य);
        }
        लक्ष्य.आँकड़े[Math.floorMod(वर्चुअल_पता, पृष्ठ_आकार)] = मान;
    }

    public void निजी_श्रेणी_लिखना(पता_स्थान पता_क्षेत्र, int प्रारंभ_पता, int आकार) {
        if (आकार < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int समाप्त_करें_पता = Math.addExact(प्रारंभ_पता, आकार);
        for (int पता = प्रारंभ_पता; पता < समाप्त_करें_पता; पता = (쪽번호(पता) + 1) * पृष्ठ_आकार) {
            int इंडेक्स = 쪽번호(पता);
            पेज_मान लक्ष्य = खोजें_पेज(पता_क्षेत्र, पता);
            if (लक्ष्य.쓰기시복사) {
                बनाएँ_निजी_पेज(पता_क्षेत्र, इंडेक्स, लक्ष्य);
            } else {
                लक्ष्य.쓰기가능 = true;
            }
        }
    }

    public void श्रेणी_लिखना(पता_स्थान पता_क्षेत्र, int प्रारंभ_पता, byte[] आँकड़े) {
        for (int इंडेक्स = 0; इंडेक्स < आँकड़े.length; इंडेक्स++) {
            लिखना_बाइट_मान(पता_क्षेत्र, प्रारंभ_पता + इंडेक्स, आँकड़े[इंडेक्स]);
        }
    }

    private पेज_मान बनाएँ_निजी_पेज(पता_स्थान पता_क्षेत्र, int इंडेक्स, पेज_मान 공유쪽) {
        पेज_मान निजी_पेज = new पेज_मान();
        निजी_पेज.आँकड़े = Arrays.copyOf(공유쪽.आँकड़े, 공유쪽.आँकड़े.length);
        निजी_पेज.쓰기가능 = true;
        निजी_पेज.쓰기시복사 = false;
        공유쪽.참조수--;
        पता_क्षेत्र.पेज_तालिका.put(Integer.valueOf(इंडेक्स), निजी_पेज);
        return निजी_पेज;
    }

    private पेज_मान खोजें_पेज(पता_स्थान पता_क्षेत्र, int पता) {
        पेज_मान लक्ष्य = पता_क्षेत्र.पेज_तालिका.get(Integer.valueOf(쪽번호(पता)));
        if (लक्ष्य == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return लक्ष्य;
    }

    private int 쪽번호(int पता) {
        if (पता < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return पता / पृष्ठ_आकार;
    }
}

