// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·창구(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int 접속번호) throws 입출력예외 {
        try { 표준창구 = new java.net.ServerSocket(접속번호);
        } catch (java.io.IOException Tsy_fetezana) { throw 예외변환.입출력(Tsy_fetezana); }
        catch (RuntimeException Tsy_fetezana) { throw 예외변환.실행(Tsy_fetezana); }
    }
    public static 수신창구 Sokafy(int 접속번호) throws 입출력예외 {
        try { return new 수신창구(접속번호);
        } catch (java.io.IOException Tsy_fetezana) { throw 예외변환.입출력(Tsy_fetezana); }
        catch (RuntimeException Tsy_fetezana) { throw 예외변환.실행(Tsy_fetezana); }
    }
    public 연결통로 받기() throws 입출력예외 {
        try { return new 연결통로(표준창구.accept());
        } catch (java.io.IOException Tsy_fetezana) { throw 예외변환.입출력(Tsy_fetezana); }
        catch (RuntimeException Tsy_fetezana) { throw 예외변환.실행(Tsy_fetezana); }
    }
    public int 접속번호() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException Tsy_fetezana) { throw 예외변환.입출력(Tsy_fetezana); }
        catch (RuntimeException Tsy_fetezana) { throw 예외변환.실행(Tsy_fetezana); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void hidio() throws 입출력예외 {
        try { 표준창구.close();
        } catch (java.io.IOException Tsy_fetezana) { throw 예외변환.입출력(Tsy_fetezana); }
        catch (RuntimeException Tsy_fetezana) { throw 예외변환.실행(Tsy_fetezana); }
    }
}
