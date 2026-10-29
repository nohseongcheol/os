// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;

/** 입력(入力)과 ਸਟ੍ਰੀਮ_ਕੀਮਤ: 순서대로 들어오는 바이트를 읽는 ਚੈਨਲ_ਦਾਖਲਾ. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int ਪੜ੍ਹਨ() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public int ਪੜ੍ਹਨ(byte[] ਸਮੱਗਰੀ) throws 입출력예외 {
        try { return 표준흐름.read(ਸਮੱਗਰੀ);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public int ਪੜ੍ਹਨ(byte[] ਸਮੱਗਰੀ, int ਚਲਾਓ_2, int ਲੰਬਾਈ_ਕੀਮਤ) throws 입출력예외 {
        try { return 표준흐름.read(ਸਮੱਗਰੀ, ਚਲਾਓ_2, ਲੰਬਾਈ_ਕੀਮਤ);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public void ਬੰਦ_ਕਰੋ() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
}
