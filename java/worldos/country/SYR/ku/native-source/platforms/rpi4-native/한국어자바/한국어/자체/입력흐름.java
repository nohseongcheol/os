// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 흐름: 순서대로 들어오는 바이트를 읽는 통로. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Bixwîne() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException Çewtî) { throw 예외변환.입출력(Çewtî); }
        catch (RuntimeException Çewtî) { throw 예외변환.실행(Çewtî); }
    }
    public int Bixwîne(byte[] 자료) throws 입출력예외 {
        try { return 표준흐름.read(자료);
        } catch (java.io.IOException Çewtî) { throw 예외변환.입출력(Çewtî); }
        catch (RuntimeException Çewtî) { throw 예외변환.실행(Çewtî); }
    }
    public int Bixwîne(byte[] 자료, int Bimeşîne, int 길이) throws 입출력예외 {
        try { return 표준흐름.read(자료, Bimeşîne, 길이);
        } catch (java.io.IOException Çewtî) { throw 예외변환.입출력(Çewtî); }
        catch (RuntimeException Çewtî) { throw 예외변환.실행(Çewtî); }
    }
    public void Bigire() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException Çewtî) { throw 예외변환.입출력(Çewtî); }
        catch (RuntimeException Çewtî) { throw 예외변환.실행(Çewtî); }
    }
}
