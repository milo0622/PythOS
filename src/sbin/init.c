#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mount.h>
#include <sys/stat.h>

int main() {
    printf("Mounting virtual partitions... ");
    mkdir("/proc", 0755);
    mkdir("/sys", 0755);
    mkdir("/dev", 0755);

    mount("proc", "/proc", "proc", 0, NULL);
    mount("sysfs", "/sys", "sys", 0, NULL);
    mount("devtmpfs", "/dev", "devtmpfs", 0, NULL);
    printf("Done!\n");

    char *python_args[] = {"/usr/bin/python3", "/sbin/init.py", NULL};
    extern char **environ;

    setenv("HOME", "/root", 1);
    setenv("PATH", "/bin:/usr/bin:/sbin", 1);

    execve(python_args[0], python_args, environ);
    
    perror("Kernel panic triggered! ");
    return 0;
}
