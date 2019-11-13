import sys
import time
import unittest
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
tt = sys.argv
test_name = sys.argv[0].split('/')[-1].split('.')[0]
tc, set_em, set_mn, set_hr, role, des, res = test_name.split('_')
url = "http://stage.mytandem.eu"
db = "e2e"
oi = "Finance"
ln = 0
tst_type = 0
tst_counter = 0
is_first_login = True
default_timeout = 10

users = {'em': 'Martha.Robinson@email.com',             # employee
         'em1': 'Jenny.Thompson@email.com',             # employee1
         'oi_usr': 'Gerry.Harris@email.com',            # OI user
         'mn': 'Dermot.Jackson@email.com',              # manager
         'sub': 'David.Wilson@email.com',               # sub
         'hr': 'alison.johnson@email.com',              # HR
         'hr_mn': 'Jamie.Duggan@email.com',             # HR+manager
         'hr_mn_direct': 'Tina.Delaney@email.com',      # HR+manager direct
         'admin': 'Barry.Deegan@email.com'}             # admin


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    @staticmethod
    def tst_log():
        global test_name
        text = test_name + "_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        print(text + " ...")  # assign_to
        return text

    def tst_login(self, usr):
        # Enter Company
        global is_first_login
        if is_first_login:
            is_first_login = False
            self.driver.find_element_by_id('e2e-company-name').send_keys(db)
            self.driver.find_element_by_id('e2e-continue-button').click()
        self.driver.find_element_by_id('e2e-username').send_keys(usr)
        self.driver.find_element_by_id('e2e-password').send_keys("pass")
        self.driver.find_element_by_id('e2e-login-button').click()
        time.sleep(1)
        assert self.driver.find_element_by_id('e2e-user-profile')
        print("    Login as " + usr + ": - Ok")

    def tst_logout(self):
        self.driver.find_element_by_id("e2e-user-profile").click()
        self.driver.find_element_by_id("e2e-dropdown-profile-logout").click()
        self.driver.find_element_by_id("e2e-yes-button").click()
        print("    Logout: - Ok")

    def tst_settings(self, em, mg, hr):
        global users
        changed = False
        if em == "on":
            em = "true"
        else:
            em = "false"

        if mg == "on":
            mg = "true"
        else:
            mg = "false"

        if hr == "on":
            hr = "true"
        else:
            hr = "false"

        # wait10 = WebDriverWait(self.driver, 15)
        self.tst_login(users["admin"])
        #  self.tst_login("Barry.Deegan@email.com")
        # wait10.until(EC.element_to_be_clickable((By.ID, 'e2e-system-administration')))
        self.driver.find_element_by_id("e2e-system-administration").click()
        # wait10.until(EC.element_to_be_clickable((By.ID, 'e2e-manage-goals')))
        self.driver.find_element_by_id("e2e-manage-goals").click()
        # wait10.until(EC.element_to_be_clickable((By.ID, 'GoalsSettings_EnableAllowEmployeeToAssignToEveryone')))
        time.sleep(2)
        if self.driver.find_element_by_id("GoalsSettings_EnableAllowEmployeeToAssignToEveryone").get_attribute("data-value") != em:
            self.driver.find_element_by_id("GoalsSettings_EnableAllowEmployeeToAssignToEveryone").click()
            changed = True
        if self.driver.find_element_by_id("GoalsSettings_EnableAllowManagerToAssignToEveryone").get_attribute("data-value") != mg:
            self.driver.find_element_by_id("GoalsSettings_EnableAllowManagerToAssignToEveryone").click()
            changed = True
        if self.driver.find_element_by_id("GoalsSettings_EnableAllowHRToAssignToEveryone").get_attribute("data-value") != hr:
            self.driver.find_element_by_id("GoalsSettings_EnableAllowHRToAssignToEveryone").click()
            changed = True
        if changed:
            self.driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div[2]/div[12]/button').click()
            time.sleep(7)
        print("    Test settings: - Ok")
        self.tst_logout()

    def if_to_any_user(self, can):
        global role, users
        user_name = users["em1"].split(".")[0]
        tst_str = self.tst_log()
        self.tst_login(users[role])

        if can:
            # Click on "Assign Goals"
            self.driver.find_element_by_id("e2e-assign-goal").click()
            self.driver.find_element_by_id("Sendto:").send_keys(user_name)
            print("    Put destination: " + user_name + " - Ok")
            self.driver.find_element_by_class_name("found-item").click()
            print("    Recepient found: - Ok")

            # Enter Goal Type
            self.driver.find_element_by_class_name("select2-selection").click()
            self.driver.find_elements_by_class_name("select2-results__option")[0].click()
            # print("    Goal type set: - Ok")
            # Due Date set
            self.driver.find_element_by_id("newPriorityDueDate").send_keys("31/12/2030")
            # print("    Goal date set: - Ok")

            # Enter Goal Title
            # click on field before element find
            self.driver.find_elements_by_class_name("public-DraftEditorPlaceholder-inner")[0].click()
            self.driver.find_elements_by_class_name("public-DraftEditor-content")[0].send_keys(tst_str)
            # print("    Goal Title set: - Ok")

            # Send Button click
            self.driver.find_element_by_id("e2e-send-button").click()
            self.driver.find_element_by_id("e2e-primary-button").click()
            print("    Goal send: - Ok")

            #  Search Goal
            self.driver.find_element_by_id("e2e-main-search-field").send_keys(tst_str)
            self.driver.find_element_by_class_name("found-item").click()
            print("    Goal found by main search: - Ok")
            self.tst_logout()

            self.tst_login(users["em1"])
            self.tst_notifications(tst_str)
            self.tst_my_goals(tst_str)
            # self.tst_logout()

            # Login as a init user and notification delete
            # self.tst_login(users[role])
            # self.driver.find_element_by_id("e2e-desktop-notifications").click()
            # self.driver.find_element_by_id('e2e-view-all-notifications').click()
            # self.driver.find_element_by_class_name("delete-notification").click()
            # print("    Notification about Goal deleting deleted: - Ok")

        else:  # if cannot
            # if impossible to find
            self.driver.find_element_by_id("e2e-assign-goal").click()
            self.driver.find_element_by_id("Sendto:").send_keys(user_name)
            if len(self.driver.find_elements_by_class_name("found-item")) == 0:
                print("    Impossible to find: - Ok")
            else:
                print("!!!======== It is possible to find but should not! ========================================")
        self.tst_logout()

    def if_to_any_oi(self, can):
        global role, users, oi
        tst_str = self.tst_log()
        self.tst_login(users[role])

        if can:
            # Click on "Assign Goals"
            self.driver.find_element_by_id("e2e-assign-goal").click()
            self.driver.find_element_by_id("Sendto:").send_keys(oi)
            print("    Put destination: '" + oi + "' - Ok")
            self.driver.find_elements_by_class_name("found-item")[3].click()
            print("    OI found: - Ok")

            # Enter Goal Type
            self.driver.find_element_by_class_name("select2-selection").click()
            self.driver.find_elements_by_class_name("select2-results__option")[0].click()
            # print("    Goal type set: - Ok")
            # Due Date set
            self.driver.find_element_by_id("newPriorityDueDate").send_keys("31/12/2030")
            # print("    Goal date set: - Ok")

            # Enter Goal Title
            # click on field before element find
            self.driver.find_elements_by_class_name("public-DraftEditorPlaceholder-inner")[0].click()
            self.driver.find_elements_by_class_name("public-DraftEditor-content")[0].send_keys(tst_str)
            # print("    Goal Title set: - Ok")

            # Send Button click
            self.driver.find_element_by_id("e2e-send-button").click()
            self.driver.find_element_by_id("e2e-primary-button").click()
            print("    Goal send: - Ok")

            # Search Goal
            self.driver.find_element_by_id("e2e-main-search-field").send_keys(tst_str)
            self.driver.find_element_by_class_name("found-item").click()
            print("    Goal found by main search: - Ok")
            self.tst_logout()

            self.tst_login(users["oi_usr"])
            self.tst_notifications(tst_str)
            self.tst_my_goals(tst_str)
            # self.tst_logout()

            # Login as a init user and notification delete
            # self.tst_login(users[role])
            # self.driver.find_element_by_id("e2e-desktop-notifications").click()
            # self.driver.find_element_by_xpath("//*[@id='e2e-view-all-notifications']/a").click()
            # self.driver.find_element_by_class_name("delete-notification").click()
            # print("    Notification about Goal deleting deleted: - Ok")
        else:  # if cannot
            # if impossible to find
            self.driver.find_element_by_id("e2e-assign-goal").click()
            self.driver.find_element_by_id("Sendto:").send_keys(oi)
            if len(self.driver.find_elements_by_class_name("found-item")) == 0:
                print("    Impossible to find: - Ok")
            else:
                print("!!!======== It is possible to find but should not! ========================================")
        self.tst_logout()

    def if_to_all_company(self, can):
        global role, users
        tst_str = self.tst_log()
        self.tst_login(users[role])

        if can:
            # Click on "Assign Goals"
            self.driver.find_element_by_id("e2e-assign-goal").click()
            self.driver.find_element_by_id("Sendto:").send_keys("All Company")
            print("    Put destination: All Company - Ok")
            self.driver.find_element_by_class_name("found-item").click()
            print("    All Company found: - Ok")

            # Enter Goal Type
            self.driver.find_element_by_class_name("select2-selection").click()
            self.driver.find_elements_by_class_name("select2-results__option")[0].click()
            # print("    Goal type set: - Ok")
            # Due Date set
            self.driver.find_element_by_id("newPriorityDueDate").send_keys("31/12/2030")
            # print("    Goal date set: - Ok")

            # Enter Goal Title
            # click on field before element find
            self.driver.find_elements_by_class_name("public-DraftEditorPlaceholder-inner")[0].click()
            self.driver.find_elements_by_class_name("public-DraftEditor-content")[0].send_keys(tst_str)
            # print("    Goal Title set: - Ok")

            # Send Button click
            self.driver.find_element_by_id("e2e-send-button").click()
            self.driver.find_element_by_id("e2e-primary-button").click()
            print("    Goal send: - Ok")

            # Search Goal
            self.driver.find_element_by_id("e2e-main-search-field").send_keys(tst_str)
            self.driver.find_element_by_class_name("found-item").click()
            print("    Goal found by main search: - Ok")
            self.tst_logout()

            self.tst_login(users["em1"])
            self.tst_notifications(tst_str)
            self.tst_my_goals(tst_str)
            # self.tst_logout()

            # Login as a init user and notification delete
            # self.tst_login(users[role])
            # self.driver.find_element_by_id("e2e-desktop-notifications").click()
            # self.driver.find_element_by_xpath("//*[@id='e2e-view-all-notifications']/a").click()
            # self.driver.find_element_by_class_name("delete-notification").click()
            # print("    Notification about Goal deleting deleted: - Ok")
        else:  # if cannot
            # if impossible to find
            self.driver.find_element_by_id("e2e-assign-goal").click()
            self.driver.find_element_by_id("Sendto:").send_keys("All Company")
            if len(self.driver.find_elements_by_class_name("found-item")) == 0:
                print("    Impossible to find: - Ok")
            else:
                print("!!!======== It is possible to find but should not! ========================================")
        self.tst_logout()

    def if_my_direct_reports(self, can):
        global role, users
        tst_str = self.tst_log()
        self.tst_login(users[role])

        if can:
            # Click on "Assign Goals"
            self.driver.find_element_by_id("e2e-assign-goal").click()
            self.driver.find_element_by_id("Sendto:").send_keys("My direct reports")
            print("    Put destination: My direct reports - Ok")
            #
            if len(self.driver.find_elements_by_class_name("found-item")) == 0:
                print("!!!======== It is impossible to find 'My direct reports' =====================================")
                return
            self.driver.find_element_by_class_name("found-item").click()
            # print("    My direct reports: - Ok")

            # Enter Goal Type
            self.driver.find_element_by_class_name("select2-selection").click()
            self.driver.find_elements_by_class_name("select2-results__option")[0].click()
            # print("    Goal type set: - Ok")
            # Due Date set
            self.driver.find_element_by_id("newPriorityDueDate").send_keys("31/12/2030")
            # print("    Goal date set: - Ok")

            # Enter Goal Title
            # click on field before element find
            self.driver.find_elements_by_class_name("public-DraftEditorPlaceholder-inner")[0].click()
            self.driver.find_elements_by_class_name("public-DraftEditor-content")[0].send_keys(tst_str)
            # print("    Goal Title set: - Ok")

            # Send Button click
            self.driver.find_element_by_id("e2e-send-button").click()
            self.driver.find_element_by_id("e2e-primary-button").click()
            print("    Goal send: - Ok")

            # Search Goal
            self.driver.find_element_by_id("e2e-main-search-field").send_keys(tst_str)
            self.driver.find_element_by_class_name("found-item").click()
            print("    Goal found by main search: - Ok")
            self.tst_logout()

            if role == "mn":
                u = users["sub"]
            else:
                u = users["hr_mn_direct"]
            self.tst_login(u)
            self.tst_notifications(tst_str)
            self.tst_my_goals(tst_str)
            # self.tst_logout()

            # Login as a init user and notification delete
            # self.tst_login(users[role])
            # self.driver.find_element_by_id("e2e-desktop-notifications").click()
            # self.driver.find_element_by_xpath("//*[@id='e2e-view-all-notifications']/a").click()
            # self.driver.find_element_by_class_name("delete-notification").click()
            # print("    Notification about Goal deleting deleted: - Ok")
        else:  # if cannot
            # if impossible to find
            self.driver.find_element_by_id("e2e-assign-goal").click()
            self.driver.find_element_by_id("Sendto:").send_keys("My direct reports")
            if len(self.driver.find_elements_by_class_name("found-item")) == 0:
                print("    Impossible to find: - Ok")
            else:
                print("!!!======== It is possible to find but should not! ========================================")
        self.tst_logout()

    def if_direct_subordinate(self, can):
        global tst_counter, users, ln
        user_name = users["sub"].split(".")[0]
        tst_str = self.tst_log()
        self.tst_login(users["mn"])

        if can:
            # Click on "Assign Goals"
            self.driver.find_element_by_id("e2e-assign-goal").click()
            self.driver.find_element_by_id("Sendto:").send_keys(user_name)
            print("    Put destination: " + user_name + " - Ok")
            self.driver.find_element_by_class_name("found-item").click()
            print("    Recepient found: - Ok")

            # Enter Goal Type
            self.driver.find_element_by_class_name("select2-selection").click()
            self.driver.find_elements_by_class_name("select2-results__option")[0].click()
            # print("    Goal type set: - Ok")
            # Due Date set
            self.driver.find_element_by_id("newPriorityDueDate").send_keys("31/12/2030")
            # print("    Goal date set: - Ok")

            # Enter Goal Title
            # click on field before element find
            self.driver.find_elements_by_class_name("public-DraftEditorPlaceholder-inner")[0].click()
            self.driver.find_elements_by_class_name("public-DraftEditor-content")[0].send_keys(tst_str)
            # print("    Goal Title set: - Ok")

            # Send Button click
            self.driver.find_element_by_id("e2e-send-button").click()
            self.driver.find_element_by_id("e2e-primary-button").click()
            print("    Goal send: - Ok")

            #  Search Goal
            self.driver.find_element_by_id("e2e-main-search-field").send_keys(tst_str)
            self.driver.find_element_by_class_name("found-item").click()
            print("    Goal found by main search: - Ok")
            self.tst_logout()

            self.tst_login(users["sub"])
            self.tst_notifications(tst_str)
            self.tst_my_goals(tst_str)
            # self.tst_logout()

            # Login as a init user and notification delete
            # self.tst_login(users["mn"])
            # self.driver.find_element_by_id("e2e-desktop-notifications").click()
            # self.driver.find_element_by_xpath("//*[@id='e2e-view-all-notifications']/a").click()
            # self.driver.find_element_by_class_name("delete-notification").click()
            # print("    Notificaten about Goal deleting deleted: - Ok")
        else:  # if cannot
            # if impossible to find
            self.driver.find_element_by_id("e2e-assign-goal").click()
            self.driver.find_element_by_id("Sendto:").send_keys(user_name)
            if len(self.driver.find_elements_by_class_name("found-item")) == 0:
                print("    Impossible to find: - Ok")
            else:
                print("!!!======== It is possible to find but should not! ========================================")
        self.tst_logout()

    # def tst_notifications(self, ttitle):
    #     self.driver.find_element_by_id("e2e-desktop-notifications").click()
    #     # print("    Notifications click: - Ok")
    #     if self.driver.find_elements_by_id('e2e-view-all-notifications') == 0:
    #         print("!!!======== There are no notifications about Goal Assign! ======================================")
    #     else:
    #         self.driver.find_element_by_id('e2e-view-all-notifications').click()
    #         nt_list = self.driver.find_elements_by_xpath("//*[text()='" + ttitle + "']")
    #         if len(nt_list) > 0:
    #             # print("    Notifications are present: - Ok")
    #             for i in nt_list:
    #                 self.driver.find_element_by_class_name("delete-notification").click()
    #             print("    Notifications found and has deleted: - Ok")
    #         else:
    #             print("!!!======== There are no notifications about Goal Assign! ==================================")

    def tst_notifications(self, ttitle):
        self.driver.find_element_by_id("e2e-desktop-notifications").click()
        time.sleep(1)
        self.driver.find_element_by_id('e2e-view-all-notifications').click()
        assert self.driver.find_element_by_xpath("//*[text()='" + ttitle + "']")
        print("    Notifications: - Ok")

    def tst_my_goals(self, ttitle):
        wait10 = WebDriverWait(self.driver, 10)
        # Check in My Goalas
        self.driver.find_element_by_id("e2e-my-goals").click()
        assert self.driver.find_element_by_xpath("//h4[text()='" + ttitle + "']")
        print("    Goal in MyGoals: - Ok")

    def is_ok(self, can):
        global des
        if des == "any":
            self.if_to_any_user(can)
        elif des == "oi":
            self.if_to_any_oi(can)
        elif des == "all":
            self.if_to_all_company(can)
        elif des == "dir":
            self.if_my_direct_reports(can)
        elif des == "sub":
            self.if_direct_subordinate(can)
        else:
            print("Error in Python test file name!")

    def is_no_menu(self):
        global role, users
        tst_str = self.tst_log()
        self.tst_login(users[role])
        # If No Assign Goal available in the menu
        dr = self.driver
        dr.implicitly_wait(1)
        if len(self.driver.find_elements_by_id("e2e-assign-goal")) == 0:
            print("    No Assign Goal menu: - Ok")
        else:
            print("!!!======== Assign Goal menu pesent but should not! ========================================")
        dr.implicitly_wait(default_timeout)
        self.tst_logout()

    def do_testing(self):
        global set_em, set_mn, set_hr
        self.tst_settings(set_em, set_mn, set_hr)
        if res == "can":
            self.is_ok(True)
        elif res == "cannot":
            self.is_ok(False)
        elif res == "no":
            self.is_no_menu()
        else:
            self.tst_log()
            print("    Skipped...")

    def test_12180(self):
        global ln, url
        driver = self.driver
        driver.implicitly_wait(default_timeout)
        self.driver.get(url)
        self.do_testing()
        driver.close()


if __name__ == '__main__':
    unittest.main()
