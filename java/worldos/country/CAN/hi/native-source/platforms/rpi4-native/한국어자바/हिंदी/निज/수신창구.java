// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;

/** 수신(受信)·पोर्ट_मान(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int पोर्ट_संख्या) throws इनपुट_आउटपुट_अपवाद {
        try { 표준창구 = new java.net.ServerSocket(पोर्ट_संख्या);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static 수신창구 खोलें(int पोर्ट_संख्या) throws इनपुट_आउटपुट_अपवाद {
        try { return new 수신창구(पोर्ट_संख्या);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public कनेक्शन 받기() throws इनपुट_आउटपुट_अपवाद {
        try { return new कनेक्शन(표준창구.accept());
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public int पोर्ट_संख्या() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws इनपुट_आउटपुट_अपवाद {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void बंदकरें() throws इनपुट_आउटपुट_अपवाद {
        try { 표준창구.close();
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
}
