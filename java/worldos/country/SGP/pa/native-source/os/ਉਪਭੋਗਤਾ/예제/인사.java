// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ਚਲਾਓ_2() {
        ਉਪਭੋਗਤਾ.ਲਿਖਣ("Hello from a separate Java ELF!\n");
        ਉਪਭੋਗਤਾ.ਲਿਖਣ(ਉਪਭੋਗਤਾ.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ਅਨੁਕ੍ਰਮਣਿਕਾ = 0; ਅਨੁਕ੍ਰਮਣਿਕਾ < ਉਪਭੋਗਤਾ.인수개수(); ਅਨੁਕ੍ਰਮਣਿਕਾ++) {
            ਉਪਭੋਗਤਾ.ਲਿਖਣ("arg: "); ਉਪਭੋਗਤਾ.ਲਿਖਣ(ਉਪਭੋਗਤਾ.ਆਰਗੂਮੈਂਟ(ਅਨੁਕ੍ਰਮਣਿਕਾ)); ਉਪਭੋਗਤਾ.ਲਿਖਣ("\n");
        }
        return ਉਪਭੋਗਤਾ.실행권한() == 3 ? 0 : 1;
    }
}
