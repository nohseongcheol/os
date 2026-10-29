// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;

/** 전문(電文)·ጣብያ_ምእታው(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.ክፈት(접속번호);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static 전문통로 ክፈት(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public void ለኣኽ(String ኣድራሻ, int 접속번호, String ሓበሬታ) throws 입출력예외 {
        try { 통신.ለኣኽ(표준종단, ኣድራሻ, 접속번호, ሓበሬታ);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void ዕጸው() { 통신.ዕጸው(표준종단); }
}
