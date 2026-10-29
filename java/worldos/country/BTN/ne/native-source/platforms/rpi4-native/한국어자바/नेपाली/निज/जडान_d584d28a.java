// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;

/** जडान(連結)·च्यानल_प्रविष्टि(通路): 상대와 이어진 TCP बाइट_मान 흐름의 종단. */
public final class जडान_d584d28a {
    private final java.net.Socket 표준연결;
    जडान_d584d28a(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static जडान_d584d28a खोल्नुहोस्(String ठेगाना, int 접속번호) throws 입출력예외 {
        try {
            return new जडान_d584d28a(new java.net.Socket(ठेगाना, 접속번호));
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public 입력흐름 입력() throws 입출력예외 {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public 출력흐름 출력() throws 입출력예외 {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public void समय_सकियो(int 밀리초) throws 입출력예외 {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void बन्दगर्नुहोस्() throws 입출력예외 {
        try { 표준연결.close();
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
}
