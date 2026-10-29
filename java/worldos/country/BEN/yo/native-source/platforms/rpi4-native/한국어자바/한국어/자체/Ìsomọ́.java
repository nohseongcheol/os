// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Darapọ̀(連結)·òpónà_ìgbéwọlé(通路): 상대와 이어진 TCP báìtì_iye 흐름의 종단. */
public final class Ìsomọ́ {
    private final java.net.Socket 표준연결;
    Ìsomọ́(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static Ìsomọ́ Ṣi(String àdírẹ́ẹ̀sì, int 접속번호) throws 입출력예외 {
        try {
            return new Ìsomọ́(new java.net.Socket(àdírẹ́ẹ̀sì, 접속번호));
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public 입력흐름 입력() throws 입출력예외 {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public 출력흐름 출력() throws 입출력예외 {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Ti() throws 입출력예외 {
        try { 표준연결.close();
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
}
