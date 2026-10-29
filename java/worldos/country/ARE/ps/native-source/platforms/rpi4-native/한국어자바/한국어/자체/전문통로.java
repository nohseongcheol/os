// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·چینل_ننوت(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.پرانيستل(접속번호);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static 전문통로 پرانيستل(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public void استول(String پته, int 접속번호, String اومتوک) throws 입출력예외 {
        try { 통신.استول(표준종단, پته, 접속번호, اومتوک);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void بندول() { 통신.بندول(표준종단); }
}
