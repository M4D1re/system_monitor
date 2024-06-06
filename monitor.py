import wmi
import psutil
import tkinter as tk

class SystemInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Information")
        self.root.geometry("600x400")

        self.cpu_label = tk.Label(root, text="CPU Information:")
        self.cpu_label.pack()

        self.cpu_info = tk.Text(root, height=10, width=50)
        self.cpu_info.pack()

        self.gpu_label = tk.Label(root, text="GPU Information:")
        self.gpu_label.pack()

        self.gpu_info = tk.Text(root, height=10, width=50)
        self.gpu_info.pack()

        self.memory_label = tk.Label(root, text="Memory Information:")
        self.memory_label.pack()

        self.memory_info = tk.Text(root, height=10, width=50)
        self.memory_info.pack()

        self.update_info()

    def get_cpu_info(self):
        c = wmi.WMI()
        cpu_data = ""
        for processor in c.Win32_Processor():
            cpu_data += "Processor Name: {}\n".format(processor.Name)
            cpu_data += "Current Clock Speed: {} MHz\n".format(processor.CurrentClockSpeed)
            cpu_data += "Max Clock Speed: {} MHz\n".format(processor.MaxClockSpeed)
            cpu_data += "Cores: {}\n".format(processor.NumberOfCores)
            cpu_data += "Threads: {}\n".format(processor.NumberOfLogicalProcessors)
            try:
                temp = psutil.sensors_temperatures().get('coretemp', [])
                if temp:
                    cpu_data += "Temperature: {} °C\n".format(temp[0].current)
                else:
                    cpu_data += "Temperature: N/A\n"
            except Exception as e:
                cpu_data += "Temperature: Error {}\n".format(e)
            cpu_data += "Load Percentage: {} %\n".format(processor.LoadPercentage)
            cpu_data += "--------------------\n"
        return cpu_data

    def get_gpu_info(self):
        c = wmi.WMI()
        gpu_data = ""
        for gpu in c.Win32_VideoController():
            gpu_data += "GPU Name: {}\n".format(gpu.Name)
            gpu_data += "Current Refresh Rate: {} Hz\n".format(gpu.CurrentRefreshRate)
            gpu_data += "Adapter Compatibility: {}\n".format(gpu.AdapterCompatibility)
            gpu_data += "Adapter RAM: {} bytes\n".format(gpu.AdapterRAM)
            gpu_data += "Video Processor: {}\n".format(gpu.VideoProcessor)
            gpu_data += "--------------------\n"
        return gpu_data

    def get_memory_info(self):
        c = wmi.WMI()
        memory_data = ""
        for mem in c.Win32_PhysicalMemory():
            memory_data += "Memory Bank: {}\n".format(mem.BankLabel)
            memory_data += "Capacity: {} bytes\n".format(mem.Capacity)
            memory_data += "Speed: {} MHz\n".format(mem.Speed)
            memory_data += "Manufacturer: {}\n".format(mem.Manufacturer)
            memory_data += "--------------------\n"
        return memory_data

    def update_info(self):
        cpu_data = self.get_cpu_info()
        gpu_data = self.get_gpu_info()
        memory_data = self.get_memory_info()

        self.cpu_info.delete(1.0, tk.END)
        self.gpu_info.delete(1.0, tk.END)
        self.memory_info.delete(1.0, tk.END)

        self.cpu_info.insert(tk.END, cpu_data)
        self.gpu_info.insert(tk.END, gpu_data)
        self.memory_info.insert(tk.END, memory_data)

        self.root.after(1000, self.update_info)

def main():
    root = tk.Tk()
    app = SystemInfoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()