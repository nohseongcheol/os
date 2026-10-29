// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.होस्ट;

import java.util.HashMap;
import java.util.Map;
import भारत.JIndOS.गाभा.हार्डवेअर_मूल्य;

/** सामान्य JVM वर व्यवस्थापित केंद्रकाच्या निश्चित परिणामांच्या चाचणीसाठी हार्डवेअरचा पर्याय. */
public final class होस्ट_हार्डवेअर implements हार्डवेअर_मूल्य {
    private final Map<Integer, Integer> हार्डवेअर_पॉर्ट_मूल्य = new HashMap<Integer, Integer>();
    private final StringBuilder अनुक्रमिक_लॉग = new StringBuilder();

    @Override
    public void अनुक्रमिक_प्रदान(String सामुग्री_मूल्य) {
        अनुक्रमिक_लॉग.append(सामुग्री_मूल्य);
        System.out.print(सामुग्री_मूल्य);
    }

    @Override
    public int पॉर्ट_बाइट_वाचा(int हार्डवेअर_पोर्ट_नंबर) {
        Integer मूल्य = हार्डवेअर_पॉर्ट_मूल्य.get(Integer.valueOf(हार्डवेअर_पोर्ट_नंबर));
        return मूल्य == null ? 0 : मूल्य.intValue();
    }

    @Override
    public void पॉर्ट_बाइट_लिहा(int हार्डवेअर_पोर्ट_नंबर, int मूल्य) {
        हार्डवेअर_पॉर्ट_मूल्य.put(Integer.valueOf(हार्डवेअर_पोर्ट_नंबर), Integer.valueOf(मूल्य & 0xff));
    }

    @Override
    public void थांबवा_प्रोसेसर() {
        // यजमान चाचण्यांत पुढील घटनेची वाट न पाहता लगेच परतावे.
    }

    public String अनुक्रमिक_लॉग() {
        return अनुक्रमिक_लॉग.toString();
    }
}

