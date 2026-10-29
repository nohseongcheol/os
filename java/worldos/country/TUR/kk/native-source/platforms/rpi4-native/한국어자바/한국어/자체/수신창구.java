// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·порт_мән(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int порт_нөмірі) throws енгізу_шығару_ерекшелік {
        try { 표준창구 = new java.net.ServerSocket(порт_нөмірі);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static 수신창구 Ашу(int порт_нөмірі) throws енгізу_шығару_ерекшелік {
        try { return new 수신창구(порт_нөмірі);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public қосылым 받기() throws енгізу_шығару_ерекшелік {
        try { return new қосылым(표준창구.accept());
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public int порт_нөмірі() { return 표준창구.getLocalPort(); }
    public void ТАЙМ_АУТ(int 밀리초) throws енгізу_шығару_ерекшелік {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Жабу() throws енгізу_шығару_ерекшелік {
        try { 표준창구.close();
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
}
