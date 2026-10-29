// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 ingirrania_aulataup_atuutilik: 순서대로 들어오는 바이트를 읽는 saana_Iliniku. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public int 읽기(byte[] titiqqat) throws 입출력예외 {
        try { return 표준흐름.read(titiqqat);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public int 읽기(byte[] titiqqat, int 시작, int takininga_atuutilik) throws 입출력예외 {
        try { return 표준흐름.read(titiqqat, 시작, takininga_atuutilik);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public void matuli() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
}
