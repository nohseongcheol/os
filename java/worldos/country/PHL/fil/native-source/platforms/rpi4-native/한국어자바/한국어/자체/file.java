// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 gumagamit 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class file {
    private file() {}
    public static byte[] 바이트읽기(String pangalan) throws I_O_pagbubukod {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(pangalan);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (수 == 임시.length) throw new I_O_pagbubukod("file sukat_82232621 제한"); 임시[수++] = (byte)VALUE; }
            byte[] sukat = new byte[수]; System.arraycopy(임시, 0, sukat, 0, 수); return sukat;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static void sumulat_byte_VALUE(String pangalan, byte[] Nilalaman_VALUE) throws I_O_pagbubukod {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(pangalan);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Nilalaman_VALUE.length; Loop_INDEX++) Stream_VALUE.write(Nilalaman_VALUE[Loop_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static String 읽기(String pangalan) throws I_O_pagbubukod {
        try { return 문자.i_decrypt_data(바이트읽기(pangalan));
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static void sumulat(String pangalan, String Nilalaman_VALUE) throws I_O_pagbubukod {
        try { sumulat_byte_VALUE(pangalan, 문자.부호화(Nilalaman_VALUE));
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
}
