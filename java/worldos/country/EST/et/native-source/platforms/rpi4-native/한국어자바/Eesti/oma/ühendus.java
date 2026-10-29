// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;

/** Ühendu(連結)·Kanal_kirje(通路): 상대와 이어진 TCP bait_VALUE 흐름의 osaleja. */
public final class ühendus {
    private final java.net.Socket 표준연결;
    ühendus(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static ühendus Ava(String ADDRESS, int pordinumber) throws I_O_erand {
        try {
            return new ühendus(new java.net.Socket(ADDRESS, pordinumber));
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public sisendvoog 입력() throws I_O_erand {
        try { return new sisendvoog(표준연결.getInputStream());
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public väljundvoog Väljund() throws I_O_erand {
        try { return new väljundvoog(표준연결.getOutputStream());
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_erand {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public int pordinumber() { return 표준연결.getPort(); }
    public int kohalik_pordinumber() { return 표준연결.getLocalPort(); }
    public boolean infotehnoloogia_suletud() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Suletud() throws I_O_erand {
        try { 표준연결.close();
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
}
