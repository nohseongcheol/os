// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·kanaal_inskrywing(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws I_O_uitsondering {
        try { 표준종단 = 통신.skep(접속번호);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static 전문통로 skep(int 접속번호) throws I_O_uitsondering {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public void e_pos(String adres, int 접속번호, String data) throws I_O_uitsondering {
        try { 통신.e_pos(표준종단, adres, 접속번호, data);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public String 받기() throws I_O_uitsondering {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public void UITTELLING(int 밀리초) throws I_O_uitsondering {
        try { 통신.UITTELLING(표준종단, 밀리초);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Sluit() { 통신.Sluit(표준종단); }
}
