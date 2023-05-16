import configparser
from pyVim import connect
from pyVmomi import vim


class Explorer:
    def __init__(self) -> None:
        # danh sách đường dẫn đến file unknown command xử cần xử lý
        self.paths = []
        # danh sách các host backend.
        self.config = configparser.ConfigParser()
        self.config.read("explorer/vmlist.cfg")
        self.hosts_info = {}
        for vm in self.config.sections():
            self.hosts_info[vm] = {}
            self.hosts_info[vm]["host"] = self.config[vm].get("host")
            self.hosts_info[vm]["username"] = self.config[vm].get("username")
            self.hosts_info[vm]["password"] = self.config[vm].get("password")
        pass

    def shutdown_process(self):
        pass

    def vm_complete(self):
        pass

    def process_file(self):
        pass

    def test(self):
        for vm in self.hosts_info:
            try:
                host_ip = self.hosts_info[vm]["host"]
                username = self.hosts_info[vm]["username"]
                password = self.hosts_info[vm]["password"]
                si = connect.SmartConnection(
                    host=host_ip,
                    user=username,
                    pwd=password,
                )
                print("Connection successful.")
                connect.Disconnect(si=si)
            except Exception as e:
                print(f"Connection failed: {e}")


if __name__ == "__main__":
    explorer = Explorer()
    explorer.test()
