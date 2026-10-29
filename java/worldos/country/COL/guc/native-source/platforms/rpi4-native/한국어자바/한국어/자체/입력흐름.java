// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 palantüsü_ajutuu: 순서대로 들어오는 바이트를 읽는 kanaalü_ekeroliaa. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public int 읽기(byte[] atijaaya) throws 입출력예외 {
        try { return 표준흐름.read(atijaaya);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public int 읽기(byte[] atijaaya, int 시작, int akaliaa_ajutuu) throws 입출력예외 {
        try { return 표준흐름.read(atijaaya, 시작, akaliaa_ajutuu);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public void asürülaa() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
}
