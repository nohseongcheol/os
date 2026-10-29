// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;

/** 출력(出力)과 प्रवाह_मान: 순서를 보존해 내보내는 바이트의 च्यानल_प्रविष्टि. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void लेख्नुहोस्(int मान) throws 입출력예외 {
        try { 표준흐름.write(मान);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public void लेख्नुहोस्(byte[] लगत) throws 입출력예외 {
        try { 표준흐름.write(लगत);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public void लेख्नुहोस्(byte[] लगत, int चलाउनुहोस्, int लम्बाइ_मान) throws 입출력예외 {
        try { 표준흐름.write(लगत, चलाउनुहोस्, लम्बाइ_मान);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public void बन्दगर्नुहोस्() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
}
