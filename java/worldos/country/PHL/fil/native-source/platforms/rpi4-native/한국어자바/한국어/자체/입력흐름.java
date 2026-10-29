// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 Stream_VALUE: 순서대로 들어오는 바이트를 읽는 channel_pagpasok. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int 읽기() throws I_O_pagbubukod {
        try { return 표준흐름.read();
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public int 읽기(byte[] data) throws I_O_pagbubukod {
        try { return 표준흐름.read(data);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public int 읽기(byte[] data, int run, int haba_VALUE) throws I_O_pagbubukod {
        try { return 표준흐름.read(data, run, haba_VALUE);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public void isara() throws I_O_pagbubukod {
        try { 표준흐름.close();
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
}
