import platform
import subprocess

import psutil


def run_powershell(command: str) -> str:
    """Run a PowerShell command and return its output."""
    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            command,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.strip()


def get_cpu_name() -> str:
    """Return the CPU name reported by Windows."""
    try:
        result = run_powershell(
            "(Get-CimInstance Win32_Processor).Name"
        )

        return result or "Unknown"
    except (subprocess.CalledProcessError, OSError):
        return "Unknown"


def get_gpu_names() -> list[str]:
    """Return the names of GPUs detected by Windows."""
    try:
        result = run_powershell(
            "(Get-CimInstance Win32_VideoController).Name"
        )

        if not result:
            return []

        return [
            line.strip()
            for line in result.splitlines()
            if line.strip()
        ]
    except (subprocess.CalledProcessError, OSError):
        return []


def get_windows_version() -> str:
    """Return the Windows edition reported by Windows."""
    try:
        result = run_powershell(
            "(Get-CimInstance Win32_OperatingSystem).Caption"
        )

        return result or "Unknown"
    except (subprocess.CalledProcessError, OSError):
        return "Unknown"


def get_system_info() -> dict:
    """Return basic system hardware and operating system information."""
    memory = psutil.virtual_memory()

    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "windows_version": get_windows_version(),
        "machine": platform.machine(),
        "processor": get_cpu_name(),
        "cpu_count": psutil.cpu_count(logical=True),
        "physical_cpu_count": psutil.cpu_count(logical=False),
        "memory_total_gb": round(memory.total / (1024**3), 2),
        "gpu_names": get_gpu_names(),
    }


def get_performance_info() -> dict:
    """Return current CPU and memory usage information."""
    memory = psutil.virtual_memory()

    return {
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "memory_usage_percent": memory.percent,
        "memory_used_gb": round(memory.used / (1024**3), 2),
        "memory_available_gb": round(memory.available / (1024**3), 2),
    }


def get_battery_info() -> dict | None:
    """Return battery information, or None if no battery is detected."""
    battery = psutil.sensors_battery()

    if battery is None:
        return None

    return {
        "percent": battery.percent,
        "plugged_in": battery.power_plugged,
        "seconds_remaining": battery.secsleft,
    }