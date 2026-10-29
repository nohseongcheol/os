// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.जावा;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char संख्या आणि Unicode संकेतबिंदू संख्या वेगळी मोजते. */
public final class वर्ण {
    private वर्ण() {}
    public static byte[] संकेतन(String सामुग्री_मूल्य) { return सामुग्री_मूल्य.getBytes(StandardCharsets.UTF_8); }
    public static String डिक्रिप्ट_करा_डेटा(byte[] सामुग्री_मूल्य) { return new String(सामुग्री_मूल्य, StandardCharsets.UTF_8); }
    public static String सामान्यीकरण_करा_मूल्य(String सामुग्री_मूल्य) { return Normalizer.normalize(सामुग्री_मूल्य, Normalizer.Form.NFC); }
    public static int वर्ण_कोड_संख्या(String सामुग्री_मूल्य) { return सामुग्री_मूल्य.codePointCount(0, सामुग्री_मूल्य.length()); }
    public static List<String> शाब्दिक_शब्द(String सामुग्री_मूल्य, Locale भाषा) {
        BreakIterator भाजक_मूल्य = BreakIterator.getWordInstance(भाषा);
        भाजक_मूल्य.setText(सामुग्री_मूल्य);
        List<String> मोजमाप = new ArrayList<>();
        int सुरू_करा = भाजक_मूल्य.first();
        for (int शेवट = भाजक_मूल्य.next(); शेवट != BreakIterator.DONE; सुरू_करा = शेवट, शेवट = भाजक_मूल्य.next())
            मोजमाप.add(सामुग्री_मूल्य.substring(सुरू_करा, शेवट));
        return मोजमाप;
    }
}
