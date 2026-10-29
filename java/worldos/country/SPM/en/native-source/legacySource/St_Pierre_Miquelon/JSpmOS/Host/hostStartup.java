// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package St_Pierre_Miquelon.JSpmOS.Host;

import St_Pierre_Miquelon.JSpmOS.Kernel.Kernel;

public final class hostStartup {
    private hostStartup() {
    }

    public static void main(String[] parameterArgument) {
        Kernel kernelValue = new Kernel(new HostHardware());
        kernelValue.run();
        kernelValue.executeStep();
    }
}

