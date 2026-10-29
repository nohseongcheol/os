// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;

/** 전문(電文)·च्यानल_प्रविष्टि(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.खोल्नुहोस्(접속번호);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static 전문통로 खोल्नुहोस्(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public void पठाउनुहोस्(String ठेगाना, int 접속번호, String लगत) throws 입출력예외 {
        try { 통신.पठाउनुहोस्(표준종단, ठेगाना, 접속번호, लगत);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public void समय_सकियो(int 밀리초) throws 입출력예외 {
        try { 통신.समय_सकियो(표준종단, 밀리초);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void बन्दगर्नुहोस्() { 통신.बन्दगर्नुहोस्(표준종단); }
}
