// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;

/** 전문(電文)·ਚੈਨਲ_ਦਾਖਲਾ(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.ਖੋਲ੍ਹੋ(접속번호);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static 전문통로 ਖੋਲ੍ਹੋ(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public void ਈਮੇਲ(String ਪਤਾ, int 접속번호, String ਸਮੱਗਰੀ) throws 입출력예외 {
        try { 통신.ਈਮੇਲ(표준종단, ਪਤਾ, 접속번호, ਸਮੱਗਰੀ);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public void ਸਮਾਂ_ਸਮਾਪਤ(int 밀리초) throws 입출력예외 {
        try { 통신.ਸਮਾਂ_ਸਮਾਪਤ(표준종단, 밀리초);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void ਬੰਦ_ਕਰੋ() { 통신.ਬੰਦ_ਕਰੋ(표준종단); }
}
