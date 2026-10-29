// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·kanaalü_ekeroliaa(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.열기(접속번호);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static 전문통로 열기(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public void ajütaa(String ejepüsee, int 접속번호, String atijaaya) throws 입출력예외 {
        try { 통신.ajütaa(표준종단, ejepüsee, 접속번호, atijaaya);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void asürülaa() { 통신.asürülaa(표준종단); }
}
