import sys
from fastmcp import FastMCP

mcp = FastMCP("Logs Server")

def _get_logs(repo: str) -> str:
    print(f"Fetching logs for repo: {repo}")
    if repo == "https://github.com/omar-baba/streamlit-error":
        return """
2025-04-06T21:34:09-04:00 Your publish request with ID da499f79-c89d-4d72-9e53-e710fdc4ee82 is now being processed.
2025-04-06T21:34:09-04:00 Quarto version was not provided. Using 1.6.42
2025-04-06T21:34:09-04:00 Loading your source code...
2025-04-06T21:34:09-04:00 From https://github.com/omar-baba/streamlit-error
2025-04-06T21:34:09-04:00  * branch            0a8257bb5530f0cbe12d5d88e85e42aa51696ae2 -> FETCH_HEAD
2025-04-06T21:34:09-04:00 HEAD is now at 0a8257b Update app.py
2025-04-06T21:34:10-04:00 Connect Cloud is providing all 38 required Python packages:
2025-04-06T21:34:10-04:00 altair==5.5.0, attrs==25.3.0, blinker==1.9.0, cachetools==5.5.2, certifi==2025.1.31
2025-04-06T21:34:10-04:00 charset-normalizer==3.4.1, click==8.1.8, gitdb==4.0.12, gitpython==3.1.44, idna==3.10
2025-04-06T21:34:10-04:00 jinja2==3.1.6, jsonschema==4.23.0, jsonschema-specifications==2024.10.1, markupsafe==3.0.2, narwhals==1.33.0
2025-04-06T21:34:10-04:00 numpy==2.2.4, packaging==24.2, pandas==2.2.3, pillow==11.1.0, protobuf==5.29.4
2025-04-06T21:34:10-04:00 pyarrow==19.0.1, pydeck==0.9.1, python-dateutil==2.9.0.post0, pytz==2025.2, referencing==0.36.2
2025-04-06T21:34:10-04:00 requests==2.32.3, rpds-py==0.24.0, setuptools==78.1.0, six==1.17.0, smmap==5.0.2
2025-04-06T21:34:10-04:00 streamlit==1.44.1, tenacity==9.1.2, toml==0.10.2, tornado==6.4.2, typing-extensions==4.13.1
2025-04-06T21:34:10-04:00 tzdata==2025.2, urllib3==2.3.0, watchdog==6.0.0
2025-04-06T21:34:10-04:00 Quarto version was not provided. Using 1.6.42
2025-04-06T21:34:10-04:00 Using Quarto version: 1.6.42
2025-04-06T21:34:10-04:00 Running on host: deployment-01960dce-31ba994f3552c2382169301fdfad3d1d-deplohv7t4
2025-04-06T21:34:10-04:00 Process ID: 389
2025-04-06T21:34:10-04:00 Running as user: uid=10002(connect) gid=10002(connect) groups=10002(connect)
2025-04-06T21:34:10-04:00 Connect version: 2025.03.0
2025-04-06T21:34:10-04:00 LANG: C.UTF-8
2025-04-06T21:34:10-04:00 Working directory: /cloud/project
2025-04-06T21:34:10-04:00 Bootstrapping environment using Python 3.12.7 (main, Feb 25 2025, 22:33:41) [GCC 11.4.0] at /cloud/lib/venv/bin/python3
2025-04-06T21:34:10-04:00 Running content using the current Python environment
2025-04-06T21:34:11-04:00
2025-04-06T21:34:11-04:00   You can now view your Streamlit app in your browser.
2025-04-06T21:34:11-04:00
2025-04-06T21:34:11-04:00   URL: http://01960dce-4713-5173-53d2-825044c25dcd.share.dev.connect.posit.cloud:80
2025-04-06T21:34:11-04:00
2025-04-06T21:34:22-04:00 2025-04-07 01:34:22.676 Uncaught app execution
2025-04-06T21:34:22-04:00 Traceback (most recent call last):
2025-04-06T21:34:22-04:00   File "/cloud/lib/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 121, in exec_func_with_error_handling
2025-04-06T21:34:22-04:00     result = func()
2025-04-06T21:34:22-04:00              ^^^^^^
2025-04-06T21:34:22-04:00   File "/cloud/lib/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 640, in code_to_exec
2025-04-06T21:34:22-04:00     exec(code, module.__dict__)
2025-04-06T21:34:22-04:00   File "/cloud/project/app.py", line 28, in <module>
2025-04-06T21:34:22-04:00     hist_values = np.histogram(data[DATE_COLUMN].dt, bins=24, range=(0,24))[0]
2025-04-06T21:34:22-04:00                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-06T21:34:22-04:00   File "/cloud/lib/venv/lib/python3.12/site-packages/numpy/lib/_histograms_impl.py", line 841, in histogram
2025-04-06T21:34:22-04:00     keep = (tmp_a >= first_edge)
2025-04-06T21:34:22-04:00             ^^^^^^^^^^^^^^^^^^^
2025-04-06T21:34:22-04:00 TypeError: '>=' not supported between instances of 'DatetimeProperties' and 'int'
2025-04-06T21:34:22-04:00 2025-04-07 01:34:22.676 Uncaught app execution
2025-04-06T21:34:22-04:00 Traceback (most recent call last):
2025-04-06T21:34:22-04:00   File "/cloud/lib/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 121, in exec_func_with_error_handling
2025-04-06T21:34:22-04:00     result = func()
2025-04-06T21:34:22-04:00              ^^^^^^
2025-04-06T21:34:22-04:00   File "/cloud/lib/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 640, in code_to_exec
2025-04-06T21:34:22-04:00     exec(code, module.__dict__)
2025-04-06T21:34:22-04:00   File "/cloud/project/app.py", line 28, in <module>
2025-04-06T21:34:22-04:00     hist_values = np.histogram(data[DATE_COLUMN].dt, bins=24, range=(0,24))[0]
2025-04-06T21:34:22-04:00                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-06T21:34:22-04:00   File "/cloud/lib/venv/lib/python3.12/site-packages/numpy/lib/_histograms_impl.py", line 841, in histogram
2025-04-06T21:34:22-04:00     keep = (tmp_a >= first_edge)
2025-04-06T21:34:22-04:00             ^^^^^^^^^^^^^^^^^^^
2025-04-06T21:34:22-04:00 TypeError: '>=' not supported between instances of 'DatetimeProperties' and 'int'    
    """
    return "Logs not found for this repo"

@mcp.tool()
def get_logs_for_repo(repo: str) -> str:
    return _get_logs(repo)


@mcp.resource("logs://{repo}")
def get_logs(repo: str) -> str:
    return _get_logs(repo)