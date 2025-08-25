import requests

class ExBkC():
    def __init__(self, host: str, port: int = None):
        self.baseUrl = host

        if port:
            self.baseUrl += f":{port}"
        
        self.session = requests.Session()
    
    def login(self, user: str, passwd: str) -> dict:
        body = {"user": user, "passwd": passwd}

        with self.session as s:
            res = s.post(self.baseUrl + "/login", json=body)
        
        if res.status_code != 200:
            return {"success": False, "code": res.status_code}
        
        self.token = res.json()["accessToken"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.session.headers.update(self.headers)

        self.masterPasswd = passwd

        return {"success": True}
    
    def insert(self, passwd: str, title: str = None, username: str = None) -> dict:
        body = {"masterPasswd": self.masterPasswd, "passwd": passwd}

        if title:
            body["title"] = title
        
        if username:
            body["username"] = username

        with self.session as s:
            res = s.post(self.baseUrl + "/insert", json=body)
        
        if res.status_code != 200:
            return {"success": False, "code": res.status_code, "msg": res.json()}
        
        return {"success": True}
    
    def update(self, upID: int, passwd: str) -> dict:
        body = {"masterPasswd": self.masterPasswd, "upID": upID - 1, "passwd": passwd}

        with self.session as s:
            res = s.patch(self.baseUrl + "/update", json=body)
        
        if res.status_code != 200:
            return {"success": False, "code": res.status_code, "msg": res.json()}
        
        return {"success": True}
    
    def get(self, upID: int) -> dict:
        body = {"masterPasswd": self.masterPasswd, "upID": upID - 1}

        with self.session as s:
            res = s.post(self.baseUrl + "/get", json=body)
        
        if res.status_code != 200:
            return {"success": False, "code": res.status_code, "msg": res.json()}
        
        return {"success": True, "passwd": res.json()[0]}
    
    def remove(self, upID: int) -> dict:
        with self.session as s:
            res = s.delete(self.baseUrl + f"/remove?upID={upID - 1}")
        
        if res.status_code != 200:
            return {"success": False, "code": res.status_code, "msg": res.json()}
        
        return {"success": True}
    
    def addUser(self, name: str, passwd: str) -> dict:
        body = {"name": name, "passwd": passwd}

        with self.session as s:
            res = s.post(self.baseUrl + "/addUser", json=body)

        if res.status_code != 200:
            return {"success": False, "code": res.status_code, "msg": res.json()}
        
        return {"success": True}
    
    def tableData(self) -> dict:
        with self.session as s:
            res = s.get(self.baseUrl + "/tableData")
        
        if res.status_code != 200:
            return {"success": False, "code": res.status_code, "msg": res.json()}
        
        return {"success": True, "data": res.json()}