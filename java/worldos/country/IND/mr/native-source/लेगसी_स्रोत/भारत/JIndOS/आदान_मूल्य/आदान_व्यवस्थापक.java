// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.आदान_मूल्य;

import java.util.ArrayDeque;
import java.util.Queue;

/** व्यत्यय आणि व्यवस्थापित संकेत यांच्या दरम्यान आदानघटना सुरक्षितपणे पोहोचवते. */
public final class आदान_व्यवस्थापक {
    private final Queue<आदान_इव्हेंट> घटना_यादी = new ArrayDeque<आदान_इव्हेंट>();
    private final int कमाल_इव्हेंट_संख्या;
    private int वगळलेले_इव्हेंट_संख्या;

    public आदान_व्यवस्थापक(int कमाल_इव्हेंट_संख्या) {
        if (कमाल_इव्हेंट_संख्या <= 0) {
            throw new IllegalArgumentException("इव्हेंट 수가 올바르지 않습니다.");
        }
        this.कमाल_इव्हेंट_संख्या = कमाल_इव्हेंट_संख्या;
    }

    public synchronized void कळ_खाली(int कळ_डेटा) {
        ठेवा_मूल्य(new आदान_इव्हेंट(आदान_इव्हेंट.प्रकार_मूल्य.कळ_खाली, कळ_डेटा & 0xff, 0));
    }

    public synchronized void कळ_वर(int कळ_डेटा) {
        ठेवा_मूल्य(new आदान_इव्हेंट(आदान_इव्हेंट.प्रकार_मूल्य.कळ_वर, कळ_डेटा & 0xff, 0));
    }

    public synchronized void माऊस_हालचाल(int आडवे_स्थान, int अनुलंब_स्थान) {
        ठेवा_मूल्य(new आदान_इव्हेंट(आदान_इव्हेंट.प्रकार_मूल्य.माऊस_हालचाल, आडवे_स्थान, अनुलंब_स्थान));
    }

    public synchronized आदान_इव्हेंट पुढील_इव्हेंट() {
        return घटना_यादी.poll();
    }

    public synchronized int वगळलेले_इव्हेंट_संख्या() {
        return वगळलेले_इव्हेंट_संख्या;
    }

    private void ठेवा_मूल्य(आदान_इव्हेंट इव्हेंट) {
        if (घटना_यादी.size() == कमाल_इव्हेंट_संख्या) {
            घटना_यादी.poll();
            वगळलेले_इव्हेंट_संख्या++;
        }
        घटना_यादी.offer(इव्हेंट);
    }
}

