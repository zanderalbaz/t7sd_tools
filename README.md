# LabJack T7 SD Tools

We created these tools to help create a more user-friendly way of interacting with the LabJack T7 data aquisition device. Our primary use case of these tools are to manage the telemetry for several LabJacks deployed remotely. We currently support 2 tools: the t7sd API and the t7sd shell.

## T7SD API
This API is written on top of LabJack's sd_utils.py program which can be found in the Example SD section of [LabJack's GitHub](https://github.com/labjack/labjack-ljm-python/tree/master), which focuses on performing SD operations using the LJM library. We have essentially written a wrapper for this file, which supports better OOP principles, and some extended functionality.

For examples on how to use this API, check out the [API Documentation](https://github.com/zanderalbaz/t7sd_tools/tree/development/t7sd_api).



## T7SD Shell
We took many of the commands from the T7SD API, and made a REPL shell for more fine-grained interaction with the LabJack. There are 2 shell modes:
1. Regular Shell
    A. This serves as an interactive shell for a single LabJack device.
    B. Usage:
    ```
        \...\t7sd_tools> python -m t7sd_shell.t7sd_shell [--identifier (ANY, 192.168.1.4, etc.)]
    ```
    It is highly-recommended to use an IP as the identifier if you are working with devices remotely.
2. Batch Shell
    A. Accepts a list of devices and a list of REPL-style commands and performs all commands on each device.
    B. Usage:
    ```
        \...\t7sd_tools> python -m t7sd_shell.batch --devices DEVICES --commands COMMANDS \
         [--parallel NUM_THREADS] \
         [--log-dir LOG_DIR] \
         [--stop-on-error]
    ```

For examples on how to use the shell/batch shell, check out the [Shell Documentation](https://github.com/zanderalbaz/t7sd_tools/tree/development/t7sd_shell).
