// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;
import java.net.*;
public final class कनेक्शन_वाहतूक {
    private कनेक्शन_वाहतूक() {}
    public static कनेक्शन उघडा(String पत्ता, int पोर्ट_नंबर) throws इनपुट_आउटपुट_अपवाद {
        try { return कनेक्शन.उघडा(पत्ता, पोर्ट_नंबर);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static पॉर्ट_स्वीकारा ग्राहक_उघडा(int पोर्ट_नंबर) throws इनपुट_आउटपुट_अपवाद {
        try { return पॉर्ट_स्वीकारा.उघडा(पोर्ट_नंबर);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static Socket जोडा(String पत्ता, int पॉर्ट_मूल्य) throws इनपुट_आउटपुट_अपवाद {
        try { return new Socket(पत्ता, पॉर्ट_मूल्य);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static ServerSocket ऐका_संचारटोक(int पॉर्ट_मूल्य) throws इनपुट_आउटपुट_अपवाद {
        try { return new ServerSocket(पॉर्ट_मूल्य);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public static Socket स्वीकारा(ServerSocket सर्व्हर_मूल्य) throws इनपुट_आउटपुट_अपवाद {
        try { return सर्व्हर_मूल्य.accept();
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
}
