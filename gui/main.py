import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import subprocess
import socket
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import client1

class DataComGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Veri İletişimi Hata Tespit Sistemi")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        self.server_process = None
        self.client2_process = None
        self.server_running = False
        self.client2_running = False
        
        self.setup_ui()
        
    def check_port(self, port):
        """Check if a port is available."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0 # Returns True if port is free (connect failed), False if in use
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = ttk.Label(main_frame, text="Veri İletişimi Hata Tespit Sistemi", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        control_frame = ttk.LabelFrame(main_frame, text="Sistem Kontrolü", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.start_all_btn = ttk.Button(control_frame, text="🚀 Sistemi Başlat", 
                                        command=self.start_system_like_runpy)
        self.start_all_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.stop_all_btn = ttk.Button(control_frame, text="⏹️  Tümünü Durdur", 
                                      command=self.stop_all_services, state=tk.DISABLED)
        self.stop_all_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.reset_btn = ttk.Button(control_frame, text="🔄 Sıfırla", 
                                   command=self.reset_system, state=tk.DISABLED)
        self.reset_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.server_status = ttk.Label(control_frame, text="Server: Kapalı", foreground="red")
        self.server_status.grid(row=1, column=0, pady=5)
        
        self.client2_status = ttk.Label(control_frame, text="Client 2: Kapalı", foreground="red")
        self.client2_status.grid(row=1, column=1, pady=5)
        
        self.system_status = ttk.Label(control_frame, text="Sistem: Hazır", foreground="green")
        self.system_status.grid(row=1, column=2, pady=5)
        
        input_frame = ttk.LabelFrame(main_frame, text="Veri Gönder", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(input_frame, text="Gönderilecek Metin:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.text_entry = ttk.Entry(input_frame, width=50)
        self.text_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Label(input_frame, text="Hata Tespit Yöntemi:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.method_var = tk.StringVar(value="CRC")
        method_combo = ttk.Combobox(input_frame, textvariable=self.method_var, 
                                    values=["PARITY", "PARITY2D", "CRC", "HAMMING", "CHECKSUM"],
                                    state="readonly", width=47)
        method_combo.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        send_btn = ttk.Button(input_frame, text="Gönder", command=self.send_data)
        send_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
        output_frame = ttk.LabelFrame(main_frame, text="Sonuçlar ve Loglar", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, width=80, 
                                                     wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        clear_btn = ttk.Button(output_frame, text="Logları Temizle", command=self.clear_logs)
        clear_btn.grid(row=1, column=0, pady=5)
        
        main_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        output_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
    def log_message(self, message):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        
    def clear_logs(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
    def start_system_like_runpy(self):
        import time
        self.log_message("="*50)
        self.log_message("Sistem başlatılıyor (run.py modu)...")
        self.log_message("="*50)

        # Check ports first
        if not self.check_port(8888):
            self.log_message("✗ HATA: Port 8888 dolu! Server başlatılamıyor.")
            messagebox.showerror("Port Hatası", "Port 8888 kullanımda. Lütfen çalışan diğer sunucuları kapatın.")
            return
            
        if not self.check_port(9999):
            self.log_message("✗ HATA: Port 9999 dolu! Client 2 başlatılamıyor.")
            messagebox.showerror("Port Hatası", "Port 9999 kullanımda. Lütfen çalışan diğer uygulamaları kapatın.")
            return
        
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        try:
            server_path = os.path.join(project_dir, "server.py")
            self.log_message(f"[DEBUG] Server path: {server_path}")
            self.log_message(f"[DEBUG] Server file exists: {os.path.exists(server_path)}")
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            self.server_process = subprocess.Popen([sys.executable, '-u', server_path],
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.STDOUT,
                                                  bufsize=0,
                                                  universal_newlines=True,
                                                  env=env,
                                                  cwd=project_dir)
            self.server_running = True
            self.server_status.config(text="Server: Çalışıyor", foreground="green")
            self.log_message("✓ Server başlatıldı")
            threading.Thread(target=self.monitor_server, daemon=True).start()
            time.sleep(0.5)
            
            client2_path = os.path.join(project_dir, "client2.py")
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            self.client2_process = subprocess.Popen([sys.executable, '-u', client2_path],
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT,
                                                    bufsize=0,
                                                    universal_newlines=True,
                                                    env=env,
                                                    cwd=project_dir)
            self.client2_running = True
            self.client2_status.config(text="Client 2: Çalışıyor", foreground="green")
            self.log_message("✓ Client 2 başlatıldı")
            self.log_message(f"[DEBUG] Client2 process PID: {self.client2_process.pid}")
            threading.Thread(target=self.monitor_client2, daemon=True).start()
            time.sleep(0.5)
            
            self.start_all_btn.config(state=tk.DISABLED)
            self.stop_all_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)
            self.system_status.config(text="Sistem: Çalışıyor", foreground="green")
            self.log_message("✓ Sistem hazır! Veri gönderebilirsiniz.")
            self.log_message("="*50)
            
        except Exception as e:
            self.log_message(f"✗ Sistem başlatılamadı: {e}")
            messagebox.showerror("Hata", f"Sistem başlatılamadı:\n{e}")
            
    def start_all_services(self):
        if not self.server_running:
            self.start_server()
        if not self.client2_running:
            self.start_client2()
            
        if self.server_running and self.client2_running:
            self.start_all_btn.config(state=tk.DISABLED)
            self.stop_all_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)
            self.log_message("✓ Tüm servisler başlatıldı")
            
    def start_server(self):
        try:
            if not self.check_port(8888):
                self.log_message("✗ HATA: Port 8888 dolu!")
                messagebox.showerror("Port Hatası", "Port 8888 kullanımda.")
                return

            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            server_path = os.path.join(project_dir, "server.py")
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            self.server_process = subprocess.Popen([sys.executable, '-u', server_path],
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.STDOUT,
                                                  bufsize=0,
                                                  universal_newlines=True,
                                                  env=env,
                                                  cwd=project_dir)
            self.server_running = True
            self.server_status.config(text="Server: Çalışıyor", foreground="green")
            self.log_message("✓ Server başlatıldı")
            threading.Thread(target=self.monitor_server, daemon=True).start()
        except Exception as e:
            self.log_message(f"✗ Server başlatılamadı: {e}")
            
    def start_client2(self):
        try:
            if not self.check_port(9999):
                self.log_message("✗ HATA: Port 9999 dolu!")
                messagebox.showerror("Port Hatası", "Port 9999 kullanımda.")
                return

            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            client2_path = os.path.join(project_dir, "client2.py")
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            self.client2_process = subprocess.Popen([sys.executable, '-u', client2_path],
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT,
                                                    bufsize=0,
                                                    universal_newlines=True,
                                                    env=env,
                                                    cwd=project_dir)
            self.client2_running = True
            self.client2_status.config(text="Client 2: Çalışıyor", foreground="green")
            self.log_message("✓ Client 2 başlatıldı")
            
            threading.Thread(target=self.monitor_client2, daemon=True).start()
        except Exception as e:
            self.log_message(f"✗ Client 2 başlatılamadı: {e}")
            
    def monitor_server(self):
        while self.server_running and self.server_process:
            try:
                if self.server_process.poll() is not None:
                    exit_code = self.server_process.poll()
                    msg = f"[SERVER] Process terminated with code {exit_code}"
                    self.root.after(0, self.log_message, msg)
                    if exit_code != 0:
                        self.root.after(0, self.server_status.config, {"text": "Server: Hata!", "foreground": "red"})
                    else:
                        self.root.after(0, self.server_status.config, {"text": "Server: Kapalı", "foreground": "red"})
                    break
                
                line = self.server_process.stdout.readline()
                if line:
                    line = line.strip()
                    if line:
                        self.root.after(0, self.log_message, f"[SERVER] {line}")
                else:
                    import time
                    time.sleep(0.01)
                    
            except Exception as e:
                self.root.after(0, self.log_message, f"[ERROR] Server monitor: {e}")
                break
                
    def monitor_client2(self):
        while self.client2_running and self.client2_process:
            try:
                if self.client2_process.poll() is not None:
                    exit_code = self.client2_process.poll()
                    msg = f"[CLIENT2] Process terminated with code {exit_code}"
                    self.root.after(0, self.log_message, msg)
                    if exit_code != 0:
                        self.root.after(0, self.client2_status.config, {"text": "Client 2: Hata!", "foreground": "red"})
                    else:
                        self.root.after(0, self.client2_status.config, {"text": "Client 2: Kapalı", "foreground": "red"})
                    break
                
                line = self.client2_process.stdout.readline()
                if line:
                    line = line.strip()
                    if line:
                        self.root.after(0, self.log_message, f"[CLIENT2] {line}")
                else:
                    import time
                    time.sleep(0.01)
                    
            except Exception as e:
                self.root.after(0, self.log_message, f"[ERROR] Client2 monitor: {e}")
                break
                
    def stop_all_services(self):
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=2)
            except:
                try:
                    self.server_process.kill()
                except:
                    pass
            self.server_process = None
            self.server_running = False
            self.server_status.config(text="Server: Kapalı", foreground="red")
            self.log_message("✗ Server durduruldu")
            
        if self.client2_process:
            try:
                self.client2_process.terminate()
                self.client2_process.wait(timeout=2)
            except:
                try:
                    self.client2_process.kill()
                except:
                    pass
            self.client2_process = None
            self.client2_running = False
            self.client2_status.config(text="Client 2: Kapalı", foreground="red")
            self.log_message("✗ Client 2 durduruldu")
            
        self.start_all_btn.config(state=tk.NORMAL)
        self.stop_all_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)
        self.system_status.config(text="Sistem: Durduruldu", foreground="red")
        
    def reset_system(self):
        self.log_message("="*50)
        self.log_message("Sistem sıfırlanıyor...")
        self.log_message("="*50)
        
        self.stop_all_services()
        self.clear_logs()
        self.text_entry.delete(0, tk.END)
        self.method_var.set("CRC")
        
        self.system_status.config(text="Sistem: Hazır", foreground="green")
        self.log_message("✓ Sistem sıfırlandı. Yeniden başlatabilirsiniz.")
        
    def generate_control_info(self, data, method):
        return client1.generate_control_info(data, method)
                
    def send_data(self):
        if not self.server_running:
            messagebox.showwarning("Uyarı", "Önce server ve client2'yi başlatın!")
            return
            
        text = self.text_entry.get().strip()
        if not text:
            messagebox.showwarning("Uyarı", "Lütfen gönderilecek metni girin!")
            return
            
        method = self.method_var.get()
        control_info = self.generate_control_info(text, method)
        packet = f"{text}|{method}|{control_info}"
        
        self.log_message("\n" + "="*50)
        self.log_message("Gönderilen Paket:")
        self.log_message(f"Veri                 : {text}")
        self.log_message(f"Yöntem               : {method}")
        self.log_message(f"Kontrol Bilgisi       : {control_info}")
        self.log_message("="*50)
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            self.log_message(f"[DEBUG] Connecting to localhost:8888 (server port)")
            sock.connect(('localhost', 8888))
            self.log_message(f"[DEBUG] Connected! Sending packet: {packet}")
            sock.sendall(packet.encode('utf-8'))
            sock.close()
            self.log_message("✓ Paket başarıyla gönderildi (server'a iletildi)")
            self.log_message("[DEBUG] Waiting for Client2 response...")
            import time
            time.sleep(0.1)
        except Exception as e:
            self.log_message(f"✗ Paket gönderilemedi: {e}")
            messagebox.showerror("Hata", f"Paket gönderilemedi:\n{e}")
            
    def on_closing(self):
        self.stop_all_services()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = DataComGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == '__main__':
    main()

