// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·کاناڵ_تێنووسین(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.کردنەوە(접속번호);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public static 전문통로 کردنەوە(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public void ناردن(String ناونیشان, int 접속번호, String دەیتا) throws 입출력예외 {
        try { 통신.ناردن(표준종단, ناونیشان, 접속번호, دەیتا);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void داخستن() { 통신.داخستن(표준종단); }
}
