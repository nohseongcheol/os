// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;

/** स्वतंत्रसंदेश(電文)·चैनल_एन्ट्री(通路): 경계를 가진 UDP 자료를 주고받는 एंडपॉइंट. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int पोर्ट_संख्या) throws इनपुट_आउटपुट_अपवाद {
        try { 표준종단 = 통신.खोलें(पोर्ट_संख्या);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public static 전문통로 खोलें(int पोर्ट_संख्या) throws इनपुट_आउटपुट_अपवाद {
        try { return new 전문통로(पोर्ट_संख्या);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public void भेजें(String पता, int पोर्ट_संख्या, String आँकड़े) throws इनपुट_आउटपुट_अपवाद {
        try { 통신.भेजें(표준종단, पता, पोर्ट_संख्या, आँकड़े);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public String 받기() throws इनपुट_आउटपुट_अपवाद {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public void 대기시간(int 밀리초) throws इनपुट_आउटपुट_अपवाद {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public int पोर्ट_संख्या() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void बंदकरें() { 통신.बंदकरें(표준종단); }
}
