// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;

/** जोड़ना(連結)·चैनल_एन्ट्री(通路): 상대와 이어진 TCP बाइट_मान 흐름의 एंडपॉइंट. */
public final class कनेक्शन {
    private final java.net.Socket 표준연결;
    कनेक्शन(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static कनेक्शन खोलें(String पता, int पोर्ट_संख्या) throws इनपुट_आउटपुट_अपवाद {
        try {
            return new कनेक्शन(new java.net.Socket(पता, पोर्ट_संख्या));
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public इनपुट_प्रवाह 입력() throws इनपुट_आउटपुट_अपवाद {
        try { return new इनपुट_प्रवाह(표준연결.getInputStream());
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public आउटपुट_प्रवाह निर्गम() throws इनपुट_आउटपुट_अपवाद {
        try { return new आउटपुट_प्रवाह(표준연결.getOutputStream());
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public void 대기시간(int 밀리초) throws इनपुट_आउटपुट_अपवाद {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public int पोर्ट_संख्या() { return 표준연결.getPort(); }
    public int स्थानीय_पोर्ट_संख्या() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void बंदकरें() throws इनपुट_आउटपुट_अपवाद {
        try { 표준연결.close();
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
}
