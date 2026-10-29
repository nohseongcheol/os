// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static connexió Obre(String Adreça, int número_de_port) throws E_S_excepció {
        try { return connexió.Obre(Adreça, número_de_port);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static rebre_port 수신열기(int número_de_port) throws E_S_excepció {
        try { return rebre_port.Obre(número_de_port);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static Socket Connecta(String Adreça, int port_VALOR) throws E_S_excepció {
        try { return new Socket(Adreça, port_VALOR);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static ServerSocket escoltar_extrem(int port_VALOR) throws E_S_excepció {
        try { return new ServerSocket(port_VALOR);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static Socket rebre(ServerSocket servidor_VALOR) throws E_S_excepció {
        try { return servidor_VALOR.accept();
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
}
