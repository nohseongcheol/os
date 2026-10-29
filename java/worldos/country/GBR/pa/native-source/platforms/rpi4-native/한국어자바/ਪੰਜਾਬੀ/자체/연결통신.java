// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static ਸਬੰਧ ਖੋਲ੍ਹੋ(String ਪਤਾ, int 접속번호) throws 입출력예외 {
        try { return ਸਬੰਧ.ਖੋਲ੍ਹੋ(ਪਤਾ, 접속번호);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.ਖੋਲ੍ਹੋ(접속번호);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static Socket ਕੁਨੈਕਸ਼ਨ_ਕਰੋ(String ਪਤਾ, int ਪੋਰਟ_ਕੀਮਤ) throws 입출력예외 {
        try { return new Socket(ਪਤਾ, ਪੋਰਟ_ਕੀਮਤ);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static ServerSocket 듣기(int ਪੋਰਟ_ਕੀਮਤ) throws 입출력예외 {
        try { return new ServerSocket(ਪੋਰਟ_ਕੀਮਤ);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static Socket 받기(ServerSocket ਸਰਵਰ_ਕੀਮਤ) throws 입출력예외 {
        try { return ਸਰਵਰ_ਕੀਮਤ.accept();
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
}
