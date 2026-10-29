// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;

/** Cysylltu(連結)·sianel_cofnod(通路): 상대와 이어진 TCP beit_VALUE 흐름의 종단. */
public final class cyswllt {
    private final java.net.Socket 표준연결;
    cyswllt(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static cyswllt Agor(String ADDRESS, int rhif_porth) throws I_O_eithriad {
        try {
            return new cyswllt(new java.net.Socket(ADDRESS, rhif_porth));
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public 입력흐름 입력() throws I_O_eithriad {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public 출력흐름 Allbwn() throws I_O_eithriad {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_eithriad {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public int rhif_porth() { return 표준연결.getPort(); }
    public int lleol_rhif_porth() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Cau() throws I_O_eithriad {
        try { 표준연결.close();
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
}
