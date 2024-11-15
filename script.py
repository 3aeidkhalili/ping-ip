import subprocess
import platform

# Display a banner
print("\033[1;32m")  # Set text color to green

print(r"""
   |___ /  __ _  ___(_) __| | | _| |__   __ _| (_) (_)
     |_ \ / _` |/ _ \ |/ _` | |/ / '_ \ / _` | | | | |
    ___) | (_| |  __/ | (_| |   <| | | | (_| | | | | |
   |____/ \__,_|\___|_|\__,_|_|\_\_| |_|\__,_|_|_|_|_|

    TeleGram ID : @s3aeidkhalili
""")

print("\033[0m")  # Reset text color

def ping_ip(ip, reachable_ips, unreachable_ips):
    """
    پینگ گرفتن از یک آی‌پی مشخص و ذخیره نتیجه در فایل
    """
    try:
        if platform.system().lower() == "windows":
            command = ["ping", "-n", "1", "-w", "1000", ip]
        else:
            command = ["ping", "-c", "1", "-W", "1", ip]
        
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if output.returncode == 0:
            # استخراج مقدار پینگ (Latency) در صورت موفق بودن
            if platform.system().lower() == "windows":
                latency = parse_latency_windows(output.stdout)
            else:
                latency = parse_latency_linux(output.stdout)
            result = f"{ip}: Reachable, Latency = {latency} ms\n"
            reachable_ips.append(result)  # افزودن به لیست آی‌پی‌های قابل دسترس
        else:
            result = f"{ip}: Unreachable\n"
            unreachable_ips.append(result)  # افزودن به لیست آی‌پی‌های غیر قابل دسترس
        
        print(result.strip())
    except Exception as e:
        unreachable_ips.append(f"{ip}: Error - {e}\n")

def parse_latency_linux(output):
    """
    استخراج مقدار پینگ از خروجی لینوکس/مک
    """
    try:
        for line in output.splitlines():
            if "time=" in line:
                latency = line.split("time=")[1].split(" ")[0]
                return latency
    except Exception:
        return "N/A"
    return "N/A"

def parse_latency_windows(output):
    """
    استخراج مقدار پینگ از خروجی ویندوز
    """
    try:
        for line in output.splitlines():
            if "time=" in line.lower():
                latency = line.split("time=")[1].split("ms")[0].strip()
                return latency
    except Exception:
        return "N/A"
    return "N/A"

def generate_ips(base_ip):
    """
    تولید آی‌پی‌ها در محدوده 1 تا 225 بر اساس آی‌پی پایه
    """
    ip_parts = base_ip.split(".")
    if len(ip_parts) != 4:
        raise ValueError("Invalid IP address format")
    
    base = ".".join(ip_parts[:3])
    return [f"{base}.{i}" for i in range(1, 226)]

def main():
    base_ip = input("Enter the base IP (e.g., 192.168.1.0): ")
    output_file = "ping_results.txt"
    reachable_ips = []  # لیست آی‌پی‌های قابل دسترس
    unreachable_ips = []  # لیست آی‌پی‌های غیر قابل دسترس

    try:
        ips = generate_ips(base_ip)
        for ip in ips:
            ping_ip(ip, reachable_ips, unreachable_ips)
        
        # مرتب‌سازی نتایج: ابتدا آی‌پی‌های قابل دسترس، سپس غیر قابل دسترس
        reachable_ips.sort()  # مرتب‌سازی آی‌پی‌های قابل دسترس
        unreachable_ips.sort()  # مرتب‌سازی آی‌پی‌های غیر قابل دسترس

        # نوشتن نتایج در فایل به ترتیب: ابتدا آی‌پی‌های قابل دسترس، سپس غیر قابل دسترس
        with open(output_file, "w") as file:
            file.writelines(reachable_ips)
            file.writelines(unreachable_ips)

        print(f"Results saved in {output_file}")
    except ValueError as ve:
        print(ve)

if __name__ == "__main__":
    main()
