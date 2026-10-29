// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** क्रम राखून बाहेर जाणारे बाइट लिहिण्याचा मार्ग. */
public final class प्रदान_प्रवाह {
    private final java.io.OutputStream प्रमाणित_प्रवाह;
    प्रदान_प्रवाह(java.io.OutputStream प्रमाणित_प्रवाह) { this.प्रमाणित_प्रवाह = प्रमाणित_प्रवाह; }
    public void लेखन(int मूल्य) throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_प्रवाह.write(मूल्य);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public void लेखन(byte[] डेटा) throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_प्रवाह.write(डेटा);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public void लेखन(byte[] डेटा, int सुरू_करा, int लांबी_मूल्य) throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_प्रवाह.write(डेटा, सुरू_करा, लांबी_मूल्य);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public void निर्गमितकरा_मूल्य() throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_प्रवाह.flush();
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public void बंद_करा() throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_प्रवाह.close();
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
}
