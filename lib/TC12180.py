##########################################################################
#  TANDEM PROJECT (c) Arvosoftware
#  e2e test Assign Goal TC12180
#  Volodymyr.Dmytrenko@arvosoftware.com
##########################################################################

import unittest
from selenium import webdriver
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.support.wait import WebDriverWait

url = "http://stage.mytandem.eu"
db = "e2e"
oi = "Finance"
ln = 0
tst_type = 0
tst_counter = 0
is_first_login = True

users = {'em': 'Martha.Robinson@email.com',             # emploee
         'em1': 'Jenny.Thompson@email.com',             # emploee1
         'oi_usr': 'Gerry.Harris@email.com',            # OI user
         'mn': 'Dermot.Jackson@email.com',              # manager
         'sub': 'David.Wilson@email.com',               # sub
         'hr': 'alison.johnson@email.com',              # HR
         'hr_mn': 'Jamie.Duggan@email.com',             # HR+manager
         'hr_mn_direct': 'Tina.Delaney@email.com',      # HR+manager direct
         'admin': 'Barry.Deegan@email.com'}             # admin

main_matrix = [["for_em", "for_mn", "for_hr", "role", "any user", "any OI", "all company", "my direct reports", "direct subordinate"],
               ["True", "True", "True", "em", "can", "can", "can", "n/a", "n/a"],  # 1
               ["True", "True", "True", "mn", "can", "can", "can", "can", "can"],  # 2
               ["True", "True", "True", "hr", "can", "can", "can", "n/a", "n/a"],  # 3
               ["True", "True", "True", "hr_mn", "n/a", "n/a", "n/a", "n/a", "n/a"],  # 4
               ["True", "False", "True", "em", "can", "can", "can", "n/a", "n/a"],  # 5
               ["True", "False", "True", "mn", "can", "can", "can", "can", "can"],  # 6
               ["True", "False", "True", "hr", "can", "can", "can", "n/a", "n/a"],  # 7
               ["True", "False", "True", "hr_mn", "n/a", "n/a", "n/a", "n/a", "n/a"],  # 8
               ["True", "False", "False", "em", "can", "can", "can", "n/a", "n/a"],  # 9
               ["True", "False", "False", "mn", "can", "can", "can", "can", "can"],  # 10
               ["True", "False", "False", "hr", "can", "can", "can", "n/a", "n/a"],  # 11
               ["True", "False", "False", "hr_mn", "n/a", "n/a", "n/a", "n/a", "n/a"],  # 12
               ["True", "True", "False", "em", "can", "can", "can", "n/a", "n/a"],  # 13
               ["True", "True", "False", "mn", "can", "can", "can", "can", "can"],  # 14
               ["True", "True", "False", "hr", "can", "can", "can", "n/a", "n/a"],  # 15
               ["True", "True", "False", "hr_mn", "n/a", "n/a", "n/a", "n/a", "n/a"],  # 16
               ["False", "False", "False", "em", "no_menu", "no_menu", "no_menu", "no_menu", "no_menu"],  # 17
               ["False", "False", "False", "mn", "cannot", "cannot", "cannot", "can", "can"],  # 18
               ["False", "False", "False", "hr", "no_menu", "no_menu", "no_menu", "no_menu", "no_menu"],  # 19
               ["False", "False", "False", "hr_mn", "cannot", "cannot", "cannot", "can", "can"],  # 20
               ["False", "False", "True", "em", "no_menu", "no_menu", "no_menu", "no_menu", "no_menu"],  # 21
               ["False", "False", "True", "mn", "cannot", "cannot", "cannot", "can", "can"],  # 22
               ["False", "False", "True", "hr", "can", "can", "can", "n/a", "n/a"],  # 23
               ["False", "False", "True", "hr_mn", "can", "can", "can", "can", "can"],  # 24
               ["False", "True", "False", "em", "no_menu", "no_menu", "no_menu", "no_menu", "no_menu"],  # 25
               ["False", "True", "False", "mn", "can", "can", "can", "can", "can"],  # 26
               ["False", "True", "False", "hr", "no_menu", "no_menu", "no_menu", "no_menu", "no_menu"],  # 27
               ["False", "True", "False", "hr_mn", "can", "can", "can", "can", "can"],  # 28
               ["False", "True", "True", "em", "no_menu", "no_menu", "no_menu", "no_menu", "no_menu"],  # 29
               ["False", "True", "True", "mn", "can", "can", "can", "can", "can"],  # 30
               ["False", "True", "True", "hr", "can", "can", "can", "n/a", "n/a"],  # 31
               ["False", "True", "True", "hr_mn", "can", "can", "can", "can", "can"]]  # 32


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    @staticmethod
    def tst_log():
        global ln, main_matrix, tst_counter
        tst_counter += 1
        text = "TC12180_" + str(tst_counter) + "_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        print(text + " : ",
              main_matrix[0][0], "=", main_matrix[ln][0] + ", ",                # for_em
              main_matrix[0][1], "=", main_matrix[ln][1] + ", ",                # for_mg
              main_matrix[0][2], "=", main_matrix[ln][2] + ", ",                # for_hr
              main_matrix[0][3], "=", main_matrix[ln][3] + ", ",                # role
              main_matrix[0][tst_type], "=", main_matrix[ln][tst_type] + " ...")  # assign_to
        return text

    def if_to_any_user(self, can):
        global tst_counter, users, ln
        user_name = users["em1"].split(".")[0]
        tst_str = self.tst_log()
        self.tst_login(users[main_matrix[ln][3]])

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
            self.tst_logout()

            # Login as a init user and notification delete
            self.tst_login(users[main_matrix[ln][3]])
            self.driver.find_element_by_id("e2e-desktop-notifications").click()
            self.driver.find_element_by_xpath("//*[@id='e2e-view-all-notifications']/a").click()
            self.driver.find_element_by_class_name("delete-notification").click()
            print("    Notificaten about Goal deleting deleted: - Ok")
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
        global tst_counter, users, ln, oi
        tst_str = self.tst_log()
        self.tst_login(users[main_matrix[ln][3]])

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
            self.tst_logout()

            # Login as a init user and notification delete
            self.tst_login(users[main_matrix[ln][3]])
            self.driver.find_element_by_id("e2e-desktop-notifications").click()
            self.driver.find_element_by_xpath("//*[@id='e2e-view-all-notifications']/a").click()
            self.driver.find_element_by_class_name("delete-notification").click()
            print("    Notification about Goal deleting deleted: - Ok")
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
        global tst_counter, users, ln
        tst_str = self.tst_log()
        self.tst_login(users[main_matrix[ln][3]])

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
            self.tst_logout()

            # Login as a init user and notification delete
            self.tst_login(users[main_matrix[ln][3]])
            self.driver.find_element_by_id("e2e-desktop-notifications").click()
            self.driver.find_element_by_xpath("//*[@id='e2e-view-all-notifications']/a").click()
            self.driver.find_element_by_class_name("delete-notification").click()
            print("    Notification about Goal deleting deleted: - Ok")
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
        global tst_counter, users, ln
        tst_str = self.tst_log()
        self.tst_login(users[main_matrix[ln][3]])

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

            if main_matrix[ln][3] == "mn":
                u = users["sub"]
            else:
                u = users["hr_mn_direct"]
            self.tst_login(u)
            self.tst_notifications(tst_str)
            self.tst_my_goals(tst_str)
            self.tst_logout()

            # Login as a init user and notification delete
            self.tst_login(users[main_matrix[ln][3]])
            self.driver.find_element_by_id("e2e-desktop-notifications").click()
            self.driver.find_element_by_xpath("//*[@id='e2e-view-all-notifications']/a").click()
            self.driver.find_element_by_class_name("delete-notification").click()
            print("    Notification about Goal deleting deleted: - Ok")
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
            self.tst_logout()

            # Login as a init user and notification delete
            self.tst_login(users["mn"])
            self.driver.find_element_by_id("e2e-desktop-notifications").click()
            self.driver.find_element_by_xpath("//*[@id='e2e-view-all-notifications']/a").click()
            self.driver.find_element_by_class_name("delete-notification").click()
            print("    Notificaten about Goal deleting deleted: - Ok")
        else:  # if cannot
            # if impossible to find
            self.driver.find_element_by_id("e2e-assign-goal").click()
            self.driver.find_element_by_id("Sendto:").send_keys(user_name)
            if len(self.driver.find_elements_by_class_name("found-item")) == 0:
                print("    Impossible to find: - Ok")
            else:
                print("!!!======== It is possible to find but should not! ========================================")
        self.tst_logout()

    def is_no_menu(self):
        global tst_counter, users, ln
        tst_str = self.tst_log()
        self.tst_login(users[main_matrix[ln][3]])
        # If No Assign Goal available in the menu
        if len(self.driver.find_elements_by_id("e2e-assign-goal")) == 0:
            print("    No Assign Goal menu: - Ok")
            self.tst_logout()
        else:
            print("!!!======== Assign Goal menu pesent but should not! ========================================")

    def tst_notifications(self, ttitle):
        self.driver.find_element_by_id("e2e-desktop-notifications").click()
        # print("    Notifications click: - Ok")
        if self.driver.find_elements_by_xpath("//*[@id='e2e-view-all-notifications']/a") == 0:
            print("!!!======== There are no notifications about Goal Assign! ========================================")
        else:
            self.driver.find_element_by_xpath("//*[@id='e2e-view-all-notifications']/a").click()
            nt_list = self.driver.find_elements_by_xpath("//*[text()='" + ttitle + "']")
            if len(nt_list) > 0:
                # print("    Notifications are present: - Ok")
                for i in nt_list:
                    self.driver.find_element_by_class_name("delete-notification").click()
                print("    Notifications found and has deleted: - Ok")
            else:
                print("!!!======== There are no notifications about Goal Assign! =====================================")

    def tst_my_goals(self, ttitle):
        wait10 = WebDriverWait(self.driver, 10)
        # Check in My Goalas
        self.driver.find_element_by_id("e2e-my-goals").click()
        if len(self.driver.find_elements_by_xpath("//h4[text()='" + ttitle + "']")) == 0:
            print("!!!======== There are no Goal in My Goals found! ========================================")
        else:
            while len(self.driver.find_elements_by_xpath("//h4[text()='" + ttitle + "']")) > 0:
                # self.driver.find_element_by_xpath("//h4[text()='" + ttitle + "']").click()
                str_xp = "//h4[text()='" + ttitle + "']"
                wait10.until(EC.element_to_be_clickable((By.XPATH, str_xp)))
                self.driver.find_element_by_xpath("//h4[text()='" + ttitle + "']").click()
                # self.driver.find_element_by_id("e2e-delete-button").click()
                wait10.until(EC.element_to_be_clickable((By.ID, 'e2e-delete-button')))
                self.driver.find_element_by_id("e2e-delete-button").click()
                wait10.until(EC.element_to_be_clickable((By.ID, 'e2e-yes-button')))
                self.driver.find_element_by_id("e2e-yes-button").click()
                # time.sleep(1)
                wait10.until(EC.element_to_be_clickable((By.ID, 'e2e-primary-button')))
                self.driver.find_element_by_id("e2e-primary-button").click()

            print("    Goal in MyGoals found and has deleted : - Ok")

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
        print("    Login as " + usr + ": - Ok")

    def is_ok(self, test_type, can):
        if main_matrix[0][test_type] == "any user":
            self.if_to_any_user(can)
        elif main_matrix[0][test_type] == "any OI":
            self.if_to_any_oi(can)
        elif main_matrix[0][test_type] == "all company":
            self.if_to_all_company(can)
        elif main_matrix[0][test_type] == "my direct reports":
            self.if_my_direct_reports(can)
        elif main_matrix[0][test_type] == "direct subordinate":
            self.if_direct_subordinate(can)
        else:
            print("Error in main_matrix!")

    def tst_logout(self):
        self.driver.find_element_by_id("e2e-user-profile").click()
        self.driver.find_element_by_id("e2e-dropdown-profile-logout").click()
        self.driver.find_element_by_id("e2e-yes-button").click()
        print("    Logout: - Ok")

    def tst_settings(self, em, mg, hr):
        global users
        changed = False
        wait10 = WebDriverWait(self.driver, 10)
        self.tst_login(users["admin"])
        #  self.tst_login("Barry.Deegan@email.com")
        wait10.until(EC.element_to_be_clickable((By.ID, 'e2e-system-administration')))
        self.driver.find_element_by_id("e2e-system-administration").click()
        wait10.until(EC.element_to_be_clickable((By.ID, 'e2e-manage-goals')))
        self.driver.find_element_by_id("e2e-manage-goals").click()
        if self.driver.find_element_by_id("GoalsSettings_EnableAllowEmployeeToAssignToEveryone").get_attribute("data-value") != em.lower():
            self.driver.find_element_by_id("GoalsSettings_EnableAllowEmployeeToAssignToEveryone").click()
            changed = True
        if self.driver.find_element_by_id("GoalsSettings_EnableAllowManagerToAssignToEveryone").get_attribute("data-value") != mg.lower():
            self.driver.find_element_by_id("GoalsSettings_EnableAllowManagerToAssignToEveryone").click()
            changed = True
        if self.driver.find_element_by_id("GoalsSettings_EnableAllowHRToAssignToEveryone").get_attribute("data-value") != hr.lower():
            self.driver.find_element_by_id("GoalsSettings_EnableAllowHRToAssignToEveryone").click()
            changed = True
        if changed:
            self.driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div[2]/div[12]/button').click()
            time.sleep(7)
        print("    Test settings: - Ok")
        self.tst_logout()

    def do_testing(self, line):
        global tst_type, tst_counter
        self.tst_settings(line[0], line[1], line[2])
        for tst_type in range(4, 9):
            if line[tst_type] == "can":
                self.is_ok(tst_type, True)
            elif line[tst_type] == "cannot":
                self.is_ok(tst_type, False)
            elif line[tst_type] == "no_menu":
                self.is_no_menu()
            else:
                self.tst_log()
                print("    Skiped...")

    def test_12180(self):
        global ln, url
        driver = self.driver
        driver.implicitly_wait(40)
        self.driver.get(url)

        for ln in range(18, len(main_matrix)+1):
            self.do_testing(main_matrix[ln])

        print("It's done!")

if __name__ == '__main__':
    unittest.main()
