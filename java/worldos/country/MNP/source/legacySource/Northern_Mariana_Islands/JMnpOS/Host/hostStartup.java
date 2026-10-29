// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Northern_Mariana_Islands.JMnpOS.Host;

import Northern_Mariana_Islands.JMnpOS.Kernel.Kernel;

public final class hostStartup {
    private hostStartup() {
    }

    public static void main(String[] parameterArgument) {
        Kernel kernelValue = new Kernel(new HostHardware());
        kernelValue.run();
        kernelValue.executeStep();
    }
}

