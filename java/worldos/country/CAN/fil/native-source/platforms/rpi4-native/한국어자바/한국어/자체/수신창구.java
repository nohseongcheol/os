// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·port_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int numero_ng_port) throws I_O_pagbubukod {
        try { 표준창구 = new java.net.ServerSocket(numero_ng_port);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static 수신창구 buksan(int numero_ng_port) throws I_O_pagbubukod {
        try { return new 수신창구(numero_ng_port);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public koneksyon 받기() throws I_O_pagbubukod {
        try { return new koneksyon(표준창구.accept());
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public int numero_ng_port() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_O_pagbubukod {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void isara() throws I_O_pagbubukod {
        try { 표준창구.close();
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
}
