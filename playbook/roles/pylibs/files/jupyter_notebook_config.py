# Set options for certfile, ip, password, and toggle off browser auto-opening
c.NotebookApp.certfile = u'/home/wsl/.jupyter/mycert.pem'
c.NotebookApp.keyfile = u'/home/wsl/.jupyter/mykey.key'
# Set ip to '*' to bind on all interfaces (ips) for the public server
c.NotebookApp.ip = '*'
# Important: Remember to change your password hash !!!
# password -> test123
c.NotebookApp.password = u'sha1:f47ed769c548:b04ccb624ed4c5cbda4095070cbef44bdb732e79'
c.NotebookApp.open_browser = False
c.NotebookApp.notebook_dir = '/mnt/wsl/working'

# It is a good idea to set a known, fixed port for server access
c.NotebookApp.port = 8888