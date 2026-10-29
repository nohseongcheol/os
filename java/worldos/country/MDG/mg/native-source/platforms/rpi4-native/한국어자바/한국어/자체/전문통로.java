// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·통로(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.Sokafy(접속번호);
        } catch (java.io.IOException Tsy_fetezana) { throw 예외변환.입출력(Tsy_fetezana); }
        catch (RuntimeException Tsy_fetezana) { throw 예외변환.실행(Tsy_fetezana); }
    }
    public static 전문통로 Sokafy(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException Tsy_fetezana) { throw 예외변환.입출력(Tsy_fetezana); }
        catch (RuntimeException Tsy_fetezana) { throw 예외변환.실행(Tsy_fetezana); }
    }
    public void 보내기(String 주소, int 접속번호, String 자료) throws 입출력예외 {
        try { 통신.보내기(표준종단, 주소, 접속번호, 자료);
        } catch (java.io.IOException Tsy_fetezana) { throw 예외변환.입출력(Tsy_fetezana); }
        catch (RuntimeException Tsy_fetezana) { throw 예외변환.실행(Tsy_fetezana); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException Tsy_fetezana) { throw 예외변환.입출력(Tsy_fetezana); }
        catch (RuntimeException Tsy_fetezana) { throw 예외변환.실행(Tsy_fetezana); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException Tsy_fetezana) { throw 예외변환.입출력(Tsy_fetezana); }
        catch (RuntimeException Tsy_fetezana) { throw 예외변환.실행(Tsy_fetezana); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void hidio() { 통신.hidio(표준종단); }
}
