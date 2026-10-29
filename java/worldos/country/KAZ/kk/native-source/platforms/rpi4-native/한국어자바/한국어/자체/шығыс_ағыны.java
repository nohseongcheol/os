// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Шығысы(出力)과 ағым_мән: 순서를 보존해 내보내는 바이트의 Арна_енгізу. */
public final class шығыс_ағыны {
    private final java.io.OutputStream 표준흐름;
    шығыс_ағыны(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Жазу(int мән) throws енгізу_шығару_ерекшелік {
        try { 표준흐름.write(мән);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public void Жазу(byte[] деректер) throws енгізу_шығару_ерекшелік {
        try { 표준흐름.write(деректер);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public void Жазу(byte[] деректер, int Орындау_2, int ұзындық_мән) throws енгізу_шығару_ерекшелік {
        try { 표준흐름.write(деректер, Орындау_2, ұзындық_мән);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public void 내보내기() throws енгізу_шығару_ерекшелік {
        try { 표준흐름.flush();
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public void Жабу() throws енгізу_шығару_ерекшелік {
        try { 표준흐름.close();
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
}
