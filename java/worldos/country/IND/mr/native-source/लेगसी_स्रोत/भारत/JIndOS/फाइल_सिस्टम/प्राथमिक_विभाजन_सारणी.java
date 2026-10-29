// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.फाइल_सिस्टम;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR मधील चार प्राथमिक विभाग वाचते. */
public final class प्राथमिक_विभाजन_सारणी {
    public static final class विभाजन_मूल्य {
        private final int प्रकार_मूल्य;
        private final long प्रारंभ_विभाग;
        private final long विभाग_संख्या;

        विभाजन_मूल्य(int प्रकार_मूल्य, long प्रारंभ_विभाग, long विभाग_संख्या) {
            this.प्रकार_मूल्य = प्रकार_मूल्य;
            this.प्रारंभ_विभाग = प्रारंभ_विभाग;
            this.विभाग_संख्या = विभाग_संख्या;
        }

        public int प्रकार_मूल्य() { return प्रकार_मूल्य; }
        public long प्रारंभ_विभाग() { return प्रारंभ_विभाग; }
        public long विभाग_संख्या() { return विभाग_संख्या; }
    }

    public List<विभाजन_मूल्य> वाचन(byte[] पहिले_विभाग) {
        if (पहिले_विभाग == null || पहिले_विभाग.length < 512
                || (पहिले_विभाग[510] & 0xff) != 0x55 || (पहिले_विभाग[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<विभाजन_मूल्य> मोजमाप = new ArrayList<विभाजन_मूल्य>();
        for (int अनुक्रमणिका = 0; अनुक्रमणिका < 4; अनुक्रमणिका++) {
            int जागा = 446 + अनुक्रमणिका * 16;
            int प्रकार_मूल्य = पहिले_विभाग[जागा + 4] & 0xff;
            long सुरू_करा = लहान_बाइटक्रम_पूर्णांक(पहिले_विभाग, जागा + 8);
            long आकार = लहान_बाइटक्रम_पूर्णांक(पहिले_विभाग, जागा + 12);
            if (प्रकार_मूल्य != 0 && आकार != 0) {
                मोजमाप.add(new विभाजन_मूल्य(प्रकार_मूल्य, सुरू_करा, आकार));
            }
        }
        return Collections.unmodifiableList(मोजमाप);
    }

    private long लहान_बाइटक्रम_पूर्णांक(byte[] डेटा, int जागा) {
        return (डेटा[जागा] & 0xffL)
                | ((डेटा[जागा + 1] & 0xffL) << 8)
                | ((डेटा[जागा + 2] & 0xffL) << 16)
                | ((डेटा[जागा + 3] & 0xffL) << 24);
    }
}

