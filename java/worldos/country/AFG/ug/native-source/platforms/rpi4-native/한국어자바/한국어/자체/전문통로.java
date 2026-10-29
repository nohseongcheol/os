// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·قانال_كىرگۈزۈش(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.ئاچ(접속번호);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public static 전문통로 ئاچ(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public void ئەۋەتمەك(String ئادرېس, int 접속번호, String مەلۇمات) throws 입출력예외 {
        try { 통신.ئەۋەتمەك(표준종단, ئادرېس, 접속번호, مەلۇمات);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public void ۋاقىت_ئاشتى(int 밀리초) throws 입출력예외 {
        try { 통신.ۋاقىت_ئاشتى(표준종단, 밀리초);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void ياپ() { 통신.ياپ(표준종단); }
}
