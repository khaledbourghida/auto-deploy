import requests

class HttpClient :
    def get(self , url , headers=None , params=None) -> requests.Response:
        response = requests.get(
            url = url,
            params = params,
            headers = headers
        )
        
        return response
    
    
    def post(self , url , headers=None , json=None) -> requests.Response:
        response = requests.post(
            url = url,
            headers = headers,
            json = json
        )
        
        return response
    
    def put(self , url , headers = None , json = None) -> requests.Response :
        response = requests.put(
            url = url,
            headers = headers ,
            json = json
        )
        
        return response
    
    def delete(self , url , headers = None ) -> requests.Response :
        response = requests.delete(
            url = url,
            headers = headers
        )
        
        return response