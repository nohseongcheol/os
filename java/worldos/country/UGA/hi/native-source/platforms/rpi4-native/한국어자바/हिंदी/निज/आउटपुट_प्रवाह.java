// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;

/** निर्गम(出力)과 स्ट्रीम_मान: 순서를 보존해 내보내는 바이트의 चैनल_एन्ट्री. */
public final class आउटपुट_प्रवाह {
    private final java.io.OutputStream 표준흐름;
    आउटपुट_प्रवाह(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void लिखें(int मान) throws इनपुट_आउटपुट_अपवाद {
        try { 표준흐름.write(मान);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public void लिखें(byte[] आँकड़े) throws इनपुट_आउटपुट_अपवाद {
        try { 표준흐름.write(आँकड़े);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public void लिखें(byte[] आँकड़े, int चलाएँ, int 길이) throws इनपुट_आउटपुट_अपवाद {
        try { 표준흐름.write(आँकड़े, चलाएँ, 길이);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public void 내보내기() throws इनपुट_आउटपुट_अपवाद {
        try { 표준흐름.flush();
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public void बंदकरें() throws इनपुट_आउटपुट_अपवाद {
        try { 표준흐름.close();
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
}
