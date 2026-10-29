// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 흐름: 순서대로 들어오는 바이트를 읽는 통로. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException 오류) { throw 예외변환.입출력(오류); }
        catch (RuntimeException 오류) { throw 예외변환.실행(오류); }
    }
    public int 읽기(byte[] 자료) throws 입출력예외 {
        try { return 표준흐름.read(자료);
        } catch (java.io.IOException 오류) { throw 예외변환.입출력(오류); }
        catch (RuntimeException 오류) { throw 예외변환.실행(오류); }
    }
    public int 읽기(byte[] 자료, int 시작, int 길이) throws 입출력예외 {
        try { return 표준흐름.read(자료, 시작, 길이);
        } catch (java.io.IOException 오류) { throw 예외변환.입출력(오류); }
        catch (RuntimeException 오류) { throw 예외변환.실행(오류); }
    }
    public void बंद_करिव() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException 오류) { throw 예외변환.입출력(오류); }
        catch (RuntimeException 오류) { throw 예외변환.실행(오류); }
    }
}
