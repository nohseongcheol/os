// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 waraango_njaru: 순서대로 들어오는 바이트를 읽는 kanaal_naatnugol. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public int 읽기(byte[] keɓe) throws 입출력예외 {
        try { return 표준흐름.read(keɓe);
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public int 읽기(byte[] keɓe, int huutoraade, int njuuteendi_njaru) throws 입출력예외 {
        try { return 표준흐름.read(keɓe, huutoraade, njuuteendi_njaru);
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public void uddude() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
}
