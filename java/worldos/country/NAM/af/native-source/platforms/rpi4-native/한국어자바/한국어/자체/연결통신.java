// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static verbinding skep(String adres, int 접속번호) throws I_O_uitsondering {
        try { return verbinding.skep(adres, 접속번호);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static 수신창구 수신열기(int 접속번호) throws I_O_uitsondering {
        try { return 수신창구.skep(접속번호);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static Socket Koppel(String adres, int ombou_VALUE) throws I_O_uitsondering {
        try { return new Socket(adres, ombou_VALUE);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static ServerSocket 듣기(int ombou_VALUE) throws I_O_uitsondering {
        try { return new ServerSocket(ombou_VALUE);
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
    public static Socket 받기(ServerSocket bediener_VALUE) throws I_O_uitsondering {
        try { return bediener_VALUE.accept();
        } catch (java.io.IOException Fout) { throw CONVERT_uitsondering.I_O(Fout); }
        catch (RuntimeException Fout) { throw CONVERT_uitsondering.uitvoer_bevel(Fout); }
    }
}
