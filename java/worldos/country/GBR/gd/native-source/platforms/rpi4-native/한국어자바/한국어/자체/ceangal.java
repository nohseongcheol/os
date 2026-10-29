// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** CONNECT(連結)·seanail_cur_a_steach(通路): 상대와 이어진 TCP baidht_VALUE 흐름의 종단. */
public final class ceangal {
    private final java.net.Socket 표준연결;
    ceangal(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static ceangal fosgail(String ADDRESS, int 접속번호) throws 입출력예외 {
        try {
            return new ceangal(new java.net.Socket(ADDRESS, 접속번호));
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public 입력흐름 입력() throws 입출력예외 {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public 출력흐름 출력() throws 입출력예외 {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public void TIMEOUT(int 밀리초) throws 입출력예외 {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void dùin() throws 입출력예외 {
        try { 표준연결.close();
        } catch (java.io.IOException Mearachd) { throw 예외변환.I_O(Mearachd); }
        catch (RuntimeException Mearachd) { throw 예외변환.gnìomhaich_àithne(Mearachd); }
    }
}
