// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** संदेशांच्या सीमा जपून UDP संदेश पाठवणारा आणि स्वीकारणारा टोकबिंदू. */
public final class स्वतंत्रसंदेश_चॅनल {
    private final java.net.DatagramSocket प्रमाणित_संचारटोक;
    private स्वतंत्रसंदेश_चॅनल(int पोर्ट_नंबर) throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_संचारटोक = संचार.उघडा(पोर्ट_नंबर);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static स्वतंत्रसंदेश_चॅनल उघडा(int पोर्ट_नंबर) throws इनपुट_आउटपुट_अपवाद {
        try { return new स्वतंत्रसंदेश_चॅनल(पोर्ट_नंबर);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public void पाठवा(String पत्ता, int पोर्ट_नंबर, String डेटा) throws इनपुट_आउटपुट_अपवाद {
        try { संचार.पाठवा(प्रमाणित_संचारटोक, पत्ता, पोर्ट_नंबर, डेटा);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public String स्वीकारा() throws इनपुट_आउटपुट_अपवाद {
        try { return संचार.स्वीकारा(प्रमाणित_संचारटोक);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public void प्रतीक्षामर्यादा(int मिलिसेकंद) throws इनपुट_आउटपुट_अपवाद {
        try { संचार.प्रतीक्षामर्यादा(प्रमाणित_संचारटोक, मिलिसेकंद);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public int पोर्ट_नंबर() { return प्रमाणित_संचारटोक.getLocalPort(); }
    public boolean आहे_बंदकेलेले() { return प्रमाणित_संचारटोक.isClosed(); }
    public void बंद_करा() { संचार.बंद_करा(प्रमाणित_संचारटोक); }
}
