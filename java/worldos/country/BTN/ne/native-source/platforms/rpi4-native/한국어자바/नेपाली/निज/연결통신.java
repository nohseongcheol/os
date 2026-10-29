// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static जडान_d584d28a खोल्नुहोस्(String ठेगाना, int 접속번호) throws 입출력예외 {
        try { return जडान_d584d28a.खोल्नुहोस्(ठेगाना, 접속번호);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.खोल्नुहोस्(접속번호);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static Socket जडान(String ठेगाना, int पोर्ट_मान) throws 입출력예외 {
        try { return new Socket(ठेगाना, पोर्ट_मान);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static ServerSocket 듣기(int पोर्ट_मान) throws 입출력예외 {
        try { return new ServerSocket(पोर्ट_मान);
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
    public static Socket 받기(ServerSocket सर्भर_मान) throws 입출력예외 {
        try { return सर्भर_मान.accept();
        } catch (java.io.IOException त्रुटि) { throw 예외변환.आगत_लगत(त्रुटि); }
        catch (RuntimeException त्रुटि) { throw 예외변환.कार्यान्वयन_गर्नुहोस्_आदेश(त्रुटि); }
    }
}
