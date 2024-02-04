import time
from pyats import aetest
import requests

# All ThousandEyes API endpoint url starts with this base url
BASE_URL = "https://api.thousandeyes.com/v7"

class CommonSetup(aetest.CommonSetup):
    '''
    Common setup tasks - this class is instantiated only once per testscript.
    '''
    test_id_list = []

    @aetest.subsection
    def create_TE_instant_tests(self, steps, token, agent, url_to_test_list):
        '''
        Creating and running the ThousandEyes instant tests to check SLA of selected
        URL list
        '''
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        api_endpoint = f"{BASE_URL}/tests/http-server/instant"

        with steps.start(
            "Creating ThousandEyes instant tests", continue_=True
            ) as step:

            for url_to_test in url_to_test_list:
                payload = {
                    "agents": [{"agentId": agent}],
                    "url": url_to_test
                }

                response = requests.post(api_endpoint, headers=headers, json=payload, timeout=30)
                if response.ok:
                    test_id = response.json()["testId"]
                    self.test_id_list.append(test_id)
                    step.passed()
                else:
                    print(response.text)
                    step.failed()

    @aetest.subsection
    def mark_tests_for_looping(self):
        '''
        Run the PerformanceTestCase with each of the generated instant tests.
        ThousandEyes creates one test for each of the URLs.
        '''
        aetest.loop.mark(PerformanceTestcase, test_id=self.test_id_list)

class PerformanceTestcase(aetest.Testcase):
    ''' Simple Testcase for checking performance of websites. '''

    metrics = {}

    @aetest.setup
    def retrieve_test_metrics(self, steps, token, test_id):
        '''
        Retrieve the test metrics of the instant test by using ThousandEyes API.
        '''
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        with steps.start(
            "Retrieving ThousandEyes performance metrics", continue_=True
            ) as step:

            for i in range (10):
                print(f"Trying to retrieve data ({i})...")
                api_endpoint = f"{BASE_URL}/test-results/{test_id}/http-server"

                response = requests.get(api_endpoint, headers=headers, timeout=30)

                data = response.json()

                if not data["results"]:
                    print("Results are not yet available.")
                    time.sleep(6)

                else:
                    self.metrics = {"url_to_test":{data['test']['url']}, "results": data['results'][0]}
                    step.passed(f"Metric retrieval for test {test_id} successful")

            step.failed(f"Couldn't retrieve metrics for {test_id}")

    @aetest.test
    def performance_test(self, steps):
        ''' Using the response from ThousandEyes tests, test for the appropriate quality of service. '''

        with steps.start(
            f"Validating total time for {self.metrics['url_to_test']}", continue_=True
        ) as step:

            threshold = 100 # This is the threshold for expected result

            try:
                total_time = self.metrics["results"]['totalTime']
                assert total_time < threshold

            except AssertionError: # Threshold is smaller than actual value
                step.failed(f"Total time {total_time}ms higher than threshold {threshold}ms")

            except KeyError: # total time is not included in the result - there is no connectivity
                error = self.metrics["results"]['errorDetails']
                step.failed(f"Connectivity issue: {error}")

            else:
                step.passed(f"Total time: {total_time}ms")

    @aetest.cleanup
    def cleanup(self):
        ''' No cleanup needed for this ThousandEyes testcase '''
        pass

if __name__ == "__main__":
    import os
    print(f"\n{'* '*15}*")
    print("* STARTING ThousandEyes TEST  *")
    print(f"{'* '*15}*\n")

    # Define your ThousandEyes API token
    api_key = os.getenv("TE_API_KEY")
    # Define your ThousandEyes agent
    agent = os.getenv("TE_AGENT")
    # Define the URLs to test
    my_urls = ("ciscolive.com","https://testdrive.sechnik.com")

    # Call the test with the api_key, urls that you want to test, and agent you want to use
    sla_test = aetest.main(
                            token=api_key,
                            url_to_test_list = my_urls,
                            agent = agent
                        )
