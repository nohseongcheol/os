// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.विवरणक_प्रविष्टी;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 जागतिक वर्णक तक्ता आणि कार्यस्थिती विभागाच्या मांडण्या राखते. */
public final class सर्वंकष_विवरणक_सारणी {
    public static final class तुकडा_मूल्य {
        private final int वॉलपेपर_मूल्य;
        private final int सीमा_मर्यादा;
        private final int ऍक्सेस_मूल्य;

        तुकडा_मूल्य(int वॉलपेपर_मूल्य, int सीमा_मर्यादा, int ऍक्सेस_मूल्य) {
            this.वॉलपेपर_मूल्य = वॉलपेपर_मूल्य;
            this.सीमा_मर्यादा = सीमा_मर्यादा;
            this.ऍक्सेस_मूल्य = ऍक्सेस_मूल्य;
        }

        public int वॉलपेपर_मूल्य() { return वॉलपेपर_मूल्य; }
        public int सीमा_मर्यादा() { return सीमा_मर्यादा; }
        public int ऍक्सेस_मूल्य() { return ऍक्सेस_मूल्य; }
    }

    private final List<तुकडा_मूल्य> तुकडे_यादी = new ArrayList<तुकडा_मूल्य>();

    public int शेवटीजोडा_प्रविष्टी(int वॉलपेपर_मूल्य, int सीमा_मर्यादा, int ऍक्सेस_मूल्य) {
        तुकडे_यादी.add(new तुकडा_मूल्य(वॉलपेपर_मूल्य, सीमा_मर्यादा, ऍक्सेस_मूल्य));
        return (तुकडे_यादी.size() - 1) * 8;
    }

    public List<तुकडा_मूल्य> तुकडे_यादी() {
        return Collections.unmodifiableList(तुकडे_यादी);
    }

    public void डिफॉल्ट_मूल्य_संच() {
        तुकडे_यादी.clear();
        शेवटीजोडा_प्रविष्टी(0, 0, 0);
        शेवटीजोडा_प्रविष्टी(0, 0xfffff, 0x9a);
        शेवटीजोडा_प्रविष्टी(0, 0xfffff, 0x92);
        शेवटीजोडा_प्रविष्टी(0, 0xfffff, 0xfa);
        शेवटीजोडा_प्रविष्टी(0, 0xfffff, 0xf2);
    }
}

