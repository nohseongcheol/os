// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;

/** 입력(入力)과 प्रवाह_मान: 순서대로 들어오는 바이트를 읽는 च्यानल_प्रविष्टि. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int पढनुहोस्() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public int पढनुहोस्(byte[] लगत) throws 입출력예외 {
        try { return 표준흐름.read(लगत);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public int पढनुहोस्(byte[] लगत, int चलाउनुहोस्, int लम्बाइ_मान) throws 입출력예외 {
        try { return 표준흐름.read(लगत, चलाउनुहोस्, लम्बाइ_मान);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public void बन्दगर्नुहोस्() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
}
