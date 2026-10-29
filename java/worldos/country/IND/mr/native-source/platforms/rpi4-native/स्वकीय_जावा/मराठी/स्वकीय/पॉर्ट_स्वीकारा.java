// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** येणाऱ्या TCP जोडण्या स्वीकारते. */
public final class पॉर्ट_स्वीकारा {
    private final java.net.ServerSocket प्रमाणित_पॉर्ट;
    private पॉर्ट_स्वीकारा(int पोर्ट_नंबर) throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_पॉर्ट = new java.net.ServerSocket(पोर्ट_नंबर);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static पॉर्ट_स्वीकारा उघडा(int पोर्ट_नंबर) throws इनपुट_आउटपुट_अपवाद {
        try { return new पॉर्ट_स्वीकारा(पोर्ट_नंबर);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public कनेक्शन स्वीकारा() throws इनपुट_आउटपुट_अपवाद {
        try { return new कनेक्शन(प्रमाणित_पॉर्ट.accept());
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public int पोर्ट_नंबर() { return प्रमाणित_पॉर्ट.getLocalPort(); }
    public void प्रतीक्षामर्यादा(int मिलिसेकंद) throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_पॉर्ट.setSoTimeout(मिलिसेकंद);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public boolean आहे_बंदकेलेले() { return प्रमाणित_पॉर्ट.isClosed(); }
    public void बंद_करा() throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_पॉर्ट.close();
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
}
