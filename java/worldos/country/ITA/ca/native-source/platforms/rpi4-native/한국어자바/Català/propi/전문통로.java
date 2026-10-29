// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;

/** 전문(電文)·Canal_introducció(通路): 경계를 가진 UDP 자료를 주고받는 extrem. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int número_de_port) throws E_S_excepció {
        try { 표준종단 = 통신.Obre(número_de_port);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static 전문통로 Obre(int número_de_port) throws E_S_excepció {
        try { return new 전문통로(número_de_port);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public void enviar(String Adreça, int número_de_port, String dades) throws E_S_excepció {
        try { 통신.enviar(표준종단, Adreça, número_de_port, dades);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public String rebre() throws E_S_excepció {
        try { return 통신.rebre(표준종단);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public void TIMEOUT(int 밀리초) throws E_S_excepció {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public int número_de_port() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Tanca() { 통신.Tanca(표준종단); }
}
