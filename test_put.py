from requests import put


print(put('http://127.0.0.1:5000/api/jobs/9', 
      json={'work_size': 1,}).json())