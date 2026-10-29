// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** A thread is one execution flow. The built-in JVM alternates flows according to executed instruction counts. */
public final class performTask {
    private performTask() {}
    public static worker run(RunnableTask TaskAction) { worker threadValue = new worker(TaskAction); threadValue.startTask(); return threadValue; }
    public static void await(worker threadValue) throws WaitInterruptedException { threadValue.await(); }
    public static boolean isAlive(worker threadValue) { return threadValue.isAlive(); }
    public static void yieldTask() { worker.yieldTask(); }
}
