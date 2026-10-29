// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** समोरील टोकाशी जोडलेल्या TCP बाइटप्रवाहाचा टोकबिंदू. */
public final class कनेक्शन {
    private final java.net.Socket प्रमाणित_लायब्ररी_ब्रिज;
    कनेक्शन(java.net.Socket प्रमाणित_लायब्ररी_ब्रिज) { this.प्रमाणित_लायब्ररी_ब्रिज = प्रमाणित_लायब्ररी_ब्रिज; }
    public static कनेक्शन उघडा(String पत्ता, int पोर्ट_नंबर) throws इनपुट_आउटपुट_अपवाद {
        try {
            return new कनेक्शन(new java.net.Socket(पत्ता, पोर्ट_नंबर));
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public आदान_प्रवाह आदान_मूल्य() throws इनपुट_आउटपुट_अपवाद {
        try { return new आदान_प्रवाह(प्रमाणित_लायब्ररी_ब्रिज.getInputStream());
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public प्रदान_प्रवाह आउटपुट() throws इनपुट_आउटपुट_अपवाद {
        try { return new प्रदान_प्रवाह(प्रमाणित_लायब्ररी_ब्रिज.getOutputStream());
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public void प्रतीक्षामर्यादा(int मिलिसेकंद) throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_लायब्ररी_ब्रिज.setSoTimeout(मिलिसेकंद);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public int पोर्ट_नंबर() { return प्रमाणित_लायब्ररी_ब्रिज.getPort(); }
    public int स्थानिक_पोर्ट_नंबर() { return प्रमाणित_लायब्ररी_ब्रिज.getLocalPort(); }
    public boolean आहे_बंदकेलेले() { return प्रमाणित_लायब्ररी_ब्रिज.isClosed(); }
    public boolean जोडलेले() { return प्रमाणित_लायब्ररी_ब्रिज.isConnected(); }
    public void बंद_करा() throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_लायब्ररी_ब्रिज.close();
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
}
