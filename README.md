

<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">E2E test for Kong Gateway Service</h3>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
This is an end-to-end demo of testing project for Kong Gateway Service.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Considerations

- Each UI page is represented by a class in /test/pages, the class provide methods to perform actions in that page. Tests then use these methods whenever they need to interact with the UI of that page. If the UI changes for a page, the tests themselves don’t need to change, only the code within the page object needs to change. Subsequently, all changes to support that new UI are located in one place.
- Test cases are put in test_*.py file under /test/ui_tests/*. There are parameterized tests and also negative cases in test_gateway_service.py.
- Tests can be run against a local environment or a remote environment, it is controlled by an environment variable ENV_NAME, please set its value to be the block name in /test/env_config/default_env.ini; by default, it is set to "local"
- Tests can be run using different browsers, or using a headless or headed mode, they are also controlled by configurations in /test/env_config/default_env.ini
- After each test run, log files can be found in the root directory with a name pattern '%Y-%m-%d--%H_%M_%S'.log, e.g. 2024-06-21--15_03_17.log
- Step by step screenshots can be seen in trace.zip in the root directory after each run, please open it in https://trace.playwright.dev/, this can help with debugging failures
- Tests are naturally grouped by modules, they are also grouped by pytest markers, for example, you can run "pytest -m smoke" to filter all smoke tests to run
- For a beautiful test report, allure is integrated in GitHub Action, it can be found in https://GitHub.com/KimXie1984/kongtest/actions/workflows/pages/pages-build-deployment
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Assumptions

- Python, Pytest and Playwright is used for this project
- This is a fast demo with limited number of cases. If there are a lot of cases, and the execution takes very long time, .e.g several hours or more, we could use pytest-xdist to run tests in parallel to accelerate.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Prerequisites
1. Docker installed
2. Python installed
3. Pip installed
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation and Run locally
1. Clone the repo
   ```sh
   git clone https://GitHub.com/KimXie1984/kongtest.git
   ```
2. Change to the repo's root directory
3. Bring up Kong Services
   ```sh
   docker-compose up -d
   ```
3. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
4. Launch tests
   ```sh
   pytest
   ```
5. Shutdown Kong Gateway Services
   ```sh
   docker-compose down
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Trade-offs

- The GitHub Action of this repository uses 1 GitHub hosted runner for both setting up the Kong Service under test, and the test execution. In real world, we would separate test execution and product to different machines to avoid failure interference and assure resource usage.
- Kong-Gateway docker-compose.yml can be automatically downloaded from Google Drive for each CI run by using https://github.com/pew-actions/google-drive-download. Currently, this project uses the checked in docker-compose.yml in root directory.
- GitHub Action currently triggers a workflow run by "push" event of this repo. We can have small granularity control detailed conditions on MR such as with specific labels or special comments such as "@test".

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Kim Xie - [@linkedin](https://www.linkedin.com/in/kim-xie-44726a47/) - 58331308@qq.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>
