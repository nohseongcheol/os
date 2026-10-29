// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;

/** 입력(入力)과 स्ट्रीम_मान: 순서대로 들어오는 바이트를 읽는 चैनल_एन्ट्री. */
public final class इनपुट_प्रवाह {
    private final java.io.InputStream 표준흐름;
    इनपुट_प्रवाह(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int पढ़ें() throws इनपुट_आउटपुट_अपवाद {
        try { return 표준흐름.read();
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public int पढ़ें(byte[] आँकड़े) throws इनपुट_आउटपुट_अपवाद {
        try { return 표준흐름.read(आँकड़े);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public int पढ़ें(byte[] आँकड़े, int चलाएँ, int 길이) throws इनपुट_आउटपुट_अपवाद {
        try { return 표준흐름.read(आँकड़े, चलाएँ, 길이);
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
    public void बंदकरें() throws इनपुट_आउटपुट_अपवाद {
        try { 표준흐름.close();
        } catch (java.io.IOException त्रुटि) { throw रूपांतरित_करें_अपवाद.इनपुट_आउटपुट(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw रूपांतरित_करें_अपवाद.निष्पादित_करें_आदेश(त्रुटि); }
    }
}
