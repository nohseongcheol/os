// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** येणारे बाइट क्रमाने वाचण्याचा मार्ग. */
public final class आदान_प्रवाह {
    private final java.io.InputStream प्रमाणित_प्रवाह;
    आदान_प्रवाह(java.io.InputStream प्रमाणित_प्रवाह) { this.प्रमाणित_प्रवाह = प्रमाणित_प्रवाह; }
    public int वाचन() throws इनपुट_आउटपुट_अपवाद {
        try { return प्रमाणित_प्रवाह.read();
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public int वाचन(byte[] डेटा) throws इनपुट_आउटपुट_अपवाद {
        try { return प्रमाणित_प्रवाह.read(डेटा);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public int वाचन(byte[] डेटा, int सुरू_करा, int लांबी_मूल्य) throws इनपुट_आउटपुट_अपवाद {
        try { return प्रमाणित_प्रवाह.read(डेटा, सुरू_करा, लांबी_मूल्य);
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
    public void बंद_करा() throws इनपुट_आउटपुट_अपवाद {
        try { प्रमाणित_प्रवाह.close();
        } catch (java.io.IOException त्रुटी) { throw रूपांतरकरा_अपवाद.इनपुट_आउटपुट(त्रुटी); }
        catch (RuntimeException त्रुटी) { throw रूपांतरकरा_अपवाद.आज्ञा_कार्यवाही_करा(त्रुटी); }
    }
}
