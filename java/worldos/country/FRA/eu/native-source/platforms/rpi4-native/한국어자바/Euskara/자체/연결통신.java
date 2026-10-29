// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static konexio Ireki(String helbide, int ataka_zenbaki) throws S_I_salbuespen {
        try { return konexio.Ireki(helbide, ataka_zenbaki);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static 수신창구 수신열기(int ataka_zenbaki) throws S_I_salbuespen {
        try { return 수신창구.Ireki(ataka_zenbaki);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static Socket Konektatu(String helbide, int ataka_balio) throws S_I_salbuespen {
        try { return new Socket(helbide, ataka_balio);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static ServerSocket entzun_amaiera_puntu(int ataka_balio) throws S_I_salbuespen {
        try { return new ServerSocket(ataka_balio);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public static Socket 받기(ServerSocket zerbitzari_balio) throws S_I_salbuespen {
        try { return zerbitzari_balio.accept();
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
}
