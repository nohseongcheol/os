// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.फाइल_सिस्टम;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT वाचनस्तराशी जुळणाऱ्या केवळ-वाचन संचिकासाठ्याचे व्यवस्थापित प्रतिरूप. */
public final class फाइल_सिस्टम {
    static final class उघडलेले_संचिका {
        final byte[] डेटा;
        int जागा;
        int संदर्भ_संख्या = 1;

        उघडलेले_संचिका(byte[] डेटा) {
            this.डेटा = डेटा;
        }
    }

    private final Map<String, byte[]> संचिका_नोंदी = new LinkedHashMap<String, byte[]>();

    public void शेवटीजोडा_संचिका(String नाव, byte[] डेटा) {
        संचिका_नोंदी.put(प्रमाणरूप_नाव(नाव), Arrays.copyOf(डेटा, डेटा.length));
    }

    उघडलेले_संचिका उघडा(String नाव) {
        byte[] डेटा = संचिका_नोंदी.get(प्रमाणरूप_नाव(नाव));
        if (डेटा == null) {
            return null;
        }
        return new उघडलेले_संचिका(डेटा);
    }

    public boolean अस्तित्वातआहे_मूल्य(String नाव) {
        return संचिका_नोंदी.containsKey(प्रमाणरूप_नाव(नाव));
    }

    public संचिका_माहिती सिस्टम_माहिती(String नाव) {
        byte[] डेटा = संचिका_नोंदी.get(प्रमाणरूप_नाव(नाव));
        if (डेटा == null) {
            return null;
        }
        return new संचिका_माहिती(डेटा.length, 0100444);
    }

    private String प्रमाणरूप_नाव(String नाव) {
        if (नाव == null) {
            throw new NullPointerException("फाइल 이름이 없습니다.");
        }
        String मोजमाप = नाव.startsWith("/") ? नाव.substring(1) : नाव;
        return मोजमाप.toUpperCase(Locale.ROOT);
    }
}
