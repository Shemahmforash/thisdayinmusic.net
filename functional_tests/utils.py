def navbar_active_element_text(browser):
    navbar = browser.find_element_by_class_name("navbar-nav")
    active_element = navbar.find_element_by_class_name("active").text
    return active_element
