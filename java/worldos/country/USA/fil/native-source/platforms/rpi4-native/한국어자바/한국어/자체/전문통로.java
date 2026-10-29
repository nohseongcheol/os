// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·channel_pagpasok(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int numero_ng_port) throws I_O_pagbubukod {
        try { 표준종단 = 통신.buksan(numero_ng_port);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static 전문통로 buksan(int numero_ng_port) throws I_O_pagbubukod {
        try { return new 전문통로(numero_ng_port);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public void i_email(String email, int numero_ng_port, String data) throws I_O_pagbubukod {
        try { 통신.i_email(표준종단, email, numero_ng_port, data);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public String 받기() throws I_O_pagbubukod {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_pagbubukod {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public int numero_ng_port() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void isara() { 통신.isara(표준종단); }
}
