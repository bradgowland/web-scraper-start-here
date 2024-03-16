# web-scraper-start-here
A springboard for scraping. Currently fetches albums and artists from the homepage for Aquarium Drunkard, save outputs to a local directory CSV. Just punch in whatever you're looking for and update the parsing function in `tasks/extract`.

# getting started
Create a directory for the project.
```
$ cd dev/
$ mkdir my-scraper
$ cd my-scraper
```

Clone this repo.
```
$ git@github.com:bradgowland/web-scraper-start-here.git
```

Setup environment and install dependencies.
```
$        python -m venv venv
$        . /venv/bin/activate
$ (venv) pip install -r requirements.txt
```

Run the basic app.
```
$ python scraper.py --task run
```

# spellbook
Web scraping is often just casting magic spells that follow no discernable rules, so I'm leaving all these here:

```
# finding stuff with selenium
css_elements = driver.find_elements_by_css_selector("[attribute-name='attribute']")
xpath_elements = driver.find_elements_by_xpath('full-xpath-here')
element_with_text = driver.find_elements_by_xpath('//*[contains(text(), \'Search Text\')]')
tag_elements = driver.find_elements_by_tag_name('tag_name')
element_starts_with_title = driver.find_element_by_css_selector("[title^='Title Starts With This']")
element_contains_title = driver.find_element_by_css_selector("[title*='Title Contains This']")

# getting stuff with selenium
text_of_element = element.text
attribute_of_element = element.get_attribute('attribute_name')

# navigating with selenium (scroll down)
from selenium.webdriver.common.keys import Keys
html = driver.find_element_by_tag_name('html')
html.send_keys(Keys.END)
```
