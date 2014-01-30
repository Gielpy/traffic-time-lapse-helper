import webbrowser
def promptDependency(need, url):
  print ('You need %s.\nOpening a browser...') % need
  webbrowser.open(url, new=2)