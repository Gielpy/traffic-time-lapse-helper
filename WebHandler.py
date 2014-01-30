import time
from promptDependency import promptDependency
try:
  from selenium import webdriver
  from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
except:
  promptDependency('Selenium for Python',
    'https://pypi.python.org/pypi/selenium')
  promptDependency('PhantomJS',
      'http://phantomjs.org/download.html')
  exit()

class WebHandler:
  browser = None

  ##############################################################################
  # sets up Selenium
  def __init__(self, visual=False):
    # uses visible Firefox window, for debugging
    if visual:
      self.browser = webdriver.Firefox()
    # normally, invisible PhantomJS
    else:
      try:
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
          "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
          "(KHTML, like Gecko) Chrome/15.0.87"
        )
        self.browser = webdriver.PhantomJS('phantomjs', desired_capabilities=dcap)
      except:
        promptDependency('PhantomJS', 'http://phantomjs.org/download.html')
        exit()

    self.browser.set_window_size(1920,1080)

  ##############################################################################
  # screenshots a site on an interval
  def screenshot(self, site, filename):
    self.browser.get(site)
    time.sleep(3) # allow scripts and data to populate

    self.browser.save_screenshot(filename)
    print('saved screenshot.')
    return True