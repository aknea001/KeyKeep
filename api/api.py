from backend import backend, encrypt
from api.exBackendConnection import ExBkC

class Api():
    def __init__(self, exBackend: bool, host: str = None, port: int = None):
        self.exBackend = ExBkC(host, port) if exBackend else False

    def login(self, user: str, passwd: str) -> bool:
        if self.exBackend:
            res = self.exBackend.login(user, passwd)

            if not res["success"]:
                print(f"Login error: {res['code']}")
                return False
            
            return True
        
        res = backend.rightMaster(passwd, user)

        if not res[0]:
            return False

        salt = backend.getSalt(user)[1]
        kek = encrypt.pbkdf2(passwd.encode(), salt.encode(), 100000, 32)
        self.AESkey = encrypt.decryptDek(kek, res[2], res[1])

        self.user = user

        return True
    
    def insert(self, passwd: str, title: str = None, username: str = None):
        if self.exBackend:
            res = self.exBackend.insert(passwd, title, username)

            if not res["success"]:
                print(f"Insert error: {res['code']}")
                return False
            
            return True
        
        backend.insert(self.user, self.AESkey, passwd, title, username)
        return
    
    def update(self, upID: int, passwd: str):
        if self.exBackend:
            res = self.exBackend.update(upID, passwd)

            if not res["success"]:
                print(f"Update error: {res['code']}")
                return False
            
            return True
        
        backend.update(self.user, self.AESkey, upID, passwd)
        return
    
    def get(self, upID: int, headless: bool):
        if self.exBackend:
            res = self.exBackend.get(upID)

            if not res["success"]:
                print(f"Get error: {res['code']}")
                return False
            
            backend.copyToClipboard(res["passwd"], headless)
            return True
        
        backend.get(self.AESkey, upID, self.user, headless)
        return
    
    def remove(self, upID: int):
        if self.exBackend:
            res = self.exBackend.remove(upID)

            if not res["success"]:
                print(f"Remove error: {res['code']}")
                return False
            
            return True
        
        backend.remove(upID, self.user)
        return
    
    def addUser(self, name: str, passwd: str):
        if self.exBackend:
            res = self.exBackend.addUser(name, passwd)

            if not res["success"]:
                print(f"Add user error: {res['code']}")
                return False
            
            return True
        
        backend.addUser(name, passwd)
        return
    
    def tableData(self) -> dict:
        if self.exBackend:
            res = self.exBackend.tableData()

            if not res["success"]:
                print(f"Table data error: {res['code']}")
                return False
            
            return {"success": True, "data": res["data"]}
        
        res = backend.tableInfo(self.user)

        return {"success": True, "data": res}