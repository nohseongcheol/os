// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static कनेक्शन खोलें(String पता, int पोर्ट_संख्या) throws इनपुट_आउटपुट_अपवाद {
        try { return कनेक्शन.खोलें(पता, पोर्ट_संख्या);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static 수신창구 수신열기(int पोर्ट_संख्या) throws इनपुट_आउटपुट_अपवाद {
        try { return 수신창구.खोलें(पोर्ट_संख्या);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static Socket जोड़ना(String पता, int पोर्ट_मान) throws इनपुट_आउटपुट_अपवाद {
        try { return new Socket(पता, पोर्ट_मान);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static ServerSocket सुनिए_एंडपॉइंट(int पोर्ट_मान) throws इनपुट_आउटपुट_अपवाद {
        try { return new ServerSocket(पोर्ट_मान);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static Socket 받기(ServerSocket 서버) throws इनपुट_आउटपुट_अपवाद {
        try { return 서버.accept();
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
}
