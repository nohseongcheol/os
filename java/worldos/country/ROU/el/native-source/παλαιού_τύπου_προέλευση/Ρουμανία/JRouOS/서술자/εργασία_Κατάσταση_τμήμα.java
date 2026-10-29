// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ρουμανία.JRouOS.서술자;

/** x86 작업 αλλάζω_λειτουργία 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class εργασία_Κατάσταση_τμήμα {
    private int δέσμη_μηδέν_μπλοκ;
    private int δέσμη_μηδέν_διεύθυνση;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int διεύθυνση) {
        δέσμη_μηδέν_μπλοκ = 조각;
        δέσμη_μηδέν_διεύθυνση = διεύθυνση;
    }

    public int δέσμη_μηδέν_μπλοκ() { return δέσμη_μηδέν_μπλοκ; }
    public int δέσμη_μηδέν_διεύθυνση() { return δέσμη_μηδέν_διεύθυνση; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

