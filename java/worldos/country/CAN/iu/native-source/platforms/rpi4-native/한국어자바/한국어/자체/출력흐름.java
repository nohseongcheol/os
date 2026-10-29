// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 ingirrania_aulataup_atuutilik: 순서를 보존해 내보내는 바이트의 saana_Iliniku. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void titiraq(int atuutilik) throws 입출력예외 {
        try { 표준흐름.write(atuutilik);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public void titiraq(byte[] titiqqat) throws 입출력예외 {
        try { 표준흐름.write(titiqqat);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public void titiraq(byte[] titiqqat, int 시작, int takininga_atuutilik) throws 입출력예외 {
        try { 표준흐름.write(titiqqat, 시작, takininga_atuutilik);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public void matuli() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
}
