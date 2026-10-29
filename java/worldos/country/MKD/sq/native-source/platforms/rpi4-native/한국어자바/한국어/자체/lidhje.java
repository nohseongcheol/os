// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Lidhu(連結)·kanal_futje(通路): 상대와 이어진 TCP bajt_VALUE 흐름의 종단. */
public final class lidhje {
    private final java.net.Socket 표준연결;
    lidhje(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static lidhje Hap(String email, int numri_i_portës) throws I_O_përjashtim {
        try {
            return new lidhje(new java.net.Socket(email, numri_i_portës));
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public 입력흐름 입력() throws I_O_përjashtim {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public 출력흐름 출력() throws I_O_përjashtim {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_përjashtim {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public int numri_i_portës() { return 표준연결.getPort(); }
    public int lokal_numri_i_portës() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Mbyll() throws I_O_përjashtim {
        try { 표준연결.close();
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
}
