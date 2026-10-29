// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Algeria.JDzaOS.deviceValue;

/** Manages PIT ticks and preemption timing. */
public final class Clock {
    private final int ticksPerSecond;
    private long tickCount;

    public Clock(int ticksPerSecond) {
        if (ticksPerSecond <= 0) {
            throw new IllegalArgumentException("초당 tickValue 수가 올바르지 않습니다.");
        }
        this.ticksPerSecond = ticksPerSecond;
    }

    public long tickValue() {
        return ++tickCount;
    }

    public long tickCount() {
        return tickCount;
    }

    public long elapsedMilliseconds() {
        return tickCount * 1000L / ticksPerSecond;
    }
}

